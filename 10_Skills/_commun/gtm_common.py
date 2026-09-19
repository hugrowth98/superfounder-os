"""Bibliotheque commune des skills d'execution du module GTM.

Tous les scripts de 10_Skills/*/scripts/ l'importent. Elle sait :
  - retrouver la racine du module GTM (le dossier qui contient OUTILS.md) et lire son .env
  - lire les choix de OUTILS.md (priorite, canal_linkedin, canal_email, crm)
  - lire et ecrire des CSV UTF-8 aux colonnes normalisees (CONVENTIONS.md section 8)
  - parler aux APIs de la stack avec `requests` uniquement : Unipile, FullEnrich, Crustdata, HubSpot

Python 3.9+ (ecrit pour 3.10, sans syntaxe exclusive). Aucune cle en dur : tout vient du .env.

Amorce a copier en tete de chaque script :

    import sys
    from pathlib import Path
    _racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
    if _racine is None:
        sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
    sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
    from gtm_common import *
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import unicodedata
import warnings
from datetime import date, datetime
from pathlib import Path

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")
try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("Le module 'requests' manque : pip3 install requests")

__all__ = [
    "COLONNES", "racine", "dossier_gtm", "load_env", "env", "lire_outils", "dossier_listes", "chemin_sortie",
    "slug", "norm_texte", "norm_linkedin_url", "slug_linkedin", "domaine", "aujourd_hui",
    "seniorite_depuis_titre", "sujet_depuis_fichier", "fraicheur", "lire_csv", "ecrire_csv", "http", "afficher", "bandeau_dry_run", "estimer",
    "Unipile", "FullEnrich", "Crustdata", "HubSpot", "extraire_post_id", "arret",
]

# Colonnes normalisees, dans cet ordre (CONVENTIONS.md section 8)
COLONNES = [
    "prenom", "nom", "titre", "seniorite", "entreprise", "domaine", "linkedin_url",
    "linkedin_entreprise_url", "email", "email_statut", "telephone", "ville", "pays", "secteur",
    "effectif", "source", "date_extraction", "score_icp", "tier", "signal_type", "signal_date",
    "signal_detail", "score_signal", "fraicheur", "exclu", "raison_exclusion", "ne_plus_contacter",
]

_RACINE: Path | None = None
_ENV_CHARGE = False


# ---------------------------------------------------------------- racine, .env, OUTILS.md

def racine(depuis: str | Path | None = None) -> Path:
    """La racine du workspace Superfounder OS : on remonte depuis ce fichier (ou `depuis`) jusqu'au
    dossier qui contient CLAUDE.md et 10_Skills/. Les reglages du module GTM sont dans
    05_Departements/Go-to-Market/ (OUTILS.md, contexte.md, GARDE-FOUS.md), le .env a la racine."""
    global _RACINE
    if _RACINE is not None and depuis is None:
        return _RACINE
    start = Path(depuis).resolve() if depuis else Path(__file__).resolve()
    for d in [start] + list(start.parents):
        if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir():
            if depuis is None:
                _RACINE = d
            return d
    arret("Racine introuvable : ce script doit vivre dans 10_Skills/ d'un workspace Superfounder OS (CLAUDE.md a la racine).")


def dossier_gtm() -> Path:
    """05_Departements/Go-to-Market/ : les reglages et les sorties du module GTM."""
    d = racine() / "05_Departements" / "Go-to-Market"
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_env() -> dict:
    """Charge <racine>/.env dans os.environ (sans ecraser une variable deja definie)."""
    global _ENV_CHARGE
    fichier = racine() / ".env"
    valeurs = {}
    if fichier.exists():
        for ligne in fichier.read_text(encoding="utf-8").splitlines():
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#") or "=" not in ligne:
                continue
            k, v = ligne.split("=", 1)
            k = k.strip().replace("export ", "")
            v = v.strip().strip('"').strip("'")
            valeurs[k] = v
            os.environ.setdefault(k, v)
    _ENV_CHARGE = True
    return valeurs


def env(nom: str, obligatoire: bool = True, aide: str = "") -> str:
    """Valeur d'une variable du .env. Si elle manque et qu'elle est obligatoire : arret propre
    avec le renvoi vers `connecter-outils`."""
    if not _ENV_CHARGE:
        load_env()
    val = os.environ.get(nom, "").strip()
    if not val and obligatoire:
        arret(f"{nom} absent du .env a la racine du workspace ({racine() / '.env'}). "
              f"Lancez `connecter-outils` pour brancher l'outil. {aide}".strip())
    return val


def lire_outils() -> dict:
    """Les quatre choix ecrits par connecter-outils dans OUTILS.md."""
    fichier = dossier_gtm() / "OUTILS.md"
    if not fichier.exists():
        arret(f"OUTILS.md introuvable ({fichier}). Lancez `connecter-outils`.")
    texte = fichier.read_text(encoding="utf-8")
    choix = {"priorite": "", "canal_linkedin": "", "canal_email": "", "crm": ""}
    for cle in choix:
        m = re.search(rf"^{cle}:\s*([a-zA-Z_-]+)", texte, re.M)
        if m and not m.group(1).startswith("["):
            choix[cle] = m.group(1).lower()
    return choix


def dossier_listes() -> Path:
    d = racine() / "05_Departements" / "Go-to-Market" / "Listes-prospection"
    d.mkdir(parents=True, exist_ok=True)
    return d


def chemin_sortie(verbe: str, sujet: str, suffixe: str = "", ext: str = ".csv") -> Path:
    """<verbe>_<sujet>_<YYYY-MM-DD>[_suffixe].csv dans Listes-prospection/."""
    nom = f"{verbe}_{slug(sujet) or 'run'}_{aujourd_hui()}"
    if suffixe:
        nom += f"_{slug(suffixe)}"
    return dossier_listes() / f"{nom}{ext}"


def sujet_depuis_fichier(chemin: str | Path, sujet: str = "") -> str:
    """Le <sujet> d'un fichier <verbe>_<sujet>_<date>.csv, ou le nom du fichier sinon."""
    if sujet:
        return sujet
    stem = Path(chemin).stem
    parts = stem.split("_")
    if len(parts) >= 3 and re.match(r"\d{4}-\d{2}-\d{2}", parts[-1]):
        return "_".join(parts[1:-1])
    if len(parts) >= 3 and re.match(r"\d{4}-\d{2}-\d{2}", parts[2]):
        return parts[1]
    return stem


