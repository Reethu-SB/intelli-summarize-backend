# Services — Intelli Summarize

This folder contains service modules that perform the core work behind the
API endpoints. Services are small, focused utilities used by routers to keep
request handling simple and testable.

Purpose of the service layer
- Encapsulate business logic and I/O (file parsing, model calls) outside of
  request handlers.
- Make functionality reusable by different routers or background tasks.
- Improve testability by allowing routers to mock service functions.

`file_processing.py` — file extraction responsibilities
- Accepts an uploaded file (`UploadFile`) and returns plain text.
- Supports PDF, DOCX, and TXT formats.
  - PDFs: tries `pdfplumber` first (robust text extraction), falls back to
    `PyMuPDF` (`fitz`) if needed.
  - DOCX: uses `python-docx` to read paragraphs.
  - TXT: decodes bytes (utf-8, then latin-1) to text.
- Raises clear exceptions on unsupported types, extraction errors, or empty
  content so callers can return appropriate HTTP errors.

`summarizer.py` — AI summary generation
- Provides a single entrypoint to generate summaries from text.
- Uses HuggingFace `transformers` summarization pipelines (model configurable
  via env var) and exposes presets for `short`, `medium`, and `long` summaries.
- Caches the pipeline instance to avoid reloading the model on each request.
- Raises informative errors on model load or runtime failures so callers can
  decide whether to retry or record the failure.

How services support routers
- Routers orchestrate request flow: validate input, call services, persist
  results, and return responses.
- The `documents` router calls `file_processing.extract_text()` to get text,
  then `summarizer.generate_summary()` to create a summary, then saves both
  the original text and the summary to the `Document` model via the DB.
- Because services raise explicit exceptions, the router can map those to
  HTTP responses (400/415/422/500) or attempt retries when appropriate.

Testing and extensibility
- Services are written to be easy to mock in tests; routers can patch service
  functions to return deterministic values.
- If summarization becomes heavy, the summarizer calls can be moved to a
  background worker or separate microservice; routers only need to call the
  service interface and handle the response.
