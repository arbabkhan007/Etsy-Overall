# Audit of the 36-listing SEO document

Verdict: the thinking is right; the execution would lose 37 tag slots outright and waste about 72
more on his own listings. Rebuilt sets are paste-ready in `audit/tags_fixed.csv`, every change and its
reason in `audit/tags_changes.csv`.

## What the document gets right
- 13 tags per listing, multi-word, single-intent, no filler.
- Titles front-load the exact product phrase (search reads the first phrase hardest).
- The image rule - real finished samples, never AI-as-if-real - is Kim's 1-star, and it is the rule the
  tiles in `tiles/` are built under.
- Spreadsheet titles name the tabs in the title itself: correct for a file a buyer cannot hold.

## Defect 1 - 37 tags are 21-23 characters. Etsy's tag box is 20, so they cannot be saved at all

| # | tag | chars | | # | tag | chars |
|---|---|---|---|---|---|---|
| 1 | `crochet holiday decor` | 21 | | 3 | `mini stocking pattern` | 21 |
| 4 | `wreath crochet pattern` | 22 | | 4 | `Christmas door wreath` | 21 |
| 5 | `crochet pattern bundle` | 22 | | 6 | `crochet Christmas tree` | 22 |
| 6 | `Christmas table decor` | 21 | | 7 | `gnome crochet pattern` | 21 |
| 10 | `emotional support plush` | 23 | | 10 | `crochet plushie bundle` | 22 |
| 12 | `turtle crochet pattern` | 22 | | 12 | `quick crochet pattern` | 21 |
| 13 | `dragon crochet pattern` | 22 | | 18 | `construction estimate` | 21 |
| 18 | `contractor spreadsheet` | 22 | | 19 | `church giving tracker` | 21 |
| 20 | `renovation cost tracker` | 23 | | 22 | `bookkeeping spreadsheet` | 23 |
| 22 | `income expense tracker` | 22 | | 23 | `real estate spreadsheet` | 23 |
| 25 | `Excel budget template` | 21 | | 26 | `wedding planning tool` | 21 |
| 26 | `Google Sheets wedding` | 21 | | 27 | `budget template bundle` | 22 |
| 28 | `Google Sheets planner` | 21 | | 28 | `daily routine tracker` | 21 |
| 31 | `household spreadsheet` | 21 | | 32 | `recipe cost calculator` | 22 |
| 32 | `bakery profit tracker` | 21 | | 33 | `Google Sheets catering` | 22 |
| 34 | `craft sale spreadsheet` | 22 | | 34 | `handmade sales tracker` | 22 |
| 34 | `vendor market planner` | 21 | | 35 | `Christmas spreadsheet` | 21 |
| 36 | `Christmas gift tracker` | 22 | | 36 | `holiday shopping list` | 21 |
| 36 | `Christmas spreadsheet` | 21 | |  | `` |  |

Replacements are in the CSV (102 of the surviving tags now sit at 19-20 chars: legal, but do not retype them - copy them).

## Defect 2 - 43 phrases are shared between his own listings (23% of the shop's slots)

| tag | listings | what the rebuild does |
|---|---|---|
| `beginner crochet` | 2, 3, 10, 11, 13, 15, 16, 17 | every slot now names the animal plus skill |
| `christmas crochet` | 1, 3, 5, 6, 7 | split into xmas / stocking / ornament / decor / gnome phrases |
| `digital crochet` | 2, 8, 15, 16, 17 | replaced with per-product pdf phrases |
| `festive crochet` | 3, 4, 5, 6, 7 | replaced with the actual motif |
| `no sew crochet` | 7, 8, 12, 16 | kept on the capybara only |
| `google sheets budget` | 20, 25, 27, 31 | four budget listings, four different phrases |
| `monthly budget` | 25, 27, 31 | Personal Finance keeps the monthly phrase |

The missing rule, now applied: **one tag string, one listing.** Etsy shows whichever of his own
listings already has clicks and sales, so the other copies are dead slots - and in the Q4 lane it is
the $11.99 Gift Tracker being outranked by his own $8.99 Secret Santa file.

