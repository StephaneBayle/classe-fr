from __future__ import annotations

import importlib.util
import json
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
            "message collectif aux familles",
            "sortie scolaire",
            "sans donnée d'élève",
            "ton clair et professionnel",
        ):
            self.assertIn(element, texte)
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

    def test_reference_profils_disciplinaires_reste_prudente(self):
        reference = PROFILES_REFERENCE.read_text(encoding="utf-8")

        for element in (
            "Français et langage",
            "Mathématiques",
            "Sciences et technologie",
            "Langues vivantes",
            "Histoire, géographie et EMC",
            "Arts et éducation physique et sportive",
            "Enseignement professionnel et technologique",
            "à vérifier",
            "revue humaine disciplinaire",
            "objectif invariant",
            "modalité évaluée",
            "Aucune famille n'atteint ce niveau",
            "engagement",
            "représentation",
            "action et expression",
            "fictives ou anonymisées",
        ):
            self.assertIn(element, reference)
        self.assertNotIn("[TODO:", reference)

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
            "francais-et-langage : le profil contient un signal de donnée personnelle.",
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
            ["Les grandes familles disciplinaires manquantes sont : francais-et-langage."],
        )


if __name__ == "__main__":
    unittest.main()
