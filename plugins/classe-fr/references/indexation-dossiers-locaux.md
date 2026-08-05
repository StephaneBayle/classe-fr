# Indexer un dossier de ressources local

Un enseignant a souvent plusieurs années de travail sur sa machine. Classe FR peut rendre ces ressources retrouvables par niveau, discipline et objectif, sans les déplacer et sans les copier. Cette référence fixe les règles ; le parcours est décrit dans `skills/bibliotheque-pedagogique/SKILL.md`.

## Le risque, avant tout le reste

Le disque d'un enseignant contient aussi des copies scannées, des listes de classe, des bulletins, des documents de suivi individuel et des échanges avec des familles. Indexer sans précaution ferait entrer dans Classe FR exactement ce que le plugin refuse partout ailleurs.

Le danger n'est pas seulement dans les contenus : **un nom de fichier est lui-même une donnée personnelle.** `PAP_Lucas_CM1.pdf` ou `notes_3eB_martin.xlsx` nomment un élève. Un index qui les enregistrerait serait un fichier de données personnelles rangé dans l'espace professeur.

## Cinq règles non négociables

- **Métadonnées seulement.** Aucun fichier n'est ouvert, lu ni analysé. Seul le nom sert, et uniquement pour proposer un titre et repérer un signal.
- **Indexation par référence.** La ressource reste où elle est. L'index ne garde qu'un emplacement relatif au dossier examiné, jamais une copie.
- **Crible avant indexation.** Les séparateurs des noms de fichiers — point, tiret, souligné — sont normalisés en espaces avant application des motifs, sinon `PAP_Lucas_CM1` échappe à la détection de nom propre. Un fichier signalé n'est pas indexé, et **son nom n'est jamais affiché** : il est rapporté par sa position dans le listing.
- **Un dossier, pas le disque.** Le balayage porte sur un dossier désigné et ses sous-dossiers immédiats. Au-delà de deux cents fichiers, le script refuse et demande de resserrer — une année, une séquence.
- **Ne rien deviner.** Niveau, discipline et objectif restent « à compléter » : un nom de fichier ne les établit pas. La licence reste « à vérifier », ces dossiers contenant du manuel scanné, du travail de collègues et des ressources trouvées en ligne.

## Ce que le crible signale

Adresse e-mail, numéro de téléphone, nom complet possible, sigle de dossier de suivi individuel, et vocabulaire de document individuel — bulletin, copie, notes, livret, trombinoscope, absences, signalement.

Le crible est volontairement large : mieux vaut écarter un fichier anodin que d'indexer une liste d'élèves. Il **signale, il ne certifie pas** : la relecture de l'enseignant reste nécessaire, comme pour `scripts/precontrole_anonymisation.py`.

## Ce que le crible ne voit pas

Une limite doit être connue plutôt que masquée : **un prénom seul dans un nom de fichier n'est pas détecté.** `Lucas-progres.odt` passe le crible, parce qu'un prénom isolé ne se distingue pas d'un mot ordinaire sans recourir à une liste de prénoms — laquelle produirait des faux positifs en cascade et dépendrait de la langue.

Sont donc repérés les couples prénom-nom, les sigles de dossier de suivi et le vocabulaire de document individuel, mais pas un prénom isolé. L'enseignant doit **relire la liste** des fiches proposées avant de les intégrer, et retirer ce que le crible a laissé passer.

## Rien n'entre sans validation

Le script propose des fiches ; il n'écrit pas dans `bibliotheque/index.yml`. L'enseignant relit, complète niveau, discipline et objectif, tranche la licence, puis décide de l'intégration. C'est la règle appliquée par `bilan-de-periode` avant toute mise à jour.

## Contrôle automatique

```bash
python3 plugins/classe-fr/scripts/indexer_dossier_ressources.py <dossier> --fiches
```

Le rapport indique le nombre de fichiers examinés, de fiches proposées et de fichiers écartés, avec pour chaque écart sa position et la catégorie repérée — jamais son nom.
