# Connecteurs publics institutionnels

Cette référence cadre les connecteurs envisagés pour enrichir Classe FR avec des ressources publiques, sans données d'élèves et sans accès à des espaces privés. Elle décrit une première version en lecture seule ; toute authentification future doit rester optionnelle, explicite et séparée du mode public.

## Sources ciblées

### data.education.gouv.fr

Utiliser `data.education.gouv.fr` pour rechercher des jeux de données publics du ministère, par exemple : calendrier scolaire, annuaire de l'éducation, programmes ou référentiels publiés, dispositifs d'inclusion, éducation prioritaire, évaluations nationales agrégées, usages numériques agrégés, orientation, diplômes et insertion.

Le connecteur attendu peut rechercher un jeu de données par thème, niveau, discipline ou mot-clé, lire ses métadonnées et récupérer un petit nombre d'enregistrements publics filtrés. Il ne sert pas à produire un diagnostic individuel d'établissement, de classe ou d'élève.

### Forge des communs numériques éducatifs

Utiliser la Forge publique `forge.apps.education.fr` pour repérer des ressources pédagogiques libres : projets publics, mini-sites, manuels, exercices, supports Markdown, README, documentation, licences, tags, descriptions et dates d'activité.

Le connecteur attendu peut rechercher des projets publics par mot-clé, discipline, niveau ou type de ressource, lire les métadonnées publiques et consulter les README ou fichiers de documentation publics. Il ne doit pas accéder à des projets privés, créer une issue, commenter, modifier un fichier ou ouvrir une merge request sans demande explicite séparée.

## Distinction des espaces

- `donnée publique` : information ouverte, publiée par une institution ou un opérateur public ; citer source, URL, date de consultation, date de mise à jour visible et licence lorsque disponible.
- `ressource publique` : contenu pédagogique ou documentation accessible publiquement ; citer projet, auteur ou organisme, URL, date de consultation, licence et statut de réutilisation.
- `espace authentifié` : ENT, messagerie, Nuage personnel, dépôt privé, espace classe, projet Forge privé ou outil qui expose des données non publiques ; ne pas y accéder dans cette version.

## Citation obligatoire

Chaque réponse qui exploite une donnée ou une ressource issue de ces connecteurs doit inclure :

- source ou projet ;
- URL ;
- date de consultation ;
- date de mise à jour ou d'activité si elle est fournie ;
- licence ou mention `licence absente ou à vérifier` ;
- limite d'interprétation lorsque la donnée est statistique, ancienne, agrégée, filtrée ou incomplète.

Formulation courte possible :

> Source : data.education.gouv.fr, jeu de données `[titre]`, URL, consulté le `[date]`, mise à jour visible le `[date]`, licence `[licence]`. Donnée publique agrégée : ne pas l'interpréter comme un diagnostic individuel.

> Source : Forge des communs numériques éducatifs, projet `[nom]`, URL, consulté le `[date]`, activité visible le `[date]`, licence `[licence ou à vérifier]`. Réutilisation à confirmer avant copie ou adaptation.

## Garde-fous

- Rester en lecture seule par défaut.
- Ne pas aspirer un jeu de données complet lorsqu'un extrait filtré suffit à répondre.
- Ne jamais traiter de donnée d'élève identifiable, de capture d'ENT, de message aux familles, de document nominatif ou de donnée de santé.
- Ne pas présenter des indicateurs agrégés comme une vérité locale sur une classe, un élève ou une équipe.
- Ne pas recommander une ressource dont la licence ou le statut de réutilisation est absent sans le signaler explicitement.
- Conserver les décisions pédagogiques sous validation humaine : une source publique éclaire le travail, elle ne remplace pas le jugement de l'enseignant.
