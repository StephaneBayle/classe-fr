# Classe FR

Plugin Codex local et inclusif pour aider les enseignants exerçant en France, de la petite section au CFA.

## Principes

- Les documents d'élèves, évaluations nominatives et messages aux familles restent hors du dépôt.
- Les corpus de style et exemples de travail sont anonymisés avant usage.
- La CUA est intégrée à chaque production : objectif invariant, obstacles anticipés et options d'accès.
- Chaque proposition est relue, contextualisée et validée par l'enseignant.

## Démarrage

1. Installer le plugin depuis la marketplace locale du dépôt.
2. Créer un espace de travail personnel hors de Git :

   ```bash
   python3 plugins/classe-fr/scripts/init_teacher_space.py teacher-space
   ```

3. Compléter le profil, indexer les ressources, puis commencer par `$cadrage-annee-scolaire`.

## Feedback

Utiliser `$feedback-au-createur` pour structurer un retour sans donnée identifiable. Le plugin crée un brouillon Markdown à déposer dans le formulaire GitHub privé.

## Vérification locale

```bash
python3 plugins/classe-fr/scripts/validate_classe_fr.py .
python3 -m unittest discover -s tests -v
```
