#!/usr/bin/env python3
"""veille_createurs.py : les posts qui ont performe chez des comptes LinkedIn choisis par l'utilisateur,
sur la fenetre S-6 a S-2, classes en quatre categories (20 educationnels, 20 lead magnets, 10 hot takes,
10 storytelling), avec les visuels telecharges et un rapport HTML ou chaque post a sa vignette.

Comptes : passes sur la ligne de commande (`--comptes <url> <url>`), ou lus dans un fichier texte (une URL
par ligne, `--fichier`), ou dans 05_Departements/Marketing/LinkedIn/comptes-veille.json si l'utilisateur a
choisi de les memoriser. Aucune liste n'est livree avec le skill : c'est l'utilisateur qui dit qui il suit.

Usage :
  python3 veille_createurs.py --comptes URL [URL ...] [--fin AAAA-MM-JJ] [--dry-run]
  python3 veille_createurs.py --fichier comptes.txt
  python3 veille_createurs.py --memorises                     (comptes-veille.json)
  python3 veille_createurs.py --reconstruire <dossier du run>  (apres avoir edite verdicts.json)

Apify : actor harvestapi/linkedin-profile-posts, 0,002 $ par post, 40 posts par compte au plus.
Sortie : 05_Departements/Marketing/LinkedIn/sources/veille-createurs_<debut>_<fin>/ (rapport.html, top.json,
posts.json, verdicts.json, images/). Ce dossier est ignore par git (donnees de l'utilisateur).
"""
from __future__ import annotations

import argparse
import collections
import datetime
import json
import re
import shutil
import statistics
import subprocess
import sys
import urllib.parse
import urllib.request
from html import escape
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from apify_run import lancer, prix  # noqa: E402
from gtm_common import afficher, arret  # noqa: E402

DOSSIER = _racine / "05_Departements" / "Marketing" / "LinkedIn"
COMPTES_FILE = DOSSIER / "comptes-veille.json"
ACTOR = "harvestapi/linkedin-profile-posts"
QUOTAS = {"EDU": 20, "LM": 20, "HOT": 10, "STORY": 10}
CAP_PAR_AUTEUR = 3
MAX_POSTS = 40
CATEGORIES = {
    "EDU": ("Éducationnel", "Le post enseigne quelque chose sans rien donner à télécharger."),
    "LM": ("Lead magnet", "Une ressource récupérable est offerte, contre un commentaire, un DM ou via un lien en clair."),
    "HOT": ("Hot take", "Une opinion tranchée, contrariante, sans ressource offerte."),
    "STORY": ("Storytelling", "Un récit à la première personne, avec un avant et un après."),
}

# ---------------------------------------------------------------- motifs (filet large, jamais le dernier mot)
GATE = [r"\bcomment\s+[\"“']?[A-Za-zÀ-ÿ0-9]{2,20}[\"”']?\s*(below|and i|to get|for the|pour)",
        r"\bcommente[rz]?\s+[\"“']?[A-Za-zÀ-ÿ0-9]{2,20}", r"\b(dm|mp)\s+me\b", r"\benvoie[- ]moi\b",
        r"\bsend me\b", r"\bi'?ll send (you|it|the)\b", r"\bje (t'|vous )?(l')?envoie\b",
        r"\bdrop\s+[\"“']?\w+[\"”']?\s+(in the comments|below)\b", r"\blien en (commentaire|bio)\b",
        r"\blink in (the )?(comments|bio)\b",
        r"\b(commentaire|comments?)\b.{0,30}\b(guide|template|playbook|checklist|pack|kit|notion|prompt|système|system)\b"]
