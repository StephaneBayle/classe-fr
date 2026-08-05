---
name: bibliotheque-pedagogique
description: Indexer et réemployer une bibliothèque locale de ressources pédagogiques avec provenance, droits, niveau, objectif et apports CUA. Utiliser pour classer des ressources possédées, institutionnelles ou produites par des pairs.
---

# Bibliothèque pédagogique

Lire `references/sources-et-droits.md`, `references/connecteurs-publics-institutionnels.md`, `references/matrice-couverture-discipline-niveau.md` et `references/confidentialite.md` avant tout traitement. Pour un dossier de ressources déjà présent sur la machine, lire aussi `references/indexation-dossiers-locaux.md`.

1. Vérifier que le document ne contient aucune donnée identifiable ; ne jamais copier une ressource externe dans le dépôt.
2. Créer ou enrichir une entrée dans `bibliotheque/index.yml` à partir du modèle fourni.
3. Associer niveau, discipline, objectif, provenance, date de consultation, licence, emplacement et apports CUA réels.
4. Pour une ressource de pair, enregistrer un lien et les conditions de réutilisation ; demander une autorisation si elles sont absentes.
5. Pour une ressource publique trouvée via `data.education.gouv.fr` ou la Forge, rester en lecture seule et citer source, URL, date de consultation, date de mise à jour ou d'activité, licence et limite de réutilisation.
6. Proposer une fiche de réemploi : pour quel objectif, sous quelle forme, avec quelles alternatives de représentation ou d'expression.

## Indexer un dossier local existant

Quand l'enseignant veut rendre retrouvables des ressources déjà sur sa machine :

1. Demander **un** dossier — une année, une séquence — et non l'ensemble du disque.
2. Lancer `scripts/indexer_dossier_ressources.py` sur ce dossier. Ne jamais ouvrir, lire ni copier les fichiers soi-même.
3. Restituer le rapport tel quel : nombre de fichiers examinés, de fiches proposées, de fichiers écartés. Ne jamais nommer un fichier écarté ; sa position et la catégorie repérée suffisent.
4. Rappeler que le crible signale sans certifier : un prénom seul dans un nom de fichier n'est pas détecté, les fichiers écartés sont à relire, et un fichier retenu peut malgré tout contenir une donnée personnelle. Faire relire la liste des fiches proposées avant toute intégration.
5. Compléter avec l'enseignant niveau, discipline et objectif, laissés « à compléter » ; trancher la licence, laissée « à vérifier ».
6. N'intégrer les fiches à `bibliotheque/index.yml` qu'après validation explicite.

Signaler lorsqu'une ressource ouvre une zone de la matrice encore « à construire » ; elle ne devient pas une couverture validée sans revue humaine, source datée et décision tracée.

Signaler clairement les métadonnées inconnues au lieu de les deviner. Produire un petit catalogue exploitable, pas une liste de liens brute.
