#!/usr/bin/env python3
"""
Lead Qualifier — Classification automatique de prospects LinkedIn
Usage:
    python3 classify_leads.py --files file1.csv file2.csv --output leads_qualifies.xlsx
"""

import argparse
import re
import sys

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ─── CLI ──────────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Qualifier des leads LinkedIn depuis des CSV")
parser.add_argument('--files', nargs='+', required=True, help='Chemins vers les fichiers CSV')
parser.add_argument('--output', default='leads_qualifies.xlsx', help='Chemin du fichier Excel de sortie')
args = parser.parse_args()

# ─── FREELANCE EXPLICIT ────────────────────────────────────────────────────────
FREELANCE_EXPLICIT_KW = [
    r'\bfreelance\b', r'\bindépendant[e]?\b', r'\bindependant[e]?\b',
    r'\bauto[-\s]?entrepreneur[e]?\b', r'\bmicro[-\s]?entrepreneur[e]?\b',
    r'\bsolopreneur\b', r'\bself[-\s]?employed\b', r'\bportage\s+salarial\b',
    r'\bà\s+mon\s+compte\b', r'\bfractionnel[le]?\b', r'\bfractional\b', r'\bportage\b',
    r'\btravailleur[se]?\s+indépendant[e]?\b',
    r'\bà\s+temps\s+partiel\b', r'\btemps\s+partiel\b',
    r'\bmanager\s+de\s+transition\b', r'\bcoach\s+de\s+transition\b',
    r'\ben\s+transition\s+professionnelle\b',
    r'\bpart[-\s]?time\s+\w+\b',   # part-time SUIVI d'un titre
]

# ─── FREELANCE FUNCTIONAL ──────────────────────────────────────────────────────
FREELANCE_FUNCTIONAL_KW = [
    r'\bconsultant[e]?\b', r'\bcoach\b', r'\bcoaching\b',
    r'\bformateur[rice]?\b', r'\bformatrice\b',
    r'\bconférencier[e]?\b', r'\bconferencier[e]?\b',
    r'\benseignant[e]?\b', r'\bprofesseur[e]?\b',
    r'\bexpert[e]?\b', r'\bspécialiste\b', r'\bspecialiste\b',
    r'\bcertifié[e]?\b', r'\bcertifie[e]?\b',
    r'\bghost\s*writer\b', r'\bghostwriter\b',
    r'\bspeaker\b', r'\bconférencière\b',
    r'\bauteur[e]?\b', r'\bauteure\b', r'\bauthor\b',
    r'\bcréateur[rice]?\b', r'\bcréatrice\b', r'\bcontent\s+creator\b',
    r'\bpersonal\s+branding\b',
    r'\bingénieur\s+(?:d.{0,3}|des\s+)affaires\b',
    r'\bbusiness\s+developer\b',
    r'\bsme\b',
    r'\bmentor\b', r'\bthérapeute\b', r'\bpsychologue\b',
    r'\bnutritionniste\b', r'\bkinésiologue\b',
    r'\bstratège\b', r'\bstrateg(?:ist|iste)\b',
    r'\bcommunity\s+manager\b',
    r'\barchitecte\b',
    r'\bcopywriter\b', r'\bcopywriting\b',
    r'\badvisor\b', r'\badviseur[e]?\b', r'\badvisory\b',
    r'\bavocat[e]?\b', r'\bjuriste\b', r'\bnotaire\b',
    r'\bcomptable\b', r'\bexpert[-\s]?comptable\b',
    r'\bpsychothérapeute\b', r'\bostéopathe\b', r'\bkinésithérapeute\b',
    r'\bpodcast(?:eur|euse|er)?\b',
    r'\bentrepreneur[e]?\b',
    r'\bconseiller[e]?\b', r'\baccompagnat(?:eur|rice)\b',
]

