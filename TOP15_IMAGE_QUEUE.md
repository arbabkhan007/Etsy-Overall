# Top 15 listings — image queue

Built Oct 3 2026 from the live storefront (33 of the 36 listings came back in the fetch; three are
not visible from outside the shop). Ranking is a **proxy**, not Etsy data: the one input that would
beat it is your per-listing Views from Stats, and if you paste that column I will re-order in one
pass. What it does use is real: your live price, what one extra sale nets you after Etsy's 6.5% +
3% + $0.25, whether the thumbnail is currently being cropped by Etsy, and whether the keyword has a
Q4 window that closes on **Oct 27**.

`net/sale = 0.905 x realised - 0.45`. Offsite ads fee (15%) is not included.

## The rule that governs every image here

Your worst review is an image review, not a pattern review:

> *"I'm sick of this AI crap infiltrating etsy! ... the instructions for the arms and legs would
> have looked NOTHING like the picture. This product is very misleading. Use a REAL photo or make
> the pattern to actually reflect the AI garbage photo you used."* — Kim, 1 star, Aug 13, on the
> axolotl listing (4553803418).

That is a 3.7 average rating with 3 stars, and it is why a crochet pattern in your shop cannot be
sold with a fabricated finished object. So every tile in this queue follows one rule: **the image may
only contain something that exists in the file the buyer receives.**

- Spreadsheets: a real screenshot of that workbook, in a clean device frame. Numbers from your file,
  never invented ones.
- Patterns: the actual PDF page (rounds, chart, gauge table) and the real motif grid, composed on the
  brand background. I can rasterise `patterns/pdf/*.pdf` directly, so these tiles are honest by
  construction.
- AI generation is allowed only for *props and setting* (a wooden hook, a ball of yarn, a folded
  blank, a desk surface) — never for the product's content, and never as a finished object.

## The queue

| # | listing | id | realised | net/sale | why the image matters | tile |
|---|---|---|---|---|---|---|
| 1 | Christmas Gift Tracker Spreadsheet | 4573955047 | $11.99 | $10.40 | only listing where price, Q4 demand and the $10 ad floor overlap | A |
| 2 | Crochet Craft Fair Tracker Spreadsheet | 4578849733 | $9.74 | $8.36 | **done** - tiles built; live gallery also needs the catering image removed | A |
| 3 | Secret Santa Spreadsheet | 4578846463 | $8.99 | $7.69 | pure Q4, buyer decides in one glance, currently a plain grid shot | A |
| 4 | Wedding Planner Spreadsheet, 52 Tabs | 4534483099 | $11.99 | $10.40 | Etsy is cropping this thumbnail off-centre; the "52" is the whole pitch | A |
| 5 | Personal Finance Spreadsheet Bundle | 4534488947 | $10.49 | $9.04 | also cropped; a bundle must look like a bundle | A |
| 6 | Budget Spreadsheet Bundle, 50 Templates | 4534495626 | $28.12 | $25.00 | one extra sale here = six pattern sales | A |
| 7 | Construction Estimate Spreadsheet Bundle | 4561670979 | $45.00 | $40.27 | biggest single sale in the shop; $45 needs the most trustworthy tile | A |
| 8 | School Management Spreadsheet | 4549077688 | $26.24 | $23.30 | institutional buyer, checks competence in the first image | A |
| 9 | Home Renovation Budget Spreadsheet | 4549642404 | $16.49 | $14.47 | high-intent search, emotional purchase, tile is the difference | A |
| 10 | Etsy Shop Spreadsheet | 4534364844 | $13.49 | $11.76 | you are the customer; a screenshot of your own numbers is the proof | A |
| 11 | Crochet Christmas Tree Skirt Pattern | 4573853611 | $7.50 | $6.34 | F-ready listing, needs the 3-sizes row and a real page | B |
| 12 | Crochet Mini Stocking / Advent Garland | 4577821049 | $4.50 | $3.63 | becomes F3 at $13.29 - the tile must show 24 motifs, not one | B |
| 13 | Crochet Christmas Wreath Pattern | 4573857903 | $6.75 | $5.65 | door-decor buyers browse on image alone | B |
| 14 | Crochet Christmas Ornament Bundle 3-in-1 | 4573849581 | $4.50 | $3.63 | bundle framing is the only way a $4.50 file reads as more than one | B |
| 15 | No Sew Christmas Gnome Pattern | 4573699869 | $4.50 | $3.63 | "no sew" is the differentiator and it is invisible in the current tile | B |

