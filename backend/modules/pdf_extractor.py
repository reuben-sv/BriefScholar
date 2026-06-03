import re

import pdfplumber


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from uploaded PDF file.
    Works with Streamlit uploaded_file object.
    """
    text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")

    return clean_text(text)


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.
    """
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" .", ".")
    text = text.replace(" ,", ",")
    return text.strip()


def split_text_into_chunks(text: str, chunk_size: int = 2500) -> list:
    """
    Split long paper text into smaller chunks.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks
