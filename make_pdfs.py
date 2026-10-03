#!/usr/bin/env python3
"""Turn the pattern markdown into print-ready HTML the buyer (or you) saves as a PDF.

There is no pandoc, weasyprint or reportlab in this environment and Etsy only takes the file you
upload, so the export is a self-contained HTML page with @page CSS: open it in Chrome, Ctrl/Cmd-P,
"Save as PDF", Letter or A4, margins default, background graphics ON. That produces the same PDF a
paid converter would for a text-and-charts pattern, and nothing can silently reflow overnight
because the renderer is in this repo, not on your machine.

Usage: python3 make_pdfs.py [patterns/*.md]      # writes dist/patterns/*.html
"""
import glob, html as H, os, re, sys

INDEXLIST = []
CREAM, INK, FOREST, TERRA, MUTE, LINE = "#F5EFE6", "#262420", "#1F4634", "#C2643F", "#7A7265", "#D7CBB8"
CSS = f"""
@page {{ size: Letter; margin: 16mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{ background: {CREAM}; color: {INK}; margin: 0; padding: 0;
  font: 10.5pt/1.5 'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif; }}
main {{ max-width: 46em; margin: 0 auto; padding: 28px 34px 60px; }}
h1 {{ font-family: 'Futura', 'Century Gothic', 'Trebuchet MS', sans-serif; color: {FOREST};
  font-size: 25pt; line-height: 1.12; margin: 0 0 .3em; letter-spacing: -.01em; }}
h2 {{ font-family: 'Futura', 'Century Gothic', 'Trebuchet MS', sans-serif; color: {FOREST};
  font-size: 14pt; margin: 1.9em 0 .5em; padding-bottom: .25em;
  border-bottom: 2px solid {TERRA}; break-after: avoid; }}
h3 {{ font-family: 'Futura', 'Century Gothic', 'Trebuchet MS', sans-serif; color: {TERRA};
  font-size: 11.5pt; margin: 1.5em 0 .35em; break-after: avoid; }}
p, li {{ orphans: 2; widows: 2; }}
ul {{ padding-left: 1.2em; }}
.meta {{ border: 1px solid {LINE}; background: #fff; padding: 10px 14px; border-radius: 6px;
  font: 9.5pt/1.5 'DejaVu Sans', 'Trebuchet MS', sans-serif; color: {MUTE}; }}
.meta b {{ color: {FOREST}; }}
table {{ border-collapse: collapse; width: 100%; margin: .7em 0 1em; font-size: 9.3pt;
  break-inside: avoid; }}
th {{ background: {FOREST}; color: {CREAM}; text-align: left; padding: 5px 8px;
  font-family: 'DejaVu Sans', sans-serif; font-size: 8.6pt; letter-spacing: .02em; }}
td {{ border-bottom: 1px solid {LINE}; padding: 4px 8px; vertical-align: top; }}
tr:nth-child(even) td {{ background: rgba(255,255,255,.55); }}
code {{ font: 8.6pt/1.35 'DejaVu Sans Mono', 'Courier New', monospace; }}
pre {{ background: #fff; border: 1px solid {LINE}; border-radius: 6px; padding: 10px 12px;
  font: 8.4pt/1.3 'DejaVu Sans Mono', 'Courier New', monospace; color: {FOREST};
  white-space: pre; overflow-x: auto; break-inside: avoid; }}
.rounds {{ background: #fff; border-left: 3px solid {FOREST}; padding: 8px 12px; margin: .6em 0 1em;
  font: 9.4pt/1.55 'DejaVu Sans Mono', 'Courier New', monospace; break-inside: avoid; }}
.warn {{ background: #FBEFE7; border: 1px solid {TERRA}; border-radius: 6px; padding: 8px 12px;
  font-family: 'DejaVu Sans', sans-serif; font-size: 9pt; }}
footer {{ position: fixed; bottom: 6mm; left: 0; right: 0; text-align: center;
  font: 7.6pt/1 'DejaVu Sans', sans-serif; color: {MUTE}; }}
@media print {{ main {{ max-width: none; padding: 0; }} .pagebreak {{ break-before: page; }} }}
"""


def inline(s):
    s = H.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)


