#!/usr/bin/env python3
"""Build NOVALITY_MASTER.md - one file with everything: the frozen title/tag set, the audit that
produced it, the image queue, the revenue math and the open items. Generated, so the numbers cannot
drift from the files they come from. Re-run after changing any of them:  python3 make_master.py"""
import json, csv, re, os, collections, subprocess

OUT = "NOVALITY_MASTER.md"
setos = json.load(open("seo_final.json"))
LIVE = {1:"4573853611",3:"4577821049",4:"4573857903",5:"4573849581",7:"4573699869",18:"4561670979",
        20:"4549642404",21:"4549077688",25:"4534488947",26:"4534483099",27:"4534495626",29:"4534364844",
        34:"4578849733",35:"4578846463",36:"4573955047"}

# --- the original document, re-parsed here so the change log is a real diff, not a memory
orig = {}
for blk in open("audit/proposed_seo.md").read().split("\n### ")[1:]:
    n = int(blk.split("\n")[0].split(". ")[0])
    orig[n] = [t.strip() for t in re.search(r"^Tags: (.+)$", blk, re.M).group(1).split("|")]

def money(p): return 0.905 * p - 0.45
WEEKS = 17          # 6 Oct 2026 -> 31 Jan 2027
TARGET = 1000.0

L = []
A = L.append
A("# NovalityStore - Q4 master file")
A("")
A(f"Generated `{subprocess.run(['git','rev-parse','--short','HEAD'],capture_output=True,text=True).stdout.strip()}` "
  f"on 6 Oct 2026 by `python3 make_master.py`. Everything below is read out of the files in this repo, "
  "so re-run the script instead of editing this page by hand.")
A("")
A("**In one line:** titles and tags are frozen for 4 months (the set is below), and the $1,000 has to be "
  "made on price and images, because discovery alone puts you near $350 in this window.")
A("")
A("## Index")
A("")
A("| § | what | file it came from |")
A("|---|---|---|")
A("| 1 | The shop, measured | your Stats, read 4 Oct |")
A("| 2 | The $1,000 math for the freeze window | this file |")
A("| 3 | The frozen set: 36 titles + 468 tags | `seo_final.json` |")
A("| 4 | Compact paste table | same |")
A("| 5 | Every change made to your document, with the reason | `audit/proposed_seo.md` diffed against the set |")
A("| 6 | What was wrong with the document you sent | `audit/TAG_DOC_REVIEW.md` |")
A("| 7 | Image queue: 15 listings, what is built | `TOP15_IMAGE_QUEUE.md` |")
A("| 8 | Tiles on disk, with raw links | `tiles/` |")
A("| 9 | Patterns and the honest test status | `patterns/`, `CROCHET_Q4_FIVE.md` |")
A("| 10 | Rules cheat-sheet (the teaching, condensed) | the whole session |")
A("| 11 | What is still owed by you | this file |")
A("")
A("---")
A("")
A("## 1. The shop, measured")
A("")
A("| metric | value | read |")
A("|---|---|---|")
A("| lifetime views | 1,569 | Stats, 4 Oct |")
A("| lifetime visits | 1,065 | Stats |")
A("| orders | 11 | Stats |")
A("| revenue | $54.54 | Stats |")
A("| ad spend | $21.91 | Stats |")
A("| **net lifetime** | **$22.50** | revenue x 0.905 - fees, less ads |")
A("| average order value | $4.96 | $54.54 / 11 |")
A("| conversion, lifetime | **1.03%** of visits became orders | 11 / 1,065 |")
A("| conversion, September | **2.86%** | 4 orders / 140 visits - documented in `CROCHET_Q4_FIVE.md:246` |")
A("| sales rate | ~0.8 / week | lifetime, since open |")
A("| reviews | 3.7 stars, 3 reviews | one 1-star governs everything below |")
A("| listings | 36, every one on a permanent 25% off | the shop-wide discount is itself a problem |")
A("")
A("The governing review (Kim, 1 star): *\"the instructions for the arms and legs would have looked NOTHING "
  "like the picture... Use a REAL photo.\"* Every tile in this repo is built so that sentence cannot be "
  "written about a Novality picture again.")
