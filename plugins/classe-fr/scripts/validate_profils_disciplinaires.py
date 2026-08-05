#!/usr/bin/env python3
"""Valider les garde-fous des profils disciplinaires fictifs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPECTED_FAMILIES = {
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
COVERAGE_LEVELS = ("appui transversal", "exemple contextualisé", "couverture validée")
VALIDATED_COVERAGE = "couverture validée"
RESERVE_MARKERS = ("à vérifier", "à confirmer")
SENSITIVE_PATTERNS = (
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"(?<!\d)(?:\+33|0)[1-9](?:[ .-]?\d{2}){4}(?!\d)"),
)


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_non_empty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(
        is_non_empty_string(item) for item in value
    )


def validate_adaptation(adaptation: object) -> list[str]:
    """Vérifier qu'une adaptation type ne change ni l'objectif ni la modalité évaluée."""
    if not isinstance(adaptation, dict):
        return ["Chaque adaptation type doit être un objet JSON."]

    errors: list[str] = []
    if not is_non_empty_string(adaptation.get("situation")):
        errors.append("Le champ `situation` de l'adaptation doit être renseigné.")
    if adaptation.get("objectif_invariant_preserve") is not True:
        errors.append("Une adaptation type doit déclarer que l'objectif invariant est préservé.")

    modalite_evaluee = adaptation.get("modalite_evaluee")
    if modalite_evaluee is not None and not is_non_empty_string(modalite_evaluee):
        errors.append("La modalité évaluée doit être un texte ou `null`.")
    modalites_expression = adaptation.get("modalites_expression")
    if not is_non_empty_string_list(modalites_expression):
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


def validate_profile(profile: dict[str, object]) -> list[str]:
    """Retourner des erreurs courtes, relisibles par une personne enseignante."""
    errors: list[str] = []
    for field in ("id", "famille", "objectif_invariant_type"):
        if not is_non_empty_string(profile.get(field)):
            errors.append(f"Le champ `{field}` doit être renseigné.")

    if not is_non_empty_string_list(profile.get("obstacles_frequents")):
        errors.append("Les obstacles fréquents doivent former une liste non vide.")
    if not is_non_empty_string_list(profile.get("modalites_souvent_evaluees")):
        errors.append("Les modalités souvent évaluées doivent former une liste non vide.")
    if not is_non_empty_string_list(profile.get("formes_de_trace")):
        errors.append("Les formes de trace possibles doivent former une liste non vide.")
    if not is_non_empty_string_list(profile.get("points_de_vigilance")):
        errors.append("Les points de vigilance doivent former une liste non vide.")
    if not is_non_empty_string_list(profile.get("sources_a_verifier")):
        errors.append("Les sources institutionnelles à vérifier doivent former une liste non vide.")

    appuis_cua = profile.get("appuis_cua")
    if not isinstance(appuis_cua, dict):
        errors.append("Les trois entrées CUA sont obligatoires.")
    else:
        for entry in CUA_ENTRIES:
            if not is_non_empty_string_list(appuis_cua.get(entry)):
                errors.append(f"Les appuis CUA `{entry}` doivent être une liste non vide.")

    reserve = profile.get("reserve_source")
    if not is_non_empty_string(reserve):
        errors.append("Le profil doit porter une réserve explicite sur la source.")
    elif not any(marker in str(reserve).lower() for marker in RESERVE_MARKERS):
        errors.append(
            "La réserve doit indiquer que la source reste à vérifier ou à confirmer."
        )

    statut = profile.get("statut_couverture")
    revue = profile.get("revue_humaine")
    if statut not in COVERAGE_LEVELS:
        errors.append(
            "Le statut de couverture attendu est : " + ", ".join(COVERAGE_LEVELS) + "."
        )
    elif statut == VALIDATED_COVERAGE:
        if not isinstance(revue, dict):
            errors.append(
                "Une couverture validée exige une revue humaine disciplinaire consignée."
            )
        else:
            for field in ("role_relecteur", "revue_le", "decision", "limites", "reference_decision"):
                if not is_non_empty_string(revue.get(field)):
                    errors.append(f"La revue humaine doit renseigner `{field}`.")
            if "nom_relecteur" in revue:
                errors.append("Le registre est public : consigner un rôle, jamais un nom.")
            if is_non_empty_string(revue.get("revue_le")) and not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}", str(revue["revue_le"])
            ):
                errors.append("La date de revue doit respecter le format AAAA-MM-JJ.")
    elif revue is not None and not isinstance(revue, dict):
        errors.append("La revue humaine doit être un objet JSON ou `null`.")

    if profile.get("validation_humaine_requise") is not True:
        errors.append("Le profil doit rappeler que la validation humaine reste requise.")
    if profile.get("donnees_personnelles") is not False:
        errors.append("Le profil doit déclarer explicitement l'absence de données personnelles.")

    adaptations = profile.get("adaptations_types")
    if not isinstance(adaptations, list) or not adaptations:
        errors.append("Les adaptations types doivent former une liste non vide.")
    else:
        for adaptation in adaptations:
            errors.extend(validate_adaptation(adaptation))
    return errors


def validate_dataset(path: Path) -> list[str]:
    """Valider le jeu de profils sans dépendance externe ni donnée personnelle."""
    try:
        profiles = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Jeu de profils disciplinaires illisible : {exc}"]
    if not isinstance(profiles, list):
        return ["Le jeu de profils disciplinaires doit être une liste JSON."]

    identifiers = {profile.get("id") for profile in profiles if isinstance(profile, dict)}
    missing = EXPECTED_FAMILIES - identifiers
    if missing:
        return [
            "Les grandes familles disciplinaires manquantes sont : "
            + ", ".join(sorted(missing))
            + "."
        ]

    errors: list[str] = []
    for profile in profiles:
        if not isinstance(profile, dict):
            errors.append("Chaque profil disciplinaire doit être un objet JSON.")
            continue
        identifier = profile.get("id", "sans identifiant")
        for error in validate_profile(profile):
            errors.append(f"{identifier} : {error}")
        serialized = json.dumps(profile, ensure_ascii=False)
        if any(pattern.search(serialized) for pattern in SENSITIVE_PATTERNS):
            errors.append(f"{identifier} : le profil contient un signal de donnée personnelle.")
    return errors


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    fixture = root / "tests" / "fixtures" / "profils-disciplinaires-fictifs.json"
    errors = validate_dataset(fixture)
    if errors:
        print("Validation des profils disciplinaires : échec")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Validation des profils disciplinaires : réussie")


if __name__ == "__main__":
    main()
