#!/usr/bin/env python3
"""construire_requete_salesnav : construit une URL de recherche Sales Navigator (personnes ou comptes) a partir
de criteres en texte, ou decode une URL existante en criteres lisibles. Aucun appel payant.

Modes :
  construire (defaut)     les options ci-dessous donnent une URL a coller dans le navigateur, ou a passer a
                          trouver-personnes --source unipile|salesnav --url "..." (ou trouver-entreprises avec --comptes)
  --decoder <url>         lit une URL Sales Navigator copiee depuis le navigateur et affiche ses filtres (type, id, texte)
  --resoudre TYPE:mots    cherche l'id d'une region, d'un secteur, d'une entreprise, d'une liste (Unipile, gratuit)

Exemples :
  python3 construire_requete_salesnav.py --titres "CEO,Fondateur,Directeur General" --region France
  python3 construire_requete_salesnav.py --titres CMO --relation 1
  python3 construire_requete_salesnav.py --titres CMO --vues-profil
  python3 construire_requete_salesnav.py --titres CMO --a-publie
  python3 construire_requete_salesnav.py --titres CMO --suit-entreprise
  python3 construire_requete_salesnav.py --titres CMO --nouveau-poste
  python3 construire_requete_salesnav.py --titres CMO --entreprises "Growth Hiring,Scalezia"
  python3 construire_requete_salesnav.py --persona atl --region France --effectif 11-50,51-200 --nom "ATL PME France" --enregistrer
  python3 construire_requete_salesnav.py --comptes --region France --effectif 11-50 --mots-cles SaaS
  python3 construire_requete_salesnav.py --decoder "https://www.linkedin.com/sales/search/people?query=..."
  python3 construire_requete_salesnav.py --resoudre region:Lyon

Encodage (verifie contre des URL produites par l'interface) : les parentheses de structure restent brutes, ":" et ","
de structure sont encodes une fois, chaque valeur de filtre est encodee deux fois (espace -> %2520, guillemet -> %2522,
parenthese d'un booleen -> %2528). Le script applique cette recette et sait la relire.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/).")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import afficher, arret, aujourd_hui, dossier_gtm, enregistrer_requete, env  # noqa: E402

VERBE = "construire-requete-salesnav"
BASE_PERSONNES = "https://www.linkedin.com/sales/search/people"
BASE_COMPTES = "https://www.linkedin.com/sales/search/company"

# ids verifies dans une URL produite par l'interface Sales Navigator (France : 2026-09-20). Les autres ids se
# trouvent avec --resoudre region:<ville ou pays> (Unipile, gratuit) ou en decodant une URL faite dans l'interface.
REGIONS = {
    "france": ("105015875", "France"),
    "etats-unis": ("103644278", "United States"),
    "united states": ("103644278", "United States"),
}
# ids repris de l'actor Sales Navigator deja utilise (trouver_personnes.py) : a confirmer au premier run
TAILLES = {"self": ("A", "Self-employed"), "1-10": ("B", "1-10"), "11-50": ("C", "11-50"), "51-200": ("D", "51-200"),
           "201-500": ("E", "201-500"), "501-1000": ("F", "501-1,000"), "1001-5000": ("G", "1,001-5,000"),
           "5001-10000": ("H", "5,001-10,000"), "10001+": ("I", "10,001+")}
SENIORITES = {"owner": ("320", "Owner"), "fondateur": ("320", "Owner"), "cxo": ("310", "CXO"), "c_level": ("310", "CXO"),
              "vp": ("300", "VP"), "director": ("220", "Director"), "directeur": ("220", "Director"),
              "manager": ("210", "Manager"), "senior": ("120", "Senior"), "entry": ("110", "Entry")}
RELATIONS = {"1": ("F", "Relations de 1er niveau"), "2": ("S", "Relations de 2e niveau"), "3": ("O", "Relations de 3e niveau et plus")}
# filtres "a cocher" (spotlights) : type, id, texte affiche par l'interface quand elle en met un
SPOTLIGHTS = {
    "vues_profil": ("VIEWED_YOUR_PROFILE", "VYP", "Vues de profil récentes"),
    "a_publie": ("POSTED_ON_LINKEDIN", "RPOL", None),
    "suit_entreprise": ("FOLLOWS_YOUR_COMPANY", "CF", None),
    "nouveau_poste": ("RECENTLY_CHANGED_JOBS", "RPC", None),
}
TYPES_RESOLUTION = {"region": "REGION", "lieu": "LOCATION", "secteur": "SALES_INDUSTRY", "entreprise": "COMPANY",
                    "liste-comptes": "ACCOUNT_LISTS", "liste-leads": "LEAD_LISTS", "ecole": "SCHOOL",
                    "techno": "TECHNOLOGIES", "fonction": "JOB_FUNCTION"}


# ------------------------------------------------------------------ encodage

def q1(s) -> str:
    """Premier passage : la valeur telle qu'elle vit dans le mini-langage de l'URL."""
    return urllib.parse.quote(str(s), safe="")


def _liste(s) -> list[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def booleen(termes: list[str], exclus: list[str] | None = None, parentheses: bool = True) -> str:
    """("CEO" OR "Directeur General") NOT (assistant OR stagiaire). Un seul terme reste nu s'il n'a pas d'espace."""
    def cite(t: str) -> str:
        t = t.strip().strip('"')
        return f'"{t}"' if (" " in t or "-" in t or len(termes) > 1) else t
    inclus = " OR ".join(cite(t) for t in termes)
    if len(termes) > 1 and parentheses:
        inclus = f"({inclus})"
    if exclus:
        inclus += " NOT (" + " OR ".join(cite(t) for t in exclus) + ")"
    return inclus