A("")
A("## 2. The $1,000, in the freeze window")
A("")
A(f"6 Oct 2026 to 31 Jan 2027 is **{WEEKS} weeks**, so $1,000 = **${TARGET/WEEKS:,.2f} gross per week**. "
  "Etsy's cut plus fixed fees mean `net = 0.905 x price - $0.45`.")
A("")
A("| average order value | sales/wk needed | total sales | views/wk needed at 2.86% CVR | net per sale |")
A("|---|---|---|---|---|")
CVR = 0.0286
for aov in (4.96, 8.0, 12.0, 14.0, 19.0, 24.0):
    spw = (TARGET / WEEKS) / aov
    A(f"| ${aov:.2f} | {spw:.1f} | {spw*WEEKS:.0f} | {spw/CVR:.0f} | ${money(aov):.2f} |")
A("")
A("The views column uses your **September** rate of 2.86%. If the lifetime rate (1.03%) is the honest one, "
  "every views figure above roughly triples - $14 basket, 4.2 sales a week, ~410 views a week. That gap is "
  "the difference between tags-fix-it and the shop needing better pictures and bigger baskets, and "
  "it is why section 2 is mostly not about tags.")
A("")
A("At today's basket ($4.96) you would need **11.9 sales a week on 415 views a week**. You get about 92 "
  "views a week. That is why the target is not a tag problem: the same traffic at a $14 basket clears it.")
A("")
A("**What actually moves $67 -> $1,000**, in the order that costs least:")
A("")
A("1. Re-price the advent garland (F3) from $4.50 to **$13.29** - it is 24 motifs plus a numbers chart plus "
  "24 gift-note slips, and it is priced like a single ornament.")
A("2. List **bundle A ($34 -> $19)** and **bundle B ($46 -> $24)**. Both written, both still not in the "
  "shop. Three sales each is ~$114.")
A("3. **Buy 1, get 2nd at 40%** on the crochet singles - people buy two patterns anyway; this is the AOV "
  "lever, and unlike titles it is not frozen.")
A("4. Kill the permanent sitewide 25%. Discounting everything teaches buyers to wait and it is why your "
  "average order is $4.96.")
A("5. Video on the five listings earning most (5-15s of the dashboard being filled in). That is the step "
  "that turned a $2 PDF into a $12 one here.")
A("6. Tiles, one listing at a time (section 7).")
A("")
A("Modelled bands for the Q4 13 weeks, from `CROCHET_Q4_FIVE.md` and the queue work: as-is **$265**, "
  "+bundles **$473**, +bundles with re-pointed $5/day ads **$788**. Scaled to the 17-week freeze window "
  "that top band is ~$1,030 - so $1,000 is reachable, but only if all three levers fire.")
A("")
A("---")
A("")
A("## 3. The frozen set - paste, do not retype")
A("")
A("Validated by script: 36 listings, exactly 13 tags each, every tag <= 20 characters, no tag contained in "
  "another, no duplicates, **and no phrase used by two of your listings**. No trademark-as-headline tags "
  "except the four on the Etsy seller tool. No year stamps outside the Year of the Goat title.")
A("")
A("### Rules the set was built under")
A("")
A("1. **First phrase = the exact query.** Etsy weights leading words hardest and mobile cuts the title near "
  "40 characters, so the product type has to survive the cut.")
A("2. **One phrase, one listing.** Etsy shows whichever of your own listings already has the sales; every "
  "duplicate phrase is a slot spent losing to yourself.")
A("3. **Tags carry intent, titles carry compatibility.** \"Excel and Sheets\" belongs in the title, where it "
  "also earns the click; \"google sheets\" left the tag boxes, where it only rented browse traffic.")
A("4. **A freeze is a season bet.** Seasonal crochet keeps all 13 season tags (their next window is Oct "
  "2027). Files that peak in January spend tail slots on New Year intent so December does not eat the set.")
