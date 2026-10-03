#!/usr/bin/env python3
"""Export the pattern markdown into the files Etsy delivers: real PDFs, plus an HTML fallback.

Why a parser in this repo instead of pandoc/Word: a pattern PDF is only worth paying for if the
rounds, the gauge table and the stitch charts survive the export intact. Any converter can silently
reflow a chart table into three columns per page and you will not notice until a buyer does. So the
structure is parsed once here and rendered twice - PDF when reportlab is installed, always HTML for
someone on a machine without it. Same blocks, same order, no markup left behind.

    python3 make_pdfs.py                      # dist/patterns/*.pdf + *.html + dist zip
    python3 make_pdfs.py patterns/F3*.md      # one file while you iterate

Fonts are the brand's DejaVu family when present, else the core PDF fonts, so the PDF never fails
because a ttf is missing on the box that builds it.
"""
import glob, html as H, os, re, sys, zipfile

CREAM, INK, FOREST, TERRA, MUTE, LINE = "#F5EFE6", "#262420", "#1F4634", "#C2643F", "#7A7265", "#D7CBB8"
FD = "/usr/share/fonts/truetype/dejavu"
META_KEYS = ("Product", "Sell as", "TEST_STATUS", "BABY_SAFE", "Pricing")
ROUNDS = re.compile(r"^(R\d|Row \d|Round \d|Ch\b|Arm |Ear |Leg |Wing |Petal |Crown |Face |Body |Centre |Head |Tail |Finish|Note)")


