"""Ghost workload: create test accounts with canary data, then (separately) delete them.

    python run_workload.py populate  out/registry.json     # set up site, users, content
    python run_workload.py delete    out/registry.json     # delete staff user A and member M

Accounts
  staff   owner  site owner (never deleted)
          a      Author  -> DELETED   (staff-account deletion experiment)
          b      Author, co-author with A, stays active
  members m      member  -> DELETED   (member-account deletion experiment)
          n      member, replies to M and is replied to by M, stays active
          p      member, likes M's comment, stays active
"""
import json
import sys
import time

from canary import Registry
from ghost_client import (ADMIN, GHOST, Member, Staff, find_link, lexical, wait_for_mail)
import requests

OWNER_EMAIL = "owner@example.com"
PASSWORD = "tq8-Vexl-ruby-Zoom-41"


def setup_site():
    s = requests.Session()
    s.headers.update({"Origin": GHOST})
    r = s.get(ADMIN + "/authentication/setup/")
    if not r.json()["setup"][0]["status"]:
        r = s.post(ADMIN + "/authentication/setup/", json={"setup": [{
            "name": "Site Owner", "email": OWNER_EMAIL, "password": PASSWORD, "blogTitle": "Audit Blog"}]})
        r.raise_for_status()
    owner = Staff(OWNER_EMAIL, PASSWORD)
    # Turn on native comments so members can comment (off by default).
    owner.put("/settings/", {"settings": [{"key": "comments_enabled", "value": "all"}]})
    return owner


def invite_staff(owner, reg, user, role_name):
    email_tok = reg.token(user, "em")
    name_tok = reg.token(user, "nm")
    email = f"{email_tok}@example.com"
    name = f"Test {name_tok}"
    roles = owner.get("/roles/?permissions=assign")["roles"]
    role_id = next(r["id"] for r in roles if r["name"] == role_name)
    owner.post("/invites/", {"invites": [{"email": email, "role_id": role_id}]})
    body = wait_for_mail(email, "/ghost/signup/")
    link = find_link(body, r"http://localhost:2368/ghost/signup/[^\s\"'<>/]+")
    # The link carries the invite token in URL-safe base64 form; undo that.
    b64 = link.rsplit("/", 1)[1]
    token = b64.replace("-", "+").replace("_", "/") + "=" * (-len(b64) % 4)
    r = requests.post(ADMIN + "/authentication/invitation/", headers={"Origin": GHOST}, json={
        "invitation": [{"token": token, "email": email, "name": name, "password": PASSWORD}]})
    r.raise_for_status()
    st = Staff(email, PASSWORD)
    reg.identifier(user, "user id", st.me["id"])
    reg.identifier(user, "email", email)
    return st, email


def populate(reg_path):
    reg = Registry("gh")
    owner = setup_site()

    # ---------------- staff user A (to be deleted) and B ----------------
    a, a_email = invite_staff(owner, reg, "a", "Author")
    b, _ = invite_staff(owner, reg, "b", "Author")

    pi = a.upload_image(f"{reg.token('a', 'pi')}.png", "profile_image")
    ci = a.upload_image(f"{reg.token('a', 'ci')}.png")
    a.put(f"/users/{a.me['id']}/", {"users": [{
        "bio": f"Bio {reg.token('a', 'bi')}",
        "location": f"City {reg.token('a', 'lo')}",
        "website": f"https://{reg.token('a', 'ws')}.example.org",
        "profile_image": pi, "cover_image": ci}]})

    # A writes a post, saves an earlier revision, then edits the revision text away.
    img = a.upload_image(f"{reg.token('a', 'im')}.png")
    title_tok, body_tok, rev_tok = reg.token("a", "pt"), reg.token("a", "pb"), reg.token("a", "rv")
    post = a.post("/posts/?formats=lexical", {"posts": [{
        "title": f"Post {title_tok}", "lexical": lexical(f"First draft {rev_tok}", f"Body {body_tok}"),
        "status": "draft", "authors": [{"id": a.me["id"]}]}]})["posts"][0]
    time.sleep(1)
    post = a.put(f"/posts/{post['id']}/?formats=lexical&save_revision=1", {"posts": [{
        "lexical": lexical(f"Body {body_tok}", image_url=img),
        "updated_at": post["updated_at"]}]})["posts"][0]
    # Authors cannot publish; the owner publishes A's post (normal editorial flow).
    post = owner.get(f"/posts/{post['id']}/")["posts"][0]
    post = owner.put(f"/posts/{post['id']}/", {"posts": [{
        "status": "published", "updated_at": post["updated_at"]}]})["posts"][0]
    reg.identifier("a", "post id", post["id"])

    # A's unpublished draft.
    draft = a.post("/posts/?formats=lexical", {"posts": [{
        "title": "Draft", "lexical": lexical(f"Draft {reg.token('a', 'dr')}"), "status": "draft",
        "authors": [{"id": a.me["id"]}]}]})["posts"][0]
    reg.identifier("a", "draft post id", draft["id"])

    # Co-authored post (A and B), published by owner.
    co = owner.post("/posts/?formats=lexical", {"posts": [{
        "title": "Co-authored", "lexical": lexical(f"Joint {reg.token('a', 'ca')}"), "status": "published",
        "authors": [{"id": b.me["id"]}, {"id": a.me["id"]}]}]})["posts"][0]

    # A asks for a password reset (produces mail addressed to A).
    requests.post(ADMIN + "/authentication/password_reset/", headers={"Origin": GHOST},
                  json={"password_reset": [{"email": a_email}]})

    # ---------------- members M (to be deleted), N, P ----------------
    members = {}
    for u in ("m", "n", "p"):
        email = f"{reg.token(u, 'em')}@example.com"
        mem = Member(email, f"Reader {reg.token(u, 'nm')}", f"https://{reg.token(u, 'rf')}.example.net/")
        members[u] = mem
        reg.identifier(u, "email", email)
        reg.identifier(u, "member uuid", mem.me["uuid"])

    m, n, p = members["m"], members["n"], members["p"]
    # Member ids come from the Admin API. List all members rather than filtering by
    # email, so the workload itself never writes emails into request URLs / logs.
    all_members = owner.get("/members/?limit=all")["members"]
    for u, mem in members.items():
        row = next(x for x in all_members if x["email"] == mem.email)
        mem.id = row["id"]
        reg.identifier(u, "member id", row["id"])

    m.api("PUT", "/member/", {"name": f"Renamed {reg.token('m', 'un')}"})
    owner.put(f"/members/{m.id}/", {"members": [{
        "note": f"Note {reg.token('m', 'nt')}", "labels": [{"name": f"label {reg.token('m', 'lb')}"}]}]})

    c_m = m.api("POST", "/comments/", {"comments": [{
        "post_id": post["id"], "html": f"<p>Comment {reg.token('m', 'cm')}</p>"}]})["comments"][0]
    c_n = n.api("POST", "/comments/", {"comments": [{
        "post_id": post["id"], "html": f"<p>Comment {reg.token('n', 'cm')}</p>"}]})["comments"][0]
    r_n = n.api("POST", "/comments/", {"comments": [{
        "post_id": post["id"], "parent_id": c_m["id"], "html": f"<p>Reply {reg.token('n', 'rp')}</p>"}]})["comments"][0]
    r_m = m.api("POST", "/comments/", {"comments": [{
        "post_id": post["id"], "parent_id": c_n["id"], "html": f"<p>Reply {reg.token('m', 'rp')}</p>"}]})["comments"][0]
    p.api("POST", f"/comments/{c_m['id']}/like/")
    m.api("POST", f"/comments/{c_n['id']}/like/")
    for cid in (c_m["id"], r_m["id"]):
        reg.identifier("m", "comment id", cid)

    reg.extra = {"a_id": a.me["id"], "m_id": m.id, "post_id": post["id"], "post_url": post["url"],
                 "co_post_id": co["id"], "a_slug": a.me["slug"], "images": [pi, ci, img]}
    data = reg.__dict__
    with open(reg_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"populated: {len(reg.tokens)} tokens, {len(reg.identifiers)} identifiers -> {reg_path}")


def delete(reg_path):
    reg = json.load(open(reg_path))
    owner = Staff(OWNER_EMAIL, PASSWORD)
    t0 = time.time()
    owner.delete(f"/users/{reg['extra']['a_id']}/")      # staff account deletion (Settings > Staff > Delete user)
    owner.delete(f"/members/{reg['extra']['m_id']}/")    # member deletion (Members > Delete member)
    reg["deleted_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0))
    reg["deleted"] = ["a", "m"]
    json.dump(reg, open(reg_path, "w"), indent=2)
    print("deleted staff user a and member m at", reg["deleted_at"])


if __name__ == "__main__":
    {"populate": populate, "delete": delete}[sys.argv[1]](sys.argv[2])
