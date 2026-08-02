# Triage des feedbacks enseignants

Les retours envoyés par le formulaire public sont visibles : ils ne doivent jamais contenir de donnée d'élève, capture d'ENT, message familial ou pièce jointe identifiable. Le triage ne recopie pas le contenu d'un retour de confidentialité ; il en conserve seulement le type, la décision et le lien vers le suivi.

## Cadence et priorité

Revoir les nouveaux retours tous les quinze jours pendant le pilote ; traiter sans attendre un retour étiqueté `confidentialite` ou `cua-accessibilite` à fort impact.

Évaluer chaque retour avec cinq critères, sans automatiser la décision :

| Critère | Question de triage |
| --- | --- |
| Impact pédagogique | L'obstacle empêche-t-il un usage enseignant utile ? |
| Accessibilité / CUA | Le retour signale-t-il une barrière de conception commune ? |
| Confidentialité | Existe-t-il un risque de diffusion ou d'usage de donnée identifiable ? |
| Fréquence | Le besoin apparaît-il dans plusieurs retours anonymes ? |
| Faisabilité | Une amélioration vérifiable est-elle réaliste dans le pilote ? |

La confidentialité passe avant le score. Pour les autres retours, documenter le raisonnement plutôt qu'additionner mécaniquement les critères.

## Labels et états de décision

Conserver `feedback-enseignant` sur le retour initial ; ajouter le label de nature correspondant : `bug`, `idee`, `ressource`, `besoin-pedagogique`, `cua-accessibilite` ou `confidentialite`. Les labels `cua-accessibilite` et `confidentialite` signalent une revue renforcée, mais ne publient aucun détail sensible.

Utiliser un commentaire de triage court et non identifiable pour rendre l'état visible : **reçu**, **à instruire**, **planifié**, **livré** ou **non retenu**. Une décision « non retenu » donne une justification courte et respectueuse ; elle ne promet ni réponse individuelle ni délai garanti.

## Suivi jusqu'à la décision

1. Vérifier la confirmation de confidentialité ; retirer ou faire reformuler tout détail sensible avant analyse.
2. Qualifier le retour avec les labels, l'impact et le statut **reçu**.
3. Passer à **à instruire**, noter la décision de priorité sans reproduire le contenu du retour.
4. Si le travail est retenu, créer ou lier une issue de réalisation et passer à **planifié** ; sinon passer à **non retenu** avec une raison courte.
5. Après livraison et validation, passer à **livré**, lier l'issue réalisée et résumer la décision dans `CHANGELOG.md`.

Le jeu de trois retours anonymes `tests/fixtures/triage-feedbacks-fictifs.json` suit ce parcours de bout en bout, dont un cas CUA/accessibilité. Il est contrôlé par `python3 plugins/classe-fr/scripts/validate_triage_feedback.py .`.
