#!/usr/bin/env python3
"""
Point d'entrée du module antivirus — restauration PDF → Word.

Orchestre LecteurJournal, Restaurateur et JournalAntivirus.
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


def executer(chemin_log: str, chemin_rapport: str) -> int:
    """Lance la lecture du journal, la restauration et le rapport."""
    projet_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, projet_dir)

    from antivirus.lecteur_journal import LecteurJournal
    from antivirus.restaurateur import Restaurateur
    from antivirus.journal_antivirus import JournalAntivirus

    lecteur = LecteurJournal(chemin_log)
    restaurateur = Restaurateur()
    journal = JournalAntivirus(chemin_rapport)

    try:
        entrees = lecteur.charger()
    except (FileNotFoundError, ValueError) as erreur:
        print(f"❌ Erreur de lecture du journal : {erreur}")
        return 1

    if not entrees:
        print("ℹ️  Aucune entrée valide dans le journal.")
        journal.sauvegarder()
        return 0

    print(f"\n📋 {len(entrees)} entrée(s) à restaurer\n")

    for entree in entrees:
        nom = entree["nom"]
        succes, message = restaurateur.restaurer_avec_statut(
            entree["chemin_pdf"],
            entree["chemin_origine"],
        )
        journal.ajouter_entree(nom, succes, message)

        symbole = "✅" if succes else "❌"
        print(f"  {symbole} {nom} : {message}")

    journal.sauvegarder()
    print(f"\n📋 Rapport sauvegardé : {chemin_rapport}")
    print(f"📊 {journal.resume()} — Taux : {journal.taux_succes:.0f}%")

    return 0 if journal.taux_succes == 100.0 else 1


def main() -> None:
    """Point d'entrée principal avec arguments CLI."""
    parser = argparse.ArgumentParser(
        description="Restaure les fichiers .docx depuis les PDF (projet académique)."
    )
    parser.add_argument(
        "--log",
        required=True,
        help="Chemin vers virus_log.json",
    )
    parser.add_argument(
        "--rapport",
        default=None,
        help="Chemin vers rapport_restauration.json",
    )
    args = parser.parse_args()

    valider_environnement()

    projet_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_rapport = args.rapport or os.path.join(
        projet_dir, "logs", "rapport_restauration.json"
    )

    sys.exit(executer(args.log, chemin_rapport))


if __name__ == "__main__":
    main()
