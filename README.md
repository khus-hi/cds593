# What Survives Account Deletion?

CDS 593 project (Astika Tyagi, Khushi Anil Teli): a deletion audit of two open-source
web applications, Ghost and Discourse. We create test users carrying unique canary
tokens, delete them through each app's own deletion feature, scan every storage layer
for what remains, and classify each surviving trace as a reasonable policy decision,
non-compliant retention, or a bug.

| folder | app | owner |
|---|---|---|
| [`ghost/`](ghost/) | Ghost 5 (Node.js + MySQL 8) | Khushi |
| `discourse/` | Discourse (Rails + PostgreSQL + Redis) | Astika |

The canary-token format is shared across both apps; see
[`ghost/workload/canary.py`](ghost/workload/canary.py) (app code `gh` for Ghost, `dc` for Discourse).
