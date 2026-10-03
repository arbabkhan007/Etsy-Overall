#!/usr/bin/env python3
"""Verify the arithmetic and claims in the crochet pattern drafts under patterns/.

A crochet pattern is mostly arithmetic: each round's stitch count must be reachable from the
previous round's increases and decreases. When that is wrong the buyer discovers it in round 9
and the review says so, so it is machine-checked here. What is NOT checked, and cannot be:
gauge, hand feel, and whether the finished shape reads as a reindeer. Those need yarn and a
hook - see TEST_STATUS in every file.

Grammar (the pattern files must be written in this dialect)
  R1  MR, 6 sc — 6                       opening magic ring
  R2  (inc) x6 — 12                       one increase in each stitch
  R3  (1 sc, inc) x6 — 18                 paired, xN repeat
  R4-R7  sc around — 24                   even rounds; also 'sc even', 'repeat around'
  R8  (2 sc, dec) x6 — 18                decrease round
  R9  dec x6 — 6                          decreases with no parens
  R10  3 sc in each st around — 18        expansion round
  Row 3  ch 1 and turn, inc, sc 7, inc — 11   flat rows (turning ch is count-neutral)
Lines that are notes, joins or finishing carry no em-dash count, so they are ignored.
Blocks of chain-worked motifs (stars, snowflakes, candy canes) say `freeform` and are skipped.

Checks
  1. every counted line CONSUMES exactly the previous count and PRODUCES the declared count
  2. ranges (R4-R7) must not change the count
  3. required sections: Materials, Gauge, Abbreviations (with UK), Finishing, Licence, TEST_STATUS
  4. declared quantities match the number of pattern blocks in the file
  5. no claims of testing that did not happen
  6. BABY_SAFE: yes must not reference eye hardware
Exits 1 on any drift.
"""
import re
import sys
import glob
import os
import os

# one round per match, and a line may hold several rounds separated by '/'
HEAD = re.compile(r"(?:R|Row|Rnd|Rows)\s*(\d+)(?:\s*-\s*(\d+))?\s+(.+?)\s*[—=]\s*(\d+)")
GROUP = re.compile(r"\(([^()]+)\)\s*x\s*(\d+)")
EACH = re.compile(r"(\d*)\s*(sc|tr|dc|hdc)\s+in each st")
EVEN = re.compile(r"\b(around|even)\b")
TAILCOUNT = re.compile(r"[—=]\s*\d+\s*[;,.]?\s*$")
LEAD = re.compile(r"^(\d+)\s+(.+)$")
TRAIL = re.compile(r"^(.+?)\s+(\d+)$")
VERBS = ("bl sc", "flo sc", "sl st", "dec", "inc", "sc", "tr", "dtr", "dc", "hdc")


def op_of(verb):
    v = verb.split(" ")[0].strip()
    if v in ("inc", "v"):
        return (1, 2)
    if v == "dec":
        return (2, 1)
    if v == "sl":
        return (0, 0)            # a join slip stitch is count-neutral in this dialect
    if v in ("sc", "tr", "dtr", "dc", "hdc"):
        return (1, 1)
    return None


FILLER = re.compile(r"^(?:work|then|continue|and|repeat|around|even|to)\b\s*", re.I)

def clause_counts(clause, mult):
    """(consumed, produced) for 'a sc, inc' style text, or None if it is prose."""
    counted = False
    cons = prod = 0
    for raw in (p.strip() for p in clause.split(",")):
        part = raw
        while True:
            q = FILLER.sub("", part).strip()
            if q == part:
                break
            part = q
        if not part:
            continue
        n, verb = 1, part
        m = LEAD.match(part)
        if m:
            n, verb = int(m.group(1)), m.group(2).strip()
        else:
            m2 = TRAIL.match(part)
            if m2 and not m2.group(1).startswith("ch") and op_of(m2.group(1)) and m2.group(2).isdigit():
                verb, n = m2.group(1).strip(), int(m2.group(2))
        if verb.startswith("ch"):
            continue                                  # turning chains are count-neutral
        w = op_of(verb)
        if w is None:
            continue
        c, p = w
        cons += c * n
        prod += p * n
        counted = True
    if not counted:
        return None
    return cons * mult, prod * mult


def parse(instr, prev):
    """Return (consumed, produced) for a whole round instruction, or None if unparseable."""
    explicit = re.search(r"(\d+\s*(?:sc|tr|dc|hdc))|(\(\s*[^()]+.*?\)\s*x\s*\d+)|\b(?:inc|dec)\b", instr)
    if not explicit and EVEN.search(instr) and prev is not None:
        return prev, prev                       # 'sc around' / 'work even' preserves the count
    cons = prod = 0
    seen = False
    for g in GROUP.finditer(instr):
        r = clause_counts(g.group(1), int(g.group(2)))
        if r:
            cons += r[0]
            prod += r[1]
            seen = True
    tail = GROUP.sub("", instr).strip()
    mult = 1
    mx = re.search(r"x\s*(\d+)\s*$", tail)
    if mx:
        mult = int(mx.group(1))
        tail = tail[:mx.start()].strip()
    m = EACH.search(tail)
    if m and prev is not None:
        k = int(m.group(1)) if m.group(1) else 3
        return prev, k * prev
    r = clause_counts(tail, mult)
    if r:
        cons += r[0]
        prod += r[1]
        seen = True
    if not seen and prev is not None and EVEN.search(instr):
        return prev, prev
    if not seen:
        return None
    return cons, prod


