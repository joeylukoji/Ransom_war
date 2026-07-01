import os

try:
    from pdf2docx import Converter
except ImportError:
    Converter = None


class Restaurateur:
    def restaurer(self, chemin_pdf: str, chemin_docx: str) -> None:
        chemin_pdf = os.path.abspath(chemin_pdf)
        chemin_docx = os.path.abspath(chemin_docx)

        if not os.path.isfile(chemin_pdf):
            raise FileNotFoundError(chemin_pdf)
        if Converter is None:
            raise RuntimeError("Installez pdf2docx : pip install pdf2docx")

        d = os.path.dirname(chemin_docx)
        if d:
            os.makedirs(d, exist_ok=True)
        cv = Converter(chemin_pdf)
        cv.convert(chemin_docx)
        cv.close()
