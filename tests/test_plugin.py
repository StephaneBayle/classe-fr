from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins" / "classe-fr" / "scripts" / "init_teacher_space.py"
VALIDATOR = ROOT / "plugins" / "classe-fr" / "scripts" / "validate_classe_fr.py"


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

    def test_tokens_imposent_l_accessibilite(self):
        tokens = ROOT / "plugins" / "classe-fr" / "assets" / "modeles" / "design-tokens.json"
        payload = json.loads(tokens.read_text(encoding="utf-8"))
        self.assertTrue(payload["accessibilite"]["contraste_renforce"])
        self.assertFalse(payload["mise_en_page"]["information_par_couleur_seule"])


if __name__ == "__main__":
    unittest.main()