def valeur(id_=None, texte=None, sel="INCLUDED", icon=None) -> dict:
    v = {"selectionType": sel}
    if id_ is not None and id_ != "":
        v["id"] = str(id_)
    if texte:
        v["text"] = texte
    if icon:
        v["icon"] = icon
    return v


def valeur_dsl(v: dict) -> str:
    parts = []
    if v.get("id") not in (None, ""):
        parts.append(f"id:{q1(v['id'])}")
    if v.get("text"):
        parts.append(f"text:{q1(v['text'])}")
    parts.append(f"selectionType:{v.get('selectionType', 'INCLUDED')}")
    if v.get("icon"):
        parts.append(f"icon:{v['icon']}")
    return "(" + ",".join(parts) + ")"


def filtre_dsl(f: dict) -> str:
    return f"(type:{f['type']},values:List({','.join(valeur_dsl(v) for v in f['values'])}))"


def construire_url(filtres: list[dict], mots_cles: str | None = None, comptes: bool = False,
                   recent_id: str | None = None, session_id: str | None = None) -> str:
    parts = []
    if recent_id:
        parts.append(f"recentSearchParam:(id:{q1(recent_id)},doLogHistory:true)")
    if mots_cles:
        parts.append(f"keywords:{q1(mots_cles)}")
    parts.append("filters:List(" + ",".join(filtre_dsl(f) for f in filtres) + ")")
    dsl = "(" + ",".join(parts) + ")"
    url = (BASE_COMPTES if comptes else BASE_PERSONNES) + "?query=" + urllib.parse.quote(dsl, safe="()")
    if session_id:
        url += "&sessionId=" + q1(session_id)
    return url + "&viewAllFilters=true"


# ------------------------------------------------------------------ decodage

def _parse(s: str, i: int = 0):
    if s.startswith("List(", i):
        i += 5
        items = []
        if i < len(s) and s[i] == ")":
            return items, i + 1
        while True:
            v, i = _parse(s, i)
            items.append(v)
            if i < len(s) and s[i] == ",":
                i += 1
                continue
            if i < len(s) and s[i] == ")":
                return items, i + 1
            raise ValueError(f"liste mal formee vers {i}")
    if i < len(s) and s[i] == "(":
        i += 1
        d = {}
        while True:
            j = s.find(":", i)
            if j < 0:
                raise ValueError(f"cle sans valeur vers {i}")
            cle = s[i:j]
            v, i = _parse(s, j + 1)
            d[cle] = v
            if i < len(s) and s[i] == ",":
                i += 1
                continue
            if i < len(s) and s[i] == ")":
                return d, i + 1
            raise ValueError(f"objet mal forme vers {i}")
    j = i
    while j < len(s) and s[j] not in "(),:":
        j += 1
    return s[i:j], j