# ---------------------------------------------------------------- texte, urls, dates

def norm_texte(s) -> str:
    """minuscule, sans accents, ponctuation remplacee par des espaces."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def slug(s) -> str:
    return re.sub(r"\s+", "-", norm_texte(s))[:60].strip("-")


def norm_linkedin_url(u) -> str:
    """https://www.linkedin.com/in/<slug> en minuscules, sans parametres ni slash final.
    Fonctionne aussi pour /company/ et /school/. Vide si ce n'est pas une URL LinkedIn."""
    if not u:
        return ""
    u = str(u).strip()
    m = re.search(r"linkedin\.com/(in|company|school|sales/lead|sales/company)/([^/?#]+)", u, re.I)
    if not m:
        return ""
    genre, ident = m.group(1).lower(), m.group(2)
    if genre == "sales/lead":
        genre = "in"
    if genre == "sales/company":
        genre = "company"
    ident = ident.split(",")[0]
    return f"https://www.linkedin.com/{genre}/{ident.lower()}"


def slug_linkedin(u) -> str:
    n = norm_linkedin_url(u)
    return n.rsplit("/", 1)[-1] if n else ""


def domaine(u) -> str:
    """'https://www.acme.fr/contact?x=1' -> 'acme.fr'. Accepte un email : renvoie son domaine."""
    if not u:
        return ""
    u = str(u).strip().lower()
    if "@" in u and " " not in u:
        return u.split("@", 1)[1]
    u = re.sub(r"^[a-z]+://", "", u)
    u = re.sub(r"^www\.", "", u)
    return u.split("/")[0].split("?")[0].split(":")[0]


def aujourd_hui() -> str:
    return date.today().isoformat()


def fraicheur(signal_date) -> str:
    """Nombre entier de jours ecoules depuis signal_date (YYYY-MM-DD ou ISO). Vide si pas de date."""
    s = str(signal_date or "")[:10]
    try:
        d = datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return ""
    return str(max(0, (date.today() - d).days))