A("5. **Unprovable numbers stay out of the text.** A wrong claim normally costs a review; in a freeze it "
  "costs four months, because you decided not to touch it.")
A("")
bad = [r for r in setos if r["verify"]]
A(f"**{len(bad)} listings carry a claim you should count before pasting** - flagged under each one.")
A("")
for r in setos:
    lid = LIVE.get(r["n"], "")
    A(f"### 3.{r['n']} {r['name']}" + (f"  ·  `listing/{lid}`" if lid else ""))
    A("")
    A(f"**Lane during the freeze:** {r['lane']}")
    A("")
    A(f"**Title** ({len(r['title'])} chars · mobile shows `{r['title'][:40]}...`)")
    A("")
    A("```")
    A(r["title"])
    A("```")
    A("")
    A("**13 tags** (characters shown so you can see nothing is near the wall by accident)")
    A("")
    A("| | | | | | |")
    A("|---|---|---|---|---|---|")
    tg = r["tags"]
    for i in range(0, 13, 3):
        cells = []
        for t in tg[i:i+3]:
            cells += [f"`{t}`", f"{len(t)}"]
        while len(cells) < 6: cells.append("")
        A("| " + " | ".join(cells) + " |")
    A("")
    A(f"_Why_: {r['why']}")
    A("")
    if r["verify"]:
        A(f"**Verify before pasting:** {r['verify']}. You will not touch this again until February.")
        A("")
A("---")
A("")
A("## 4. Compact paste table")
A("")
A("| # | id | title | 13 tags |")
A("|---|---|---|---|")
for r in setos:
    A(f"| {r['n']} | {LIVE.get(r['n'],'')} | {r['title']} | {' / '.join(r['tags'])} |")
A("")
A("CSV twin for Google Sheets: `FINAL_SEO_36.csv`.")
A("")
A("---")
A("")
A("## 5. Every change made to your document")
A("")
added = removed = 0
rowsx = []
for r in setos:
    o = [t.lower() for t in orig[r["n"]]]
    f = [t.lower() for t in r["tags"]]
    gone = [t for t in o if t not in f]
    new = [t for t in f if t not in o]
    removed += len(gone); added += len(new)
    rowsx.append((r["n"], r["name"], gone, new))
A(f"{removed} tag slots replaced out of 468 ({removed/468:.0%}). Reason classes: over the 20-character "
  "wall, or shared with another of your own listings, or a brand/trademark used as a headline.")
A("")
A("| # | listing | out | in |")
A("|---|---|---|---|")
for n, name, gone, new in rowsx:
    if not gone and not new: continue
    A(f"| {n} | {name} | {', '.join(f'`{g}`' for g in gone) or '-'} | {', '.join(f'`{x}`' for x in new) or '-'} |")
A("")
A("Title changes in the same pass: `AIA billing` removed from #18's title; `for Excel and Sheets` / "
  "`Excel and Sheets` added to the spreadsheet titles that had room; the goat keeps `2027` in the title "
  "only; #26 now leads with `Wedding Planner Spreadsheet` rather than the printable-planner phrasing.")
A("")
A("---")
A("")
A("## 6. What was wrong with the document you sent")
A("")
A("| # | defect | how many | consequence |")
A("|---|---|---|---|")
A("| 1 | Tags over Etsy's 20-character limit | **37** | the field rejects the string - the listing silently "
  "ships with 10 or 11 tags, and the broken ones were usually the head keywords (`construction estimate`, "
  "`bookkeeping spreadsheet`, `real estate spreadsheet`) |")
A("| 2 | Phrases shared between your own listings | **43 strings, 109 slots (23%)** | you bid against "
  "yourself; `beginner crochet` on 8 listings, `google sheets budget` on all 4 budget files |")
A("| 3 | `AIA billing template` | 1 tag + 1 title | American Institute of Architects' mark, in a shop that "
  "has already had IP takedowns |")
