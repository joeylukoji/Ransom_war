"""Tests pytest pour le module virus."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from virus.explorateur import Explorateur
from virus.convertisseur import Convertisseur
from virus.journal_virus import JournalVirus


class TestExplorateurPytest(unittest.TestCase):
    @patch("virus.explorateur.os.walk")
    @patch("virus.explorateur.os.path.isdir", return_value=True)
    @patch("virus.explorateur.os.path.exists", return_value=True)
    @patch("virus.explorateur.os.path.abspath", side_effect=lambda p: p)
    def test_collecte_docx(self, _a, _e, _d, mock_walk):
        mock_walk.return_value = [("/test", [], ["a.docx", "b.txt"])]
        resultat = Explorateur().collecter_fichiers_word("/test")
        self.assertEqual(resultat, [os.path.join("/test", "a.docx")])

    @patch("virus.explorateur.os.path.exists", return_value=False)
    def test_racine_inexistante(self, _):
        with self.assertRaises(ValueError):
            Explorateur().collecter_fichiers_word("/inexistant")


class TestConvertisseurPytest(unittest.TestCase):
    @patch("virus.convertisseur.docx2pdf_convert")
    @patch("virus.convertisseur.os.path.isfile", return_value=True)
    def test_conversion(self, _f, mock_convert):
        with patch("virus.convertisseur.os.path.abspath", side_effect=lambda p: p):
            pdf = Convertisseur().convertir_en_pdf("/t/doc.docx")
        self.assertEqual(pdf, "/t/doc.pdf")
        mock_convert.assert_called_once()

    @patch("virus.convertisseur.os.path.isfile", return_value=False)
    def test_introuvable(self, _):
        with self.assertRaises(FileNotFoundError):
            Convertisseur().convertir_en_pdf("/x.docx")


class TestJournalVirusPytest(unittest.TestCase):
    def test_sauvegarde(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = os.path.join(tmp, "log.json")
            j = JournalVirus(log)
            j.ajouter_entree("a.docx", "/a.docx", 10, "/a.pdf")
            j.sauvegarder()
            with open(log, encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data[0]["nom"], "a.docx")

    def test_entree_valide(self):
        self.assertTrue(
            JournalVirus.entree_valide(
                {"nom": "a", "chemin_origine": "/a", "taille_octets": 1, "chemin_pdf": "/p"}
            )
        )
