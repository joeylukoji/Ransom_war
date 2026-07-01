#!/usr/bin/env python3
"""
Prépare l'environnement de test isolé pour le projet virus/antivirus.

Crée ~/test_virus_antivirus avec des fichiers .docx de démonstration
et copie le projet dans ce répertoire pour respecter les contraintes de sécurité.
"""

import os
import shutil
import zipfile

TEST_ROOT = os.path.expanduser("~/test_virus_antivirus")
PROJECT_SRC = os.path.dirname(os.path.abspath(__file__))
PROJECT_DEST = os.path.join(TEST_ROOT, "projet_virus_antivirus")


def _creer_docx_minimal(chemin: str, titre: str) -> None:
    """Crée un fichier .docx minimal valide (sans dépendance externe)."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    word_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>
"""

    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>{titre}</w:t></w:r></w:p>
  </w:body>
</w:document>"""

    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("word/_rels/document.xml.rels", word_rels)
        archive.writestr("word/document.xml", document)


def _copier_projet() -> None:
    """Copie le projet dans le répertoire de test."""
    if os.path.normpath(PROJECT_SRC) == os.path.normpath(PROJECT_DEST):
        return

    shutil.copytree(
        PROJECT_SRC,
        PROJECT_DEST,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )


def main() -> None:
    """Crée l'environnement de test et affiche les instructions."""
    fichiers_test = [
        (os.path.join(TEST_ROOT, "Documents", "rapport.docx"), "Rapport de test"),
        (os.path.join(TEST_ROOT, "Documents", "notes.docx"), "Notes de cours"),
        (os.path.join(TEST_ROOT, "Bureau", "memo.docx"), "Mémo important"),
    ]

    print(f"📁 Création de l'environnement : {TEST_ROOT}")

    for chemin, titre in fichiers_test:
        _creer_docx_minimal(chemin, titre)
        print(f"  ✅ {chemin}")

    _copier_projet()
    print(f"  ✅ Projet copié vers {PROJECT_DEST}")

    print("\n🚀 Prochaines étapes :")
    print(f"   cd {PROJECT_DEST}")
    print(f"   pip install -r requirements.txt")
    print(f"   python virus/main_virus.py --root {TEST_ROOT}")
    print(f"   python antivirus/main_antivirus.py --log ./logs/virus_log.json")


if __name__ == "__main__":
    main()
