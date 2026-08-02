# Contribuer à Classe FR

Merci de contribuer à Classe FR avec une attention particulière à la confidentialité, à l'accessibilité et aux usages réels des enseignants.

## Avant de proposer un changement

- Ouvrir ou lier une issue décrivant l'usage enseignant visé.
- Utiliser uniquement des exemples fictifs ou entièrement anonymisés.
- Ne jamais déposer de document d'élève, capture d'ENT, message aux familles, nom, adresse, donnée de santé ou donnée de handicap.
- Préserver l'objectif invariant et les trois entrées CUA dans les livrables pédagogiques : engagement, représentations variées, action et expression.

## Vérifications locales

Avant toute pull request, exécuter :

```bash
python3 plugins/classe-fr/scripts/validate_classe_fr.py .
python3 -m unittest discover -s tests -v
```

Relancer le premier contrôle après toute modification de `plugin.json`, d'une compétence, d'une référence ou d'un modèle.

## Pull requests

Une pull request doit indiquer :

- l'usage enseignant visé ;
- l'issue associée ;
- les validations exécutées ;
- l'impact éventuel sur la CUA, les sources ou la confidentialité.

Les captures d'écran et pièces jointes ne doivent contenir aucune donnée identifiable.
