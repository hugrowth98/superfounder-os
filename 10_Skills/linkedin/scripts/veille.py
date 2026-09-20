#!/usr/bin/env python3
"""veille.py : lit les sources de veille de l'utilisateur (newsletters RSS, chaines YouTube, autres flux), recupere
likes, vues et abonnes, calcule une velocite par item, et ecrit le dump de la semaine dans
05_Departements/Marketing/LinkedIn/sources/veille_AAAA-MM-JJ.json (ou --format md pour un digest lisible).

Sources : 05_Departements/Marketing/LinkedIn/sources-veille.json (rempli par installer-contenu, ou a la main).
Abonnes : 05_Departements/Marketing/LinkedIn/sources/veille-abonnes.json (abonnes.py, une fois par mois).
Transcripts YouTube : bibliotheque youtube-transcript-api si elle est installee (pip3 install youtube-transcript-api),
sinon le script continue sans et le dit.

Usage :
  python3 veille.py [--jours 7] [--source newsletters|youtube|toutes] [--tier 1|2|3|tous]
                    [--sans-transcripts] [--contenu-complet] [--format json|md] [--out fichier] [--stdout]

Stdlib uniquement (la bibliotheque de transcripts est optionnelle). Aucun appel payant : flux et pages publics.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from html import unescape
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
DOSSIER = _racine / "05_Departements" / "Marketing" / "LinkedIn"
SOURCES_FILE = DOSSIER / "sources-veille.json"
CACHE_DIR = DOSSIER / "sources"
ABONNES_FILE = CACHE_DIR / "veille-abonnes.json"
CHAINES_FILE = CACHE_DIR / "veille-chaines.json"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
YOUTUBE_COOKIE = "CONSENT=YES+"
TIMEOUT = 15
PAYWALL_MARKERS_TAIL = ["read more", "continue reading", "subscribe to read", "subscribe to continue", "upgrade to paid",
                        "lire la suite", "abonnez-vous pour lire"]


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def http_get(url: str, timeout: int = TIMEOUT, yt_cookie: bool = False) -> bytes:
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
    if yt_cookie:
        headers["Cookie"] = YOUTUBE_COOKIE
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def strip_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"<figure.*?</figure>", "", html, flags=re.DOTALL)
    text = re.sub(r"<picture.*?</picture>", "", text, flags=re.DOTALL)
    text = re.sub(r"<img[^>]*>", "", text)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def detect_paywall(content: str) -> bool:
    if not content:
        return False
    tail = content[-200:].lower()
    return any(m in tail for m in PAYWALL_MARKERS_TAIL)


def parse_pubdate(s: str):
    if not s:
        return None
    s = s.strip()
    for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M %Z"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# ------------------------------------------------------------------ sources

def charger_sources() -> dict:
    if not SOURCES_FILE.exists():
        sys.exit(f"ERREUR : {SOURCES_FILE} introuvable. Lancez \"Installe mon contenu\" ou creez le fichier (voir le sous-skill veille).")
    try:
        return json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"ERREUR : {SOURCES_FILE} n'est pas un JSON valide : {e}")


def flux_newsletters(sources: dict) -> list:
    """[(nom, url, tags, tier)] pour chaque flux de newsletter, toutes categories confondues."""
    out = []
    for categorie, bloc in (sources.get("newsletters") or {}).items():
        if categorie.startswith("_") or not isinstance(bloc, dict):
            continue
        for f in bloc.get("flux", []) or []:
            if f.get("url"):
                out.append((f.get("nom") or f["url"], f["url"], f.get("tags", []), bloc.get("tier", 1)))
    for f in sources.get("autres_flux", []) or []:
        if isinstance(f, dict) and f.get("url"):
            out.append((f.get("nom") or f["url"], f["url"], f.get("tags", []), f.get("tier", 1)))
    return out


def handles_youtube(sources: dict, tier: str) -> list:
    yt = sources.get("youtube") or {}
    cles = ["tier_1", "tier_2", "tier_3"] if tier == "tous" else [f"tier_{tier}"]
    out = []
    for k in cles:
        bloc = yt.get(k)
        if isinstance(bloc, dict):
            out.extend(h for h in bloc.get("chaines", []) or [] if isinstance(h, str) and h.strip())
    return out


# ------------------------------------------------------------------ newsletters

def stats_archive_substack(feed_url: str) -> dict:
    """Likes, commentaires, partages par URL d'article, lus sur la page d'archive (Substack). Vide pour un autre flux."""
    if "/feed" not in feed_url:
        return {}
    archive_url = feed_url.replace("/feed", "/archive")
    try:
        html = http_get(archive_url).decode("utf-8", errors="ignore")
    except Exception:
        return {}
    # les liens peuvent porter un domaine personnalise (autre que substack.com) : on prend tout href qui contient /p/
    urls = re.findall(r'href="(https?://[^"]*?/p/[^"]+?)"', html)
    vus, uniques = set(), []
    for u in urls:
        c = u.split("?")[0].rstrip("/")
        if "/comments" in c or c in vus:
            continue
        vus.add(c); uniques.append(c)
    stats = {}
    for url in uniques:
        idx = html.find(url)
        if idx == -1:
            continue
        nums = re.findall(r">([0-9]+)<", html[idx:idx + 3500])
        if len(nums) >= 2:
            # cle par slug (/p/xxx) : les liens du flux peuvent porter un domaine personnalise
            stats[slug(url)] = {"likes": int(nums[0]), "commentaires": int(nums[1]), "partages": int(nums[2]) if len(nums) >= 3 else 0}
    return stats


def slug(url: str) -> str:
    m = re.search(r"/p/([^/?#]+)", url)
    return m.group(1) if m else url.split("?")[0].rstrip("/")


def velocite(engagement: int, abonnes: int, age_jours: float) -> dict:
    if not abonnes or abonnes <= 0:
        return {"taux": None, "velocite": None}
    taux = (engagement / abonnes) * 1000
    return {"taux": round(taux, 3), "velocite": round(taux / max(0.5, age_jours), 3)}


def lire_flux_rss(nom: str, url: str, cutoff: datetime, tags: list, tier: int, stats: dict, abonnes: int) -> list:
    try:
        xml_data = http_get(url)
    except Exception as e:
        return [{"_erreur": f"{nom}: {e}", "source": nom}]
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        return [{"_erreur": f"{nom}: flux illisible ({e})", "source": nom}]
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    atom = "{http://www.w3.org/2005/Atom}"
    items, now = [], datetime.now(timezone.utc)
    entries = list(root.iter("item")) or list(root.iter(f"{atom}entry"))
    for it in entries:
        if it.tag == f"{atom}entry":
            title = (it.findtext(f"{atom}title") or "").strip()
            link_el = it.find(f"{atom}link"); link = (link_el.get("href") if link_el is not None else "") or ""
            desc = (it.findtext(f"{atom}summary") or "").strip()
            pub_dt = parse_pubdate(it.findtext(f"{atom}published") or it.findtext(f"{atom}updated") or "")
            content_raw = it.findtext(f"{atom}content") or desc
        else:
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            desc = (it.findtext("description") or "").strip()
            pub_dt = parse_pubdate(it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date") or "")
            c = it.find("content:encoded", ns)
            content_raw = c.text if c is not None and c.text else desc
        if pub_dt and pub_dt < cutoff:
            continue
        contenu = strip_html(content_raw)
        st = (stats.get(slug(link)) or {}) if stats else {}
        age = (now - pub_dt).total_seconds() / 86400 if pub_dt else None
        eng = velocite(st["likes"], abonnes, age) if st and abonnes and age is not None else {}
        items.append({
            "source": nom, "type": "newsletter", "tier": tier, "titre": title, "lien": link,
            "date": pub_dt.strftime("%Y-%m-%d") if pub_dt else "?", "age_jours": round(age, 1) if age is not None else None,
            "resume": strip_html(desc)[:300], "contenu": contenu, "mots": len(contenu.split()),
            "paywall": detect_paywall(contenu), "tags": tags or [], "abonnes": abonnes,
            "likes": st.get("likes"), "commentaires": st.get("commentaires"), "partages": st.get("partages"),
            "taux": eng.get("taux"), "velocite": eng.get("velocite"),
        })
    return items


def collecter_newsletters(sources: dict, cutoff: datetime, abonnes_map: dict, workers: int = 10) -> list:
    flux = flux_newsletters(sources)
    stats_par_flux = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(stats_archive_substack, u): n for n, u, t, tier in flux}
        for fut in as_completed(futs):
            try:
                stats_par_flux[futs[fut]] = fut.result()
            except Exception:
                stats_par_flux[futs[fut]] = {}
    out = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(lire_flux_rss, n, u, cutoff, t, tier, stats_par_flux.get(n, {}), abonnes_map.get(n)): n for n, u, t, tier in flux}
        for fut in as_completed(futs):
            out.extend(fut.result())
    return out


# ------------------------------------------------------------------ youtube

def charger_json(p: Path) -> dict:
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def resoudre_chaine(handle: str, cache: dict):
    if cache.get(handle):
        return cache[handle]
    h = handle.lstrip("@")
    try:
        html = http_get(f"https://www.youtube.com/@{h}", timeout=10, yt_cookie=True).decode("utf-8", errors="ignore")
        for pat in (r"youtube\.com/channel/(UC[A-Za-z0-9_-]{22})", r'"channelId":"(UC[A-Za-z0-9_-]{22})"', r'"externalId":"(UC[A-Za-z0-9_-]{22})"'):
            m = re.search(pat, html)
            if m:
                cache[handle] = m.group(1)
                return m.group(1)
    except Exception:
        pass
    cache[handle] = None
    return None


def transcript_youtube(video_url: str):
    """Le transcript par la bibliotheque youtube-transcript-api, ou None (absente, video sans sous-titres, erreur)."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except ImportError:
        return None
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})", video_url)
    if not m:
        return None
    try:
        api = YouTubeTranscriptApi()
        try:
            res = api.fetch(m.group(1), languages=["fr", "en"])
        except Exception:
            res = api.fetch(m.group(1))
        return " ".join(seg.text for seg in res) or None
    except Exception:
        return None


