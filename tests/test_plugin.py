from __future__ import annotations

import importlib.util
import json
import re
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins" / "classe-fr" / "scripts" / "init_teacher_space.py"
VALIDATOR = ROOT / "plugins" / "classe-fr" / "scripts" / "validate_classe_fr.py"
PRECONTROL = ROOT / "plugins" / "classe-fr" / "scripts" / "precontrole_anonymisation.py"
PARCOURS_VALIDATOR = ROOT / "plugins" / "classe-fr" / "scripts" / "validate_parcours_fictifs.py"
PARCOURS_FIXTURE = ROOT / "tests" / "fixtures" / "parcours-pedagogiques-fictifs.json"
SOURCES_VALIDATOR = ROOT / "plugins" / "classe-fr" / "scripts" / "validate_registre_sources.py"
SOURCES_REGISTRY = ROOT / "plugins" / "classe-fr" / "references" / "registre-sources-institutionnelles.json"
SOURCES_FIXTURE = ROOT / "tests" / "fixtures" / "registre-revue-sources-fictif.json"
FEEDBACK_VALIDATOR = ROOT / "plugins" / "classe-fr" / "scripts" / "validate_triage_feedback.py"
FEEDBACK_FIXTURE = ROOT / "tests" / "fixtures" / "triage-feedbacks-fictifs.json"
PROFILES_VALIDATOR = ROOT / "plugins" / "classe-fr" / "scripts" / "validate_profils_disciplinaires.py"
PROFILES_FIXTURE = ROOT / "tests" / "fixtures" / "profils-disciplinaires-fictifs.json"
PROFILES_REFERENCE = ROOT / "plugins" / "classe-fr" / "references" / "profils-disciplinaires.md"
REVIEW_VALIDATOR = ROOT / "plugins" / "classe-fr" / "scripts" / "validate_revue_disciplinaire.py"
REVIEW_FIXTURE = ROOT / "tests" / "fixtures" / "revues-disciplinaires-fictives.json"
REVIEW_REFERENCE = ROOT / "plugins" / "classe-fr" / "references" / "revue-disciplinaire.md"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClasseFrTests(unittest.TestCase):
    def test_initialise_un_espace_professeur_sans_donnees(self):
        module = load_module(SCRIPT, "init_teacher_space")
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "espace-professeur"
            module.initialise(destination)
            self.assertTrue((destination / "profil" / "enseignant.yml").exists())
            self.assertTrue((destination / "bibliotheque" / "index.yml").exists())
            self.assertTrue((destination / "style" / "design-tokens.json").exists())
            self.assertTrue((destination / "feedbacks" / "feedback-modele.md").exists())
            self.assertIn("contenus professionnels anonymisés", (destination / "README.md").read_text(encoding="utf-8"))

    def test_accueil_produit_avant_de_proposer_un_espace(self):
        accueil = (
            ROOT / "plugins" / "classe-fr" / "skills" / "demarrer-avec-classe-fr" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for element in (
            "name: demarrer-avec-classe-fr",
            "Accueillir en produisant",
            "trois questions",
            "confidentialité",
            "premier livrable réel",
            "Ne jamais créer de fichier sans accord explicite",
            "Ne jamais demander de document",
            "validation humaine",
            "Aucune discipline n'est couverte comme validée",
            "DEMARRER.md",
            "CONFIANCE.md",
        ):
            self.assertIn(element, accueil, element)

        livrable = accueil.index("Produire un premier livrable réel")
        espace = accueil.index("Proposer l'espace professeur, puis le créer")
        self.assertLess(livrable, espace, "L'espace doit être proposé après le premier livrable.")

    def test_accueil_amorce_le_profil_sans_le_deviner(self):
        accueil = (
            ROOT / "plugins" / "classe-fr" / "skills" / "demarrer-avec-classe-fr" / "SKILL.md"
        ).read_text(encoding="utf-8")
        modele = (
            ROOT / "plugins" / "classe-fr" / "assets" / "modeles" / "profil-enseignant.yml"
        ).read_text(encoding="utf-8")

        for champ in (
            "niveaux",
            "disciplines",
            "priorites_annuelles",
            "contraintes",
            "contenus_anonymises_confirmes",
            "stockage_hors_depot_confirme",
        ):
            self.assertIn(champ, modele, champ)
            self.assertIn(champ, accueil, champ)
        self.assertIn("laisser « à compléter » ; ne pas les deviner", accueil)
        self.assertIn("seulement après que l'enseignant a confirmé", accueil)

    def test_accueil_annonce_l_indexation_sans_balayer(self):
        accueil = (
            ROOT / "plugins" / "classe-fr" / "skills" / "demarrer-avec-classe-fr" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("sans jamais les copier", accueil)
        self.assertIn("ne balayer aucun dossier pendant l'accueil", accueil)

    def test_agent_renvoie_le_premier_contact_vers_la_session_principale(self):
        agent = (
            ROOT / "plugins" / "classe-fr" / "agents" / "classe-fr-pedagogie.md"
        ).read_text(encoding="utf-8")

        self.assertIn("demarrer-avec-classe-fr", agent)
        self.assertIn("Tu es en lecture seule", agent)
        self.assertIn("session principale", agent)
        self.assertIn("ne tente pas la création toi-même", agent)

    def test_espace_professeur_est_repris_sans_ecraser_le_travail(self):
        module = load_module(SCRIPT, "init_teacher_space_reprise")
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "espace-professeur"
            premier = module.initialise(destination)

            profil = destination / "profil" / "enseignant.yml"
            profil.write_text("profil:\n  niveaux: [CAP]\n", encoding="utf-8")
            (destination / "bibliotheque" / "index.yml").unlink()

            second = module.initialise(destination)

            self.assertIn("profil/enseignant.yml", premier)
            self.assertEqual(second, ["bibliotheque/index.yml"])
            self.assertIn("CAP", profil.read_text(encoding="utf-8"))
            self.assertEqual(module.initialise(destination), [])

    def test_readme_met_l_accueil_en_avant_et_range_la_commande(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        depart = readme.index("## Démarrer vite")
        aller_plus_loin = readme.index("## Aller plus loin")
        commande = readme.index("init_teacher_space.py")

        self.assertIn("Je débute avec Classe FR", readme[depart:aller_plus_loin])
        self.assertGreater(commande, aller_plus_loin, "La commande doit rester hors du démarrage.")
        self.assertIn("jamais écrasé", readme)

    def test_validation_du_depot(self):
        module = load_module(VALIDATOR, "validate_classe_fr")
        self.assertEqual(module.validate(ROOT), [])

    def test_licence_et_documents_github_sont_coherents_avec_un_depot_public(self):
        licence = (ROOT / "LICENSE").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        labels_script = (
            ROOT / "plugins" / "classe-fr" / "scripts" / "create_github_labels.sh"
        ).read_text(encoding="utf-8")

        self.assertIn("source disponible propriétaire", licence)
        self.assertNotIn("confidentiel", licence.lower())
        self.assertIn("Description courte", readme)
        self.assertIn("Topics recommandés", readme)
        self.assertIn("Utiliser avec Claude Code ou Cowork", readme)
        self.assertIn("guide de démarrage", readme)
        self.assertIn("cas d’usage complets", readme)
        self.assertIn("niveau de confiance", readme)
        self.assertIn("maintenance", labels_script)
        for relative_path in (
            "CONTRIBUTING.md",
            "SECURITY.md",
            ".github/CODEOWNERS",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/dependabot.yml",
        ):
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_entrees_claude_cowork_routent_vers_les_competences_et_les_garde_fous(self):
        claude_memory = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        claude_agent = (
            ROOT / "plugins" / "classe-fr" / "agents" / "classe-fr-pedagogie.md"
        ).read_text(encoding="utf-8")
        claude_project_agent = (
            ROOT / ".claude" / "agents" / "classe-fr-pedagogie.md"
        ).read_text(encoding="utf-8")

        for content in (claude_memory, claude_agent):
            for element in (
                "demarrer-avec-classe-fr",
                "cadrage-annee-scolaire",
                "bibliotheque-pedagogique",
                "style-et-design-prof",
                "programmation-annuelle",
                "preparation-differenciation",
                "cua-accessibilite-pedagogique",
                "evaluation-retours",
                "communication-familles",
                "bilan-de-periode",
                "feedback-au-createur",
                "objectif invariant",
                "engagement",
                "représentation",
                "action et expression",
            ):
                self.assertIn(element, content)
        self.assertIn("classe-fr-pedagogie", claude_memory)
        self.assertIn("name: classe-fr-pedagogie", claude_agent)
        self.assertIn("tools: Read, Glob, Grep", claude_agent)
        self.assertIn("donnée d'élève identifiable", claude_agent)
        self.assertIn("name: classe-fr-pedagogie", claude_project_agent)
        self.assertIn("plugins/classe-fr/agents/classe-fr-pedagogie.md", claude_project_agent)
        self.assertIn("aucune donnée d'élève identifiable", claude_project_agent)

    def test_guide_de_demarrage_couvre_les_premiers_usages_enseignants(self):
        guide = (ROOT / "DEMARRER.md").read_text(encoding="utf-8")

        for element in (
            "préparer une séance",
            "rendre un support plus accessible",
            "rédiger une communication collective aux familles",
            "Demande prête à copier",
            "Informations minimales à fournir",
            "Exemple fictif de réponse attendue",
            "Points à vérifier avant usage",
            "Engagement",
            "Représentations variées",
            "Action et expression",
            "aucun nom d'élève",
            "validation humaine",
        ):
            self.assertIn(element, guide)

    def test_prompts_par_defaut_guident_les_premiers_usages(self):
        manifest = json.loads(
            (ROOT / "plugins" / "classe-fr" / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        prompts = manifest["interface"]["defaultPrompt"]
        texte = "\n".join(prompts)

        self.assertEqual(len(prompts), 3)
        for element in (
            "Je débute avec Classe FR",
            "mon niveau et de ma discipline",
            "45 minutes",
            "CM1",
            "fractions",
            "objectif",
            "déroulé",
            "trace écrite",
            "options CUA",
            "support fictif",
            "objectif invariant",
            "obstacles possibles",
            "corrections concrètes",
            "version imprimable",
        ):
            self.assertIn(element, texte)
        self.assertIn("Je débute avec Classe FR", prompts[0])
        for prompt in prompts:
            self.assertNotIn("ma classe", prompt)
            self.assertNotIn("profil de style", prompt)
            self.assertNotIn("feedback", prompt)

    def test_page_confiance_clarifie_le_perimetre_du_pilote(self):
        page = (ROOT / "CONFIANCE.md").read_text(encoding="utf-8")
        matrice = (
            ROOT
            / "plugins"
            / "classe-fr"
            / "references"
            / "matrice-couverture-discipline-niveau.md"
        ).read_text(encoding="utf-8")

        for element in (
            "Ce que Classe FR sait faire aujourd’hui",
            "La source de vérité",
            "matrice de couverture discipline × niveau",
            "appui transversal fiable",
            "exemple fictif disponible",
            "couverture validée par revue humaine",
            "Aucune discipline n’est aujourd’hui couverte comme validée",
            "source institutionnelle",
            "programme",
            "référentiel",
            "validation humaine",
        ):
            self.assertIn(element, page)
        self.assertIn("../../../CONFIANCE.md", matrice)

    def test_page_publique_est_presente_et_reference_des_images_locales(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

        for relative_path in (
            "plugins/classe-fr/assets/images/public/classe-fr-hero.png",
            "plugins/classe-fr/assets/images/public/preparer-seance.png",
            "plugins/classe-fr/assets/images/public/accessibilite-confidentialite.png",
            "docs/assets/classe-fr-hero.png",
            "docs/assets/preparer-seance.png",
            "docs/assets/accessibilite-confidentialite.png",
        ):
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)
        self.assertIn("Voir la page publique", readme)
        self.assertIn("https://stephanebayle.github.io/classe-fr/", readme)
        self.assertIn("Préparer la classe avec plus de clarté.", page)
        self.assertIn("Essayez avec cette demande.", page)
        self.assertIn("Ce que vous obtenez.", page)
        self.assertIn("conception universelle de l'apprentissage (CUA)", page)
        self.assertIn("commencez par cette option", page)
        self.assertIn("Aucune matière n'est présentée comme validée", page)
        self.assertIn("Démarrer seul en 4 étapes.", page)
        self.assertIn("Cette page présente le plugin", page)
        self.assertIn("Dans le menu Plugins, choisissez Ajouter une marketplace", page)
        self.assertIn("Si un champ Réf. Git apparaît", page)
        self.assertIn("Questions fréquentes.", page)
        self.assertIn("Je ne vois pas le menu Plugins.", page)
        self.assertIn("Puis-je coller une copie d'élève ?", page)
        self.assertIn("Faire un retour", page)
        self.assertIn("issues/new?template=teacher-feedback.yml", page)
        self.assertIn("Vos données restent dans votre espace de travail.", page)
        self.assertNotIn("Les données restent hors du dépôt.", page)
        self.assertNotIn("Le dépôt et le formulaire", page)
        self.assertNotIn("collaborateurs du repo", page)
        self.assertIn("alt=\"Bureau de préparation", page)
        self.assertIn("alt=\"Carnet de préparation", page)
        self.assertIn("alt=\"Support pédagogique abstrait", page)

    def test_cas_usage_complets_sont_fictifs_relisibles_et_couvrants(self):
        cas = (ROOT / "CAS-USAGE.md").read_text(encoding="utf-8")

        for element in (
            "Cas d’usage complets",
            "Tous les exemples sont fictifs",
            "Demande initiale",
            "Informations fournies",
            "Réponse produite",
            "Vérifications humaines restantes",
            "transformer un support peu accessible",
            "préparer une séance courte",
            "créer une grille d’évaluation",
            "rédiger un message collectif aux familles",
            "préparer un bilan de période anonymisé",
            "6e",
            "CM1",
            "CAP",
            "4e",
            "maternelle",
            "Objectif invariant",
            "Engagement",
            "Représentations variées",
            "Action et expression",
            "aucune classe réelle",
            "validation humaine",
        ):
            self.assertIn(element, cas)
        self.assertGreaterEqual(cas.count("## Cas "), 5)

    def test_feedback_createur_est_court_public_et_confirme(self):
        modele = (
            ROOT / "plugins" / "classe-fr" / "assets" / "modeles" / "feedback.md"
        ).read_text(encoding="utf-8")
        skill = (
            ROOT / "plugins" / "classe-fr" / "skills" / "feedback-au-createur" / "SKILL.md"
        ).read_text(encoding="utf-8")
        formulaire = (
            ROOT / ".github" / "ISSUE_TEMPLATE" / "teacher-feedback.yml"
        ).read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for element in (
            "Ce formulaire est public",
            "ne joignez aucun document",
            "Contexte pédagogique non identifiable",
            "Impact : faible | moyen | élevé",
            "Résultat attendu ou proposition",
            "Confirmation de confidentialité obligatoire",
            "Version courte prête à coller",
            "aucun nom",
        ):
            self.assertIn(element, modele)
        for element in (
            "tenir en une page",
            "version courte prête à coller",
            "Ne jamais créer, envoyer ou publier le retour sans demande explicite séparée",
            "Éviter le vocabulaire technique GitHub",
            "formulaire public",
        ):
            self.assertIn(element, skill)
        self.assertIn("Ce formulaire est public", formulaire)
        self.assertIn("Le formulaire de retour est public", readme)

    def test_tokens_imposent_l_accessibilite(self):
        tokens = ROOT / "plugins" / "classe-fr" / "assets" / "modeles" / "design-tokens.json"
        payload = json.loads(tokens.read_text(encoding="utf-8"))
        self.assertTrue(payload["accessibilite"]["contraste_renforce"])
        self.assertFalse(payload["mise_en_page"]["information_par_couleur_seule"])

    def test_precontrole_anonymisation_signale_sans_afficher_les_donnees(self):
        module = load_module(PRECONTROL, "precontrole_anonymisation")
        document_fictif = (
            "Camille Martin — camille.martin@example.test\n"
            "Téléphone : 06 12 34 56 78\n"
            "12 rue des Écoles\n"
            "Identifiant : AB123456\n"
        )
        rapport = module.formater_rapport(module.detecter_signaux(document_fictif))

        self.assertIn("adresse e-mail", rapport)
        self.assertIn("numéro de téléphone", rapport)
        self.assertIn("adresse postale possible", rapport)
        self.assertIn("identifiant possible", rapport)
        self.assertIn("nom complet possible", rapport)
        self.assertNotIn("Camille Martin", rapport)
        self.assertNotIn("example.test", rapport)

    def test_precontrole_exige_un_format_texte(self):
        module = load_module(PRECONTROL, "precontrole_anonymisation_format")
        with tempfile.TemporaryDirectory() as temporary:
            document = Path(temporary) / "support.pdf"
            document.write_text("contenu fictif", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Format non pris en charge"):
                module.lire_document(document)

    def test_precontrole_exige_une_relecture_explicite_avant_usage(self):
        with tempfile.TemporaryDirectory() as temporary:
            document = Path(temporary) / "support.md"
            document.write_text("objectif de séance fictif", encoding="utf-8")

            sans_confirmation = subprocess.run(
                [sys.executable, str(PRECONTROL), str(document)],
                capture_output=True,
                check=False,
                text=True,
            )
            avec_confirmation = subprocess.run(
                [sys.executable, str(PRECONTROL), str(document), "--confirme-relecture"],
                capture_output=True,
                check=False,
                text=True,
            )

        self.assertEqual(sans_confirmation.returncode, 3)
        self.assertIn("Ajoutez --confirme-relecture", sans_confirmation.stdout)
        self.assertEqual(avec_confirmation.returncode, 0)
        self.assertIn("Relecture explicitement confirmée", avec_confirmation.stdout)

    def test_audit_accessible_distingue_resultats_et_entrees_cua(self):
        audit = (
            ROOT / "plugins" / "classe-fr" / "assets" / "modeles" / "audit-support-accessible.md"
        ).read_text(encoding="utf-8")
        for element in (
            "Exigences respectées",
            "Points à renforcer",
            "Choix pédagogique à valider",
            "Engagement",
            "Représentations variées",
            "Action et expression",
            "information ne repose jamais sur la seule couleur",
            "version imprimable lisible",
        ):
            self.assertIn(element, audit)

    def test_parcours_fictifs_couvrent_les_contextes_et_les_entrees_cua(self):
        module = load_module(PARCOURS_VALIDATOR, "validate_parcours_fictifs")
        self.assertEqual(module.validate_dataset(PARCOURS_FIXTURE), [])

    def test_parcours_non_conforme_echoue_avec_un_message_comprehensible(self):
        module = load_module(PARCOURS_VALIDATOR, "validate_parcours_fictifs_erreur")
        cases = json.loads(PARCOURS_FIXTURE.read_text(encoding="utf-8"))
        case_non_conforme = copy.deepcopy(cases[0])
        case_non_conforme["options_cua"]["action_expression"] = []

        errors = module.validate_case(case_non_conforme)

        self.assertIn("Les options CUA `action_expression` doivent être une liste non vide.", errors)

    def test_parcours_ne_remplace_pas_une_modalite_explicitement_evaluee(self):
        module = load_module(PARCOURS_VALIDATOR, "validate_parcours_fictifs_modalite")
        cases = json.loads(PARCOURS_FIXTURE.read_text(encoding="utf-8"))
        case_non_conforme = copy.deepcopy(cases[4])
        case_non_conforme["modalites_expression"].append("Expliquer oralement")

        errors = module.validate_case(case_non_conforme)

        self.assertIn(
            "Quand la modalité est évaluée, ne pas la remplacer par une expression non équivalente.",
            errors,
        )

    def test_registre_sources_requiert_les_metadonnees_et_les_statuts(self):
        module = load_module(SOURCES_VALIDATOR, "validate_registre_sources")
        self.assertEqual(module.validate_registry(SOURCES_REGISTRY), [])
        self.assertEqual(module.validate_registry(SOURCES_FIXTURE), [])

    def test_connecteurs_publics_sont_documentes_en_lecture_seule(self):
        reference = (
            ROOT
            / "plugins"
            / "classe-fr"
            / "references"
            / "connecteurs-publics-institutionnels.md"
        ).read_text(encoding="utf-8")
        sources = (
            ROOT / "plugins" / "classe-fr" / "references" / "sources-et-droits.md"
        ).read_text(encoding="utf-8")
        confidentialite = (
            ROOT / "plugins" / "classe-fr" / "references" / "confidentialite.md"
        ).read_text(encoding="utf-8")

        for element in (
            "data.education.gouv.fr",
            "Forge des communs numériques éducatifs",
            "lecture seule",
            "date de consultation",
            "licence absente ou à vérifier",
            "limite d'interprétation",
            "espace authentifié",
            "diagnostic individuel",
        ):
            self.assertIn(element, reference)
        self.assertIn("connecteurs-publics-institutionnels.md", sources)
        self.assertIn("projet Forge privé", confidentialite)

    def test_competences_citent_les_sources_publiques_avec_prudence(self):
        fichiers = [
            ROOT
            / "plugins"
            / "classe-fr"
            / "skills"
            / "bibliotheque-pedagogique"
            / "SKILL.md",
            ROOT
            / "plugins"
            / "classe-fr"
            / "skills"
            / "programmation-annuelle"
            / "SKILL.md",
            ROOT
            / "plugins"
            / "classe-fr"
            / "skills"
            / "preparation-differenciation"
            / "SKILL.md",
        ]

        for fichier in fichiers:
            contenu = fichier.read_text(encoding="utf-8")
            self.assertIn("connecteurs-publics-institutionnels.md", contenu)
            self.assertIn("date de consultation", contenu)
            self.assertIn("licence", contenu)

    def test_rapport_de_revue_rend_les_decisions_visibles(self):
        module = load_module(SOURCES_VALIDATOR, "validate_registre_sources_rapport")
        sources = json.loads(SOURCES_FIXTURE.read_text(encoding="utf-8"))
        rapport = module.format_review_report(sources)

        for statut in ("changement constaté", "à analyser", "aucun changement pertinent"):
            self.assertIn(statut, rapport)
        self.assertIn("Aucune recommandation pédagogique n'est modifiée", rapport)

    def test_triage_feedback_fictif_est_tracable_de_bout_en_bout(self):
        module = load_module(FEEDBACK_VALIDATOR, "validate_triage_feedback")
        self.assertEqual(module.validate_dataset(FEEDBACK_FIXTURE), [])

    def test_triage_feedback_livre_exige_toutes_les_etapes(self):
        module = load_module(FEEDBACK_VALIDATOR, "validate_triage_feedback_etapes")
        feedback = json.loads(FEEDBACK_FIXTURE.read_text(encoding="utf-8"))[0]
        feedback["historique"] = feedback["historique"][:-1]

        errors = module.validate_feedback(feedback)

        self.assertIn("Un feedback livré doit suivre : reçu, à instruire, planifié, livré.", errors)

    def test_matrice_couverture_distingue_appui_exemple_et_validation(self):
        matrice = (
            ROOT
            / "plugins"
            / "classe-fr"
            / "references"
            / "matrice-couverture-discipline-niveau.md"
        ).read_text(encoding="utf-8")

        for element in (
            "Appui transversal",
            "Exemple contextualisé",
            "Couverture validée",
            "PS",
            "CP",
            "CM1 / 6e",
            "Collège",
            "Lycée général ou technologique",
            "Lycée professionnel ou CFA",
            "Aucune cellule n'atteint encore ce niveau",
        ):
            self.assertIn(element, matrice)

    @staticmethod
    def _lignes_matrice_disciplinaire() -> dict[str, dict[str, str]]:
        """Relire le tableau par famille de la matrice, indexé par identifiant de profil."""
        matrice = (
            ROOT
            / "plugins"
            / "classe-fr"
            / "references"
            / "matrice-couverture-discipline-niveau.md"
        ).read_text(encoding="utf-8")
        section = matrice.split("## Couverture par famille disciplinaire", 1)[1]
        section = section.split("## Lire les niveaux de couverture", 1)[0]

        colonnes = (
            "niveau",
            "famille",
            "appui_transversal",
            "exemple_contextualise",
            "statut_couverture",
            "couverture_validee",
            "preuve",
        )
        lignes: dict[str, dict[str, str]] = {}
        for ligne in section.splitlines():
            if not ligne.startswith("|") or set(ligne) <= set("| -"):
                continue
            cellules = [cellule.strip() for cellule in ligne.strip("|").split("|")]
            if len(cellules) != len(colonnes) or cellules[0] == "Niveau ou voie":
                continue
            entree = dict(zip(colonnes, cellules))
            identifiants = re.findall(r"Profil `([\w-]+)`", entree["preuve"])
            assert len(identifiants) == 1, entree["preuve"]
            lignes[identifiants[0]] = entree
        return lignes

    def test_matrice_et_profils_disciplinaires_annoncent_le_meme_statut(self):
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        lignes = self._lignes_matrice_disciplinaire()

        self.assertEqual(
            sorted(lignes),
            sorted(profil["id"] for profil in profils),
            "La matrice et les profils disciplinaires ne listent pas les mêmes familles.",
        )
        for profil in profils:
            ligne = lignes[profil["id"]]
            self.assertEqual(
                ligne["statut_couverture"].lower(),
                profil["statut_couverture"],
                f"Statut divergent pour {profil['id']}.",
            )
            self.assertEqual(ligne["famille"], profil["famille"], profil["id"])

    def test_matrice_ne_promet_aucune_couverture_validee_sans_revue_humaine(self):
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        lignes = self._lignes_matrice_disciplinaire()

        for profil in profils:
            self.assertIsNone(
                profil["revue_humaine"],
                f"{profil['id']} annonce une revue humaine non consignée dans la matrice.",
            )
            self.assertNotEqual(profil["statut_couverture"], "couverture validée", profil["id"])
            self.assertEqual(
                lignes[profil["id"]]["couverture_validee"],
                "À construire",
                f"{profil['id']} promet une couverture validée sans revue humaine.",
            )

    def test_matrice_reserve_l_exemple_contextualise_a_un_parcours_fictif(self):
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        parcours = {
            cas["id"] for cas in json.loads(PARCOURS_FIXTURE.read_text(encoding="utf-8"))
        }
        lignes = self._lignes_matrice_disciplinaire()

        for profil in profils:
            ligne = lignes[profil["id"]]
            cites = set(re.findall(r"parcours fictifs? ((?:`[\w-]+`(?: et )?)+)", ligne["preuve"]))
            identifiants = {
                identifiant
                for groupe in cites
                for identifiant in re.findall(r"`([\w-]+)`", groupe)
            }
            if profil["statut_couverture"] == "exemple contextualisé":
                self.assertTrue(identifiants, f"{profil['id']} sans parcours fictif cité.")
                self.assertTrue(
                    identifiants <= parcours,
                    f"{profil['id']} cite un parcours fictif inexistant : {identifiants - parcours}",
                )
            else:
                self.assertEqual(identifiants, set(), profil["id"])
                self.assertIn("Aucun parcours fictif", ligne["exemple_contextualise"])

    def test_page_confiance_reste_coherente_avec_la_matrice_disciplinaire(self):
        page = (ROOT / "CONFIANCE.md").read_text(encoding="utf-8")
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))

        avec_exemple = [
            profil for profil in profils if profil["statut_couverture"] == "exemple contextualisé"
        ]
        self.assertEqual(len(avec_exemple), len(profils))
        for fragment in (
            "Les dix familles disciplinaires disposent donc d’au moins un exemple fictif.",
            "pas qu’une matière est validée",
            "Aucune discipline n’est aujourd’hui couverte comme validée",
        ):
            self.assertIn(fragment, page)

    def test_parcours_fictifs_couvrent_les_grandes_familles_disciplinaires(self):
        module = load_module(PARCOURS_VALIDATOR, "validate_parcours_fictifs_familles")
        cas = json.loads(PARCOURS_FIXTURE.read_text(encoding="utf-8"))
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual(module.FAMILY_IDS, {profil["id"] for profil in profils})
        self.assertEqual({case["famille"] for case in cas}, module.FAMILY_IDS)
        self.assertGreaterEqual(len(cas), 12)

    def test_parcours_sans_famille_connue_est_refuse(self):
        module = load_module(PARCOURS_VALIDATOR, "validate_parcours_fictifs_famille_inconnue")
        cas = json.loads(PARCOURS_FIXTURE.read_text(encoding="utf-8"))
        case_non_conforme = copy.deepcopy(cas[0])
        case_non_conforme["famille"] = "philosophie"

        errors = module.validate_case(case_non_conforme)

        self.assertTrue(
            any("doit se rattacher à une famille" in error for error in errors),
            errors,
        )

    def test_validateur_parcours_signale_une_famille_sans_parcours(self):
        module = load_module(PARCOURS_VALIDATOR, "validate_parcours_fictifs_famille_absente")
        cas = copy.deepcopy(json.loads(PARCOURS_FIXTURE.read_text(encoding="utf-8")))
        for case in cas:
            if case["famille"] == "eps":
                case["famille"] = "francais"

        with tempfile.TemporaryDirectory() as temporary:
            fichier = Path(temporary) / "parcours.json"
            fichier.write_text(json.dumps(cas, ensure_ascii=False), encoding="utf-8")
            errors = module.validate_dataset(fichier)

        self.assertEqual(
            errors,
            ["Les familles disciplinaires sans parcours fictif sont : eps."],
        )

    def test_procedure_de_revue_disciplinaire_est_documentee(self):
        reference = REVIEW_REFERENCE.read_text(encoding="utf-8")
        matrice = (
            ROOT
            / "plugins"
            / "classe-fr"
            / "references"
            / "matrice-couverture-discipline-niveau.md"
        ).read_text(encoding="utf-8")

        for element in (
            "## Qui peut relire",
            "## Ce qui doit être vérifié",
            "## Ce qu'il faut consigner",
            "## Lier la décision",
            "## Quand rétrograder",
            "enseignant",
            "formateur",
            "pair compétent",
            "mainteneur",
            "jamais son nom",
            "**Objectif**",
            "**Niveau**",
            "**Vocabulaire**",
            "**Source**",
            "**CUA**",
            "**Modalité évaluée**",
            "**Confidentialité**",
            "journal de version",
            "Classe FR n'est pas une autorité pédagogique",
        ):
            self.assertIn(element, reference, element)
        self.assertIn("Comment une cellule passe à « Couverture validée »", matrice)
        self.assertIn("references/revue-disciplinaire.md", matrice)

    def test_revues_disciplinaires_fictives_couvrent_les_trois_decisions(self):
        module = load_module(REVIEW_VALIDATOR, "validate_revue_disciplinaire")
        revues = json.loads(REVIEW_FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual(module.validate_dataset(REVIEW_FIXTURE), [])
        self.assertEqual({revue["decision"] for revue in revues}, set(module.DECISIONS))

    def test_couverture_validee_exige_les_sept_points_verifies(self):
        module = load_module(REVIEW_VALIDATOR, "validate_revue_disciplinaire_points")
        revues = json.loads(REVIEW_FIXTURE.read_text(encoding="utf-8"))
        revue = copy.deepcopy(revues[0])
        revue["points_verifies"]["source"] = False

        errors = module.validate_review(revue)

        self.assertIn(
            "Une couverture validée exige les sept points vérifiés ; il manque : source.",
            errors,
        )

    def test_couverture_validee_exige_une_source_datee_et_des_limites(self):
        module = load_module(REVIEW_VALIDATOR, "validate_revue_disciplinaire_source")
        revues = json.loads(REVIEW_FIXTURE.read_text(encoding="utf-8"))
        sans_source = copy.deepcopy(revues[0])
        del sans_source["source"]
        sans_limites = copy.deepcopy(revues[0])
        sans_limites["limites"] = ""
        sans_reference = copy.deepcopy(revues[0])
        sans_reference["reference_decision"] = ""

        self.assertIn("La source retenue est obligatoire.", module.validate_review(sans_source))
        self.assertIn("Le champ `limites` doit être renseigné.", module.validate_review(sans_limites))
        self.assertIn(
            "Le champ `reference_decision` doit être renseigné.",
            module.validate_review(sans_reference),
        )

    def test_retrogradation_exige_un_motif(self):
        module = load_module(REVIEW_VALIDATOR, "validate_revue_disciplinaire_retrogradation")
        revues = json.loads(REVIEW_FIXTURE.read_text(encoding="utf-8"))
        revue = copy.deepcopy(revues[2])
        del revue["motif_retrogradation"]

        errors = module.validate_review(revue)

        self.assertIn("Une rétrogradation doit consigner son motif.", errors)

    def test_revue_consigne_un_role_et_jamais_un_nom(self):
        module = load_module(REVIEW_VALIDATOR, "validate_revue_disciplinaire_role")
        revues = json.loads(REVIEW_FIXTURE.read_text(encoding="utf-8"))
        avec_nom = copy.deepcopy(revues[0])
        avec_nom["nom_relecteur"] = "Camille Martin"
        sans_role = copy.deepcopy(revues[0])
        sans_role["role_relecteur"] = "Personne ayant relu le document"

        self.assertIn(
            "Le registre est public : retirer le champ `nom_relecteur`.",
            module.validate_review(avec_nom),
        )
        self.assertTrue(
            any("décrit par son rôle" in error for error in module.validate_review(sans_role)),
            module.validate_review(sans_role),
        )

    def test_profil_en_couverture_validee_exige_limites_et_reference_de_decision(self):
        module = load_module(PROFILES_VALIDATOR, "validate_profils_disciplinaires_decision")
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        profil = copy.deepcopy(profils[0])
        profil["statut_couverture"] = "couverture validée"
        profil["revue_humaine"] = {
            "role_relecteur": "Enseignante de cycle 2, relecture disciplinaire",
            "revue_le": "2026-08-05",
            "decision": "couverture validée",
        }

        errors = module.validate_profile(profil)

        self.assertIn("La revue humaine doit renseigner `limites`.", errors)
        self.assertIn("La revue humaine doit renseigner `reference_decision`.", errors)

        profil["revue_humaine"]["limites"] = "Porte sur le seul repérage d'une information écrite."
        profil["revue_humaine"]["reference_decision"] = "issue fictive #000"
        self.assertEqual(module.validate_profile(profil), [])

        profil["revue_humaine"]["nom_relecteur"] = "Camille Martin"
        self.assertIn(
            "Le registre est public : consigner un rôle, jamais un nom.",
            module.validate_profile(profil),
        )

    def test_competences_signalent_la_limite_de_couverture(self):
        for nom in (
            "preparation-differenciation",
            "programmation-annuelle",
            "evaluation-retours",
            "cua-accessibilite-pedagogique",
        ):
            contenu = (
                ROOT / "plugins" / "classe-fr" / "skills" / nom / "SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("Aucune famille n'étant en couverture validée", contenu, nom)

    def test_reference_profils_disciplinaires_reste_prudente(self):
        reference = PROFILES_REFERENCE.read_text(encoding="utf-8")

        for element in (
            "## Français",
            "## Mathématiques",
            "## Histoire, géographie et EMC",
            "## Sciences, SVT et physique-chimie",
            "## Langues vivantes",
            "## Technologie et numérique",
            "## Arts plastiques et éducation musicale",
            "## Éducation physique et sportive",
            "## Voie professionnelle et CFA",
            "## Maternelle, par domaines d'apprentissage",
            "Repère transversal",
            "Vigilance disciplinaire",
            "Source à vérifier",
            "revue humaine disciplinaire",
            "objectif invariant",
            "Modalité évaluée",
            "Aucune famille n'atteint le niveau",
            "Engagement, représentation, action et expression",
            "fictives ou anonymisées",
        ):
            self.assertIn(element, reference)
        self.assertNotIn("[TODO:", reference)

    def test_chaque_profil_disciplinaire_documente_les_six_reperes_attendus(self):
        reference = PROFILES_REFERENCE.read_text(encoding="utf-8")
        familles = [
            "## Français",
            "## Mathématiques",
            "## Histoire, géographie et EMC",
            "## Sciences, SVT et physique-chimie",
            "## Langues vivantes",
            "## Technologie et numérique",
            "## Arts plastiques et éducation musicale",
            "## Éducation physique et sportive",
            "## Voie professionnelle et CFA",
            "## Maternelle, par domaines d'apprentissage",
        ]

        for famille in familles:
            debut = reference.index(famille)
            suivants = [
                reference.index(autre)
                for autre in familles + ["## Contrôle automatique"]
                if reference.index(autre) > debut
            ]
            entree = reference[debut : min(suivants)]
            for repere in (
                "**Souvent évalué**",
                "**Obstacles fréquents**",
                "**Options CUA utiles**",
                "**Formes de trace**",
                "**Vigilance**",
                "**Sources à vérifier**",
            ):
                self.assertIn(repere, entree, f"{famille} sans {repere}")

    def test_competences_peuvent_lire_les_profils_disciplinaires(self):
        for nom in (
            "preparation-differenciation",
            "programmation-annuelle",
            "evaluation-retours",
            "cua-accessibilite-pedagogique",
        ):
            contenu = (
                ROOT / "plugins" / "classe-fr" / "skills" / nom / "SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("references/profils-disciplinaires.md", contenu, nom)

    def test_profils_disciplinaires_couvrent_les_grandes_familles(self):
        module = load_module(PROFILES_VALIDATOR, "validate_profils_disciplinaires")
        self.assertEqual(module.validate_dataset(PROFILES_FIXTURE), [])

    def test_profil_disciplinaire_incomplet_echoue_avec_un_message_comprehensible(self):
        module = load_module(PROFILES_VALIDATOR, "validate_profils_disciplinaires_erreur")
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        profil_non_conforme = copy.deepcopy(profils[0])
        profil_non_conforme["appuis_cua"]["action_expression"] = []

        errors = module.validate_profile(profil_non_conforme)

        self.assertIn("Les appuis CUA `action_expression` doivent être une liste non vide.", errors)

    def test_profil_sans_reserve_de_source_est_refuse(self):
        module = load_module(PROFILES_VALIDATOR, "validate_profils_disciplinaires_source")
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        profil_non_conforme = copy.deepcopy(profils[0])
        profil_non_conforme["reserve_source"] = "Conforme au programme officiel en vigueur."

        errors = module.validate_profile(profil_non_conforme)

        self.assertIn(
            "La réserve doit indiquer que la source reste à vérifier ou à confirmer.",
            errors,
        )

    def test_couverture_validee_exige_une_revue_humaine_consignee(self):
        module = load_module(PROFILES_VALIDATOR, "validate_profils_disciplinaires_revue")
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        profil_non_conforme = copy.deepcopy(profils[0])
        profil_non_conforme["statut_couverture"] = "couverture validée"

        errors = module.validate_profile(profil_non_conforme)

        self.assertIn(
            "Une couverture validée exige une revue humaine disciplinaire consignée.",
            errors,
        )

        profil_conforme = copy.deepcopy(profil_non_conforme)
        profil_conforme["revue_humaine"] = {
            "role_relecteur": "Enseignante de lettres, second degré",
            "revue_le": "2026-08-05",
            "decision": "Repères jugés cohérents avec la source citée.",
            "limites": "Porte sur ce seul niveau ; ne couvre pas le reste du cycle.",
            "reference_decision": "issue fictive #000",
        }
        self.assertEqual(module.validate_profile(profil_conforme), [])

    def test_profil_preserve_l_objectif_invariant_et_la_modalite_evaluee(self):
        module = load_module(PROFILES_VALIDATOR, "validate_profils_disciplinaires_objectif")
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        profil = copy.deepcopy(profils[0])

        objectif_perdu = copy.deepcopy(profil)
        objectif_perdu["adaptations_types"][0]["objectif_invariant_preserve"] = False
        modalite_remplacee = copy.deepcopy(profil)
        modalite_remplacee["adaptations_types"][1]["modalites_expression"].append(
            "Expliquer oralement"
        )

        self.assertIn(
            "Une adaptation type doit déclarer que l'objectif invariant est préservé.",
            module.validate_profile(objectif_perdu),
        )
        self.assertIn(
            "Quand la modalité est évaluée, ne pas la remplacer par une expression non équivalente.",
            module.validate_profile(modalite_remplacee),
        )

    def test_profils_disciplinaires_ne_contiennent_aucune_donnee_personnelle(self):
        module = load_module(PROFILES_VALIDATOR, "validate_profils_disciplinaires_confidentialite")
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))
        profil_non_conforme = copy.deepcopy(profils[0])
        profil_non_conforme["obstacles_frequents"].append("Contact : famille@example.test")

        with tempfile.TemporaryDirectory() as temporary:
            fichier = Path(temporary) / "profils.json"
            fichier.write_text(
                json.dumps(profils[1:] + [profil_non_conforme], ensure_ascii=False),
                encoding="utf-8",
            )
            errors = module.validate_dataset(fichier)

        self.assertIn(
            "francais : le profil contient un signal de donnée personnelle.",
            errors,
        )

    def test_validateur_profils_signale_une_famille_manquante(self):
        module = load_module(PROFILES_VALIDATOR, "validate_profils_disciplinaires_famille")
        profils = json.loads(PROFILES_FIXTURE.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as temporary:
            fichier = Path(temporary) / "profils.json"
            fichier.write_text(json.dumps(profils[1:], ensure_ascii=False), encoding="utf-8")
            errors = module.validate_dataset(fichier)

        self.assertEqual(
            errors,
            ["Les grandes familles disciplinaires manquantes sont : francais."],
        )


if __name__ == "__main__":
    unittest.main()
