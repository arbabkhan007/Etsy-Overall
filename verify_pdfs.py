#!/usr/bin/env python3
"""Prove the exported PDFs match their markdown - the grids included.

verify_patterns.py checks the arithmetic of the pattern. This checks the artefact you actually
deliver: that every chart cell landed on the page where the markdown says it should. A stitch chart
is the worst possible place for a silent layout bug, because nobody can tell from the text dump that
a row shifted - only someone crocheting row 6 of the letter W will, at 11pm, with the pattern on
their phone and a half-finished stocking in their lap.

    python3 make_pdfs.py && python3 verify_pdfs.py

Needs pymupdf (pip install pymupdf); skipped gracefully if it is not installed, because the build
box might not have it and a missing audit tool must not fail a pattern release.
"""
import glob, os, re, sys

FOREST = (31 / 255, 70 / 255, 52 / 255)
TOL = 0.03


def expected(md_path):
    """letter/number -> grid of 0/1 rows, from the pipe tables in the chart markdown."""
    out, name = {}, None
    for ln in open(md_path):
        m = re.match(r"^##\s+(.+)$", ln)
        if m:
            name = m.group(1).strip(); out[name] = []; continue
        if ln.startswith("|") and "`" in ln:
            out[name].append([1 if c.strip("` ") == "#" else 0 for c in ln.strip().strip("|").split("|")])
    return {k: v for k, v in out.items() if v}


def rendered(pdf_path):
    """Read the grids back off the page as they are actually built: each chart is a vertical stack of
    cell rows, and the only place a chart ends is the gap before the next heading. So the rows are
    grouped by y-run, not by cell adjacency - a two-digit number has a six-cell blank gutter inside
    it, and any proximity rule either fuses neighbouring letters or splits that digit in half. Both
    of those mistakes happened here before this sentence did."""
    try:
        import pymupdf
    except ImportError:
        return None
    doc, grids = pymupdf.open(pdf_path), []
    for page in doc:
        cells = []
        for d in page.get_drawings():
            r, f = d["rect"], d.get("fill")
            if f and 4 < r.width < 30 and 4 < r.height < 30 \
               and max(abs(a - b) for a, b in zip(f, FOREST)) <= TOL:
                cells.append((round(r.y0, 2), round(r.x0, 2), r.width))
        if not cells:
            continue
        cw = min(c[2] for c in cells)
        rows = {}
        for y, x, _ in cells:
            rows.setdefault(y, []).append(x)
        ys = sorted(rows)
        runs, cur = [], [ys[0]]
        for a, b in zip(ys, ys[1:]):
            if b - a <= cw * 1.4:
                cur.append(b)
            else:
                runs.append(cur); cur = [b]
        runs.append(cur)
        runsets = [set(r) for r in runs]
        for rs in runsets:
            pts = [(y, x) for y, xs in rows.items() if y in rs for x in xs]
            minx = min(x for _, x in pts); miny = min(y for y, _ in pts)
            at = {(round((y - miny) / cw), round((x - minx) / cw)): 1 for y, x in pts}
            nr = max(r for r, _ in at) + 1
            nc = max(c for _, c in at) + 1
            grids.append([[at.get((r, c), 0) for c in range(nc)] for r in range(nr)])
    doc.close()
    return grids


def crop(m):
    """Crop to the ink on all four sides, on both sides of every comparison: the page only draws the
    filled cells, so the empty margin of the source grid is not something the PDF can show."""
    rows = [r for r in m if any(r)]
    if not rows:
        return [""]
    keep = [c for c in range(len(rows[0])) if any(r[c] for r in rows)]
    width = (max(keep) - min(keep) + 1) if keep else 0
    return ["".join(str(v) for v in r[min(keep):min(keep) + width]) for r in rows] if keep else [""]


def main():
    md = {os.path.splitext(os.path.basename(p))[0]: expected(p)
          for p in sorted(glob.glob("patterns/charts/*.md"))}
    if not md:
        print("no chart markdown found"); return 1
    problems, checked = [], 0
    for stem, want in md.items():
        pdf = f"dist/patterns/{stem}.pdf"
        if not os.path.exists(pdf):
            problems.append(f"{stem}: no exported PDF (run make_pdfs.py)")
            continue
        got = rendered(pdf)
        if got is None:
            print(f"{stem}.pdf: pymupdf not installed - geometry audit skipped"); return 0
        gm = [crop(g) for g in got]
        for name, grid in want.items():
            g = crop(grid)
            checked += 1
            if g not in gm:
                near = next((x for x in gm if len(x) == len(g)), None)
                det = ""
                if near:
                    bad = [i for i, (a, b) in enumerate(zip(g, near)) if a != b]
                    det = f"; closest grid differs on rows {bad[:4]}"
                problems.append(f"{stem}: `{name}` is not on the page as written "
                                f"(expected {len(g)}x{len(g[0])} rows{det})")
    for f in sorted(glob.glob("patterns/F*.md")) + ["patterns/START-HERE.md"]:
        stem = os.path.splitext(os.path.basename(f))[0]
        p = f"dist/patterns/{stem}.pdf"
        if not os.path.exists(p):
            problems.append(f"{stem}: missing PDF")
        elif os.path.getsize(p) < 6000:
            problems.append(f"{stem}: PDF is {os.path.getsize(p)}B - too small to be the whole pattern")
    if problems:
        print(f"DRIFT in {len(problems)} place(s):")
        for x in problems:
            print("  -", x)
        return 1
    print(f"PDFs consistent with source: {len(md)} chart files ({checked} grids), every grid drawn "
          f"where the markdown says")
    return 0


if __name__ == "__main__":
    sys.exit(main())
