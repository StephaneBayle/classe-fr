# Repository Guidelines

## Structure du projet

Le plugin est contenu dans `plugins/classe-fr/`. Ses dix compétences se trouvent dans `skills/<nom>/`, chacune avec un `SKILL.md` et `agents/openai.yaml`. Les modèles réutilisables sont dans `assets/modeles/`, les références pédagogiques et de confidentialité dans `references/`, et les scripts de maintenance dans `scripts/`.

Les tests sont dans `tests/`. La configuration de la marketplace est dans `.agents/plugins/`, tandis que le formulaire de feedback public et l’automatisation de validation sont dans `.github/`. Toute issue, tout commentaire ou toute pièce jointe peut être visible : n’y déposez jamais de donnée d’élève, capture d’ENT, message aux familles ou document identifiable.

## Développement et vérification

Ce dépôt ne possède pas de phase de build. Exécutez les deux contrôles avant toute proposition :

```bash
python3 plugins/classe-fr/scripts/validate_classe_fr.py .
python3 -m unittest discover -s tests -v
```

Le premier vérifie le manifeste, les compétences, les références, les modèles et les protections de confidentialité. Le second exécute les tests Python. Lancez aussi le premier contrôle après toute modification de `plugin.json`, d’une compétence ou d’un modèle.

## Style et conventions de nommage

Rédigez les contenus destinés aux enseignants en français clair, inclusif et directement actionnable. Préservez l’objectif invariant et les trois entrées CUA dans les livrables pédagogiques.

Utilisez le kebab-case pour les dossiers de compétences, par exemple `preparation-differenciation`. Indentez le Python avec quatre espaces, le JSON et le YAML avec deux espaces. Les scripts et tests doivent rester sans dépendance externe lorsque cela est possible. N’ajoutez pas de TODO non traité dans un `SKILL.md`.

## Tests et données sensibles

Ajoutez un test `test_<comportement>` pour chaque règle nouvelle. Utilisez uniquement des cas fictifs couvrant les niveaux concernés. Ne versionnez jamais de documents d’élèves, de captures d’ENT, de messages aux familles, de noms, d’adresses, de données de santé ni de pièces jointes identifiables. Les espaces personnels (`teacher-space/`, `teachers/`) restent locaux et ignorés par Git.

## Commits et pull requests

L’historique est encore court ; employez des messages brefs à l’impératif, par exemple `Ajoute la grille d’audit CUA`. Une pull request doit expliquer l’usage enseignant visé, lier l’issue associée, lister les validations exécutées et signaler tout impact sur la CUA, les sources ou la confidentialité. Ajoutez une capture uniquement si elle éclaire un changement d’interface ou de support.