# ---------------------------------------------------------------- structure
def parse(md):
    """markdown -> blocks. Only the constructs the pattern files use: h1-h3, paragraphs, one-level
    lists, pipe tables, fenced blocks, and the bold-key front matter."""
    lines, blocks = md.split("\n"), []
    head_end = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
    meta, cur, title = [], None, None
    for ln in lines[:head_end]:
        if ln.startswith("# ") and title is None:
            title = ln[2:].strip(); continue
        m = re.match(r"^\*\*([A-Za-z _]+):\*\*\s*(.*)$", ln)
        if m:
            cur = [m.group(1), m.group(2).strip()]; meta.append(cur)
        elif cur and ln.strip():
            cur[1] = (cur[1] + " " + ln.strip()).strip()
    if title:
        blocks.append(("h1", title))          # title first: it is what the buyer reads when the
    if meta:                                  # file lands in their downloads folder
        blocks.append(("meta", meta))
    i = head_end
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            j, buf = i + 1, []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j]); j += 1
            blocks.append(("pre", "\n".join(buf))); i = j + 1; continue
        m = re.match(r"^(#{1,3})\s+(.*)$", ln)
        if m:
            blocks.append((f"h{len(m.group(1))}", m.group(2).strip())); i += 1; continue
        if ln.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not set(lines[i].replace("|", "").strip()) <= set("-: "):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append(("table", rows)); continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:].strip()); i += 1
            blocks.append(("ul", items)); continue
        if not ln.strip():
            i += 1; continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |```)", lines[i]):
            buf.append(lines[i].strip()); i += 1
        # A pattern paragraph is not prose. Markdown joins soft line breaks, and every round you
        # wrote on its own line - the one thing the whole file exists to be readable by - would come
        # out as a wall of text, so counted lines are re-split before they reach either emitter.
        counted = [b for b in buf if ROUNDS.match(b) or " — " in b]
        if len(counted) > 1:
            for b in buf:
                blocks.append(("rounds" if ROUNDS.match(b) or " — " in b else "p", b))
            continue
        txt = " ".join(buf)
        blocks.append(("rounds" if ROUNDS.match(txt) or " — " in txt else "p", txt))
    return blocks


# ---------------------------------------------------------------- html
CSS = f"""
@page {{ size: Letter; margin: 16mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{ background: {CREAM}; color: {INK}; margin: 0;
  font: 10.5pt/1.5 'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif; }}
main {{ max-width: 46em; margin: 0 auto; padding: 28px 34px 60px; }}
h1 {{ font-family: 'Futura', 'Trebuchet MS', sans-serif; color: {FOREST}; font-size: 25pt;
  line-height: 1.12; margin: .2em 0 .3em; }}
h2 {{ font-family: 'Futura', 'Trebuchet MS', sans-serif; color: {FOREST}; font-size: 14pt;
  margin: 1.9em 0 .5em; padding-bottom: .25em; border-bottom: 2px solid {TERRA}; break-after: avoid; }}
h3 {{ font-family: 'Futura', 'Trebuchet MS', sans-serif; color: {TERRA}; font-size: 11.5pt;
  margin: 1.5em 0 .35em; break-after: avoid; }}
p, li {{ orphans: 2; widows: 2; }}
ul {{ padding-left: 1.2em; }}
.meta {{ border: 1px solid {LINE}; background: #fff; padding: 10px 14px; border-radius: 6px;
  font: 9.5pt/1.5 'DejaVu Sans', 'Trebuchet MS', sans-serif; color: {MUTE}; }}
.meta b {{ color: {FOREST}; }}
table {{ border-collapse: collapse; width: 100%; margin: .7em 0 1em; font-size: 9.3pt; break-inside: avoid; }}
th {{ background: {FOREST}; color: {CREAM}; text-align: left; padding: 5px 8px;
  font-family: 'DejaVu Sans', sans-serif; font-size: 8.6pt; }}
td {{ border-bottom: 1px solid {LINE}; padding: 4px 8px; vertical-align: top; }}
tr:nth-child(even) td {{ background: rgba(255,255,255,.55); }}
td.chart, th.chart {{ text-align: center; padding: 1px 3px; }}
.x {{ color: {FOREST}; font-size: 11pt; }}
.dot {{ color: {LINE}; }}
code {{ font: 8.6pt/1.35 'DejaVu Sans Mono', 'Courier New', monospace; }}
pre {{ background: #fff; border: 1px solid {LINE}; border-radius: 6px; padding: 10px 12px;
  font: 8.4pt/1.3 'DejaVu Sans Mono', monospace; color: {FOREST}; white-space: pre;
  overflow-x: auto; break-inside: avoid; }}
.rounds {{ background: #fff; border-left: 3px solid {FOREST}; padding: 8px 12px; margin: .6em 0 1em;
  font: 9.4pt/1.55 'DejaVu Sans Mono', monospace; break-inside: avoid; }}
footer {{ position: fixed; bottom: 6mm; left: 0; right: 0; text-align: center;
  font: 7.6pt/1 'DejaVu Sans', sans-serif; color: {MUTE}; }}
@media print {{ main {{ max-width: none; padding: 0; }} }}
"""


def esc(s, to="html", face="Mono"):
    """One rule for both emitters, two tag vocabularies: bold is <b> either way, and a code span is
    <code> in the browser but a mono <font> in the PDF, naming the face that was actually registered.

    The replacements are lambdas, not backreferences, on purpose. "\1" inside a non-raw string is
    chr(1), which re.sub happily inserts - so every code span in the PDF silently became one
    invisible control character and the listing title vanished. A markup string that references a
    group can also re-interpret the text it wraps; a lambda can neither."""
    s = H.escape(s, quote=False)
    wrap = (lambda m: "<code>" + m.group(1) + "</code>") if to != "pdf" else (
        lambda m: f'<font face="{face}">' + m.group(1) + "</font>")
    s = re.sub(r"`([^`]+)`", wrap, s)
    return re.sub(r"\*\*([^*]+)\*\*", lambda m: "<b>" + m.group(1) + "</b>", s)



def chartable(rows):
    """A grid of single-char cells (the stitch charts) wants a different table than a materials list:
    centred, tight, and every '#' a filled square the eye can read at a glance."""
    body = rows[1:] if len(rows) > 1 else rows
    flat = [c.strip("` ") for r in body for c in r]
    return bool(flat) and all(len(c) == 1 and c in ".#" for c in flat)


def html_of(blocks):
    out = []
    for kind, val in blocks:
        if kind == "meta":
            out.append("<div class='meta'>" + "".join(
                f"<b>{H.escape(k)}:</b> {esc(v)}<br>" for k, v in val) + "</div>")
        elif kind in ("h1", "h2", "h3"):
            out.append(f"<{kind}>{esc(val)}</{kind}>")
        elif kind == "pre":
            out.append("<pre>" + H.escape(val, quote=False) + "</pre>")
        elif kind == "ul":
            out.append("<ul>" + "".join(f"<li>{esc(li)}</li>" for li in val) + "</ul>")
        elif kind == "table":
            ch = chartable(val)
            t = ["<table>"]
            for n, r in enumerate(val):
                tag = "th" if n == 0 else "td"
                cls = ' class="chart"' if ch else ""
                cells = []
                for c in r:
                    txt = c.strip("` ")
                    if ch and n > 0:
                        cells.append(f'<{tag}{cls}><span class="{"x" if txt == "#" else "dot"}">'
                                     f'{"&#9632;" if txt == "#" else "&#183;"}</span></{tag}>')
                    else:
                        cells.append(f"<{tag}{cls}>{esc(txt if ch else c)}</{tag}>")
                t.append("<tr>" + "".join(cells) + "</tr>")
            t.append("</table>"); out.append("\n".join(t))
        elif kind == "rounds":
            out.append(f'<div class="rounds">{esc(val)}</div>')
        else:
            out.append(f"<p>{esc(val)}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------- pdf
def fonts():
    """Register the brand's DejaVu family; fall back to the core 14 so a machine without the ttf
    still builds a readable PDF instead of crashing in the middle of an upload day."""
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        for n, f in (("Sans", "DejaVuSans.ttf"), ("SansB", "DejaVuSans-Bold.ttf"),
                     ("Mono", "DejaVuSansMono.ttf"), ("MonoB", "DejaVuSansMono-Bold.ttf")):
            pdfmetrics.registerFont(TTFont(n, os.path.join(FD, f)))
        # Without the family map, a <b> span inside a "Sans" paragraph makes reportlab hunt for a
        # Sans-Bold it cannot name and raises inside the paragraph parser, mid-build.
        pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="SansB", italic="Sans", boldItalic="SansB")
        pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="MonoB", italic="Mono", boldItalic="MonoB")
        return dict(body="Sans", bold="SansB", mono="Mono", serif="Sans")
    except Exception:
        return dict(body="Helvetica", bold="Helvetica-Bold", mono="Courier", serif="Times-Roman")


def pdf_of(blocks, path, footer):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import LETTER
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, KeepTogether,
                                        PageTemplate, Paragraph, Spacer, CondPageBreak, Table,
                                        TableStyle, XPreformatted)
    except ImportError:
        return None
    F = fonts()
    esc = lambda t: globals()['esc'](t, 'pdf', F['mono'])
    C = lambda v: colors.HexColor(v)
    CW = LETTER[0] - 2 * 46
    st = {
        "h1": ParagraphStyle("h1", fontName=F["bold"], fontSize=19, leading=22, textColor=C(FOREST), spaceAfter=2),
        "h2": ParagraphStyle("h2", fontName=F["bold"], fontSize=12.5, leading=15, textColor=C(FOREST), spaceBefore=11, spaceAfter=3),
        "h3": ParagraphStyle("h3", fontName=F["bold"], fontSize=10, leading=13, textColor=C(TERRA), spaceBefore=8, spaceAfter=2),
        "p": ParagraphStyle("p", fontName=F["body"], fontSize=9.2, leading=13.4, textColor=C(INK), spaceAfter=5),
        "li": ParagraphStyle("li", fontName=F["body"], fontSize=9.2, leading=13.2, textColor=C(INK),
                             leftIndent=11, spaceAfter=2.5),
        "rd": ParagraphStyle("rd", fontName=F["mono"], fontSize=8.5, leading=12.4, textColor=C(INK)),
        "pre": ParagraphStyle("pre", fontName=F["mono"], fontSize=8, leading=11.4, textColor=C(FOREST)),
        "m": ParagraphStyle("m", fontName=F["body"], fontSize=8.4, leading=12.6, textColor=C(MUTE)),
        "th": ParagraphStyle("th", fontName=F["bold"], fontSize=7.7, leading=10, textColor=C(CREAM)),
        "td": ParagraphStyle("td", fontName=F["body"], fontSize=8.2, leading=11, textColor=C(INK)),
        "cell": ParagraphStyle("cell", fontName=F["mono"], fontSize=8.4, leading=10, alignment=1),
    }

    def foot(canv, doc):
        canv.saveState()
        canv.setFont(F["body"], 7.2); canv.setFillColor(C(MUTE))
        canv.drawCentredString(LETTER[0] / 2, 26, footer)
        canv.drawRightString(LETTER[0] - 46, 26, f"page {doc.page}")
        canv.setStrokeColor(C(LINE)); canv.setLineWidth(0.6)
        canv.line(46, 36, LETTER[0] - 46, 36)
        canv.restoreState()

    doc = BaseDocTemplate(path, pagesize=LETTER, leftMargin=46, rightMargin=46,
                          topMargin=44, bottomMargin=44, title=blocks[0][1] if blocks[0][0] == "h1" else "pattern")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(46, 44, CW, LETTER[1] - 88, id="f")], onPage=foot)])

    def box(flow, border=None, bg="#FFFFFF", pad=8):
        t = Table([[flow]], colWidths=[CW])
        s = [("BACKGROUND", (0, 0), (-1, -1), C(bg)), ("LEFTPADDING", (0, 0), (-1, -1), pad),
             ("RIGHTPADDING", (0, 0), (-1, -1), pad), ("TOPPADDING", (0, 0), (-1, -1), 5),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
        if border:
            s += [("BOX", (0, 0), (-1, -1), 0.7, C(border))]
        if border == FOREST:
            s += [("LINEBEFORE", (0, 0), (0, -1), 2.6, C(FOREST)), ("LINEAFTER", (0, 0), (-1, -1), 0, C(bg))]
        t.setStyle(TableStyle(s + [("LEFTPADDING", (0, 0), (0, 0), 11)] if border == FOREST else []))
        return t

    def table(rows):
        ch = chartable(rows)
        hdr, body = rows[0], rows[1:]
        if ch:
            n = max(len(r) for r in rows)
            cw = min(13.5, CW / n)
            for t_ in ():
                pass

            # Filled cells, not glyphs: a font substitution or a missing ttf turns "black square"
            # into a smudge, and a stitch chart is the one place a PDF must be unambiguous.
            data = [[Paragraph(f"<font size=6 color='{MUTE}'>{c}</font>", st["cell"]) if ri == 0 else ""
                     for c in r] for ri, r in enumerate(rows)]
            # splitByRow=0: a grid that breaks across a page is a chart the buyer has to hold open
            # with two hands, and rows 8 and 9 of a letter end up on separate sheets. Better a short
            # page than a split glyph, so the whole grid moves.
            t = Table(data, colWidths=[cw] * n, rowHeights=[11] + [cw] * (len(data) - 1), splitByRow=0)
            style = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                     ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                     ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                     ("INNERGRID", (0, 1), (-1, -1), 0.35, C(LINE)),
                     ("BOX", (0, 1), (-1, -1), 0.7, C(FOREST))]
            for ri, r in enumerate(rows):
                if ri == 0:
                    continue
                for ci, c in enumerate(r):
                    if c.strip("` ") == "#":
                        style.append(("BACKGROUND", (ci, ri), (ci, ri), C(FOREST)))
            t.setStyle(TableStyle(style))
            t.hAlign = "LEFT"
            return t
        nc = max(len(r) for r in rows)
        cw = [CW / nc] * nc
        data = [[Paragraph(esc(c), st["th"]) for c in hdr]]
        for r in body:
            data.append([Paragraph(esc(c), st["td"]) for c in r] + [""] * (nc - len(r)))
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), C(FOREST)),
                               ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C("#FFFFFF"), C("#FBF6EC")]),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                               ("LEFTPADDING", (0, 0), (-1, -1), 6),
                               ("LINEBELOW", (0, 1), (-1, -2), 0.4, C(LINE)),
                               ("BOX", (0, 0), (-1, -1), 0.5, C(LINE))]))
        return t

    story, pend, pend_keep = [], None, False
    for kind, val in blocks:
        if kind == "meta":
            f = [Paragraph(f"<b><font color='{FOREST}'>{H.escape(k)}:</font></b> {esc(v)}", st["m"]) for k, v in val]
            flow = box(Table([[x] for x in f], colWidths=[CW]), border=LINE, bg="#FBF6EC", pad=9)
        elif kind == "h1":
            flow = [Paragraph(esc(val), st["h1"]), HRFlowable(width="100%", thickness=2.2, color=C(TERRA), spaceBefore=1, spaceAfter=7)]
        elif kind in ("h2", "h3"):
            if pend is not None:                 # heading stacked on heading (h2 then h3): flush the
                story.append(pend)                # first, or KeepTogether gets a None and dies on wrap
            pend = Paragraph(esc(val), st[kind]); flow = None
        elif kind == "pre":
            flow = box(XPreformatted(H.escape(val, quote=False), st["pre"]), border=LINE)
        elif kind == "rounds":
            flow = box(Paragraph(esc(val), st["rd"]), border=FOREST, bg="#FFFFFF")
        elif kind == "ul":
            flow = [Paragraph(f"<bullet>&bull;</bullet>{esc(li)}", st["li"]) for li in val]
        elif kind == "table":
            flow = table(val)
        else:
            flow = Paragraph(esc(val), st["p"])
        if pend is not None:
            items = flow if isinstance(flow, list) else ([flow] if flow is not None else [])
            if items:
                if pend_keep and kind == "table" and chartable(val):  # noqa: S602 - h2 label + grid
                    # KeepTogether moves a group that fits; an unsplittable grid plus its label does
                    # not fit at the bottom of a page and would leave the letter's name stranded
                    # there, so the space is reserved before the label is emitted.
                    need = 30 + 11 + 13.5 * (len(val) - 1)
                    story.append(CondPageBreak(need))
                story.append(KeepTogether([pend, Spacer(1, 3), items[0]]))
                flow = items[1:]
            else:
                story.append(pend); flow = []
            pend = None
        story.extend(flow if isinstance(flow, list) else [flow])
    if pend is not None:
        story.append(pend)
    doc.build(story)
    return path