Lane A = spreadsheet tiles (evergreen; the image keeps paying all year). Lane B = the five crochet
listings that the Q4 window and the new pattern PDFs are about to upgrade - these are the ones where
I can build the whole tile from files already in this repo.

## Not in the top 15, on purpose

Sea turtle $2.25, chenille duck $2.25, axolotl $3.37, capybara $3.37, loaf cat $3.37, bunny lovey
$3.75, goat 2027 $3.75, baby dragon $5.25, highland cow $5.25, halloween bundle $6.00, emotional
support bundle $4.50. A new picture on a $3.37 listing earns about $2.57 more per sale and the maths
does not clear the hour of work; those need a **price and tier change** first (single $6.99 / set /
everything), and after that they deserve tiles too. The halloween bundle is 28 days past its window.

## Workflow, one at a time

For each row: you send the 13 tags you want on that listing (and for Lane A, one screenshot of the
real workbook), I build the tile set - 2700x2025 main, plus the feature tile and the what-you-get
tile - as PNGs in `dist/tiles/<id>/`, with the tag words used as the on-image chips where they are
true claims. Nothing goes into the image that is not in the file.

## Built so far

| listing | tiles | how |
|---|---|---|
| 4577821049 advent garland (F3) | `tiles/4577821049/01-main.png`, `02-contents.png`, `03-honest.png` | real PDF pages + the real 1-24 chart sheet, rasterised from `patterns/pdf/` |
| 4578846463 secret santa | `tiles/4578846463/01-rules.png` | rules diagram - labelled as an illustration, because it is one |
| 4578849733 craft fair tracker | `tiles/4578849733/01-main.png`, `02-editions.png` | tab strip drawn from the tab names in his own live images - deliberately **no** cells filled with invented figures |

## Two defects found in the live image sets (these outrank any new tile)

1. **Wrong product inside the crochet listing.** `4578849733` image #10 is described by Etsy as
   "a digital monthly summary dashboard for a **catering business** manager" - that is the Catering
   Spreadsheet's screenshot sitting in the Craft Fair Tracker's gallery. Delete it or swap it for the
   crochet dashboard. A buyer who notices the name mismatch has exactly the reason Kim wrote about.
2. **Palette drift.** Several tiles use dark purple headers with red bars; the brand kit is forest
   `#1F4634` / terracotta `#C2643F` on cream `#F5EFE6`. Purple tiles + cream tiles in one gallery
   reads as two sellers. The new tiles here use the brand palette for that reason.

## Claims that still need proof against the actual files

Nothing in this list is on the new tiles, but all of it is on his existing ones. If a number is
wrong, the tile has to change before the review does.

| listing | claim on a live image | how to check |
|---|---|---|
| 4573955047 gift tracker | 2,500+ formulas | open the .xlsx, count `=` cells; if it is 900, say "900+" |
| 4573955047 gift tracker | 56 dropdown menus, 6 charts, 46+ colour rules, 13 tabs, 18 occasions | same file, count each |
| 4578849733 craft fair | Premium 14 tabs / Basic 8 tabs, 4 files, 12-page guide | file count and tab names |
| 4578849733 craft fair | price = true cost / (1 - margin) | confirm the pricing tab actually divides by (1-margin) |
| 4578846463 secret santa | 12 linked tabs, "zero set-up" | count the tabs in the file |
| 4578846463 secret santa | 4 files: PREMIUM Noel, PREMIUM Arctic, PREMIUM EXAMPLE, User Guide (+ a Basic edition?) | count what actually downloads - a fifth file or a missing Basic edition is a message, not a review |
| 4578846463 secret santa | "no macros, works offline" | if the draw is a formula shuffle rather than a macro, say "no add-ins" instead - clearer and still true |

Send the .xlsx and `python3` will count all of it in one pass - formulas, dropdowns, conditional
formats, charts, tabs - and print the exact strings to put back on the tiles.
