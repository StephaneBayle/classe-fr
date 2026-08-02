# Classe FR

![Bannière illustrative de Classe FR : des chemins d’apprentissage reliant école, collège, lycée et apprentissage.](plugins/classe-fr/assets/images/banner-classe-fr.png)

**Préparer, adapter et améliorer son travail pédagogique, de la maternelle au CFA : à l’école, au collège, au lycée et en apprentissage.**

Classe FR est un plugin pour Codex/ChatGPT Work pensé pour les enseignants exerçant en France. Il aide à préparer le travail de l’année, à organiser ses ressources, à créer des supports plus accessibles et à formuler des communications professionnelles. C’est un copilote de préparation : l’enseignant garde toujours la décision pédagogique et relit chaque production avant de l’utiliser.

## Ce que Classe FR peut vous aider à faire

- cadrer une année, une prise de poste ou une nouvelle classe ;
- construire une programmation par périodes à partir de sources datées ;
- préparer une séance, une séquence, un support ou une évaluation ;
- organiser votre propre bibliothèque de ressources et préciser leurs droits d’usage ;
- harmoniser vos documents et vos messages aux familles à partir de textes professionnels anonymisés ;
- faire un bilan de période et préparer un retour d’expérience pour le créateur.

Les compétences s’adressent aux enseignants de maternelle, d’élémentaire, de collège, de lycée général, technologique ou professionnel, ainsi que de CFA. Elles proposent des repères adaptés au niveau, mais ne remplacent ni les programmes, ni le travail d’équipe, ni votre connaissance de la classe.

## Installer dans Codex/ChatGPT Work

L’installation par l’interface est recommandée : elle ne demande ni terminal ni compte GitHub particulier.

1. Dans Codex/ChatGPT Work, ouvrez **Plugins**, puis choisissez **Ajouter une marketplace**.
2. Renseignez `StephaneBayle/classe-fr` dans **Source** et `main` dans **Réf. Git**. Laissez **Chemins partiels** vide.
3. Cliquez sur **Ajouter une marketplace**, recherchez **Classe FR**, puis choisissez **Installer**.
4. Ouvrez une **nouvelle conversation** : les compétences du plugin sont alors disponibles.

Le dépôt étant public, tous les enseignants peuvent suivre ce parcours. Ils n’ont pas besoin d’être invités comme collaborateurs GitHub.

## Utiliser avec Claude Code ou Cowork

Classe FR reste structuré comme plugin OpenAI, mais il peut aussi être ajouté dans Claude depuis le menu de personnalisation des plugins.

1. Dans Claude, ouvrez **Personnaliser**, puis **Plugins**.
2. Cliquez sur **Ajouter**, puis choisissez **Ajouter une place de marché**.
3. Sélectionnez **Ajouter depuis un dépôt**.
4. Renseignez le dépôt `StephaneBayle/classe-fr`, ou l’URL Git `https://github.com/StephaneBayle/classe-fr.git`, puis synchronisez la marketplace.
5. Recherchez **Classe FR**, activez le plugin, puis ouvrez une nouvelle conversation.

Le dépôt fournit aussi trois entrées compatibles avec Claude Code/Cowork pour les personnes qui travaillent directement depuis les fichiers source.

- `CLAUDE.md` donne les règles du projet quand vous ouvrez ce dépôt dans Claude Code ou Cowork.
- `.claude/agents/classe-fr-pedagogie.md` permet à Claude Code de découvrir automatiquement l’agent quand le dépôt est ouvert comme projet.
- `plugins/classe-fr/agents/classe-fr-pedagogie.md` fournit un agent Claude portable qui reprend les garde-fous du plugin : confidentialité, objectif invariant, CUA, sources datées et responsabilité de validation par l’enseignant.

Dans Claude Code ou Cowork, demandez par exemple : « Utilise l’agent `classe-fr-pedagogie` pour préparer une séance inclusive de CM1 sur les fractions. » L’agent lit les compétences dans `plugins/classe-fr/skills/` et les références utiles avant de produire un livrable. Le plugin ne transmet aucune donnée : vous devez continuer à travailler uniquement avec des exemples fictifs ou anonymisés.

