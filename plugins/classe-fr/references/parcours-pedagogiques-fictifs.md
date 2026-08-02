# Parcours pédagogiques fictifs de contrôle

Ces six cas sont des données de test entièrement fictives. Ils vérifient que Classe FR garde le même objectif d'apprentissage tout en proposant les trois entrées CUA, une source publique documentée et un support imprimable. Ils ne représentent ni une classe réelle ni une promesse d'adaptation universelle.

| Contexte | Parcours contrôlé | Résultat court attendu |
| --- | --- | --- |
| PS | Ordonner les étapes d'un récit entendu | L'ordre est montré ou raconté à partir d'images. |
| CP | Repérer une information explicitement écrite | La même information est pointée ou entourée. |
| CM1 / 6e | Comparer deux fractions simples | Le raisonnement utilise dessin et écriture fractionnaire. |
| Collège | Interpréter une variation dans un graphique | La tendance ne dépend pas de la seule couleur. |
| Lycée général ou technologique | Justifier une démarche de résolution | La rédaction reste évaluée quand elle est l'objectif annoncé. |
| Lycée professionnel ou CFA | Ordonner une procédure professionnelle fictive | La procédure est expliquée ou mise en ordre. |

Le fichier `tests/fixtures/parcours-pedagogiques-fictifs.json` est le jeu de données contrôlé. Exécuter `python3 plugins/classe-fr/scripts/validate_parcours_fictifs.py .` pour le relire automatiquement. En cas de non-conformité, le message indique le contexte et le champ à corriger ; aucun cas ne contient de donnée personnelle.
