"""Trace scanner: look for every canary token and user identifier in every storage layer.

    python scan.py <registry.json> <label> <out.json>

Layers scanned (Ghost harness):
  db            logical dump of the live MySQL database, one row per line
  binlog        MySQL binary log, decoded row images (INSERT/UPDATE/DELETE)
  innodb_raw    raw bytes of InnoDB files: table spaces, system/undo tablespaces,
                redo log, doublewrite buffer (finds deleted-but-not-overwritten rows)
  content       Ghost content directory: file names and file contents
                (images, data/ exports and backups, logs, settings)
  stdout        Ghost container stdout/stderr (what `docker logs` / a log shipper keeps)
  mail          every message Ghost sent, as captured by Mailpit
  public_web    unauthenticated HTTP: home, RSS, sitemaps, author page, post page,
                uploaded image URLs, public comments API
  admin_api     what the Ghost admin UI shows: posts, users, members, history log
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "..", "harness", "state")
GHOST = "http://localhost:2368"
MAILPIT = "http://localhost:8025/api/v1"
MYSQL = "harness-mysql-1"
GHOST_CT = "harness-ghost-1"
OWNER = ("owner@example.com", "tq8-Vexl-ruby-Zoom-41")


def load_needles(reg):
    needles = {}
    for tok, meta in reg["tokens"].items():
        needles[tok] = {"user": meta["user"], "kind": "token:" + meta["type"]}
    for val, meta in reg["identifiers"].items():
        needles[val] = {"user": meta["user"], "kind": "id:" + meta["kind"]}
        if meta["kind"] == "email":
            # Ghost derives Gravatar URLs from md5(email); a surviving hash is a derived identifier.
            md5 = hashlib.md5(val.strip().lower().encode()).hexdigest()
            needles[md5] = {"user": meta["user"], "kind": "id:gravatar md5(email)"}
    return needles


class Hits:
    def __init__(self, needles):
        self.needles = needles
        self.hits = defaultdict(int)   # (layer, location, needle) -> count

    def scan_text(self, layer, location, text):
        low = text.lower()
        for n in self.needles:
            c = low.count(n.lower())
            if c:
                self.hits[(layer, location, n)] += c

    def scan_bytes(self, layer, location, data):
        for n in self.needles:
            c = data.count(n.encode())
            if c:
                self.hits[(layer, location, n)] += c

    def rows(self):
        return [{"layer": l, "location": loc, "needle": n, "count": c, **self.needles[n]}
                for (l, loc, n), c in sorted(self.hits.items())]


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, check=True).stdout


# ------------------------------------------------------------------ layers --

def scan_db(h):
    dump = sh(["docker", "exec", MYSQL, "mysqldump", "-uroot", "-prootpw", "--skip-extended-insert",
               "--no-create-info", "--skip-triggers", "ghost"]).decode("utf8", "replace")
    for line in dump.splitlines():
        m = re.match(r"INSERT INTO `([^`]+)`", line)
        if m:
            h.scan_text("db", m.group(1), line)


def scan_binlog(h):
    """Read every row event in the binary log (as a replica would) and attribute hits
    to the operation and table. A DELETE event carries the full before-image of the row."""
    from pymysqlreplication import BinLogStreamReader
    from pymysqlreplication.row_event import DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent
    first = sh(["docker", "exec", MYSQL, "mysql", "-uroot", "-prootpw", "-N", "-e",
                "SHOW BINARY LOGS"]).decode().split()[0]
    stream = BinLogStreamReader(
        connection_settings={"host": "127.0.0.1", "port": 3306, "user": "root", "passwd": "rootpw"},
        server_id=4242, blocking=False, resume_stream=True, log_file=first, log_pos=4,
        only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent])
    op = {WriteRowsEvent: "INSERT", UpdateRowsEvent: "UPDATE", DeleteRowsEvent: "DELETE"}
    for ev in stream:
        if ev.schema != "ghost":
            continue
        for row in ev.rows:
            h.scan_text("binlog", f"{op[type(ev)]} {ev.table}", repr(row))
    stream.close()


def scan_innodb_raw(h):
    base = os.path.join(STATE, "mysql")
    targets = []
    for root, _, files in os.walk(base):
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, base)
            if rel.startswith(("ghost/", "#innodb_redo", "undo_", "ibdata1", "#ib_")):
                targets.append((rel, p))
    for rel, p in targets:
        with open(p, "rb") as fh:
            h.scan_bytes("innodb_raw", rel, fh.read())


def scan_content(h):
    base = os.path.join(STATE, "content")
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ("themes", "public")]
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, base)
            top = rel.split(os.sep)[0]
            h.scan_text("content", f"{top}/ (file name)", rel)
            with open(p, "rb") as fh:
                h.scan_bytes("content", f"{top}/{f}" if top in ("data", "logs") else f"{top}/ (file body)",
                             fh.read())


def scan_stdout(h):
    out = subprocess.run(["docker", "logs", GHOST_CT], capture_output=True)
    h.scan_bytes("stdout", "docker logs ghost", out.stdout + out.stderr)


def scan_mail(h):
    msgs = requests.get(MAILPIT + "/messages", params={"limit": 1000}).json()["messages"]
    for m in msgs:
        raw = requests.get(f"{MAILPIT}/message/{m['ID']}/raw").content
        full = requests.get(f"{MAILPIT}/message/{m['ID']}").json()
        decoded = (full.get("Text", "") + full.get("HTML", "")).encode()
        h.scan_bytes("mail", f"mail: {m['Subject'][:60]}", raw + b"\n" + decoded)


def scan_public(h, reg):
    ex = reg["extra"]
    urls = ["/", "/rss/", "/sitemap.xml", "/sitemap-posts.xml", "/sitemap-pages.xml",
            "/sitemap-authors.xml", "/sitemap-tags.xml", f"/author/{ex['a_slug']}/",
            f"/author/{ex['a_slug']}/rss/", ex["post_url"].replace(GHOST, ""),
            f"/members/api/comments/post/{ex['post_id']}/"]
    for u in urls:
        try:
            r = requests.get(GHOST + u, timeout=20)
            if r.status_code == 200:
                h.scan_text("public_web", u, r.text)
        except requests.RequestException:
            pass
    # Uploaded files: is the file itself still served?
    for img in ex["images"]:
        path = img.replace(GHOST, "")
        r = requests.get(GHOST + path, timeout=20)
        if r.status_code == 200:
            h.scan_text("public_web", "uploaded image still served", path)


def scan_admin(h):
    s = requests.Session()
    s.headers.update({"Origin": GHOST, "Accept-Version": "v5.0"})
    s.post(GHOST + "/ghost/api/admin/session/", json={"username": OWNER[0], "password": OWNER[1]})
    for name, path in [("posts", "/posts/?limit=all&formats=lexical,html&filter=status:[draft,published]"),
                       ("pages", "/pages/?limit=all&formats=lexical"),
                       ("users", "/users/?limit=all"),
                       ("members", "/members/?limit=all&include=labels"),
                       ("labels", "/labels/?limit=all"),
                       ("tags", "/tags/?limit=all"),
                       ("history log", "/actions/?limit=all"),
                       ("member activity feed", "/members/events/?limit=all")]:
        r = s.get(GHOST + "/ghost/api/admin" + path, timeout=30)
        if r.status_code == 200:
            h.scan_text("admin_api", name, r.text)


def main():
    reg_path, label, out = sys.argv[1:4]
    reg = json.load(open(reg_path))
    h = Hits(load_needles(reg))
    for fn in (scan_db, scan_binlog, scan_innodb_raw, scan_content, scan_stdout, scan_mail, scan_admin):
        fn(h)
    scan_public(h, reg)
    result = {"label": label, "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "hits": h.rows()}
    json.dump(result, open(out, "w"), indent=1)
    print(f"{label}: {len(result['hits'])} (layer, location, needle) hits -> {out}")


if __name__ == "__main__":
    main()