GIVE = [r"\b(download|grab|steal|swipe|copy)\s+(it|them|the|this|all|my|your)\b", r"\bgiving (you|it|them|away)\b",
        r"\bi'?m giving\b", r"\bje (te|vous) (le |la |les )?(donne|offre|partage|envoie)\b", r"\bje (t'|vous )offre\b",
        r"\bit'?s (all )?(free|yours)\b", r"\byours,? (for )?free\b", r"\btout est gratuit\b",
        r"\b(get|access|take) (it|them|the \w+)\s+(for )?free\b", r"\bhere \(for free\)\b",
        r"\b(free|gratuit(e|es|s)?)\s+(guide|template|playbook|checklist|kit|repo|library|ressource|course|cours)\b",
        r"\b(guide|template|playbook|checklist|kit|repo|ressource|cours)\s+(complet\s+)?(gratuit|offert)\b",
        r"\b(lien|link)\s*(ci-dessous|below|in bio|dans la bio)\b", r"\bfor free\)?:",
        r"\bacc[eè]s gratuit\b", r"\bgratuit(ement)?\s*!?\s*(\U0001F447|↓)"]
ASSET = r"\b(guide|template|playbook|checklist|cheat ?sheet|swipe file|prompts?|framework|notion|workflow|toolkit|kit|ebook|pdf|doc|système|systeme|blueprint|script|sop|skills?|repo|library|course|cours)\b"
BARE_LINK = re.compile(r"\b[a-z0-9][a-z0-9-]{2,}\.(com|io|ai|co|guide|free|so|app|dev|net|org|fr)\b(?!\S*@)", re.I)
EDU = [r"\bhere'?s how\b", r"\bstep[- ]by[- ]step\b", r"\bhow to\b", r"\bvoici comment\b",
       r"\b\d+\s+(steps?|étapes?|etapes?|ways?|tips?|astuces?|erreurs?|mistakes?|lessons?|leçons|tools?|outils)\b",
       r"\bprompt\s*:", r"\btuto(riel)?\b", r"\bexemple\b", r"\bexample\b", r"\bstop doing\b", r"\bméthode|method\b",
       r"\bframework\b", r"\bplaybook\b", r"\bvs\.?\b", r"\btakeaways?\b"]
HOT = [r"\bunpopular opinion\b", r"\bhot take\b", r"\bcontroversial\b", r"\bopinion impopulaire\b",
       r"\bis (dead|a lie|a scam|a trap|overrated|broken)\b", r"\best (mort|un mensonge|une arnaque|un piège|surcoté)\b",
       r"\bstop (using|doing|saying|hiring|posting)\b", r"\barrêtez de\b", r"\bnobody (wants|needs|cares|tells)\b",
       r"\bpersonne ne (veut|dit|vous dira)\b", r"\bi disagree\b", r"\bje ne suis pas d'accord\b", r"\bthe truth\b",
       r"\bla vérité\b", r"\bwrong\b", r"\bmyth\b", r"\bmythe\b", r"\bplease stop\b", r"\byou don'?t need\b",
       r"\bvous n'avez pas besoin\b", r"\bpas besoin\b", r"\bfire your\b", r"\bis not (a|the)\b", r"\bn'est pas (un|une|le|la)\b",
       r"\beveryone (is|says|thinks)\b", r"\btout le monde (dit|pense|croit)\b", r"\bthey'?re (all )?wrong\b"]
STORY = [r"\b(\d+|two|three|five|ten|deux|trois|cinq|dix) (years?|ans|months?|mois|weeks?|semaines) ago\b",
         r"\bil y a (\d+|deux|trois|cinq|dix) (ans|mois|semaines)\b", r"\bin 20[12]\d\b", r"\ben 20[12]\d\b",
         r"\bwhen i (was|started|quit|left|lost|failed|got)\b", r"\bquand j'?(ai|étais|suis)\b",
         r"\bi (failed|quit|lost|left|was fired|got fired|went bankrupt|burned out)\b",
         r"\bj'ai (raté|échoué|quitté|perdu|démissionné|planté)\b",
         r"\bmy (story|journey|first|biggest mistake|worst)\b", r"\bmon (histoire|parcours|premier|pire|plus gros)\b",
         r"\bi'?m \d\d\b", r"\bj'ai \d\d ans\b", r"\btoday (i|we)\b", r"\baujourd'hui (je|on)\b",
         r"\bback then\b", r"\bà l'époque\b", r"\blesson(s)? (i|we) learned\b", r"\bce que j'ai (appris|retenu)\b",
         r"\bwhat i learned\b", r"\bfast forward\b", r"\bi remember\b", r"\bje me souviens\b"]
