"""
NovalityStore — brand asset generator
=====================================
Draws every shop asset at Etsy's real pixel specs using only Pillow + the DejaVu
fonts on the box. Deliberately deterministic: an AI-generated logo looks great in a
preview and falls apart at 16px on a phone, and I can't see the output to catch it.
The one AI layer used (assets/banner_bg.png) sits BEHIND an opaque panel, so if the
texture is ever ugly the type is still perfectly readable.

Run:  python3 make_brand_assets.py
Out:  brand/
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------------- brand system
CREAM      = (245, 239, 230)   # F5EFE6  page / background
CREAM_DEEP = (236, 226, 212)   # ECE2D4  panel tint
FOREST     = (31, 70, 52)      # 1F4634  primary ink / logo field
FOREST_SOFT= (62, 97, 80)      # 3E6150  secondary green for motifs
TERRA      = (194, 100, 63)    # C2643F  the one accent (CTA, sale, underline)
TERRA_DEEP = (163, 78, 44)      # A34E2C  accent pressed/darker
INK        = (38, 36, 32)       # 262420  body text on cream
MUTE       = (122, 114, 101)    # 7A7265  secondary text on cream
LINE       = (215, 203, 184)    # D7CBB8  hairlines

WORDMARK   = "Novality"
WORDMARK_2 = "Store"
TAGLINE    = "Crochet patterns & spreadsheet planners you can start tonight"
KICKER     = "DIGITAL DOWNLOAD  ·  INSTANT ACCESS  ·  EXCEL + GOOGLE SHEETS + US/UK TERMS"

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, px):
    return ImageFont.truetype(os.path.join(FD, name), px)

OUT = "brand"
os.makedirs(OUT, exist_ok=True)


def F(path):
    p = os.path.join("assets", path)
    return Image.open(p).convert("RGB") if os.path.exists(p) else None


# ------------------------------------------------------------------- primitives
def rounded(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def centre_text(img, text, fnt, fill, xy=None, anchor="mm"):
    """xy defaults to the exact horizontal centre — nothing drifts."""
    d = ImageDraw.Draw(img)
    w, h = img.size
    d.text(xy or (w // 2, h // 2), text, font=fnt, fill=fill, anchor=anchor)
    return d


def stitch_row(draw, x0, y, n, step, colour, arc=16, weight=4):
    """A crochet chain: alternating arcs on the centre line. Reads as 'maker'."""
    for i in range(n):
        cx = x0 + i * step + step // 2
        top = i % 2 == 0
        bbox = (cx - arc, y - (arc if top else 0), cx + arc, y + (arc if top else 0) * 2 - arc + arc)
        bbox = (cx - arc, y - arc, cx + arc, y + arc)
        if top:
            draw.arc(bbox, 180, 360, fill=colour, width=weight)
        else:
            draw.arc(bbox, 0, 180, fill=colour, width=weight)


def grid_block(draw, x, y, cols, rows, cell, colour, check_fill=None):
    """A planner grid with a couple of ticks. Reads as 'organised'."""
    for r in range(rows):
        for c in range(cols):
            bx = x + c * cell
            by = y + r * cell
            draw.rectangle((bx, by, bx + cell, by + cell), outline=colour, width=2)
            if check_fill and (r * cols + c) % 5 == 2:
                pad = int(cell * 0.3)
                rounded(draw, (bx + pad, by + pad, bx + cell - pad, by + cell - pad),
                        3, fill=check_fill)


def wordmark(img, x, y, size, on_dark=False, align="left"):
    """Novality in serif bold + Store in serif light, with a terracotta underline."""
    d = ImageDraw.Draw(img)
    ink = CREAM if on_dark else FOREST
    big = font("DejaVuSerif-Bold.ttf", size)
    small = font("DejaVuSerif.ttf", int(size * 0.92))
    w1 = d.textlength(WORDMARK, font=big)
    w2 = d.textlength(WORDMARK_2, font=small)
    total = w1 + int(size * 0.18) + w2
    if align == "center":
        x = (img.size[0] - total) // 2
    d.text((x, y), WORDMARK, font=big, fill=ink)
    d.text((x + w1 + int(size * 0.18), y + int(size * 0.06)), WORDMARK_2, font=small,
           fill=TERRA if not on_dark else TERRA)
    # underline sits under the whole lockup, anchored to the baseline
    uy = y + int(size * 1.16)
    d.line((x, uy, x + total, uy), fill=TERRA, width=max(3, size // 22))
    return total, uy


# ------------------------------------------------------------------- the mark
def _bezier(p0, p1, p2, n=120):
    out = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 2
        b = 2 * (1 - t) * t
        c = t ** 2
        out.append((a * p0[0] + b * p1[0] + c * p2[0],
                    a * p0[1] + b * p1[1] + c * p2[1]))
    return out


def _thick_path(d, pts, w, colour):
    """Round-capped stroke: overlapping discs along the path. Keeps the mark
    smooth at 160px where a plain polyline would show faceted joints."""
    r = w / 2
    for (x, y) in pts:
        d.ellipse((x - r, y - r, x + r, y + r), fill=colour)


def make_mark(size=640, bg=FOREST, ink=CREAM, accent=TERRA, radius=0.22):
    """A monogram N whose diagonal is a stitch curve: one idea for crochet, one
    letter for the shop name. Deliberately 3 strokes so it survives tiny sizes."""
    img = Image.new("RGB", (size, size), bg)
    d = ImageDraw.Draw(img)
    if radius:
        r = int(size * radius)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), radius=r, fill=255)
        base = Image.new("RGB", (size, size), CREAM)
        base.paste(img, (0, 0), mask)
        img = base
        d = ImageDraw.Draw(img)
    w = size * 0.085
    x_l, x_r = size * 0.30, size * 0.70
    y_t, y_b = size * 0.33, size * 0.67
    _thick_path(d, [(x_l, y) for y in range(int(y_t), int(y_b) + 1)], w, ink)
    _thick_path(d, [(x_r, y) for y in range(int(y_t), int(y_b) + 1)], w, ink)
    _thick_path(d, _bezier((x_l, y_t + w * 0.2), (size * 0.50, size * 0.24),
                           (x_r, y_b - w * 0.2)), w, accent)
    return img


def circular(img, bg=None):
    size = img.size[0]
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGB", (size, size), bg or CREAM)
    out.paste(img, (0, 0), mask)
    return out


# --------------------------------------------------------------------- banner
def make_banner():
    """Etsy shop banner: 3360 x 840. Left-weighted type on an opaque panel so the
    AI texture can never make the words unreadable."""
    W, H = 3360, 840
    img = Image.new("RGB", (W, H), CREAM)

    bg = F("banner_bg.png")
    if bg is not None:
        img.paste(bg.resize((W, H)), (0, 0))
        img = img.filter(ImageFilter.GaussianBlur(0.6))
        veil = Image.new("RGB", (W, H), CREAM)
        img = Image.blend(img, veil, 0.42)

    d = ImageDraw.Draw(img)
    # top + bottom rules give it structure at any crop
    d.rectangle((0, 0, W, 10), fill=FOREST)
    d.rectangle((0, H - 10, W, H), fill=FOREST)

    # the type panel: opaque, generous, sits on the left two-thirds
    px0, py0, px1, py1 = 150, 150, 2180, 690
    panel = Image.new("RGB", (px1 - px0, py1 - py0), CREAM)
    img.paste(panel, (px0, py0))
    d = ImageDraw.Draw(img)
    rounded(d, (px0, py0, px1, py1), 26, outline=LINE, width=2)

    wordmark(img, px0 + 62, py0 + 74, 150)
    d = ImageDraw.Draw(img)
    d.text((px0 + 64, py0 + 352), TAGLINE, font=font("DejaVuSans.ttf", 46), fill=INK)
    d.text((px0 + 64, py0 + 434), KICKER, font=font("DejaVuSans.ttf", 27), fill=MUTE)
    # sale-free CTA pill: the banner should never advertise a discount that can expire
    bx, by = px0 + 64, py0 + 500
    label = "Instant download — no shipping, no waiting"
    tw = d.textlength(label, font=font("DejaVuSans-Bold.ttf", 34))
    rounded(d, (bx, by, bx + tw + 74, by + 74), 37, fill=TERRA)
    d.text((bx + 37, by + 16), label, font=font("DejaVuSans-Bold.ttf", 34), fill=CREAM)

    # right side: mark + the two motifs, so the banner says what the shop sells
    mx = 2560
    badge = make_mark(560)
    img.paste(badge, (mx, 150))
    d = ImageDraw.Draw(img)
    stitch_row(d, mx + 40, 762, 6, 78, FOREST_SOFT, arc=20, weight=5)

    img.save(f"{OUT}/etsy_shop_banner_3360x840.png", optimize=True)
    # Etsy also accepts a smaller upload; ship a 1260-wide fallback for slow connections
    img.resize((1260, 315), Image.LANCZOS).save(f"{OUT}/etsy_shop_banner_1260x315.png", optimize=True)
    return img


# ---------------------------------------------------------------------- icons
def make_icons():
    """Shop icon (160) + avatar sizes. Etsy scales hard, so the 160 is the real test."""
    for size, name in [(640, "shop_icon_640"), (320, "shop_icon_320"), (160, "shop_icon_160")]:
        mark = make_mark(size)
        mark.save(f"{OUT}/{name}.png", optimize=True)

    # square logo lockup for About / packaging: mark above, wordmark below
    S = 1080
    img = Image.new("RGB", (S, S), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, S, S), outline=LINE, width=3)
    img.paste(make_mark(560), ((S - 560) // 2, 150))
    wordmark(img, 0, 800, 108, align="center")
    d = ImageDraw.Draw(img)
    d.text((S // 2, 962), "PATTERNS  ·  PLANNERS  ·  SPREADSHEETS",
           font=font("DejaVuSans.ttf", 25), fill=MUTE, anchor="mm")
    img.save(f"{OUT}/shop_icon_square_lockup.png", optimize=True)

    # wide lockup for the About page / invoice / any header
    W, H = 2000, 480
    img = Image.new("RGB", (W, H), CREAM)
    img.paste(make_mark(330, radius=0.26), (110, 75))
    wordmark(img, 520, 118, 132)
    d = ImageDraw.Draw(img)
    d.text((524, 330), TAGLINE, font=font("DejaVuSans.ttf", 38), fill=INK)
    img.save(f"{OUT}/logo_wide_lockup.png", optimize=True)
    return img


# ---------------------------------------------------------- section hero images
def make_section_banners():
    """Etsy section banners are 1600x200. Two sections, two colours of signal."""
    specs = [
        ("Crochet Patterns", "PDF patterns · US + UK terms · sizes and yardage on every page", "crochet"),
        ("Spreadsheet Planners", "Excel + Google Sheets · formulas built in · free updates", "sheets"),
    ]
    for title, sub, kind in specs:
        W, H = 1600, 200
        img = Image.new("RGB", (W, H), FOREST)
        d = ImageDraw.Draw(img)
        if kind == "crochet":
            stitch_row(d, 40, 172, 22, 70, (58, 97, 80), arc=20, weight=4)
            stitch_row(d, 40, 30, 22, 70, (58, 97, 80), arc=20, weight=4)
        else:
            for i in range(24):
                x = 40 + i * 66
                d.rectangle((x, 34, x + 58, 60), outline=(58, 97, 80), width=2)
            for i in range(24):
                x = 40 + i * 66
                d.rectangle((x, 142, x + 58, 168), outline=(58, 97, 80), width=2)
        d.text((80, 78), title, font=font("DejaVuSerif-Bold.ttf", 58), fill=CREAM)
        tw = d.textlength(title, font=font("DejaVuSerif-Bold.ttf", 58))
        d.text((80 + tw + 34, 96), sub, font=font("DejaVuSans.ttf", 26), fill=(198, 214, 202))
        d.line((80, 152, 80 + tw, 152), fill=TERRA, width=4)
        img.save(f"{OUT}/section_{kind}_1600x200.png", optimize=True)


# ---------------------------------------------------------------- full-bleed card
def make_sale_card():
    """A 1:1 promo tile for the shop announcement / social. The only place a
    discount should be stated, because it can be swapped in a day."""
    S = 1080
    img = Image.new("RGB", (S, S), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, S, S), outline=FOREST, width=6)
    d.rectangle((26, 26, S - 26, S - 26), outline=LINE, width=2)
    img.paste(make_mark(280), ((S - 280) // 2, 120))
    wordmark(img, 0, 470, 96, align="center")
    d = ImageDraw.Draw(img)
    d.text((S // 2, 640), "25% off every pattern and planner",
           font=font("DejaVuSans-Bold.ttf", 46), fill=INK, anchor="mm")
    d.text((S // 2, 712), "this weekend only", font=font("DejaVuSans.ttf", 34),
           fill=MUTE, anchor="mm")
    rounded(d, (S // 2 - 250, 812, S // 2 + 250, 900), 44, fill=TERRA)
    d.text((S // 2, 856), "SHOP THE SALE", font=font("DejaVuSans-Bold.ttf", 36),
           fill=CREAM, anchor="mm")
    d.text((S // 2, 986), "etsy.com/shop/NovalityStore",
           font=font("DejaVuSansMono.ttf", 27), fill=MUTE, anchor="mm")
    img.save(f"{OUT}/promo_tile_1080.png", optimize=True)


# ---------------------------------------------------------------------- palette
def make_palette():
    W, H = 2000, 620
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.text((60, 42), "NovalityStore — colour system", font=font("DejaVuSerif-Bold.ttf", 52), fill=FOREST)
    d.text((60, 116), "One accent, and it is only ever used for the thing you want clicked.",
           font=font("DejaVuSans.ttf", 30), fill=MUTE)
    swatches = [
        ("CREAM", CREAM, "backgrounds, logo ink"),
        ("FOREST", FOREST, "wordmark, icon field, headings"),
        ("TERRACOTTA", TERRA, "CTA, underline, sale — only here"),
        ("FOREST SOFT", FOREST_SOFT, "motifs, dividers, section lines"),
        ("INK", INK, "body text on cream"),
        ("MUTE", MUTE, "captions, meta, disabled"),
    ]
    cw, ch = 296, 300
    for i, (name, rgb, use) in enumerate(swatches):
        x = 60 + i * (cw + 16)
        y = 200
        d.rectangle((x, y, x + cw, y + 150), fill=rgb, outline=LINE, width=2)
        hexv = "#%02X%02X%02X" % rgb
        dark = sum(rgb) / 3 < 140
        d.text((x + 14, y + 168), name, font=font("DejaVuSans-Bold.ttf", 27),
               fill=FOREST)
        d.text((x + 14, y + 204), hexv, font=font("DejaVuSansMono.ttf", 26), fill=INK)
        d.text((x + 14, y + 242), use, font=font("DejaVuSans.ttf", 20), fill=MUTE)
    d.text((60, 556), "Type: DejaVu Serif Bold (wordmark) / DejaVu Sans (everything else). "
                      "Free web swaps: Playfair Display → serif, Inter → sans.",
           font=font("DejaVuSans.ttf", 24), fill=MUTE)
    img.save(f"{OUT}/palette_and_type.png", optimize=True)


# ------------------------------------------------- listing image templates
def _fit(img, box):
    """Cover-fit an image into a box, centred — so any photo they drop in behaves."""
    bw, bh = box[2] - box[0], box[3] - box[1]
    if img is None:
        return None
    r = max(bw / img.width, bh / img.height)
    img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    x = box[0] + (bw - img.width) // 2
    y = box[1] + (bh - img.height) // 2
    return img, (x, y)


def fit_font(text, px, max_w, d, face="DejaVuSerif-Bold.ttf"):
    """Shrink until the line fits. Hard-coded sizes are how text gets clipped on a
    2000px canvas while still looking fine in a preview — the worst kind of bug."""
    while px > 16 and d.textlength(text, font=font(face, px)) > max_w:
        px = int(px * 0.94)
    return font(face, px)


def make_listing_templates():
    """Etsy's grid is 4:3 (2700x2025 recommended, 2000x1500 min) but SEARCH shows a
    centre-cropped SQUARE. So every word lives inside the middle 1500px — a title that
    only fits edge-to-edge is a title that gets cut off where it matters."""
    W, H = 2000, 1500
    SAFE = 1500                       # the square Etsy will actually show
    x0 = (W - SAFE) // 2              # 250
    for kind, accent, kicker, facts in [
        ("crochet", TERRA, "PDF PATTERN  ·  US + UK TERMS", ["3 SIZES", "12 PAGES", "NO SEW"]),
        ("spreadsheet", FOREST, "EXCEL + GOOGLE SHEETS  ·  FREE UPDATES",
         ["13 TABS", "EXCEL + SHEETS", "COUNTDOWN"]),
    ]:
        img = Image.new("RGB", (W, H), CREAM)
        d = ImageDraw.Draw(img)
        art = (x0, 250, W - x0, H - 300)
        panel = Image.new("RGB", (art[2] - art[0], art[3] - art[1]), CREAM_DEEP)
        img.paste(panel, (art[0], art[1]))
        d = ImageDraw.Draw(img)
        rounded(d, (art[0], art[1], art[2], art[3]), 22, outline=LINE, width=3)
        cx, cy = W // 2, (art[1] + art[3]) // 2
        d.text((cx, cy - 30), "DROP YOUR OWN PHOTO HERE",
               font=font("DejaVuSans-Bold.ttf", 52), fill=(176, 165, 149), anchor="mm")
        d.text((cx, cy + 42), "real make · daylight · no renders",
               font=font("DejaVuSans.ttf", 32), fill=(190, 180, 166), anchor="mm")
        d.text((cx, cy + 140), "2000px or larger · 4:3",
               font=font("DejaVuSansMono.ttf", 24), fill=(198, 188, 174), anchor="mm")

        title_ph = "PRODUCT TITLE · 5 WORDS"
        tf = fit_font(title_ph, 66, SAFE - 80, d)
        d.text((cx, 124), title_ph, font=tf, fill=FOREST, anchor="mm")
        kf = fit_font(kicker, 30, SAFE - 80, d)
        d.text((cx, 196), kicker, font=kf, fill=MUTE, anchor="mm")
        d.line((art[0], 232, art[2], 232), fill=LINE, width=2)

        y = H - 250
        d.rectangle((0, y, W, H), fill=accent)
        seg = SAFE // len(facts)
        for i, f in enumerate(facts):
            ff = fit_font(f, 46, seg - 40, d, face="DejaVuSans-Bold.ttf")
            d.text((x0 + seg * i + seg // 2, y + 74), f, font=ff, fill=CREAM, anchor="mm")
            if i:
                d.line((x0 + seg * i, y + 38, x0 + seg * i, y + 110), fill=CREAM, width=2)
        d.text((cx, y + 176), "NovalityStore",
               font=font("DejaVuSerif-Bold.ttf", 38), fill=CREAM, anchor="mm")
        img.save(f"{OUT}/listing_template_{kind}_2000x1500.png", optimize=True)

    # what search will actually show you
    for kind in ("crochet", "spreadsheet"):
        img = Image.open(f"{OUT}/listing_template_{kind}_2000x1500.png")
        img.crop((x0, 0, x0 + SAFE, H)).resize((720, 720), Image.LANCZOS).save(
            f"{OUT}/preview_search_square_{kind}.png", optimize=True)


def make_icon_500():
    """Etsy's shop icon is 500x500 and it crops to a CIRCLE, so the colour field must
    be full-bleed: a rounded badge loses its corners and reads as a clipped square.
    The mark sits in the centre 78%, which survives every crop Etsy applies."""
    full = make_mark(500, radius=0)
    full.save(f"{OUT}/shop_icon_500.png", optimize=True)

    # preview the crop itself rather than guessing at it - light and dark chrome
    for bgc, name in (((224, 224, 224), "crop_on_light"), ((24, 24, 26), "crop_on_dark")):
        S = 620
        img = Image.new("RGB", (S, S), bgc)
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).ellipse((60, 60, S - 60, S - 60), fill=255)
        icon = full.resize((S - 120, S - 120), Image.LANCZOS)
        base = Image.new("RGB", (S, S), (0, 0, 0))
        base.paste(icon, (60, 60))
        img.paste(base, (0, 0), mask)
        ImageDraw.Draw(img).ellipse((60, 60, S - 60, S - 60), outline=LINE, width=2)
        img.save(f"{OUT}/shop_icon_{name}.png", optimize=True)

    # the 40px reality check: this is the size buyers actually see next to your name
    chk = Image.new("RGB", (900, 120), (255, 255, 255))
    d = ImageDraw.Draw(chk)
    small = full.resize((40, 40), Image.LANCZOS)
    m = Image.new("L", (40, 40), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 39, 39), fill=255)
    bg40 = Image.new("RGB", (40, 40), (255, 255, 255))
    bg40.paste(small, (0, 0), m)
    chk.paste(bg40, (28, 40))
    d.text((88, 52), "NovalityStore", font=font("DejaVuSans.ttf", 34),
           fill=(17, 17, 17), anchor="lm")
    d.text((88, 86), "3.7 ★ (3)  ·  Washington, United States",
           font=font("DejaVuSans.ttf", 20), fill=(120, 120, 120), anchor="lm")
    chk.save(f"{OUT}/shop_icon_40px_check.png", optimize=True)


def make_mini_banner():
    """Etsy's mini banner is 1200 x 160 - 7.5:1, so the big banner cannot simply be
    scaled into it. Forest field, mark, one line of type. No tagline: at 160px tall it
    is unreadable mush, and no second accent either - the stitch already owns terracotta."""
    W, H = 1200, 160
    img = Image.new("RGB", (W, H), FOREST)
    mx, msz = 34, 140
    img.paste(make_mark(msz, radius=0), (mx, (H - msz) // 2))
    d = ImageDraw.Draw(img)
    label, right = "Novality Store", "PATTERNS  +  PLANNERS"
    rf = font("DejaVuSans.ttf", 26)
    rw = int(d.textlength(right, font=rf))
    tx = mx + msz + 42          # clear the mark by 42px or its stem reads as a letter
    # reserve the right label plus a 120px gutter, or a longer name would collide with it
    f = fit_font(label, 76, W - tx - rw - 120 - 40, d, face="DejaVuSerif-Bold.ttf")
    d.text((tx, H // 2), label, font=f, fill=CREAM, anchor="lm")
    d.text((W - 40, H // 2), right, font=rf, fill=(200, 194, 182), anchor="rm")
    img.save(f"{OUT}/etsy_banner_mini_1200x160.png", optimize=True)


if __name__ == "__main__":
    make_banner()
    make_icons()
    make_icon_500()
    make_mini_banner()
    make_section_banners()
    make_sale_card()
    make_palette()
    make_listing_templates()
    files = sorted(os.listdir(OUT))
    print("brand/ → %d files" % len(files))
    for f in files:
        p = os.path.join(OUT, f)
        im = Image.open(p)
        print(f"  {f:38} {im.size[0]}x{im.size[1]:<5} {os.path.getsize(p)//1024:>4} KB")