# ─── CEO STRICT ────────────────────────────────────────────────────────────────
CEO_STRICT_KW = [
    r'\bceo\b', r'\bpdg\b', r'\bdg\b',
    r'\b(directeur|directrice)\s+général[e]?\b',
    r'\bpresident[e]?\b', r'\bprésident[e]?\b', r'\bpresidente\b',
    r'\bprésident[e]?[-\s]directeur\b',
    r'\bfondateur[rice]?\b', r'\bfondatrice\b',
    r'\bfounder\b', r'\bco[-\s]?founder[s]?\b', r'\bcofounder[s]?\b',
    r'\bco[-\s]?fondateur[rice]?\b', r'\bcofondateur[rice]?\b',
    r'\bchief\s+executive(?:\s+officer)?\b',
    r'\bdirigean[t]e?\b',
    r'\bgérant[e]?\b', r'\bgerant[e]?\b',
    r'\bowner\b', r'\bpropriétaire\b', r'\bproprietaire\b',
    r'\bmanaging\s+director\b', r'\bmanaging\s+partner\b',
    r'\bexecutive\s+director\b', r'\bchairman\b', r'\bchairwoman\b',
    r'\bchairperson\b', r'\bco[-\s]?ceo\b', r'\bchief\s+exec\b',
    r'\bassocié[e]?\s+(gérant|dirigeant)\b',
]

CEO_NEGATIVE_KW = [
    r'\bfutur\s+entrepreneur\b', r'\ben\s+devenir\b',
    r'\bfutur[e]?\s+fondateur\b',
    r'\bleadership\s+diversit[eé]\b', r'\bdiversit[eé]\b',
    r'\bchef\s+de\s+groupe\b', r'\bchef\s+de\s+secteur\b',
    r'\bchef\s+de\s+rayon\b', r'\bchef\s+de\s+produit\b',
    r'\bchef\s+de\s+service\b', r'\bchef\s+de\s+zone\b',
    r'\bchef\s+de\s+r[eé]gion\b',
]

# ─── CMO / SALES ────────────────────────────────────────────────────────────────
CMO_STRICT_KW = [
    r'\bcmo\b', r'\bchief\s+marketing\s+officer\b',
    r'\bvp\s+(of\s+)?marketing\b', r'\bvice[-\s]?president\s+marketing\b',
    r'\bhead\s+of\s+marketing\b',
    r'\b(directeur|directrice)\s+(du\s+)?marketing\b',
    r'\bmarketing\s+director\b', r'\bdirector\s+of\s+marketing\b',
    r'\bdirectrice\s+marketing\b',
    r'\bvice[-\s]?président[e]?\s+marketing\b',
    r'\bvice[-\s]?president\s+marketing\b',
]

SALES_STRICT_KW = [
    r'\bcro\b', r'\bcco\b',
    r'\bchief\s+revenue\s+officer\b', r'\bchief\s+commercial\s+officer\b',
    r'\bchief\s+sales\s+officer\b',
    r'\bvp\s+(of\s+)?sales\b', r'\bvp\s+(du\s+)?commercial\b',
    r'\bvice[-\s]?president\s+(sales|commercial)\b',
    r'\bhead\s+of\s+sales\b', r'\bhead\s+of\s+revenue\b',
    r'\b(directeur|directrice)\s+(du\s+|des\s+)?commercial[e]?\b',
    r'\b(directeur|directrice)\s+(des\s+)?ventes\b',
    r'\bsales\s+director\b', r'\bdirector\s+of\s+sales\b',
    r'\bdirector\s+of\s+business\s+development\b',
]

CSUITE_KW = [
    r'\bcoo\b', r'\bcfo\b', r'\bcto\b', r'\bcpo\b', r'\bchro\b', r'\bcio\b',
    r'\bchief\s+\w+\s+officer\b',
    r'\bvice[-\s]?président[e]?\b', r'\bvice\s+president\b',
    r'\bvp\b',
    r'\bhead\s+of\b',
    r'\b(directeur|directrice)\b',
    r'\bdirector\b',
    r'\bassocié[e]?\b',
    r'\bcountry\s+manager\b', r'\bgeneral\s+manager\b',
    r'\bmanaging\s+partner\b', r'\bsenior\s+vice\s+president\b',
    r'\bsvp\b', r'\bevp\b', r'\bchief\s+of\s+staff\b',
]

MANAGER_KW = [
    r'\bmanager\b', r'\bresponsable\b',
    r'\bchef\s+de\s+(projet|produit|service)\b',
    r'\bteam\s+lead(?:er)?\b', r'\bsuperviseur\b', r'\bsupervisor\b',
    r'\bproject\s+manager\b', r'\bproduct\s+manager\b',
    r'\bchargé[e]?\s+de\b',
]

