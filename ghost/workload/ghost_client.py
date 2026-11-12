"""Small helpers for driving Ghost's Admin API, Members API and Mailpit."""
import re
import struct
import time
import zlib
from urllib.parse import unquote

import requests

GHOST = "http://localhost:2368"
ADMIN = GHOST + "/ghost/api/admin"
MAILPIT = "http://localhost:8025/api/v1"


def png_bytes(seed: str) -> bytes:
    """A valid 8x8 PNG whose pixels depend on `seed`, so every upload is a distinct file."""
    h = abs(hash(seed))
    rgb = bytes([(h >> 0) & 255, (h >> 8) & 255, (h >> 16) & 255])
    raw = b"".join(b"\x00" + rgb * 8 for _ in range(8))

    def chunk(kind, data):
        c = kind + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 8, 8, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


class Staff:
    """A logged-in staff (admin/editor/author) session."""

    def __init__(self, email, password):
        self.s = requests.Session()
        self.s.headers.update({"Origin": GHOST, "Accept-Version": "v5.0"})
        r = self.s.post(ADMIN + "/session/", json={"username": email, "password": password})
        r.raise_for_status()
        self.me = self.get("/users/me/")["users"][0]

    def _check(self, r):
        if r.status_code >= 400:
            raise RuntimeError(f"{r.request.method} {r.url} -> {r.status_code}: {r.text[:300]}")
        return r.json() if r.content else {}

    def get(self, path, **kw):
        return self._check(self.s.get(ADMIN + path, **kw))

    def post(self, path, body=None, **kw):
        return self._check(self.s.post(ADMIN + path, json=body, **kw))

    def put(self, path, body, **kw):
        return self._check(self.s.put(ADMIN + path, json=body, **kw))

    def delete(self, path, **kw):
        return self._check(self.s.delete(ADMIN + path, **kw))

    def upload_image(self, filename, purpose="image"):
        files = {"file": (filename, png_bytes(filename), "image/png")}
        r = self.s.post(ADMIN + "/images/upload/", files=files, data={"purpose": purpose})
        return self._check(r)["images"][0]["url"]


def lexical(*paragraphs, image_url=None):
    """Minimal Lexical document (Ghost 5's editor format)."""
    children = [{
        "type": "paragraph", "version": 1, "direction": "ltr", "format": "", "indent": 0,
        "children": [{"type": "extended-text", "version": 1, "text": p, "detail": 0,
                      "format": 0, "mode": "normal", "style": ""}],
    } for p in paragraphs]
    if image_url:
        children.append({"type": "image", "version": 1, "src": image_url, "alt": "", "caption": "",
                         "title": "", "width": 8, "height": 8, "cardWidth": "regular", "href": ""})
    import json
    return json.dumps({"root": {"type": "root", "version": 1, "direction": "ltr", "format": "",
                                "indent": 0, "children": children}})


# ---------------------------------------------------------------- mail ----

def wait_for_mail(to_addr, contains="", timeout=30):
    """Return the text of the newest Mailpit message to `to_addr` (optionally containing a string)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        msgs = requests.get(MAILPIT + "/search", params={"query": f"to:{to_addr}"}).json()["messages"]
        for m in msgs:
            full = requests.get(f"{MAILPIT}/message/{m['ID']}").json()
            body = full.get("Text", "") + full.get("HTML", "")
            if contains in body:
                return body
        time.sleep(1)
    raise TimeoutError(f"no mail to {to_addr} containing {contains!r}")


def find_link(body, pattern):
    m = re.search(pattern, body)
    if not m:
        raise ValueError(f"link {pattern} not found")
    return unquote(m.group(0)).replace("&amp;", "&")


# -------------------------------------------------------------- members ----

class Member:
    """A signed-in member session (signup through the real magic-link flow)."""

    def __init__(self, email, name, referrer_url):
        self.email = email
        self.s = requests.Session()
        self.s.headers.update({"Origin": GHOST})
        url_history = [{"path": "/", "time": int(time.time() * 1000),
                        "referrerSource": "audit", "referrerMedium": None,
                        "referrerUrl": referrer_url}]
        r = self.s.post(GHOST + "/members/api/send-magic-link/", json={
            "email": email, "emailType": "signup", "name": name, "urlHistory": url_history})
        if r.status_code >= 400:
            raise RuntimeError(f"magic link -> {r.status_code}: {r.text[:300]}")
        body = wait_for_mail(email, "token=")
        link = find_link(body, r"http://localhost:2368/members/\?token=[^\s\"'<>]+")
        self.s.get(link, allow_redirects=True)
        self.me = self.api("GET", "/member/")

    def api(self, method, path, body=None):
        r = self.s.request(method, GHOST + "/members/api" + path, json=body)
        if r.status_code >= 400:
            raise RuntimeError(f"{method} {path} -> {r.status_code}: {r.text[:300]}")
        return r.json() if r.content else {}
