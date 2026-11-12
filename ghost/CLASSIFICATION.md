# Ghost: classification of residual traces

Ghost 5.130.6, MySQL 8.0. Staff user **A** deleted via Settings > Staff, member **M** deleted
via Members (Ghost has no member self-deletion). Paths are relative to `core/server/`.
Categories are engineering judgments based on the code, docs and GDPR Art. 17, not legal findings.

| # | Trace | Whose | Category | Why it survives (code) | Fix |
|---|---|---|---|---|---|
| 1 | Full JSON DB backup in `content/data/` on every staff deletion: A's profile, bcrypt hash, posts, plus every other staff user's hash | A | **Non-compliant** | `services/Users.js` `destroyUser()` calls `dbBackup.backup()`; `data/db/backup.js` writes it; nothing removes it | **Fixed**: backup removed once deletion commits; `privacy:deletionBackupRetentionDays` keeps it N days for undo |
| 2 | History log (`actions`) keeps A's name and email, M's name | A, M | **Non-compliant** | `models/base/plugins/actions.js` stores `primary_name`; never anonymised, no retention | **Fixed**: name/email replaced by "Deleted user/member"; the delete event itself no longer records the name |
| 3 | Profile and cover images stay on disk, publicly served | A | **Bug** | deletion never calls the storage adapter; files unreferenced after the users row goes | **Fixed**: deleted (with `_o` original and resized copies) if nothing else references them |
| 4 | `sessions` row with A's user id, IP, user agent; expires in 6 months, never purged | A | **Bug** | `sessions.user_id` has no FK; `destroyUser()` doesn't clear sessions (`changePassword()` does) | **Fixed**: sessions destroyed in the deletion transaction |
| 5 | Posts, draft, co-authored post reassigned to owner, tagged `#<slug>` | A | Policy | `Post.reassignByAuthor()`, `assignTagToUserPosts()`: posts belong to the publication | none |
| 6 | Post revisions incl. text edited away, author nulled | A | Policy | `lib/PostRevisions.js` `removeAuthorFromRevisions()` | none |
| 7 | Image inside a kept post | A | Policy | belongs to the post | none |
| 8 | M's comment and reply stay public, author shown as nobody; P's like on M's comment stays | M | Policy | `comments.member_id` `setNullDelete`, keeps threads intact | optional: let member choose |
| 9 | Magic-link tokens with M's email, name, IP, referrer | M | Policy (time-limited) | `services/members/jobs/clean-tokens.js` deletes tokens > 24 h old daily (gone in 24-48 h; not yet confirmed by a 24 h scan) | none |
| 10 | Label named after M | M | Policy | labels are admin-created site objects | none |
| 11 | Request logs contain A's user id, upload file names, post titles | A, M | Policy (caveat) | normal access logs; `logging.rotation.enabled: false` by default | document; enable rotation |
| 12 | Emails already sent (invite, reset, signup, comment notifications with M's text) | A, M | Outside Ghost | mail lives with provider/recipients | none |
| 13 | MySQL binlog DELETE before-images hold complete deleted rows | A, M | Policy, infra (30 days) | `log_bin=ON`, `binlog_format=ROW`, `binlog_expire_logs_seconds=2592000` | document |
| 14 | Raw InnoDB pages / undo / redo hold deleted bytes | A, M | Outside app (storage engine) | purge frees space without zeroing; forensic only | out of scope |
