#!/usr/bin/env python3
"""reconstruire : refait les pages de piliers, la carte et le calendrier du Content Brain.

Lit 01_Strategie/Strategie-contenu.md (les piliers et leurs sujets) et le frontmatter des fiches de
03_Base-de-connaissances/, des idees de 04_Idees/, des posts de 05_Calendrier-editorial/ et des fiches
de 02_Veille/. Ecrit :
  - 01_Strategie/Piliers/Pilier_<Nom>.md     une page par pilier, sans numero, et rien d'autre : ses sujets sont des
                                             sections de la page, avec le lien vers chaque fiche, puis
                                             ses idees, ses posts et sa veille
  - la ligne **Pilier :** en bas de chaque fiche, qui pointe vers la page du pilier
  - la section "Ou on en est" de Content-Brain.md (entre les marqueurs carte:debut et carte:fin)
  - le tableau par semaine de 05_Calendrier-editorial/Calendrier.md (entre calendrier:debut et calendrier:fin)

Il n'y a pas de page par sujet. Les pages `Sujet_*.md` et les pages de piliers numerotees
(`Pilier-N_*.md`) ecrites par une version precedente partent dans 11_Archives/ : elles sont refaites
au nouveau nom. Rien n'est supprime. Une page de pilier qui ne correspond
plus a la strategie est signalee.

Usage :
  python3 reconstruire.py --dry-run     ce qui serait ecrit, sans rien toucher
  python3 reconstruire.py               ecrit
  python3 reconstruire.py --brain <dossier>   un autre dossier que celui du workspace (tests)

Stdlib uniquement.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
TYPES = [("enseignement", "Enseignements"), ("methode", "Methodes"), ("preuve", "Preuves"), ("histoire", "Histoires")]
LIBELLE = {"enseignement": "Enseignements", "methode": "Méthodes", "preuve": "Preuves", "histoire": "Histoires"}
ENTETE = "> Page reconstruite par `clean-content` (script `reconstruire.py`). Ne pas modifier à la main : changez le `pilier` ou les `sujets` d'une fiche, ou la section Piliers de la stratégie.\n"
MARQUE = "Page reconstruite par `clean-content`"
SINGULIER = {"enseignement": "Enseignement", "methode": "Méthode", "preuve": "Preuve", "histoire": "Histoire"}


def deplacer(source: Path, cible: Path, dry: bool, journal: list[str], verbe: str) -> None:
    if cible.exists():
        cible = cible.with_name(f"{cible.stem}_{datetime.now().strftime('%H%M%S')}{cible.suffix}")
    journal.append(f"{verbe} {source} -> {cible}")
    if not dry:
        cible.parent.mkdir(parents=True, exist_ok=True)
        source.rename(cible)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def slug(s: str) -> str:
    s = re.sub(r"[\\/:*?\"<>|#^\[\]'’]", " ", str(s)).strip()
    return re.sub(r"\s+", "-", s)


def lire_frontmatter(texte: str) -> tuple[dict, str]:
    if not texte.startswith("---"):
        return {}, texte
    fin = texte.find("\n---", 3)
    if fin == -1:
        return {}, texte
    data, cle = {}, None
    for ligne in texte[3:fin].splitlines():
        m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", ligne)
        if m:
            cle, val = m.group(1), m.group(2).split(" #")[0].strip()
            if val.startswith("[") and val.endswith("]"):
                data[cle] = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
            else:
                data[cle] = val.strip("\"'")
        elif cle and ligne.strip().startswith("- "):
            if not isinstance(data.get(cle), list):
                data[cle] = [] if not data.get(cle) else [data[cle]]
            data[cle].append(ligne.strip()[2:].strip().strip("\"'"))
    return data, texte[fin + 4:].lstrip("\n")


def titre_de(corps: str, defaut: str) -> str:
    m = re.search(r"^# (.+)$", corps, re.M)
    return m.group(1).strip() if m else defaut


def lire_strategie(chemin: Path) -> list[dict]:
    """Les piliers de la section Piliers : titre `### Pilier N : Nom (XX %)`, ligne Portee, liste Sujets."""
    piliers, courant, dans_sujets = [], None, False
    if not chemin.exists():
        return piliers
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^###\s+Pilier\s+(\d+)\s*:\s*(.+?)\s*(?:\(([^)]*)\))?\s*$", ligne)
        if m:
            nom = m.group(2).strip()
            courant = None
            dans_sujets = False
            if nom.startswith("["):
                continue
            courant = {"n": int(m.group(1)), "nom": nom, "part": (m.group(3) or "").strip(), "portee": "", "sujets": []}
            piliers.append(courant)
            continue
        if ligne.startswith("## ") or ligne.startswith("### "):
            courant, dans_sujets = None, False
            continue
        if courant is None:
            continue
        if re.match(r"^Port[ée]e\s*:", ligne):
            courant["portee"] = ligne.split(":", 1)[1].strip()
            dans_sujets = False
        elif re.match(r"^Sujets\s*:", ligne):
            dans_sujets = True
        elif dans_sujets and ligne.strip().startswith("- "):
            brut = ligne.strip()[2:].strip()
            if brut.startswith("["):
                continue
            nom, _, douleur = brut.partition(" : ")
            courant["sujets"].append({"nom": nom.strip(), "douleur": douleur.strip()})
        elif ligne.strip() and not ligne.strip().startswith("- "):
            dans_sujets = False
    return piliers


def lire_dossier(dossier: Path) -> list[dict]:
    fiches = []
    if not dossier.is_dir():
        return fiches
    for p in sorted(dossier.rglob("*.md")):
        fm, corps = lire_frontmatter(p.read_text(encoding="utf-8"))
        if not fm:
            continue
        fm["_chemin"], fm["_titre"] = p, titre_de(corps, p.stem)
        fiches.append(fm)
    return fiches


def lien(fiche: dict) -> str:
    return f"[[{fiche['_chemin'].stem}|{fiche['_titre']}]]" if fiche["_titre"] != fiche["_chemin"].stem else f"[[{fiche['_chemin'].stem}]]"


def ecrire(chemin: Path, contenu: str, dry: bool, journal: list[str]) -> None:
    ancien = chemin.read_text(encoding="utf-8") if chemin.exists() else None
    if ancien == contenu:
        return
    journal.append(("maj     " if ancien is not None else "nouveau ") + str(chemin))
    if not dry:
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(contenu, encoding="utf-8")


def remplacer_bloc(texte: str, nom: str, bloc: str) -> str | None:
    debut, fin = f"<!-- {nom}:debut -->", f"<!-- {nom}:fin -->"
    i, j = texte.find(debut), texte.find(fin)
    if i == -1 or j == -1 or j < i:
        return None
    return texte[: i + len(debut)] + "\n" + bloc.rstrip("\n") + "\n" + texte[j:]


def maj_lien_fiche(fiche: dict, ligne_lien: str, dry: bool, journal: list[str]) -> None:
    p = fiche["_chemin"]
    lignes = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    reste = [l for l in lignes if not re.match(r"^\*\*(Sujets|Pilier) :\*\*", l)]
    pos = next((k for k, l in enumerate(reste) if l.startswith("**Voir aussi :**")), len(reste))
    reste.insert(pos, ligne_lien)
    ecrire(p, "\n".join(reste) + "\n", dry, journal)


def semaine(d: str) -> str | None:
    try:
        an, sem, _ = datetime.strptime(d[:10], "%Y-%m-%d").isocalendar()
        return f"{an}-S{sem:02d}"
    except (ValueError, TypeError):
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brain", help="dossier Content-Brain (defaut : celui du workspace)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.brain:
        brain = Path(a.brain).resolve()
    elif _racine:
        brain = _racine / "05_Departements" / "Marketing" / "Content-Brain"
    else:
        sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/). Passez --brain <dossier>.")
    if not brain.is_dir():
        sys.exit(f"Content Brain introuvable : {brain}. Lancez \"Installe mon contenu\".")

    strat, base, journal, alertes = brain / "01_Strategie", brain / "03_Base-de-connaissances", [], []
    dossier_piliers = strat / "Piliers"
    piliers = lire_strategie(strat / "Strategie-contenu.md")

    # Rangement des pages d'une version precedente : piliers a la racine de 01_Strategie/, pages de sujets.
    parent_archives = next((d for d in brain.parents if (d / "11_Archives").is_dir()), brain)
    archive = parent_archives / "11_Archives" / f"content-brain-anciennes-pages_{date.today().isoformat()}"
    anciennes = sorted(strat.glob("*.md")) + (sorted(dossier_piliers.glob("*.md")) if dossier_piliers.is_dir() else [])
    for p in anciennes:
        if not re.match(r"^(Pilier-\d+_|Sujet_)", p.stem):
            continue
        if MARQUE in p.read_text(encoding="utf-8")[:600]:
            deplacer(p, archive / p.name, a.dry_run, journal, "archivé")
        else:
            alertes.append(f"page écrite à la main, laissée en place : {p.name}")

    fiches = [f for t, d in TYPES for f in lire_dossier(base / d)]
    par_nom = {norm(p["nom"]): p for p in piliers}
    for p in piliers:
        p["fiches"], p["page"] = [], f"Pilier_{slug(p['nom'])}"
        for s in p["sujets"]:
            s["fiches"] = []

    sans_pilier = []
    for f in fiches:
        p = par_nom.get(norm(f.get("pilier", "")))
        if p is None:
            sans_pilier.append(f)
            continue
        p["fiches"].append(f)
        sujets = f.get("sujets") or []
        sujets = [sujets] if isinstance(sujets, str) else sujets
        trouves = [s for nom in sujets for s in p["sujets"] if norm(s["nom"]) == norm(nom)]
        inconnus = [nom for nom in sujets if nom and not any(norm(s["nom"]) == norm(nom) for s in p["sujets"])]
        if inconnus:
            alertes.append(f"sujet hors stratégie ({', '.join(inconnus)}) : {f['_chemin'].name}")
        for s in trouves:
            s["fiches"].append(f)
        f["_sujets"] = trouves
        maj_lien_fiche(f, f"**Pilier :** [[{p['page']}|{p['nom']}]]", a.dry_run, journal)

    sources = lire_dossier(base / "Sources")
    idees = lire_dossier(brain / "04_Idees")
    posts = lire_dossier(brain / "05_Calendrier-editorial" / "Brouillons") + lire_dossier(brain / "05_Calendrier-editorial" / "Publies")
    veille = lire_dossier(brain / "02_Veille" / "Marche") + lire_dossier(brain / "02_Veille" / "Inspirations")

    def du_pilier(liste: list[dict], p: dict) -> list[dict]:
        return [f for f in liste if norm(f.get("pilier", "")) == norm(p["nom"])]

    def compte(liste: list[dict]) -> str:
        return ", ".join(f"{LIBELLE[t].lower()} {sum(1 for f in liste if f.get('type') == t)}" for t, _ in TYPES)

    def puces(liste: list[dict]) -> str:
        ordre = [t for t, _ in TYPES]
        tri = sorted(liste, key=lambda f: ordre.index(f.get("type")) if f.get("type") in ordre else len(ordre))
        return "\n".join(f"- {SINGULIER.get(f.get('type'), 'Fiche')} : {lien(f)}" for f in tri)

    attendues = set()
    for p in piliers:
        trous = []
        lignes = [f"# {p['nom']}\n", ENTETE]
        if p["portee"]:
            lignes.append(f"**Portée :** {p['portee']}\n")
        lignes.append(f"**Part visée :** {p['part'] or 'non précisée'}. **Fiches :** {len(p['fiches'])} ({compte(p['fiches'])}).\n")
        lignes.append("## Sujets\n")
        if not p["sujets"]:
            lignes.append("Aucun sujet défini dans la stratégie.\n")
        for s in p["sujets"]:
            lignes.append(f"### {s['nom']}\n")
            lignes.append(f"Douleur client : {s['douleur'] or 'à préciser'}\n")
            lignes.append((puces(s["fiches"]) if s["fiches"] else "Aucune fiche pour l'instant.") + "\n")
            manque = [t for t in ("preuve", "histoire") if not any(f.get("type") == t for f in s["fiches"])]
            if not s["fiches"]:
                trous.append(f"{s['nom']} : aucune fiche")
            elif manque:
                trous.append(f"{s['nom']} : il manque {' et '.join('une ' + m for m in manque)}")
        hors = [f for f in p["fiches"] if not f.get("_sujets")]
        if hors:
            lignes.append("## Fiches sans sujet\n\n" + puces(hors) + "\n")
        for titre, liste in (("Idées", du_pilier(idees, p)), ("Posts", du_pilier(posts, p)), ("Veille", du_pilier(veille, p))):
            if liste:
                lignes.append(f"## {titre}\n\n" + "\n".join(f"- {lien(f)}" for f in liste) + "\n")
        lignes.append("## Pas encore couvert\n\n" + ("\n".join(f"- {t}" for t in trous) if trous else "Tous les sujets ont au moins une preuve et une histoire.") + "\n")
        lignes.append("Retour à la carte : [[Content-Brain]]. Stratégie : [[Strategie-contenu]].")
        p["trous"] = trous
        attendues.add(p["page"])
        ecrire(dossier_piliers / f"{p['page']}.md", "\n".join(lignes) + "\n", a.dry_run, journal)

    connues = {p.stem for p in dossier_piliers.glob("*.md")} if dossier_piliers.is_dir() else set()
    connues -= {Path(l.split(" -> ")[0].split(" ", 1)[1].strip()).stem for l in journal if l.startswith("archivé")}
    for nom in sorted(connues - attendues):
        alertes.append(f"page de pilier qui ne correspond plus à la stratégie (à archiver sur un oui) : Piliers/{nom}.md")

    def repartition(liste: list[dict], champ: str) -> str:
        valeurs = sorted({str(f.get(champ) or "non renseigné") for f in liste})
        return ", ".join(f"{sum(1 for f in liste if str(f.get(champ) or 'non renseigné') == v)} {v}" for v in valeurs) or "aucun"

    carte = [f"Reconstruit le {date.today().isoformat()}.\n", "| Pilier | Fiches | Détail | Sujets avec un manque |", "|---|---|---|---|"]
    for p in piliers:
        carte.append(f"| [[{p['page']}|{p['nom']}]] | {len(p['fiches'])} | {compte(p['fiches'])} | {len(p['trous'])} sur {len(p['sujets'])} |")
    if not piliers:
        carte.append("| aucun pilier dans la stratégie | 0 | | |")
    carte += ["", f"- Fiches sans pilier reconnu : {len(sans_pilier)}", f"- Sources traitées : {len(sources)} ({repartition(sources, 'nature')})",
              f"- Idées : {len(idees)} ({repartition(idees, 'statut')})", f"- Posts : {len(posts)} ({repartition(posts, 'statut')})"]
    if alertes:
        carte += ["", "À regarder :"] + [f"- {x}" for x in alertes[:15]]
    note = brain / "Content-Brain.md"
    if note.exists():
        nouveau = remplacer_bloc(note.read_text(encoding="utf-8"), "carte", "\n".join(carte))
        if nouveau is None:
            alertes.append("marqueurs carte:debut et carte:fin absents de Content-Brain.md : carte non écrite")
        else:
            ecrire(note, nouveau, a.dry_run, journal)

    par_semaine: dict[str, list[dict]] = {}
    for f in posts:
        jour = f.get("publie_le") or f.get("programme_pour") or (re.search(r"\d{4}-\d{2}-\d{2}", f["_chemin"].stem) or [""])[0]
        par_semaine.setdefault(semaine(str(jour)) or "sans date", []).append(dict(f, _jour=str(jour)[:10]))
    tableau = []
    for sem in sorted(par_semaine, reverse=True):
        tableau += [f"### {sem}\n", "| Date | Post | Format | Pilier | Statut | Impressions | Réactions | Commentaires |", "|---|---|---|---|---|---|---|---|"]
        for f in sorted(par_semaine[sem], key=lambda x: x["_jour"]):
            tableau.append(f"| {f['_jour'] or '?'} | {lien(f)} | {f.get('format', '')} | {f.get('pilier', '')} | {f.get('statut', '')} | "
                           f"{f.get('impressions', '')} | {f.get('reactions', '')} | {f.get('commentaires', '')} |")
        tableau.append("")
    cal = brain / "05_Calendrier-editorial" / "Calendrier.md"
    if cal.exists():
        nouveau = remplacer_bloc(cal.read_text(encoding="utf-8"), "calendrier", "\n".join(tableau) if tableau else "Aucun post pour l'instant.")
        if nouveau is not None:
            ecrire(cal, nouveau, a.dry_run, journal)

    print(f"{'[dry-run] ' if a.dry_run else ''}{len(piliers)} pilier(s), {sum(len(p['sujets']) for p in piliers)} sujet(s), "
          f"{len(fiches)} fiche(s) dont {len(sans_pilier)} sans pilier, {len(sources)} source(s), {len(idees)} idée(s), {len(posts)} post(s).")
    for l in journal:
        print("  " + l)
    for x in alertes:
        print("  ! " + x)
    for f in sans_pilier[:20]:
        print(f"  ! pilier absent ou inconnu : {f['_chemin'].name} (pilier : {f.get('pilier') or 'vide'})")


if __name__ == "__main__":
    main()