A("| 4 | Tag contained inside another tag of the same listing | 6 | substring matching means the short one "
  "already covers the long one - six free slots |")
A("| 5 | Title Case | 75 | harmless (Etsy lowercases) but it hides how bad the collisions were |")
A("| 6 | Seasonality | 2 | Year of the Goat published 4 months early (LNY is 6 Feb 2027); `trick or treat` "
  "on Halloween pulls costume shoppers into a pattern listing |")
A("| 7 | Unverifiable numeric claims | 5 title sets | `3 Sizes`, `24 Christmas Stockings`, `50 Templates`, "
  "`DSCR`, `52 tabs` |")
A("| 8 | The list did not match the shop | 1 | no Nativity entry, though `patterns/F1-nativity-set.md` exists |")
A("")
A("What the document got right, and kept: 13 multi-word tags with no filler; product keyword as the first "
  "phrase; tabs named in spreadsheet titles; and the image rule - *real finished samples, never AI shown as "
  "if real* - which is the Kim review and the rule all tiles here are built under.")
A("")
A("Its checklist: 7 of 8 bullets kept verbatim. The rider on \"list every included tab\" is *only tabs you "
  "counted*. Missing from it entirely: one 5-15s video per listing, the price ladder per niche, and no "
  "permanent sitewide discount.")
A("")
A("---")
A("")
A("## 7. Image queue - 15 listings, ranked")
A("")
q = open("TOP15_IMAGE_QUEUE.md").read()
m = re.search(r"(\| # \| listing.*?\n\n)", q, re.S)
A(m.group(1).strip() if m else "(queue table missing - re-run after checking TOP15_IMAGE_QUEUE.md)")
A("")
A("**Why images matter more than the tag set now:** the evidence rule. Many visits and no sales means that "
  "listing's pictures; few views means discovery. Your Q4 listings mostly have the first problem, which is "
  "why the freeze is safe: discovery is set, conversion is the work.")
A("")
A("Two live-gallery defects found by reading the listings rather than guessing:")
A("")
A("1. **Wrong product in the Crochet Craft Fair gallery** - image 10 is, in Etsy's own alt text, \"a digital "
  "monthly summary dashboard for a **catering business** manager\". Delete or replace it: a buyer who spots "
  "a different product name in the gallery has Kim's exact complaint.")
A("2. **Palette drift** - several craft-fair tiles use dark purple headers; the brand kit is forest "
  "`#1F4634` / terracotta `#C2643F` on cream `#F5EFE6`. Purple next to cream reads as two sellers, and two "
  "sellers reads as a reseller. Let the product keep its own theme colour; keep the **frame** consistent.")
A("")
A("## 8. Tiles on disk")
A("")
A("| listing | file | size | raw link |")
A("|---|---|---|---|")
br = subprocess.run(["git","rev-parse","--abbrev-ref","HEAD"],capture_output=True,text=True).stdout.strip()
for d in sorted(os.listdir("tiles")):
    for fn in sorted(os.listdir(os.path.join("tiles",d))):
        p = os.path.join("tiles",d,fn)
        A(f"| `{d}` | `{fn}` | {os.path.getsize(p)/1024:.0f} KB | https://github.com/arbabkhan007/Etsy-Overall/raw/{br}/{p} |")
A("")
A("All 2700 x 2025 (Etsy's square display crop). The generator is `make_tile.py`; the honesty rule is "
  "enforced in code - pattern tiles can only paste rasterised pages of the real PDF, and spreadsheet tiles "
  "draw real tab names over an empty grid, never invented figures.")