EXECUTANT_KW = [
    r'\bproduct\s+owner\b', r'\bingénieur\b', r'\bengineer\b',
    r'\bdéveloppeur\b', r'\bdeveloper\b', r'\bdesigner\b',
    r'\banalyst[e]?\b', r'\bstagiaire\b', r'\bintern\b',
    r'\bassistant[e]?\b', r'\bcoordinateur\b', r'\bcoordinator\b',
    r'\bgrowth\s+hacker\b', r'\bgrowth\s+market(?:er|ing)\b',
    r'\bmedia\s+buyer\b', r'\bcreative\s+strategist\b',
]

# ─── HELPERS ───────────────────────────────────────────────────────────────────
ILLEGAL_CHARS_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')

def clean_str(val):
    if pd.isna(val):
        return ''
    return ILLEGAL_CHARS_RE.sub('', str(val))

def normalize(text):
    if pd.isna(text):
        return ""
    return str(text).lower().strip()

def parse_company_size(size_str):
    if pd.isna(size_str) or str(size_str).strip() in ('', 'nan', 'none'):
        return None
    s = str(size_str).lower().replace(',', '').replace(' ', '')
    if any(x in s for x in ('self', 'solopreneur', 'myself')):
        return 1
    m = re.search(r'(\d+)', s)
    return int(m.group(1)) if m else None

def match_any(text, patterns):
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

# ─── SCORING ───────────────────────────────────────────────────────────────────
def score_lead(category, size):
    if category == "CEO":
        if size is not None and size > 10:
            return 10
        return 9

    elif category in ("CMO / Head of Marketing", "Head of Sales"):
        if size is None:    return 6
        if size > 50:       return 8
        if size > 10:       return 7
        return 6

    elif category == "Freelance / Indépendant":
        return 4

    else:  # Directeur/C-suite, Responsable/Manager, Exécutant
        return 1


def get_tier(score):
    if score >= 9:  return "Tier 1"
    if score >= 6:  return "Tier 2"
    if score >= 4:  return "Tier 3"
    return "—"


# ─── COLUMN ALIASES (camelCase + snake_case support) ──────────────────────────
COL_ALIASES = {
    'occupation':   ['occupation', 'Occupation', 'poste'],
    'job_title':    ['jobTitle', 'job_title', 'JobTitle', 'job title', 'title', 'headline'],
    'company_size': ['companySize', 'company_size', 'companyEmployeesOnLinkedin',
                     'company_employees', 'employees', 'taille_entreprise'],
}

# col_map is built after loading CSVs (populated below)
col_map = {}

def get_col_val(row, logical):
    actual = col_map.get(logical)
    if actual and actual in row.index:
        return row[actual]
    return ''

