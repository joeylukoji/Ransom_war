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
    parser.add_argument("--root", default=TEST_ROOT)
    parser.add_argument("--log", default=None)
    args = parser.parse_args()

    valider_environnement()
    projet = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, projet)

    from virus.explorateur import Explorateur
    from virus.convertisseur import Convertisseur
    from virus.journal_virus import JournalVirus

    racine = os.path.realpath(os.path.expanduser(args.root))
    if os.path.realpath(TEST_ROOT) not in racine:
        print("ERREUR : --root doit être dans le répertoire de test.")
        sys.exit(1)

    log = args.log or os.path.join(projet, "logs", "virus_log.json")
    journal = JournalVirus(log)
    convertisseur = Convertisseur()

    for chemin in Explorateur().collecter_fichiers_word(racine):
        nom = os.path.basename(chemin)
        try:
            pdf = convertisseur.convertir_en_pdf(chemin)
            journal.ajouter(chemin, pdf)
            print(f"OK  {nom} -> {os.path.basename(pdf)}")
        except Exception as e:
            print(f"ERR {nom} : {e}")

    journal.sauvegarder()
    print(f"Journal : {log} ({len(journal.entrees)} entrée(s))")


if __name__ == "__main__":
    main()
