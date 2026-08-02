#!/usr/bin/env python3
"""Repérer localement des signaux de données identifiantes avant un usage.

Ce contrôle est volontairement limité : il émet des avertissements, ne garantit
pas l'anonymisation et ne remplace jamais la relecture de l'enseignant.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


SUPPORTED_SUFFIXES = {".csv", ".html", ".json", ".md", ".txt", ".yaml", ".yml"}
PATTERNS = {
    "adresse e-mail": re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    "numéro de téléphone": re.compile(
        r"(?<!\d)(?:\+33|0)[1-9](?:[ .-]?\d{2}){4}(?!\d)"
    ),
    "adresse postale possible": re.compile(
        r"\b\d{1,4}\s+(?:bis\s+|ter\s+)?"
        r"(?:rue|avenue|boulevard|chemin|impasse|allée|place|route)\b",
        re.IGNORECASE,
    ),
    "identifiant possible": re.compile(r"\b(?:[A-Z]{2}\d{6,}|\d{10}[A-Z])\b"),
    "nom complet possible": re.compile(
        r"\b[A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]{1,}\s+[A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]{1,}\b"
    ),
}


def lire_document(path: Path) -> str:
    """Lire uniquement un fichier texte local pris en charge, sans le modifier."""
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        suffixes = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise ValueError(f"Format non pris en charge. Formats texte : {suffixes}.")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Le fichier doit être encodé en UTF-8.") from exc
    except OSError as exc:
        raise ValueError(f"Fichier illisible : {exc}") from exc


def detecter_signaux(text: str) -> dict[str, list[int]]:
    """Retourner les catégories et lignes à relire, sans conserver les extraits."""
    signaux: dict[str, list[int]] = defaultdict(list)
    for numero, line in enumerate(text.splitlines(), start=1):
        for categorie, pattern in PATTERNS.items():
            if pattern.search(line):
                signaux[categorie].append(numero)
    return dict(signaux)


def formater_rapport(signaux: dict[str, list[int]]) -> str:
    """Présenter les seuls emplacements à relire, jamais le texte analysé."""
    if not signaux:
        return (
            "Pré-contrôle local terminé : aucun signal usuel détecté.\n"
            "Ce résultat ne prouve pas l'anonymisation : relisez le document."
        )
    lignes = [
        "Pré-contrôle local : avertissements détectés.",
        "Aucun extrait n'est affiché, transmis ou enregistré par cet outil.",
        "Relisez et anonymisez les passages signalés avant toute utilisation.",
    ]
    for categorie, numeros in sorted(signaux.items()):
        positions = ", ".join(str(numero) for numero in numeros)
        lignes.append(f"- {categorie} : ligne(s) {positions}")
    return "\n".join(lignes)


def analyser(path: Path) -> dict[str, list[int]]:
    """Analyser un document local sans l'envoyer, le copier ni le journaliser."""
    return detecter_signaux(lire_document(path))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path, help="Fichier texte local à relire")
    parser.add_argument(
        "--confirme-relecture",
        action="store_true",
        help="Confirme que l'enseignant a relu le document avant son usage.",
    )
    args = parser.parse_args()

    try:
        signaux = analyser(args.document)
    except ValueError as exc:
        parser.error(str(exc))

    print(formater_rapport(signaux))
    if signaux:
        raise SystemExit(2)
    if not args.confirme_relecture:
        print("Ajoutez --confirme-relecture seulement après votre relecture explicite.")
        raise SystemExit(3)
    print("Relecture explicitement confirmée : le document reste sous votre contrôle local.")


if __name__ == "__main__":
    main()
