"""AI summarization service using HuggingFace Transformers.

Provides `generate_summary(text: str, summary_type: str) -> str` and an alias
`summarize_text` for backward compatibility with the router. Uses a cached
`transformers` summarization pipeline (default model configurable via
`SUMMARIZER_MODEL` env var).

Presets:
  - short  : concise summary
  - medium : default
  - long   : more detailed

On failure the function raises `RuntimeError` with an informative message so
calling FastAPI endpoints can handle/retry as appropriate.
"""

import os
import logging
from typing import Dict

from transformers import pipeline, Pipeline


_SUMMARIZER: Pipeline | None = None


def _get_summarizer() -> Pipeline:
    """Return a cached summarization pipeline instance.

    The model may be overridden with the `SUMMARIZER_MODEL` environment
    variable (for example: `facebook/bart-large-cnn`, `t5-base`, or
    `google/pegasus-xsum`). Loading the model is done once and reused.
    """
    global _SUMMARIZER
    if _SUMMARIZER is not None:
        return _SUMMARIZER

    model_name = os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn")
    try:
        _SUMMARIZER = pipeline("summarization", model=model_name, device=-1)
        return _SUMMARIZER
    except Exception as exc:
        logging.exception("Failed to create summarization pipeline using model %s", model_name)
        raise RuntimeError(f"Failed to load summarization model '{model_name}': {exc}")


# Preset token-lengths for summary types. Values are model-dependent but
# provide reasonable defaults across common seq2seq models.
LENGTH_PRESETS: Dict[str, Dict[str, int]] = {
    "short": {"max_length": 60, "min_length": 10},
    "medium": {"max_length": 150, "min_length": 40},
    "long": {"max_length": 300, "min_length": 80},
}


def generate_summary(text: str, summary_type: str = "medium") -> str:
    """Generate a summary for `text` using the preset `summary_type`.

    - `summary_type` must be one of: 'short', 'medium', 'long'.
    - Returns the generated summary string on success.
    - Raises `RuntimeError` with an informative message on failure.
    """
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("No text provided for summarization")

    summary_type = (summary_type or "medium").lower()
    if summary_type not in LENGTH_PRESETS:
        raise RuntimeError("Invalid summary_type; expected one of: short, medium, long")

    params = LENGTH_PRESETS[summary_type]

    # Get or create the summarization pipeline
    summarizer = _get_summarizer()

    try:
        # The pipeline may return a list of dicts with 'summary_text'
        result = summarizer(text, max_length=params["max_length"], min_length=params["min_length"], truncation=True)
        if isinstance(result, list) and result:
            # Combine results if multiple chunks were returned
            summaries = [r.get("summary_text", "") for r in result]
            combined = "\n".join(s.strip() for s in summaries if s).strip()
            if combined:
                return combined
        # Fallback if unexpected pipeline output
        raise RuntimeError("Summarizer returned no summary")
    except Exception as exc:
        logging.exception("Summarization error")
        raise RuntimeError(f"Summarization failed: {exc}")


# Backwards-compatible alias used by routers
def summarize_text(text: str, length: str = "medium") -> str:
    return generate_summary(text, summary_type=length)
