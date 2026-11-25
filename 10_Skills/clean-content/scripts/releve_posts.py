#!/usr/bin/env python3
"""releve_posts : met a jour les chiffres des posts publies dans 05_Calendrier-editorial/Publies/.

Source des chiffres :
  --source unipile       (defaut) GET /api/v1/users/{vous}/posts avec votre compte LinkedIn. Gratuit.
  --depuis-json <f>      un fichier JSON : une liste d'objets {url, texte, date, impressions, reactions,
                         commentaires, partages}. Sert aux tests, ou quand les chiffres viennent d'ailleurs
                         (export LinkedIn, `planifier_post.py --stats`).

Pour chaque post de Publies/ dont `chiffres_definitifs` n'est pas "oui", le script retrouve le post
LinkedIn (par l'identifiant d'activite de l'URL, sinon par le debut du texte), ecrit impressions,
reactions, commentaires, partages et releve_le dans le frontmatter, puis marque `chiffres_definitifs: oui`
au-dela de --jours (30 par defaut) apres la publication.

Il ajoute aussi le lien du post dans le champ `utilise_dans` des fiches citees dans son champ `fiches`.

  --importer   cree un fichier dans Publies/ pour chaque post LinkedIn recent absent du calendrier
               (statut publie, format et pilier vides, a completer). Sans cette option ils sont listes.

Usage :
  python3 releve_posts.py --dry-run
  python3 releve_posts.py --limite 40
  python3 releve_posts.py --depuis-json chiffres.json --importer

Les noms de champs de la reponse Unipile varient selon les versions de l'API : le script essaie
plusieurs noms et laisse vide ce qu'il ne trouve pas. Verifiez le premier releve a la main.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
CHAMPS = ["impressions", "reactions", "commentaires", "partages"]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def id_activite(url: str) -> str:
    m = re.search(r"(\d{15,})", str(url or ""))
    return m.group(1) if m else ""


def premier(d: dict, *cles):
    for c in cles:
        v = d.get(c)
        if v not in (None, ""):
            return v
    return ""


def depuis_unipile(limite: int) -> list[dict]:
    sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
    from gtm_common import Unipile  # noqa: E402
    u = Unipile()
    ident = u.own_provider_id or "me"
    rep = u.get(f"/api/v1/users/{ident}/posts", {"account_id": u.account_id, "limit": limite})
    items = rep.get("items", rep) if isinstance(rep, dict) else rep
    posts = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        pid = str(premier(it, "social_id", "id"))
        posts.append({
            "url": premier(it, "share_url", "url") or (f"https://www.linkedin.com/feed/update/{pid}" if pid else ""),
            "texte": premier(it, "text", "commentary"),
            "date": str(premier(it, "parsed_datetime", "date", "created_at"))[:10],
            "impressions": premier(it, "impressions_counter", "impressions", "views_counter"),
            "reactions": premier(it, "reaction_counter", "reactions_counter", "likes_counter"),
            "commentaires": premier(it, "comment_counter", "comments_counter"),
            "partages": premier(it, "repost_counter", "reposts_counter", "shares_counter"),
        })
    return posts


def decouper(texte: str) -> tuple[list[str], str]:
    if not texte.startswith("---"):
        return [], texte
    fin = texte.find("\n---", 3)
    if fin == -1:
        return [], texte
    return texte[4:fin].split("\n"), texte[fin + 4:]


def valeur(fm: list[str], cle: str) -> str:
    for l in fm:
        m = re.match(rf"^{cle}\s*:\s*(.*)$", l)
        if m:
            return m.group(1).split(" #")[0].strip().strip("\"'")
    return ""


def poser(fm: list[str], cle: str, val) -> None:
    for k, l in enumerate(fm):
        if re.match(rf"^{cle}\s*:", l):
            fm[k] = f"{cle}: {val}"
            return
    fm.append(f"{cle}: {val}")


def corps_post(corps: str) -> str:
    m = re.search(r"##[^\n]*POST COMPLET[^\n]*\n(.*?)(?=\n## |\Z)", corps, re.S)
    return (m.group(1) if m else corps).strip()


def ajouter_utilise_dans(fiche: Path, lien_post: str, dry: bool) -> bool:
    fm, corps = decouper(fiche.read_text(encoding="utf-8"))
    if not fm:
        return False
    actuel = valeur(fm, "utilise_dans")
    if lien_post in actuel:
        return False
    deja = [v.strip() for v in actuel.strip("[]").split(",") if v.strip()]
    poser(fm, "utilise_dans", "[" + ", ".join(deja + [f'"{lien_post}"']) + "]")
    if not dry:
        fiche.write_text("---\n" + "\n".join(fm) + "\n---" + corps, encoding="utf-8")
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=["unipile"], default="unipile")
    ap.add_argument("--depuis-json", help="fichier JSON de posts avec leurs chiffres, au lieu d'appeler Unipile")
    ap.add_argument("--limite", type=int, default=30, help="nombre de posts recents a lire (defaut 30)")
    ap.add_argument("--jours", type=int, default=30, help="apres ce delai, les chiffres sont marques definitifs (defaut 30)")
    ap.add_argument("--importer", action="store_true", help="creer dans Publies/ les posts LinkedIn absents du calendrier")
    ap.add_argument("--brain", help="dossier Content-Brain (defaut : celui du workspace)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.brain:
        brain = Path(a.brain).resolve()
    elif _racine:
        brain = _racine / "05_Departements" / "Marketing" / "Content-Brain"
    else:
        sys.exit("Racine du workspace introuvable. Passez --brain <dossier>.")
    publies = brain / "05_Calendrier-editorial" / "Publies"
    if not publies.is_dir():
        sys.exit(f"Dossier introuvable : {publies}. Lancez \"Installe mon contenu\".")

    if a.depuis_json:
        distants = json.loads(Path(a.depuis_json).read_text(encoding="utf-8"))
    elif a.dry_run:
        print(f"[dry-run] les {a.limite} derniers posts de votre compte seraient lus via Unipile (gratuit), rien n'est écrit.")
        distants = []
    else:
        if _racine is None:
            sys.exit("Racine du workspace introuvable : --source unipile a besoin de 10_Skills/_commun/.")
        distants = depuis_unipile(a.limite)

    par_id = {id_activite(d.get("url")): d for d in distants if id_activite(d.get("url"))}
    par_texte = {norm(d.get("texte"))[:80]: d for d in distants if d.get("texte")}
    aujourd_hui, vus, maj, clos, liens = date.today(), set(), 0, 0, 0
    index_fiches = {p.stem: p for p in (brain / "03_Base-de-connaissances").rglob("*.md")}

    for p in sorted(publies.glob("*.md")):
        fm, corps = decouper(p.read_text(encoding="utf-8"))
        if not fm:
            continue
        d = par_id.get(id_activite(valeur(fm, "url"))) or par_texte.get(norm(corps_post(corps))[:80])
        if d:
            vus.add(id(d))
        for nom in re.findall(r"\[\[([^\]|]+)", " ".join(l for l in fm if l.startswith("fiches"))):
            fiche = index_fiches.get(nom.split("/")[-1])
            if fiche and ajouter_utilise_dans(fiche, f"[[{p.stem}]]", a.dry_run):
                liens += 1
        if valeur(fm, "chiffres_definitifs") == "oui" or not d:
            continue
        for c in CHAMPS:
            if d.get(c) not in (None, ""):
                poser(fm, c, d[c])
        if d.get("url") and not valeur(fm, "url"):
            poser(fm, "url", d["url"])
        if d.get("date") and not valeur(fm, "publie_le"):
            poser(fm, "publie_le", d["date"])
        poser(fm, "releve_le", aujourd_hui.isoformat())
        try:
            age = (aujourd_hui - datetime.strptime(valeur(fm, "publie_le")[:10], "%Y-%m-%d").date()).days
        except ValueError:
            age = 0
        if age > a.jours:
            poser(fm, "chiffres_definitifs", "oui")
            clos += 1
        maj += 1
        if not a.dry_run:
            p.write_text("---\n" + "\n".join(fm) + "\n---" + corps, encoding="utf-8")

    absents = [d for d in distants if id(d) not in vus]
    crees = 0
    if a.importer:
        for d in absents:
            jour = (d.get("date") or aujourd_hui.isoformat())[:10]
            mots = re.sub(r"[^A-Za-z0-9À-ÿ ]", "", str(d.get("texte") or "post")).split()[:5]
            cible = publies / f"Post-{'-'.join(mots) or 'post'}_{jour}.md"
            if cible.exists():
                continue
            fm = ["type: post", "statut: publie", "format:", "support: texte", "canal: linkedin", "pilier:", "idee:", "fiches: []",
                  f"publie_le: {jour}", f"url: {d.get('url', '')}"] + [f"{c}: {d.get(c, '')}" for c in CHAMPS] + [f"releve_le: {aujourd_hui.isoformat()}", "chiffres_definitifs: non"]
            crees += 1
            if not a.dry_run:
                cible.write_text("---\n" + "\n".join(fm) + "\n---\n\n" + str(d.get("texte") or "") + "\n", encoding="utf-8")

    print(f"{'[dry-run] ' if a.dry_run else ''}{len(distants)} post(s) lus, {maj} mis à jour dont {clos} clos, "
          f"{liens} lien(s) ajouté(s) dans les fiches, {crees} importé(s), {len(absents) - crees} absent(s) du calendrier.")
    if absents and not a.importer:
        for d in absents[:15]:
            print(f"  absent du calendrier : {(d.get('date') or '?')[:10]}  {str(d.get('texte') or '')[:70]!r}")
        print("  Relancez avec --importer pour les créer dans Publies/.")


if __name__ == "__main__":
    main()
