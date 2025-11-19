"""
Intelli Summarize - FastAPI app entrypoint.

Run with:
	uvicorn main:app --reload

This file creates the FastAPI app, includes the `/documents` router,
creates database tables on startup using SQLAlchemy, and registers
basic exception handlers.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging

# Import SQLAlchemy engine and Base (metadata) from database.py
from database import engine, Base

# Import the documents router; expects `routers/documents.py` to expose `router`
from routers.documents import router as documents_router


app = FastAPI(title="Intelli Summarize")

# Include the documents router under /documents
app.include_router(documents_router, prefix="/documents")


@app.on_event("startup")
async def on_startup() -> None:
	"""Create all database tables defined on SQLAlchemy models' metadata.

	Uses `Base.metadata.create_all(bind=engine)` so tables are ensured on
	application startup. If the call fails, the exception is logged and
	propagated so the app won't silently run in a broken state.
	"""
	try:
		Base.metadata.create_all(bind=engine)
		logging.info("Database tables created or already exist.")
	except Exception:
		logging.exception("Failed to create database tables on startup")
		raise


@app.get("/")
async def root() -> dict:
	"""Health-check/root endpoint."""
	return {"status": "ok"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
	"""Return JSON for FastAPI/Starlette HTTPExceptions."""
	return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
	"""Catch-all exception handler: log and return 500 response."""
	logging.exception("Unhandled exception while processing request")
	return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
