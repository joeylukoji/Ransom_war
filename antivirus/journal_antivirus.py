import json
import os
from datetime import datetime


class JournalAntivirus:
    def __init__(self, chemin_rapport: str):
        self.chemin_rapport = os.path.abspath(chemin_rapport)
        self.entrees = []

    def ajouter(
        self,
        nom: str,
        chemin_pdf: str,
        chemin_docx: str,
        succes: bool,
        message: str,
    ) -> None:
        self.entrees.append({
            "nom": nom,
            "operation": "pdf_vers_word",
            "chemin_source": os.path.abspath(chemin_pdf),
            "chemin_resultat": os.path.abspath(chemin_docx),
            "chemin_pdf": os.path.abspath(chemin_pdf),
            "chemin_docx": os.path.abspath(chemin_docx),
            "succes": succes,
            "message": message,
            "date": datetime.now().isoformat(timespec="seconds"),
        })

    def sauvegarder(self) -> None:
        os.makedirs(os.path.dirname(self.chemin_rapport), exist_ok=True)
        with open(self.chemin_rapport, "w", encoding="utf-8") as f:
            json.dump(self.entrees, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())

    def taux_succes(self) -> float:
        if not self.entrees:
            return 0.0
        ok = sum(1 for e in self.entrees if e["succes"])
        return ok / len(self.entrees) * 100
