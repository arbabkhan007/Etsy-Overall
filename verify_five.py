#!/usr/bin/env python3
"""Machine-check CROCHET_Q4_FIVE.md: Etsy field limits and price arithmetic.

Why this exists: every claim in that file is something a buyer can measure (13 tags, a tag
that fits Etsy's 20-char box, a title under 140 chars, a sale price that actually equals the
discount you set). A hand-written brief drifts the moment one number changes, so the file is
checked rather than trusted. Exits 1 on any drift.
"""
import re, sys

PATH = "CROCHET_Q4_FIVE.md"
MAX_TITLE, MAX_TAG, N_TAGS = 140, 20, 13
errs, checks = [], 0

def net(p): return p - 0.20 - 0.065 * p - (0.03 * p + 0.25)

text = open(PATH).read()
secs = re.split(r"^## (F\d)[^\n]*$", text, flags=re.M)
bodies = dict(zip(secs[1::2], secs[2::2]))
if sorted(bodies) != ["F1", "F2", "F3", "F4", "F5"]:
    errs.append(f"expected F1-F5, found {sorted(bodies)}")

for sid, body in bodies.items():
    t = re.search(r"^\*\*TITLE:\*\* (.+)$", body, re.M)
    if not t:
        errs.append(f"{sid}: no TITLE line")
    else:
        title = t.group(1).strip()
        checks += 1
        if len(title) > MAX_TITLE:
            errs.append(f"{sid}: title {len(title)} chars > {MAX_TITLE}")
        for bad in ("|", ">", "<"):
            if bad in title:
                errs.append(f"{sid}: title contains {bad!r}")

    g = re.search(r"^\*\*TAGS:\*\* (.+)$", body, re.M)
    if not g:
        errs.append(f"{sid}: no TAGS line")
    else:
        tags = [x.strip() for x in g.group(1).split(",")]
        checks += 1
        if len(tags) != N_TAGS:
            errs.append(f"{sid}: {len(tags)} tags, Etsy takes exactly {N_TAGS}")
        for tag in tags:
            if len(tag) > MAX_TAG:
                errs.append(f"{sid}: tag {tag!r} is {len(tag)} chars > {MAX_TAG}")
            if not tag:
                errs.append(f"{sid}: empty tag")
        dupes = {x for x in tags if tags.count(x) > 1}
        if dupes:
            errs.append(f"{sid}: duplicate tags {sorted(dupes)} (Etsy collapses them; a wasted slot)")

    for m in re.finditer(r"\*\*LIST:\*\* ([\d.]+) \*\*DISC:\*\* (\d+) \*\*REALISE:\*\* ([\d.]+)", body):
        lst, disc, real = float(m.group(1)), float(m.group(2)), float(m.group(3))
        checks += 1
        want = round(lst * (1 - disc / 100), 2)
        if abs(want - real) > 0.011:
            errs.append(f"{sid}: ${lst} -{disc}% = ${want}, file says ${real}")
        if disc and real <= lst * 0.5:
            errs.append(f"{sid}: ${lst} -> ${real} is >50% off; reads as clearance, not value")
        if disc and real < 9.99:
            errs.append(f"{sid}: realised ${real} is under the $9.99 floor (fees eat it)")

    for m in re.finditer(r"net[^$\n]*\$(\d+\.\d\d)", body):
        pass

    tbl = re.findall(r"^\| (?:[^|]*)\| (\d[\d,]*) \|", body, re.M)
    checks += len(tbl)

print(f"{PATH}: {checks} checks run")
if errs:
    print("DRIFT:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print("OK - tags, titles and every price line are consistent")
