import os
import shutil
import zipfile

TEST_ROOT = os.path.expanduser("~/test_virus_antivirus")
PROJECT_SRC = os.path.dirname(os.path.abspath(__file__))
PROJECT_DEST = os.path.join(TEST_ROOT, "projet_virus_antivirus")

DOC_XML = """<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body><w:p><w:r><w:t>{texte}</w:t></w:r></w:p></w:body>
</w:document>"""


def creer_docx(chemin: str, texte: str) -> None:
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with zipfile.ZipFile(chemin, "w") as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        z.writestr("_rels/.rels", '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        z.writestr("word/_rels/document.xml.rels", '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')
        z.writestr("word/document.xml", DOC_XML.format(texte=texte))


if __name__ == "__main__":
    for nom, texte in [
        ("Documents/rapport.docx", "Rapport"),
        ("Documents/notes.docx", "Notes"),
        ("Bureau/memo.docx", "Memo"),
    ]:
        creer_docx(os.path.join(TEST_ROOT, nom), texte)

    if os.path.normpath(PROJECT_SRC) != os.path.normpath(PROJECT_DEST):
        shutil.copytree(
            PROJECT_SRC, PROJECT_DEST, dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", ".git", ".pytest_cache"),
        )

    print(f"Pret. cd {PROJECT_DEST}")
    print(f"python virus/main_virus.py --root {TEST_ROOT}")
