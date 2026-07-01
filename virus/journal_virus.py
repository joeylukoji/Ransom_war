"""
Journal des opérations du virus (transformation Word → PDF).

Responsabilité unique : enregistrer et sérialiser les métadonnées en JSON.
"""

import json
import os
from typing import Any, Dict, List


CHAMPS_REQUIS = ("nom", "chemin_origine", "taille_octets", "chemin_pdf")


class JournalVirus:
    """Gère le journal JSON des fichiers transformés."""

    def __init__(self, chemin_log: str):
        """
        Initialise le journal.

        Args:
            chemin_log: Chemin vers le fichier virus_log.json.
        """
        self.chemin_log = os.path.abspath(chemin_log)
        self._entrees: List[Dict[str, Any]] = []

    def ajouter_entree(
        self,
        nom: str,
        chemin_origine: str,
        taille_octets: int,
        chemin_pdf: str,
    ) -> None:
        """
        Ajoute une entrée au journal.

        Args:
            nom: Nom du fichier original.
            chemin_origine: Chemin absolu du fichier .docx d'origine.
            taille_octets: Taille du fichier .docx en octets.
            chemin_pdf: Chemin absolu du PDF généré.
        """
        self._entrees.append(
            {
                "nom": nom,
                "chemin_origine": os.path.abspath(chemin_origine),
                "taille_octets": taille_octets,
                "chemin_pdf": os.path.abspath(chemin_pdf),
            }
        )

    def ajouter_depuis_fichier(self, chemin_docx: str, chemin_pdf: str) -> None:
        """Ajoute une entrée en déduisant nom et taille depuis le fichier source."""
        chemin_abs = os.path.abspath(chemin_docx)
        self.ajouter_entree(
            nom=os.path.basename(chemin_abs),
            chemin_origine=chemin_abs,
            taille_octets=os.path.getsize(chemin_abs),
            chemin_pdf=chemin_pdf,
        )

    @property
    def entrees(self) -> List[Dict[str, Any]]:
        """Retourne une copie des entrées du journal."""
        return list(self._entrees)

    def sauvegarder(self) -> None:
        """Sérialise toutes les entrées vers virus_log.json."""
        repertoire = os.path.dirname(self.chemin_log)
        if repertoire:
            os.makedirs(repertoire, exist_ok=True)

        with open(self.chemin_log, "w", encoding="utf-8") as fichier:
            json.dump(self._entrees, fichier, indent=2, ensure_ascii=False)

    @staticmethod
    def entree_valide(entree: Dict[str, Any]) -> bool:
        """Vérifie qu'une entrée contient tous les champs requis."""
        return all(champ in entree and entree[champ] is not None for champ in CHAMPS_REQUIS)


if __name__ == "__main__":
    import tempfile
    import unittest

    class TestJournalVirus(unittest.TestCase):
        """Tests unitaires pour la classe JournalVirus."""

        def test_ajouter_et_sauvegarder(self):
            with tempfile.TemporaryDirectory() as tmp:
                chemin_log = os.path.join(tmp, "virus_log.json")
                journal = JournalVirus(chemin_log)
                journal.ajouter_entree(
                    nom="test.docx",
                    chemin_origine="/tmp/test.docx",
                    taille_octets=1024,
                    chemin_pdf="/tmp/test.pdf",
                )
                journal.sauvegarder()

                with open(chemin_log, encoding="utf-8") as f:
                    donnees = json.load(f)

                self.assertEqual(len(donnees), 1)
                self.assertEqual(donnees[0]["nom"], "test.docx")
                self.assertEqual(donnees[0]["taille_octets"], 1024)

        def test_entree_invalide_sans_chemin_pdf(self):
            entree = {
                "nom": "test.docx",
                "chemin_origine": "/tmp/test.docx",
                "taille_octets": 100,
            }
            self.assertFalse(JournalVirus.entree_valide(entree))

    unittest.main()
