# CONFIGURATION DE SÉCURITÉ — ENVIRONNEMENT DE TEST UNIQUEMENT
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import chemin_log
from antivirus.lecteur_journal import LecteurJournal
from antivirus.restaurateur import Restaurateur
from antivirus.journal_antivirus import JournalAntivirus


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default=None)
    parser.add_argument("--rapport", default=None)
    args = parser.parse_args()

    log_virus = os.path.abspath(args.log or chemin_log("virus_log.json"))
    rapport = os.path.abspath(args.rapport or chemin_log("rapport_restauration.json"))

    if not os.path.isfile(log_virus):
        print(f"ERREUR : journal introuvable : {log_virus}")
        print("Lancez d'abord : python virus/main_virus.py")
        sys.exit(1)

    journal = JournalAntivirus(rapport)
    restaurateur = Restaurateur()

    for entree in LecteurJournal(log_virus).charger():
        nom = entree["nom"]
        chemin_pdf = entree["chemin_pdf"]
        chemin_docx = entree["chemin_origine"]
        try:
            restaurateur.restaurer(chemin_pdf, chemin_docx)
            journal.ajouter(nom, chemin_pdf, chemin_docx, True, "Conversion PDF -> Word réussie")
            print(f"OK  {nom} -> {chemin_docx}")
        except Exception as e:
            journal.ajouter(nom, chemin_pdf, chemin_docx, False, str(e))
            print(f"ERR {nom} : {e}")

    journal.sauvegarder()
    print(f"Rapport enregistré : {rapport} ({len(journal.entrees)} entrée(s))")


if __name__ == "__main__":
    main()
