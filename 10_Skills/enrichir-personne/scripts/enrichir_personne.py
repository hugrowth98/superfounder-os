"""enrichir_personne : complete un CSV de personnes avec le profil LinkedIn (Unipile, ou Apify en secours)
puis, sur demande, le contact verifie (FullEnrich : email pro, mobile).

Usage :
  python3 enrichir_personne.py --in liste.csv                       profil LinkedIn via Unipile (lignes avec linkedin_url)
  python3 enrichir_personne.py --in liste.csv --source apify         profil via Apify harvestapi/linkedin-profile-scraper (0,004 $/profil)
  python3 enrichir_personne.py --in liste.csv --contact              + email pro FullEnrich (1 credit par email trouve)
  python3 enrichir_personne.py --in liste.csv --contact --telephone  + mobile FullEnrich (10 credits par mobile trouve)
  python3 enrichir_personne.py --in liste.csv --max 50 --dry-run     montre ce qui serait fait et le cout

Regle : on ne relance que ce qui est vide (profil deja enrichi = ligne avec `date_enrichissement`, email deja
present = pas d'appel FullEnrich). --force ignore la regle. Sortie : Listes-prospection/enrichir-personne_<sujet>_<date>.csv
(le fichier d'entree n'est jamais ecrase).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (FullEnrich, Unipile, afficher, aujourd_hui, arret, bandeau_dry_run, chemin_sortie, domaine,  # noqa: E402
                        ecrire_csv, lire_csv, norm_linkedin_url, seniorite_depuis_titre, slug_linkedin, sujet_depuis_fichier)
from apify_run import lancer, prix  # noqa: E402

VERBE = "enrichir-personne"


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


def _periode(p: dict) -> str:
    deb = _g(p, "start", "startDate.text", "start_date")
    fin = _g(p, "end", "endDate.text", "end_date") or "aujourd'hui"
    if isinstance(deb, dict):
        deb = f"{deb.get('month', '')}/{deb.get('year', '')}".strip("/")
    if isinstance(fin, dict):
        fin = f"{fin.get('month', '')}/{fin.get('year', '')}".strip("/")
    return f"{deb} -> {fin}" if deb else ""


def fusion_profil(ligne: dict, prof: dict, source: str) -> None:
    """Ecrit dans la ligne ce que le profil apporte, sans ecraser une valeur deja presente sauf le titre."""
    exp = prof.get("work_experience") or prof.get("experience") or prof.get("positions") or []
    exp = [e for e in exp if isinstance(e, dict)]
    courant = prof.get("currentPosition") or prof.get("current_positions") or []
    courant = courant[0] if isinstance(courant, list) and courant else (courant if isinstance(courant, dict) else (exp[0] if exp else {}))
    titre = _g(courant, "position", "title", "role") or _g(prof, "headline")
    maj = {
        "prenom": _g(prof, "first_name", "firstName"), "nom": _g(prof, "last_name", "lastName"),
        "titre": titre, "entreprise": _g(courant, "company", "companyName", "company_name"),
        "linkedin_entreprise_url": norm_linkedin_url(_g(courant, "companyLinkedinUrl", "company_linkedin_url", "company_url")),
        "ville": _g(prof, "location.parsed.city") or (_g(prof, "location") if isinstance(prof.get("location"), str) else ""),
        "pays": _g(prof, "location.parsed.country"),
        "linkedin_url": norm_linkedin_url(_g(prof, "linkedinUrl", "public_profile_url")) or
        (f"https://www.linkedin.com/in/{_g(prof, 'public_identifier', 'publicIdentifier')}" if _g(prof, "public_identifier", "publicIdentifier") else ""),
        "headline": _g(prof, "headline"), "resume": (_g(prof, "summary", "about") or "")[:500],
        "anciennete_poste": _periode(courant), "nb_relations": _g(prof, "connections_count", "connectionsCount"),
        "abonnes": _g(prof, "follower_count", "followerCount"),
        "degre_relation": _g(prof, "network_distance"),
        "provider_id": _g(prof, "provider_id", "id") if source == "unipile" else "",
        "experiences": " | ".join(f"{_g(e, 'position', 'title')} chez {_g(e, 'company', 'companyName')} ({_periode(e)})" for e in exp[:4]),
        "formation": " | ".join(f"{_g(e, 'school', 'schoolName')} {_g(e, 'degree')}".strip() for e in (prof.get("education") or [])[:2] if isinstance(e, dict)),
        "competences": " | ".join((_g(s, "name") if isinstance(s, dict) else str(s)) for s in (prof.get("skills") or [])[:10]),
        "langues": " | ".join((_g(l, "name") if isinstance(l, dict) else str(l)) for l in (prof.get("languages") or [])[:5]),
        "ouvert_au_poste": "oui" if prof.get("openToWork") or prof.get("open_to_work") else "",
        "recrute": "oui" if prof.get("hiring") else "",
    }
    ci = prof.get("contact_info") or {}
    emails = ci.get("emails") or prof.get("emails") or []
    if emails and not ligne.get("email"):
        e0 = emails[0]
        maj["email"] = e0 if isinstance(e0, str) else _g(e0, "email", "value")
        maj["email_statut"] = "LINKEDIN_1ER_DEGRE" if source == "unipile" else "APIFY_NON_VERIFIE"
    phones = ci.get("phones") or []
    if phones and not ligne.get("telephone"):
        p0 = phones[0]
        maj["telephone"] = p0 if isinstance(p0, str) else _g(p0, "number", "value")
    for k, v in maj.items():
        if v and (k == "titre" or not (ligne.get(k) or "").strip()):
            ligne[k] = v
    if ligne.get("titre") and not ligne.get("seniorite"):
        ligne["seniorite"] = seniorite_depuis_titre(ligne["titre"])
    if ligne.get("email") and not ligne.get("domaine"):
        d = domaine(ligne["email"])
        if d and d not in ("gmail.com", "hotmail.com", "yahoo.fr", "outlook.com", "icloud.com"):
            ligne["domaine"] = d
    ligne["date_enrichissement"] = aujourd_hui()
    ligne["source"] = (ligne.get("source") or "") + (f"+{source}" if ligne.get("source") else source)


def profils_unipile(lignes: list[dict], cibles: list[int], dry_run: bool, pause: float) -> int:
    if dry_run:
        bandeau_dry_run("Unipile GET /api/v1/users/{identifiant}", [f"{len(cibles)} profil(s) a lire, une requete par profil, pause {pause}s",
                                                                    "cout : abonnement Unipile ; chaque lecture compte comme une vue de profil sur le compte LinkedIn"])
        return 0
    u = Unipile()
    ok = 0
    for n, i in enumerate(cibles, 1):
        l = lignes[i]
        ident = slug_linkedin(l.get("linkedin_url")) or l.get("provider_id")
        try:
            prof = u.profil(ident)
            fusion_profil(l, prof, "unipile")
            ok += 1
        except Exception as e:
            l["erreur_enrichissement"] = str(e)[:120]
        if n % 10 == 0:
            afficher(f"  [unipile] {n}/{len(cibles)} profils lus")
        time.sleep(pause)
    return ok


def profils_apify(lignes: list[dict], cibles: list[int], dry_run: bool) -> int:
    urls = [norm_linkedin_url(lignes[i].get("linkedin_url")) for i in cibles]
    urls = [u for u in urls if u]
    actor = "harvestapi/linkedin-profile-scraper"
    items, _ = lancer(actor, {"urls": urls, "profileScraperMode": "Profile details no email ($4 per 1k)"},
                      label="profile-scraper", dry_run=dry_run, estimation=prix(actor, len(urls)))
    if dry_run:
        return 0
    par_url = {norm_linkedin_url(_g(it, "linkedinUrl") or f"https://www.linkedin.com/in/{_g(it, 'publicIdentifier')}"): it for it in items}
    ok = 0
    for i in cibles:
        prof = par_url.get(norm_linkedin_url(lignes[i].get("linkedin_url")))
        if prof:
            fusion_profil(lignes[i], prof, actor)
            ok += 1
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True)
    ap.add_argument("--source", choices=["unipile", "apify"], default="unipile", help="outil pour le profil (defaut unipile)")
    ap.add_argument("--contact", action="store_true", help="ajouter l'email pro via FullEnrich")
    ap.add_argument("--telephone", action="store_true", help="ajouter le mobile via FullEnrich (10 credits par mobile)")
    ap.add_argument("--sans-profil", action="store_true", help="ne faire que la partie contact")
    ap.add_argument("--max", type=int, help="nombre de lignes a traiter dans ce run")
    ap.add_argument("--pause", type=float, default=1.5, help="unipile : secondes entre deux profils")
    ap.add_argument("--force", action="store_true", help="re-enrichir meme ce qui est deja rempli")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    lignes = lire_csv(a.entree)
    sujet = sujet_depuis_fichier(a.entree, a.sujet)
    if not a.sans_profil:
        cibles = [i for i, l in enumerate(lignes)
                  if (norm_linkedin_url(l.get("linkedin_url")) or l.get("provider_id")) and (a.force or not l.get("date_enrichissement"))]
        if a.max:
            cibles = cibles[:a.max]
        afficher(f"  [profil] {len(cibles)} ligne(s) a enrichir sur {len(lignes)} ({a.source})")
        if cibles:
            ok = profils_unipile(lignes, cibles, a.dry_run, a.pause) if a.source == "unipile" else profils_apify(lignes, cibles, a.dry_run)
            if not a.dry_run:
                afficher(f"  [profil] {ok} profil(s) enrichi(s)")
    if a.contact or a.telephone:
        champs = (["contact.emails"] if a.contact else []) + (["contact.phones"] if a.telephone else [])
        stats = FullEnrich(exiger_cle=not a.dry_run).enrichir_lignes(lignes, champs, forcer=a.force, dry_run=a.dry_run, nom=f"enrichir-personne {sujet}", maximum=a.max)
        if a.telephone and not a.dry_run:
            afficher(f"  [contact] {stats}")
    if a.dry_run:
        return
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet)
    ecrire_csv(lignes, sortie)
    afficher(f"{len(lignes)} lignes -> {sortie}")


if __name__ == "__main__":
    main()
