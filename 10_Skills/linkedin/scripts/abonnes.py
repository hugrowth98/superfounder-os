#!/usr/bin/env python3
"""abonnes.py : lit le nombre d'abonnes de chaque source de veille (page d'archive Substack, page "a propos" d'une
chaine YouTube) et l'ecrit dans 05_Departements/Marketing/Content-Brain/02_Veille/sources/veille-abonnes.json.
Sert a calculer la velocite dans veille.py. Cache de 30 jours : ne refait rien si le fichier est plus recent,
sauf avec --force.

Usage : python3 abonnes.py [--force]
Stdlib uniquement, aucun appel payant.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
DOSSIER = _racine / "05_Departements" / "Marketing" / "Content-Brain" / "02_Veille"
SOURCES_FILE = DOSSIER / "Sources-veille.json"
ABONNES_FILE = DOSSIER / "sources" / "veille-abonnes.json"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
TIMEOUT = 12
CACHE_JOURS = 30


def http_get(url: str, yt_cookie: bool = False) -> str:
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    if yt_cookie:
        headers["Cookie"] = "CONSENT=YES+"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def nombre(texte: str):
    """'146K', '1.2M', '23,000', '23 000' vers un entier."""
    t = texte.strip().replace(",", "").replace(" ", "").replace(" ", "")
    m = re.match(r"^([0-9.]+)([KMB]?)$", t, re.IGNORECASE)
    if not m:
        return None
    return int(float(m.group(1)) * {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[m.group(2).upper()])


def abonnes_newsletter(nom: str, feed_url: str) -> dict:
    if "/feed" not in feed_url:
        return {"nom": nom, "plateforme": "newsletters", "abonnes": None, "url": feed_url, "erreur": "pas une archive Substack, abonnes a saisir a la main dans le JSON"}
    archive = feed_url.replace("/feed", "/archive")
    try:
        html = http_get(archive)
        for pat in (r"Over\s+([0-9.,]+[KMB]?)\s+subscribers", r"([0-9.,]+[KMB]?)\s+subscribers", r"([0-9.,\s]+[KMB]?)\s+abonn"):
            m = re.search(pat, html)
            if m and nombre(m.group(1)):
                return {"nom": nom, "plateforme": "newsletters", "abonnes": nombre(m.group(1)), "url": archive}
        return {"nom": nom, "plateforme": "newsletters", "abonnes": None, "url": archive, "erreur": "nombre d'abonnes introuvable sur la page"}
    except Exception as e:
        return {"nom": nom, "plateforme": "newsletters", "abonnes": None, "url": archive, "erreur": str(e)}


def abonnes_youtube(handle: str) -> dict:
    about = f"https://www.youtube.com/@{handle.lstrip('@')}/about"
    try:
        html = http_get(about, yt_cookie=True)
        for pat in (r'"subscriberCountText":"([0-9.,]+[KMB]?)\s+subscribers?"', r'"subscriberCountText":"([0-9.,\s]+[KMB]?)\s+abonn'):
            m = re.search(pat, html)
            if m and nombre(m.group(1)):
                return {"nom": handle, "plateforme": "youtube", "abonnes": nombre(m.group(1)), "url": about}
        return {"nom": handle, "plateforme": "youtube", "abonnes": None, "url": about, "erreur": "nombre d'abonnes introuvable"}
    except Exception as e:
        return {"nom": handle, "plateforme": "youtube", "abonnes": None, "url": about, "erreur": str(e)}


def main():
    ap = argparse.ArgumentParser(description="Abonnes des sources de veille (cache 30 jours)")
    ap.add_argument("--force", action="store_true", help="rafraichir meme si le cache est recent")
    a = ap.parse_args()
    if not SOURCES_FILE.exists():
        sys.exit(f"ERREUR : {SOURCES_FILE} introuvable. Lancez \"Installe mon contenu\" ou creez le fichier.")
    existant = {}
    if ABONNES_FILE.exists():
        try:
            existant = json.loads(ABONNES_FILE.read_text(encoding="utf-8"))
        except Exception:
            existant = {}
    if not a.force and existant.get("maj"):
        try:
            age = datetime.now() - datetime.fromisoformat(existant["maj"])
            if age < timedelta(days=CACHE_JOURS):
                print(f"  [cache] veille-abonnes.json a jour ({age.days} jours), rien a faire ; --force pour rafraichir.", file=sys.stderr)
                return
        except Exception:
            pass
    sources = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    news = []
    for cat, bloc in (sources.get("newsletters") or {}).items():
        if cat.startswith("_") or not isinstance(bloc, dict):
            continue
        for f in bloc.get("flux", []) or []:
            if f.get("url"):
                news.append((f.get("nom") or f["url"], f["url"], f.get("abonnes")))
    for f in sources.get("autres_flux", []) or []:
        if isinstance(f, dict) and f.get("url"):
            news.append((f.get("nom") or f["url"], f["url"], f.get("abonnes")))
    chaines = []
    for k in ("tier_1", "tier_2", "tier_3"):
        chaines.extend(((sources.get("youtube") or {}).get(k) or {}).get("chaines", []) or [])
    print(f"  [lecture] {len(news)} newsletters, {len(chaines)} chaines YouTube...", file=sys.stderr)
    resultats, erreurs = {"newsletters": {}, "youtube": {}}, []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(abonnes_newsletter, n, u): (n, manuel) for n, u, manuel in news}
        for fut in as_completed(futs):
            r = fut.result(); n, manuel = futs[fut]
            if r.get("abonnes"):
                resultats["newsletters"][n] = {"abonnes": r["abonnes"], "url": r["url"]}
            elif manuel:
                resultats["newsletters"][n] = {"abonnes": int(manuel), "url": r["url"], "saisi": True}
            else:
                erreurs.append(f"{n} : {r.get('erreur', 'pas de donnee')} (ajoutez \"abonnes\": N dans Sources-veille.json)")
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(abonnes_youtube, h): h for h in chaines}
        for fut in as_completed(futs):
            r = fut.result()
            if r.get("abonnes"):
                resultats["youtube"][r["nom"]] = {"abonnes": r["abonnes"], "url": r["url"]}
            else:
                erreurs.append(f"{r['nom']} : {r.get('erreur', 'pas de donnee')}")
    ABONNES_FILE.parent.mkdir(parents=True, exist_ok=True)
    ABONNES_FILE.write_text(json.dumps({
        "maj": datetime.now().isoformat(timespec="seconds"),
        "stats": {"newsletters": len(resultats["newsletters"]), "youtube": len(resultats["youtube"]), "erreurs": len(erreurs)},
        "abonnes": resultats, "erreurs": erreurs,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [ecrit] {len(resultats['newsletters'])} newsletters, {len(resultats['youtube'])} chaines : {ABONNES_FILE}", file=sys.stderr)
    for e in erreurs:
        print(f"  [erreur] {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