_SENIORITES = [
    ("fondateur", r"\b(fondateur|fondatrice|founder|co ?founder|cofondat|owner|proprietaire|gerant|gerante|ceo|pdg|president|presidente|dirigeant|dirigeante|managing director|directeur general|directrice generale|chief executive)\b"),
    ("c_level", r"\b(c[a-z]o|chief [a-z]+ officer|directeur associe|directrice associee|managing partner|associe)\b"),
    ("vp", r"\b(vp|vice president|vice presidente|svp|evp)\b"),
    ("directeur", r"\b(directeur|directrice|director|dsi|drh|daf)\b"),
    ("head", r"\b(head of|head|responsable|lead)\b"),
    ("manager", r"\b(manager|chef de|charge de|chargee de)\b"),
    ("senior", r"\b(senior|expert|specialiste|specialist|consultant|consultante)\b"),
]


def seniorite_depuis_titre(titre) -> str:
    """Seniorite normalisee (fondateur, c_level, vp, directeur, head, manager, senior, autre)
    depuis un intitule de poste ou un headline. Regle simple, affinee par qualifier-liste."""
    t = " " + norm_texte(titre) + " "
    if not t.strip():
        return ""
    for nom, motif in _SENIORITES:
        if re.search(motif, t):
            return nom
    return "autre"


def extraire_post_id(url: str) -> str:
    """Id numerique d'un post LinkedIn depuis son URL (ou l'URN tel quel)."""
    if url.startswith("urn:li:"):
        return url
    m = re.search(r"(?:activity|share|ugcPost)[/:-](\d+)", url)
    if not m:
        raise ValueError(f"Impossible d'extraire l'id du post depuis : {url}")
    return m.group(1)


# ---------------------------------------------------------------- CSV

def lire_csv(chemin: str | Path) -> list[dict]:
    """Lit un CSV UTF-8 (avec ou sans BOM), separateur virgule ou point-virgule detecte."""
    p = Path(chemin)
    if not p.exists():
        arret(f"Fichier introuvable : {p}")
    with open(p, encoding="utf-8-sig", newline="") as fh:
        debut = fh.read(4096)
        fh.seek(0)
        sep = ";" if debut.count(";") > debut.count(",") else ","
        return [dict(r) for r in csv.DictReader(fh, delimiter=sep)]


def ecrire_csv(lignes: list[dict], chemin: str | Path, colonnes_extra: list[str] | None = None) -> Path:
    """Ecrit un CSV UTF-8 : d'abord les colonnes normalisees presentes, dans l'ordre du contrat,
    puis les colonnes supplementaires dans l'ordre de premiere apparition."""
    p = Path(chemin)
    p.parent.mkdir(parents=True, exist_ok=True)
    presentes = set()
    ordre_extra: list[str] = []
    for l in lignes:
        for k in l:
            presentes.add(k)
            if k not in COLONNES and k not in ordre_extra:
                ordre_extra.append(k)
    for k in colonnes_extra or []:
        if k not in ordre_extra and k not in COLONNES:
            ordre_extra.append(k)
    cols = [c for c in COLONNES if c in presentes] + ordre_extra
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for l in lignes:
            w.writerow({c: _plat(l.get(c)) for c in cols})
    return p


def _plat(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "oui" if v else "non"
    if isinstance(v, (list, tuple)):
        return " | ".join(_plat(x) for x in v if x not in (None, ""))
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False)
    return str(v).replace("\r", " ").replace("\n", " ").strip()


# ---------------------------------------------------------------- HTTP et affichage

def http(methode: str, url: str, headers: dict | None = None, params: dict | None = None,
         json_body=None, timeout: int = 60, essais: int = 3, auth=None):
    """Appel HTTP avec reprise sur 429 et 5xx. Renvoie (statut, corps decode ou texte)."""
    derniere = None
    for tentative in range(essais):
        try:
            r = requests.request(methode, url, headers=headers, params=params, json=json_body,
                                 timeout=timeout, auth=auth)
        except requests.RequestException as e:
            derniere = f"reseau : {e}"
            time.sleep(2 * (tentative + 1))
            continue
        if r.status_code == 429 or r.status_code >= 500:
            derniere = f"HTTP {r.status_code} : {r.text[:300]}"
            time.sleep(3 * (tentative + 1))
            continue
        try:
            corps = r.json() if r.text else {}
        except ValueError:
            corps = r.text
        return r.status_code, corps
    raise RuntimeError(f"{methode} {url} a echoue apres {essais} essais ({derniere})")


