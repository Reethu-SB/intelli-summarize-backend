# Models — Intelli Summarize

This folder contains SQLAlchemy model definitions used by the backend.

What SQLAlchemy models are
- Models are Python classes that map to database tables via SQLAlchemy's
  declarative `Base`. Each class defines columns (table fields) and
  optionally indexes, constraints, and relationships.

Why the `Document` model exists
- The application stores uploaded documents and their AI-generated summaries.
- The `Document` model represents a single uploaded file and its stored
  metadata so the app can query, display, and re-process documents later.

Fields stored in `Document`
- `id` — Integer primary key (unique identifier).
- `filename` — Original filename (string, not null).
- `content` — Full extracted text from the uploaded file (text, not null).
- `summary` — Generated summary (text, nullable until created).
- `uploaded_at` — Timestamp when the document was uploaded (defaults to current time).

How models interact with the database
- `database.py` exposes an `engine`, `SessionLocal` and `Base` (the declarative base).
- On startup the app can call `Base.metadata.create_all(bind=engine)` to ensure tables exist.
- Requests use a session from `get_db()` (a dependency) to add/query models:
  - Create: `db.add(obj); db.commit(); db.refresh(obj)`
  - Query: `db.query(Document).filter(...).all()`
  - Update/Delete: modify the object and `db.commit()` or `db.delete(obj)` then `db.commit()`

Notes
- For schema migrations in production, use a migration tool such as Alembic
  instead of `create_all()` to manage schema changes safely.
- Keep model definitions small and focused; business logic belongs in services.
