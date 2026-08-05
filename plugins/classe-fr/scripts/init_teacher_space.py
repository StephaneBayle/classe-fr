#!/usr/bin/env python3
"""Initialiser un espace personnel séparé du code du plugin."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MODELS = PLUGIN_ROOT / "assets" / "modeles"


README_ESPACE = (
    "# Espace professeur\n\n"
    "Conserver ici uniquement des contenus professionnels anonymisés. "
    "Ne pas y placer de copie nominative, message familial ou donnée sensible.\n"
)


def copy_model(name: str, target: Path) -> bool:
    """Copier un modèle sans jamais écraser le travail déjà présent."""
    if target.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(MODELS / name, target)
    return True


def initialise(destination: Path) -> list[str]:
    """Créer ou compléter un espace personnel ; retourner les éléments créés.

    L'appel est répétable : un espace déjà présent est complété, jamais écrasé.
    """
    created: list[str] = []
    destination.mkdir(parents=True, exist_ok=True)
    for model, relative in (
        ("profil-enseignant.yml", Path("profil") / "enseignant.yml"),
        ("bibliotheque.yml", Path("bibliotheque") / "index.yml"),
        ("guide-style.md", Path("style") / "guide-style.md"),
        ("design-tokens.json", Path("style") / "design-tokens.json"),
        ("feedback.md", Path("feedbacks") / "feedback-modele.md"),
    ):
        if copy_model(model, destination / relative):
            created.append(str(relative))
    for name in ("productions", "corpus-style-anonymise"):
        dossier = destination / name
        if not dossier.exists():
            dossier.mkdir(parents=True)
            created.append(f"{name}/")
    readme = destination / "README.md"
    if not readme.exists():
        readme.write_text(README_ESPACE, encoding="utf-8")
        created.append("README.md")
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="Dossier personnel à créer")
    args = parser.parse_args()
    created = initialise(args.destination)
    if not created:
        print(f"Espace professeur déjà complet, rien à ajouter : {args.destination}")
        return
    print(f"Espace professeur à jour : {args.destination}")
    for element in created:
        print(f"- ajouté : {element}")


if __name__ == "__main__":
    main()