def decoder(url: str) -> dict:
    """URL Sales Navigator -> {'comptes': bool, 'mots_cles': str, 'filtres': [{'type', 'values': [{'id','text','selectionType'}]}],
    'recent_id', 'session_id'}. Les textes sont rendus lisibles (decodes une seconde fois)."""
    u = urllib.parse.urlsplit(url.strip())
    qs = urllib.parse.parse_qs(u.query, keep_blank_values=True)
    query = (qs.get("query") or [""])[0]
    if not query:
        arret("URL sans parametre query : collez l'URL complete de la recherche Sales Navigator.")
    obj, _ = _parse(query)
    if not isinstance(obj, dict):
        arret("query illisible : est-ce bien une URL de recherche Sales Navigator ?")
    filtres = []
    for f in obj.get("filters", []) or []:
        vals = []
        for v in f.get("values", []) or []:
            val = {"selectionType": v.get("selectionType", "INCLUDED")}
            if v.get("id"):
                val["id"] = v["id"]
            if v.get("text"):
                val["text"] = urllib.parse.unquote(v["text"])
            if v.get("icon"):
                val["icon"] = v["icon"]
            vals.append(val)
        filtres.append({"type": f.get("type", "?"), "values": vals})
    recent = obj.get("recentSearchParam") or {}
    return {"comptes": "/search/company" in u.path, "mots_cles": urllib.parse.unquote(obj.get("keywords", "") or ""),
            "filtres": filtres, "recent_id": recent.get("id", "") if isinstance(recent, dict) else "",
            "session_id": (qs.get("sessionId") or [""])[0]}


def resume(filtres: list[dict], mots_cles: str = "") -> list[str]:
    lignes = []
    if mots_cles:
        lignes.append(f"mots-cles : {mots_cles}")
    for f in filtres:
        vals = []
        for v in f["values"]:
            libelle = v.get("text") or v.get("id", "")
            if v.get("text") and v.get("id"):
                libelle = f"{v['text']} (id {v['id']})"
            if v.get("selectionType") == "EXCLUDED":
                libelle = "NON " + libelle
            vals.append(libelle)
        lignes.append(f"{f['type']} : {' | '.join(vals)}")
    return lignes


# ------------------------------------------------------------------ resolution des ids (Unipile, gratuit)

def unipile_disponible() -> bool:
    return bool(env("UNIPILE_API_KEY", obligatoire=False) and env("UNIPILE_DSN", obligatoire=False)
                and env("UNIPILE_ACCOUNT_ID", obligatoire=False))


def resoudre(type_court: str, mots: str, limite: int = 10) -> list[dict]:
    t = TYPES_RESOLUTION.get(type_court.lower())
    if not t:
        arret(f"type inconnu '{type_court}' : choisissez parmi {', '.join(TYPES_RESOLUTION)}")
    if not unipile_disponible():
        arret("Unipile n'est pas branche (UNIPILE_API_KEY, UNIPILE_DSN, UNIPILE_ACCOUNT_ID) : faites la recherche une fois "
              "dans l'interface Sales Navigator, copiez l'URL, et lisez l'id avec --decoder. Ou branchez Unipile (connecter-outils).")
    from gtm_common import Unipile  # noqa: E402
    service = "CLASSIC" if t in ("LOCATION", "COMPANY", "SCHOOL", "INDUSTRY", "JOB_FUNCTION", "JOB_TITLE", "SKILL") else "SALES_NAVIGATOR"
    items = Unipile().parametres(t, mots, service=service, limite=limite)
    return [{"id": str(it.get("id", "")), "title": it.get("title", "")} for it in items]


