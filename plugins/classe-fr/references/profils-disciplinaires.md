# Profils disciplinaires

Cette référence donne des repères transversaux par grande famille disciplinaire. Elle n'est ni un programme, ni un référentiel, ni une expertise disciplinaire validée : elle aide seulement à choisir des obstacles plausibles et des appuis CUA cohérents avant que l'enseignant ne décide. Les repères ci-dessous restent **à vérifier** auprès d'une source institutionnelle datée avant tout usage en classe.

| Famille | Objectif invariant type | Statut de couverture |
| --- | --- | --- |
| Français et langage | Comprendre puis produire un propos structuré, à l'oral ou à l'écrit | Appui transversal |
| Mathématiques | Raisonner sur une situation numérique ou géométrique et justifier | Exemple contextualisé |
| Sciences et technologie | Interpréter des données et conclure de façon argumentée | Exemple contextualisé |
| Langues vivantes | Comprendre et produire un message dans la langue cible | Appui transversal |
| Histoire, géographie et EMC | Mettre en relation des documents et argumenter | Appui transversal |
| Arts et éducation physique et sportive | Réaliser une production ou une performance et expliciter ses choix | Appui transversal |
| Enseignement professionnel et technologique | Conduire une procédure professionnelle en respectant étapes et sécurité | Exemple contextualisé |

## Garde-fous à respecter

- Ne jamais citer un programme, un attendu de fin de cycle ou un référentiel sans source datée ; à défaut, signaler que le repère est à vérifier.
- Ne jamais annoncer une **couverture validée** sans revue humaine disciplinaire consignée : rôle du relecteur, date et décision. Aucune famille n'atteint ce niveau aujourd'hui.
- Préserver l'objectif invariant : une adaptation change l'accès à la tâche, jamais l'apprentissage visé.
- Respecter la modalité évaluée quand elle est explicite : si la rédaction, l'oral ou le geste professionnel est l'objectif annoncé, il ne peut pas être remplacé par une expression non équivalente.
- Proposer les trois entrées CUA — engagement, représentation, action et expression — quand le livrable s'y prête.
- N'utiliser que des situations fictives ou anonymisées ; aucun profil ne contient de donnée personnelle.

## Contrôle automatique

Le jeu de contrôle est `tests/fixtures/profils-disciplinaires-fictifs.json`. Exécuter :

```bash
python3 plugins/classe-fr/scripts/validate_profils_disciplinaires.py .
```

Le message d'erreur indique la famille concernée et le garde-fou non respecté. Les statuts de couverture sont tenus à jour avec `references/matrice-couverture-discipline-niveau.md` et la procédure de revue reste décrite dans `references/revue-sources-institutionnelles.md`.
