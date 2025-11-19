"""SQLAlchemy `Document` model for Intelli Summarize.

Defines the `documents` table with an indexed `id` and `filename`.
Fields: id, filename, content, summary, uploaded_at.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index
from database import Base


class Document(Base):
    __tablename__ = "documents"

    # Primary key (indexed for quick lookups)
    id = Column(Integer, primary_key=True, index=True)

    # Original filename of the uploaded document
    filename = Column(String(255), nullable=False, index=True)

    # Full document content
    content = Column(Text, nullable=False)

    # Generated summary (nullable until created)
    summary = Column(Text, nullable=True)

    # Timestamp when the document was uploaded; set to current time by DB
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


# Explicit indexes (id and filename are already indexed above, this keeps intent clear)
Index("ix_documents_id", Document.id)
Index("ix_documents_filename", Document.filename)
