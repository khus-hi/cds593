# Fixes to Ghost's deletion path

Fixes for the four traces classified as bugs or non-compliant (see `../CLASSIFICATION.md`, rows 1-4).
`deletion-fixes.patch` is the unified diff against Ghost 5.130.6; `src/` holds the patched files,
and `Dockerfile` layers them onto the official `ghost:5-alpine` image.

| Fix | Trace | Change |
|---|---|---|
| Destroy sessions | bug: `sessions` rows outlived the user | `services/Users.js` + `destroyUserSessions()` |
| Delete orphaned images | bug: profile/cover images still served | `services/Users.js` + `deleteOrphanedImages()` |
| Backup retention | non-compliant: pre-deletion backup kept forever | `services/Users.js` + `pruneDeletionBackups()`; config `privacy:deletionBackupRetentionDays` (default 0) |
| Scrub history log | non-compliant: name/email kept in `actions` | `services/Users.js`, `api/endpoints/members.js`, `models/base/plugins/actions.js` + `scrubActions()` |

Size: 33 lines changed in 3 existing Ghost files, plus one new 157-line helper
(`services/privacy/deletion-cleanup.js`).

Re-run the audit on the patched build:

    PATCHED=1 ./run_audit.sh results/patched 600
