#!/usr/bin/env python3
"""Compose Etsy listing tiles (2700x2025) from files that already exist in this repo.

The rule this tool is built around: a tile may only show what the buyer receives. So the artwork is
the real PDF page rasterised at print resolution, the real generated stitch chart, and text drawn
from claims that verify_patterns.py can check. Nothing here invents a finished object, because the
shop's one 1-star review is a complaint that a picture did not match the pattern.

    python3 make_tile.py --id 4577821049            # one listing
    python3 make_tile.py --all                      # everything specced so far

Output: tiles/<id>/01-main.png, 02-contents.png ... at 2700x2025 (tracked, unlike dist/).
"""
import argparse, glob, json, os, subprocess, sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("pillow is required: pip install pillow")

CREAM, INK, FOREST, TERRA, MUTE, LINE = "#F5EFE6", "#262420", "#1F4634", "#C2643F", "#7A7265", "#D7CBB8"
W, H = 2700, 2025
FD = "/usr/share/fonts/truetype/dejavu"

# ---- one entry per listing in TOP15_IMAGE_QUEUE.md. `pages` are 1-indexed PDF pages of the actual
# ---- product file; `chips` must each be true of that file.
SPEC = {
    "4577821049": {
        "pdf": "patterns/pdf/F3-advent-garland.pdf",
        "tiles": [
            {"file": "01-main.png", "kicker": "AMIGURUMI ADVENT CALENDAR  ·  24 DAYS",
             "headline": "The 24-Day\nAdvent Garland",
             "sub": "24 numbered minis, the 1-24 day chart, and a gift note to hide inside each one. Every round counted and machine-checked, US and UK terms.",
             "chips": ["24 motifs, 6-12 cm", "approx 20 g of DK", "24 printable gift notes", "US + UK terms"],
             "pages": [9, 12], "caption": "real pages from the PDF you download"},
            {"file": "02-contents.png", "kicker": "WHAT IS IN THE FILE",
             "headline": "Everything,\nnumbered",
             "list": ["24 motifs, M01 to M24, one page each",
                      "The day-number chart, 1 to 24, worked in link stitch",
                      "24 printable gift notes, a prompt per day",
                      "Garland cord, loops, and the bead-throwing trick",
                      "Gauge, sizes, blocking, safety wording, licence"],
             "pdf": "patterns/pdf/numbers-1-24.pdf", "pages": [1],
             "chips": ["1 square = 1 stitch", "two-digit days included"],
             "caption": "the actual chart sheet from the download"},
            {"file": "03-honest.png", "kicker": "READ THIS BEFORE YOU CAST ON",
             "headline": "Checked counts.\nReal pages.",
             "para": "Every round in this file was checked by script: each one consumes exactly the stitches the round before it made, so a count cannot drift. What a script cannot check is gauge, look and feel, because those belong to your hook and your yarn.\nYou need: 3.0 mm hook, DK acrylic, about 20 g in four colours, 24 beads or the printed day tags.\nThese are ornaments, not toys - not for a child under three, and the optional 9 mm safety eyes are why that sentence is printed in the PDF.",
             "chips": ["round counts checked by script", "gauge is still yours to match", "24 motifs, 24 gift notes"]},
        ],
    },
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


def wrap(draw, text, fnt, maxw):
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            t = (line + " " + word).strip()
            if draw.textlength(t, font=fnt) <= maxw or not line:
                line = t
            else:
                out.append(line); line = word
        out.append(line)
    return out


def page_images(pdf, nums, dpi=168):
    """Rasterise real pages of the product PDF - the only artwork this tool is allowed to use."""
    try:
        import pymupdf
    except ImportError:
        sys.exit("pymupdf is required to embed real pages: pip install pymupdf")
    if not os.path.exists(pdf):
        sys.exit(f"{pdf} missing - run make_pdfs.py first")
    doc = pymupdf.open(pdf)
    out = []
    for n in nums:
        pg = doc[min(n - 1, doc.page_count - 1)]
        pm = pg.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
        out.append(img)
    doc.close()
    return out


def card(img, hgt, shadow=26):
    """A page as a physical card: white, hairline border, soft drop shadow."""
    ratio = img.width / img.height
    w = int(hgt * ratio)
    im = img.resize((w, hgt), Image.LANCZOS)
    out = Image.new("RGB", (w + shadow * 2, hgt + shadow * 2), CREAM)
    d = ImageDraw.Draw(out)
    d.rectangle((shadow + 8, shadow + 10, shadow + w + 8, shadow + hgt + 10), fill="#E4DBC9")
    out.paste(im, (shadow, shadow))
    d.rectangle((shadow, shadow, shadow + w, shadow + hgt), outline=LINE, width=3)
    return out


def tile(spec, outpath):
    """Two-column layout with measured wrapping. The left column is text, the right column is the
    product. Nothing is allowed to be drawn outside its column, which is the whole reason the first
    version of this function clipped a list at 1250 px and ran a chart through the chips: an Etsy
    tile is read at 75 px wide in the grid, so an overlap that looks small here is fatal there."""
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle((44, 44, W - 44, H - 44), outline=LINE, width=4)
    d.rectangle((44, 44, W - 44, 60), fill=FOREST)
    d.rectangle((44, H - 60, W - 44, H - 44), fill=TERRA)

    art = bool(spec.get("pages") or spec.get("extra"))
    x = 150
    colw = 1180 if art else 2400
    top, bottom = 175, H - 215

    y = top
    if spec.get("kicker"):
        d.text((x, y), spec["kicker"], font=font("DejaVuSans-Bold.ttf", 34), fill=TERRA)
        y += 74

    hs = 118 if art else 148
    if spec.get("headline"):
        hf = font("DejaVuSans-Bold.ttf", hs)
        for ln in spec["headline"].split("\n"):
            d.text((x, y), ln, font=hf, fill=FOREST)
            y += int(hf.size * 1.15)
        y += 16
        d.line((x, y, x + 560, y), fill=TERRA, width=7)
        y += 52

    if spec.get("sub"):
        sf = font("DejaVuSans.ttf", 40 if art else 44)
        for ln in wrap(d, spec["sub"].replace("\n", " "), sf, colw - 20):
            d.text((x, y), ln, font=sf, fill=INK); y += 60
        y += 22

    if spec.get("para"):
        pf = font("DejaVuSans.ttf", 40)
        for ln in wrap(d, spec["para"], pf, colw - 20):
            if ln == "":
                y += 26; continue
            d.text((x, y), ln, font=pf, fill=INK); y += 56
        y += 22

    if spec.get("list"):
        lf = font("DejaVuSans.ttf", 43)
        for item in spec["list"]:
            lines = wrap(d, item, lf, colw - 80)
            for n, ln in enumerate(lines):
                if n == 0:
                    d.ellipse((x + 6, y + 16, x + 22, y + 32), fill=TERRA)
                d.text((x + 44 if n == 0 else x + 52, y), ln, font=lf, fill=INK)
                y += 60
            y += 12
        y += 14

    if spec.get("chips"):
        cf = font("DejaVuSans-Bold.ttf", 36)
        cx, cy = x, y + 6
        for ch in spec["chips"]:
            w = int(d.textlength(ch, font=cf)) + 74
            if cx + w > x + colw:
                cx, cy = x, cy + 96
            d.rounded_rectangle((cx, cy, cx + w, cy + 74), radius=37, fill="#FFFFFF", outline=FOREST, width=4)
            d.ellipse((cx + 26, cy + 29, cx + 44, cy + 47), fill=TERRA)
            d.text((cx + 58, cy + 16), ch, font=cf, fill=FOREST)
            cx += w + 24

    ax, aw = 150 + colw + 70, W - 150 - (150 + colw + 70)
    if art:
        caption = spec.get("caption", "pages from the file you download")
        ah = H - top - 260 if spec.get("pages") else H - 260
        if spec.get("pages"):
            imgs = page_images(spec.get("pdf") or SPEC[spec["_key"]]["pdf"], spec["pages"])
            ph = int((H - top - 520) / max(1, 1 + 0.10 * (len(imgs) - 1)))
            cards = [card(im, ph) for im in imgs]
            ang = [-3.4, 2.2, -1.2]
            step = 250
            tot = cards[0].width + step * (len(cards) - 1) + 30
            scale = min(1.0, aw / tot)
            if scale < 1:
                cards = [card(im, int(ph * scale)) for im in imgs]
                step = int(step * scale)
            px, py = ax + max(0, (aw - cards[0].width) // 2), top + 40
            for i, c in enumerate(cards):
                rot = c.rotate(ang[i % len(ang)], expand=True, resample=Image.BICUBIC, fillcolor=CREAM)
                img.paste(rot, (px + i * step, py - i * 26))
            d.text((px + 30, py + ph + 96), caption, font=font("DejaVuSans.ttf", 32), fill=MUTE)
        elif spec.get("extra") and os.path.exists(spec["extra"]):
            ex = Image.open(spec["extra"]).convert("RGB")
            tw = aw - 60
            th = int(tw * ex.height / ex.width)
            if th > H - 420:
                th = H - 420; tw = int(th * ex.width / ex.height)
            ex = ex.resize((tw, th), Image.LANCZOS)
            box = Image.new("RGB", (ex.width + 52, ex.height + 52), "#FFFFFF")
            box.paste(ex, (26, 26))
            ImageDraw.Draw(box).rectangle((13, 13, ex.width + 38, ex.height + 38), outline=LINE, width=3)
            tx = ax + (aw - box.width) // 2
            ty = top + 60 + (ah - box.height) // 2
            img.paste(box, (tx, ty))
            d.text((ax, ty + box.height + 46), caption, font=font("DejaVuSans.ttf", 31), fill=MUTE)

    d.text((x, H - 172), "NovalityStore", font=font("DejaVuSans-Bold.ttf", 46), fill=FOREST)
    w = d.textlength("NovalityStore", font=font("DejaVuSans-Bold.ttf", 46))
    d.text((x + w + 34, H - 162), "digital patterns  \u00b7  personal use licence  \u00b7  instant download",
           font=font("DejaVuSans.ttf", 36), fill=MUTE)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    img.save(outpath)
    return outpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", help="listing id from TOP15_IMAGE_QUEUE.md")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    ids = list(SPEC) if a.all else ([a.id] if a.id else [])
    if not ids:
        print("no listing specced yet; known ids:", ", ".join(SPEC)); return 1
    for lid in ids:
        spec = SPEC[lid]
        for t in spec["tiles"]:
            t["_key"] = lid
            p = tile(t, f"tiles/{lid}/{t['file']}")
            print(f"  {p}  ({os.path.getsize(p)/1e6:.2f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
