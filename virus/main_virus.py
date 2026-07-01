# CONFIGURATION DE SÉCURITÉ — ENVIRONNEMENT DE TEST UNIQUEMENT
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import chemin_log, dossier_fichiers, valider_racine
from virus.explorateur import Explorateur
from virus.convertisseur import Convertisseur
from virus.journal_virus import JournalVirus


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None, help="Défaut : fichiers/")
    parser.add_argument("--log", default=None)
    args = parser.parse_args()

    racine = valider_racine(args.root or dossier_fichiers())
    log = os.path.abspath(args.log or chemin_log("virus_log.json"))
    journal = JournalVirus(log)

    for chemin in Explorateur().collecter_fichiers_word(racine):
        nom = os.path.basename(chemin)
        try:
            pdf = Convertisseur().convertir_en_pdf(chemin)
            journal.ajouter(chemin, pdf, True, "Conversion Word -> PDF réussie")
            print(f"OK  {nom} -> {pdf}")
        except Exception as e:
            journal.ajouter(chemin, None, False, str(e))
            print(f"ERR {nom} : {e}")

    journal.sauvegarder()
    print(f"Journal enregistré : {log} ({len(journal.entrees)} entrée(s))")


if __name__ == "__main__":
    main()