# ─── CLASSIFICATION ────────────────────────────────────────────────────────────
def classify(row):
    """Returns (category, score, tier)."""
    occ = normalize(get_col_val(row, 'occupation'))
    job = normalize(get_col_val(row, 'job_title'))
    combined = occ + " " + job

    size = parse_company_size(get_col_val(row, 'company_size'))
    size_big  = size is not None and size > 10
    size_solo = size is not None and size <= 1

    def result(cat):
        sc = score_lead(cat, size)
        return cat, sc, get_tier(sc)

    # P0 — Intern/stagiaire
    if match_any(combined, [r'\bstagiaire\b', r'\bintern\b', r'\bapprentissage\b', r'\balternan[t]e?\b']):
        return result("Exécutant")

    # P1 — Freelance explicite
    if match_any(combined, FREELANCE_EXPLICIT_KW):
        return result("Freelance / Indépendant")

    # P2 — Fonctionnel dans occupation
    if match_any(occ, FREELANCE_FUNCTIONAL_KW):
        return result("Freelance / Indépendant")

    occ_is_responsable = bool(re.search(r'\bresponsable\b', occ, re.IGNORECASE))
    occ_is_chef_de = (bool(re.search(r'\bchef\s+de\b', occ, re.IGNORECASE)) and
                      not bool(re.search(r'\bchef\s+d.entreprise\b', occ, re.IGNORECASE)))

    # P3 — CMO/Sales dans occupation
    if match_any(occ, CMO_STRICT_KW) and not match_any(combined, FREELANCE_FUNCTIONAL_KW):
        return result("CMO / Head of Marketing")
    if match_any(occ, SALES_STRICT_KW) and not match_any(combined, FREELANCE_FUNCTIONAL_KW):
        return result("Head of Sales")

    # P4 — CEO dans occupation
    if match_any(occ, CEO_STRICT_KW):
        if occ_is_chef_de and not match_any(occ, [r'\bceo\b', r'\bpdg\b', r'\bfondateur\b',
                r'\bfounder\b', r'\bgérant\b', r'\bprésident\b', r'\bpresident\b', r'\bdirigean\b']):
            return result("Responsable / Manager")
        if match_any(occ, CEO_NEGATIVE_KW):
            return result("Responsable / Manager")
        if size_solo:
            return result("Freelance / Indépendant")
        if size_big:
            return result("CEO")
        if match_any(job, FREELANCE_FUNCTIONAL_KW):
            return result("Freelance / Indépendant")
        return result("CEO")

    # P5 — CEO dans job_title seulement
    if match_any(job, CEO_STRICT_KW):
        if match_any(job, CEO_NEGATIVE_KW) or match_any(occ, CEO_NEGATIVE_KW):
            return result("Responsable / Manager")
        if occ_is_responsable or occ_is_chef_de:
            return result("Responsable / Manager")
        if len(occ.strip()) > 3 and not match_any(occ, CEO_STRICT_KW):
            return result("Freelance / Indépendant")
        if match_any(combined, FREELANCE_FUNCTIONAL_KW):
            return result("Freelance / Indépendant")
        return result("CEO")

    # P6 — CMO/Sales depuis job_title
    if match_any(job, CMO_STRICT_KW) and not match_any(combined, FREELANCE_FUNCTIONAL_KW) \
            and not occ_is_responsable and not occ_is_chef_de:
        return result("CMO / Head of Marketing")
    if match_any(job, SALES_STRICT_KW) and not match_any(combined, FREELANCE_FUNCTIONAL_KW) \
            and not occ_is_responsable and not occ_is_chef_de:
        return result("Head of Sales")

    # P7 — Fonctionnel dans job_title
    if match_any(job, FREELANCE_FUNCTIONAL_KW):
        return result("Freelance / Indépendant")

    # P8 — Exécutant explicite
    if match_any(combined, EXECUTANT_KW):
        return result("Exécutant")

    # P9 — C-suite dans occupation
    if match_any(occ, CSUITE_KW):
        return result("Directeur / C-suite")

    # P10 — Manager
    if match_any(combined, MANAGER_KW):
        return result("Responsable / Manager")

    return result("Exécutant")


# ─── LOAD CSVs ────────────────────────────────────────────────────────────────
dfs = []
for path in args.files:
    try:
        df = pd.read_csv(path, dtype=str)
        dfs.append(df)
        print(f"  ✓ {path} — {len(df)} lignes")
    except Exception as e:
        print(f"  ✗ Erreur {path}: {e}", file=sys.stderr)

if not dfs:
    print("Aucun fichier chargé. Vérifiez les chemins.", file=sys.stderr)
    sys.exit(1)

all_df = pd.concat(dfs, ignore_index=True)
print(f"\nTotal : {len(all_df)} leads")

# ─── BUILD COLUMN MAP (resolve camelCase / snake_case aliases) ─────────────────
col_lower_map = {c.lower(): c for c in all_df.columns}
for logical, aliases in COL_ALIASES.items():
    for alias in aliases:
        if alias in all_df.columns:
            col_map[logical] = alias
            break
        if alias.lower() in col_lower_map:
            col_map[logical] = col_lower_map[alias.lower()]
            break

print(f"Colonnes détectées : { {k: v for k, v in col_map.items()} }")

# ─── Supprimer les anciennes colonnes de qualification si elles existent déjà ──
for old_col in ['Catégorie', 'Cat_gorie', 'Score', 'Tier']:
    if old_col in all_df.columns:
        all_df.drop(columns=[old_col], inplace=True)

results = all_df.apply(classify, axis=1)
all_df['Catégorie'] = results.apply(lambda x: x[0])
all_df['Score']     = results.apply(lambda x: x[1])
all_df['Tier']      = results.apply(lambda x: x[2])

print("\nDistribution :")
print(all_df['Catégorie'].value_counts().to_string())

