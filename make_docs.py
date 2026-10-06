#!/usr/bin/env python3
"""Build the two handoff files from the data in this repo, with a leak guard between them.

  NOVALITY_LISTINGS.md  - the copy file. Safe to share, print, hand to a VA. Contains no money,
                          no traffic numbers, no conversion rates: it is asserted to contain no '$'.
  NOVALITY_METRICS.md   - your numbers. The target maths, the ladder, the ad maths. Keep private.

Re-run after changing any source file:  python3 make_docs.py
Sources: seo_final.json (the frozen set), audit/proposed_seo.md (the document you sent),
TOP15_IMAGE_QUEUE.md, tiles/, patterns/, CROCHET_Q4_FIVE.md.
"""
import json, re, os, csv, subprocess, collections

setos = json.load(open("seo_final.json"))
LIVE = {1:"4573853611",3:"4577821049",4:"4573857903",5:"4573849581",7:"4573699869",18:"4561670979",
        20:"4549642404",21:"4549077688",25:"4534488947",26:"4534483099",27:"4534495626",29:"4534364844",
        34:"4578849733",35:"4578846463",36:"4573955047"}
HEAD = subprocess.run(["git","rev-parse","--short","HEAD"],capture_output=True,text=True).stdout.strip()
BR   = subprocess.run(["git","rev-parse","--abbrev-ref","HEAD"],capture_output=True,text=True).stdout.strip()
orig = {}
for blk in open("audit/proposed_seo.md").read().split("\n### ")[1:]:
    n = int(blk.split("\n")[0].split(". ")[0])
    orig[n] = [t.strip() for t in re.search(r"^Tags: (.+)$", blk, re.M).group(1).split("|")]

def scrub(t):
    """Money never belongs in the copy file: prices are the one lever you keep free during a freeze, so a
    price written here goes stale on purpose. Rewrite the few that carry meaning, then backstop the rest."""
    t = (t.replace("it is what makes $8 a bargain", "it is what makes the price feel small next to a printed blanket")
          .replace("the feature worth charging $45 for", "the feature that justifies the highest price in your shop")
          .replace("or you rank beside printable PDFs at $3", "or you rank beside cheap printable PDFs")
          .replace("the price ($28) needs the number", "a bundle price needs the number to justify it")
          .replace("what makes this $9 not a spreadsheet", "what makes this a game, not a spreadsheet")
          .replace("fees column matches Etsy's real 6.5%+3%+$0.25", "fees column matches Etsy's real percentage plus fixed transaction fee"))
    return re.sub(r"\$\d[\d,.]*", "the listed price", t)

P, M = [], []          # P = public-safe, M = metrics
def a(t=""): P.append(t)
def m(t=""): M.append(t)

# ---------------------------------------------------------------- public: the copy file
a("# NovalityStore - listing copy, frozen to ~10 Feb 2027")
a("")
a(f"Generated `{HEAD}` on 6 Oct 2026 by `python3 make_docs.py`. **No money or traffic figures live in "
  "this file** - they are in `NOVALITY_METRICS.md`. Paste from here, do not retype: 102 tags sit at "
  "19-20 characters and a mistyped tag is a dead slot you cannot fix until February.")
a("")
a("| § | what |")
a("|---|---|")
a("| 1 | The five rules the set was built under |")
a("| 2 | The frozen set: 36 titles + 468 tags, with what to verify first |")
a("| 3 | Compact paste table |")
a("| 4 | Every change made to the document you sent |")
a("| 5 | What was wrong with that document |")
a("| 6 | Image work list and the tile/file match rule |")
a("| 7 | Tiles on disk |")
a("| 8 | Freeze protocol |")
a("| 9 | Rules cheat-sheet |")
a("")
a("## 1. The rules this set was built under")
a("")
a("1. **First phrase = the exact query.** Etsy weights the leading words hardest and mobile cuts the title "
  "near 40 characters, so the product type has to survive the cut.")
