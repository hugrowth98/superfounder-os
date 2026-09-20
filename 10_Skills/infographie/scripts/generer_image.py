#!/usr/bin/env python3
"""generer_image : genere l'image d'une infographie a partir du prompt final d'un brief (ou d'un prompt donne), avec
OpenAI (gpt-image) ou fal.ai, et la range a cote du brief dans 05_Departements/Marketing/LinkedIn/.

Moteurs (--moteur) :
  openai   POST https://api.openai.com/v1/images/generations, modele gpt-image-2 (defaut) ou gpt-image-1 ; cle OPENAI_API_KEY
  fal      file d'attente fal.ai (https://queue.fal.run/<modele>), modele openai/gpt-image-2 (defaut), fal-ai/nano-banana-pro,
           fal-ai/ideogram/v3, ou tout autre ; cle FAL_KEY
Sans --moteur : openai si OPENAI_API_KEY est dans .env, fal si FAL_KEY, sinon arret (le prompt reste a coller dans un outil).

Le prompt vient de --brief <fichier.md> (le bloc "Prompt de generation", ou le dernier bloc de code) ou de --prompt-fichier <txt>
ou de --prompt "...". Le prompt utilise est ecrit a cote de l'image (.prompt.txt) pour la variante suivante.

Exemples :
  python3 generer_image.py --brief 05_Departements/Marketing/LinkedIn/Infographie-signaux_2026-09-20.md --dry-run
  python3 generer_image.py --brief <brief.md>                      (openai si la cle est la, sinon fal)
  python3 generer_image.py --brief <brief.md> --moteur fal --modele fal-ai/nano-banana-pro --resolution 2K
  python3 generer_image.py --brief <brief.md> --variante 2         (Infographie-..._v2.png)
  python3 generer_image.py --prompt "..." --format 1:1 --out visuel.png
Cout : selon le moteur, le modele, la taille et la qualite (quelques dizaines de centimes par image en qualite haute) ;
le script affiche le modele et la taille avant de lancer, et ne lance rien en --dry-run.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import afficher, arret, aujourd_hui, bandeau_dry_run, env, http, racine  # noqa: E402

FORMATS = {"4:5": (1024, 1280), "1:1": (1024, 1024), "3:2": (1536, 1024), "2:3": (1024, 1536), "16:9": (1536, 864), "9:16": (864, 1536)}
TAILLES_OPENAI = {"4:5": ["1024x1280", "1024x1536"], "1:1": ["1024x1024"], "3:2": ["1536x1024"], "2:3": ["1024x1536"],
                  "16:9": ["1536x1024"], "9:16": ["1024x1536"]}
DOSSIER_SORTIE = "05_Departements/Marketing/LinkedIn"


# ------------------------------------------------------------------ prompt

def prompt_depuis_brief(chemin: Path) -> str:
    """Le bloc 'Prompt de generation' d'un brief : le contenu du bloc de code qui suit ce titre, sinon le texte du titre au suivant,
    sinon le dernier bloc de code du fichier."""
    t = chemin.read_text(encoding="utf-8")
    m = re.search(r"^#{1,6}\s*(?:\d+\.\s*)?prompt[^\n]*\n(.*?)(?=^#{1,6}\s|\Z)", t, re.I | re.M | re.S)
    section = m.group(1) if m else ""
    code = re.findall(r"```[a-zA-Z]*\n(.*?)```", section, re.S)
    if code:
        return code[-1].strip()
    if section.strip():
        return section.strip()
    code = re.findall(r"```[a-zA-Z]*\n(.*?)```", t, re.S)
    if code:
        return code[-1].strip()
    arret(f"aucun bloc 'Prompt de generation' ni bloc de code dans {chemin}")


def sujet_depuis_brief(chemin: Path) -> str:
    m = re.match(r"Infographie-(.+?)_\d{4}-\d{2}-\d{2}", chemin.stem)
    return m.group(1) if m else chemin.stem


# ------------------------------------------------------------------ OpenAI

def via_openai(prompt: str, modele: str, fmt: str, qualite: str, dry_run: bool) -> bytes:
    tailles = TAILLES_OPENAI[fmt]
    if dry_run:
        bandeau_dry_run("OpenAI POST /v1/images/generations", [f"modele : {modele}", f"taille : {tailles[0]} (repli {tailles[-1]} si refusee)",
                                                              f"qualite : {qualite}", f"prompt : {len(prompt.split())} mots",
                                                              "cout : selon le modele, la taille et la qualite (voir la page de prix OpenAI)"])
        return b""
    cle = env("OPENAI_API_KEY", aide="Cle sur platform.openai.com, API keys ; a ecrire dans .env.")
    derniere = ""
    for taille in tailles:
        body = {"model": modele, "prompt": prompt, "n": 1, "size": taille, "quality": qualite}
        st, corps = http("POST", "https://api.openai.com/v1/images/generations",
                         headers={"Authorization": f"Bearer {cle}", "Content-Type": "application/json"}, json_body=body, timeout=300)
        if st == 200 and isinstance(corps, dict) and corps.get("data"):
            d = corps["data"][0]
            if d.get("b64_json"):
                afficher(f"  [openai] {modele}, {taille}, qualite {qualite}")
                return base64.b64decode(d["b64_json"])
            if d.get("url"):
                afficher(f"  [openai] {modele}, {taille} (telechargement)")
                return urllib.request.urlopen(d["url"], timeout=120).read()
        derniere = f"HTTP {st} : {str(corps)[:300]}"
        msg = str(corps).lower()
        if st == 400 and ("size" in msg or "taille" in msg) and taille != tailles[-1]:
            afficher(f"  [openai] taille {taille} refusee, essai {tailles[-1]}")
            continue
        break
    arret(f"OpenAI images : {derniere}")


# ------------------------------------------------------------------ fal.ai

def corps_fal(modele: str, prompt: str, fmt: str, qualite: str, resolution: str) -> dict:
    w, h = FORMATS[fmt]
    body = {"prompt": prompt, "num_images": 1, "output_format": "png"}
    if "nano-banana" in modele:
        body["aspect_ratio"] = fmt
        body["resolution"] = resolution
    else:
        body["image_size"] = {"width": w, "height": h}
        if "gpt-image" in modele:
            body["quality"] = qualite
    return body


def via_fal(prompt: str, modele: str, fmt: str, qualite: str, resolution: str, dry_run: bool) -> bytes:
    body = corps_fal(modele, prompt, fmt, qualite, resolution)
    if dry_run:
        bandeau_dry_run(f"fal.ai POST https://queue.fal.run/{modele}", [f"corps : {json.dumps({k: v for k, v in body.items() if k != 'prompt'}, ensure_ascii=False)}",
                                                                          f"prompt : {len(prompt.split())} mots",
                                                                          "cout : selon le modele (voir la page du modele sur fal.ai)"])
        return b""
    cle = env("FAL_KEY", aide="Cle sur fal.ai, Settings, API keys ; a ecrire dans .env.")
    h = {"Authorization": f"Key {cle}", "Content-Type": "application/json"}
    st, corps = http("POST", f"https://queue.fal.run/{modele}", headers=h, json_body=body, timeout=60)
    if st >= 400 or not isinstance(corps, dict):
        arret(f"fal.ai : HTTP {st} : {str(corps)[:300]}")
    status_url, response_url = corps.get("status_url"), corps.get("response_url")
    if not status_url:
        arret(f"fal.ai : reponse sans status_url : {str(corps)[:300]}")
    debut = time.time()
    while time.time() - debut < 600:
        st, s = http("GET", status_url, headers=h, timeout=60)
        statut = (s or {}).get("status") if isinstance(s, dict) else ""
        if statut == "COMPLETED":
            break
        if st >= 400:
            arret(f"fal.ai statut : HTTP {st} : {str(s)[:200]}")
        time.sleep(3)
    else:
        arret("fal.ai : pas de resultat en 10 minutes")
    st, res = http("GET", response_url, headers=h, timeout=120)
    images = (res or {}).get("images") if isinstance(res, dict) else None
    if not images:
        arret(f"fal.ai : pas d'image dans la reponse : {str(res)[:300]}")
    url = images[0].get("url")
    afficher(f"  [fal] {modele}, {images[0].get('width')}x{images[0].get('height')}")
    return urllib.request.urlopen(url, timeout=120).read()


# ------------------------------------------------------------------ main

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--brief", help="le brief Infographie-<sujet>_<date>.md : son bloc Prompt de generation")
    src.add_argument("--prompt-fichier", help="un fichier texte contenant le prompt")
    src.add_argument("--prompt", help="le prompt en ligne de commande")
    ap.add_argument("--moteur", choices=["openai", "fal"], help="defaut : openai si OPENAI_API_KEY, sinon fal si FAL_KEY")
    ap.add_argument("--modele", help="openai : gpt-image-2 (defaut), gpt-image-1 ; fal : openai/gpt-image-2 (defaut), fal-ai/nano-banana-pro, fal-ai/ideogram/v3...")
    ap.add_argument("--format", default="4:5", choices=sorted(FORMATS), help="ratio de l'image (defaut 4:5)")
    ap.add_argument("--qualite", default="high", choices=["auto", "low", "medium", "high"], help="gpt-image : qualite (defaut high)")
    ap.add_argument("--resolution", default="2K", choices=["1K", "2K", "4K"], help="nano-banana : resolution (defaut 2K)")
    ap.add_argument("--variante", type=int, help="numero de variante : suffixe _v<N> sur le nom de l'image")
    ap.add_argument("--sujet", help="sujet pour le nom du fichier (defaut : celui du brief)")
    ap.add_argument("--out", help="chemin PNG de sortie (defaut : a cote du brief, ou 05_Departements/Marketing/LinkedIn/)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.brief:
        brief = Path(a.brief)
        if not brief.exists():
            arret(f"brief introuvable : {brief}")
        prompt = prompt_depuis_brief(brief)
        sujet = a.sujet or sujet_depuis_brief(brief)
        dossier = brief.parent
    else:
        prompt = Path(a.prompt_fichier).read_text(encoding="utf-8").strip() if a.prompt_fichier else a.prompt.strip()
        sujet = a.sujet or "visuel"
        dossier = racine() / DOSSIER_SORTIE
    if len(prompt.split()) < 40:
        afficher("  [attention] prompt court (moins de 40 mots) : un prompt d'infographie fait 300 a 900 mots avec le texte exact")

    moteur = a.moteur
    if not moteur:
        if env("OPENAI_API_KEY", obligatoire=False):
            moteur = "openai"
        elif env("FAL_KEY", obligatoire=False):
            moteur = "fal"
        elif a.dry_run:
            moteur = "openai"
            afficher("  [moteur] aucune cle dans .env : dry-run sur openai ; au vrai run, ecrivez OPENAI_API_KEY ou FAL_KEY (verifier_connexions.py --set CLE=valeur)")
        else:
            arret("aucune cle : OPENAI_API_KEY ou FAL_KEY dans .env (verifier_connexions.py --set CLE=valeur), ou collez le prompt dans l'outil d'image de votre client")
        if env("OPENAI_API_KEY", obligatoire=False) or env("FAL_KEY", obligatoire=False):
            afficher(f"  [moteur] {moteur} (d'apres les cles du .env)")
    modele = a.modele or ("gpt-image-2" if moteur == "openai" else "openai/gpt-image-2")

    if a.out:
        sortie = Path(a.out)
    else:
        dossier.mkdir(parents=True, exist_ok=True)
        nom = f"Infographie-{sujet}_{aujourd_hui()}" + (f"_v{a.variante}" if a.variante else "")
        sortie = dossier / f"{nom}.png"
    afficher(f"  [sortie] {sortie}")

    donnees = via_openai(prompt, modele, a.format, a.qualite, a.dry_run) if moteur == "openai" else via_fal(prompt, modele, a.format, a.qualite, a.resolution, a.dry_run)
    if a.dry_run:
        return
    sortie.write_bytes(donnees)
    sortie.with_suffix(".prompt.txt").write_text(f"# {moteur} {modele} {a.format} {aujourd_hui()}\n\n{prompt}\n", encoding="utf-8")
    afficher(f"image ecrite ({len(donnees) // 1024} Ko) -> {sortie} ; prompt utilise -> {sortie.with_suffix('.prompt.txt')}")


if __name__ == "__main__":
    main()
