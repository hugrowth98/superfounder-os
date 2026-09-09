#!/usr/bin/env python3
"""Vérifie l'intégrité des skills du dépôt.

- chaque SKILL.md a un frontmatter YAML avec `name` et `description`
- `name` correspond au nom du dossier
- aucun tiret cadratin (U+2014) ni demi-cadratin (U+2013) dans les .md du dépôt
- aucune clé API en clair dans les fichiers versionnés

Usage : python3 scripts/validate_skills.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASHES = ("—", "–")
SECRET_RE = re.compile(r"(?i)(api[_-]?key|token|secret)\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{24,}")
TEXT_SUFFIXES = {".md", ".py", ".json", ".example", ".sh", ".yml", ".yaml"}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    data = {}
    current = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            current = m.group(1)
            data[current] = m.group(2).strip()
        elif current and line.startswith(" "):
            data[current] = (data[current] + " " + line.strip()).strip()
    return data


def iter_files(suffixes):
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path.suffix in suffixes or path.name in {".env.example"}:
            yield path


def main():
    errors = []
    skills = sorted(p for p in ROOT.rglob("SKILL.md") if ".git" not in p.parts)
    for path in skills:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        rel = path.relative_to(ROOT)
        if fm is None:
            errors.append(f"{rel}: frontmatter absent ou mal fermé")
            continue
        name = fm.get("name", "").strip()
        desc = fm.get("description", "").strip().lstrip(">").strip()
        if not name:
            errors.append(f"{rel}: champ `name` manquant")
        elif name != path.parent.name:
            errors.append(f"{rel}: `name` ({name}) ne correspond pas au dossier ({path.parent.name})")
        if not desc:
            errors.append(f"{rel}: champ `description` manquant")

    for path in iter_files({".md"}):
        text = path.read_text(encoding="utf-8")
        for dash in DASHES:
            if dash in text:
                line = next(i for i, l in enumerate(text.splitlines(), 1) if dash in l)
                errors.append(f"{path.relative_to(ROOT)}:{line}: tiret cadratin ou demi-cadratin interdit")
                break

    for path in iter_files(TEXT_SUFFIXES):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if SECRET_RE.search(text):
            errors.append(f"{path.relative_to(ROOT)}: chaîne ressemblant à une clé API")

    print(f"{len(skills)} skills vérifiés")
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("OK : frontmatter valide, aucun tiret cadratin, aucune clé détectée")


if __name__ == "__main__":
    main()