a("2. **One phrase, one listing.** Etsy shows whichever of your own listings already has the sales, so a "
  "tag used twice is a slot spent losing to yourself. There is not one shared phrase in this set.")
a("3. **Tags carry intent, titles carry compatibility.** `Excel and Sheets` belongs in a title, where it "
  "also earns the click. `google sheets` left the tag boxes, where it only rented browse traffic.")
a("4. **A freeze is a season bet.** Seasonal crochet keeps all 13 season tags - its next window is October "
  "2027 and it needs full strength for the eight weeks that matter. Files that peak after New Year spend "
  "tail slots on January intent so December does not eat the set.")
a("5. **Unprovable numbers stay out of the text.** A wrong claim normally costs a review; in a freeze it "
  "costs four months, because you have decided not to touch it.")
a("")
a("## 2. The frozen set")
a("")
a("Validated by script: 36 listings, 13 tags each, every tag <= 20 characters, no tag contained inside "
  "another, and no phrase used by two listings. No trademark used as a tag headline except four on the "
  "Etsy seller tool. No year stamps outside the goat listing, where the year is the product.")
a("")
bad = [r for r in setos if r["verify"]]
a(f"**{len(bad)} listings carry a numeric claim in the title.** Count it in the delivered file before you "
  "paste - each is flagged under its listing.")
a("")
for r in setos:
    lid = LIVE.get(r["n"], "")
    a(f"### 2.{r['n']} {r['name']}" + (f"  ·  `listing/{lid}`" if lid else ""))
    a("")
    a(f"**Freeze lane:** {r['lane']}")
    a("")
    a(f"**Title** ({len(r['title'])} chars · mobile shows `{r['title'][:40]}...`)")
    a("")
    a("```"); a(r["title"]); a("```")
    a("")
    a("**13 tags** with their character counts")
    a("")
    a("| | | | | | |")
    a("|---|---|---|---|---|---|")
    tg = r["tags"]
    for i in range(0, 13, 3):
        cells = []
        for t in tg[i:i+3]: cells += [f"`{t}`", f"{len(t)}"]
        while len(cells) < 6: cells.append("")
        a("| " + " | ".join(cells) + " |")
    a("")
    a("_Why_: " + scrub(r["why"]))
    a("")
    if r["verify"]:
        a("**Verify before pasting:** " + scrub(r["verify"]) + ".")
        a("")
a("## 3. Compact paste table")
a("")
a("| # | live id | title | 13 tags |")
a("|---|---|---|---|")
for r in setos:
    a(f"| {r['n']} | {LIVE.get(r['n'],'')} | {r['title']} | {' / '.join(r['tags'])} |")
a("")
a("CSV twin for Sheets: `FINAL_SEO_36.csv`.")
a("")
a("## 4. Every change made to your document")
a("")
rem = add = 0; rowsx = []
for r in setos:
    o = [t.lower() for t in orig[r["n"]]]; f = [t.lower() for t in r["tags"]]
    gone = [t for t in o if t not in f]; new = [t for t in f if t not in o]
    rem += len(gone); add += len(new); rowsx.append((r["n"], r["name"], gone, new))
a(f"{rem} of 468 tag slots replaced ({rem/468:.0%}). Three reasons only: over the 20-character wall, "
  "shared with another of your own listings, or a brand/trademark used as a headline.")
a("")
a("| # | listing | out | in |")
a("|---|---|---|---|")
for n, name, gone, new in rowsx:
    if not gone and not new: continue
    a(f"| {n} | {name} | {', '.join(f'`{g}`' for g in gone) or '-'} | {', '.join(f'`{x}`' for x in new) or '-'} |")
a("")
a("Title changes: `AIA billing` out of #18; `Excel and Sheets` added to the spreadsheet titles that had "
  "room; the goat keeps `2027` in the title only; #26 now leads with `Wedding Planner Spreadsheet` "
  "instead of printable-planner phrasing.")
