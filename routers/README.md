# Routers — Intelli Summarize

This folder contains the FastAPI routers that define API endpoints.

What routers are
- Routers group related API endpoints (routes) and their request/response
  handling. They are mounted on the main FastAPI app (e.g. `app.include_router`).

The `documents` router
- Handles document-related operations such as uploading files and retrieving
  stored documents or summaries.

Upload endpoint (POST `/documents/upload/`)
- Accepts file uploads (multipart/form-data) and form fields such as
  `length` (short|medium|long) and `retries`.
- Workflow:
  1. Save the uploaded file to `uploads/` with a unique name.
  2. Extract text from the file (PDF/DOCX/TXT).
  3. Generate a summary using the summarizer service.
  4. Store the original text and summary in the database (`Document` model).
  5. Return JSON with the document `id`, `filename`, and `summary`.

Supported file formats
- PDF (.pdf)
- Word (.docx)
- Plain text (.txt)

Expected responses
- Success (201): JSON containing `id`, `filename`, and `summary`.
- Partial success: If summarization fails after retries the document is
  persisted with `summary: null` and a message explaining the failure is returned.

Error handling
- 400 Bad Request: invalid input (e.g., empty file, missing required fields).
- 415 Unsupported Media Type: uploaded file type not supported.
- 422 Unprocessable Entity: extraction or summarization failed for the file.
- 500 Internal Server Error: unexpected server-side errors while saving or processing.

Notes
- Extraction and summarization are implemented in `services/` to keep the
  router focused on request handling and orchestration.
- For retries and heavy model work consider moving summarization to a background
  worker or separate service in production.