# ---------------------------------------------------------------- main
HOWTO = f"""HOW TO PUBLISH THESE FILES - read once, it prevents the two common mistakes

1. Etsy takes up to 5 files per listing, 20 MB each, and a ZIP counts as ONE file. The zip is the
   safe shape: upload `patterns-and-charts.zip`, not four loose PDFs, so a buyer never gets 3 of 4.
2. Upload the PDFs. Do not upload this txt, the source markdown, or the listing images - they are
   for you.
3. Before the first upload, open one PDF and check the chart pages: if a grid has split across a
   page, re-run make_pdfs.py after moving that chart under its own heading.

The files in pdf/:
  F1-nativity-set.pdf     20 blocks - shared body base + 19 figures
  F2-baby-loveys.pdf      4 loveys, 3 sizes, baby-safe face option first
  F3-advent-garland.pdf   24 motifs + numbers
  F4-stockings.pdf        stocking base + 5 fronts + turned cuff
  AZ-name-chart.pdf       A-Z mosaic chart   <- the reason someone pays $11.99 not $1.62
  numbers-1-24.pdf        day numerals for the garland and cuffs
  START-HERE.pdf          the cover page every buyer should open first

Every pattern says TEST_STATUS: untested. Keep it that way until you have stitched the pieces, and
keep "tested by", "tech edited" and "proofed" out of the listing copy - you have no testers yet.
"""


