# Matrice de couverture discipline × niveau

Cette matrice décrit le périmètre réellement documenté du pilote ; elle ne promet pas une couverture uniforme des disciplines ni des classes. Une cellule ne devient pas « validée » parce qu'elle existe dans une démonstration.

| Niveau ou voie | Discipline ou contexte | Appui transversal | Exemple contextualisé | Couverture validée | Preuve actuelle |
| --- | --- | --- | --- | --- | --- |
| PS | Langage oral | CUA, préparation, support imprimable | Ordonner les étapes d'un récit entendu | À construire | Parcours fictif `ps` |
| CP | Français | CUA, préparation, évaluation | Repérer une information explicitement écrite | À construire | Parcours fictif `cp` |
| CM1 / 6e | Mathématiques | CUA, préparation, programmation | Comparer deux fractions simples | À construire | Parcours fictif `cm1-6e` |
| Collège | Sciences de la vie et de la Terre | CUA, préparation, évaluation | Interpréter un graphique de données | À construire | Parcours fictif `college` |
| Lycée général ou technologique | Physique-chimie | CUA, préparation, évaluation | Justifier une démarche de résolution | À construire | Parcours fictif `lycee-general-technologique` |
| Lycée professionnel ou CFA | Enseignement professionnel | CUA, préparation, programmation | Ordonner une procédure professionnelle fictive | À construire | Parcours fictif `lycee-professionnel-cfa` |
| PS au CFA | Toute autre discipline ou voie | CUA, style de support, bibliothèque et confidentialité | Aucun exemple disciplinaire à ce stade | À construire | Aucun parcours contextualisé |

## Lire les niveaux de couverture

- **Appui transversal** : une compétence ou une règle commune aide à concevoir un support, sans exemple disciplinaire spécifique.
- **Exemple contextualisé** : un parcours fictif documente un objectif invariant, des obstacles, des options CUA, une source et une sortie courte pour un contexte donné.
- **Couverture validée** : un parcours contextualisé a été revu par une personne compétente sur le niveau et la discipline, avec une source datée et une décision consignée. **Aucune cellule n'atteint encore ce niveau dans le pilote.**

Les six parcours du premier lot sont conservés dans `tests/fixtures/parcours-pedagogiques-fictifs.json` et résumés dans `references/parcours-pedagogiques-fictifs.md`. Ils permettent de vérifier l'objectif invariant, les obstacles, les trois entrées CUA, la source documentée, l'absence de donnée personnelle et le support imprimable ; ce ne sont pas des séquences prêtes à prescrire.

## Prioriser les prochaines contributions

1. Partir des retours anonymes triés selon `references/triage-feedbacks-enseignants.md` : confidentialité et CUA passent avant toute autre demande.
2. Relever les zones sans exemple contextualisé, puis rechercher l'impact pédagogique, la fréquence anonymisée et la faisabilité.
3. Préparer un parcours fictif avec objectif invariant, obstacles, options CUA, source datée et résultat attendu court.
4. Demander une revue humaine disciplinaire avant de passer une cellule à « Couverture validée » ; lier la décision à une issue et au journal de version.

La matrice est maintenue à chaque ajout ou retrait de parcours. Ne jamais y ajouter de nom d'élève, de classe identifiable, de capture ou de ressource copiée sans droit.