def afficher(msg: str) -> None:
    print(msg, flush=True)


def arret(msg: str) -> None:
    print(f"[stop] {msg}", file=sys.stderr, flush=True)
    sys.exit(1)


def bandeau_dry_run(titre: str, lignes: list[str]) -> None:
    afficher(f"[dry-run] {titre}")
    for l in lignes:
        afficher(f"          {l}")
    afficher("[dry-run] Aucun appel API effectue. Relancez sans --dry-run pour executer.")


def estimer(n: int, prix_unitaire: float, depart: float = 0.0, unite: str = "resultat") -> str:
    total = n * prix_unitaire + depart
    return f"{n} {unite}(s) x {prix_unitaire:.4f} $ + {depart:.3f} $ de depart = environ {total:.2f} $"


# ---------------------------------------------------------------- Unipile

class Unipile:
    """Client REST Unipile (compte LinkedIn de l'utilisateur). Cles : UNIPILE_API_KEY, UNIPILE_DSN,
    UNIPILE_ACCOUNT_ID (et UNIPILE_OWN_PROVIDER_ID pour distinguer nos messages des reponses)."""

    def __init__(self, exiger_compte: bool = True):
        self.dernier_total = None
        self.dsn = env("UNIPILE_DSN").rstrip("/")
        self.cle = env("UNIPILE_API_KEY")
        self.account_id = env("UNIPILE_ACCOUNT_ID", obligatoire=exiger_compte)
        self.own_provider_id = env("UNIPILE_OWN_PROVIDER_ID", obligatoire=False)

    def _h(self, json_: bool = False) -> dict:
        h = {"X-API-KEY": self.cle, "Accept": "application/json"}
        if json_:
            h["Content-Type"] = "application/json"
        return h

    def get(self, chemin: str, params: dict | None = None):
        params = {k: v for k, v in (params or {}).items() if v is not None}
        st, corps = http("GET", f"{self.dsn}{chemin}", headers=self._h(), params=params)
        if st >= 400:
            raise RuntimeError(f"Unipile GET {chemin} -> HTTP {st} : {str(corps)[:300]}")
        return corps

    def post(self, chemin: str, body: dict, params: dict | None = None):
        st, corps = http("POST", f"{self.dsn}{chemin}", headers=self._h(True), params=params, json_body=body)
        if st >= 400:
            raise RuntimeError(f"Unipile POST {chemin} -> HTTP {st} : {str(corps)[:300]}")
        return corps

    # comptes
    def comptes(self) -> list[dict]:
        data = self.get("/api/v1/accounts")
        return data.get("items", data if isinstance(data, list) else [])

    # recherche LinkedIn / Sales Navigator (meme endpoint, seul `api` change)
    def recherche(self, api: str = "sales_navigator", categorie: str = "people", url: str | None = None,
                  mots_cles: str | None = None, max_resultats: int = 100) -> list[dict]:
        items, cursor, iterations = [], None, 0
        page = 50 if api == "classic" else 100
        while len(items) < max_resultats and iterations < max_resultats + 50:
            iterations += 1
            body = {"api": api, "category": categorie, "limit": min(page, max_resultats - len(items))}
            if url:
                body["url"] = url
            if mots_cles:
                body["keywords"] = mots_cles
            if cursor:
                body["cursor"] = cursor
            data = self.post("/api/v1/linkedin/search", body, params={"account_id": self.account_id})
            lot = data.get("items", [])
            items.extend(lot)
            tot = (data.get("paging") or {}).get("total_count")
            if tot is not None:
                self.dernier_total = tot
            cursor = data.get("cursor") or (data.get("paging") or {}).get("cursor")
            if not cursor or not lot:
                break
        return items[:max_resultats]

    def profil(self, identifiant: str, complet: bool = True) -> dict:
        params = {"account_id": self.account_id}
        if complet:
            params["linkedin_sections"] = "*"
        return self.get(f"/api/v1/users/{identifiant}", params)

    def entreprise(self, identifiant: str) -> dict:
        try:
            return self.get(f"/api/v1/linkedin/company/{identifiant}", {"account_id": self.account_id})
        except RuntimeError as e:
            if "404" not in str(e):
                raise
            items = self.recherche(api="classic", categorie="companies", mots_cles=identifiant, max_resultats=5)
            if not items:
                raise RuntimeError(f"Entreprise introuvable, meme via recherche : {identifiant}") from e
            top = items[0]
            ident = slug_linkedin(top.get("profile_url") or top.get("linkedin_url") or "") or str(top.get("id"))
            return self.get(f"/api/v1/linkedin/company/{ident}", {"account_id": self.account_id})

    def _pages(self, chemin: str, max_pages: int, params_extra: dict | None = None) -> list[dict]:
        items, cursor, pages = [], None, 0
        while pages < max_pages:
            pages += 1
            params = {"account_id": self.account_id, "limit": 100}
            params.update(params_extra or {})
            if cursor:
                params["cursor"] = cursor
            data = self.get(chemin, params)
            lot = data.get("items", [])
            items.extend(lot)
            tot = (data.get("paging") or {}).get("total_count")
            if tot is not None:
                self.dernier_total = tot
            cursor = data.get("cursor") or (data.get("paging") or {}).get("cursor")
            if not cursor or not lot:
                break
        return items

    def reactions(self, post_id: str, max_pages: int = 10) -> list[dict]:
        return self._pages(f"/api/v1/posts/{post_id}/reactions", max_pages)

    def commentaires(self, post_id: str, max_pages: int = 10) -> list[dict]:
        return self._pages(f"/api/v1/posts/{post_id}/comments", max_pages)

    def chats(self, limite: int = 100) -> list[dict]:
        data = self.get("/api/v1/chats", {"account_id": self.account_id, "limit": limite})
        return data.get("items", data if isinstance(data, list) else [])

    def messages(self, chat_id: str, limite: int = 50) -> list[dict]:
        data = self.get(f"/api/v1/chats/{chat_id}/messages", {"limit": limite})
        return data.get("items", data if isinstance(data, list) else [])

    def participants(self, chat_id: str) -> list[dict]:
        data = self.get(f"/api/v1/chats/{chat_id}/attendees")
        return data.get("items", data if isinstance(data, list) else [])

    def inviter(self, provider_id: str, message: str | None = None) -> dict:
        body = {"account_id": self.account_id, "provider_id": provider_id}
        if message:
            body["message"] = message
        return self.post("/api/v1/users/invite", body)

    def envoyer_dm(self, provider_id: str, texte: str) -> dict:
        return self.post("/api/v1/chats", {"account_id": self.account_id, "attendees_ids": [provider_id], "text": texte})

    def repondants(self) -> list[dict]:
        """Conversations ou le dernier message ne vient pas de nous (donc le prospect a repondu)."""
        resultat = []
        for chat in self.chats():
            chat_id = chat.get("id")
            if not chat_id:
                continue
            msgs = self.messages(chat_id)
            if not msgs:
                continue
            dernier = msgs[-1] if msgs[-1].get("timestamp", "") >= msgs[0].get("timestamp", "") else msgs[0]
            de_nous = dernier.get("is_sender")
            if de_nous is None:
                exp = dernier.get("sender_id") or (dernier.get("sender") or {}).get("id")
                de_nous = bool(self.own_provider_id) and exp == self.own_provider_id
            if de_nous in (1, True):
                continue
            resultat.append({
                "chat_id": chat_id,
                "provider_id": chat.get("attendee_provider_id") or dernier.get("sender_id"),
                "nom_chat": chat.get("name"),
                "dernier_message": dernier.get("text"),
                "date_reponse": (dernier.get("timestamp") or "")[:10],
            })
        return resultat