a("")
a("## 5. What was wrong with the document you sent")
a("")
a("| # | defect | how many | consequence |")
a("|---|---|---|---|")
a("| 1 | Tags over Etsy's 20-character limit | **37** | the field rejects the string, so the listing ships "
  "with 10 or 11 tags - and the broken ones were usually head keywords (`construction estimate`, "
  "`bookkeeping spreadsheet`, `real estate spreadsheet`) |")
a("| 2 | Phrases shared between your own listings | **43 strings / 109 slots** | you bid against yourself: "
  "`beginner crochet` on 8 listings, `google sheets budget` on all 4 budget files |")
a("| 3 | `AIA billing template` | 1 tag + 1 title | the American Institute of Architects' mark, in a shop "
  "that has already had IP takedowns |")
a("| 4 | A tag contained inside another tag of the same listing | 6 | substring matching means the short "
  "one already covers the long one - six free slots |")
a("| 5 | Title Case | 75 | harmless, but it hid how bad the collisions were: `Christmas` and `christmas` "
  "are the same string to Etsy |")
a("| 6 | Seasonality | 2 | the goat published four months early (Lunar New Year is 6 Feb 2027); "
  "`trick or treat` pulls costume shoppers into a pattern listing |")
a("| 7 | Numeric claims with no proof behind them | 5 title sets | `3 Sizes`, `24 Christmas Stockings`, "
  "`50 Templates`, `DSCR`, `52 tabs` |")
a("| 8 | It did not match the shop | 1 | no Nativity entry, though `patterns/F1-nativity-set.md` exists |")
a("")
a("What it got right, and kept: 13 multi-word tags with no filler, product keyword as the first phrase, "
  "tabs named inside spreadsheet titles, and the image rule - real finished samples, never AI shown as if "
  "real. Its own checklist survived 7 of 8 bullets; the rider on \"list every included tab\" is *only tabs "
  "you counted*. It was missing video, the price ladder, and the note that a sitewide discount is not free.")
a("")
a("## 6. Image work list, and the rule that governs it")
a("")
a("Ranked queue with the reasoning lives in `TOP15_IMAGE_QUEUE.md`. Status:")
a("")
q = open("TOP15_IMAGE_QUEUE.md").read()
tbl = re.search(r"(\| # \| listing.*?\n\n)", q, re.S)
rows = [l for l in tbl.group(1).strip().splitlines() if l.startswith("|")]
a("| " + " | ".join([c for i, c in enumerate([x.strip() for x in rows[0].strip('|').split('|')]) if i not in (3, 4)]) + " |")  # header, same columns
keep = [2, 5]
a("|" + "---|" * 5)
for l in rows[2:]:
    cs = [c for i, c in enumerate([x.strip() for x in l.strip('|').split('|')]) if i not in (3, 4)]
    # the queue's reasoning column quotes prices; rephrase rather than drop, then backstop
    for i, c in enumerate(cs):
        cs[i] = (c.replace("price, Q4 demand and the $10 ad floor", "price, Q4 demand and the ad floor")
                  .replace("$45 needs the most trustworthy tile", "the price needs the most trustworthy tile"))
    cs = [re.sub(r"\$\d[\d,.]*", "(see the metrics file)", c) for c in cs]   # no money in this file
    a("| " + " | ".join(cs) + " |")
a("")
a("*(price columns deliberately dropped here - they are in the metrics file and on Etsy; this file is the "
  "one you might print or share.)*")
a("")
a("**The tile must describe the file that downloads.** Two live examples of what that means:")
a("")
a("1. The Crochet Craft Fair gallery's image 10 is, in Etsy's own alt text, \"a digital monthly summary "
  "dashboard for a **catering business** manager\" - a screenshot from a different listing. Delete it.")
