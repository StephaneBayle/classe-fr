#!/usr/bin/env python3
"""Valider le registre de revue des sources institutionnelles."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "source",
    "url",
    "niveaux_cycles",
    "disciplines",
    "date_consultation",
    "date_derniere_revue",
    "statut",
    "valide_par",
    "prochaine_revue",
    "decision_liee",
    "note_revue",
}
STATUSES = {"changement constaté", "à analyser", "aucun changement pertinent"}
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")


def validate_registry(path: Path) -> list[str]:
    """Contrôler le registre sans télécharger ni reproduire les sources externes."""
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Registre de sources illisible : {exc}"]
    if not isinstance(entries, list) or not entries:
        return ["Le registre de sources doit contenir au moins une entrée."]

    errors: list[str] = []
    ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("Chaque source doit être un objet JSON.")
            continue
        identifier = entry.get("id", "sans identifiant")
        missing = REQUIRED_FIELDS - set(entry)
        if missing:
            errors.append(f"{identifier} : métadonnées manquantes : {sorted(missing)}.")
            continue
        if not isinstance(identifier, str) or not identifier.strip() or identifier in ids:
            errors.append(f"{identifier} : identifiant absent ou dupliqué.")
        ids.add(identifier)
        for field in ("source", "url", "valide_par", "decision_liee", "note_revue"):
            if not isinstance(entry[field], str) or not entry[field].strip():
                errors.append(f"{identifier} : `{field}` doit être renseigné.")
        if not str(entry["url"]).startswith("https://"):
            errors.append(f"{identifier} : l'URL doit être publique et sécurisée (`https://`).")
        for field in ("niveaux_cycles", "disciplines"):
            if not isinstance(entry[field], list) or not entry[field] or not all(
                isinstance(value, str) and value.strip() for value in entry[field]
            ):
                errors.append(f"{identifier} : `{field}` doit être une liste non vide.")
        for field in ("date_consultation", "date_derniere_revue", "prochaine_revue"):
            if not isinstance(entry[field], str) or not DATE_PATTERN.fullmatch(entry[field]):
                errors.append(f"{identifier} : `{field}` doit respecter le format AAAA-MM-JJ.")
        if entry["statut"] not in STATUSES:
            errors.append(f"{identifier} : statut inconnu `{entry['statut']}`.")
    return errors


def format_review_report(entries: list[dict[str, object]]) -> str:
    """Produire un rapport court qui demande une décision humaine explicite."""
    lines = [
        "# Rapport de revue des sources",
        "",
        "| Source | Statut | Note constatée | Décision liée |",
        "| --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| {source} | {statut} | {note} | {decision} |".format(
                source=entry["source"],
                statut=entry["statut"],
                note=entry["note_revue"],
                decision=entry["decision_liee"],
            )
        )
    lines.extend(
        [
            "",
            "Aucune recommandation pédagogique n'est modifiée sans analyse et validation humaines.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    registry = root / "plugins" / "classe-fr" / "references" / "registre-sources-institutionnelles.json"
    errors = validate_registry(registry)
    if errors:
        print("Validation du registre de sources : échec")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Validation du registre de sources : réussie")


if __name__ == "__main__":
    main()