# ---------------------------------------------------------------- FullEnrich

class FullEnrich:
    """Client FullEnrich v2. Cle : FULLENRICH_API_KEY. 1 credit par email pro trouve, 10 par mobile,
    facture seulement sur resultat trouve, gratuit si deja enrichi il y a moins de 3 mois."""
    BASE = "https://app.fullenrich.com/api/v2"

    def __init__(self, exiger_cle: bool = True):
        self.cle = env("FULLENRICH_API_KEY", obligatoire=exiger_cle)

    def _h(self) -> dict:
        if not self.cle:
            env("FULLENRICH_API_KEY")
        return {"Authorization": f"Bearer {self.cle}", "Content-Type": "application/json"}

    def _req(self, methode: str, chemin: str, body=None):
        st, corps = http(methode, f"{self.BASE}{chemin}", headers=self._h(), json_body=body)
        if st == 402:
            raise RuntimeError("FullEnrich : credits insuffisants (HTTP 402)")
        if st >= 400:
            raise RuntimeError(f"FullEnrich {methode} {chemin} -> HTTP {st} : {str(corps)[:300]}")
        return corps

    def credits(self) -> int:
        return int(self._req("GET", "/account/credits").get("balance", 0))

    def lancer(self, contacts: list[dict], nom: str = "module GTM") -> str:
        """contacts : dicts {first_name, last_name, company_name|domain|linkedin_url, enrich_fields, custom}."""
        return self._req("POST", "/contact/enrich/bulk", {"name": nom, "data": contacts})["enrichment_id"]

    def attendre(self, enrichment_id: str, timeout_s: int = 600, intervalle_s: int = 15) -> dict:
        fin = time.time() + timeout_s
        time.sleep(20)
        while time.time() < fin:
            res = self._req("GET", f"/contact/enrich/bulk/{enrichment_id}")
            statut = res.get("status")
            if statut == "FINISHED":
                return res
            if statut in ("CANCELED", "CREDITS_INSUFFICIENT", "RATE_LIMIT", "UNKNOWN"):
                raise RuntimeError(f"FullEnrich : enrichissement {enrichment_id} termine en {statut}")
            time.sleep(intervalle_s)
        raise TimeoutError(f"FullEnrich : {enrichment_id} pas fini apres {timeout_s}s")

    @staticmethod
    def contact_depuis_ligne(ligne: dict, champs: list[str]) -> dict | None:
        """Construit l'entree FullEnrich depuis une ligne normalisee. None si la ligne ne permet
        aucun match (il faut prenom + nom + entreprise ou domaine, ou une URL LinkedIn)."""
        c = {"enrich_fields": champs}
        if ligne.get("prenom"):
            c["first_name"] = ligne["prenom"].strip()
        if ligne.get("nom"):
            c["last_name"] = ligne["nom"].strip()
        if ligne.get("domaine"):
            c["domain"] = domaine(ligne["domaine"])
        if ligne.get("entreprise"):
            c["company_name"] = ligne["entreprise"].strip()
        if ligne.get("linkedin_url"):
            c["linkedin_url"] = norm_linkedin_url(ligne["linkedin_url"]) or ligne["linkedin_url"].strip()
        ok_nom = bool(c.get("first_name") and c.get("last_name") and (c.get("domain") or c.get("company_name")))
        if not ok_nom and not c.get("linkedin_url"):
            return None
        return c

    @staticmethod
    def aplatir(item: dict) -> dict:
        ci = item.get("contact_info") or {}
        we = ci.get("most_probable_work_email") or {}
        ph = ci.get("most_probable_phone") or {}
        prof = item.get("profile") or {}
        emp = (prof.get("employment") or {}).get("current") or {}
        return {
            "email": we.get("email") or "",
            "email_statut": we.get("status") or "",
            "telephone": ph.get("number") or "",
            "titre_fullenrich": emp.get("title") or "",
            "seniorite_fullenrich": emp.get("seniority") or "",
            "custom_id": (item.get("custom") or {}).get("user_id") or "",
        }

    STATUTS_INVALIDES = {"INVALID", "INVALID_DOMAIN", "INVALIDE", "BOUNCE", "BOUNCED", "UNKNOWN_INVALID"}

    @classmethod
    def a_enrichir(cls, ligne: dict, champs: list[str], forcer: bool = False) -> bool:
        """Regle "ne relance que si vide" : email vide ou statut invalide pour les emails,
        telephone vide pour les mobiles. --force ignore la regle."""
        if forcer:
            return True
        besoin = False
        if "contact.emails" in champs:
            besoin |= not (ligne.get("email") or "").strip() or (ligne.get("email_statut") or "").upper() in cls.STATUTS_INVALIDES
        if "contact.phones" in champs:
            besoin |= not (ligne.get("telephone") or "").strip()
        return besoin

    def enrichir_lignes(self, lignes: list[dict], champs: list[str], forcer: bool = False,
                        dry_run: bool = False, nom: str = "module GTM", maximum: int | None = None) -> dict:
        """Enrichit en place les lignes normalisees (lots de 100). Renvoie les compteurs.
        Cout annonce avant tout appel : 1 credit par email pro trouve, 10 par mobile, facture au resultat."""
        candidats = [(i, l) for i, l in enumerate(lignes) if self.a_enrichir(l, champs, forcer)]
        if maximum:
            candidats = candidats[:maximum]
        entrees, sans_cle = [], 0
        for i, l in candidats:
            c = self.contact_depuis_ligne(l, champs)
            if c is None:
                sans_cle += 1
                continue
            c["custom"] = {"user_id": str(i)}
            entrees.append(c)
        credits_max = len(entrees) * ((1 if "contact.emails" in champs else 0) + (10 if "contact.phones" in champs else 0))
        estimation = len(entrees) * ((0.6 if "contact.emails" in champs else 0) + (3 if "contact.phones" in champs else 0))
        stats = {"lignes": len(lignes), "a_traiter": len(entrees), "deja_remplies": len(lignes) - len(candidats),
                 "sans_cle_de_match": sans_cle, "credits_max": credits_max, "credits_estimes": round(estimation),
                 "trouves": 0, "credits_factures": 0}
        if dry_run:
            bandeau_dry_run("FullEnrich contact/enrich/bulk",
                            [f"{len(entrees)} contact(s) a enrichir sur {len(lignes)} ({stats['deja_remplies']} deja remplis, {sans_cle} sans prenom+nom+entreprise ni URL LinkedIn)",
                             f"champs : {', '.join(champs)}",
                             f"cout : au plus {credits_max} credits, environ {round(estimation)} au taux de match habituel (60 % emails, 30 % mobiles)"])
            return stats
        if not entrees:
            afficher("  [fullenrich] rien a enrichir : toutes les lignes sont deja remplies ou sans cle de match")
            return stats
        solde = self.credits()
        afficher(f"  [fullenrich] solde {solde} credits, cout max {credits_max}, estime {round(estimation)}")
        if solde < round(estimation):
            arret(f"FullEnrich : solde {solde} inferieur au cout estime {round(estimation)} credits. Rechargez ou reduisez avec --max.")
        for debut in range(0, len(entrees), 100):
            lot = entrees[debut:debut + 100]
            eid = self.lancer(lot, nom=f"{nom} {debut // 100 + 1}")
            afficher(f"  [fullenrich] lot {debut // 100 + 1} lance ({len(lot)} contacts, id {eid})")
            res = self.attendre(eid)
            stats["credits_factures"] += int(((res.get("cost") or {}).get("credits")) or 0)
            for item in res.get("data", []):
                plat = self.aplatir(item)
                try:
                    idx = int(plat["custom_id"])
                except (TypeError, ValueError):
                    continue
                cible = lignes[idx]
                if "contact.emails" in champs and plat["email"]:
                    cible["email"], cible["email_statut"] = plat["email"], plat["email_statut"]
                    stats["trouves"] += 1
                elif "contact.emails" in champs and not cible.get("email_statut"):
                    cible["email_statut"] = "NOT_FOUND"
                if "contact.phones" in champs and plat["telephone"]:
                    cible["telephone"] = plat["telephone"]
                    stats["trouves"] += 1
                if plat["titre_fullenrich"] and not cible.get("titre"):
                    cible["titre"] = plat["titre_fullenrich"]
            time.sleep(1)
        afficher(f"  [fullenrich] {stats['trouves']} resultat(s) trouve(s), {stats['credits_factures']} credits factures, solde {self.credits()}")
        return stats


