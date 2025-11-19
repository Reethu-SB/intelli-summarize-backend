# Tests — Intelli Summarize

This folder contains tests for the backend. Tests are written with `pytest`
and use FastAPI's `TestClient` for endpoint testing.

What is tested
- File upload handling (PDF, DOCX, TXT)
- Text extraction from uploaded files (extraction logic)
- Summarization output and length options (short/medium/long)
- Handling of invalid formats and empty uploads (error responses)

Testing approach
- Unit tests mock or patch heavy dependencies (like the summarizer and
  extraction internals) so tests run fast and deterministically.
- Integration-style tests use a temporary SQLite database to avoid touching
  your production data and to allow table creation during tests.

How to run tests

1. Install test dependencies (from project root):

```powershell
python -m pip install -r requirements.txt
```

2. Run pytest:

```powershell
pytest -q
```

Tips for writing tests
- Patch service functions in `services/` (e.g., summarizer) to return
  predictable values when testing routers.
- Use the provided fixtures in `tests/` for setting up a temporary DB and
  `TestClient` to call endpoints.
- Keep tests small and focused: one assertion per behavior where possible.