def main():
    files = sys.argv[1:] or sorted(glob.glob("patterns/F*.md") + glob.glob("patterns/START-HERE.md")
                                   + glob.glob("patterns/charts/*.md"))
    os.makedirs("dist/patterns", exist_ok=True)
    made = []
    for f in files:
        md = open(f).read()
        blocks = parse(md)
        title = next((v for k, v in blocks if k == "h1"), os.path.basename(f))
        name = os.path.splitext(os.path.basename(f))[0]
        page = (f"<!doctype html><html><head><meta charset=utf-8><title>{H.escape(title)}</title>"
                f"<style>{CSS}</style></head><body><main>{html_of(blocks)}</main>"
                f"<footer>NovalityStore &middot; personal use only &middot; novalitystore.etsy.com"
                f" &middot; patterns untested until stitched</footer></body></html>")
        hp = f"dist/patterns/{name}.html"
        open(hp, "w").write(page)
        pp = pdf_of(blocks, f"dist/patterns/{name}.pdf",
                    "NovalityStore  \u00b7  personal use only  \u00b7  novalitystore.etsy.com  \u00b7  "
                    "untested draft - report any round that does not work")
        made.append((name, title, os.path.getsize(hp), os.path.getsize(pp) if pp else 0))
        print(f"  {name:<18} html {made[-1][2]//1024:>3} KB" + (f"  pdf {made[-1][3]//1024:>3} KB" if pp else "  pdf (reportlab missing)"))
    head = ("<!doctype html><html><head><meta charset=utf-8><title>Novality pattern files</title><style>"
            "body{background:%s;font:15px/1.6 'DejaVu Sans',sans-serif;color:%s;margin:0;padding:40px}"
            "a{color:%s;font-weight:600;text-decoration:none;border-bottom:1px solid %s}"
            "h1{color:%s;font-size:26px;margin:0 0 6px}p.k{color:%s}li{margin:0 0 8px}</style></head><body>"
            "<h1>Print-ready pattern files</h1><p class='k'>The .pdf links exist when reportlab is "
            "installed; the .html links open the same page in a browser, where Ctrl-P / &#8984;-P and "
            "&quot;Save as PDF&quot; (Letter or A4, margins Default, <b>Background graphics ticked</b>) "
            "gives the identical file. Upload the PDF.</p><ul>") % (CREAM, INK, FOREST, TERRA, FOREST, MUTE)
    idx = [head]
    for n, t, _, _ in made:
        idx.append(f"<li><a href='{n}.pdf'>{H.escape(t)}</a> &nbsp;<a href='{n}.html'>[html]</a></li>")
    idx.append("</ul></body></html>")
    open("dist/patterns/index.html", "w").write("".join(idx))
    print(f"{len(made)} pattern file(s) in dist/patterns/")
    zp = "Novality_Crochet_Patterns_v1.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("HOW-TO-UPLOAD.txt", HOWTO)
        for n, t, hs, ps in made:
            if ps:
                z.write(f"dist/patterns/{n}.pdf", f"pdfs/{n}.pdf")
            z.write(f"dist/patterns/{n}.html", f"print-ready-html/{n}.html")
        for f in sorted(glob.glob("patterns/*.md")) + sorted(glob.glob("patterns/charts/*.md")) + \
                 ["make_pdfs.py", "make_charts.py", "verify_patterns.py", "verify_pdfs.py"]:
            z.write(f, "source/" + f.split("patterns/")[-1])
        for f in sorted(glob.glob("patterns/charts/*.png")):
            z.write(f, "listing-images/" + os.path.basename(f))
    print(f"deliverable zip: {zp}  ({os.path.getsize(zp) / 1e6:.2f} MB, "
          f"{len(zipfile.ZipFile(zp).namelist())} entries)")


if __name__ == "__main__":
    main()