BLOCK = re.compile(r"\b(i'?m hiring|i am hiring|we'?re hiring|nous recrutons|je recrute|referral bonus|job opening|apply here"
                   r"|announcing\b|introducing (our|my)\b|we just launched|je lance (mon|ma|notre)|nous lançons)\b", re.I)


# ---------------------------------------------------------------- fenetre, comptes
def fenetre(fin: str) -> tuple[str, str]:
    """Du lundi de S-6 au dimanche de S-2, par rapport a la semaine de `fin`."""
    d = datetime.date.fromisoformat(fin)
    lundi = d - datetime.timedelta(days=d.weekday())
    return (lundi - datetime.timedelta(weeks=6)).isoformat(), (lundi - datetime.timedelta(weeks=2, days=-6)).isoformat()


def identifiant(url: str) -> str | None:
    m = re.search(r"linkedin\.com/in/([^/?#]+)", url)
    return urllib.parse.unquote(m.group(1)).lower().strip() if m else None


def lire_comptes(args) -> list[dict]:
    urls: list[str] = []
    if args.comptes:
        urls += args.comptes
    if args.fichier:
        urls += [l.strip() for l in Path(args.fichier).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    if args.memorises:
        if not COMPTES_FILE.exists():
            arret(f"{COMPTES_FILE} n'existe pas : passez les comptes avec --comptes ou --fichier, le skill proposera de les memoriser.")
        urls += [c["url"] for c in json.loads(COMPTES_FILE.read_text(encoding="utf-8")).get("comptes", [])]
    vus, comptes = set(), []
    for u in urls:
        pid = identifiant(u)
        if not pid:
            afficher(f"  ignore (pas une URL de profil LinkedIn) : {u}")
            continue
        if pid in vus:
            continue
        vus.add(pid)
        comptes.append({"public_identifier": pid, "url": f"https://www.linkedin.com/in/{pid}/"})
    if not comptes:
        arret("Aucun compte a suivre. Donnez au moins une URL de profil LinkedIn (https://www.linkedin.com/in/...).")
    return comptes


# ---------------------------------------------------------------- normalisation, classement
def normaliser(brut: list[dict], w0: str, w1: str, connus: set[str]) -> list[dict]:
    rows = []
    for x in brut:
        date = (x.get("postedAt") or {}).get("date", "")[:10]
        if not (w0 <= date <= w1):
            continue
        au = x.get("author") or {}
        pid = (au.get("publicIdentifier") or "").lower()
        if pid not in connus:
            continue
        eg = x.get("engagement") or {}
        L, C, S = eg.get("likes") or 0, eg.get("comments") or 0, eg.get("shares") or 0
        doc = x.get("document") or {}
        covers = [u for p in (doc.get("coverPages") or []) for u in (p.get("imageUrls") or [])]
        rows.append({"id": x.get("id"), "date": date, "author": au.get("name"), "pid": pid, "url": x.get("linkedinUrl"),
                     "content": x.get("content") or "", "likes": L, "comments": C, "shares": S, "total": L + C + S,
                     "images": [i["url"] for i in (x.get("postImages") or []) if i.get("url")],
                     "doc_pages": doc.get("totalPageCount"), "doc_covers": covers,
                     "doc_transcript": doc.get("transcribedDocumentUrl"),
                     "video": (x.get("postVideo") or {}).get("videoUrl"),
                     "video_thumb": (x.get("postVideo") or {}).get("thumbnailUrl")})
    return rows


def _hits(pats, t):
    return sum(1 for p in pats if re.search(p, t, re.I))


def classer(rows: list[dict], verdicts: dict) -> list[dict]:
    by = collections.defaultdict(list)
    for r in rows:
        by[r["pid"]].append(r["total"])
    med = {k: max(statistics.median(v), 1) for k, v in by.items()}
    for r in rows:
        t = r["content"]
        asset = bool(re.search(ASSET, t, re.I))
        r["cand"] = {"LM": asset and (_hits(GATE, t) >= 1 or _hits(GIVE, t) >= 1 or bool(BARE_LINK.search(t))),
                     "EDU": _hits(EDU, t) >= 1 or bool(r["doc_covers"]),
                     "HOT": _hits(HOT, t) >= 1,
                     "STORY": _hits(STORY, t) >= 2 or (_hits(STORY, t) >= 1 and len(t.split()) > 120)}
        r["overperf"] = round(r["total"] / med[r["pid"]], 2)
        r["n_posts_auteur"] = len(by[r["pid"]])
        if BLOCK.search(t):
            r["verdict"], r["verdict_source"] = "NON", "exclusion"
        elif r["id"] in verdicts:
            r["verdict"], r["verdict_source"] = verdicts[r["id"]], "manuel"
        else:
            c = r["cand"]
            r["verdict"] = "LM" if c["LM"] else "STORY" if c["STORY"] else "HOT" if c["HOT"] else "EDU" if c["EDU"] else "NON"
            r["verdict_source"] = "regex"
    return rows


def choisir(rows, cat, n, cap=CAP_PAR_AUTEUR):
    out, vus = [], collections.Counter()
    for r in sorted([r for r in rows if r["verdict"] == cat], key=lambda r: -r["total"]):
        if vus[r["pid"]] >= cap:
            continue
        vus[r["pid"]] += 1
        out.append(r)
        if len(out) == n:
            break
    return out


# ---------------------------------------------------------------- medias
def _get(url, chemin: Path, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        chemin.write_bytes(r.read())


def vignette(src: Path, dst: Path) -> None:
    """Vignette 820 px : sips sur macOS, sinon Pillow si installe, sinon copie telle quelle."""
    if shutil.which("sips"):
        subprocess.run(["sips", "-Z", "820", str(src), "--out", str(dst)], capture_output=True)
        return
    try:
        from PIL import Image  # type: ignore
        im = Image.open(src)
        im.thumbnail((820, 820))
        im.save(dst)
    except Exception:
        shutil.copy(src, dst)


def telecharger_medias(top: dict, run: Path, precedent: dict | None = None) -> tuple[int, int]:
    img, th = run / "images", run / "images" / "thumbs"
    th.mkdir(parents=True, exist_ok=True)
    ok = err = 0
    for cat, items in top.items():
        for i, r in enumerate(items, 1):
            prev = (precedent or {}).get(r["id"])
            if prev and prev.get("local_images") and all((img / f).exists() for f in prev["local_images"]):
                r["local_images"] = prev["local_images"]
                if prev.get("local_pdf"):
                    r["local_pdf"] = prev["local_pdf"]
                continue
            srcs = [("img", u) for u in r["images"]] + [("cover", u) for u in r["doc_covers"]]
            if not srcs and r.get("video_thumb"):
                srcs = [("video", r["video_thumb"])]
            saved = []
            for j, (kind, u) in enumerate(srcs, 1):
                nom = f"{cat}{i:02d}_{kind}{j}.jpg"
                try:
                    _get(u, img / nom, 40)
                    vignette(img / nom, th / nom)
                    saved.append(nom)
                    ok += 1
                except Exception as ex:
                    err += 1
                    afficher(f"  echec {nom} : {type(ex).__name__}")
            r["local_images"] = saved
            if r.get("doc_transcript"):
                nom = f"{cat}{i:02d}_carrousel.pdf"
                try:
                    _get(r["doc_transcript"], img / nom, 90)
                    r["local_pdf"] = nom
                    ok += 1
                except Exception as ex:
                    err += 1
                    afficher(f"  echec {nom} : {type(ex).__name__}")
    return ok, err


# ---------------------------------------------------------------- rapport HTML
CSS = """
:root{--fond:#FAF9F5;--carte:#F0ECE0;--accent:#1D3BE0;--texte:#141413;--gris:#5C5A54;--ligne:#E3DAC8}
*{box-sizing:border-box}body{margin:0;background:var(--fond);color:var(--gris);font-family:-apple-system,Helvetica,Arial,sans-serif;font-size:14px;line-height:1.45}
.wrap{max-width:1380px;margin:0 auto;padding:40px 32px 80px}
h1{color:var(--texte);font-weight:600;letter-spacing:-.03em;font-size:34px;line-height:1.05;margin:0 0 8px}h1 span{color:var(--accent)}
h2{color:var(--texte);font-weight:600;font-size:24px;margin:48px 0 4px}.cnt{font-family:Menlo,monospace;font-size:14px;color:var(--accent);margin-left:8px}
.sub{margin:0 0 14px}.meta{font-family:Menlo,monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:22px}
nav a{display:inline-block;margin:0 10px 22px 0;padding:8px 14px;border-radius:999px;background:var(--carte);color:var(--texte);text-decoration:none;font-weight:600}
table{width:100%;border-collapse:collapse;background:var(--carte);border-radius:16px;overflow:hidden}
th{text-align:left;font-family:Menlo,monospace;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;padding:12px;border-bottom:1.5px solid var(--ligne)}
td{padding:12px;border-bottom:1.5px solid var(--ligne);vertical-align:top}tr:last-child td{border-bottom:none}
.rk{font-family:Menlo,monospace;color:var(--accent);font-weight:600;white-space:nowrap}
.th{width:150px}.th img{width:130px;height:130px;object-fit:cover;object-position:top;border-radius:10px;display:block;background:var(--fond)}
.noimg{width:130px;height:130px;border-radius:10px;background:var(--fond);display:flex;align-items:center;justify-content:center;font-size:12px}
.more,.pdf{font-family:Menlo,monospace;font-size:11px;margin-top:4px}.pdf{color:var(--accent)}
.au{width:170px;color:var(--texte)}.dt{color:var(--gris);font-size:12px}
.num{width:150px;white-space:nowrap;color:var(--texte)}.x{color:var(--accent);font-weight:600}
.tx{color:var(--texte)}summary{cursor:pointer;list-style:none}summary::-webkit-details-marker{display:none}
summary::after{content:" \\25B8 lire le post";color:var(--accent);font-size:12px}details[open] summary::after{content:" \\25BE replier"}
.full{margin-top:10px;padding:14px;background:var(--fond);border-radius:10px;line-height:1.55}
.lk{display:inline-block;margin-top:8px;color:var(--accent);text-decoration:none;font-weight:600}.vs{font-size:11px;color:var(--gris);margin-left:10px}
table.small td,table.small th{padding:6px 10px;font-size:12.5px}table.small a{color:var(--texte);text-decoration:none}
"""


def _fmt(n):
    return f"{n:,}".replace(",", " ")


def _media(r):
    if r.get("doc_covers"):
        return f"carrousel {r.get('doc_pages') or ''} p."
    if r.get("video"):
        return "vidéo"
    return "image" if r.get("images") else "texte"


def _vignette(r):
    imgs = r.get("local_images") or []
    if not imgs:
        return '<div class="noimg">texte seul</div>'
    extra = f'<div class="more">+{len(imgs) - 1}</div>' if len(imgs) > 1 else ""
    pdf = f'<a class="pdf" href="images/{escape(r["local_pdf"])}">PDF</a>' if r.get("local_pdf") else ""
    return f'<a href="images/{escape(imgs[0])}" target="_blank"><img src="images/thumbs/{escape(imgs[0])}" loading="lazy"></a>{extra}{pdf}'


def _ligne(cat, i, r):
    hook = " ".join(x.strip() for x in r["content"].split("\n") if x.strip())[:200]
    full = "<br>".join(escape(x) for x in r["content"].split("\n"))
    return f"""<tr><td class="rk">{cat}{i:02d}</td><td class="th">{_vignette(r)}</td>
<td class="au"><b>{escape(r['author'] or '')}</b><br><span class="dt">{escape(r['date'])} · {_media(r)}</span></td>
<td class="num"><b>{_fmt(r['total'])}</b><br><span class="dt">{_fmt(r['likes'])} L · {_fmt(r['comments'])} C · {_fmt(r['shares'])} P</span><br><span class="x">x{r['overperf']} <span class="dt">sur {r['n_posts_auteur']} posts</span></span></td>
<td class="tx"><details><summary>{escape(hook)}</summary><div class="full">{full}</div></details>
<a class="lk" href="{escape(r['url'] or '')}" target="_blank">Voir sur LinkedIn</a> <span class="vs">verdict {r['verdict_source']}</span></td></tr>"""


def ecrire_rapport(run: Path, top: dict, rows: list[dict], w0: str, w1: str) -> Path:
    nav = "".join(f'<a href="#{c}">{CATEGORIES[c][0]} ({len(top[c])})</a>' for c in CATEGORIES) + '<a href="#annexe">Annexe</a>'
    sections = ""
    for c, (titre, sous) in CATEGORIES.items():
        lignes = "".join(_ligne(c, i, r) for i, r in enumerate(top[c], 1))
        sections += f"""<section id="{c}"><h2>{titre}<span class="cnt">{len(top[c])}</span></h2><p class="sub">{sous}</p>
<table><thead><tr><th>#</th><th>Visuel</th><th>Auteur</th><th>Engagement</th><th>Post</th></tr></thead><tbody>{lignes}</tbody></table></section>"""
    tous = sorted(rows, key=lambda r: -r["total"])
    annexe = "".join(f"""<tr><td>{escape(r['date'])}</td><td>{escape(r['author'] or '')}</td><td>{_fmt(r['total'])}</td>
<td>{r['verdict'] if r['verdict'] != 'NON' else ''}</td><td><a href="{escape(r['url'] or '')}" target="_blank">{escape(' '.join(r['content'].split())[:120])}</a></td></tr>""" for r in tous)
    doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Veille créateurs {w0} au {w1}</title><style>{CSS}</style></head>
<body><div class="wrap"><div class="meta">Veille créateurs · S-6 à S-2</div>
<h1>Les posts qui ont performé <span>du {w0} au {w1}</span></h1>
<p class="sub">{len(rows)} posts, {len({r['pid'] for r in rows})} comptes actifs. Classement par interactions totales, {CAP_PAR_AUTEUR} posts au plus par compte. « x » : rapport à la médiane du compte sur la fenêtre. Clic sur la vignette : image en grand. Clic sur l'accroche : le post entier.</p>
<nav>{nav}</nav>{sections}
<section id="annexe"><h2>Annexe · les {len(tous)} posts de la fenêtre</h2><p class="sub">Du plus performant au moins performant. La colonne Type est vide pour ce qui n'entre dans aucune catégorie.</p>
<table class="small"><thead><tr><th>Date</th><th>Auteur</th><th>Total</th><th>Type</th><th>Début du post</th></tr></thead><tbody>{annexe}</tbody></table></section>
</div></body></html>"""
    out = run / "rapport.html"
    out.write_text(doc, encoding="utf-8")
    return out


# ---------------------------------------------------------------- pipeline
def construire(run: Path, brut: list[dict], comptes: list[dict], w0: str, w1: str, medias: bool = True) -> None:
    verdicts_p = run / "verdicts.json"
    verdicts = {k: v for k, v in json.loads(verdicts_p.read_text(encoding="utf-8")).items() if not k.startswith("_")} if verdicts_p.exists() else {}
    rows = classer(normaliser(brut, w0, w1, {c["public_identifier"] for c in comptes}), verdicts)
    (run / "posts.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    top = {c: choisir(rows, c, n) for c, n in QUOTAS.items()}
    afficher(f"{len(rows)} posts dans la fenetre, {len({r['pid'] for r in rows})} comptes actifs, {len(verdicts)} verdicts manuels")
    for c, its in top.items():
        nreg = sum(1 for r in its if r["verdict_source"] == "regex")
        afficher(f"  {c:5} : {len(its)} retenus, dont {nreg} sur verdict automatique")
    cands = [r for its in top.values() for r in its if r["verdict_source"] == "regex"]
    ids = {r["id"] for r in cands}
    cands += [r for r in sorted(rows, key=lambda r: -r["total"]) if r["verdict_source"] == "regex" and r["verdict"] != "NON" and r["id"] not in ids][:40]
    with open(run / "candidats.txt", "w", encoding="utf-8") as f:
        f.write("# id  total  [candidatures]  auteur | debut du post. Verdict a ecrire dans verdicts.json : LM, EDU, HOT, STORY ou NON.\n")
        for r in cands:
            flags = ",".join(k for k, v in r["cand"].items() if v)
            f.write(f"{r['id']} {r['total']:5d} [{flags:16}] {(r['author'] or '')[:18]:18} | {' '.join(r['content'].split())[:160]}\n")
    if not verdicts_p.exists():
        verdicts_p.write_text(json.dumps({"_comment": "LM lead magnet, EDU educationnel, HOT hot take, STORY storytelling, NON hors sujet. Un post absent garde le verdict automatique."}, ensure_ascii=False, indent=1), encoding="utf-8")
    precedent = {}
    if (run / "top.json").exists():
        precedent = {r["id"]: r for its in json.loads((run / "top.json").read_text(encoding="utf-8"))["top"].values() for r in its}
    if medias:
        ok, err = telecharger_medias(top, run, precedent)
        afficher(f"medias : {ok} telecharges, {err} echecs")
    (run / "top.json").write_text(json.dumps({"window": [w0, w1], "quotas": QUOTAS, "top": top}, ensure_ascii=False, indent=1), encoding="utf-8")
    rapport = ecrire_rapport(run, top, rows, w0, w1)
    afficher(f"rapport : {rapport}")
    afficher(f"{len(cands)} candidats a arbitrer dans {run / 'candidats.txt'} ; puis : veille_createurs.py --reconstruire \"{run}\"")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--comptes", nargs="*", help="URLs de profils LinkedIn")
    ap.add_argument("--fichier", help="fichier texte, une URL par ligne")
    ap.add_argument("--memorises", action="store_true", help="lire comptes-veille.json")
    ap.add_argument("--fin", default=datetime.date.today().isoformat(), help="date de reference (defaut : aujourd'hui)")
    ap.add_argument("--dry-run", action="store_true", help="afficher la fenetre, les comptes et le cout, ne rien lancer")
    ap.add_argument("--sans-medias", action="store_true")
    ap.add_argument("--reconstruire", help="dossier d'un run existant : reclasser avec verdicts.json sans relancer Apify")
    a = ap.parse_args()

    if a.reconstruire:
        run = Path(a.reconstruire)
        meta = json.loads((run / "run.json").read_text(encoding="utf-8"))
        brut = json.loads((run / "posts.raw.json").read_text(encoding="utf-8"))
        construire(run, brut, meta["comptes"], meta["window"][0], meta["window"][1], medias=not a.sans_medias)
        return

    comptes = lire_comptes(a)
    w0, w1 = fenetre(a.fin)
    entree = {"targetUrls": [c["url"] for c in comptes], "maxPosts": MAX_POSTS, "postedLimit": "3months",
              "postedLimitDate": w0, "includeQuotePosts": True, "includeReposts": False,
              "scrapeReactions": False, "scrapeComments": False}
    estimation = prix(ACTOR, len(comptes) * MAX_POSTS)
    afficher(f"Fenetre S-6 a S-2 : {w0} -> {w1}")
    afficher(f"{len(comptes)} comptes : " + ", ".join(c["public_identifier"] for c in comptes))
    afficher(f"Cout maximal : {estimation}")
    brut, infos = lancer(ACTOR, entree, timeout_s=1200, label="posts des createurs", dry_run=a.dry_run, estimation=estimation)
    if a.dry_run:
        return
    run = DOSSIER / "sources" / f"veille-createurs_{w0}_{w1}"
    run.mkdir(parents=True, exist_ok=True)
    (run / "posts.raw.json").write_text(json.dumps(brut, ensure_ascii=False), encoding="utf-8")
    (run / "run.json").write_text(json.dumps({"window": [w0, w1], "comptes": comptes, "apify_run": infos.get("id"),
                                              "date": datetime.date.today().isoformat()}, ensure_ascii=False, indent=1), encoding="utf-8")
    sans_post = sorted({c["public_identifier"] for c in comptes} - {(x.get("author") or {}).get("publicIdentifier", "").lower() for x in brut})
    if sans_post:
        afficher(f"comptes sans post recupere ({len(sans_post)}) : {', '.join(sans_post)}")
    construire(run, brut, comptes, w0, w1, medias=not a.sans_medias)


if __name__ == "__main__":
    main()