def bibliotheque_transcripts() -> bool:
    try:
        import youtube_transcript_api  # noqa: F401
        return True
    except ImportError:
        return False


def lire_flux_youtube(handle: str, channel_id: str, cutoff: datetime, abonnes: int, tier: int) -> list:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        xml_data = http_get(url)
    except Exception as e:
        return [{"_erreur": f"{handle}: {e}", "source": handle}]
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        return [{"_erreur": f"{handle}: flux illisible ({e})", "source": handle}]
    atom, media = "{http://www.w3.org/2005/Atom}", "{http://search.yahoo.com/mrss/}"
    items, now = [], datetime.now(timezone.utc)
    for entry in root.iter(f"{atom}entry"):
        title = (entry.findtext(f"{atom}title") or "").strip()
        link_el = entry.find(f"{atom}link"); link = (link_el.get("href") if link_el is not None else "") or ""
        pub_dt = parse_pubdate(entry.findtext(f"{atom}published") or "")
        if pub_dt and pub_dt < cutoff:
            continue
        grp = entry.find(f"{media}group")
        desc = ""
        if grp is not None:
            d = grp.find(f"{media}description"); desc = (d.text or "").strip() if d is not None else ""
        vues = None
        st = entry.find(f".//{media}statistics")
        if st is not None:
            try:
                vues = int(st.get("views", 0))
            except (TypeError, ValueError):
                vues = None
        age = (now - pub_dt).total_seconds() / 86400 if pub_dt else None
        eng = velocite(vues, abonnes, age) if vues and abonnes and age is not None else {}
        items.append({
            "source": handle, "type": "youtube", "tier": tier, "titre": title, "lien": link,
            "date": pub_dt.strftime("%Y-%m-%d") if pub_dt else "?", "age_jours": round(age, 1) if age is not None else None,
            "resume": desc[:300], "contenu": desc, "mots": len(desc.split()), "paywall": False, "tags": ["youtube"],
            "abonnes": abonnes, "vues": vues, "taux": eng.get("taux"), "velocite": eng.get("velocite"),
        })
    return items


