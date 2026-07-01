"""
Journal des opérations de l'antivirus (rapport de restauration).

Responsabilité unique : enregistrer succès/échecs et sérialiser en JSON.
"""

import json
import os
from typing import Any, Dict, List


CHAMPS_REQUIS = ("nom", "succes", "message")


class JournalAntivirus:
    """Gère le rapport JSON des restaurations."""

    def __init__(self, chemin_rapport: str):
        """
        Initialise le journal antivirus.

        Args:
            chemin_rapport: Chemin vers rapport_restauration.json.
        """
        self.chemin_rapport = os.path.abspath(chemin_rapport)
        self._entrees: List[Dict[str, Any]] = []

    def ajouter_entree(self, nom: str, succes: bool, message: str) -> None:
        """
        Ajoute une entrée au rapport.

        Args:
            nom: Nom du fichier concerné.
            succes: True si la restauration a réussi.
            message: Description du résultat.
        """
        self._entrees.append(
            {
                "nom": nom,
                "succes": succes,
                "message": message,
            }
        )

    @property
    def entrees(self) -> List[Dict[str, Any]]:
        """Retourne une copie des entrées."""
        return list(self._entrees)

    @property
    def taux_succes(self) -> float:
        """Retourne le pourcentage de restaurations réussies."""
        if not self._entrees:
            return 0.0
        reussites = sum(1 for e in self._entrees if e["succes"])
        return (reussites / len(self._entrees)) * 100

    def sauvegarder(self) -> None:
        """Sérialise le rapport vers rapport_restauration.json."""
        repertoire = os.path.dirname(self.chemin_rapport)
        if repertoire:
            os.makedirs(repertoire, exist_ok=True)

        with open(self.chemin_rapport, "w", encoding="utf-8") as fichier:
            json.dump(self._entrees, fichier, indent=2, ensure_ascii=False)

    def resume(self) -> str:
        """Retourne un résumé textuel des restaurations."""
        total = len(self._entrees)
        reussites = sum(1 for e in self._entrees if e["succes"])
        echecs = total - reussites
        return f"{reussites}/{total} restaurations réussies ({echecs} échec(s))"


if __name__ == "__main__":
    import tempfile
    import unittest

    class TestJournalAntivirus(unittest.TestCase):
        """Tests unitaires pour la classe JournalAntivirus."""

        def test_ajouter_et_taux_succes(self):
            with tempfile.TemporaryDirectory() as tmp:
                chemin = os.path.join(tmp, "rapport.json")
                journal = JournalAntivirus(chemin)
                journal.ajouter_entree("a.docx", True, "OK")
                journal.ajouter_entree("b.docx", False, "Erreur")
                journal.sauvegarder()

                self.assertEqual(journal.taux_succes, 50.0)
                self.assertIn("1/2", journal.resume())

                with open(chemin, encoding="utf-8") as f:
                    donnees = json.load(f)
                self.assertEqual(len(donnees), 2)

        def test_journal_vide(self):
            journal = JournalAntivirus("/tmp/rapport.json")
            self.assertEqual(journal.taux_succes, 0.0)
            self.assertEqual(journal.resume(), "0/0 restaurations réussies (0 échec(s))")

    unittest.main()
