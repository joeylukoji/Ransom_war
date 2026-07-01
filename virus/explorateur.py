"""
Explorateur de fichiers Word (.docx) dans un répertoire racine.

Responsabilité unique : parcourir le système de fichiers et collecter
les chemins absolus des fichiers .docx.
"""

import os
from typing import List


class Explorateur:
    """Parcourt récursivement un répertoire pour trouver les fichiers .docx."""

    def collecter_fichiers_word(self, racine: str) -> List[str]:
        """
        Parcourt récursivement `racine` et retourne tous les chemins absolus
        des fichiers se terminant par .docx.

        Args:
            racine: Chemin du répertoire racine à explorer.

        Returns:
            Liste triée de chemins absolus vers les fichiers .docx trouvés.

        Raises:
            ValueError: Si `racine` n'existe pas ou n'est pas un répertoire.
        """
        if not os.path.exists(racine):
            raise ValueError(f"Le répertoire racine n'existe pas : {racine}")
        if not os.path.isdir(racine):
            raise ValueError(f"Le chemin n'est pas un répertoire : {racine}")

        fichiers: List[str] = []
        racine_abs = os.path.abspath(racine)

        for dossier_courant, _, noms_fichiers in os.walk(racine_abs):
            try:
                for nom in noms_fichiers:
                    if nom.lower().endswith(".docx"):
                        fichiers.append(os.path.join(dossier_courant, nom))
            except OSError as erreur:
                print(f"⚠️  Accès refusé ou erreur dans {dossier_courant} : {erreur}")

        return sorted(fichiers)


if __name__ == "__main__":
    import unittest
    from unittest.mock import patch

    class TestExplorateur(unittest.TestCase):
        """Tests unitaires pour la classe Explorateur."""

        def setUp(self):
            self.explorateur = Explorateur()

        @patch("virus.explorateur.os.walk")
        @patch("virus.explorateur.os.path.isdir", return_value=True)
        @patch("virus.explorateur.os.path.exists", return_value=True)
        @patch("virus.explorateur.os.path.abspath", side_effect=lambda p: p)
        def test_collecte_docx_multiples(self, _abspath, _exists, _isdir, mock_walk):
            mock_walk.return_value = [
                ("/test", [], ["rapport.docx", "notes.txt", "memo.docx"]),
                ("/test/sous", [], ["archive.docx"]),
            ]
            resultat = self.explorateur.collecter_fichiers_word("/test")
            self.assertEqual(
                resultat,
                ["/test/archive.docx", "/test/memo.docx", "/test/rapport.docx"],
            )

        @patch("virus.explorateur.os.walk")
        @patch("virus.explorateur.os.path.isdir", return_value=True)
        @patch("virus.explorateur.os.path.exists", return_value=True)
        @patch("virus.explorateur.os.path.abspath", side_effect=lambda p: p)
        def test_ignore_fichiers_non_docx(self, _abspath, _exists, _isdir, mock_walk):
            mock_walk.return_value = [
                ("/test", [], ["image.png", "document.pdf", "readme.md"]),
            ]
            resultat = self.explorateur.collecter_fichiers_word("/test")
            self.assertEqual(resultat, [])

    unittest.main()
