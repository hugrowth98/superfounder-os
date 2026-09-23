#!/usr/bin/env python3
"""rendre_infographie.py : rend un data.json en HTML puis en PNG 1080x1350 (echelle 2), dans un ou plusieurs
gabarits, aux couleurs et polices de 03_Branding/charte-visuelle.md. Sans charte remplie : le style editorial
neutre du master (fond creme, cartes, un accent chaud, Poppins et Lora).

Usage :
  python3 rendre_infographie.py <dossier>/data.json --gabarits grille glossaire systeme
  python3 rendre_infographie.py <dossier>/data.json --gabarits all        (les huit, pour tester)
  python3 rendre_infographie.py --charte                                    (affiche les jetons lus, ne rend rien)

Sorties a cote de data.json : <slug>_<lettre>-<gabarit>_<date>.html et .png. Le PNG demande Chrome ou
Chromium ; sans navigateur, seul le HTML est ecrit et le script le dit (ouvrir le HTML et faire une capture).
Aucun appel reseau : les polices Google Fonts se chargent au rendu si le nom est connu, sinon la police
systeme la plus proche.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gabarits_html import GABARITS  # noqa: E402

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
CHARTE = _racine / "03_Branding" / "charte-visuelle.md"

# Style editorial neutre du master (lecture-charte.md), quand la charte est vide.
NEUTRE = {"fond": "#FAF9F5", "carte": "#F0ECE0", "bloc": "#141413", "texte": "#141413", "gris": "#6B6963",
          "accent": "#D97757", "cta": "#D97757", "titres": "Poppins", "corps": "Lora", "mono": "IBM Plex Mono", "logo": ""}
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")


def _cellules(ligne: str) -> list[str]:
    return [c.strip() for c in ligne.strip().strip("|").split("|")]


def lire_charte(chemin: Path = CHARTE) -> dict:
    """Lit les tableaux 'Palette, par role' et 'Typographies' et la ligne Logo. Un champ '[a remplir]' garde
    la valeur neutre. Renvoie un dict brut : fond, carte, bloc, texte, gris, accent, cta, titres, corps, mono, logo, source."""
    v = dict(NEUTRE)
    v["source"] = "neutre"
    if not chemin.exists():
        return v
    txt = chemin.read_text(encoding="utf-8")
    roles = {"fond principal": "fond", "fond des cartes": "carte", "fond des blocs": "bloc", "texte principal": "texte",
             "texte secondaire": "gris", "accent principal": "accent", "accent secondaire": "cta"}
    typos = {"titres": "titres", "corps": "corps", "monospace": "mono"}
    trouve = 0
    for ligne in txt.splitlines():
        if not ligne.strip().startswith("|"):
            if ligne.lower().lstrip("- ").startswith("fichier :") and "remplir" not in ligne.lower():
                m = re.search(r"`?([^`\s]+\.(png|svg|jpg|jpeg))`?", ligne, re.I)
                if m:
                    v["logo"] = m.group(1)
            continue
        c = _cellules(ligne)
        if len(c) < 2:
            continue
        cle = c[0].lower()
        for role, k in roles.items():
            if cle.startswith(role):
                m = HEX.search(c[1])
                if m:
                    v[k] = m.group(0).upper()
                    trouve += 1
        for niveau, k in typos.items():
            if cle == niveau and "remplir" not in c[1].lower() and c[1]:
                v[k] = c[1].split(",")[0].split("(")[0].strip()
                trouve += 1
    if trouve:
        v["source"] = str(chemin.relative_to(_racine))
    return v


def _lum(hexa: str) -> float:
    h = hexa.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _mix(a: str, b: str, p: float) -> str:
    ha, hb = a.lstrip("#"), b.lstrip("#")
    out = "".join(f"{round(int(ha[i:i+2], 16) * (1 - p) + int(hb[i:i+2], 16) * p):02X}" for i in (0, 2, 4))
    return "#" + out


def jetons(charte: dict, dossier_sortie: Path) -> dict:
    """Transforme la charte brute en jetons pour les gabarits."""
    fond, carte, bloc, texte, gris = charte["fond"], charte["carte"], charte["bloc"], charte["texte"], charte["gris"]
    accent, cta = charte["accent"], charte["cta"]
    bloc_sombre = _lum(bloc) < 0.45
    t = {
        "fond": fond, "carte": carte, "bloc": bloc, "texte": texte, "gris": gris, "accent": accent, "cta": cta,
        "cta_texte": "#FFFFFF" if _lum(cta) < 0.45 else texte,
        "bloc_texte": "#FFFFFF" if bloc_sombre else texte,
        "bloc_legende": _mix(bloc, "#FFFFFF", 0.7) if bloc_sombre else gris,
        "ligne": _mix(fond, texte, 0.12), "ligne_carte": _mix(carte, texte, 0.12),
        "font_titres": f"'{charte['titres']}',sans-serif", "font_corps": f"'{charte['corps']}',sans-serif",
        "font_mono": f"'{charte['mono']}',Menlo,monospace",
    }
    familles = [f"family={f.replace(' ', '+')}:wght@400;500;600;700" for f in {charte["titres"], charte["corps"], charte["mono"]}]
    t["fonts_css"] = f"@import url('https://fonts.googleapis.com/css2?{'&'.join(familles)}&display=swap');"
    logo = ""
    if charte.get("logo"):
        p = (_racine / charte["logo"]) if not charte["logo"].startswith("/") else Path(charte["logo"])
        if p.exists():
            logo = str(p.resolve())
    t["logo"] = logo
    return t


def chrome() -> str | None:
    candidats = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium",
                 "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"]
    for c in candidats:
        if c.startswith("/") and Path(c).exists():
            return c
        if not c.startswith("/") and shutil.which(c):
            return shutil.which(c)
    return None


def rendre(d: dict, gab: str, t: dict, out_dir: Path, lettre: str, navigateur: str | None) -> Path:
    html = GABARITS[gab](d, t)
    nom = f"{d['slug']}_{lettre}-{gab}_{d['date']}"
    p_html, p_png = out_dir / f"{nom}.html", out_dir / f"{nom}.png"
    p_html.write_text(html, encoding="utf-8")
    if not navigateur:
        print(f"html : {p_html} (pas de Chrome trouve : ouvrez-le et faites une capture 1080x1350)")
        return p_html
    r = subprocess.run([navigateur, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--window-size=1080,1350", f"--screenshot={p_png}", f"file://{p_html}"], capture_output=True)
    if r.returncode != 0 or not p_png.exists():
        print(f"echec du rendu PNG pour {nom} : {r.stderr.decode()[-300:]}")
        return p_html
    print(f"png : {p_png}")
    return p_png


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", nargs="?")
    ap.add_argument("--gabarits", nargs="+")
    ap.add_argument("--charte", action="store_true", help="afficher les jetons lus dans la charte")
    a = ap.parse_args()
    ch = lire_charte()
    if a.charte or not a.data:
        print(json.dumps(ch, ensure_ascii=False, indent=1))
        if not a.data:
            return
    if not a.gabarits:
        sys.exit("--gabarits obligatoire : " + ", ".join(GABARITS) + " ou all")
    d = json.loads(Path(a.data).read_text(encoding="utf-8"))
    out_dir = Path(a.data).resolve().parent
    gabs = list(GABARITS) if a.gabarits == ["all"] else a.gabarits
    inconnus = [g for g in gabs if g not in GABARITS]
    if inconnus:
        sys.exit(f"gabarit inconnu : {inconnus}. Disponibles : {', '.join(GABARITS)}")
    t = jetons(ch, out_dir)
    print(f"charte : {ch['source']} | fond {t['fond']} carte {t['carte']} bloc {t['bloc']} accent {t['accent']} cta {t['cta']} | {ch['titres']} / {ch['corps']} / {ch['mono']}")
    nav = chrome()
    for i, g in enumerate(gabs):
        rendre(d, g, t, out_dir, chr(65 + i), nav)


if __name__ == "__main__":
    main()
