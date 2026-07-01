"""
Restaurateur PDF → Word.

Responsabilité unique : reconvertir un PDF en .docx à l'emplacement d'origine.
"""

import os
from typing import Tuple

try:
    from pdf2docx import Converter as Pdf2DocxConverter
except ImportError:
    Pdf2DocxConverter = None


class Restaurateur:
    """Restaure les fichiers Word à partir des PDF générés."""

    def restaurer(self, chemin_pdf: str, chemin_destination: str) -> str:
        """
        Convertit un PDF en .docx et l'enregistre à l'emplacement d'origine.

        Args:
            chemin_pdf: Chemin absolu du fichier PDF source.
            chemin_destination: Chemin absolu où recréer le fichier .docx.

        Returns:
            Chemin absolu du fichier .docx restauré.

        Raises:
            FileNotFoundError: Si le PDF source n'existe pas.
            ValueError: Si les chemins ne sont pas valides.
            RuntimeError: Si la conversion échoue.
        """
        chemin_pdf_abs = os.path.abspath(chemin_pdf)
        chemin_dest_abs = os.path.abspath(chemin_destination)

        if not os.path.isfile(chemin_pdf_abs):
            raise FileNotFoundError(f"PDF introuvable : {chemin_pdf_abs}")
        if not chemin_pdf_abs.lower().endswith(".pdf"):
            raise ValueError(f"Le fichier source doit être un .pdf : {chemin_pdf_abs}")
        if not chemin_dest_abs.lower().endswith(".docx"):
            raise ValueError(
                f"La destination doit être un .docx : {chemin_dest_abs}"
            )

        repertoire = os.path.dirname(chemin_dest_abs)
        if repertoire:
            os.makedirs(repertoire, exist_ok=True)

        try:
            if Pdf2DocxConverter is None:
                raise ImportError("pdf2docx non installé")
            convertisseur = Pdf2DocxConverter(chemin_pdf_abs)
            convertisseur.convert(chemin_dest_abs)
            convertisseur.close()
        except ImportError as erreur:
            raise RuntimeError(
                "La bibliothèque pdf2docx n'est pas installée. "
                "Exécutez : pip install pdf2docx"
            ) from erreur
        except Exception as erreur:
            raise RuntimeError(
                f"Échec de la restauration de {chemin_pdf_abs} : {erreur}"
            ) from erreur

        if not os.path.isfile(chemin_dest_abs):
            raise RuntimeError(
                f"Le fichier .docx n'a pas été généré : {chemin_dest_abs}"
            )

        return chemin_dest_abs

    def restaurer_avec_statut(
        self, chemin_pdf: str, chemin_destination: str
    ) -> Tuple[bool, str]:
        """
        Restaure un fichier et retourne le statut.

        Returns:
            Tuple (succès booléen, message).
        """
        try:
            self.restaurer(chemin_pdf, chemin_destination)
            return True, "Restauration réussie"
        except (FileNotFoundError, ValueError, RuntimeError) as erreur:
            return False, str(erreur)


if __name__ == "__main__":
    import unittest
    from unittest.mock import patch, MagicMock

    class TestRestaurateur(unittest.TestCase):
        """Tests unitaires pour la classe Restaurateur."""

        def setUp(self):
            self.restaurateur = Restaurateur()

        @patch("antivirus.restaurateur.Pdf2DocxConverter")
        @patch("antivirus.restaurateur.os.path.isfile", return_value=True)
        @patch("antivirus.restaurateur.os.makedirs")
        def test_restauration_reussie(self, _makedirs, _isfile, mock_converter_cls):
            mock_instance = MagicMock()
            mock_converter_cls.return_value = mock_instance

            with patch(
                "antivirus.restaurateur.os.path.abspath", side_effect=lambda p: p
            ):
                chemin = self.restaurateur.restaurer("/test/doc.pdf", "/test/doc.docx")

            mock_converter_cls.assert_called_once_with("/test/doc.pdf")
            mock_instance.convert.assert_called_once_with("/test/doc.docx")
            mock_instance.close.assert_called_once()
            self.assertEqual(chemin, "/test/doc.docx")

        @patch("antivirus.restaurateur.os.path.isfile", return_value=False)
        def test_pdf_introuvable(self, _isfile):
            with self.assertRaises(FileNotFoundError):
                self.restaurateur.restaurer("/test/inexistant.pdf", "/test/doc.docx")

    unittest.main()
