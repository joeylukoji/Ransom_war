import os


class Explorateur:
    def collecter_fichiers_word(self, racine: str) -> list[str]:
        if not os.path.isdir(racine):
            raise ValueError(f"Répertoire invalide : {racine}")

        fichiers = []
        for dossier, _, noms in os.walk(os.path.abspath(racine)):
            for nom in noms:
                if not nom.startswith("~$") and nom.lower().endswith(".docx"):
                    fichiers.append(os.path.join(dossier, nom))
        return sorted(fichiers)
