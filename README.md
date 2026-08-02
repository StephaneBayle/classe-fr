# Classe FR

**Préparer, adapter et relire son enseignement, de la petite section au CFA.**

Classe FR est un plugin Codex pensé pour les enseignants exerçant en France. Il aide à préparer le travail de l’année, à organiser ses ressources, à créer des supports plus accessibles et à formuler des communications professionnelles. C’est un copilote de préparation : l’enseignant garde toujours la décision pédagogique et relit chaque production avant de l’utiliser.

## Ce que Classe FR peut vous aider à faire

- cadrer une année, une prise de poste ou une nouvelle classe ;
- construire une programmation par périodes à partir de sources datées ;
- préparer une séance, une séquence, un support ou une évaluation ;
- organiser votre propre bibliothèque de ressources et préciser leurs droits d’usage ;
- harmoniser vos documents et vos messages aux familles à partir de textes professionnels anonymisés ;
- faire un bilan de période et préparer un retour d’expérience pour le créateur.

Les compétences sont utilisables de la PS à la terminale, en lycée professionnel et en CFA. Elles proposent des repères adaptés au niveau, mais ne remplacent ni les programmes, ni le travail d’équipe, ni votre connaissance de la classe.

## Commencer simplement

1. Installez le plugin dans Codex depuis cette marketplace, puis créez votre espace professeur local :

   ```bash
   python3 plugins/classe-fr/scripts/init_teacher_space.py teacher-space
   ```

2. Commencez par demander à Codex : « Je prépare une année de CP. Aide-moi à la cadrer avec `$cadrage-annee-scolaire`. »

3. Ajoutez progressivement vos ressources dans votre bibliothèque, puis utilisez par exemple :

   - `$programmation-annuelle` pour répartir les apprentissages ;
   - `$preparation-differenciation` pour concevoir une séance ;
   - `$evaluation-retours` pour expliciter les critères et les retours.

Vous pouvez aussi demander une réponse en langage courant : les noms des compétences ne sont là que pour raccourcir le chemin.

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
