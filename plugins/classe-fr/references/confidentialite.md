# Confidentialité et usage professionnel

Avant d'utiliser une ressource, demander une confirmation explicite : « Ce contenu ne contient-il aucun nom, identifiant, résultat nominatif, élément familial, médical ou de vie privée ? »

- Refuser les copies d'élèves, évaluations nominatives, captures d'écran d'ENT et messages aux familles non anonymisés.
- Refuser l'accès à un ENT, une messagerie, un Nuage personnel, un dépôt privé ou un projet Forge privé dans le mode public en lecture seule.
- Ne conserver aucun document personnel dans le dépôt, les modèles ou les exemples de test.
- Ne pas demander de diagnostic, de dossier médical ou de donnée de handicap.
- Pour une évaluation ou un feedback, remplacer les personnes par des rôles neutres et supprimer les détails indirectement identifiants.
- L'enseignant relit toujours la production avant diffusion, envoi ou dépôt.

## Pré-contrôle local facultatif

Avant d'utiliser un fichier texte local (Markdown, texte brut, CSV, YAML, JSON ou HTML), l'enseignant peut lancer :

```bash
python3 plugins/classe-fr/scripts/precontrole_anonymisation.py chemin/vers/document.md
```

Le script repère des signaux usuels — adresse e-mail, numéro de téléphone, adresse postale, identifiant ou nom complet possible — et indique seulement les numéros de ligne à relire. Il ne transmet, ne copie, n'affiche ni n'enregistre le contenu analysé. Un avertissement impose de corriger ou d'anonymiser le document ; en l'absence de signal, `--confirme-relecture` reste nécessaire avant son usage.

Ce pré-contrôle local est facultatif et explicable. Il ne détecte pas toutes les données indirectement identifiantes, ne prouve jamais l'anonymisation et ne remplace pas le jugement de l'enseignant.

Référence CNIL : https://www.cnil.fr/fr/enseignant-usage-systeme-ia
