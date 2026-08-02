#!/usr/bin/env python3
"""Valider un suivi fictif de triage des feedbacks enseignants."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


STATUSES = ("reçu", "à instruire", "planifié", "livré", "non retenu")
DELIVERED_PATH = ("reçu", "à instruire", "planifié", "livré")
SENSITIVE_PATTERNS = (
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"(?<!\d)(?:\+33|0)[1-9](?:[ .-]?\d{2}){4}(?!\d)"),
)


def validate_feedback(feedback: dict[str, object]) -> list[str]:
    """Vérifier qu'un retour fictif est traçable sans contenu identifiable."""
    errors: list[str] = []
    for field in ("id", "type", "decision", "issue_liee", "journal_version"):
        if not isinstance(feedback.get(field), str) or not feedback[field].strip():
            errors.append(f"Le champ `{field}` doit être renseigné.")
    for field in ("impact", "frequence", "faisabilite"):
        value = feedback.get(field)
        if not isinstance(value, int) or not 1 <= value <= 3:
            errors.append(f"`{field}` doit être un score entier de 1 à 3.")
    if feedback.get("confidentialite_confirmee") is not True:
        errors.append("La confirmation de confidentialité est obligatoire.")

    history = feedback.get("historique")
    if not isinstance(history, list) or not history:
        errors.append("L'historique de triage est obligatoire.")
    else:
        statuses = [step.get("statut") for step in history if isinstance(step, dict)]
        if any(status not in STATUSES for status in statuses):
            errors.append("L'historique contient un statut de triage inconnu.")
        decision = feedback.get("decision")
        if decision == "livré" and statuses != list(DELIVERED_PATH):
            errors.append("Un feedback livré doit suivre : reçu, à instruire, planifié, livré.")
        if decision == "non retenu" and statuses != ["reçu", "à instruire", "non retenu"]:
            errors.append("Un feedback non retenu doit indiquer la décision après instruction.")
        for step in history:
            if not isinstance(step, dict) or not isinstance(step.get("date"), str) or not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}", step.get("date", "")
            ):
                errors.append("Chaque étape doit contenir une date au format AAAA-MM-JJ.")
                break
    serialized = json.dumps(feedback, ensure_ascii=False)
    if any(pattern.search(serialized) for pattern in SENSITIVE_PATTERNS):
        errors.append("Le suivi ne doit contenir aucun signal de donnée personnelle.")
    return errors


def validate_dataset(path: Path) -> list[str]:
    try:
        feedbacks = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Jeu de triage fictif illisible : {exc}"]
    if not isinstance(feedbacks, list) or len(feedbacks) != 3:
        return ["Le jeu de triage doit contenir exactement trois feedbacks fictifs."]
    errors: list[str] = []
    for feedback in feedbacks:
        if not isinstance(feedback, dict):
            errors.append("Chaque feedback doit être un objet JSON.")
            continue
        identifier = feedback.get("id", "sans identifiant")
        errors.extend(f"{identifier} : {error}" for error in validate_feedback(feedback))
    return errors


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    fixture = root / "tests" / "fixtures" / "triage-feedbacks-fictifs.json"
    errors = validate_dataset(fixture)
    if errors:
        print("Validation du triage fictif : échec")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Validation du triage fictif : réussie")


if __name__ == "__main__":
    main()
