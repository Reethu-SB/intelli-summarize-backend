# Intelli Summarize — Backend

A small FastAPI backend that accepts uploaded documents (PDF, DOCX, TXT),
extracts their text, generates AI-powered summaries, and stores the original
text and summary in a database.

## Features

- Accepts uploads of PDF, DOCX, and TXT files
- Extracts text using `pdfplumber` / `PyMuPDF` (PDF) and `python-docx` (DOCX)
- Generates short/medium/long summaries using HuggingFace transformers
- Stores documents and summaries via SQLAlchemy (MySQL or SQLite)

## Supported file formats

- PDF (.pdf)
- Microsoft Word (.docx)
- Plain text (.txt)

## How summarization works

The backend uses a summarization pipeline provided by HuggingFace Transformers
(configurable model). Uploaded files are converted to plain text, then the
text is sent to the summarizer with a preset for `short`, `medium`, or `long`
length. Summaries and the original text are persisted in the database.

## Project structure

- `main.py` — FastAPI application entrypoint
- `database.py` — SQLAlchemy engine, `Base`, and `get_db` dependency
- `models/` — SQLAlchemy models (e.g. `models/document.py`)
- `routers/` — API routers (e.g. `routers/documents.py`)
- `services/` — Helper services (file extraction, summarizer, etc.)
- `uploads/` — Saved uploaded files
- `tests/` — Pytest test suite
- `.env.example` — Example environment variables
- `requirements.txt` — Python dependencies

## Setup

1. Copy and edit environment variables:

```powershell
cp .env.example .env
# Edit .env and set DATABASE_URL, SECRET_KEY, etc.
```

2. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

3. (Optional) Validate environment variables:

```powershell
python .\scripts\validate_env.py
```

## Run the server

Start the FastAPI app locally (auto-reload while developing):

```powershell
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. The OpenAPI docs are
at `http://127.0.0.1:8000/docs`.

## Tests

Run the test suite with pytest:

```powershell
pytest -q
```

## Contributing

- Fork the repo and create a feature branch for your changes
- Run and add tests for any new functionality
- Follow existing coding style and keep changes minimal and focused
- Open a pull request with a clear description of the change

If you'd like, include a short setup note in your PR describing any
additional environment setup (e.g., GPU drivers for model performance).

## Notes

- For development you can use SQLite (`TESTING=1` in `.env`) to avoid needing
  a MySQL server.
- Large transformer models may require significant memory; consider using a
  smaller model or running the summarizer on a separate service if needed.
# intelli-summarize-backend