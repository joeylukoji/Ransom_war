import os
import sys

DOSSIER_FICHIERS = "fichiers"


def dossier_projet() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def dossier_fichiers() -> str:
    return os.path.join(dossier_projet(), DOSSIER_FICHIERS)


def chemin_log(nom: str) -> str:
    return os.path.join(dossier_projet(), "logs", nom)


def valider_racine(racine: str) -> str:
    """Les fichiers traités doivent rester dans le dossier fichiers/."""
    base = os.path.realpath(dossier_fichiers())
    racine_abs = os.path.realpath(os.path.expanduser(racine))
    if os.path.commonpath([base, racine_abs]) != base:
        print(f"ERREUR : utiliser uniquement le dossier {base}")
        sys.exit(1)
    return racine_abs