# ---------------------------------------------------------------- Crustdata

class Crustdata:
    """Client REST Crustdata. Cle : CRUSTDATA_API_KEY."""
    BASE = "https://api.crustdata.com"

    def __init__(self, exiger_cle: bool = True):
        self.cle = env("CRUSTDATA_API_KEY", obligatoire=exiger_cle)

    def _req(self, methode: str, chemin: str, body=None, params=None):
        if not self.cle:
            env("CRUSTDATA_API_KEY")
        h = {"Authorization": f"Token {self.cle}", "Content-Type": "application/json"}
        st, corps = http(methode, f"{self.BASE}{chemin}", headers=h, json_body=body, params=params)
        if st == 402:
            raise RuntimeError("Crustdata : credits insuffisants (HTTP 402)")
        if st >= 400:
            raise RuntimeError(f"Crustdata {methode} {chemin} -> HTTP {st} : {str(corps)[:300]}")
        return corps

    def credits(self):
        return self._req("GET", "/user/credits").get("credits")

    def entreprises(self, industry=None, employee_range=None, location=None, keywords=None, limit=50) -> list[dict]:
        body = {"limit": limit}
        for k, v in (("industry", industry), ("employee_range", employee_range), ("location", location), ("keywords", keywords)):
            if v:
                body[k] = v
        return self._req("POST", "/v1/companies/search", body).get("results", [])

    def entreprise(self, dom: str) -> dict:
        res = self._req("GET", "/screener/company", params={"company_domain": dom})
        return (res[0] if isinstance(res, list) and res else res) or {}

    def personnes(self, entreprise=None, titres=None, seniorites=None, region=None, domaines=None,
                  limit=100, cursor=None) -> dict:
        conds = []
        if entreprise:
            conds.append({"column": "current_employers.name", "type": "[.]", "value": entreprise})
        if domaines:
            conds.append({"column": "current_employers.company_website_domain", "type": "in", "value": domaines})
        if titres:
            conds.append({"op": "or", "conditions": [{"column": "current_employers.title", "type": "[.]", "value": t} for t in titres]})
        if seniorites:
            conds.append({"column": "current_employers.seniority_level", "type": "in", "value": seniorites})
        if region:
            conds.append({"column": "region", "type": "[.]", "value": region})
        if not conds:
            raise ValueError("Crustdata : au moins un critere (entreprise, titres, seniorites, region, domaines)")
        filtres = conds[0] if len(conds) == 1 else {"op": "and", "conditions": conds}
        body = {"filters": filtres, "limit": min(limit, 1000)}
        if cursor:
            body["cursor"] = cursor
        return self._req("POST", "/screener/persondb/search/", body)


