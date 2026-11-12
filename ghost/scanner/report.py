"""Compare scans and summarise what survives for the deleted users.

    python report.py <registry.json> <scan1.json> <scan2.json> ... > summary.md

For every deleted user, prints (a) a layer x phase matrix of how many distinct
needles (tokens + identifiers) are present, and (b) the surviving locations
per needle in the last scan, plus the metrics from the proposal.
"""
import json
import sys
from collections import defaultdict

LAYERS = ["db", "binlog", "innodb_raw", "content", "stdout", "mail", "public_web", "admin_api"]


def main():
    reg = json.load(open(sys.argv[1]))
    scans = [json.load(open(p)) for p in sys.argv[2:]]
    deleted = reg.get("deleted", [])
    out = []
    w = out.append

    for user in deleted:
        toks = {t: m for t, m in reg["tokens"].items() if m["user"] == user}
        ids = {v: m for v, m in reg["identifiers"].items() if m["user"] == user}
        import hashlib
        for v, m in list(ids.items()):
            if m["kind"] == "email":
                ids[hashlib.md5(v.lower().encode()).hexdigest()] = {"user": user, "kind": "gravatar md5(email)"}
        needles = set(toks) | set(ids)
        w(f"\n## User `{user}`: {len(toks)} canary tokens, {len(ids)} identifiers\n")
        w("Distinct needles found, per layer and phase:\n")
        w("| layer | " + " | ".join(s["label"] for s in scans) + " |")
        w("|---|" + "---|" * len(scans))
        per = []
        for s in scans:
            d = defaultdict(set)
            for h in s["hits"]:
                if h["needle"] in needles:
                    d[h["layer"]].add(h["needle"])
            per.append(d)
        for layer in LAYERS:
            w(f"| {layer} | " + " | ".join(str(len(d[layer])) for d in per) + " |")
        anyl = [set().union(*d.values()) if d else set() for d in per]
        w("| **any layer** | " + " | ".join(str(len(a)) for a in anyl) + " |")

        # Metrics on the last scan
        last = scans[-1]
        tok_found = {h["needle"] for h in last["hits"] if h["needle"] in toks}
        types = sorted({m["type"] for m in toks.values()})
        removed = [t for t in types if not any(toks[n]["type"] == t for n in tok_found)]
        w(f"\nAfter deletion ({last['label']}): {len(tok_found)}/{len(toks)} canary tokens still observable "
          f"somewhere; {len(removed)}/{len(types)} data types completely removed "
          f"({', '.join(removed) or 'none'}).\n")

        w("Where each surviving needle is, in the last scan:\n")
        w("| needle | what | locations |")
        w("|---|---|---|")
        locs = defaultdict(list)
        for h in last["hits"]:
            if h["needle"] in needles:
                locs[h["needle"]].append(f"{h['layer']}:{h['location']}")
        for n in sorted(locs, key=lambda n: (n not in toks, n)):
            what = toks[n]["desc"] if n in toks else ids[n]["kind"]
            w(f"| `{n}` | {what} | {'; '.join(sorted(locs[n]))} |")

    print("\n".join(out))


if __name__ == "__main__":
    main()
