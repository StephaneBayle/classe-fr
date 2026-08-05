# Revue humaine disciplinaire

Une famille ou un niveau ne passe jamais en **couverture validée** parce qu'un exemple fictif existe. Ce statut suppose une relecture explicite par une personne compétente, une source datée et une décision consignée. Cette référence décrit la procédure ; les statuts eux-mêmes vivent dans `references/matrice-couverture-discipline-niveau.md`.

Classe FR n'est pas une autorité pédagogique. Une couverture validée signifie qu'une personne compétente a relu et assumé une décision, pas que le plugin certifie une conformité officielle.

## Qui peut relire

- Un enseignant exerçant sur le niveau et la discipline concernés.
- Un formateur ou un conseiller pédagogique du domaine.
- Un pair compétent sur la voie ou le diplôme, notamment en voie professionnelle et en CFA.
- Un mainteneur du dépôt, à condition de s'appuyer sur une source institutionnelle datée et de le dire.

On consigne le **rôle** du relecteur, jamais son nom. Le registre est public : aucune identité, aucun établissement, aucune coordonnée n'y figure. Un relecteur qui souhaite être nommé peut l'être dans l'issue liée, à sa demande explicite.

## Ce qui doit être vérifié

Une revue est complète lorsque les sept points ont été examinés :

1. **Objectif** : l'objectif invariant est formulé, et il reste le même dans toutes les adaptations proposées.
2. **Niveau** : les attentes correspondent au niveau ou au cycle annoncé, sans avance ni retard implicite.
3. **Vocabulaire** : le lexique disciplinaire est juste et cohérent avec l'usage professionnel du domaine.
4. **Source** : chaque élément dépendant d'un programme, d'un référentiel ou d'un examen s'appuie sur une source datée.
5. **CUA** : les trois entrées sont réellement utiles, et non décoratives.
6. **Modalité évaluée** : quand une modalité constitue l'objectif, aucune adaptation ne la remplace par une expression non équivalente.
7. **Confidentialité** : aucun contenu identifiable, aucune donnée d'élève, aucun document réel issu d'une classe.

Un seul point non vérifié interdit la couverture validée. La décision reste alors « maintien en exemple contextualisé ».

## Ce qu'il faut consigner

Chaque revue produit une entrée dans `tests/fixtures/revues-disciplinaires-fictives.json` pour les cas de contrôle, et une entrée équivalente dans la matrice pour les décisions réelles :

- la famille et le niveau concernés ;
- le rôle du relecteur et la date de revue, au format AAAA-MM-JJ ;
- les sept points vérifiés ;
- la source retenue : organisme, URL publique et date de consultation ;
- la décision : **couverture validée**, **maintien en exemple contextualisé** ou **rétrogradation** ;
- les limites de la décision, c'est-à-dire ce qu'elle ne couvre pas ;
- la référence de décision : numéro d'issue ou entrée du journal de version ;
- la confirmation qu'aucune donnée personnelle n'est présente.

Les limites sont obligatoires même quand la décision est favorable : une couverture validée porte toujours sur un périmètre borné, jamais sur une discipline entière.

## Lier la décision

Toute décision est reliée à une issue du dépôt et reportée dans `CHANGELOG.md` à la publication suivante. La matrice cite la référence de décision dans sa colonne de preuve. Une cellule passée en couverture validée sans référence de décision est une erreur : le validateur la refuse.

## Quand rétrograder

Une couverture validée n'est pas acquise. Rétrograder vers « exemple contextualisé » dès que l'un de ces cas survient :

- la source citée a changé, a été retirée ou n'est plus datable ;
- un texte institutionnel modifie l'attendu, le référentiel ou le cadrage d'examen ;
- la revue trimestrielle de `references/revue-sources-institutionnelles.md` signale un changement constaté sur la source retenue ;
- un retour enseignant instruit montre que le repère induit en erreur.

La rétrogradation est elle-même une décision consignée, avec son motif. On ne retire jamais silencieusement une couverture : la trace du changement compte autant que le changement.

## Contrôle automatique

Les cas de contrôle sont fictifs. Exécuter :

```bash
python3 plugins/classe-fr/scripts/validate_revue_disciplinaire.py .
```

Le validateur refuse une décision de couverture validée sans les sept points vérifiés, sans source datée, sans limites ou sans référence de décision ; il refuse une rétrogradation sans motif, un nom de relecteur à la place d'un rôle, et tout signal de donnée personnelle.
