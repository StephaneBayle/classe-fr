# Parcours pédagogiques fictifs de contrôle

Ces douze cas sont des données de test entièrement fictives. Ils vérifient que Classe FR garde le même objectif d'apprentissage tout en proposant les trois entrées CUA, une source publique documentée et un support imprimable. Ils ne représentent ni une classe réelle ni une promesse d'adaptation universelle, et ne valent en aucun cas séquence à prescrire.

Chaque parcours se rattache à une famille de `references/profils-disciplinaires.md`. Les dix familles ont désormais au moins un parcours ; cela leur donne le statut « Exemple contextualisé » dans `references/matrice-couverture-discipline-niveau.md`, jamais celui de couverture validée.

## Premier lot, par niveau

| Contexte | Famille | Parcours contrôlé | Résultat court attendu |
| --- | --- | --- | --- |
| PS | `maternelle` | Ordonner les étapes d'un récit entendu | L'ordre est montré ou raconté à partir d'images. |
| CP | `francais` | Repérer une information explicitement écrite | La même information est pointée ou entourée. |
| CM1 / 6e | `mathematiques` | Comparer deux fractions simples | Le raisonnement utilise dessin et écriture fractionnaire. |
| Collège | `sciences-svt-physique-chimie` | Interpréter une variation dans un graphique | La tendance ne dépend pas de la seule couleur. |
| Lycée général ou technologique | `sciences-svt-physique-chimie` | Justifier une démarche de résolution | La rédaction reste évaluée quand elle est l'objectif annoncé. |
| Lycée professionnel ou CFA | `voie-professionnelle-cfa` | Ordonner une procédure professionnelle fictive | La procédure est expliquée ou mise en ordre. |

## Second lot, par famille disciplinaire

| Contexte | Famille | Parcours contrôlé | Résultat court attendu |
| --- | --- | --- | --- |
| 4e | `histoire-geographie-emc` | Mettre en relation deux documents fictifs | La mise en relation passe par un tableau ou par l'oral. |
| CM2 | `langues-vivantes` | Comprendre un document audio court | L'activité langagière évaluée reste la compréhension orale. |
| 4e | `technologie-numerique` | Expliciter une démarche de modification technique | La démarche est explicitée, avec un repli sans équipement. |
| CM2 | `arts-plastiques-education-musicale` | Expliciter deux choix plastiques | Les choix sont légendés ou expliqués oralement. |
| 6e | `arts-plastiques-education-musicale` | Repérer un contraste sonore | Le contraste est montré sur une frise ou nommé à l'oral. |
| 2de | `eps` | Réaliser une performance motrice et l'analyser | La réalisation motrice reste évaluée, sans substitution écrite. |

Le fichier `tests/fixtures/parcours-pedagogiques-fictifs.json` est le jeu de données contrôlé. Exécuter `python3 plugins/classe-fr/scripts/validate_parcours_fictifs.py .` pour le relire automatiquement. Le validateur exige pour chaque cas un objectif invariant, des obstacles, les trois entrées CUA, une source datée, un support imprimable, une famille disciplinaire connue et l'absence de donnée personnelle ; il refuse aussi qu'une modalité explicitement évaluée soit remplacée par une expression non équivalente. En cas de non-conformité, le message indique le contexte et le champ à corriger.
