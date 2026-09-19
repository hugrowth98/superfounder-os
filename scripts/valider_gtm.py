#!/usr/bin/env python3
"""Valide la coherence du GTM-OS : frontmatter, tirets interdits, mots interdits,
references croisees (sous-skills, ressources, skills d'execution, actors), colonnes CSV.
Usage : python3 scripts/valider.py [--racine <dossier>]
"""
import os, re, sys, argparse

VERBES = ["trouver-entreprises","trouver-lookalikes","trouver-personnes","enrichir-personne",
          "enrichir-entreprise","trouver-email","trouver-telephone",
          "scraper-offres-emploi","scraper-engagement",
          "qualifier-liste","dedoublonner","crm","envoyer-sequence","verifier-reponses"]
MASTERS = ["construire-liste","detecter-signaux","cold-email","cold-call"]
INSTALL = ["installer-gtm","connecter-outils"]
INTERDITS = ["ColdIQ","coldiq","Clay ","Clay.","Claygent","Trigify","RB2B","Bombora","Crunchbase",
             "PredictLeads","TheirStack","6sense","Common Room","Koala","Serper","BuiltWith",
             "YALC","data workspace","Evaboot","PhantomBuster","ZoomInfo","Clearbit","NeverBounce",
             "ZeroBounce","MillionVerifier","Findymail","Prospeo","LeadMagic","Instantly","Smartlead",
             "Crawford","Braun","Hey ","J'espère que vous allez bien","Je me permets"]
TOLERES = {"signalbase/signalbase-api": "Signalbase"}  # nom d'actor autorise

GTM_DIRS = tuple("10_Skills/" + d for d in MASTERS + INSTALL + VERBES + ["_commun"])


def MODULE_GTM(rel):
    return rel.startswith(GTM_DIRS)


def lire(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    R = a.racine
    S = os.path.join(R, "10_Skills")
    erreurs, avert = [], []

    # 1. presence des dossiers attendus
    for d in MASTERS + INSTALL + VERBES:
        p = os.path.join(S, d, "SKILL.md")
        if not os.path.exists(p):
            erreurs.append(f"[manquant] 10_Skills/{d}/SKILL.md")

    for p in ["10_Skills/detecter-signaux/scripts/detecter_signal.py", "10_Skills/enrichir-entreprise/scripts/detecter_techno.py",
              "10_Skills/enrichir-entreprise/scripts/scraper_pubs.py", "10_Skills/_commun/gtm_common.py"]:
        if not os.path.exists(os.path.join(R, p)):
            erreurs.append(f"[manquant] {p}")
    # 2. parcours de tous les .md et .py
    fichiers = []
    for dp, dn, fn in os.walk(R):
        if "/.git" in dp or "11_Archives" in dp or "/.agents" in dp or "/.claude" in dp: continue
        for f in fn:
            if f.endswith((".md", ".py")):
                fichiers.append(os.path.join(dp, f))
    for p in fichiers:
        t = lire(p); rel = os.path.relpath(p, R)
        exempt = rel in ("docs/conventions-gtm.md", "scripts/valider_gtm.py", "scripts/validate_skills.py", "CHANGELOG.md", "01_About-Me/anti-ai-voice.md") or rel.startswith("11_Archives/")
        for i, l in enumerate(t.splitlines(), 1):
            if (chr(0x2014) in l or chr(0x2013) in l) and not exempt:
                erreurs.append(f"[tiret] {rel}:{i}")
            for m in ([] if exempt else INTERDITS):
                if m in l:
                    ll = l
                    for act in TOLERES: ll = ll.replace(act, "")
                    if m in ll and not ("signalbase" in m.lower()):
                        erreurs.append(f"[interdit:{m.strip()}] {rel}:{i}")
        if p.endswith("SKILL.md"):
            if not t.startswith("---"):
                erreurs.append(f"[frontmatter] {rel} ne commence pas par ---")
            else:
                fm = t.split("---")[1]
                nom = re.search(r"^name:\s*(\S+)", fm, re.M)
                dossier = os.path.basename(os.path.dirname(p))
                if not nom: erreurs.append(f"[frontmatter] {rel} sans name")
                elif nom.group(1) != dossier: erreurs.append(f"[name] {rel} name={nom.group(1)} dossier={dossier}")
                if "description:" not in fm: erreurs.append(f"[frontmatter] {rel} sans description")
            # references vers sous-skills et ressources
            base = os.path.dirname(p)
            for m in re.finditer(r"\{SKILL_BASE\}/(sous-skills|ressources)/([A-Za-z0-9_./-]+)", t):
                cible = os.path.join(base, m.group(1), m.group(2))
                if not os.path.exists(cible) and not os.path.exists(os.path.join(os.path.dirname(base), m.group(1), m.group(2))):
                    # sous-skill referencant une ressource du master parent
                    parent = os.path.dirname(os.path.dirname(base))
                    if not os.path.exists(os.path.join(parent, m.group(1), m.group(2))):
                        erreurs.append(f"[ref] {rel} -> {m.group(1)}/{m.group(2)} introuvable")
            # references vers skills d'execution
            for v in re.findall(r"`([a-z-]+)`", t):
                if v in VERBES or v in MASTERS or v in INSTALL:
                    if not os.path.exists(os.path.join(S, v, "SKILL.md")):
                        erreurs.append(f"[ref-skill] {rel} -> {v} introuvable")
            # tutoiement suspect dans un skill
            if MODULE_GTM(rel) and re.search(r"\b(tu peux|tu dois|tes prospects|ton ICP|ta liste)\b", t):
                avert.append(f"[tutoiement] {rel}")
    # 3. scripts compilent
    import py_compile
    for p in fichiers:
        if p.endswith(".py") and "/scripts/valider.py" not in p:
            try: py_compile.compile(p, doraise=True)
            except Exception as e: erreurs.append(f"[py] {os.path.relpath(p,R)} : {e}")
    # 4. OUTILS.md actors vs skills
    chemin_outils = os.path.join(R, "05_Departements", "Go-to-Market", "OUTILS.md")
    outils = lire(chemin_outils) if os.path.exists(chemin_outils) else ""
    actors_outils = set(re.findall(r"`([a-z0-9_-]+/[a-z0-9_-]+)`", outils))
    actors_skills = set()
    for p in fichiers:
        if "/10_Skills/" in p and MODULE_GTM(os.path.relpath(p, R)):
            actors_skills |= set(re.findall(r"\b([a-z0-9_-]+/[a-z0-9_-]+(?:-scraper|-search|-employees|-api|-detector|-library|-places|-posts|-comments|-jobs-scraper))\b", lire(p)))
    for act in sorted(actors_skills - actors_outils):
        avert.append(f"[actor] utilise dans un skill mais absent de OUTILS.md : {act}")

    print(f"{len(fichiers)} fichiers verifies, {len(erreurs)} erreurs, {len(avert)} avertissements")
    for e in erreurs: print("ERREUR", e)
    for w in avert: print("AVERT ", w)
    sys.exit(1 if erreurs else 0)

if __name__ == "__main__":
    main()
