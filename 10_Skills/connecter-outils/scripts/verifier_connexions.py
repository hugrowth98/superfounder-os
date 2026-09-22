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
import json
import re
import sys
from datetime import date
from pathlib import Path

_ici = Path(__file__).resolve()
_racine = next(p for p in _ici.parents if (p / "CLAUDE.md").exists() and (p / "10_Skills").is_dir())
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import dossier_gtm, Crustdata, FullEnrich, HubSpot, PredictLeads, Prospeo, Publora, TheirStack, Unipile, afficher, env, http, load_env, racine  # noqa: E402

OUTILS_LIBELLES = {"apify": "Apify", "unipile": "Unipile", "crustdata": "Crustdata", "fullenrich": "FullEnrich",
                   "ocean": "Ocean.io", "lemlist": "Lemlist", "hubspot": "HubSpot", "prospeo": "Prospeo",
                   "predictleads": "PredictLeads", "theirstack": "TheirStack", "publora": "Publora"}


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
    st, corps = http("GET", "https://api.ocean.io/api/public_api/v2/credits/balance", headers={"X-Api-Token": env("OCEAN_API_KEY")})
    if st != 200:
        return False, f"HTTP {st}"
    c = (corps.get("credits") or {}) if isinstance(corps, dict) else {}
    return True, f"solde {(c.get('recurrent') or 0) + (c.get('oneTime') or 0)} credits (recurrents {c.get('recurrent', 0)}, ponctuels {c.get('oneTime', 0)} ; appel gratuit)"


def tester_lemlist() -> tuple[bool, str]:
    cle = env("LEMLIST_API_KEY", obligatoire=False)
    if not cle:
        return False, "LEMLIST_API_KEY absente : l'envoi et la lecture des reponses passent par l'API (cle sur app.lemlist.com, Settings, Integrations)"
    st, corps = http("GET", "https://api.lemlist.com/api/team", auth=("", cle))
    if st != 200:
        return False, f"HTTP {st}"
    return True, f"equipe {corps.get('name') or corps.get('_id')}"


def tester_hubspot() -> tuple[bool, str]:
    HubSpot().test()
    return True, "token Private App valide (lecture contacts)"


def tester_predictleads() -> tuple[bool, str]:
    rep = PredictLeads().test()
    attrs = ((rep.get("data") or {}).get("attributes") if isinstance(rep.get("data"), dict) else {}) or {}
    return True, "cle + token valides" + (f" (abonnement : {attrs.get('plan') or attrs.get('name') or 'actif'})" if attrs else "")


def tester_theirstack() -> tuple[bool, str]:
    TheirStack().test()
    return True, "cle valide (recherche floutee, aucun credit consomme)"


def tester_prospeo() -> tuple[bool, str]:
    c = Prospeo().compte()
    return True, f"{c.get('remaining_credits', '?')} credits restants, plan {c.get('current_plan', '?')} (appel gratuit)"


def tester_publora() -> tuple[bool, str]:
    comptes = Publora().comptes()
    li = [c for c in comptes if str(c.get("platformId", "")).startswith("linkedin")]
    if not li:
        return True, f"cle valide, {len(comptes)} compte(s) connecte(s) mais aucun LinkedIn : connectez-le dans le tableau de bord Publora"
    return True, "cle valide, LinkedIn : " + ", ".join(f"{c.get('displayName') or c.get('username')} ({c.get('tokenStatus', '?')})" for c in li) + " (appel gratuit)"


def tester_salesnav() -> tuple[bool, str]:
    fichier = env("LINKEDIN_COOKIES_FILE", obligatoire=False) or str(racine() / ".linkedin-cookies.json")
    try:
        import browser_cookie3  # noqa: F401
        auto = True
    except ImportError:
        auto = False
    if auto:
        return True, "browser_cookie3 installe : cookies et user agent relus dans le navigateur avant chaque run (non testes : un test = un run payant)"
    ua = env("LINKEDIN_USER_AGENT", obligatoire=False)
    if Path(fichier).exists():
        data = json.loads(Path(fichier).read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("userAgent") or ua:
            return True, f"export complet de cookies + user agent presents dans {Path(fichier).name} (pas de rafraichissement auto : pip3 install browser_cookie3)"
    if env("LINKEDIN_LI_AT", obligatoire=False) and ua:
        return True, "li_at + user agent presents" + (" + li_a" if env("LINKEDIN_LI_A", obligatoire=False) else " (li_a manquant : pas de Sales Nav)") + " ; conseil : pip3 install browser_cookie3 pour les relire automatiquement"
    return False, "ni browser_cookie3, ni LINKEDIN_COOKIES_FILE, ni LINKEDIN_LI_AT + LINKEDIN_USER_AGENT"


TESTS = {"apify": tester_apify, "unipile": tester_unipile, "crustdata": tester_crustdata,
         "fullenrich": tester_fullenrich, "ocean": tester_ocean, "lemlist": tester_lemlist,
         "hubspot": tester_hubspot, "salesnav": tester_salesnav, "prospeo": tester_prospeo,
         "predictleads": tester_predictleads, "theirstack": tester_theirstack, "publora": tester_publora}
CLES = {"apify": "APIFY_TOKEN", "unipile": "UNIPILE_API_KEY", "crustdata": "CRUSTDATA_API_KEY",
        "fullenrich": "FULLENRICH_API_KEY", "ocean": "OCEAN_API_KEY", "lemlist": "LEMLIST_API_KEY",
        "hubspot": "HUBSPOT_ACCESS_TOKEN", "salesnav": "LINKEDIN_LI_AT", "prospeo": "PROSPEO_API_KEY",
        "predictleads": "PREDICTLEADS_API_KEY", "theirstack": "THEIRSTACK_API_KEY", "publora": "PUBLORA_API_KEY"}


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
    secours = [o for o in ("predictleads", "theirstack") if resultats.get(o, (False, ""))[0]]
    signaux_secours = ", ".join(secours) if secours else "aucun"
    for cle, val in (("priorite", priorite), ("canal_linkedin", canal_linkedin), ("canal_email", "lemlist"), ("crm", crm), ("signaux_secours", signaux_secours)):
        t = re.sub(rf"^{cle}:.*$", f"{cle}: {val}", t, count=1, flags=re.M)
    p.write_text(t, encoding="utf-8")
    afficher(f"[outils] OUTILS.md mis a jour : priorite={priorite}, canal_linkedin={canal_linkedin}, canal_email=lemlist, crm={crm}, signaux_secours={signaux_secours}")


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