def id_ou_resolu(val: str, table: dict, type_court: str, sans_resolution: bool) -> tuple[str, str]:
    """Rend (id, texte) pour une valeur : id numerique tel quel, libelle connu dans la table, sinon Unipile."""
    v = val.strip()
    if re.fullmatch(r"\d+", v):
        return v, ""
    if v.lower() in table:
        return table[v.lower()]
    if sans_resolution:
        arret(f"'{v}' n'est pas dans la table des ids connus et --sans-resolution est actif : donnez l'id numerique.")
    trouves = resoudre(type_court, v, limite=5)
    if not trouves:
        arret(f"aucun id trouve pour '{v}' ({type_court}). Essayez --resoudre {type_court}:<autre orthographe>.")
    choix = trouves[0]
    autres = ", ".join(f"{x['title']} ({x['id']})" for x in trouves[1:4])
    afficher(f"  [resolution] {type_court} '{v}' -> {choix['title']} (id {choix['id']})" + (f" ; autres : {autres}" if autres else ""))
    return choix["id"], choix["title"]


# ------------------------------------------------------------------ contexte.md (personas)

def titres_du_persona(persona: str) -> list[str]:
    chemin = dossier_gtm() / "contexte.md"
    if not chemin.exists():
        arret(f"{chemin} introuvable : lancez installer-gtm.")
    texte = chemin.read_text(encoding="utf-8")
    bloc = re.search(rf"###\s*{persona.upper()}\b.*?(?=\n###|\n## |\Z)", texte, re.S)
    if not bloc:
        arret(f"section 3 de contexte.md : pas de fiche {persona.upper()}.")
    m = re.search(r"Titres à chercher\s*:\s*(.*)", bloc.group(0))
    if not m:
        arret(f"fiche {persona.upper()} : ligne 'Titres à chercher' absente.")
    val = re.sub(r"<!--.*?-->", "", m.group(1)).strip()
    if not val or val.startswith("["):
        arret(f"fiche {persona.upper()} : les titres ne sont pas remplis dans contexte.md (installer-gtm, phase 3).")
    return _liste(val)


# ------------------------------------------------------------------ enregistrement

def enregistrer(nom: str, persona: str, lignes_resume: list[str], url: str) -> Path:
    return enregistrer_requete(nom, persona, " ; ".join(lignes_resume), url)


