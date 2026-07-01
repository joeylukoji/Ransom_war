import json
import os


class JournalAntivirus:
    def __init__(self, chemin_rapport: str):
        self.chemin_rapport = os.path.abspath(chemin_rapport)
        self.entrees = []

    def ajouter(self, nom: str, succes: bool, message: str) -> None:
        self.entrees.append({"nom": nom, "succes": succes, "message": message})

    def sauvegarder(self) -> None:
        d = os.path.dirname(self.chemin_rapport)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(self.chemin_rapport, "w", encoding="utf-8") as f:
            json.dump(self.entrees, f, indent=2, ensure_ascii=False)

    def taux_succes(self) -> float:
        if not self.entrees:
            return 0.0
        ok = sum(1 for e in self.entrees if e["succes"])
        return ok / len(self.entrees) * 100