## Choisir et déclencher une compétence

Vous pouvez décrire votre besoin avec vos mots : l’assistant sélectionnera la compétence pertinente. Pour la choisir vous-même, écrivez son nom précédé de `$` dans Codex, par exemple `$preparation-differenciation`. Dans ChatGPT Work, tapez `@`, puis choisissez **Classe FR** ou la compétence proposée.

Commencez toujours par indiquer le niveau, la discipline ou le domaine, et ce que vous souhaitez obtenir. Voici les dix compétences et des demandes prêtes à copier.

| Compétence | À utiliser quand… | Demande prête à copier |
| --- | --- | --- |
| `$cadrage-annee-scolaire` | vous démarrez une année, une nouvelle classe ou une prise de poste | « Je prends une classe de CE2. Aide-moi à cadrer mon année, avec mes priorités et les grandes étapes. » |
| `$bibliotheque-pedagogique` | vous voulez classer et retrouver vos propres ressources | « Aide-moi à organiser mes ressources de français 6e par objectif, niveau, source et droit d’usage. » |
| `$style-et-design-prof` | vous voulez harmoniser vos supports, évaluations et messages | « À partir de ces textes professionnels anonymisés, aide-moi à définir mon style d’écriture et mes règles de mise en page accessibles. » |
| `$programmation-annuelle` | vous répartissez les apprentissages sur l’année ou les périodes | « Construis une programmation annuelle de mathématiques pour une 5e, à partir des repères que je fournis et des sources à vérifier. » |
| `$preparation-differenciation` | vous préparez une séquence, une séance ou un support | « Prépare une séance de SVT en seconde sur la biodiversité : objectif clair, déroulé, supports et plusieurs accès au contenu. » |
| `$cua-accessibilite-pedagogique` | vous voulez rendre une séance, un support ou une évaluation plus accessible | « Audite cette évaluation de lecture en CM2 selon la CUA, sans changer ce qui est réellement évalué. » |
| `$evaluation-retours` | vous créez une évaluation, une grille ou un retour aux élèves | « Conçois une grille d’évaluation pour un oral de CAP, avec critères explicites et modalités d’expression adaptées. » |
| `$communication-familles` | vous rédigez un message collectif ou une information pratique | « Rédige un message clair aux familles de 4e sur la sortie scolaire, sans mentionner d’élève en particulier. » |
| `$bilan-de-periode` | vous faites le point après une période, une séquence ou avant une réunion | « Aide-moi à faire le bilan de ma période en maternelle : acquis observés, ajustements à envisager et prochaines priorités. » |
| `$feedback-au-createur` | vous souhaitez signaler un bug, une idée ou un besoin pour faire évoluer Classe FR | « Aide-moi à formuler un retour sur Classe FR concernant l’accessibilité, sans aucune donnée personnelle ni document identifiable. » |

Pour organiser vos ressources et vos productions, demandez à l’assistant de créer un espace professeur local dans votre dossier de travail. Les personnes qui préfèrent le faire elles-mêmes peuvent exécuter :

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

## Licence

Classe FR est publié comme **source disponible propriétaire**. Le dépôt peut être consulté publiquement pour comprendre, installer et auditer le plugin depuis sa source officielle, mais il n'accorde pas de droit de copie, modification, redistribution ou réutilisation en dehors d'un accord écrit préalable.

Consultez [LICENSE](LICENSE) pour les conditions complètes. Le manifeste du plugin conserve la valeur `UNLICENSED` afin de rendre explicite qu'il ne s'agit pas d'un projet open source.

## Métadonnées GitHub recommandées

Description courte : `Assistant pédagogique inclusif pour enseignants en France.`

Topics recommandés : `education`, `enseignement`, `france`, `enseignants`, `accessibility`, `cua`, `pedagogy`, `chatgpt`, `codex`, `plugin`.
