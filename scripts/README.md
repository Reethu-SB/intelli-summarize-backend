# Scripts

This folder contains optional helper scripts and automation utilities for
the project. Scripts here are not required for normal operation but can be
useful for development, maintenance, or deployment tasks.

Typical contents
- Database initialization or migration helpers
- Cleanup tools (e.g., remove old uploads)
- Small automation scripts used during development or CI

Guidance
- Keep scripts idempotent and safe to run repeatedly when possible.
- Document any required environment variables or preconditions in the
  script header or in the project README.
- Prefer placing long-running or production tasks into dedicated services
  rather than one-off scripts.