a("2. **Listing `4577821049` is a mismatch waiting to happen.** Its live description sells a 9-page PDF: "
  "24 mini stockings in 2 sizes (2.5in and 4in), 6 cuff variations, an A-Z monogram chart, a bonus 12-mini "
  "version, about 120g of scrap yarn, roughly 40 minutes each. The tile built for it (`01-main.png`) "
  "headlines 24 **numbered** motifs, a 1-24 chart and 24 gift notes - which is `patterns/F3-advent-garland.md`, "
  "a different file that has not been uploaded and is not yet worked by hand. **Do not paste those "
  "tiles with the current file, and do not swap in F3 without deciding what happens to the 2 sizes, the "
  "monogram chart and the 12-mini bonus.** Either extend F3 to absorb them or keep your file and use the "
  "honest-tile spec for what you actually ship. That is the exact shape of the 1-star review: picture and "
  "file disagreeing.")
a("")
a("## 7. Tiles on disk")
a("")
a("| listing | file | raw link (needs repo access now the repo is private) |")
a("|---|---|---|")
for d in sorted(os.listdir("tiles")):
    for fn in sorted(os.listdir(os.path.join("tiles", d))):
        a(f"| `{d}` | `{fn}` | https://github.com/arbabkhan007/Etsy-Overall/raw/{BR}/tiles/{d}/{fn} |")
a("")
a("All 2700 x 2025 (Etsy's square display crop). `make_tile.py` is the generator, and the honesty rule is "
  "in the code: pattern tiles can only paste rasterised pages of the real PDF, spreadsheet tiles draw real "
  "tab names over an empty grid. If you need a link a buyer or a VA can open without GitHub access, "
  "download the PNG and put it wherever you keep working files - do not re-publicise the repo.")
a("")
a("## 8. Freeze protocol")
a("")
a("- Do all 36 in **one sitting**, this week. Every day of drift is a day of the Q4 ramp you do not get back.")
a("- **Expect a 3-10 day wobble in impressions**, then a rebuild. That dip is the crawl re-matching, not a "
  "verdict. Reacting to it is the single most expensive mistake available inside a freeze.")
a("- The freeze covers titles and tags only. Sale, prices, ads, images and video stay adjustable - and that "
  "is where the quarter is actually won (see the metrics file).")
a("- One exception: listing #14 (Halloween) is out of season inside this window. Paste it, ignore it, "
  "revisit in August.")
a("- If a listing is already ranking, change **tags only** - a title edit resets the match you rank on. "
  "This set changes both, so do it in one sitting rather than rolling, and let the re-learning happen once.")
a("")
a("## 9. Rules cheat-sheet")
a("")
a("- **Tags are the brief for the tile, not the copy on it.** Tags choose which promise the picture headlines.")
a("- **Count, then claim.** Declared counts must equal delivered counts - in files, tabs, formulas and tiles.")
a("- **Never let a number on a tile be true of the repo but false of the product.**")
a("- **A freeze applies to text, not to money.**")
a("- **Many visits and no sales is that listing's pictures. Few views is discovery.** Diagnose before editing.")
a("- **Seasons have publish dates:** 27 Oct last useful publish for Christmas ranking, 27 Nov Black Friday, "
  "12 Dec last day a hand-finished item lands, 6 Feb 2027 Lunar New Year.")
a("")

# ---------------------------------------------------------------- private: metrics
m("# NovalityStore - the numbers file")
m("")
m("**Keep this private.** It is not in the copy file on purpose: your traffic, your conversion rates, your "
  "fee maths and your price ladder are the parts of this business a competitor would use.")
m("")
m(f"Generated `{HEAD}`, 6 Oct 2026. Source: your Stats read on 4 Oct, and `CROCHET_Q4_FIVE.md`.")
m("")
m("## 1. The shop, measured")
m("")
m("| metric | value |")
m("|---|---|")
for k, v in [("lifetime views","1,569"),("lifetime visits","1,065"),("orders","11"),("revenue","$54.54"),
             ("ad spend","$21.91"),("**net lifetime**","**$22.50**"),("average order value","$4.96"),
             ("conversion, lifetime","**1.03%** = 11 / 1,065"),("conversion, September","**2.86%** = 4 / 140 "
             "(`CROCHET_Q4_FIVE.md:246`)"),("sales rate","~0.8 / week"),("reviews","3.7 stars, 3 reviews"),
             ("listings","36, every one on a permanent 25% off"),("time on Etsy","4 months")]:
    m(f"| {k} | {v} |")