# ─── BUILD EXCEL ──────────────────────────────────────────────────────────────
# Garder TOUTES les colonnes originales — placer Catégorie/Score/Tier en premier
qual_cols = ['Catégorie', 'Score', 'Tier']
other_cols = [c for c in all_df.columns if c not in qual_cols]
cols_present = qual_cols + other_cols
export_df = all_df[cols_present].copy()
export_df = export_df.sort_values(['Score', 'Catégorie'], ascending=[False, True])

wb = Workbook()

CAT_COLORS = {
    "CEO":                    "D4EFDF",
    "Freelance / Indépendant":"D6EAF8",
    "CMO / Head of Marketing":"FEF9E7",
    "Head of Sales":          "FDEBD0",
    "Directeur / C-suite":    "E8DAEF",
    "Responsable / Manager":  "FDFEFE",
    "Exécutant":              "F2F3F4",
}
SCORE_COLORS = {
    10: "1A5C36", 9: "27AE60",
    8: "E67E22",  7: "F39C12", 6: "F0B27A",
    4: "CA6F1E",
    1: "BDC3C7",
}
TIER_COLORS = {
    "Tier 1": "1E8449",
    "Tier 2": "2471A3",
    "Tier 3": "CA6F1E",
    "—":      "95A5A6",
}

header_font  = Font(name='Arial', bold=True, color='FFFFFF', size=10)
header_fill  = PatternFill('solid', start_color='2C3E50')
header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
cell_font    = Font(name='Arial', size=9)
center_align = Alignment(horizontal='center', vertical='center')
left_align   = Alignment(horizontal='left', vertical='center', wrap_text=True)
thin_border  = Border(
    left=Side(style='thin', color='D5D8DC'), right=Side(style='thin', color='D5D8DC'),
    top=Side(style='thin', color='D5D8DC'), bottom=Side(style='thin', color='D5D8DC'),
)

COL_WIDTHS = {
    'Catégorie': 24, 'Score': 7, 'Tier': 9,
    'firstName': 14, 'lastName': 14,
    'occupation': 28, 'job_title': 45,
    'company_name': 22, 'location': 22,
    'linkedinEmail': 28, 'proEmail': 28, 'phoneNumbers': 16,
    'linkedinUrl': 40, 'prospectList': 20,
    'messageSent': 14, 'messageReplied': 14,
    'connectedAt': 14, 'profileStatus': 14,
}

headers = [c.replace('_', ' ').title() for c in cols_present]


def style_header(ws, cols):
    for ci, h in enumerate(cols, 1):
        c = ws.cell(row=1, column=ci, value=h)
        c.font, c.fill, c.alignment, c.border = header_font, header_fill, header_align, thin_border
    ws.row_dimensions[1].height = 30


def write_data_rows(ws, df, cp):
    for ri, (_, row) in enumerate(df.iterrows(), 2):
        cat = row.get('Catégorie', '')
        bg = CAT_COLORS.get(cat, 'FFFFFF')
        for ci, col_name in enumerate(cp, 1):
            val = clean_str(row[col_name])
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.font, cell.border = cell_font, thin_border
            if col_name == 'Catégorie':
                cell.fill = PatternFill('solid', start_color=bg)
                cell.font = Font(name='Arial', size=9, bold=True)
                cell.alignment = center_align
            elif col_name == 'Score':
                sc_val = int(row['Score']) if str(row['Score']).isdigit() else 1
                cell.fill = PatternFill('solid', start_color=SCORE_COLORS.get(sc_val, 'BDC3C7'))
                cell.font = Font(name='Arial', size=9, bold=True, color='FFFFFF')
                cell.alignment = center_align
            elif col_name == 'Tier':
                tier_val = str(row.get('Tier', '—'))
                cell.fill = PatternFill('solid', start_color=TIER_COLORS.get(tier_val, '95A5A6'))
                cell.font = Font(name='Arial', size=9, bold=True, color='FFFFFF')
                cell.alignment = center_align
            else:
                cell.alignment = left_align


def set_col_widths(ws, cp):
    for ci, col_name in enumerate(cp, 1):
        # Essaye le nom exact, puis une version normalisée
        width = COL_WIDTHS.get(col_name)
        if width is None:
            # largeur adaptative selon longueur du nom de colonne
            width = max(12, min(40, len(col_name) + 4))
        ws.column_dimensions[get_column_letter(ci)].width = width


