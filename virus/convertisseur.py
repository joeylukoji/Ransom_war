import os

try:
    from docx2pdf import convert
except ImportError:
    convert = None


class Convertisseur:
    def convertir_en_pdf(self, chemin_docx: str) -> str:
        chemin_abs = os.path.abspath(chemin_docx)
        if not os.path.isfile(chemin_abs):
            raise FileNotFoundError(chemin_abs)

        chemin_pdf = os.path.splitext(chemin_abs)[0] + ".pdf"
        if convert is None:
            raise RuntimeError("Installez docx2pdf : pip install docx2pdf")

        convert(chemin_abs, chemin_pdf)
        if not os.path.isfile(chemin_pdf):
            raise RuntimeError(f"PDF non généré : {chemin_pdf}")
        return chemin_pdf