def check_block(name, body, errors):
    if "freeform" in body:
        return None
    lines = []
    for raw in body.splitlines():
        if raw.lower().startswith(("note:", "finish:", "freeform", "check:")):
            continue
        got = list(HEAD.finditer(raw))
        lines.extend(got)
        if not got and TAILCOUNT.search(raw):
            errors.append(f"{name}: '{raw.strip()[:38]}...' ends in a stitch count but has no "
                          f"R#/Row# label - a round line must be self-contained, never wrapped")
    if not lines:
        if "freeform" not in body and "**Base:**" not in body:
            errors.append(f"{name}: no counted rounds, no '**Base:**' and no 'freeform' marker")
        return None
    if len(lines) < 3 and "**Base:**" not in body and "freeform" not in body:
        errors.append(f"{name}: only {len(lines)} counted rounds - too short to be a real piece "
                      f"(declare '**Base:** Lxx' if this figure reuses one)")
    prev = None
    for m in lines:
        a, b, instr, want = m.group(1), m.group(2), m.group(3), int(m.group(4))
        reps = (int(b) - int(a) + 1) if b else 1
        if re.search(r"\bMR\b|\brm\b|\bch\s+\d+\s*,", instr):
            prev = None                      # new piece started inside this block
        r = parse(instr, prev)
        if r is None:
            errors.append(f"{name} {a}: cannot read stitch math from '{instr[:44]}'")
            continue
        cons, prod = r
        if prod != want:
            errors.append(f"{name} {a}: math gives {prod} sts, line declares {want}")
        if prev is not None and cons != prev:
            errors.append(f"{name} {a}: uses {cons} sts but previous round made {prev}")
        if b and prod != prev:
            errors.append(f"{name} {a}-{b}: a {reps}-round even stretch cannot change count ({prev} -> {prod})")
        prev = prod
    return prev


REQUIRED = ("## Materials", "## Gauge", "## Abbreviations", "## Finishing", "## Licence", "TEST_STATUS:")
# A pack cover is not a pattern: no rounds to recompute, no gauge of its own. What it can be held to
# is whether the files it promises actually exist - a stale cover page is a "only 3 of 5 patterns"
# refund, so the cross-check replaces the round check for these.
EXEMPT = ("START-HERE", "README", "CHANGELOG")
CLAIM = re.compile(r"\b(\d{1,3})\s+(?:mini\s+)?(motifs?|figures?|patterns?|pieces?|minis?|loveys?|stockings?)\b")
BAD_CLAIM = ("tested by", "proofed by", "tech edited", "testers", "hand-tested")


def block_heads(text):
    return [re.match(r"^#+\s+(\S+)", l).group(1)
            for l in text.splitlines() if re.match(r"^#{3,4}\s+[MFPL]\d{2}\b", l)]


def check_file(path, errors):
    text = open(path, encoding="utf-8").read()
    base = os.path.basename(path)
    heads = [h for h in block_heads(text) if h[0] in "FM"]
    parts = re.split(r"^(#{3,4}\s+\S+[^\n]*)$", text, flags=re.M)
    blocks = {}
    for i in range(1, len(parts), 2):
        m = re.match(r"^#+\s+(\S+)", parts[i])
        if m and re.match(r"^[MFPL]\d{2}$", m.group(1)):
            blocks[m.group(1)] = parts[i + 1]
    for req in REQUIRED:
        if req not in text:
            errors.append(f"{base}: missing required section '{req}'")
    if "## Abbreviations" in text and "UK" not in text:
        errors.append(f"{base}: abbreviations table must show UK terms too")
    low = text.lower()
    for bad in BAD_CLAIM:
        for m in re.finditer(r"([^\n]*)%s([^\n]*)" % re.escape(bad), low):
            if "not " in m.group(0) or "untested" in m.group(0) or "never" in m.group(0):
                continue
            errors.append(f"{base}: claims '{bad}' - {m.group(0).strip()[:60]!r}")
    if "BABY_SAFE: yes" in text and re.search(r"safety[- ]eye", text, re.I):
        errors.append(f"{base}: BABY_SAFE: yes but the file references eye hardware")
    for c in CLAIM.finditer(text):
        n, unit = int(c.group(1)), c.group(2).rstrip("s")
        if unit in ("motif", "figure", "mini", "piece") and len(heads) != n:
            errors.append(f"{base}: says '{n} {c.group(2)}' but the file holds {len(heads)} pattern blocks")
    for name, body in blocks.items():
        check_block(name, body, errors)
    return len(blocks)


def main():
    errors = []
    files = sorted(glob.glob("patterns/*.md"))
    covers = [f for f in files if os.path.splitext(os.path.basename(f))[0].upper().startswith(EXEMPT)]
    real = [f for f in files if f not in covers]
    for c in covers:
        txt = open(c).read()
        named = set(re.findall(r"`([A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)\.pdf`", txt))
        allmd = files + sorted(glob.glob("patterns/charts/*.md"))
        have = {os.path.splitext(os.path.basename(f))[0] for f in allmd}
        for want in sorted(named):
            if want not in have:
                errors.append(f"{os.path.basename(c)}: promises `{want}.pdf` but patterns/{want}.md does not exist")
        for f in real:
            stem = os.path.splitext(os.path.basename(f))[0]
            if stem not in txt:
                errors.append(f"{os.path.basename(c)}: {stem}.md is in the folder but not on the cover")
    files = real

    tot = sum(check_file(p, errors) for p in files)
    if errors:
        print(f"DRIFT in {len(errors)} place(s):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"{len(files)} file(s), {tot} pattern blocks - round math and claims consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
