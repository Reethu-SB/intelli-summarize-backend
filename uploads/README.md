# Uploads

This directory temporarily stores uploaded files while the application
extracts text from them. Files are saved here only for processing and should
not be committed to version control.

Usage notes
- Uploaded files are written to this folder when received by the `/documents`
  upload endpoint, then processed (text extraction and summarization).
- In production, files should be removed as soon as processing completes to
  avoid storing sensitive data and to free disk space.

Git / security
- Add `uploads/` to `.gitignore` so uploaded files are not committed.
- Keep this README in the folder; you may commit `uploads/README.md` but nothing
  else from the directory.

Example `.gitignore` entry:

```
uploads/
!/uploads/README.md
```

Best practices
- Set restrictive file permissions for this folder so only the application
  user can read/write files.
- Regularly clear old files (cron job or background worker) if automatic
  deletion on processing is not implemented.
