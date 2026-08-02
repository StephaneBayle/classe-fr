#!/usr/bin/env python3
"""Contrôles légers et sans dépendance pour le dépôt Classe FR."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPECTED_SKILLS = {
    "cadrage-annee-scolaire",
    "bibliotheque-pedagogique",
    "style-et-design-prof",
    "programmation-annuelle",
    "preparation-differenciation",
    "cua-accessibilite-pedagogique",
    "evaluation-retours",
    "communication-familles",
    "bilan-de-periode",
    "feedback-au-createur",
}
REQUIRED_REFERENCES = {
    "niveaux-et-cycles.md",
    "cua-et-accessibilite.md",
    "sources-et-droits.md",
    "confidentialite.md",
    "parcours-pedagogiques-fictifs.md",
    "revue-sources-institutionnelles.md",
    "triage-feedbacks-enseignants.md",
    "matrice-couverture-discipline-niveau.md",
}
REQUIRED_CONTENT = {
    "references/cua-et-accessibilite.md": (
        "Objectif invariant",
        "Engagement",
        "Représentation",
        "Action et expression",
    ),
    "references/sources-et-droits.md": ("Éduscol", "Primàbord", "Ne pas aspirer"),
    "references/confidentialite.md": ("aucun nom", "donnée de handicap", "CNIL"),
    "assets/modeles/grille-cua.md": (
        "Objectif invariant",
        "Engagement",
        "Représentations variées",
        "Action et expression",
    ),
    "assets/modeles/audit-support-accessible.md": (
        "Exigences respectées",
        "Points à renforcer",
        "Choix pédagogique à valider",
        "Engagement",
        "Représentations variées",
        "Action et expression",
        "version imprimable",
    ),
    "assets/modeles/feedback.md": ("cua-accessibilite", "aucun nom"),
    "references/parcours-pedagogiques-fictifs.md": (
        "PS",
        "CP",
        "CM1 / 6e",
        "Collège",
        "Lycée général ou technologique",
        "Lycée professionnel ou CFA",
    ),
    "references/revue-sources-institutionnelles.md": (
        "tous les trois mois",
        "changement constaté",
        "à analyser",
        "aucun changement pertinent",
    ),
    "references/triage-feedbacks-enseignants.md": (
        "tous les quinze jours",
        "reçu",
        "à instruire",
        "planifié",
        "livré",
        "non retenu",
    ),
    "references/matrice-couverture-discipline-niveau.md": (
        "Appui transversal",
        "Exemple contextualisé",
        "Couverture validée",
        "PS",
        "CP",
        "CM1 / 6e",
        "Collège",
        "Lycée général ou technologique",
        "Lycée professionnel ou CFA",
        "Aucune cellule n'atteint encore ce niveau",
    ),
}
CLAUDE_REQUIRED_TERMS = (
    "classe-fr-pedagogie",
    "confidentialité",
    "objectif invariant",
    "engagement",
    "représentation",
    "action et expression",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    plugin = root / "plugins" / "classe-fr"
    manifest_path = plugin / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Manifest illisible : {exc}"]

    if manifest.get("name") != "classe-fr":
        fail(errors, "Le manifest doit porter le nom classe-fr.")
    if manifest.get("version") != "0.1.0":
        fail(errors, "La version attendue est 0.1.0.")
    if manifest.get("license") != "UNLICENSED":
        fail(errors, "La licence du pilote doit être UNLICENSED.")
    if not manifest.get("author", {}).get("name"):
        fail(errors, "Le manifest doit indiquer un auteur.")
    if len(manifest.get("interface", {}).get("defaultPrompt", [])) > 3:
        fail(errors, "Le manifest ne peut contenir que trois prompts par défaut.")
    if manifest.get("interface", {}).get("category") != "Education":
        fail(errors, "La catégorie du plugin doit être Education.")

    skills_dir = plugin / "skills"
    actual_skills = {item.name for item in skills_dir.iterdir() if item.is_dir()}
    if actual_skills != EXPECTED_SKILLS:
        fail(errors, f"Compétences attendues : {sorted(EXPECTED_SKILLS)} ; obtenues : {sorted(actual_skills)}")
    for name in EXPECTED_SKILLS:
        skill = skills_dir / name / "SKILL.md"
        metadata = skills_dir / name / "agents" / "openai.yaml"
        if not skill.exists() or not metadata.exists():
            fail(errors, f"Compétence incomplète : {name}")
            continue
        content = skill.read_text(encoding="utf-8")
        interface = metadata.read_text(encoding="utf-8")
        if "[TODO:" in content or not re.search(r"^description: .+", content, re.MULTILINE):
            fail(errors, f"Instructions non finalisées : {name}")
        if f"${name}" not in interface:
            fail(errors, f"Prompt d'interface invalide : {name}")

    claude_memory = root / "CLAUDE.md"
    claude_agent = plugin / "agents" / "classe-fr-pedagogie.md"
    claude_project_agent = root / ".claude" / "agents" / "classe-fr-pedagogie.md"
    if not claude_memory.is_file():
        fail(errors, "Le fichier CLAUDE.md est requis pour Claude Code/Cowork.")
    else:
        memory_content = claude_memory.read_text(encoding="utf-8")
        for term in CLAUDE_REQUIRED_TERMS:
            if term not in memory_content:
                fail(errors, f"CLAUDE.md doit rappeler : {term}")
        for name in EXPECTED_SKILLS:
            if name not in memory_content:
                fail(errors, f"CLAUDE.md doit référencer la compétence : {name}")
    if not claude_agent.is_file():
        fail(errors, "L'agent Claude classe-fr-pedagogie est requis.")
    else:
        agent_content = claude_agent.read_text(encoding="utf-8")
        for term in ("name: classe-fr-pedagogie", "tools: Read, Glob, Grep", "donnée d'élève identifiable"):
            if term not in agent_content:
                fail(errors, f"Agent Claude incomplet : {term}")
        for name in EXPECTED_SKILLS:
            if name not in agent_content:
                fail(errors, f"L'agent Claude doit router vers : {name}")
    if not claude_project_agent.is_file():
        fail(errors, "Le wrapper .claude/agents/classe-fr-pedagogie.md est requis.")
    else:
        project_agent_content = claude_project_agent.read_text(encoding="utf-8")
        for term in (
            "name: classe-fr-pedagogie",
            "plugins/classe-fr/agents/classe-fr-pedagogie.md",
            "aucune donnée d'élève identifiable",
        ):
            if term not in project_agent_content:
                fail(errors, f"Wrapper Claude incomplet : {term}")

    references = {item.name for item in (plugin / "references").glob("*.md")}
    missing = REQUIRED_REFERENCES - references
    if missing:
        fail(errors, f"Références manquantes : {sorted(missing)}")
    for relative_path, expected_terms in REQUIRED_CONTENT.items():
        source = plugin / relative_path
        if not source.is_file():
            fail(errors, f"Élément manquant : {relative_path}")
            continue
        content = source.read_text(encoding="utf-8")
        for term in expected_terms:
            if term not in content:
                fail(errors, f"Contenu requis absent de {relative_path} : {term}")
    precontrol = plugin / "scripts" / "precontrole_anonymisation.py"
    if not precontrol.is_file() or "--confirme-relecture" not in precontrol.read_text(encoding="utf-8"):
        fail(errors, "Le pré-contrôle local d'anonymisation est incomplet.")
    parcours_validator = plugin / "scripts" / "validate_parcours_fictifs.py"
    fixture = root / "tests" / "fixtures" / "parcours-pedagogiques-fictifs.json"
    if not parcours_validator.is_file() or not fixture.is_file():
        fail(errors, "Les parcours pédagogiques fictifs et leur validateur sont requis.")
    registry_validator = plugin / "scripts" / "validate_registre_sources.py"
    registry = plugin / "references" / "registre-sources-institutionnelles.json"
    report = plugin / "assets" / "modeles" / "rapport-revue-sources.md"
    if not registry_validator.is_file() or not registry.is_file() or not report.is_file():
        fail(errors, "Le registre versionné des sources et son rapport sont requis.")
    feedback_validator = plugin / "scripts" / "validate_triage_feedback.py"
    feedback_fixture = root / "tests" / "fixtures" / "triage-feedbacks-fictifs.json"
    if not feedback_validator.is_file() or not feedback_fixture.is_file():
        fail(errors, "Le cycle de triage fictif des feedbacks est requis.")
    tokens_path = plugin / "assets" / "modeles" / "design-tokens.json"
    try:
        tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
        accessibility = tokens.get("accessibilite", {})
        layout = tokens.get("mise_en_page", {})
        if not accessibility.get("contraste_renforce") or layout.get("information_par_couleur_seule") is not False:
            fail(errors, "Les tokens doivent imposer le contraste et proscrire la couleur seule.")
    except (OSError, json.JSONDecodeError):
        fail(errors, "Les design tokens doivent être un JSON valide.")
    feedback_form = root / ".github" / "ISSUE_TEMPLATE" / "teacher-feedback.yml"
    labels_script = plugin / "scripts" / "create_github_labels.sh"
    if not feedback_form.is_file() or "cua-accessibilite" not in feedback_form.read_text(encoding="utf-8"):
        fail(errors, "Le formulaire GitHub doit couvrir les feedbacks CUA.")
    if not labels_script.is_file() or "feedback-enseignant" not in labels_script.read_text(encoding="utf-8"):
        fail(errors, "La procédure de labels GitHub est incomplète.")
    license_path = root / "LICENSE"
    try:
        license_text = license_path.read_text(encoding="utf-8")
    except OSError:
        fail(errors, "Le fichier LICENSE est requis.")
        license_text = ""
    if "source disponible propriétaire" not in license_text:
        fail(errors, "La licence doit clarifier le statut propriétaire source disponible.")
    if "confidentiel" in license_text.lower() or "pilote privé" in license_text.lower():
        fail(errors, "La licence ne doit pas qualifier le dépôt public de confidentiel ou privé.")
    readme = (root / "README.md").read_text(encoding="utf-8")
    for term in ("Description courte", "Topics recommandés", "source disponible propriétaire"):
        if term not in readme:
            fail(errors, f"README incomplet pour les bonnes pratiques GitHub : {term}")
    for relative_path in (
        "CONTRIBUTING.md",
        "SECURITY.md",
        ".github/CODEOWNERS",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/dependabot.yml",
    ):
        if not (root / relative_path).is_file():
            fail(errors, f"Document GitHub manquant : {relative_path}")
    if "maintenance" not in labels_script.read_text(encoding="utf-8"):
        fail(errors, "Le label maintenance doit être prévu pour Dependabot.")
    ignored = (root / ".gitignore").read_text(encoding="utf-8")
    if "teacher-space/" not in ignored or "teachers/" not in ignored:
        fail(errors, "Les espaces personnels doivent être ignorés par Git.")
    return errors


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)
    if errors:
        print("Validation Classe FR : échec")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Validation Classe FR : réussie")


if __name__ == "__main__":
    main()
