#!/bin/sh
# Full Ghost deletion audit: fresh stack -> workload -> scan -> delete -> scans over time.
#   ./run_audit.sh [results-dir] [wait-seconds-before-t2]
set -e
cd "$(dirname "$0")"
OUT=${1:-results/run}; WAIT=${2:-600}
mkdir -p "$OUT"
harness/reset.sh
python3 workload/run_workload.py populate "$OUT/registry.json"
sleep 15   # let async work (emails, events) settle before the baseline
python3 scanner/scan.py "$OUT/registry.json" t0-before "$OUT/scan-t0-before.json"
python3 workload/run_workload.py delete "$OUT/registry.json"
python3 scanner/scan.py "$OUT/registry.json" t1-immediate "$OUT/scan-t1-immediate.json"
sleep "$WAIT"   # background jobs, InnoDB purge, log flushes
python3 scanner/scan.py "$OUT/registry.json" t2-after-jobs "$OUT/scan-t2-after-jobs.json"
(cd harness && docker compose restart mysql >/dev/null && docker compose restart ghost >/dev/null)
until curl -sf -o /dev/null http://localhost:2368/ghost/api/admin/site/; do sleep 2; done
python3 scanner/scan.py "$OUT/registry.json" t3-after-restart "$OUT/scan-t3-after-restart.json"
python3 scanner/report.py "$OUT/registry.json" "$OUT"/scan-t0-before.json "$OUT"/scan-t1-immediate.json \
    "$OUT"/scan-t2-after-jobs.json "$OUT"/scan-t3-after-restart.json > "$OUT/summary.md"
echo "done -> $OUT/summary.md"
