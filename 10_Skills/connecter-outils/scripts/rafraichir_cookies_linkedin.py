#!/usr/bin/env python3
"""Rafraichit les cookies LinkedIn pour les actors Apify Sales Navigator depuis le navigateur local.

Lit les cookies linkedin.com de tous les profils Chrome, Arc, Brave et Edge (dechiffres par le
trousseau du systeme), choisit la session Sales Navigator (cookie `li_a`) la plus fraiche, ou le
compte donne par LINKEDIN_CHROME_ACCOUNT dans .env, et ecrit un fichier JSON
{"userAgent": ..., "cookie": [...]} au format Cookie-Editor attendu par
curious_coder/linkedin-sales-navigator-search-scraper. Le user agent est construit depuis la
version reelle de Chrome : un user agent perime fait renouveler la session par LinkedIn (la page 1
passe, la page 2 repond "Cookies are expired").

Le fichier va a LINKEDIN_COOKIES_FILE (.env), sinon <racine>/.linkedin-cookies.json (ignore par git).
Les scripts trouver-personnes et trouver-entreprises l'appellent avant chaque run Apify Sales Navigator.
Aucune valeur de cookie n'est affichee.

Usage :
  python3 rafraichir_cookies_linkedin.py            met a jour le fichier
  python3 rafraichir_cookies_linkedin.py --check    montre les sessions trouvees sans ecrire
  python3 rafraichir_cookies_linkedin.py --compte moi@entreprise.com

Prerequis : pip3 install browser_cookie3
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import env, racine  # noqa: E402

try:
    import browser_cookie3 as bc3
except ImportError:
    sys.exit("browser_cookie3 manquant : pip3 install browser_cookie3")

REQUIS = {"li_at", "JSESSIONID"}
DOMAINES = {".linkedin.com", ".www.linkedin.com", "www.linkedin.com"}  # pas les sous-domaines pays
NAVIGATEURS = {
    "chrome": ["~/Library/Application Support/Google/Chrome", "~/.config/google-chrome",
               "~/AppData/Local/Google/Chrome/User Data"],
    "arc": ["~/Library/Application Support/Arc/User Data"],
    "brave": ["~/Library/Application Support/BraveSoftware/Brave-Browser", "~/.config/BraveSoftware/Brave-Browser",
              "~/AppData/Local/BraveSoftware/Brave-Browser/User Data"],
    "edge": ["~/Library/Application Support/Microsoft Edge", "~/.config/microsoft-edge",
             "~/AppData/Local/Microsoft/Edge/User Data"],
}


def base_de(navigateur: str) -> Path | None:
    for p in NAVIGATEURS[navigateur]:
        if Path(p).expanduser().exists():
            return Path(p).expanduser()
    return None


def profils(navigateur: str) -> list[tuple[str, str, Path]]:
    """(label, compte, fichier Cookies) pour chaque profil du navigateur."""
    base = base_de(navigateur)
    if base is None:
        return []
    try:
        cache = json.loads((base / "Local State").read_text(encoding="utf-8"))["profile"]["info_cache"]
    except Exception:
        cache = {}
    out = []
    for f in sorted(list(base.glob("*/Cookies")) + list(base.glob("*/Network/Cookies"))):
        prof = f.parent.name if f.parent.name != "Network" else f.parent.parent.name
        info = cache.get(prof, {})
        out.append((f"{navigateur}/{info.get('name') or prof}", info.get("user_name", ""), f))
    return out


def lire(navigateur: str, fichier: Path) -> list:
    try:
        return list(getattr(bc3, navigateur)(cookie_file=str(fichier), domain_name="linkedin.com"))
    except Exception as e:  # base verrouillee, trousseau refuse, navigateur non supporte
        print(f"  {navigateur} ({fichier.parent.name}) : {type(e).__name__}: {str(e)[:80]}")
        return []


def user_agent(navigateur: str) -> str:
    base = base_de(navigateur)
    version = ""
    if base and (base / "Last Version").exists():
        version = (base / "Last Version").read_text(encoding="utf-8").strip().split(".")[0]
    major = version or "130"
    plateforme = "Macintosh; Intel Mac OS X 10_15_7" if sys.platform == "darwin" else \
        "Windows NT 10.0; Win64; x64" if sys.platform.startswith("win") else "X11; Linux x86_64"
    return f"Mozilla/5.0 ({plateforme}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major}.0.0.0 Safari/537.36"


def au_format_cookie_editor(c) -> dict:
    domaine = c.domain or ".linkedin.com"
    return {"domain": domaine, "expirationDate": float(c.expires) if c.expires else None,
            "hostOnly": not domaine.startswith("."), "httpOnly": False, "name": c.name, "path": c.path or "/",
            "sameSite": "unspecified", "secure": bool(c.secure), "session": c.expires is None, "storeId": "0",
            "value": c.value}


def trouver_session(compte: str, seulement: str | None):
    trouves = []
    print("Sessions LinkedIn dans les navigateurs :")
    for nav in ([seulement] if seulement else NAVIGATEURS):
        for label, user, fichier in profils(nav):
            jar = lire(nav, fichier)
            noms = {c.name: c for c in jar}
            if not REQUIS <= noms.keys():
                continue
            score = (bool(compte) and user == compte, "li_a" in noms, noms["li_at"].expires or 0)
            print(f"  {label} ({user or 'sans compte'}) : {len(jar)} cookies, Sales Navigator : {'oui' if 'li_a' in noms else 'non'}")
            trouves.append((score, nav, label, jar))
    if not trouves:
        return None, None, None
    trouves.sort(key=lambda t: t[0], reverse=True)
    _, nav, label, jar = trouves[0]
    return nav, label, jar


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--compte", default=env("LINKEDIN_CHROME_ACCOUNT", obligatoire=False),
                    help="email du profil navigateur a privilegier (LINKEDIN_CHROME_ACCOUNT dans .env)")
    ap.add_argument("--navigateur", choices=list(NAVIGATEURS))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--silencieux", action="store_true", help="une ligne de sortie, pour l'appel depuis un autre script")
    a = ap.parse_args()

    if a.silencieux:
        sys.stdout = open("/dev/null", "w") if sys.platform != "win32" else open("nul", "w")
    nav, label, jar = trouver_session(a.compte, a.navigateur)
    if not jar:
        print("Aucun profil avec une session LinkedIn. Connectez-vous a LinkedIn dans votre navigateur puis relancez.")
        sys.exit(1)

    vus = {}
    for c in jar:
        vus[(c.name, c.domain, c.path)] = c
    maintenant = dt.datetime.now().timestamp()
    cookies = [au_format_cookie_editor(c) for c in vus.values()]
    cookies = [c for c in cookies if c["domain"] in DOMAINES and (c["expirationDate"] is None or c["expirationDate"] > maintenant)]
    li_at = next(c for c in cookies if c["name"] == "li_at")
    expire = dt.datetime.fromtimestamp(li_at["expirationDate"]).strftime("%Y-%m-%d") if li_at["expirationDate"] else "session"
    ua = user_agent(nav)
    print(f"\nProfil retenu : {label}\nCookies : {len(cookies)}\nli_at expire le : {expire}\nUser agent : Chrome/{ua.split('Chrome/')[1].split('.')[0]}")
    if a.check:
        return

    cible = Path(env("LINKEDIN_COOKIES_FILE", obligatoire=False) or racine() / ".linkedin-cookies.json")
    cible.write_text(json.dumps({"_maj": dt.date.today().isoformat(), "_profil": label, "userAgent": ua, "cookie": cookies},
                                ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        cible.chmod(0o600)
    except OSError:
        pass
    print(f"Ecrit : {cible}")
    if a.silencieux:
        sys.stdout = sys.__stdout__
        print(f"cookies LinkedIn rafraichis depuis {label} (li_at valable jusqu'au {expire}, user agent Chrome/{ua.split('Chrome/')[1].split('.')[0]})")


if __name__ == "__main__":
    main()
