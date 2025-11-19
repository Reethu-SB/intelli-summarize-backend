"""File text extraction helpers for uploaded documents.

Provides `extract_text(file: UploadFile) -> str` which supports PDF, DOCX,
and TXT files. Uses `pdfplumber` (preferred) or `PyMuPDF` as a fallback for
PDFs and `python-docx` for DOCX. Raises `ValueError` for unsupported types
and `RuntimeError` for extraction failures.
"""

from io import BytesIO
from typing import Optional

from fastapi import UploadFile


async def extract_text(file: UploadFile) -> str:
    """Read an uploaded file and return extracted text.

    - `file`: FastAPI `UploadFile` instance
    - Returns extracted text (str)
    - Raises `ValueError` for unsupported file types
    - Raises `RuntimeError` for extraction failures or empty content
    """
    filename = (file.filename or "").lower()

    # Read file bytes and close the upload
    try:
        data = await file.read()
    finally:
        await file.close()

    if not data:
        raise RuntimeError("Uploaded file is empty")

    # PDF extraction: prefer pdfplumber, fall back to PyMuPDF (fitz)
    if filename.endswith(".pdf"):
        # Try pdfplumber first
        try:
            import pdfplumber

            with pdfplumber.open(BytesIO(data)) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
            text = "\n".join(pages).strip()
            if text:
                return text
        except Exception:
            # ignore and try fallback
            pass

        # Fallback: PyMuPDF
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(stream=data, filetype="pdf")
            text_parts = [page.get_text() for page in doc]
            doc.close()
            text = "\n".join(text_parts).strip()
            if text:
                return text
            raise RuntimeError("No text extracted from PDF")
        except Exception as exc:
            raise RuntimeError(f"PDF extraction failed: {exc}")

    # DOCX extraction using python-docx
    if filename.endswith(".docx"):
        try:
            import docx

            doc = docx.Document(BytesIO(data))
            paragraphs = [p.text for p in doc.paragraphs]
            text = "\n".join(paragraphs).strip()
            if text:
                return text
            raise RuntimeError("No text extracted from DOCX")
        except Exception as exc:
            raise RuntimeError(f"DOCX extraction failed: {exc}")

    # Plain text files
    if filename.endswith(".txt"):
        try:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = data.decode("latin-1")
            text = text.strip()
            if text:
                return text
            raise RuntimeError("Uploaded text file is empty")
        except Exception as exc:
            raise RuntimeError(f"Text extraction failed: {exc}")

    # Unsupported file type
    raise ValueError("Unsupported file type; supported: .pdf, .docx, .txt")
