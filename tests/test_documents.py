"""Pytest suite for document upload endpoints.

These tests use a temporary SQLite database (set via `DATABASE_URL`) and
monkeypatch the extraction/summarization functions to avoid heavy model
dependencies. Tests cover valid uploads (PDF, DOCX, TXT), invalid files,
empty uploads, and summary length options.
"""

import importlib
import sys
from pathlib import Path
from io import BytesIO

import pytest
from fastapi.testclient import TestClient


def _import_app_with_sqlite(tmp_path):
    """Ensure environment uses a temporary SQLite DB and import a fresh `main` app."""
    # Use a file-based SQLite DB in the temporary path so SQLAlchemy can create tables
    db_path = tmp_path / "test.db"
    sqlite_url = f"sqlite:///{db_path.as_posix()}"

    # Ensure fresh import: remove modules that may cache DB/routers
    for name in ["main", "database", "routers.documents", "models.document", "models", "services.summarizer"]:
        if name in sys.modules:
            del sys.modules[name]

    # Set env var before importing (database.py reads env on import)
    import os

    os.environ["DATABASE_URL"] = sqlite_url

    # Import main (will import database and create app)
    main = importlib.import_module("main")
    return main


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create TestClient with patched extraction and summarizer functions.

    - Patches `routers.documents` to provide deterministic extraction and
      summarization results so tests are reliable and fast.
    """
    main = _import_app_with_sqlite(tmp_path)

    # Import the router module to patch functions
    docs_mod = importlib.import_module("routers.documents")

    # Patch PDF/DOCX extraction to return predictable text
    monkeypatch.setattr(docs_mod, "extract_text_from_pdf", lambda data: "Extracted PDF text.")
    monkeypatch.setattr(docs_mod, "extract_text_from_docx", lambda data: "Extracted DOCX text.")

    # Patch summarizer to include the requested length in the output
    def fake_summarize(text: str, length: str = "medium") -> str:
        return f"{length}_summary_for:{text[:30]}"

    monkeypatch.setattr(docs_mod, "summarize_text", fake_summarize)

    with TestClient(main.app) as test_client:
        yield test_client


def test_upload_txt_success(client):
    files = {"file": ("notes.txt", BytesIO(b"Hello from txt file"), "text/plain")}
    data = {"length": "short", "retries": "0"}
    resp = client.post("/documents/upload/", files=files, data=data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["filename"] == "notes.txt"
    assert body["summary"].startswith("short_summary_for:")


def test_upload_pdf_docx_success(client):
    # PDF upload (content bytes won't be parsed because extraction is patched)
    files = {"file": ("doc.pdf", BytesIO(b"%PDF-1.4 fake content"), "application/pdf")}
    resp = client.post("/documents/upload/", files=files, data={"length": "medium"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["filename"] == "doc.pdf"
    assert body["summary"].startswith("medium_summary_for:")

    # DOCX upload (content bytes won't be parsed because extraction is patched)
    files = {"file": ("file.docx", BytesIO(b"PK fake docx content"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    resp = client.post("/documents/upload/", files=files, data={"length": "long"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["filename"] == "file.docx"
    assert body["summary"].startswith("long_summary_for:")


def test_invalid_and_empty_files(client):
    # Unsupported file type (jpg)
    files = {"file": ("image.jpg", BytesIO(b"\xff\xd8\xff fake jpg"), "image/jpeg")}
    resp = client.post("/documents/upload/", files=files)
    assert resp.status_code == 415

    # Another unsupported type (xls)
    files = {"file": ("sheet.xls", BytesIO(b"fake xls"), "application/vnd.ms-excel")}
    resp = client.post("/documents/upload/", files=files)
    assert resp.status_code == 415

    # Empty file
    files = {"file": ("empty.txt", BytesIO(b""), "text/plain")}
    resp = client.post("/documents/upload/", files=files)
    assert resp.status_code == 400


@pytest.mark.parametrize("length", ["short", "medium", "long"])
def test_summary_length_options(client, length):
    files = {"file": (f"sample_{length}.txt", BytesIO(b"Some longish text to summarize."), "text/plain")}
    resp = client.post("/documents/upload/", files=files, data={"length": length})
    assert resp.status_code == 201
    body = resp.json()
    assert body["summary"].startswith(f"{length}_summary_for:")
