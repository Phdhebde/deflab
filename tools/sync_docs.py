#!/usr/bin/env python3
"""Recopie les write-ups dans le site au moment du build.

Source unique de vérité : `modules/<slug>/README.md`. Le site ne duplique
jamais le contenu dans le dépôt — il le recopie à la volée dans `docs/modules/`
(répertoire ignoré par Git) avant `mkdocs build`.

Les liens relatifs des write-ups (`detections/...`, `evidence/...`) pointent
vers des fichiers qui n'existent pas dans le site : ils sont réécrits vers
GitHub pour rester cliquables des deux côtés.

Usage : python tools/sync_docs.py
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = ROOT / "modules"
OUT_DIR = ROOT / "docs" / "modules"

REPO_URL = "https://github.com/Phdhebde/deflab"
BRANCH = "main"

TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^>\s*\*\*Statut\s*:\*\*\s*([^·|\n]+)", re.MULTILINE)
# [texte](cible) où cible n'est ni absolue, ni une ancre, ni un mailto
RELATIVE_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()(?!https?://|#|mailto:|/)([^)]+)\)")


def rewrite_links(markdown: str, slug: str) -> str:
    """Réécrit les liens relatifs vers le dossier du module sur GitHub."""

    def repl(match: re.Match[str]) -> str:
        prefix, target = match.group(1), match.group(2).lstrip("./")
        kind = "raw" if prefix.startswith("!") else "blob"
        base = "https://raw.githubusercontent.com/Phdhebde/deflab" if kind == "raw" else f"{REPO_URL}/blob"
        return f"{prefix}{base}/{BRANCH}/modules/{slug}/{target})"

    return RELATIVE_LINK_RE.sub(repl, markdown)


def extract(markdown: str, pattern: re.Pattern[str], default: str) -> str:
    match = pattern.search(markdown)
    return match.group(1).strip() if match else default


def main() -> int:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    modules = []
    if MODULES_DIR.is_dir():
        modules = sorted(
            p for p in MODULES_DIR.iterdir()
            if p.is_dir() and not p.name.startswith(".") and (p / "README.md").exists()
        )

    rows = []
    for module in modules:
        slug = module.name
        markdown = (module / "README.md").read_text(encoding="utf-8-sig")
        title = extract(markdown, TITLE_RE, slug)
        status = extract(markdown, STATUS_RE, "—")

        body = rewrite_links(markdown, slug)
        body += (
            f"\n\n---\n\n"
            f"[:material-github: Voir le module sur GitHub]({REPO_URL}/tree/{BRANCH}/modules/{slug})\n"
        )
        (OUT_DIR / f"{slug}.md").write_text(body, encoding="utf-8")

        rows.append(f"| [{title}]({slug}.md) | {status} |")
        print(f"  {slug} -> docs/modules/{slug}.md")

    index = ["# Modules", ""]
    if rows:
        index += ["| Module | Statut |", "| --- | --- |", *rows]
    else:
        index += ["*Aucun module publié pour l'instant.*"]
    (OUT_DIR / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")

    print(f"{len(modules)} module(s) synchronisé(s) vers docs/modules/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
