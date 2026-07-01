#!/usr/bin/env python3
"""
Point d'entrée du module virus — transformation Word → PDF.

Orchestre Explorateur, Convertisseur et JournalVirus.
"""

# ⚠️ CONFIGURATION DE SÉCURITÉ — ENVIRONNEMENT DE TEST UNIQUEMENT
import argparse
import os
import sys

TEST_ROOT = os.path.expanduser("~/test_virus_antivirus")


def valider_environnement() -> None:
    """
    Valide que le code s'exécute UNIQUEMENT sur le répertoire de test.
    Empêche toute exécution sur le système réel.
    """
    if TEST_ROOT not in os.path.realpath(os.getcwd()):
        print("❌ ERREUR DE SÉCURITÉ : Ce code doit s'exécuter UNIQUEMENT")
        print(f"   dans le répertoire de test : {TEST_ROOT}")
        print("   Abandon de l'exécution.")
        sys.exit(1)

    print(f"✅ Environnement validé. Répertoire de test : {TEST_ROOT}")


def executer(racine: str, chemin_log: str) -> int:
    """Lance le parcours, la conversion et la journalisation."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from virus.explorateur import Explorateur
    from virus.convertisseur import Convertisseur
    from virus.journal_virus import JournalVirus

    explorateur = Explorateur()
    convertisseur = Convertisseur()
    journal = JournalVirus(chemin_log)

    try:
        fichiers = explorateur.collecter_fichiers_word(racine)
    except ValueError as erreur:
        print(f"❌ Erreur d'exploration : {erreur}")
        return 1

    if not fichiers:
        print(f"ℹ️  Aucun fichier .docx trouvé sous {racine}")
        journal.sauvegarder()
        return 0

    print(f"\n📂 {len(fichiers)} fichier(s) .docx trouvé(s)\n")

    succes = 0
    echecs = 0

    for chemin_docx in fichiers:
        nom = os.path.basename(chemin_docx)
        chemin_pdf, message = convertisseur.convertir_avec_statut(chemin_docx)

        if chemin_pdf:
            journal.ajouter_depuis_fichier(chemin_docx, chemin_pdf)
            print(f"  ✅ {nom} → {os.path.basename(chemin_pdf)}")
            succes += 1
        else:
            print(f"  ❌ {nom} : {message}")
            echecs += 1

    journal.sauvegarder()
    print(f"\n📋 Journal sauvegardé : {chemin_log}")
    print(f"📊 Résumé : {succes} succès, {echecs} échec(s)")

    return 0 if echecs == 0 else 1


def main() -> None:
    """Point d'entrée principal avec arguments CLI."""
    parser = argparse.ArgumentParser(
        description="Transforme les fichiers .docx en PDF (projet académique)."
    )
    parser.add_argument(
        "--root",
        default=TEST_ROOT,
        help=f"Répertoire racine à parcourir (défaut : {TEST_ROOT})",
    )
    parser.add_argument(
        "--log",
        default=None,
        help="Chemin du fichier virus_log.json",
    )
    args = parser.parse_args()

    valider_environnement()

    projet_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_log = args.log or os.path.join(projet_dir, "logs", "virus_log.json")

    racine = os.path.expanduser(args.root)
    if TEST_ROOT not in os.path.realpath(racine):
        print("❌ ERREUR DE SÉCURITÉ : --root doit être dans le répertoire de test.")
        sys.exit(1)

    sys.exit(executer(racine, chemin_log))


if __name__ == "__main__":
    main()
