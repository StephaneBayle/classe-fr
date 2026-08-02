#!/usr/bin/env python3
"""Initialiser un espace personnel séparé du code du plugin."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MODELS = PLUGIN_ROOT / "assets" / "modeles"


def copy_model(name: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(MODELS / name, target)


def initialise(destination: Path) -> None:
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"L'espace existe déjà et n'est pas vide : {destination}")

    destination.mkdir(parents=True, exist_ok=True)
    copy_model("profil-enseignant.yml", destination / "profil" / "enseignant.yml")
    copy_model("bibliotheque.yml", destination / "bibliotheque" / "index.yml")
    copy_model("guide-style.md", destination / "style" / "guide-style.md")
    copy_model("design-tokens.json", destination / "style" / "design-tokens.json")
    copy_model("feedback.md", destination / "feedbacks" / "feedback-modele.md")
    for name in ("productions", "corpus-style-anonymise"):
        (destination / name).mkdir(exist_ok=True)
    (destination / "README.md").write_text(
        "# Espace professeur\n\n"
        "Conserver ici uniquement des contenus professionnels anonymisés. "
        "Ne pas y placer de copie nominative, message familial ou donnée sensible.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="Dossier personnel à créer")
    args = parser.parse_args()
    initialise(args.destination)
    print(f"Espace professeur créé : {args.destination}")


if __name__ == "__main__":
    main()
