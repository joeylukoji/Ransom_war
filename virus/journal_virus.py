import json
import os
from datetime import datetime

CHAMPS_REQUIS = ("nom", "operation", "chemin_origine", "chemin_resultat", "taille_octets", "succes")


class JournalVirus:
    def __init__(self, chemin_log: str):
        self.chemin_log = os.path.abspath(chemin_log)
        self.entrees = []

    def ajouter(self, chemin_docx: str, chemin_pdf: str | None, succes: bool, message: str = "") -> None:
        chemin_docx = os.path.abspath(chemin_docx)
        self.entrees.append({
            "nom": os.path.basename(chemin_docx),
            "operation": "word_vers_pdf",
            "chemin_origine": chemin_docx,
            "chemin_resultat": os.path.abspath(chemin_pdf) if chemin_pdf else None,
            "chemin_pdf": os.path.abspath(chemin_pdf) if chemin_pdf else None,
            "taille_octets": os.path.getsize(chemin_docx) if os.path.isfile(chemin_docx) else 0,
            "succes": succes,
            "message": message,
            "date": datetime.now().isoformat(timespec="seconds"),
        })

    def sauvegarder(self) -> None:
        os.makedirs(os.path.dirname(self.chemin_log), exist_ok=True)
        with open(self.chemin_log, "w", encoding="utf-8") as f:
            json.dump(self.entrees, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())

    @staticmethod
    def entree_valide(entree: dict) -> bool:
        return (
            isinstance(entree, dict)
            and entree.get("succes") is True
            and entree.get("chemin_pdf")
            and entree.get("chemin_origine")
        )
