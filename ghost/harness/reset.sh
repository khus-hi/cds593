#!/bin/sh
# Wipe all state and start a fresh Ghost stack; waits until Ghost answers.
set -e
cd "$(dirname "$0")"
docker compose down -v >/dev/null 2>&1 || true
rm -rf state
mkdir -p state/mysql state/content state/mail
docker compose up -d
until curl -sf -o /dev/null http://localhost:2368/ghost/api/admin/site/; do sleep 2; done
echo "Ghost is up"
