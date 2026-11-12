#!/bin/sh
# Wipe all state and start a fresh Ghost stack; waits until Ghost answers.
set -e
cd "$(dirname "$0")"
COMPOSE="docker compose -f docker-compose.yml"
[ "$PATCHED" = 1 ] && COMPOSE="$COMPOSE -f docker-compose.patched.yml"
$COMPOSE down -v >/dev/null 2>&1 || true
rm -rf state
mkdir -p state/mysql state/content state/mail
$COMPOSE up -d --build
until curl -sf -o /dev/null http://localhost:2368/ghost/api/admin/site/; do sleep 2; done
echo "Ghost is up"