m("")
m("The governing review (Kim, 1 star): *\"the instructions for the arms and legs would have looked NOTHING "
  "like the picture... Use a REAL photo.\"* That review, not the star average, is why the tile rules exist.")
m("")
m("## 2. The target, inside the freeze window")
m("")
WK, TGT = 17, 1000.0
m(f"6 Oct 2026 - 31 Jan 2027 = **{WK} weeks**, so **${TGT/WK:,.2f} gross per week** is the target. "
  "Fees: `net = 0.905 x price - $0.45`.")
m("")
m("| basket | sales/wk | total sales | views/wk @ 2.86% | views/wk @ 1.03% | net per sale |")
m("|---|---|---|---|---|---|")
for aov in (4.96, 8.0, 12.0, 14.0, 19.0, 24.0, 28.12):
    spw = (TGT / WK) / aov
    m(f"| ${aov:.2f} | {spw:.1f} | {spw*WK:.0f} | {spw/0.0286:.0f} | {spw/0.0103:.0f} | ${0.905*aov-0.45:.2f} |")
m("")
m("Today's trajectory - 0.8 sales a week at $4.96 - is **$67 over the whole window**. The September rate "
  "(2.86%) flatters you: at the lifetime rate (1.03%) a $14 basket needs ~410 views a week against the "
  "~92 you get now. Both readings say the same thing: **this is a basket-size problem with a discovery "
  "tailwind, not a tags problem.**")
m("")
m("## 3. What closes the gap, cheapest first")
m("")
m("| # | action | effect |")
m("|---|---|---|")
m("| 1 | Re-price the advent garland (F3) $4.50 to **$13.29** | +$8.83 gross, +$7.99 net on every sale of "
  "a file you have already written |")
m("| 2 | List **bundle A ($34 to $19)** and **bundle B ($46 to $24)** - written, not yet listed | $16.75 "
  "and $21.27 net each; three sales of each is about $114 |")
m("| 3 | Buy 1, get 2nd at 40% on crochet singles | moves AOV from $4.96 toward $8 without touching a title |")
m("| 4 | Kill the permanent sitewide 25% | it is why $4.96 is your average, and it teaches buyers to wait |")
m("| 5 | One 5-15s video on the five best earners | this is the step that turned a $2 PDF into a $12 one |")
m("| 6 | Finish the tiles, one listing at a time | 3 of 15 rows done; row 4 is the wedding thumbnail crop |")
m("")
m("Modelled bands for Q4: as-is **$265**, + bundles **$473**, + bundles with re-pointed $5/day ads "
  "**$788**. Scaled to the 17-week window the top band is about **$1,030** - so $1,000 is reachable, but "
  "only with all three levers firing. Tags alone land near $350.")
m("")
m("## 4. Ads")
m("")
m("| fact | value |")
m("|---|---|")
m("| lifetime ad spend | $21.91 on $54.54 revenue |")
m("| implied | you have been paying for traffic you did not convert |")
m("| floor | Etsy needs about $5/day before an ad learns; below that it is noise |")
m("| where | only the listings with net/sale of $8 or better: the gift tracker, the craft fair tracker, the "
  "wedding and budget bundles, construction at $45 |")
m("| read after 7 days | Promoted Impressions and the CVR under each listing's search-term analytics - the "
  "only per-query data Etsy still gives sellers |")
m("")
m("## 5. The five crochet picks, by what they actually pay")
m("")
m("| pick | net per sale |")
m("|---|---|")
for k, v in [("F5 bundle","$28.37"),("F2 lovies","$19.90"),("F1 nativity","$15.38"),
             ("F3 advent garland","$11.58"),("F4 stockings","$10.40")]:
    m(f"| {k} | {v} |")
