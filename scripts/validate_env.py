"""Validate required environment variables for Intelli Summarize.

Run this script during local setup or CI to ensure required env vars are set:
    python scripts/validate_env.py

It checks for either `DATABASE_URL` or the individual DB_* vars, plus
`SECRET_KEY` and `UPLOAD_DIR`. Exits with code 0 on success, 1 on failure.
"""

import os
import sys
from dotenv import load_dotenv


def check_env() -> int:
    load_dotenv()
    missing = []

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # require DB_USER, DB_NAME at minimum when DATABASE_URL is absent
        if not os.getenv("DB_USER"):
            missing.append("DB_USER")
        if not os.getenv("DB_NAME"):
            missing.append("DB_NAME")

    if not os.getenv("SECRET_KEY"):
        missing.append("SECRET_KEY")

    if not os.getenv("UPLOAD_DIR"):
        missing.append("UPLOAD_DIR")

    # Summarizer model is optional but warn if missing
    if not os.getenv("SUMMARIZER_MODEL"):
        print("Warning: SUMMARIZER_MODEL not set — default model will be used.")

    if missing:
        print("Missing required environment variables:")
        for m in missing:
            print(f" - {m}")
        return 1

    print("Environment OK — all required variables are present.")
    return 0


if __name__ == "__main__":
    sys.exit(check_env())
