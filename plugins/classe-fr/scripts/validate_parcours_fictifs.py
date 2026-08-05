#!/usr/bin/env python3
"""Valider les cas fictifs de parcours pédagogiques représentatifs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPECTED_IDS = {
    "ps",
    "cp",
    "cm1-6e",
    "college",
    "lycee-general-technologique",
    "lycee-professionnel-cfa",
    "college-histoire-geographie-emc",
    "cm2-langues-vivantes",
    "college-technologie-numerique",
    "cm2-arts-plastiques",
    "college-education-musicale",
    "lycee-eps",
}
FAMILY_IDS = {
    "francais",
    "mathematiques",
    "histoire-geographie-emc",
    "sciences-svt-physique-chimie",
    "langues-vivantes",
    "technologie-numerique",
    "arts-plastiques-education-musicale",
    "eps",
    "voie-professionnelle-cfa",
    "maternelle",
}
CUA_ENTRIES = ("engagement", "representations", "action_expression")
SENSITIVE_PATTERNS = (
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"(?<!\d)(?:\+33|0)[1-9](?:[ .-]?\d{2}){4}(?!\d)"),
)


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_case(case: dict[str, object]) -> list[str]:
    """Retourner des erreurs courtes, relisibles par une personne enseignante."""
    errors: list[str] = []
    for field in ("id", "niveau", "discipline", "objectif_invariant", "support_imprimable", "sortie_attendue"):
        if not is_non_empty_string(case.get(field)):
            errors.append(f"Le champ `{field}` doit être renseigné.")

    if case.get("famille") not in FAMILY_IDS:
        errors.append(
            "Le parcours doit se rattacher à une famille de `references/profils-disciplinaires.md` : "
            + ", ".join(sorted(FAMILY_IDS))
            + "."
        )

    obstacles = case.get("obstacles")
    if not isinstance(obstacles, list) or not obstacles or not all(
        is_non_empty_string(item) for item in obstacles
    ):
        errors.append("Les obstacles anticipés doivent former une liste non vide.")

    options_cua = case.get("options_cua")
    if not isinstance(options_cua, dict):
        errors.append("Les trois entrées CUA sont obligatoires.")
    else:
        for entry in CUA_ENTRIES:
            options = options_cua.get(entry)
            if not isinstance(options, list) or not options or not all(
                is_non_empty_string(item) for item in options
            ):
                errors.append(f"Les options CUA `{entry}` doivent être une liste non vide.")

    source = case.get("source")
    if not isinstance(source, dict):
        errors.append("La source documentée est obligatoire.")
    else:
        for field in ("organisme", "url", "consultee_le"):
            if not is_non_empty_string(source.get(field)):
                errors.append(f"La source doit renseigner `{field}`.")
        if is_non_empty_string(source.get("url")) and not str(source["url"]).startswith("https://"):
            errors.append("La source doit utiliser une URL publique sécurisée (`https://`).")
        if is_non_empty_string(source.get("consultee_le")) and not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", str(source["consultee_le"])
        ):
            errors.append("La date de consultation doit respecter le format AAAA-MM-JJ.")

    if case.get("donnees_personnelles") is not False:
        errors.append("Le cas doit déclarer explicitement l'absence de données personnelles.")

    modalite_evaluee = case.get("modalite_evaluee")
    if modalite_evaluee is not None and not is_non_empty_string(modalite_evaluee):
        errors.append("La modalité évaluée doit être un texte ou `null`.")
    modalites_expression = case.get("modalites_expression")
    if not isinstance(modalites_expression, list) or not modalites_expression or not all(
        is_non_empty_string(item) for item in modalites_expression
    ):
        errors.append("Les modalités d'expression doivent former une liste non vide.")
    elif modalite_evaluee is None and len(modalites_expression) < 2:
        errors.append(
            "Sans modalité évaluée, prévoir au moins deux expressions équivalentes de l'objectif."
        )
    elif modalite_evaluee is not None and modalites_expression != [modalite_evaluee]:
        errors.append(
            "Quand la modalité est évaluée, ne pas la remplacer par une expression non équivalente."
        )
    return errors


def validate_dataset(path: Path) -> list[str]:
    """Valider le jeu de cas sans dépendance externe ni donnée personnelle."""
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Jeu de parcours fictifs illisible : {exc}"]
    if not isinstance(cases, list):
        return ["Le jeu de parcours fictifs doit être une liste JSON."]

    identifiers = {case.get("id") for case in cases if isinstance(case, dict)}
    if identifiers != EXPECTED_IDS:
        return [
            "Les contextes fictifs attendus sont : "
            + ", ".join(sorted(EXPECTED_IDS))
            + "."
        ]

    familles = {case.get("famille") for case in cases if isinstance(case, dict)}
    familles_absentes = FAMILY_IDS - familles
    if familles_absentes:
        return [
            "Les familles disciplinaires sans parcours fictif sont : "
            + ", ".join(sorted(familles_absentes))
            + "."
        ]

    errors: list[str] = []
    for case in cases:
        if not isinstance(case, dict):
            errors.append("Chaque parcours fictif doit être un objet JSON.")
            continue
        identifier = case.get("id", "sans identifiant")
        for error in validate_case(case):
            errors.append(f"{identifier} : {error}")
        serialized = json.dumps(case, ensure_ascii=False)
        if any(pattern.search(serialized) for pattern in SENSITIVE_PATTERNS):
            errors.append(f"{identifier} : le cas contient un signal de donnée personnelle.")
    return errors


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    fixture = root / "tests" / "fixtures" / "parcours-pedagogiques-fictifs.json"
    errors = validate_dataset(fixture)
    if errors:
        print("Validation des parcours fictifs : échec")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Validation des parcours fictifs : réussie")


if __name__ == "__main__":
    main()
