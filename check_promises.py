"""
NovalityStore — promise / spec cross-checker
===========================================

The one-star review that started all this was a *product* failure, not a marketing
failure: the photo promised arms the instructions did not produce. Copy drift is
the same bug wearing better clothes, so it gets a machine check instead of a
resolution.

What it does
  1. Reads the listing copy out of `listing_pack.py` (single source of truth).
  2. Reads the build specs out of `Q4_BUILD_BRIEFS.md`.
  3. Extracts every quantitative claim the buyer will be able to count
     (page counts, tab counts, item counts, sizes, video minutes).
  4. Fails if a claim has no matching spec, or if a count disagrees.

Run:  python3 check_promises.py        -> report
      python3 check_promises.py --quiet -> exit code only, for CI/pre-commit
Exit: 0 = copy and specs agree, 1 = you are about to ship a broken promise
"""

import re
import sys

import listing_pack as LP

BRIEF = "Q4_BUILD_BRIEFS.md"

# Claims we can verify mechanically. `pattern` pulls the number out of the copy;
# `expect` says how the brief must substantiate it.
COUNT_CHECKS = [
    # (label, regex on copy, how to count inside the brief section)
    ("PDF page count",   r"(\d+)-page",                 r"^\|\s*P\d+\s*\|"),
    ("spreadsheet tabs", r"(\d+)\s+tabs?\b",            r"^\|\s*`?\w[\w &/()\-]*`?\s*\|.*\|$"),
]
# Claims that only need to be *present* in the brief (n counts as "same number, nearby")
ITEM_CHECKS = [
    ("mini/ornament count",   r"(\d+)\s+(?:mini|miniature|amigurumi|ornament)", r"(?:mini|ornament|amigurumi)"),
    ("stocking count",        r"(\d+)\s+stocking",            r"stocking"),
    ("size/length count",     r"(\d+)\s+(?:sizes?|lengths?|finished sizes?)",   r"(?:size|length|version)"),
    ("variations offered",    r"(\d+)\s+(?:cuff |variations?|colourways?|colorways?)", r"(?:variation|cuff|colourway|colorway)"),
    ("holders / extras",      r"(\d+)\s+(?:place-card|napkin|pattern|holder)",   r"(?:place-card|napkin|holder)"),
    ("participants",          r"(\d+)[\s-]*(?:participants?|guests?|people)",    r"(?:participant|people|group)"),
    ("yardage ceiling",       r"under (\d+) yds",           r"yds|yardage"),
]