def render(md):
    """Tiny markdown subset: headings, lists, tables, fences, paragraphs. No dependency, no
    surprise - and the pattern files only ever use those five constructs."""
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j]); j += 1
            out.append("<pre>" + H.escape("\n".join(buf), quote=False) + "</pre>"); i = j + 1; continue
        m = re.match(r"^(#{1,3})\s+(.*)$", ln)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if ln.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not set(lines[i].replace("|", "").strip()) <= set("-: "):
                    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    rows.append(cells)
                i += 1
            t = ["<table>"]
            if rows:
                t.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>")
            for r in rows[1:]:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</table>"); out.append("\n".join(t)); continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{inline(lines[i][2:])}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        if not ln.strip():
            i += 1; continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |```)", lines[i]):
            buf.append(lines[i]); i += 1
        txt = " ".join(buf).strip()
        tag = "p"
        if re.match(r"^(R\d|Row \d|Round \d|Ch\b|Finish:|Note:)", txt) or " — " in txt and " sc" in txt:
            tag = "div"
            out.append(f'<div class="rounds">{inline(txt)}</div>'); continue
        out.append(f"<{tag}>{inline(txt)}</{tag}>")
    return "\n".join(out)


def main():
    files = sys.argv[1:] or sorted(glob.glob("patterns/F*.md") + glob.glob("patterns/START-HERE.md") + glob.glob("patterns/charts/*.md"))
    os.makedirs("dist/patterns", exist_ok=True)
    n = 0
    for f in files:
        md = open(f).read()
        title = re.search(r"^#\s+(.*)$", md, re.M)
        title = H.unescape(title.group(1)) if title else os.path.basename(f)
        meta = re.findall(r"^\*\*(Product|Sell as|TEST_STATUS|BABY_SAFE):\*\*\s*(.*)$", md, re.M)
        chip = "".join(f"<b>{k}:</b> {inline(v)}<br>" for k, v in meta)
        body = render(md)
        name = os.path.splitext(os.path.basename(f))[0]
        (INDEX := INDEXLIST).append((name, title))
        page = (f"<!doctype html><html><head><meta charset=utf-8><title>{H.escape(title)}</title>"
                f"<style>{CSS}</style></head><body><main>"
                f"<div class='meta'>{chip}</div>{body}</main>"
                f"<footer>NovalityStore &nbsp;·&nbsp; personal use only &nbsp;·&nbsp; "
                f"novalitystore.etsy.com</footer></body></html>")
        open(f"dist/patterns/{name}.html", "w").write(page)
        n += 1
        print(f"  dist/patterns/{name}.html  ({os.path.getsize(f'dist/patterns/{name}.html')//1024} KB)")
    idx = ["<!doctype html><html><head><meta charset=utf-8><title>Novality pattern PDFs</title>",
           f"<style>body{{background:{CREAM};font:15px/1.6 'DejaVu Sans',sans-serif;color:{INK};margin:0;padding:40px}}",
           f"a{{color:{FOREST};font-weight:600;text-decoration:none;border-bottom:1px solid {TERRA}}}",
           f"h1{{color:{FOREST};font-size:26px;margin:0 0 6px}}p.k{{color:{MUTE};margin:0 0 26px}}",
           "li{{margin:0 0 8px}}</style></head><body>",
           "<h1>Print-ready pattern files</h1>",
           "<p class='k'>Open a file, then Ctrl-P / &#8984;-P &rarr; <b>Save as PDF</b> &rarr; Letter or A4, "
           "margins Default, <b>Background graphics ticked</b>. That tick is why the colour and the "
           "round tables survive the export.</p><ul>"]
    idx += [f"<li><a href='{n}.html'>{H.escape(t)}</a></li>" for n, t in INDEXLIST]
    idx.append("</ul><footer style='color:#7A7265;font-size:12px'>NovalityStore &middot; personal use only"
               " &middot; patterns are untested drafts until you have stitched one</footer></body></html>")
    open("dist/patterns/index.html", "w").write("".join(idx))
    print(f"{n} file(s) ready - open one, Ctrl/Cmd-P, Save as PDF, background graphics ON.")


if __name__ == "__main__":
    main()
