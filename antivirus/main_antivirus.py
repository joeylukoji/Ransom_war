# CONFIGURATION DE SÉCURITÉ — ENVIRONNEMENT DE TEST UNIQUEMENT
import argparse
import os
import sys

TEST_ROOT = os.path.expanduser("~/test_virus_antivirus")


def valider_environnement():
    test_root = os.path.realpath(TEST_ROOT)
    if test_root not in os.path.realpath(os.getcwd()):
        print(f"ERREUR : exécuter depuis {test_root}")
        sys.exit(1)
    print(f"Environnement OK : {test_root}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--rapport", default=None)
    args = parser.parse_args()

    valider_environnement()
    projet = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, projet)

    from antivirus.lecteur_journal import LecteurJournal
    from antivirus.restaurateur import Restaurateur
    from antivirus.journal_antivirus import JournalAntivirus

    rapport = args.rapport or os.path.join(projet, "logs", "rapport_restauration.json")
    journal = JournalAntivirus(rapport)
    restaurateur = Restaurateur()

    for entree in LecteurJournal(args.log).charger():
        nom = entree["nom"]
        try:
            restaurateur.restaurer(entree["chemin_pdf"], entree["chemin_origine"])
            journal.ajouter(nom, True, "Restauration réussie")
            print(f"OK  {nom}")
        except Exception as e:
            journal.ajouter(nom, False, str(e))
            print(f"ERR {nom} : {e}")

    journal.sauvegarder()
    print(f"Rapport : {rapport} — {journal.taux_succes():.0f}% succès")


if __name__ == "__main__":
    main()