def collecter_youtube(sources: dict, cutoff: datetime, tier: str, abonnes_map: dict, transcripts: bool, workers: int = 10) -> list:
    cache = charger_json(CHAINES_FILE)
    yt = sources.get("youtube") or {}
    tiers = {}
    for k in ("tier_1", "tier_2", "tier_3"):
        for h in (yt.get(k) or {}).get("chaines", []) or []:
            tiers[h] = int(k[-1])
    handles = handles_youtube(sources, tier)
    resolus = []
    for h in handles:
        cid = resoudre_chaine(h, cache)
        if cid:
            resolus.append((h, cid))
        else:
            log(f"  [youtube] chaine introuvable : {h}")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CHAINES_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
    out = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(lire_flux_youtube, h, cid, cutoff, abonnes_map.get(h), tiers.get(h, 1)): h for h, cid in resolus}
        for fut in as_completed(futs):
            out.extend(fut.result())
    videos = [it for it in out if it.get("type") == "youtube" and it.get("lien")]
    if transcripts and videos:
        if not bibliotheque_transcripts():
            log("  [transcripts] bibliotheque youtube-transcript-api absente : pas de transcripts (pip3 install youtube-transcript-api)")
        else:
            log(f"  [transcripts] {len(videos)} videos...")
            with ThreadPoolExecutor(max_workers=4) as ex:
                futs = {ex.submit(transcript_youtube, it["lien"]): it for it in videos}
                for fut in as_completed(futs):
                    try:
                        futs[fut]["transcript"] = fut.result()
                    except Exception:
                        futs[fut]["transcript"] = None
    return out


# ------------------------------------------------------------------ abonnes, rendu

def charger_abonnes() -> dict:
    data = charger_json(ABONNES_FILE)
    flat = {}
    for bloc in (data.get("abonnes") or {}).values():
        for nom, info in bloc.items():
            flat[nom] = info.get("abonnes")
    return flat