# ── Onglet 1 : Tous les leads ─────────────────────────────────────────────────
ws = wb.active
ws.title = "Tous les leads"
style_header(ws, headers)
ws.freeze_panes = 'C2'
write_data_rows(ws, export_df, cols_present)
set_col_widths(ws, cols_present)
ws.auto_filter.ref = ws.dimensions

# ── Onglet 2 : Résumé ─────────────────────────────────────────────────────────
ws2 = wb.create_sheet("Résumé")
summary_data = export_df.groupby('Catégorie').agg(
    Nombre=('Catégorie', 'count'), Score=('Score', 'first')
).reset_index().sort_values('Score', ascending=False)

ws2['A1'] = 'Résumé de la qualification'
ws2['A1'].font = Font(name='Arial', bold=True, size=14, color='2C3E50')
ws2.merge_cells('A1:D1')
ws2.row_dimensions[1].height = 28

for ci, h in enumerate(['Catégorie', 'Nombre de leads', 'Score max', 'Tier'], 1):
    c = ws2.cell(row=3, column=ci, value=h)
    c.font, c.fill, c.alignment, c.border = header_font, header_fill, header_align, thin_border
ws2.row_dimensions[3].height = 25

for ri, (_, srow) in enumerate(summary_data.iterrows(), 4):
    cat = srow['Catégorie']
    bg = CAT_COLORS.get(cat, 'FFFFFF')
    sv = int(srow['Score'])
    tier = get_tier(sv)

    c1 = ws2.cell(row=ri, column=1, value=cat)
    c1.fill, c1.border = PatternFill('solid', start_color=bg), thin_border
    c1.font = Font(name='Arial', size=10, bold=True)
    c1.alignment = left_align

    c2 = ws2.cell(row=ri, column=2, value=srow['Nombre'])
    c2.font, c2.alignment, c2.border = Font(name='Arial', size=10), center_align, thin_border

    c3 = ws2.cell(row=ri, column=3, value=sv)
    c3.fill = PatternFill('solid', start_color=SCORE_COLORS.get(sv, 'BDC3C7'))
    c3.font = Font(name='Arial', size=10, bold=True, color='FFFFFF')
    c3.alignment, c3.border = center_align, thin_border

    c4 = ws2.cell(row=ri, column=4, value=tier)
    c4.fill = PatternFill('solid', start_color=TIER_COLORS.get(tier, '95A5A6'))
    c4.font = Font(name='Arial', size=10, bold=True, color='FFFFFF')
    c4.alignment, c4.border = center_align, thin_border

    ws2.row_dimensions[ri].height = 22

total_row = 4 + len(summary_data)
ws2.cell(row=total_row, column=1, value='TOTAL').font = Font(name='Arial', bold=True, size=10)
ws2.cell(row=total_row, column=1).border = thin_border
ws2.cell(row=total_row, column=1).alignment = left_align
ct = ws2.cell(row=total_row, column=2, value=f'=SUM(B4:B{total_row-1})')
ct.font, ct.alignment, ct.border = Font(name='Arial', bold=True, size=10), center_align, thin_border
ws2.cell(row=total_row, column=3).border = thin_border
ws2.cell(row=total_row, column=4).border = thin_border
ws2.row_dimensions[total_row].height = 22

ws2.column_dimensions['A'].width = 28
ws2.column_dimensions['B'].width = 18
ws2.column_dimensions['C'].width = 12
ws2.column_dimensions['D'].width = 10

# ── Onglets par catégorie ──────────────────────────────────────────────────────
for cat_name in summary_data['Catégorie'].tolist():
    safe_name = re.sub(r'[/\\?*:\[\]]', '-', cat_name)[:31]
    ws_cat = wb.create_sheet(safe_name)
    style_header(ws_cat, headers)
    ws_cat.freeze_panes = 'C2'
    cat_df = export_df[export_df['Catégorie'] == cat_name]
    write_data_rows(ws_cat, cat_df, cols_present)
    set_col_widths(ws_cat, cols_present)
    ws_cat.auto_filter.ref = ws_cat.dimensions

wb.save(args.output)
print(f"\n✅ Fichier sauvegardé : {args.output}")
