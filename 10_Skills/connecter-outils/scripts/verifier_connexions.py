"""Teste chaque cle du .env avec un appel gratuit, puis (option) coche OUTILS.md.

Usage :
    python3 verifier_connexions.py                          teste tout ce qui est present dans .env
    python3 verifier_connexions.py --outil unipile          un seul outil
    python3 verifier_connexions.py --ecrire-outils          met a jour "Etat des connexions" + priorite/canaux/crm
    python3 verifier_connexions.py --set CLE=VALEUR         ecrit (ou remplace) une ligne du .env, sans l'afficher
    python3 verifier_connexions.py --canal-linkedin lemlist --ecrire-outils

Outils : apify, unipile, crustdata, fullenrich, ocean, lemlist, hubspot, salesnav (cookies pour Apify).
Aucune valeur de cle n'est jamais affichee.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

_ici = Path(__file__).resolve()
_racine = next(p for p in _ici.parents if (p / "CLAUDE.md").exists() and (p / "10_Skills").is_dir())
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import dossier_gtm, Crustdata, FullEnrich, HubSpot, Unipile, afficher, env, http, load_env, racine  # noqa: E402

OUTILS_LIBELLES = {"apify": "Apify", "unipile": "Unipile", "crustdata": "Crustdata", "fullenrich": "FullEnrich",
                   "ocean": "Ocean.io", "lemlist": "Lemlist", "hubspot": "HubSpot"}


def set_env(cle: str, valeur: str) -> None:
    """Ecrit CLE=VALEUR dans <racine>/.env (cree le fichier depuis .env.example si besoin)."""
    fichier = racine() / ".env"
    if not fichier.exists():
        modele = racine() / ".env.example"
        fichier.write_text(modele.read_text(encoding="utf-8") if modele.exists() else "", encoding="utf-8")
    lignes = fichier.read_text(encoding="utf-8").splitlines()
    fait = False
    for i, l in enumerate(lignes):
        if l.strip().startswith(f"{cle}="):
            lignes[i] = f"{cle}={valeur}"
            fait = True
    if not fait:
        lignes.append(f"{cle}={valeur}")
    fichier.write_text("\n".join(lignes).rstrip("\n") + "\n", encoding="utf-8")
    afficher(f"[env] {cle} ecrit dans {fichier}")


def tester_apify() -> tuple[bool, str]:
    st, corps = http("GET", "https://api.apify.com/v2/users/me", params={"token": env("APIFY_TOKEN")})
    if st != 200:
        return False, f"HTTP {st}"
    d = corps.get("data", {})
    return True, f"compte {d.get('username')}, plan {(d.get('plan') or {}).get('tier', '?')}"


def tester_unipile() -> tuple[bool, str]:
    u = Unipile(exiger_compte=False)
    comptes = u.comptes()
    li = [c for c in comptes if (c.get("type") or "").upper() == "LINKEDIN"]
    if not li:
        return False, "aucun compte LinkedIn connecte dans Unipile (dashboard > Accounts > Connect)"
    c = li[0]
    statut = (c.get("sources") or [{}])[0].get("status") or c.get("status") or "?"
    own = ((c.get("connection_params") or {}).get("im") or {}).get("id") or ""
    if not env("UNIPILE_ACCOUNT_ID", obligatoire=False):
        set_env("UNIPILE_ACCOUNT_ID", c.get("id", ""))
    if own and not env("UNIPILE_OWN_PROVIDER_ID", obligatoire=False):
        set_env("UNIPILE_OWN_PROVIDER_ID", own)
    ok = str(statut).upper() == "OK"
    return ok, f"compte LinkedIn {c.get('name') or c.get('id')}, statut {statut}"


def tester_crustdata() -> tuple[bool, str]:
    return True, f"{Crustdata().credits()} credits"


def tester_fullenrich() -> tuple[bool, str]:
    return True, f"{FullEnrich().credits()} credits"


def tester_ocean() -> tuple[bool, str]:
    st, corps = http("GET", "https://api.ocean.io/v2/credits/balance", params={"apiToken": env("OCEAN_API_KEY")})
    if st != 200:
        return False, f"HTTP {st}"
    solde = corps.get("balance") if isinstance(corps, dict) else corps
    return True, f"solde {solde if solde is not None else corps} credits (appel gratuit)"


def tester_lemlist() -> tuple[bool, str]:
    cle = env("LEMLIST_API_KEY", obligatoire=False)
    if not cle:
        return True, "pas de cle dans .env : connexion par MCP OAuth (claude mcp add --transport http lemlist https://app.lemlist.com/mcp)"
    st, corps = http("GET", "https://api.lemlist.com/api/team", auth=("", cle))
    if st != 200:
        return False, f"HTTP {st}"
    return True, f"equipe {corps.get('name') or corps.get('_id')}"


def tester_hubspot() -> tuple[bool, str]:
    HubSpot().test()
    return True, "token Private App valide (lecture contacts)"


def tester_salesnav() -> tuple[bool, str]:
    li_at = env("LINKEDIN_LI_AT", obligatoire=False)
    ua = env("LINKEDIN_USER_AGENT", obligatoire=False)
    fichier = env("LINKEDIN_COOKIES_FILE", obligatoire=False)
    if fichier and Path(fichier).exists() and ua:
        return True, "export complet de cookies + user agent presents (non testes : un test = un run payant)"
    if li_at and ua:
        return True, "li_at + user agent presents" + (" + li_a" if env("LINKEDIN_LI_A", obligatoire=False) else " (li_a manquant : pas de Sales Nav)")
    return False, "LINKEDIN_LI_AT et LINKEDIN_USER_AGENT manquants (ou LINKEDIN_COOKIES_FILE)"


TESTS = {"apify": tester_apify, "unipile": tester_unipile, "crustdata": tester_crustdata,
         "fullenrich": tester_fullenrich, "ocean": tester_ocean, "lemlist": tester_lemlist,
         "hubspot": tester_hubspot, "salesnav": tester_salesnav}
CLES = {"apify": "APIFY_TOKEN", "unipile": "UNIPILE_API_KEY", "crustdata": "CRUSTDATA_API_KEY",
        "fullenrich": "FULLENRICH_API_KEY", "ocean": "OCEAN_API_KEY", "lemlist": "LEMLIST_API_KEY",
        "hubspot": "HUBSPOT_ACCESS_TOKEN", "salesnav": "LINKEDIN_LI_AT"}


def ecrire_outils(resultats: dict, canal_linkedin: str | None) -> None:
    p = dossier_gtm() / "OUTILS.md"
    t = p.read_text(encoding="utf-8")
    jour = date.today().isoformat()
    for outil, lib in OUTILS_LIBELLES.items():
        ok, detail = resultats.get(outil, (None, ""))
        if ok is None:
            continue
        case = "[x]" if ok else "[ ]"
        ligne = f"| {lib} | {case} | {jour} | {detail} |"
        t, n = re.subn(rf"^\| {re.escape(lib)} \|.*$", ligne, t, count=1, flags=re.M)
        if not n:
            t = t.rstrip("\n") + "\n" + ligne + "\n"
    priorite = "apify" if resultats.get("apify", (False, ""))[0] else "api"
    unipile_ok = resultats.get("unipile", (False, ""))[0]
    if not canal_linkedin:
        canal_linkedin = "unipile" if unipile_ok else "lemlist"
    crm = "hubspot" if resultats.get("hubspot", (False, ""))[0] else "aucun"
    for cle, val in (("priorite", priorite), ("canal_linkedin", canal_linkedin), ("canal_email", "lemlist"), ("crm", crm)):
        t = re.sub(rf"^{cle}:.*$", f"{cle}: {val}", t, count=1, flags=re.M)
    p.write_text(t, encoding="utf-8")
    afficher(f"[outils] OUTILS.md mis a jour : priorite={priorite}, canal_linkedin={canal_linkedin}, canal_email=lemlist, crm={crm}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outil", choices=sorted(TESTS), help="ne tester qu'un outil")
    ap.add_argument("--ecrire-outils", action="store_true", help="cocher OUTILS.md et ecrire priorite/canaux/crm")
    ap.add_argument("--canal-linkedin", choices=["unipile", "lemlist"], help="canal LinkedIn choisi a l'onboarding")
    ap.add_argument("--set", metavar="CLE=VALEUR", help="ecrire une variable dans .env (jamais affichee)")
    a = ap.parse_args()

    if a.set:
        if "=" not in a.set:
            ap.error("--set attend CLE=VALEUR")
        k, v = a.set.split("=", 1)
        set_env(k.strip(), v.strip())
        return

    load_env()
    resultats = {}
    for outil, test in TESTS.items():
        if a.outil and outil != a.outil:
            continue
        if not env(CLES[outil], obligatoire=False) and outil not in ("lemlist", "salesnav"):
            afficher(f"  {outil:11s} : pas de cle dans .env, ignore")
            continue
        try:
            ok, detail = test()
        except SystemExit:
            raise
        except Exception as e:  # une cle fausse ne doit pas arreter les autres tests
            ok, detail = False, str(e)[:160]
        resultats[outil] = (ok, detail)
        afficher(f"  {outil:11s} : {'OK ' if ok else 'KO '} {detail}")
    if a.ecrire_outils:
        ecrire_outils(resultats, a.canal_linkedin)


if __name__ == "__main__":
    main()