def fmt_num(n):
    if n is None:
        return "?"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def rendu_markdown(items: list, jours: int) -> str:
    items = [it for it in items if "_erreur" not in it]
    def cle(it):
        v = it.get("velocite"); return v if v is not None else -1
    news = sorted([it for it in items if it["type"] == "newsletter"], key=cle, reverse=True)
    videos = sorted([it for it in items if it["type"] == "youtube"], key=cle, reverse=True)
    out = [f"# Veille brute, derniers {jours} jours (triee par velocite)", "",
           f"{len(news)} articles, {len(videos)} videos, genere le {datetime.now().strftime('%Y-%m-%d %H:%M')}. "
           "Velocite = engagement pour 1 000 abonnes par jour (likes des newsletters, vues des videos).", ""]
    for titre, liste in (("Newsletters", news), ("YouTube", videos)):
        if not liste:
            continue
        out += [f"## {titre}", ""]
        for it in liste:
            v = it.get("velocite")
            marque = "[fort]" if v and v >= 30 else ("[chaud]" if v and v >= 5 else "")
            age = f"{it['age_jours']}j" if it.get("age_jours") is not None else "?"
            out.append(f"### {marque} [{it['date']}] {it['source']} : {it['titre']}{' (paywall)' if it.get('paywall') else ''}")
            stats = []
            for k, lab in (("likes", "likes"), ("commentaires", "commentaires"), ("vues", "vues"), ("abonnes", "abonnes")):
                if it.get(k) is not None:
                    stats.append(f"{fmt_num(it[k])} {lab}")
            stats.append(age)
            if v is not None:
                stats.append(f"velocite {v:.1f}/jour")
            stats.append(f"{it['mots']} mots")
            out.append(f"- {', '.join(stats)}, [lien]({it['lien']})")
            if it.get("resume"):
                out.append(f"- {it['resume'][:200]}")
            out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Veille : flux RSS des newsletters, chaines YouTube, velocite, dump JSON")
    ap.add_argument("--jours", type=int, default=7, help="fenetre de fraicheur en jours (defaut 7)")
    ap.add_argument("--source", choices=["newsletters", "youtube", "toutes"], default="toutes")
    ap.add_argument("--tier", default="1", choices=["1", "2", "3", "tous"], help="priorite des chaines YouTube (defaut 1)")
    ap.add_argument("--sans-transcripts", action="store_true", help="ne pas chercher les transcripts YouTube")
    ap.add_argument("--contenu-complet", action="store_true", help="texte integral (sinon extrait de 1 500 caracteres)")
    ap.add_argument("--format", choices=["json", "md"], default="json")
    ap.add_argument("--out", help="fichier de sortie (defaut : sources/veille_AAAA-MM-JJ.json ou .md)")
    ap.add_argument("--stdout", action="store_true", help="ecrire sur la sortie standard au lieu d'un fichier")
    a = ap.parse_args()

    sources = charger_sources()
    abonnes_map = charger_abonnes()
    if not abonnes_map:
        log("  [abonnes] veille-abonnes.json absent : pas de velocite. Lancez abonnes.py une fois.")
    cutoff = datetime.now(timezone.utc) - timedelta(days=a.jours)
    items = []
    if a.source in ("newsletters", "toutes"):
        items.extend(collecter_newsletters(sources, cutoff, abonnes_map))
    if a.source in ("youtube", "toutes"):
        items.extend(collecter_youtube(sources, cutoff, a.tier, abonnes_map, transcripts=not a.sans_transcripts))
    if not a.contenu_complet:
        for it in items:
            if len(it.get("contenu") or "") > 1500:
                it["extrait"] = it["contenu"][:1500]; del it["contenu"]
    items.sort(key=lambda x: x.get("date", ""), reverse=True)

    texte = rendu_markdown(items, a.jours) if a.format == "md" else json.dumps(items, ensure_ascii=False, indent=2)
    erreurs = [it for it in items if "_erreur" in it]
    valides = [it for it in items if "_erreur" not in it]
    if a.stdout:
        print(texte)
    else:
        out = Path(a.out) if a.out else CACHE_DIR / f"veille_{datetime.now().strftime('%Y-%m-%d')}.{a.format}"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(texte, encoding="utf-8")
        log(f"  [sortie] {out}")
    log(f"  [stats] {len(valides)} items ({sum(1 for i in valides if i['type']=='newsletter')} articles, "
        f"{sum(1 for i in valides if i['type']=='youtube')} videos), {len(erreurs)} erreurs, fenetre {a.jours} jours")
    for e in erreurs:
        log(f"  [erreur] {e['_erreur']}")


if __name__ == "__main__":
    main()
