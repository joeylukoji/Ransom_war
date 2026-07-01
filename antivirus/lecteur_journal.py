import json
import os

from virus.journal_virus import JournalVirus


class LecteurJournal:
    def __init__(self, chemin_log: str):
        self.chemin_log = os.path.abspath(chemin_log)

    def charger(self) -> list[dict]:
        if not os.path.isfile(self.chemin_log):
            raise FileNotFoundError(self.chemin_log)

        with open(self.chemin_log, encoding="utf-8") as f:
            donnees = json.load(f)

        if not isinstance(donnees, list):
            raise ValueError("Le journal doit être une liste JSON.")

        return [e for e in donnees if JournalVirus.entree_valide(e)]
