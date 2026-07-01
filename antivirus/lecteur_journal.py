"""
Lecteur du journal virus (virus_log.json).

Responsabilité unique : charger, valider et filtrer les entrées du journal.
"""

import json
import os
from typing import Any, Dict, List

from virus.journal_virus import CHAMPS_REQUIS, JournalVirus


class LecteurJournal:
    """Charge et valide le fichier virus_log.json."""

    def __init__(self, chemin_log: str):
        """
        Initialise le lecteur.

        Args:
            chemin_log: Chemin vers virus_log.json.
        """
        self.chemin_log = os.path.abspath(chemin_log)

    def charger(self) -> List[Dict[str, Any]]:
        """
        Charge le journal et retourne les entrées valides.

        Returns:
            Liste de dictionnaires avec les champs requis.

        Raises:
            FileNotFoundError: Si le fichier journal n'existe pas.
            ValueError: Si le JSON est invalide ou n'est pas une liste.
        """
        if not os.path.isfile(self.chemin_log):
            raise FileNotFoundError(f"Journal introuvable : {self.chemin_log}")

        with open(self.chemin_log, encoding="utf-8") as fichier:
            try:
                donnees = json.load(fichier)
            except json.JSONDecodeError as erreur:
                raise ValueError(f"JSON invalide dans {self.chemin_log} : {erreur}") from erreur

        if not isinstance(donnees, list):
            raise ValueError("Le journal doit être une liste JSON.")

        entrees_valides = [e for e in donnees if self._entree_valide(e)]
        entrees_ignorees = len(donnees) - len(entrees_valides)

        if entrees_ignorees:
            print(f"⚠️  {entrees_ignorees} entrée(s) incomplète(s) ignorée(s).")

        return entrees_valides

    @staticmethod
    def _entree_valide(entree: Any) -> bool:
        """Vérifie qu'une entrée est un dictionnaire complet."""
        if not isinstance(entree, dict):
            return False
        return JournalVirus.entree_valide(entree)

    @staticmethod
    def champs_requis() -> tuple:
        """Retourne les champs attendus (compatibilité avec JournalVirus)."""
        return CHAMPS_REQUIS


if __name__ == "__main__":
    import tempfile
    import unittest

    class TestLecteurJournal(unittest.TestCase):
        """Tests unitaires pour la classe LecteurJournal."""

        def test_charger_entrees_valides(self):
            with tempfile.TemporaryDirectory() as tmp:
                chemin = os.path.join(tmp, "virus_log.json")
                donnees = [
                    {
                        "nom": "a.docx",
                        "chemin_origine": "/tmp/a.docx",
                        "taille_octets": 100,
                        "chemin_pdf": "/tmp/a.pdf",
                    },
                    {"nom": "incomplet.docx"},
                ]
                with open(chemin, "w", encoding="utf-8") as f:
                    json.dump(donnees, f)

                lecteur = LecteurJournal(chemin)
                resultat = lecteur.charger()
                self.assertEqual(len(resultat), 1)
                self.assertEqual(resultat[0]["nom"], "a.docx")

        def test_fichier_introuvable(self):
            lecteur = LecteurJournal("/chemin/inexistant/virus_log.json")
            with self.assertRaises(FileNotFoundError):
                lecteur.charger()

    unittest.main()
