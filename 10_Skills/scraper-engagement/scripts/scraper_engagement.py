"""scraper_engagement : les personnes qui ont commente ou reagi a un ou plusieurs posts LinkedIn (les votres, ceux
d'un concurrent, d'un event), une ligne par personne et par post, signal_type = commentaire ou like.

Sources (--source) :
  unipile   par defaut : GET /api/v1/posts/{id}/reactions et /comments avec le compte LinkedIn de l'utilisateur (abonnement)
  apify     secours : harvestapi/linkedin-post-comments (0,002 $ par commentaire) + harvestapi/linkedin-post-reactions (0,002 $ par reaction)

Usage :
  python3 scraper_engagement.py --post "https://www.linkedin.com/posts/..." [--post ...] [--type both|commentaires|reactions]
  python3 scraper_engagement.py --posts posts.txt --type commentaires --source apify --max 500 --dry-run
Un commentaire vaut plus qu'un like : quand une personne a fait les deux, la ligne porte signal_type = commentaire
et reaction_type garde la reaction. Sortie : Listes-prospection/scraper-engagement_<sujet>_<date>.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (Unipile, afficher, aujourd_hui, arret, bandeau_dry_run, chemin_sortie, ecrire_csv, extraire_post_id,  # noqa: E402
                        fraicheur, lire_outils, norm_linkedin_url, seniorite_depuis_titre)
from apify_run import lancer, prix  # noqa: E402

VERBE = "scraper-engagement"
ACTOR_COMMENTAIRES = "harvestapi/linkedin-post-comments"
ACTOR_REACTIONS = "harvestapi/linkedin-post-reactions"


def _g(d, *cles, defaut=""):
    for c in cles:
        cur = d
        for part in c.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                break
        if cur not in (None, "", [], {}):
            return cur
    return defaut


def _split_nom(nom):
    nom = (nom or "").strip()
    parts = nom.split(" ", 1)
    return (parts[0], parts[1]) if len(parts) > 1 else (nom, "")


def _personne(auteur: dict, source: str) -> dict:
    prenom, nom = _g(auteur, "first_name", "firstName"), _g(auteur, "last_name", "lastName")
    if not prenom:
        prenom, nom = _split_nom(_g(auteur, "name"))
    titre = _g(auteur, "headline", "occupation", "position")
    url = norm_linkedin_url(_g(auteur, "profile_url", "public_profile_url", "linkedinUrl", "url")) or (
        f"https://www.linkedin.com/in/{_g(auteur, 'public_identifier', 'publicIdentifier')}" if _g(auteur, "public_identifier", "publicIdentifier") else "")
    return {"prenom": prenom, "nom": nom, "titre": titre, "seniorite": seniorite_depuis_titre(titre), "linkedin_url": url,
            "source": source, "date_extraction": aujourd_hui(),
            "provider_id": _g(auteur, "id", "provider_id", "member_urn") if source == "unipile" else "",
            "degre_relation": _g(auteur, "network_distance"), "type_auteur": _g(auteur, "type")}


def fusionner(par_cle: dict, cle: str, ligne: dict) -> None:
    if cle in par_cle:
        deja = par_cle[cle]
        if ligne["signal_type"] == "commentaire" and deja["signal_type"] == "like":
            ligne["reaction_type"] = deja.get("reaction_type", "")
            par_cle[cle] = ligne
        elif ligne["signal_type"] == "like" and deja["signal_type"] == "commentaire":
            deja["reaction_type"] = ligne.get("reaction_type", "")
        return
    par_cle[cle] = ligne


def via_unipile(posts: list[str], types: list[str], max_pages: int, dry_run: bool) -> list[dict]:
    if dry_run:
        bandeau_dry_run("Unipile posts/{id}/reactions et /comments", [f"{len(posts)} post(s), {', '.join(types)}, jusqu'a {max_pages} pages de 100 par type",
                                                                     "cout : abonnement Unipile, lecture avec le compte LinkedIn de l'utilisateur"])
        return []
    u = Unipile()
    lignes = []
    for post in posts:
        pid = extraire_post_id(post)
        par_cle: dict = {}
        if "reactions" in types:
            for r in u.reactions(pid, max_pages):
                auteur = r.get("author") or r.get("member") or r
                l = _personne(auteur, "unipile")
                l.update({"signal_type": "like", "reaction_type": _g(r, "value", "reaction_type", "type"), "signal_date": str(_g(r, "date", "created_at", "timestamp"))[:10],
                          "signal_detail": f"a reagi ({_g(r, 'value', 'reaction_type', 'type') or 'LIKE'}) au post", "post_url": post})
                fusionner(par_cle, l["linkedin_url"] or f"{l['prenom']} {l['nom']}", l)
        if "commentaires" in types:
            for c in u.commentaires(pid, max_pages):
                auteur = c.get("author") or c.get("author_details") or c
                if isinstance(auteur, str):
                    auteur = {"name": auteur, "profile_url": c.get("author_profile_url", ""), "id": c.get("author_id", "")}
                l = _personne(auteur, "unipile")
                l.update({"signal_type": "commentaire", "signal_date": str(_g(c, "date", "created_at", "timestamp"))[:10],
                          "signal_detail": (_g(c, "text", "commentary") or "").replace("\n", " ")[:500], "post_url": post,
                          "commentaire_id": _g(c, "id"), "nb_likes_commentaire": _g(c, "reaction_counter", "likes")})
                fusionner(par_cle, l["linkedin_url"] or f"{l['prenom']} {l['nom']}", l)
        lignes.extend(par_cle.values())
        afficher(f"  [unipile] {post[:70]}... : {len(par_cle)} personne(s)")
    return lignes


def via_apify(posts: list[str], types: list[str], maximum: int, dry_run: bool) -> list[dict]:
    par_post: dict = {p: {} for p in posts}
    if "commentaires" in types:
        items, _ = lancer(ACTOR_COMMENTAIRES, {"posts": posts, "maxItems": maximum, "scrapeReplies": False, "profileScraperMode": "short"},
                          label="post-comments", dry_run=dry_run, estimation=prix(ACTOR_COMMENTAIRES, maximum * len(posts)))
        for it in items:
            post = _g(it, "query.post") or posts[0]
            l = _personne(it.get("actor") or {}, ACTOR_COMMENTAIRES)
            l.update({"signal_type": "commentaire", "signal_date": str(_g(it, "createdAt"))[:10],
                      "signal_detail": (_g(it, "commentary") or "").replace("\n", " ")[:500], "post_url": post,
                      "commentaire_id": _g(it, "id"), "nb_likes_commentaire": _g(it, "engagement.likes")})
            fusionner(par_post.setdefault(post, {}), l["linkedin_url"] or f"{l['prenom']} {l['nom']}", l)
    if "reactions" in types:
        items, _ = lancer(ACTOR_REACTIONS, {"posts": posts, "maxItems": maximum, "profileScraperMode": "short"},
                          label="post-reactions", dry_run=dry_run, estimation=prix(ACTOR_REACTIONS, maximum * len(posts)))
        for it in items:
            post = _g(it, "query.post") or posts[0]
            l = _personne(it.get("actor") or it.get("profile") or {}, ACTOR_REACTIONS)
            typ = _g(it, "reactionType", "type", "reaction")
            l.update({"signal_type": "like", "reaction_type": typ, "signal_date": str(_g(it, "createdAt"))[:10],
                      "signal_detail": f"a reagi ({typ or 'LIKE'}) au post", "post_url": post})
            fusionner(par_post.setdefault(post, {}), l["linkedin_url"] or f"{l['prenom']} {l['nom']}", l)
    return [l for d in par_post.values() for l in d.values()]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--post", action="append", help="URL d'un post (repetable)")
    ap.add_argument("--posts", help="fichier texte, une URL par ligne")
    ap.add_argument("--type", choices=["both", "commentaires", "reactions"], default="both")
    ap.add_argument("--source", choices=["unipile", "apify"])
    ap.add_argument("--max-pages", type=int, default=10, help="unipile : pages de 100 par type (defaut 10)")
    ap.add_argument("--max", type=int, default=1000, help="apify : items max par post et par type")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    posts = list(a.post or [])
    if a.posts:
        posts += [l.strip() for l in Path(a.posts).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    if not posts:
        arret("donnez au moins un post (--post URL ou --posts fichier.txt)")
    for p in posts:
        try:
            extraire_post_id(p)
        except ValueError as e:
            arret(str(e) + " (copiez le lien via le menu 'Copier le lien' du post)")
    types = ["commentaires", "reactions"] if a.type == "both" else [a.type]
    source = a.source or ("unipile" if lire_outils().get("canal_linkedin", "unipile") != "lemlist" else "apify")
    lignes = via_unipile(posts, types, a.max_pages, a.dry_run) if source == "unipile" else via_apify(posts, types, a.max, a.dry_run)
    if a.dry_run:
        return
    compte: dict = {}
    for l in lignes:
        cle = l.get("linkedin_url") or f"{l.get('prenom')} {l.get('nom')}"
        compte[cle] = compte.get(cle, 0) + 1
    for l in lignes:
        l["nb_posts_engages"] = compte[l.get("linkedin_url") or f"{l.get('prenom')} {l.get('nom')}"]
        l["fraicheur"] = fraicheur(l.get("signal_date"))
    lignes.sort(key=lambda l: (0 if l["signal_type"] == "commentaire" else 1, -l["nb_posts_engages"]))
    sujet = a.sujet or (posts[0].split("/posts/")[-1].split("_")[0] if "/posts/" in posts[0] else "posts")
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet)
    ecrire_csv(lignes, sortie)
    nc = sum(1 for l in lignes if l["signal_type"] == "commentaire")
    afficher(f"{len(lignes)} engagement(s) sur {len(posts)} post(s) : {nc} commentaires, {len(lignes) - nc} reactions -> {sortie}")


if __name__ == "__main__":
    main()
