# Ghost deletion audit (Khushi's part of "What Survives Account Deletion?")

Reproducible audit of what Ghost 5.130 (Node.js + MySQL 8) leaves behind after a staff
user and a member are deleted through Ghost's own delete buttons.

## Run it

Needs Docker and Python 3 with `requests`, `mysql-replication`, `cryptography`
(`pip install requests mysql-replication cryptography`).

    ./run_audit.sh results/myrun 600                 # fresh stack, workload, scans at 4 points in time
    PATCHED=1 ./run_audit.sh results/patched 600     # same, on the fixed Ghost build

`results/myrun/summary.md` holds the per-layer tables. Takes ~12 minutes.

## Layout

| path | what |
|---|---|
| `harness/docker-compose.yml` | Ghost 5 + MySQL 8 (defaults, binlog on) + Mailpit; all state bind-mounted under `harness/state/` |
| `harness/reset.sh` | wipe state and start a fresh stack |
| `workload/canary.py` | canary-token format (shared design, app code `gh`/`dc`) |
| `workload/run_workload.py` | `populate`: owner + staff A, B + members M, N, P with canary data; `delete`: deletes A and M |
| `scanner/scan.py` | scans 8 layers: db, binlog, innodb_raw, content, stdout, mail, public_web, admin_api |
| `scanner/report.py` | per-user, per-layer, per-phase tables + proposal metrics |
| `results/baseline/` | the reference run on unmodified Ghost (registry, 4 scans, summary) |
| `results/patched/` | the same audit on Ghost with the fixes |
| `CLASSIFICATION.md` | every surviving trace classified as policy / non-compliant / bug |
| `fixes/` | patch for the bugs and non-compliant traces, plus the patched image build |

## Scan phases

t0 before deletion · t1 right after · t2 after 10 min (background jobs, InnoDB purge) ·
t3 after restarting Ghost and MySQL. The proposal's 24 h scan has not been run yet:
re-run `scanner/scan.py <registry> t4-24h <out>` on a stack left running for a day.

## Notes

* `security__staffDeviceVerification=false` and `server__host=0.0.0.0` are the only
  departures from the official image defaults (needed for scripted logins / no IPv6).
* The workload never puts emails into request URLs, so log hits come from Ghost itself.