## Defect 3 - one legal risk
`AIA billing template` (#18) is the American Institute of Architects' mark. This shop has already had
IP takedowns delete listings. Replaced with `progress billing`, which is what the tab actually does.

## Smaller things
- Six tags are substrings of another tag in the same listing (`secret santa` in `secret santa draw`,
  `animal pdf` in `crochet animal pdf`, `travel planner` in `excel travel planner`, `family budget` in
  `excel family budget`, `expense tracker` in `income expense tracker`, `gift exchange` in `gift
  exchange tool`) = six free slots. Etsy matches substrings, so the short one already covers the long.
- Year of the Goat (#2) is four months early: Lunar New Year 2027 is 6 February. Publish early January.
- Halloween (#14) is post-season; `trick or treat` pulled costume shoppers into a pattern listing, so
  it is now `trick or treat decor`.
- 75 tags were written Title Case. Etsy lowercases on save - which also means the collisions above are
  worse than they look, because `Christmas` and `christmas` are the same string.
- Titles are 76-115 chars, inside the 140 limit; the spreadsheet titles have ~25 chars of headroom if
  he wants more keyword room there.
- Title claims are unaudited: `3 Sizes` (#1, 4, 6, 7), `24 Christmas Stockings` (#3), `50 ...
  Templates` (#27), `DSCR calculator` (#23), plus `52 tabs` on the live wedding listing.
- The list does not match the shop 1:1 - no Nativity entry, though `patterns/F1-nativity-set.md` exists.

## The checklist at the end

| bullet | verdict |
|---|---|
| First phrase = primary keyword | keep - highest-value rule in the list |
| Add all 13 tags to every listing | keep, and add: none of them shared with another of your listings |
| No irrelevant filler tags | keep |
| Use attributes and categories | keep - attributes are a second free set of keywords |
| Type, format, benefit in the first two sentences | keep |
| Dashboard screenshots, list every tab | keep, with proof: only tabs you counted, only the file the buyer downloads |
| Real samples, disclose skill/yarn/hook/size/terms | keep - this is the Kim rule |
| Review after weeks, not daily | keep, and on a listing that already sells change tags only - a title edit resets the match you rank on |

Missing from it: one 5-15s video per listing (what turned a $2 PDF into a $12 one for him), the price
ladder per niche, and no permanent sitewide 25% off.

## Scores (proxy, not Etsy data)

Per-listing tag-set score after the rebuild: 40 validity (13 slots, all <=20) + 25 specificity
(penalised per phrase shared with another of his listings) + 20 intent (does the set contain a
purchase word: pattern/spreadsheet/tracker/template/xlsx) + 15 breadth (distinct words / 22).

| score | # | listing | self-collisions | slots changed |
|---|---|---|---|---|
| (100, 0) | 36 | Christmas Gift Tracker | 0 | 6 |
| (100, 0) | 35 | Secret Santa Spreadsheet | 0 | 5 |
| (100, 0) | 34 | Crochet Craft Fair Tracker | 0 | 6 |
| (100, 0) | 32 | Cottage Bakery Business | 0 | 6 |
| (100, 0) | 31 | Family Budget | 0 | 9 |
| (100, 0) | 25 | Personal Finance Bundle | 0 | 7 |
| (99, 0) | 33 | Catering Business Spreadsheet | 0 | 5 |
| (99, 0) | 29 | Etsy Seller Spreadsheet | 0 | 3 |
| (99, 0) | 27 | Budget Spreadsheet Bundle | 0 | 7 |
| (99, 0) | 24 | Rental Property Management | 0 | 0 |
| (99, 0) | 22 | Small Business Bookkeeping | 0 | 7 |
| (99, 0) | 19 | Church Management Spreadsheet | 0 | 4 |
| (98, 0) | 30 | Travel Planner | 0 | 4 |
| (98, 0) | 28 | Lifestyle Planner Bundle | 0 | 5 |
| (98, 0) | 26 | Wedding Planner | 0 | 5 |
| (98, 0) | 21 | School Management Spreadsheet | 0 | 3 |
| (98, 0) | 18 | Construction Estimate Bundle | 0 | 7 |
| (97, 0) | 23 | Rental Property Analysis | 0 | 4 |
| (97, 0) | 20 | Home Renovation Budget | 0 | 5 |
| (97, 0) | 17 | Chenille Duck Pattern | 0 | 5 |
| (97, 0) | 16 | Axolotl Pattern | 0 | 9 |
| (97, 0) | 14 | Halloween Bundle | 0 | 5 |
| (97, 0) | 12 | Sea Turtle Pattern | 0 | 8 |
| (97, 0) | 10 | Emotional Support Bundle | 0 | 7 |
| (97, 0) | 8 | Capybara Pattern | 0 | 7 |
| (97, 0) | 7 | Christmas Gnome Pattern | 0 | 7 |
| (97, 0) | 2 | Year of the Goat Pattern | 0 | 6 |
| (96, 0) | 13 | Baby Dragon Pattern | 0 | 6 |
| (96, 0) | 5 | Christmas Ornament Bundle | 0 | 6 |
| (95, 0) | 15 | Highland Cow Pattern | 0 | 6 |
| (95, 0) | 9 | Loaf Cat Pattern | 0 | 4 |
| (95, 0) | 6 | Crochet Christmas Tree Pattern | 0 | 8 |
| (95, 0) | 3 | Mini Christmas Stocking Pattern | 0 | 6 |
| (95, 0) | 1 | Christmas Tree Skirt Pattern | 0 | 5 |
| (93, 0) | 11 | Bunny Lovey Pattern | 0 | 1 |
| (92, 0) | 4 | Christmas Wreath Pattern | 0 | 8 |