m("")
m("## 6. Pattern pack - the honest status line")
m("")
m("`TEST_STATUS: untested` stays inside `patterns/F1`, `F2` and `F4` until you stitch them; F3 has "
  "machine-verified round counts and a 14-page PDF but has not been worked by hand either. It is not a "
  "formality - the whole reason your 1-star exists is a picture and a file disagreeing. When you stitch "
  "F3, that flips and I rebuild the PDFs, the tiles and the zip in one pass.")
m("")
m("Also open: `patterns/charts/nativity-link-stitch.md` is referenced by F1 and does not exist in the pack.")
m("")
m("## 7. What is still owed")
m("")
m("| item | why it blocks |")
m("|---|---|")
m("| one .xlsx | 17 titles carry numeric claims I cannot verify; in a freeze those become four-month "
  "commitments |")
m("| bundles A and B listed | the largest basket-size lever in section 3 |")
m("| Promoted Impressions + CVR after 7 days | decides whether $5/day stays |")
m("| a decision on F3 vs the live stocking file | the tiles for `4577821049` cannot be pasted until the "
  "file matches the picture |")
m("| one stitched F3 | the only thing that flips `TEST_STATUS` |")
m("| nativity chart file | F1 promises it |")
m("")
m("## 8. Keeping this file private")
m("")
m("This repo is now private, so these numbers are off the open web - but note two things. Anything already "
  "published at a raw GitHub URL can still sit in search caches, so do not re-share old links; and the "
  "history of this repo contains earlier versions of a public file, which is fine inside a private repo "
  "and would matter again the moment it is made public. If you ever want a shareable copy of just the "
  "listing text, that is `NOVALITY_LISTINGS.md`, which is built to contain no figures at all.")

os.makedirs(".", exist_ok=True)
open("NOVALITY_LISTINGS.md","w").write("\n".join(P)+"\n")
open("NOVALITY_METRICS.md","w").write("\n".join(M)+"\n")

# ---------------------------------------------------------------- guards
pub = "\n".join(P); met = "\n".join(M)
leaks = [w for w in ["$","2.86","1.03","1,569","1,065","0.905","CVR","forecast","/wk","net per sale",
                    "TEST_STATUS","re-price","bundle A","sales/wk"] if w in pub]
grid = []
for ln in pub.splitlines():
    ls = ln.strip()
    if not (ls.startswith("| `") and ls.endswith("|")): continue
    cells = [c.strip() for c in ls.strip("|").split("|")]
    while cells and cells[-1] == "": cells.pop()
    if len(cells) % 2 or not all(re.fullmatch(r"`[^`]+`", c) for c in cells[0::2]) or not all(c.isdigit() for c in cells[1::2]): continue
    grid += [(c.strip("`"), int(n)) for c, n in zip(cells[0::2], cells[1::2])]
assert len(setos) == 36 and all(len(r["tags"]) == 13 for r in setos)
assert not [t for r in setos for t in r["tags"] if len(t) > 20]
assert not [x for x in grid if len(x[0]) != x[1]], "rendered length disagrees with the tag"
assert len(grid) == 468, len(grid)
blob = " ".join(t for r in setos for t in r["tags"]).lower()
assert "aia" not in blob and "disney" not in blob
assert not [t for r in setos if r["n"] != 2 for t in r["tags"] if re.search(r"20\d\d", t)]
own = collections.Counter(t.lower() for r in setos for t in r["tags"])
assert not [t for t, c in own.items() if c > 1], "a phrase is on two listings"
print(f"NOVALITY_LISTINGS.md {len(pub):,} B  |  NOVALITY_METRICS.md {len(met):,} B")
print(f"guards: {len(grid)}/468 tag cells verified against their printed lengths; "
      f"leak check on the public file -> {'FAIL ' + str(leaks) if leaks else 'clean, no $ or traffic figures'}")
if leaks: raise SystemExit(1)
print("money figures present in the metrics file:", sum(1 for _ in re.finditer(r"\$\d", met)), "occurrences")