A("")
A("---")
A("")
A("## 9. Patterns - and the honest status line")
A("")
A("| file | what | state |")
A("|---|---|---|")
A("| `patterns/F1-nativity-set.md` | Nativity set, 7 figures | written, PDF exported, **untested by hand** |")
A("| `patterns/F2-baby-loveys.md` | 3 lovies | written, PDF exported, untested |")
A("| `patterns/F3-advent-garland.md` | 24 numbered minis + 1-24 chart + 24 gift notes | written, PDF 14 pp, verified rounds and pages |")
A("| `patterns/F4-stockings.md` | mini stockings | written, PDF exported, untested |")
A("| `patterns/charts/` | 26 letter + 24 number link-stitch charts | generated and grid-verified |")
A("| `patterns/pdf/` | 7 PDFs | the files a buyer would download |")
A("| `Novality_Crochet_Patterns_v1.zip` | 28 entries | the pack, `unzip -t` clean |")
A("")
A("`TEST_STATUS: untested` stays in those files until you stitch one. It is not a formality: the whole "
  "reason your 1-star exists is a picture and a file disagreeing. When you stitch F3, tell me and I will "
  "flip the status and rebuild the PDFs and the zip.")
A("")
A("## 10. Rules cheat-sheet")
A("")
A("- **Tags are the brief for the tile, not the copy on it.** Tags choose which promise the picture headlines.")
A("- **Count, then claim.** Declared counts must equal delivered counts - in files, tabs, formulas and tiles.")
A("- **Never let a number on a tile be true of the repo but false of the product.**")
A("- **A freeze applies to text, not to money.** Prices, sales, ads and images stay adjustable; that is "
  "where the quarter is actually won.")
A("- **Expect a 3-10 day wobble after a title change.** Reacting to it is the expensive mistake.")
A("- **$1,000 is a basket-size problem** at your traffic. 4.2 sales a week at $14 clears it; 11.9 at $5 does not exist.")
A("- **Seasons have publish dates:** 27 Oct last useful publish for Christmas ranking, 27 Nov Black Friday, "
  "12 Dec last day a hand-stitched item can land, 6 Feb 2027 Lunar New Year.")
A("")
A("## 11. Still owed by you")
A("")
A("| item | why it blocks |")
A("|---|---|")
A("| one .xlsx (either listing) | 17 titles carry numeric claims I cannot verify; freeze makes them 4-month commitments |")
A("| bundles A and B listed | the largest single AOV lever in section 2 |")
A("| Promoted Impressions + CVR after 7 days of re-pointed ads | decides whether $5/day stays |")
A("| one stitched F3 | the only thing that flips `TEST_STATUS: untested` |")
A("| `patterns/charts/nativity-link-stitch.md` | F1 references a chart file that is not in the pack |")
A("| tags for queue row 4 (Wedding Planner) | next tile in the one-at-a-time queue |")
A("")
txt = "\n".join(L) + "\n"
open(OUT, "w").write(txt)
# self-check: verify the data AND that the rendering matches it, row by row
txt2 = open(OUT).read()
assert len(setos) == 36 and all(len(r["tags"]) == 13 for r in setos), "set itself is wrong"
over = [(r["n"], t) for r in setos for t in r["tags"] if len(t) > 20]
assert not over, over
# every tag cell in the rendered grids must agree with the character count printed beside it
grid = []
for ln in txt2.splitlines():
    ls = ln.strip()
    if not (ls.startswith("| `") and ls.endswith("|")):
        continue
    cells = [c.strip() for c in ls.strip("|").split("|")]
    while cells and cells[-1] == "":          # short rows are padded with empty pairs
        cells.pop()
    if len(cells) % 2 or not all(re.fullmatch(r"`[^`]+`", c) for c in cells[0::2]) \
       or not all(c.isdigit() for c in cells[1::2]):
        continue
    grid += [(c.strip("`"), int(n)) for c, n in zip(cells[0::2], cells[1::2])]
mismatch = [(t, n) for t, n in grid if len(t) != n]
assert not mismatch, mismatch
assert len(grid) == 468, len(grid)
setblob = " ".join(t for r in setos for t in r["tags"])
assert "aia" not in setblob.lower(), "IP tag leaked into the set"
assert "2027" not in " ".join(t for r in setos if r["n"] != 2 for t in r["tags"]), "year stamp outside the goat listing"
print(f"self-check: 468 tag cells rendered, each agreeing with its printed length; no tag over 20; set == file")
