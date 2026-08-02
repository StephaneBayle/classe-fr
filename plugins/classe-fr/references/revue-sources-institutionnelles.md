# Revue versionnée des sources institutionnelles

Le registre `registre-sources-institutionnelles.json` contient une entrée par source citée dans le plugin : source, URL, niveaux ou cycles, disciplines, dates de consultation et de dernière revue, statut, rôle de validation, prochaine revue, décision liée et note de constat. Les sources de pairs restent des liens avec leur licence ; elles ne sont ni copiées ni aspirées.

## Cadence et déroulé

Réviser le registre au moins tous les trois mois, avant une publication importante et dès qu'un changement est signalé.

1. Ouvrir la source publique, relever seulement l'URL, le titre, la date visible et les évolutions pertinentes.
2. Choisir un statut : **changement constaté**, **à analyser** ou **aucun changement pertinent**.
3. Produire `assets/modeles/rapport-revue-sources.md` et relier chaque décision à une issue ou à une note de version.
4. En cas de changement, ne pas modifier silencieusement une recommandation : créer ou lier une issue, analyser l'impact pédagogique, puis faire valider la décision humaine.
5. Consigner la décision livrée dans le journal de version sans reproduire le contenu de la source.

Le jeu `tests/fixtures/registre-revue-sources-fictif.json` vérifie les trois statuts sur des sources publiques fictives. Lancer `python3 plugins/classe-fr/scripts/validate_registre_sources.py .` pour valider le registre réel ; les tests automatisés vérifient aussi le jeu fictif et le rapport généré.
