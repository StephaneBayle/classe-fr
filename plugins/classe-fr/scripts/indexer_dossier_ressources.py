#!/usr/bin/env python3
"""Proposer des fiches de bibliothèque à partir d'un dossier local, sans lire les fichiers.

Ce script ne lit aucun contenu, ne copie aucune ressource et n'écrit pas dans la
bibliothèque. Il propose des entrées que l'enseignant valide avant intégration.
Le crible sur les noms de fichiers signale ; il ne certifie pas l'anonymat.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


VOLUME_MAXIMUM = 200
SUFFIXES_IGNORES = {".ds_store", ".tmp", ".part", ".lock"}
SEPARATEURS = re.compile(r"[._\-]+")
MOTIFS_NOM_DE_FICHIER = {
    "adresse e-mail": re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    "numéro de téléphone": re.compile(r"(?<!\d)(?:\+33|0)[1-9](?:[ .-]?\d{2}){4}(?!\d)"),
    "nom complet possible": re.compile(
        r"\b[A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]{1,}\s+[A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]{1,}\b"
    ),
    "dossier de suivi individuel": re.compile(
        r"\b(?:pap|pps|ppre|pai|gevasco|mdph|ess)\b", re.IGNORECASE
    ),
    "document individuel possible": re.compile(
        r"\b(?:bulletin|bulletins|copie|copies|notes|note|livret|trombinoscope|"
        r"absences|retards|sanction|signalement|eleve|eleves|élève|élèves)\b",
        re.IGNORECASE,
    ),
}


def normaliser(nom: str) -> str:
    """Remplacer les séparateurs de nom de fichier par des espaces.

    Sans cette étape, `PAP_Lucas_CM1` échapperait à la détection de nom propre.
    """
    return SEPARATEURS.sub(" ", nom).strip()


def signaux_du_nom(nom: str) -> list[str]:
    """Retourner les catégories repérées dans un nom de fichier, jamais le nom."""
    normalise = normaliser(nom)
    return [
        categorie
        for categorie, motif in MOTIFS_NOM_DE_FICHIER.items()
        if motif.search(normalise)
    ]


def lister_fichiers(dossier: Path) -> list[Path]:
    """Lister le dossier et ses sous-dossiers immédiats, sans ouvrir de fichier."""
    fichiers: list[Path] = []
    for entree in sorted(dossier.iterdir()):
        if entree.name.startswith("."):
            continue
        if entree.is_file():
            fichiers.append(entree)
        elif entree.is_dir():
            fichiers.extend(
                sous_entree
                for sous_entree in sorted(entree.iterdir())
                if sous_entree.is_file() and not sous_entree.name.startswith(".")
            )
    return [
        fichier for fichier in fichiers if fichier.suffix.lower() not in SUFFIXES_IGNORES
    ]


def fiche(fichier: Path, racine: Path, consulte_le: str) -> dict[str, object]:
    """Construire une fiche de bibliothèque sans rien deviner du contenu."""
    return {
        "titre": fichier.stem,
        "statut": "personnelle",
        "niveau": "À compléter",
        "discipline": "À compléter",
        "objectif": "À compléter",
        "licence": "À vérifier",
        "emplacement_ou_url": str(fichier.relative_to(racine)),
        "consulte_le": consulte_le,
        "apports_cua": [],
        "note_de_reemploi": "Fiche proposée automatiquement ; à relire avant réemploi.",
    }


def indexer(dossier: Path, consulte_le: str | None = None) -> dict[str, object]:
    """Proposer des fiches et signaler les fichiers écartés, sans les nommer."""
    if not dossier.is_dir():
        raise ValueError(f"Dossier introuvable : {dossier}")

    fichiers = lister_fichiers(dossier)
    if len(fichiers) > VOLUME_MAXIMUM:
        raise ValueError(
            f"{len(fichiers)} fichiers repérés, au-delà de {VOLUME_MAXIMUM}. "
            "Choisir un dossier plus resserré, par exemple une année ou une séquence."
        )

    consulte_le = consulte_le or date.today().isoformat()
    fiches: list[dict[str, object]] = []
    ecartes: list[dict[str, object]] = []
    for position, fichier in enumerate(fichiers, start=1):
        signaux = signaux_du_nom(fichier.name)
        if signaux:
            ecartes.append({"position": position, "signaux": signaux})
            continue
        fiches.append(fiche(fichier, dossier, consulte_le))
    return {"fiches": fiches, "ecartes": ecartes, "total": len(fichiers)}


def formater_rapport(resultat: dict[str, object]) -> str:
    """Présenter le résultat sans jamais afficher un nom de fichier écarté."""
    fiches = resultat["fiches"]
    ecartes = resultat["ecartes"]
    lignes = [
        f"Fichiers examinés : {resultat['total']}.",
        f"Fiches proposées : {len(fiches)}.",
        f"Fichiers écartés : {len(ecartes)}.",
    ]
    if ecartes:
        lignes.append("")
        lignes.append(
            "Ces fichiers portent un signal de donnée personnelle dans leur nom. "
            "Ils ne sont pas indexés et ne sont pas nommés ici ; à vous de les relire."
        )
        for ecarte in ecartes:
            categories = ", ".join(ecarte["signaux"])
            lignes.append(f"- fichier n°{ecarte['position']} du listing : {categories}")
    lignes.append("")
    lignes.append(
        "Aucun fichier n'a été ouvert, lu ni copié. Niveau, discipline et objectif "
        "restent à compléter ; la licence reste à vérifier. Rien n'est ajouté à la "
        "bibliothèque avant votre validation."
    )
    return "\n".join(lignes)


def echapper(valeur: object) -> str:
    """Protéger une valeur issue d'un nom de fichier arbitraire."""
    return str(valeur).replace("\\", "\\\\").replace('"', '\\"')


def formater_fiches_yaml(fiches: list[dict[str, object]]) -> str:
    """Rendre les fiches au format de `assets/modeles/bibliotheque.yml`."""
    if not fiches:
        return "ressources: []\n"
    lignes = ["ressources:"]
    for entree in fiches:
        lignes.append(f'  - titre: "{echapper(entree["titre"])}"')
        for cle in (
            "statut",
            "niveau",
            "discipline",
            "objectif",
            "licence",
            "emplacement_ou_url",
            "consulte_le",
        ):
            lignes.append(f'    {cle}: "{echapper(entree[cle])}"')
        lignes.append("    apports_cua: []")
        lignes.append(f'    note_de_reemploi: "{echapper(entree["note_de_reemploi"])}"')
    return "\n".join(lignes) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path, help="Dossier de ressources à examiner")
    parser.add_argument(
        "--fiches",
        action="store_true",
        help="Afficher les fiches proposées au format bibliothèque",
    )
    args = parser.parse_args()
    try:
        resultat = indexer(args.dossier)
    except ValueError as exc:
        print(f"Indexation impossible : {exc}")
        raise SystemExit(2) from exc
    print(formater_rapport(resultat))
    if args.fiches:
        print()
        print(formater_fiches_yaml(resultat["fiches"]), end="")


if __name__ == "__main__":
    main()
