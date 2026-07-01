import json
import os

CHAMPS_REQUIS = ("nom", "chemin_origine", "taille_octets", "chemin_pdf")


class JournalVirus:
    def __init__(self, chemin_log: str):
        self.chemin_log = os.path.abspath(chemin_log)
        self.entrees = []

    def ajouter(self, chemin_docx: str, chemin_pdf: str) -> None:
        chemin_docx = os.path.abspath(chemin_docx)
        self.entrees.append({
            "nom": os.path.basename(chemin_docx),
            "chemin_origine": chemin_docx,
            "taille_octets": os.path.getsize(chemin_docx),
            "chemin_pdf": os.path.abspath(chemin_pdf),
        })

    def sauvegarder(self) -> None:
        d = os.path.dirname(self.chemin_log)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(self.chemin_log, "w", encoding="utf-8") as f:
            json.dump(self.entrees, f, indent=2, ensure_ascii=False)

    @staticmethod
    def entree_valide(entree: dict) -> bool:
        return isinstance(entree, dict) and all(
            entree.get(c) is not None for c in CHAMPS_REQUIS
        )
