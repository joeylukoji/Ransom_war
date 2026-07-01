import os
import zipfile

from config import dossier_fichiers, dossier_projet

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
    racine = dossier_fichiers()
    for nom, texte in [
        ("rapport.docx", "Rapport"),
        ("notes.docx", "Notes"),
        ("memo.docx", "Memo"),
    ]:
        creer_docx(os.path.join(racine, nom), texte)

    os.makedirs(os.path.join(dossier_projet(), "logs"), exist_ok=True)
    print(f"Dossier fichiers : {racine}")
    print(f"cd {dossier_projet()}")
    print("python virus/main_virus.py")
    print("python antivirus/main_antivirus.py")
