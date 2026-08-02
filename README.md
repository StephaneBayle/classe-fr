# Classe FR

**Préparer, adapter et relire son enseignement, de la maternelle au CFA : à l’école, au collège, au lycée et en apprentissage.**

Classe FR est un plugin Codex pensé pour les enseignants exerçant en France. Il aide à préparer le travail de l’année, à organiser ses ressources, à créer des supports plus accessibles et à formuler des communications professionnelles. C’est un copilote de préparation : l’enseignant garde toujours la décision pédagogique et relit chaque production avant de l’utiliser.

## Ce que Classe FR peut vous aider à faire

- cadrer une année, une prise de poste ou une nouvelle classe ;
- construire une programmation par périodes à partir de sources datées ;
- préparer une séance, une séquence, un support ou une évaluation ;
- organiser votre propre bibliothèque de ressources et préciser leurs droits d’usage ;
- harmoniser vos documents et vos messages aux familles à partir de textes professionnels anonymisés ;
- faire un bilan de période et préparer un retour d’expérience pour le créateur.

Les compétences s’adressent aux enseignants de maternelle, d’élémentaire, de collège, de lycée général, technologique ou professionnel, ainsi que de CFA. Elles proposent des repères adaptés au niveau, mais ne remplacent ni les programmes, ni le travail d’équipe, ni votre connaissance de la classe.

## Installer dans Codex ou ChatGPT

L’installation par l’interface est recommandée : elle ne demande ni terminal ni compte GitHub particulier.

1. Dans Codex ou ChatGPT Work, ouvrez **Plugins**, puis choisissez **Ajouter une marketplace**.
2. Renseignez `StephaneBayle/classe-fr` dans **Source** et `main` dans **Réf. Git**. Laissez **Chemins partiels** vide.
3. Cliquez sur **Ajouter une marketplace**, recherchez **Classe FR**, puis choisissez **Installer**.
4. Ouvrez une **nouvelle conversation** : les compétences du plugin sont alors disponibles.

Le dépôt étant public, tous les enseignants peuvent suivre ce parcours. Ils n’ont pas besoin d’être invités comme collaborateurs GitHub.

## Préparer sa première séance

Dans la nouvelle conversation, décrivez simplement votre contexte. Par exemple :

> J’enseigne les mathématiques en 5e. Aide-moi à préparer une séance sur les fractions, avec un objectif précis et des options accessibles à tous les élèves.

Codex choisira les compétences utiles. Vous pouvez aussi les appeler directement :

- `$cadrage-annee-scolaire` pour démarrer une année ou une nouvelle classe ;
- `$programmation-annuelle` pour répartir les apprentissages ;
- `$preparation-differenciation` pour concevoir une séance ;
- `$evaluation-retours` pour expliciter les critères et les retours.

Pour organiser vos ressources et vos productions, demandez à Codex de créer un espace professeur local dans votre dossier de travail. Les personnes qui préfèrent le faire elles-mêmes peuvent exécuter :

```bash
python3 plugins/classe-fr/scripts/init_teacher_space.py teacher-space
```

## Une accessibilité pensée dès le départ

Classe FR applique la **conception universelle de l’apprentissage (CUA)**. Chaque proposition commence par ce qui doit être appris, puis anticipe les obstacles possibles. Elle propose, quand c’est pertinent, plusieurs façons équivalentes de s’engager, d’accéder au contenu et de montrer ce qui a été compris.

Concrètement, cela peut associer une consigne orale et visuelle, une manipulation, un exemple guidé, du vocabulaire explicité, un temps d’anticipation ou plusieurs formes de restitution. L’objectif ne change pas. La CUA ne remplace pas les adaptations individualisées ni les décisions de l’équipe éducative.

## Vos données restent sous votre contrôle

L’espace professeur est local et ignoré par Git. **N’ajoutez jamais** de copie d’élève, évaluation nominative, message aux familles, capture d’ENT, nom, adresse, donnée médicale ou donnée de handicap. Anonymisez vos exemples professionnels avant de les utiliser. Relisez toujours un support avant diffusion.

Le dépôt est public : toute issue, commentaire ou pièce jointe est potentiellement visible. Pour proposer une amélioration, utilisez [$feedback-au-createur](https://github.com/StephaneBayle/classe-fr/issues/new?template=teacher-feedback.yml) uniquement avec un contexte pédagogique non identifiable.

## Ressources et contributions

Les ressources institutionnelles et de pairs sont référencées avec leur source, leur date de consultation et leur licence. Classe FR ne recopie pas les contenus protégés sans autorisation.

Ce projet est un pilote public en version `0.1.0`. Les améliorations attendues sont suivies dans les [issues](https://github.com/StephaneBayle/classe-fr/issues). Pour contribuer au dépôt, consultez [le guide de contribution](AGENTS.md), lancez les validations indiquées et liez votre proposition à une issue.

La licence est actuellement `UNLICENSED` : la consultation publique du dépôt n’accorde pas de droit de réutilisation ou de redistribution.
