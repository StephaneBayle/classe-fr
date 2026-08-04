# Classe FR

![Bureau de préparation Classe FR avec supports, ordinateur et parcours d'apprentissage illustrés.](plugins/classe-fr/assets/images/public/classe-fr-hero.png)

**Un assistant de préparation pédagogique pour les enseignants en France.**

Classe FR aide à préparer, adapter et relire le travail de classe, de la maternelle au CFA. Il sert à gagner en clarté avant la séance, à rendre les supports plus accessibles et à garder les bons réflexes de confidentialité. L'enseignant reste responsable de la décision pédagogique et relit chaque production avant usage.

[Voir la page publique](https://stephanebayle.github.io/classe-fr/) · [guide de démarrage](DEMARRER.md) · [cas d’usage complets](CAS-USAGE.md) · [niveau de confiance](CONFIANCE.md) · [Dernière release](https://github.com/StephaneBayle/classe-fr/releases/latest)

## Trois usages simples

| Préparer | Adapter | Relire en confiance |
| --- | --- | --- |
| Cadrer une année, construire une programmation, préparer une séance ou une évaluation. | Transformer une consigne, un support ou une activité avec les principes CUA. | Vérifier les sources, les droits, la confidentialité et les points à valider humainement. |

Classe FR travaille avec des exemples fictifs ou anonymisés. Il ne remplace ni les programmes, ni le travail d'équipe, ni votre connaissance de la classe.

## Démarrer vite

1. Ouvrez [DEMARRER.md](DEMARRER.md).
2. Copiez une demande prête à l'emploi.
3. Indiquez le niveau, la discipline, l'objectif et le format attendu.
4. Relisez la proposition avant usage.

Exemple :

```text
Prépare une séance de 45 minutes en CM1 sur la comparaison de fractions simples.
Je veux un objectif clair, un déroulé, une trace écrite courte, une version imprimable
et des options CUA. Les exemples doivent rester fictifs.
```

## Installer

### Codex / ChatGPT Work

1. Ouvrez **Plugins**, puis **Ajouter une marketplace**.
2. Renseignez `StephaneBayle/classe-fr` dans **Source** et `main` dans **Réf. Git**.
3. Recherchez **Classe FR**, installez-le, puis ouvrez une nouvelle conversation.

### Utiliser avec Claude Code ou Cowork

1. Dans Claude, ouvrez **Personnaliser**, puis **Plugins**.
2. Choisissez **Ajouter depuis un dépôt**.
3. Renseignez `StephaneBayle/classe-fr` ou `https://github.com/StephaneBayle/classe-fr.git`.
4. Activez **Classe FR**, puis ouvrez une nouvelle conversation.

Le dépôt fournit aussi `CLAUDE.md`, `.claude/agents/classe-fr-pedagogie.md` et `plugins/classe-fr/agents/classe-fr-pedagogie.md` pour les usages Claude Code / Cowork depuis les fichiers source.

## Choisir une compétence

Vous pouvez décrire votre besoin en langage courant ou appeler directement une compétence avec `$nom-de-competence`.

| Compétence | Usage principal |
| --- | --- |
| `$cadrage-annee-scolaire` | démarrer une année, une prise de poste ou une nouvelle classe |
| `$bibliotheque-pedagogique` | organiser des ressources avec provenance, droits et objectifs |
| `$style-et-design-prof` | harmoniser supports, consignes et messages à partir d'exemples anonymisés |
| `$programmation-annuelle` | répartir les apprentissages par périodes avec sources datées |
| `$preparation-differenciation` | préparer une séance, une séquence ou un support accessible |
| `$cua-accessibilite-pedagogique` | auditer ou transformer un support selon la CUA |
| `$evaluation-retours` | créer une grille ou un retour pédagogique anonymisé |
| `$communication-familles` | rédiger un message collectif clair et non nominatif |
| `$bilan-de-periode` | faire le point après une période ou une séquence |
| `$feedback-au-createur` | formuler un retour public sans donnée personnelle |

## Confidentialité

Le dépôt est public. Le formulaire de retour est public : tout message ou document joint peut être visible. **Ne publiez jamais** de copie d'élève, évaluation nominative, message aux familles, capture d'ENT, nom, adresse, donnée médicale ou donnée de handicap.

L'espace professeur local est ignoré par Git. Pour le créer :

```bash
python3 plugins/classe-fr/scripts/init_teacher_space.py teacher-space
```

## Contribuer

Classe FR est un pilote public en version `0.2.0`. Les ressources institutionnelles et de pairs sont référencées avec source, date de consultation et licence. Le plugin ne recopie pas de contenus protégés sans autorisation.

Pour contribuer, consultez [AGENTS.md](AGENTS.md), ouvrez ou liez une [issue](https://github.com/StephaneBayle/classe-fr/issues), puis lancez :

```bash
python3 plugins/classe-fr/scripts/validate_classe_fr.py .
python3 -m unittest discover -s tests -v
```

## Licence

Classe FR est publié comme **source disponible propriétaire**. Le dépôt peut être consulté publiquement pour comprendre, installer et auditer le plugin depuis sa source officielle, mais il n'accorde pas de droit de copie, modification, redistribution ou réutilisation en dehors d'un accord écrit préalable.

Consultez [LICENSE](LICENSE) pour les conditions complètes. Le manifeste conserve la valeur `UNLICENSED` afin de rendre explicite qu'il ne s'agit pas d'un projet open source.

## Métadonnées GitHub recommandées

Description courte : `Assistant pédagogique inclusif pour enseignants en France.`

Topics recommandés : `education`, `enseignement`, `france`, `enseignants`, `accessibility`, `cua`, `pedagogy`, `chatgpt`, `codex`, `plugin`.
