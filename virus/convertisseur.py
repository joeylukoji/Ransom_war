"""
Convertisseur Word (.docx) vers PDF.

Responsabilité unique : convertir un fichier .docx en .pdf via docx2pdf.
"""

import os
from typing import Optional, Tuple

try:
    from docx2pdf import convert as docx2pdf_convert
except ImportError:
    docx2pdf_convert = None


class Convertisseur:
    """Convertit des fichiers Word en PDF."""

    def convertir_en_pdf(self, chemin_docx: str) -> str:
        """
        Convertit un fichier .docx en .pdf dans le même répertoire.

        Args:
            chemin_docx: Chemin absolu ou relatif vers le fichier .docx.

        Returns:
            Chemin absolu du fichier PDF généré.

        Raises:
            FileNotFoundError: Si le fichier source n'existe pas.
            ValueError: Si le fichier n'est pas un .docx.
            RuntimeError: Si la conversion échoue.
        """
        chemin_abs = os.path.abspath(chemin_docx)

        if not os.path.isfile(chemin_abs):
            raise FileNotFoundError(f"Fichier introuvable : {chemin_abs}")
        if not chemin_abs.lower().endswith(".docx"):
            raise ValueError(f"Le fichier doit être un .docx : {chemin_abs}")

        repertoire = os.path.dirname(chemin_abs)
        nom_base = os.path.splitext(os.path.basename(chemin_abs))[0]
        chemin_pdf = os.path.join(repertoire, f"{nom_base}.pdf")

        try:
            if docx2pdf_convert is None:
                raise ImportError("docx2pdf non installé")
            docx2pdf_convert(chemin_abs, chemin_pdf)
        except ImportError as erreur:
            raise RuntimeError(
                "La bibliothèque docx2pdf n'est pas installée. "
                "Exécutez : pip install docx2pdf"
            ) from erreur
        except Exception as erreur:
            raise RuntimeError(
                f"Échec de la conversion de {chemin_abs} : {erreur}"
            ) from erreur

        if not os.path.isfile(chemin_pdf):
            raise RuntimeError(f"Le PDF n'a pas été généré : {chemin_pdf}")

        return os.path.abspath(chemin_pdf)

    def convertir_avec_statut(self, chemin_docx: str) -> Tuple[Optional[str], str]:
        """
        Convertit un fichier et retourne le chemin PDF ou None en cas d'échec.

        Returns:
            Tuple (chemin_pdf ou None, message de statut).
        """
        try:
            chemin_pdf = self.convertir_en_pdf(chemin_docx)
            return chemin_pdf, "Conversion réussie"
        except (FileNotFoundError, ValueError, RuntimeError) as erreur:
            return None, str(erreur)


if __name__ == "__main__":
    import unittest
    from unittest.mock import patch, MagicMock

    class TestConvertisseur(unittest.TestCase):
        """Tests unitaires pour la classe Convertisseur."""

        def setUp(self):
            self.convertisseur = Convertisseur()

        @patch("virus.convertisseur.docx2pdf_convert")
        @patch("virus.convertisseur.os.path.isfile", return_value=True)
        def test_conversion_reussie(self, _isfile, mock_convert):
            with patch("virus.convertisseur.os.path.abspath", side_effect=lambda p: p):
                chemin_docx = "/test/document.docx"
                chemin_pdf = self.convertisseur.convertir_en_pdf(chemin_docx)
                mock_convert.assert_called_once_with(chemin_docx, "/test/document.pdf")
                self.assertEqual(chemin_pdf, "/test/document.pdf")

        @patch("virus.convertisseur.os.path.isfile", return_value=False)
        def test_fichier_introuvable(self, _isfile):
            with self.assertRaises(FileNotFoundError):
                self.convertisseur.convertir_en_pdf("/test/inexistant.docx")

    unittest.main()
