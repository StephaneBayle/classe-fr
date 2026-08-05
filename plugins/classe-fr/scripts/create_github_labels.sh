#!/usr/bin/env sh
set -eu

# À exécuter après `gh auth login` et création du dépôt GitHub public.
REPOSITORY="StephaneBayle/classe-fr"

gh label create "feedback-enseignant" --repo "$REPOSITORY" --color "176B5B" --description "Retours enseignants" --force
gh label create "bug" --repo "$REPOSITORY" --color "D73A4A" --description "Dysfonctionnement reproductible" --force
gh label create "idee" --repo "$REPOSITORY" --color "0E8A16" --description "Proposition d'évolution" --force
gh label create "ressource" --repo "$REPOSITORY" --color "1D76DB" --description "Suggestion de ressource" --force
gh label create "besoin-pedagogique" --repo "$REPOSITORY" --color "5319E7" --description "Besoin pédagogique" --force
gh label create "cua-accessibilite" --repo "$REPOSITORY" --color "FBCA04" --description "Accessibilité ou CUA" --force
gh label create "confidentialite" --repo "$REPOSITORY" --color "B60205" --description "Sujet sensible sans pièce jointe" --force
gh label create "maintenance" --repo "$REPOSITORY" --color "6A737D" --description "Maintenance du dépôt et automatisations" --force
gh label create "urgent" --repo "$REPOSITORY" --color "D93F0B" --description "À traiter en priorité" --force
