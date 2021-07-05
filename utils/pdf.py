from PyPDF2 import PdfFileReader
from io import BytesIO
from typing import Sequence


def check_for_keywords(bytes_, keywords: Sequence):
    if not bytes_:
        return
    reader = PdfFileReader(BytesIO(bytes_), strict=False)
    for page in reader.pages:
        text = page.extractText()
        if any(found := [keyword for keyword in keywords if keyword in text]):
            return found
    return None
