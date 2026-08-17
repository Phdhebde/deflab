#!/usr/bin/env python3
"""Vérifie que chaque module respecte le gabarit imposé.

Le gabarit n'est pas une bonne intention : c'est une contrainte mécanique.
Ce script est exécuté par la CI (`.github/workflows/validate.yml`) et échoue
dès qu'un module s'écarte de la structure.

Usage : python tools/check_structure.py [modules/05-windows-logs ...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = ROOT / "modules"

# Les dix sections du gabarit (shared/template/MODULE.md), dans l'ordre.
REQUIRED_SECTIONS = [
    "Objectif",
    "Prérequis",
    "Architecture",
    "Montage",
    "Scénario d'attaque",
    "Ce que je vois",
    "La détection",
    "Validation",
    "Faux positifs observés",
    "Angles morts",
]

# Interface uniforme : le lecteur apprend les cibles une seule fois.
REQUIRED_MAKE_TARGETS = ["up", "down", "attack", "verify", "clean"]

SECTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)
TARGET_RE = re.compile(r"^([A-Za-z0-9_.-]+)\s*:(?!=)", re.MULTILINE)


def normalize(text: str) -> str:
    """Compare les titres sans se laisser piéger par la casse ou les apostrophes."""
    return text.replace("’", "'").casefold().strip()


def check_sections(readme: Path) -> list[str]:
    found = SECTION_RE.findall(readme.read_text(encoding="utf-8"))
    actual = [(int(num), title) for num, title in found]

    errors = []
    expected = list(enumerate(REQUIRED_SECTIONS, start=1))

    if len(actual) != len(expected):
        errors.append(
            f"{len(actual)} section(s) `## N. ...` trouvée(s), {len(expected)} attendues"
        )

    for (exp_num, exp_title), got in zip(expected, actual + [(None, None)] * len(expected)):
        if got[0] is None:
            errors.append(f"section manquante : `## {exp_num}. {exp_title}`")
        elif got[0] != exp_num or normalize(got[1]) != normalize(exp_title):
            errors.append(
                f"attendu `## {exp_num}. {exp_title}`, trouvé `## {got[0]}. {got[1]}`"
            )

    return errors


def check_makefile(makefile: Path) -> list[str]:
    if not makefile.exists():
        return ["Makefile manquant (interface uniforme up/down/attack/verify/clean)"]

    targets = set(TARGET_RE.findall(makefile.read_text(encoding="utf-8")))
    missing = [t for t in REQUIRED_MAKE_TARGETS if t not in targets]
    return [f"cible Make manquante : `{t}`" for t in missing]


def check_module(module: Path) -> list[str]:
    readme = module / "README.md"
    if not readme.exists():
        return ["README.md manquant — le write-up est la source unique de vérité"]
    return check_sections(readme) + check_makefile(module / "Makefile")


def discover(argv: list[str]) -> list[Path]:
    if argv:
        return [Path(a).resolve() for a in argv]
    if not MODULES_DIR.is_dir():
        return []
    return sorted(p for p in MODULES_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))


def main(argv: list[str]) -> int:
    modules = discover(argv)
    if not modules:
        print("Aucun module à vérifier.")
        return 0

    failed = 0
    for module in modules:
        errors = check_module(module)
        label = module.relative_to(ROOT) if module.is_relative_to(ROOT) else module
        if errors:
            failed += 1
            print(f"FAIL  {label}")
            for err in errors:
                print(f"        - {err}")
        else:
            print(f"ok    {label}")

    print(f"\n{len(modules) - failed}/{len(modules)} module(s) conforme(s) au gabarit.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
