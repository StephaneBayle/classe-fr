#!/usr/bin/env python3
"""Valider les décisions fictives de revue humaine disciplinaire."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


DECISIONS = (
    "couverture validée",
    "maintien en exemple contextualisé",
    "rétrogradation",
)
VALIDATED_DECISION = "couverture validée"
DOWNGRADE_DECISION = "rétrogradation"
REQUIRED_CHECKS = (
    "objectif",
    "niveau",
    "vocabulaire",
    "source",
    "cua",
    "modalite_evaluee",
    "confidentialite",
)
REVIEWER_ROLES = ("enseignant", "formateur", "pair", "mainteneur", "conseiller")
FORBIDDEN_FIELDS = ("nom_relecteur", "relecteur", "etablissement", "courriel")
SENSITIVE_PATTERNS = (
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"(?<!\d)(?:\+33|0)[1-9](?:[ .-]?\d{2}){4}(?!\d)"),
)


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_source(source: object) -> list[str]:
    """Exiger une source publique réellement datable."""
    if not isinstance(source, dict):
        return ["La source retenue est obligatoire."]

    errors: list[str] = []
    for field in ("organisme", "url", "consultee_le"):
        if not is_non_empty_string(source.get(field)):
            errors.append(f"La source doit renseigner `{field}`.")
    if is_non_empty_string(source.get("url")) and not str(source["url"]).startswith("https://"):
        errors.append("La source doit utiliser une URL publique sécurisée (`https://`).")
    if is_non_empty_string(source.get("consultee_le")) and not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}", str(source["consultee_le"])
    ):
        errors.append("La date de consultation doit respecter le format AAAA-MM-JJ.")
    return errors


def validate_review(review: dict[str, object]) -> list[str]:
    """Retourner des erreurs courtes, relisibles par une personne enseignante."""
    errors: list[str] = []
    for field in ("id", "famille", "niveau", "role_relecteur", "limites", "reference_decision"):
        if not is_non_empty_string(review.get(field)):
            errors.append(f"Le champ `{field}` doit être renseigné.")

    role = review.get("role_relecteur")
    if is_non_empty_string(role) and not any(
        mot in str(role).lower() for mot in REVIEWER_ROLES
    ):
        errors.append(
            "Le relecteur doit être décrit par son rôle : "
            + ", ".join(REVIEWER_ROLES)
            + "."
        )
    for field in FORBIDDEN_FIELDS:
        if field in review:
            errors.append(f"Le registre est public : retirer le champ `{field}`.")

    revue_le = review.get("revue_le")
    if not is_non_empty_string(revue_le):
        errors.append("La date de revue doit être renseignée.")
    elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(revue_le)):
        errors.append("La date de revue doit respecter le format AAAA-MM-JJ.")

    points = review.get("points_verifies")
    if not isinstance(points, dict):
        errors.append("Les sept points de revue doivent être renseignés.")
        points = {}
    else:
        manquants = [point for point in REQUIRED_CHECKS if point not in points]
        if manquants:
            errors.append(
                "Points de revue absents : " + ", ".join(manquants) + "."
            )

    decision = review.get("decision")
    if decision not in DECISIONS:
        errors.append("La décision attendue est : " + ", ".join(DECISIONS) + ".")
    elif decision == VALIDATED_DECISION:
        non_verifies = [
            point for point in REQUIRED_CHECKS if points.get(point) is not True
        ]
        if non_verifies:
            errors.append(
                "Une couverture validée exige les sept points vérifiés ; il manque : "
                + ", ".join(non_verifies)
                + "."
            )
        errors.extend(validate_source(review.get("source")))
    elif decision == DOWNGRADE_DECISION and not is_non_empty_string(
        review.get("motif_retrogradation")
    ):
        errors.append("Une rétrogradation doit consigner son motif.")

    if review.get("donnees_personnelles") is not False:
        errors.append("La revue doit déclarer explicitement l'absence de données personnelles.")
    return errors


def validate_dataset(path: Path) -> list[str]:
    """Valider le jeu de revues sans dépendance externe ni donnée personnelle."""
    try:
        reviews = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Jeu de revues disciplinaires illisible : {exc}"]
    if not isinstance(reviews, list):
        return ["Le jeu de revues disciplinaires doit être une liste JSON."]

    decisions = {review.get("decision") for review in reviews if isinstance(review, dict)}
    manquantes = set(DECISIONS) - decisions
    if manquantes:
        return [
            "Les décisions de contrôle manquantes sont : "
            + ", ".join(sorted(manquantes))
            + "."
        ]

    errors: list[str] = []
    for review in reviews:
        if not isinstance(review, dict):
            errors.append("Chaque revue disciplinaire doit être un objet JSON.")
            continue
        identifier = review.get("id", "sans identifiant")
        for error in validate_review(review):
            errors.append(f"{identifier} : {error}")
        serialized = json.dumps(review, ensure_ascii=False)
        if any(pattern.search(serialized) for pattern in SENSITIVE_PATTERNS):
            errors.append(f"{identifier} : la revue contient un signal de donnée personnelle.")
    return errors


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    fixture = root / "tests" / "fixtures" / "revues-disciplinaires-fictives.json"
    errors = validate_dataset(fixture)
    if errors:
        print("Validation des revues disciplinaires : échec")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Validation des revues disciplinaires : réussie")


if __name__ == "__main__":
    main()
