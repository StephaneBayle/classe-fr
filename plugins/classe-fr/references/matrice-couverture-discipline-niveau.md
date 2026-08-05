# Matrice de couverture discipline × niveau

Cette matrice décrit le périmètre réellement documenté du pilote ; elle ne promet pas une couverture uniforme des disciplines ni des classes. Une cellule ne devient pas « validée » parce qu'elle existe dans une démonstration. Pour une lecture plus directe côté enseignant, consulter aussi `../../../CONFIANCE.md`. Les repères de conception par matière sont dans `references/profils-disciplinaires.md` ; ils ne modifient aucun statut de cette matrice.

| Niveau ou voie | Discipline ou contexte | Appui transversal | Exemple contextualisé | Couverture validée | Preuve actuelle |
| --- | --- | --- | --- | --- | --- |
| PS | Langage oral | CUA, préparation, support imprimable | Ordonner les étapes d'un récit entendu | À construire | Parcours fictif `ps` |
| CP | Français | CUA, préparation, évaluation | Repérer une information explicitement écrite | À construire | Parcours fictif `cp` |
| CM1 / 6e | Mathématiques | CUA, préparation, programmation | Comparer deux fractions simples | À construire | Parcours fictif `cm1-6e` |
| Collège | Sciences de la vie et de la Terre | CUA, préparation, évaluation | Interpréter un graphique de données | À construire | Parcours fictif `college` |
| Lycée général ou technologique | Physique-chimie | CUA, préparation, évaluation | Justifier une démarche de résolution | À construire | Parcours fictif `lycee-general-technologique` |
| Lycée professionnel ou CFA | Enseignement professionnel | CUA, préparation, programmation | Ordonner une procédure professionnelle fictive | À construire | Parcours fictif `lycee-professionnel-cfa` |
| PS au CFA | Toute autre discipline ou voie | CUA, style de support, bibliothèque et confidentialité | Aucun exemple disciplinaire à ce stade | À construire | Aucun parcours contextualisé |

## Couverture par famille disciplinaire

Cette seconde entrée relit le même périmètre par famille disciplinaire, à partir de `references/profils-disciplinaires.md`. Une famille passe d'« Appui transversal » à « Exemple contextualisé » uniquement lorsqu'un parcours fictif documente un contexte de cette famille. Les dix familles ont désormais au moins un parcours ; c'est un progrès de couverture d'exemples, pas de validation. Un exemple fictif ne vaut jamais prescription et la colonne « Couverture validée » reste « À construire » partout, faute de revue humaine disciplinaire.

| Niveau ou voie | Famille disciplinaire | Appui transversal | Exemple contextualisé | Statut de couverture | Couverture validée | Preuve actuelle |
| --- | --- | --- | --- | --- | --- | --- |
| CP | Français | CUA, préparation, évaluation | Repérer une information explicitement écrite | Exemple contextualisé | À construire | Profil `francais` et parcours fictif `cp` |
| CM1 / 6e | Mathématiques | CUA, préparation, programmation | Comparer deux fractions simples | Exemple contextualisé | À construire | Profil `mathematiques` et parcours fictif `cm1-6e` |
| 4e | Histoire, géographie et EMC | CUA, préparation, évaluation | Mettre en relation deux documents fictifs | Exemple contextualisé | À construire | Profil `histoire-geographie-emc` et parcours fictif `college-histoire-geographie-emc` |
| Collège et lycée général ou technologique | Sciences, SVT et physique-chimie | CUA, préparation, évaluation | Interpréter un graphique ; justifier une démarche | Exemple contextualisé | À construire | Profil `sciences-svt-physique-chimie` et parcours fictifs `college` et `lycee-general-technologique` |
| CM2 | Langues vivantes | CUA, préparation, évaluation | Comprendre un document audio court | Exemple contextualisé | À construire | Profil `langues-vivantes` et parcours fictif `cm2-langues-vivantes` |
| 4e | Technologie et numérique | CUA, style de support, bibliothèque | Expliciter une démarche de modification technique | Exemple contextualisé | À construire | Profil `technologie-numerique` et parcours fictif `college-technologie-numerique` |
| CM2 et 6e | Arts plastiques et éducation musicale | CUA, style de support | Expliciter deux choix plastiques ; repérer un contraste sonore | Exemple contextualisé | À construire | Profil `arts-plastiques-education-musicale` et parcours fictifs `cm2-arts-plastiques` et `college-education-musicale` |
| 2de | Éducation physique et sportive | CUA, préparation | Réaliser une performance motrice et l'analyser | Exemple contextualisé | À construire | Profil `eps` et parcours fictif `lycee-eps` |
| Lycée professionnel ou CFA | Voie professionnelle et CFA | CUA, préparation, programmation | Ordonner une procédure professionnelle fictive | Exemple contextualisé | À construire | Profil `voie-professionnelle-cfa` et parcours fictif `lycee-professionnel-cfa` |
| PS | Maternelle, par domaines d'apprentissage | CUA, préparation, support imprimable | Ordonner les étapes d'un récit entendu | Exemple contextualisé | À construire | Profil `maternelle` et parcours fictif `ps` |

Les statuts de ce tableau sont tenus identiques à ceux de `tests/fixtures/profils-disciplinaires-fictifs.json` ; un écart fait échouer les tests du dépôt. Aucun programme, référentiel ni repère de progression n'est ajouté ici : ces éléments restent à vérifier auprès d'une source institutionnelle datée.

## Lire les niveaux de couverture

- **Appui transversal** : une compétence ou une règle commune aide à concevoir un support, sans exemple disciplinaire spécifique.
- **Exemple contextualisé** : un parcours fictif documente un objectif invariant, des obstacles, des options CUA, une source et une sortie courte pour un contexte donné.
- **Couverture validée** : un parcours contextualisé a été revu par une personne compétente sur le niveau et la discipline, avec une source datée et une décision consignée. **Aucune cellule n'atteint encore ce niveau dans le pilote.**

Les douze parcours fictifs sont conservés dans `tests/fixtures/parcours-pedagogiques-fictifs.json` et résumés dans `references/parcours-pedagogiques-fictifs.md`. Ils permettent de vérifier l'objectif invariant, les obstacles, les trois entrées CUA, la source documentée, l'absence de donnée personnelle et le support imprimable ; ce ne sont pas des séquences prêtes à prescrire.

## Prioriser les prochaines contributions

1. Partir des retours anonymes triés selon `references/triage-feedbacks-enseignants.md` : confidentialité et CUA passent avant toute autre demande.
2. Relever les zones sans exemple contextualisé, puis rechercher l'impact pédagogique, la fréquence anonymisée et la faisabilité.
3. Préparer un parcours fictif avec objectif invariant, obstacles, options CUA, source datée et résultat attendu court.
4. Demander une revue humaine disciplinaire avant de passer une cellule à « Couverture validée » ; lier la décision à une issue et au journal de version.

La matrice est maintenue à chaque ajout ou retrait de parcours. Ne jamais y ajouter de nom d'élève, de classe identifiable, de capture ou de ressource copiée sans droit.