# ---------------------------------------------------------------- HubSpot

class HubSpot:
    """Client REST HubSpot (token Private App). Cle : HUBSPOT_ACCESS_TOKEN."""
    BASE = "https://api.hubapi.com"

    def __init__(self, exiger_cle: bool = True):
        self.token = env("HUBSPOT_ACCESS_TOKEN", obligatoire=exiger_cle)

    def _req(self, methode: str, chemin: str, body=None, params=None):
        if not self.token:
            env("HUBSPOT_ACCESS_TOKEN")
        h = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        st, corps = http(methode, f"{self.BASE}{chemin}", headers=h, json_body=body, params=params)
        if st >= 400:
            raise RuntimeError(f"HubSpot {methode} {chemin} -> HTTP {st} : {str(corps)[:300]}")
        return corps

    def test(self) -> dict:
        return self._req("GET", "/crm/v3/objects/contacts", params={"limit": 1})

    def contacts_par_email(self, emails: list[str], proprietes: list[str] | None = None) -> dict:
        """{email minuscule: {id, props}} pour les emails connus du CRM (lots de 100)."""
        trouves = {}
        emails = sorted({e.lower().strip() for e in emails if e and "@" in e})
        for i in range(0, len(emails), 100):
            lot = emails[i:i + 100]
            res = self._req("POST", "/crm/v3/objects/contacts/batch/read",
                            {"idProperty": "email", "properties": ["email", "lifecyclestage"] + (proprietes or []),
                             "inputs": [{"id": e} for e in lot]})
            for it in res.get("results", []):
                k = (it.get("properties", {}).get("email") or "").lower()
                if k:
                    trouves[k] = {"id": it["id"], "props": it.get("properties", {})}
        return trouves

    def entreprises_par_domaine(self, domaines: list[str]) -> dict:
        """{domaine: id}. `domain` n'est pas une propriete unique : on passe par l'API search."""
        trouves = {}
        domaines = sorted({d.lower().strip() for d in domaines if d})
        for i in range(0, len(domaines), 90):
            lot = domaines[i:i + 90]
            after = None
            while True:
                body = {"filterGroups": [{"filters": [{"propertyName": "domain", "operator": "IN", "values": lot}]}],
                        "properties": ["domain", "name"], "limit": 100}
                if after:
                    body["after"] = after
                res = self._req("POST", "/crm/v3/objects/companies/search", body)
                for it in res.get("results", []):
                    d = (it.get("properties", {}).get("domain") or "").lower()
                    if d and d not in trouves:
                        trouves[d] = it["id"]
                after = ((res.get("paging") or {}).get("next") or {}).get("after")
                if not after:
                    break
        return trouves
