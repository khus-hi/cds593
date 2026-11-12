"""Canary-token design (shared format, meant to be reused for Discourse).

A token looks like   cnry-gh-a-pt-3f9c1e   but is written without separators:

    cnry  gh   a     pt    3f9c1e
    |     |    |     |     +-- 6 random hex chars (unique per run)
    |     |    |     +-------- data-type code (see DATA_TYPES)
    |     |    +-------------- user letter (a, b, m, n, ...)
    |     +------------------- app code: gh = Ghost, dc = Discourse
    +------------------------- fixed prefix, never occurs in real data

Design choices:
  * lowercase a-z0-9 only, so the token survives slugification, case folding,
    URL encoding, JSON/HTML escaping and Lexical/Mobiledoc serialisation unchanged;
  * no separators, so a slug like "my-cnryghapt3f9c1e-post" still contains it verbatim;
  * every (user, data type) pair gets its own token, so any hit tells us *whose*
    data of *which kind* survived, not just "something survived".

Besides tokens, the scanner also searches for each user's identifiers that the
app generates itself (internal id, uuid, email), which cannot carry a canary.
"""
import json
import secrets

PREFIX = "cnry"

DATA_TYPES = {
    "nm": "display name",
    "em": "email address",
    "bi": "profile bio",
    "lo": "profile location",
    "ws": "profile website",
    "pi": "profile image upload (filename)",
    "ci": "cover image upload (filename)",
    "pt": "published post title",
    "pb": "published post body",
    "rv": "earlier post revision (text later edited away)",
    "dr": "draft post body",
    "pg": "page body",
    "ca": "co-authored post body",
    "im": "image uploaded into a post (filename)",
    "cm": "comment body",
    "rp": "reply body",
    "nt": "admin note on member",
    "lb": "member label",
    "rf": "signup referrer URL (attribution)",
    "un": "name after self-service profile update",
}


class Registry:
    def __init__(self, app, run_id=None):
        self.app = app
        self.run_id = run_id or secrets.token_hex(2)
        self.tokens = {}       # token -> {user, type, desc}
        self.identifiers = {}  # value -> {user, kind}

    def token(self, user, dtype):
        assert dtype in DATA_TYPES, dtype
        tok = f"{PREFIX}{self.app}{user}{dtype}{secrets.token_hex(3)}"
        self.tokens[tok] = {"user": user, "type": dtype, "desc": DATA_TYPES[dtype]}
        return tok

    def identifier(self, user, kind, value):
        if value:
            self.identifiers[str(value)] = {"user": user, "kind": kind}

    def save(self, path):
        with open(path, "w") as f:
            json.dump({"app": self.app, "run_id": self.run_id,
                       "tokens": self.tokens, "identifiers": self.identifiers}, f, indent=2)