# ------------------------------------------------------------------ main

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--titres", help="titres du poste actuel, separes par des virgules (booleen OR, guillemets ajoutes)")
    ap.add_argument("--titres-exclus", help="titres a exclure (NOT), ex : assistant,stagiaire,alternant")
    ap.add_argument("--booleen-titre", help="booleen complet pour le titre, tel quel (prime sur --titres)")
    ap.add_argument("--persona", choices=["atl", "btl"], help="prend les titres de la fiche ATL ou BTL de contexte.md")
    ap.add_argument("--mots-cles", help="mots-cles libres (champ keywords)")
    ap.add_argument("--entreprises", help="entreprises actuelles, noms separes par des virgules (booleen OR)")
    ap.add_argument("--entreprises-exclues", help="entreprises actuelles a exclure")
    ap.add_argument("--anciennes-entreprises", help="entreprises passees (PAST_COMPANY)")
    ap.add_argument("--region", help="regions ou pays : libelle connu (France), id numerique, ou libelle a resoudre par Unipile")
    ap.add_argument("--regions-exclues")
    ap.add_argument("--effectif", help="tranches : self,1-10,11-50,51-200,201-500,501-1000,1001-5000,5001-10000,10001+")
    ap.add_argument("--seniorites", help="owner,cxo,vp,director,manager,senior,entry")
    ap.add_argument("--relation", help="1, 2 ou 3 (niveau de relation), separes par des virgules")
    ap.add_argument("--vues-profil", action="store_true", help="a consulte votre profil recemment")
    ap.add_argument("--a-publie", action="store_true", help="a publie sur LinkedIn dans les 30 derniers jours")
    ap.add_argument("--suit-entreprise", action="store_true", help="suit votre page entreprise")
    ap.add_argument("--nouveau-poste", action="store_true", help="a change de poste dans les 90 derniers jours")
    ap.add_argument("--secteur", help="secteurs Sales Navigator : id ou libelle a resoudre")
    ap.add_argument("--liste-comptes", help="liste de comptes Sales Navigator : id[:nom]")
    ap.add_argument("--liste-leads", help="liste de leads Sales Navigator : id[:nom]")
    ap.add_argument("--filtre", action="append", default=[], help="filtre libre TYPE:id[:texte[:INCLUDED|EXCLUDED]], repetable")
    ap.add_argument("--comptes", action="store_true", help="recherche de comptes (entreprises) au lieu de personnes")
    ap.add_argument("--recent-id", help="recentSearchParam.id d'une URL fraiche (facultatif)")
    ap.add_argument("--session-id", help="sessionId d'une URL fraiche (facultatif, expire)")
    ap.add_argument("--nom", help="nom de la requete (pour --enregistrer et le resume)")
    ap.add_argument("--enregistrer", action="store_true", help="ajoute la requete a Ciblage/requetes-booleennes.md")
    ap.add_argument("--sans-resolution", action="store_true", help="n'appelle jamais Unipile pour trouver un id")
    ap.add_argument("--json", action="store_true", help="sortie JSON (url, filtres, resume)")
    ap.add_argument("--decoder", metavar="URL", help="decode une URL Sales Navigator existante")
    ap.add_argument("--resoudre", metavar="TYPE:mots", help="cherche des ids : region:Lyon, secteur:logiciels, entreprise:Scalezia, liste-comptes:Clients")
    a = ap.parse_args()

    if a.resoudre:
        if ":" not in a.resoudre:
            arret("format attendu : --resoudre region:Lyon")
        t, mots = a.resoudre.split(":", 1)
        trouves = resoudre(t, mots)
        if a.json:
            print(json.dumps(trouves, ensure_ascii=False, indent=2))
        else:
            for x in trouves:
                print(f"{x['id']}\t{x['title']}")
            if not trouves:
                afficher("aucun resultat")
        return

    if a.decoder:
        d = decoder(a.decoder)
        if a.json:
            print(json.dumps(d, ensure_ascii=False, indent=2))
            return
        afficher(f"recherche de {'comptes' if d['comptes'] else 'personnes'}")
        for l in resume(d["filtres"], d["mots_cles"]):
            afficher("  " + l)
        if d["recent_id"] or d["session_id"]:
            afficher(f"  (session : recent_id={d['recent_id'] or '-'}, sessionId={'present' if d['session_id'] else '-'} ; inutiles pour rejouer la recherche)")
        afficher("URL propre (sans session) :")
        print(construire_url(d["filtres"], d["mots_cles"], comptes=d["comptes"]))
        return

    filtres: list[dict] = []
    persona = a.persona or ""
    titres = _liste(a.titres)
    if a.persona:
        titres = titres_du_persona(a.persona) + titres
    if not a.comptes:
        if a.booleen_titre:
            filtres.append({"type": "CURRENT_TITLE", "values": [valeur(texte=a.booleen_titre.strip())]})
        elif titres:
            filtres.append({"type": "CURRENT_TITLE", "values": [valeur(texte=booleen(titres, _liste(a.titres_exclus)))]})
        if a.relation:
            vals = []
            for r in _liste(a.relation):
                if r not in RELATIONS:
                    arret("--relation attend 1, 2 ou 3")
                vals.append(valeur(*RELATIONS[r]))
            filtres.append({"type": "RELATIONSHIP", "values": vals})
        if a.entreprises or a.entreprises_exclues:
            vals = []
            if a.entreprises:
                vals.append(valeur(texte=booleen(_liste(a.entreprises), parentheses=False)))
            if a.entreprises_exclues:
                vals.append(valeur(texte=booleen(_liste(a.entreprises_exclues), parentheses=False), sel="EXCLUDED"))
            filtres.append({"type": "CURRENT_COMPANY", "values": vals})
        if a.anciennes_entreprises:
            filtres.append({"type": "PAST_COMPANY", "values": [valeur(texte=booleen(_liste(a.anciennes_entreprises), parentheses=False))]})
        if a.seniorites:
            vals = []
            for s in _liste(a.seniorites):
                if s.lower() not in SENIORITES:
                    arret(f"seniorite inconnue '{s}' : {', '.join(SENIORITES)}")
                vals.append(valeur(*SENIORITES[s.lower()]))
            filtres.append({"type": "SENIORITY_LEVEL", "values": vals})
    if a.region or a.regions_exclues:
        vals = [valeur(*id_ou_resolu(r, REGIONS, "region", a.sans_resolution)) for r in _liste(a.region)]
        vals += [valeur(*id_ou_resolu(r, REGIONS, "region", a.sans_resolution), sel="EXCLUDED") for r in _liste(a.regions_exclues)]
        filtres.append({"type": "REGION", "values": vals})
    if a.effectif:
        vals = []
        for t in _liste(a.effectif):
            if t not in TAILLES:
                arret(f"tranche inconnue '{t}' : {', '.join(TAILLES)}")
            vals.append(valeur(*TAILLES[t]))
        filtres.append({"type": "COMPANY_HEADCOUNT", "values": vals})
    if a.secteur:
        vals = [valeur(*id_ou_resolu(s, {}, "secteur", a.sans_resolution)) for s in _liste(a.secteur)]
        filtres.append({"type": "INDUSTRY", "values": vals})
    for opt, cle in (("vues_profil", a.vues_profil), ("a_publie", a.a_publie), ("suit_entreprise", a.suit_entreprise), ("nouveau_poste", a.nouveau_poste)):
        if cle:
            t, id_, texte = SPOTLIGHTS[opt]
            filtres.append({"type": t, "values": [valeur(id_, texte)]})
    for opt, t in ((a.liste_comptes, "ACCOUNT_LIST"), (a.liste_leads, "LEAD_LIST")):
        if opt:
            id_, _, nom = opt.partition(":")
            filtres.append({"type": t, "values": [valeur(id_.strip(), nom.strip() or None, icon="list")]})
    for f in a.filtre:
        parts = f.split(":")
        if len(parts) < 2:
            arret("--filtre attend TYPE:id[:texte[:INCLUDED|EXCLUDED]]")
        t, id_ = parts[0].strip().upper(), parts[1].strip()
        texte = parts[2].strip() if len(parts) > 2 else None
        sel = parts[3].strip().upper() if len(parts) > 3 else "INCLUDED"
        filtres.append({"type": t, "values": [valeur(id_ or None, texte, sel)]})

    if not filtres and not a.mots_cles:
        arret("aucun critere : donnez au moins --titres, --persona, --mots-cles, --region, --effectif ou un filtre a cocher.")

    url = construire_url(filtres, a.mots_cles, comptes=a.comptes, recent_id=a.recent_id, session_id=a.session_id)
    lignes = resume(filtres, a.mots_cles or "")
    nom = a.nom or (titres[0] if titres else (a.mots_cles or "requete"))
    if a.json:
        print(json.dumps({"nom": nom, "comptes": a.comptes, "filtres": filtres, "mots_cles": a.mots_cles or "", "resume": lignes, "url": url},
                         ensure_ascii=False, indent=2))
    else:
        afficher(f"requete de {'comptes' if a.comptes else 'personnes'} : {nom}")
        for l in lignes:
            afficher("  " + l)
        print(url)
        if a.comptes:
            afficher('next step : trouver-entreprises --source unipile --url "<url>" (ou --source salesnav avec vos cookies), --dry-run d\'abord')
        else:
            afficher('next step : trouver-personnes --source unipile --url "<url>" --max 100 (ou --source salesnav avec vos cookies), --dry-run d\'abord')
        if any(f["type"] in ("VIEWED_YOUR_PROFILE", "FOLLOWS_YOUR_COMPANY") for f in filtres):
            afficher("note : ces filtres ne marchent qu'avec le compte dont c'est le profil ou la page (Unipile ou vos cookies).")
    if a.enregistrer:
        chemin = enregistrer(nom, persona, lignes, url)
        afficher(f"requete ajoutee a {chemin}")


if __name__ == "__main__":
    main()
