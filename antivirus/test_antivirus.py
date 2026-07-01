"""Tests pytest pour le module antivirus."""

import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from antivirus.lecteur_journal import LecteurJournal
from antivirus.restaurateur import Restaurateur
from antivirus.journal_antivirus import JournalAntivirus


class TestLecteurJournalPytest(unittest.TestCase):
    def test_charger_filtre(self):
        with tempfile.TemporaryDirectory() as tmp:
            chemin = os.path.join(tmp, "log.json")
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(
                    [
                        {
                            "nom": "a.docx",
                            "chemin_origine": "/a.docx",
                            "taille_octets": 1,
                            "chemin_pdf": "/a.pdf",
                        },
                        {"nom": "bad"},
                    ],
                    f,
                )
            self.assertEqual(len(LecteurJournal(chemin).charger()), 1)

    def test_introuvable(self):
        with self.assertRaises(FileNotFoundError):
            LecteurJournal("/nope.json").charger()


class TestRestaurateurPytest(unittest.TestCase):
    @patch("antivirus.restaurateur.Pdf2DocxConverter")
    @patch("antivirus.restaurateur.os.path.isfile", return_value=True)
    def test_restauration(self, _f, mock_cls):
        mock_cls.return_value = MagicMock()
        with patch("antivirus.restaurateur.os.path.abspath", side_effect=lambda p: p):
            path = Restaurateur().restaurer("/a.pdf", "/a.docx")
        self.assertEqual(path, "/a.docx")

    @patch("antivirus.restaurateur.os.path.isfile", return_value=False)
    def test_pdf_manquant(self, _):
        with self.assertRaises(FileNotFoundError):
            Restaurateur().restaurer("/x.pdf", "/x.docx")


class TestJournalAntivirusPytest(unittest.TestCase):
    def test_taux_succes(self):
        j = JournalAntivirus("/tmp/r.json")
        j.ajouter_entree("a", True, "ok")
        j.ajouter_entree("b", False, "err")
        self.assertEqual(j.taux_succes, 50.0)

    def test_resume_vide(self):
        j = JournalAntivirus("/tmp/r.json")
        self.assertIn("0/0", j.resume())