def sections(text: str) -> dict:
    """Split the brief into {listing_id: section_text} on '## <ID> ·' headings."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+([A-Z]\d+)\s*·", line)
        if m:
            if cur:
                out[cur] = "\n".join(buf)
            cur, buf = m.group(1), []
            continue
        if re.match(r"^#\s", line) and cur:      # a top-level heading ends a section
            out[cur] = "\n".join(buf); cur, buf = None, []
            continue
        if cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf)
    return out


def table_rows(section: str, header_pat: str) -> int:
    """Count data rows of the first markdown table whose header matches."""
    lines = section.splitlines()
    for i, ln in enumerate(lines):
        if re.search(header_pat, ln) and ln.strip().startswith("|"):
            n = 0
            for row in lines[i + 2:]:
                if not row.strip().startswith("|"):
                    break
                n += 1
            return n
    return 0


def count_rows(section: str, pat: str) -> int:
    return len([l for l in section.splitlines() if re.match(pat, l.strip())])


def num(n: str) -> str:
    """Regex that matches n only as a standalone integer.

    Without the lookarounds, '2.5 in stocking' satisfies a claim of '5 sizes' and
    the check passes for the wrong reason - the most dangerous kind of green light."""
    return rf"(?<![\d.]){n}(?![\d.])"


def copy_text(l: dict) -> str:
    return f"{l.get('title','')}\n{l.get('desc','')}"


def video_claims(txt: str):
    """Minute counts that are genuinely video promises.

    Scoped to the sentence containing 'video' or 'walkthrough', because
    '24-mini amigurumi' and '10-minute audit tab' are not video claims, and a
    checker that cries wolf on those gets ignored within a day."""
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", txt):
        if re.search(r"walkthrough|video", sent, re.I):
            out += re.findall(r"(\d+)\s*[- ]?min(?:ute)?s?\b", sent, re.I)
    return out


def main():
    brief = open(BRIEF, encoding="utf-8").read()
    secs = sections(brief)
    problems, checks_ok, unchecked = [], [], []

    for l in LP.LISTINGS:
        if not l.get("new"):
            continue                            # only new builds need a spec
        lid = l["id"]
        txt = copy_text(l)
        sec = secs.get(lid)
        if not sec:
            problems.append(f"{lid}: has listing copy but NO section in {BRIEF}")
            continue

        # 1. hard numeric checks: declared counts must equal the spec's rows
        m = re.search(r"(\d+)-page", txt)
        if m:
            claim, got = int(m.group(1)), count_rows(sec, r"^\|\s*P\d+\s*\|")
            if got == 0:
                problems.append(f"{lid}: copy promises a {claim}-page PDF, brief has no P# page plan")
            elif claim != got:
                problems.append(f"{lid}: copy promises {claim} pages, brief specs only {got}")
            else:
                checks_ok.append(f"{lid}: {claim}-page PDF == {got} page-plan rows")

        m = re.search(r"(\d+)\s+tabs?\b", txt, re.I)
        if m:
            claim, got = int(m.group(1)), table_rows(sec, r"^\|\s*(?:#\s*\|\s*)?Tab\b")
            if got == 0:
                problems.append(f"{lid}: copy promises {claim} tabs, brief has no tab table")
            elif claim != got:
                problems.append(f"{lid}: copy promises {claim} tabs, brief specs {got}")
            else:
                checks_ok.append(f"{lid}: {claim} tabs == {got} tab rows")

        for n in video_claims(txt):
            if re.search(num(n) + r"[^\n]{0,40}(?:min|video|walkthrough)"
                         r"|(?:video|walkthrough)[^\n]{0,40}" + num(n), sec, re.I):
                checks_ok.append(f"{lid}: {n}-minute video substantiated in brief")
            else:
                problems.append(f"{lid}: copy promises a {n}-minute walkthrough; the brief never specs one")

        # 2. soft checks: the number behind every countable claim must exist in the spec
        for label, cp, bp in ITEM_CHECKS:
            for cm in re.finditer(cp, txt, re.I):
                n = cm.group(1)
                # The number must sit IN the claim phrase ("5 sizes", "24 mini stockings"),
                # not merely near those words - otherwise '| P5 |' substantiates '5 sizes'
                # and the check goes green on a coincidence.
                near = re.search(num(n) + r"[^\n]{0,22}?(?:" + bp + ")", sec, re.I)
                if near:
                    checks_ok.append(f"{lid}: {label} '{n}' substantiated in brief")
                else:
                    problems.append(
                        f"{lid}: {label} claims {n}, but the brief never states "
                        f"“{n} … {'/'.join(re.findall(r'[a-z]+', bp)[:3])}” as a spec line")

        # 3. flag anything numeric in the copy the checker has no rule for, so blind
        #    spots are visible instead of silently passing
        known = set()
        for _, cp, _ in COUNT_CHECKS + ITEM_CHECKS:
            for mm in re.finditer(cp, txt, re.I):
                known.add(mm.group(1))
        for mm in re.finditer(r"(?<![\d.])(\d{1,4})(?![\d.])", txt):
            n = mm.group(1)
            ctx = txt[max(0, mm.start() - 34):mm.end() + 34].replace("\n", " ")
            if n in known or re.search(r"\b(in|ft|mm|yds|US|UK|A4|\d{4}|years? old)\b", ctx, re.I):
                continue
            if re.search(r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+", ctx):
                continue                      # calendar dates, not product counts
            if re.search(r"\b\d+\s*(?:minutes?|hours?)\s+(?:each|total|per)", ctx, re.I):
                continue                      # effort claims, not buyer-countable deliverables
            if n not in secs.get(lid, ""):
                unchecked.append(f"{lid}: unverified number '{n}' — \"{ctx.strip()[:72]}\"")

    print("=" * 96)
    print("PROMISE / SPEC CROSS-CHECK   listing copy  vs  Q4_BUILD_BRIEFS.md")
    print("=" * 96)
    print(f"substantiated claims : {len(checks_ok)}")
    print(f"problems             : {len(problems)}")
    print(f"unverified numbers   : {len(unchecked)}")
    print("-" * 96)
    for p in problems:
        print("  ✗", p)
    if unchecked and "--quiet" not in sys.argv:
        print("-" * 96)
        print("  numbers the checker has no rule for (fine if they are not buyer-countable):")
        for u in sorted(set(unchecked))[:18]:
            print("   ·", u)
    if checks_ok and "--quiet" not in sys.argv:
        print("-" * 96)
        for c in checks_ok:
            print("   ok", c)
    print("=" * 96)
    if problems:
        print("RESULT: FAIL — fix the brief or trim the copy. Never publish the mismatch.")
    else:
        print("RESULT: PASS — every countable promise in the new-build copy has a spec behind it.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
