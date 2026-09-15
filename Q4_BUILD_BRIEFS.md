# Q4 Build Briefs — the 8 new listings
### What to make, precisely, so the listing copy stays true

Written as the counterpart to `Q4_LISTINGS.md`. **The listing copy is the contract.** Every number
promised in a title or description is restated here as a spec, and `check_promises.py` fails the
build when the two disagree. That check exists because of one review: a pattern whose photo promised
arms the instructions didn't produce.

## How to use this

1. Build to the brief. Where you make a design decision that contradicts me, **fix the copy in the
   same sitting** — never ship a promise you can't keep.
2. Every crochet section is a **scaffold, not a finished pattern.** The round counts are sound
   starting points for the shapes described; they are not gauge-tested, because I cannot hold a hook.
   Each section says what to test and what to change. Publishing one of these without a test-crochet
   is how the last 1-star happened.
3. Every spreadsheet section gives tab → column → formula. Formulas use only functions that exist in
   **both** Excel (2016+) and Google Sheets: `SUMIFS COUNTIFS IFERROR INDEX MATCH VLOOKUP TEXT TODAY
   DATE EOMONTH NETWORKDAYS COUNTA ROUNDUP CEILING`. Deliberately avoided: `XLOOKUP`, `FILTER`,
   `LAMBDA`, `LET`, `UNIQUE` — they break on older Excel, and a refund costs more than the feature.

**Claim → spec index.** Left column is what the listing copy actually promises a buyer — it is not
what I thought would be nice. Anything in a brief that the copy *doesn't* claim (N1's and N2's videos,
for instance) is a seller-side upgrade: build it if you want it, but it only enters the listing when it
genuinely exists, and you add it to the promise list here at the same moment.

`python3 check_promises.py` enforces this file against `Q4_LISTINGS.md` and exits 1 on drift. It was
negative-tested by planting seven separate count errors across page counts, tab counts, item counts
and yardage — all seven were caught. A check you have never seen fail is decoration.

| Listing | Numbers promised in the copy | Where this file makes them real |
|---|---|---|
| N1 advent calendar | 24 minis · 18-page PDF · 12-mini travel version · **12-minute hanger video** | §N1 page plan (18 rows) · §N1 mini list (24) · §N1 hanger + video |
| N2 table runner | 15-page PDF · 2 lengths · 4 place-card holders | §N2 page plan (15 rows) · §N2 grading · *(join video: not yet promised)* |
| N3 mini stockings | 24 stockings · 9-page PDF · 2 sizes · 6 cuff variations · 12-mini version | §N3 page plan (9 rows) · §N3 variations |
| N4 goat / lamb | **11-page PDF** · 2 sizes · under 100 yds · loop-stitch fleece | §N4 page plan (11 rows) · §N4 scaffold |
| N6 dinner planner | 7 tabs · automatic recipe scaling | §N6 tab spec (7) · §N6 scaling math |
| N7 card tracker | 7 tabs · printable 2×4 label grid | §N7 tab spec (7) · §N7 labels + postmark design |
| N8 Secret Santa | 9 tabs · one-button rule-respecting draw | §N8 tab spec (9) · §N8 script |
| N9 New Year reset | 13 tabs · 30-day challenge · **7-min walkthrough** | §N9 tab spec (13) · §N9 video |

---

# CROCHET

## Shared crochet standards — apply to all four, then never think about them again

**1. Gauge is a measurement, not a formality.** State hook, yarn weight, and
`10 sc × 10 rows = X in over 4 in / 10 cm`, then publish a **fit tolerance**: "under 3.5 in swatch →
go up 0.25mm; over 4.25 in → go down." Amigurumi buyers resize constantly and a pattern that ignores
this earns "mine came out tiny" reviews.

**2. The magic ring and the closed base.** Beginners fail in the first two rounds more than anywhere
else. Every pattern carries, on page 2, a 4-photo strip: ring formed → ring closed → round 2 started
→ base viewed from below. One afternoon of photography, and roughly a third of the "I'm stuck"
messages disappear.

**3. Never describe a shaping step in prose alone.** Wherever the silhouette changes (heel, toe,
horn, wing fold, cuff), a diagram or photo is mandatory. Rule: **if a reader could do it two ways and
only one looks right, it needs a picture.** That is exactly the axolotl failure — limbs described, not
shown, and a render used instead of either.

**4. Written *and* charted for anything repeated.** Past 6 rounds of repeat, give both. Cheap once,
and it's a large part of why someone pays $6 instead of taking a free single.

Scaffold notation below: `sc` single crochet · `inc` 2 sc in one st · `dec` sc2tog · `(x)×y` repeat
y times · `BLO/FLO` back/front loop only · `tr` treble · `ch` chain · `sl st` slip stitch · `MR` magic
ring · spiral, do not join, marker every round unless stated.

---

## N1 · Crochet Christmas Advent Calendar — 24 minis + hanging tree

**Promise:** 18-page illustrated PDF · 24 mini amigurumi at 1.5–2 in · tree hanger with 24 clipping
points · optional 12-mini travel version · 12-minute video on the hanger corner · US + UK terms.
**Why $15 realised is defensible:** the buyer is making a December ritual, not a plushie. Adjacent
sellers hold $8–$25 at 1,300–3,800 reviews, so $15 is the middle of a proven band, not an aspiration.

### Page plan — exactly 18, because that's what the copy says

| # | Page content |
|---|---|
| P1 | Cover: finished calendar on a real wall in daylight, name, skill line, "24 minis" badge |
| P2 | What you get + the 4-photo magic-ring / closed-base strip |
| P3 | Materials, yarn-weight substitution table, tools, safety notes for under-3s, the reusability line |
| P4 | Gauge + fit tolerance, blocking, abbreviation table |
| P5 | **The shared mini body** — one construction used by 16 of the 24, with its swap points |
| P6 | Assembly index: which minis get which finishing (clip, loop, ring), day-number mapping, printable number sheet |
| P7 | Day 1 · Tree |
| P8 | Day 2 · Star |
| P9 | Day 3 · Bauble |
| P10 | Day 4 · Bell |
| P11 | Day 5 · Snowman |
| P12 | Day 6 · Reindeer |
| P13 | Day 7 · Penguin |
| P14 | Day 8 · Candy cane |
| P15 | Days 9–16 in shared-body format (one block per mini, 3 lines each) |
| P16 | Days 17–24 in shared-body format |
| P17 | **The hanger:** tree outline, 24 clip points, spacing math, stiffening, hanging, video link |
| P18 | 12-mini travel version, colourway chart, print options, licence + contact |

### The 24 minis — and the constraint that keeps this finishable

Sixteen share one body so the calendar is a weekend, not a month. Buyers abandon advent sets around
mini #7 because every mini is a new construction. Don't do that to them.

| Days | Method | Cost |
|---|---|---|
| 1–8 | Fully written individually: tree, star, bauble, bell, snowman, reindeer, penguin, candy cane | 1 page each (P7–P14) |
| 9–16 | Shared body + 2 additions: elf hat, mitten, stocking, gift box, gingerbread, snowflake, holly, candle | 8 minis on P15 |
| 17–24 | Shared body + 2 additions: bell jar, candy corn, wreath, cookie, chick, teddy, robin, angel | 8 minis on P16 |

**Shared body (scaffold — test one before you write the rest).** Worsted 4, 3.5mm, worked bottom-up:
```
MR · R1 6sc (6) · R2 inc×6 (12) · R3 (1sc,inc)×6 (18)
R4–R7 sc 18 (4 rnds) · R8 (7sc,dec)×2 (16) · R9 (2sc,dec)×4 (12)
stuff firm · R10 dec×6 (6) · close.
```
At the stated gauge this blocks out ~1.5 in tall — the size the listing promises. Every mini on days
9–24 is this body **plus exactly two things**: a top feature and a face treatment. If a mini needs
more than two additions, it is a different pattern, not an advent mini — cut it.

**The 16 additions (two lines each — that's the whole authoring job for P15/P16):**
- Elf hat → 8-ch loop at crown · embroidered eyes only
- Mitten → thumb: ch 4, attach at round 5 side, FLO sc into the ch · no face
- Stocking → BLO sc round 1 for a cuff line · ch-6 hanging loop at round 4
- Gift box → separate 6-st lid disc · ch-4 ribbon laid over round 8 and stitched
- Gingerbread → 4 flat ch-3 limbs · face embroidered (photo, not prose, for the arm angle)
- Snowflake → 6 ch-spikes worked separately, stiffened in diluted PVA · no face
- Holly → 2 felt leaves as a no-crochet option · 3 French-knot berries
- Candle → wick: 6-ch in brown worked FLO so it stands · drip stitch in cream
- Bell jar → rounds 1–4 in gold · bead placed inside before round 5
- Candy corn → colour changes at rounds 3 and 6 · no embroidery at all
- Wreath → 5-ch ring joined into round 2 all the way · 6 red beads
- Cookie → ch-3 sprinkles sewn with two stitches each · face optional
- Chick → 4-ch wings FLO · orange beak worked as a 3-st triangle
- Teddy → 4 ears: MR 6sc, flattened, sewn at round 2 positions 3 and 15 · muzzle in cream
- Robin → 5-ch wings · red throat embroidered across rounds 5–6
- Angel → halo: 12-ch ring in gold, stiffened, stitched behind head · no legs

**Day numbers.** Do not crochet numbers onto 24 minis. Ship a printable 1–24 label sheet (2×4 stock)
on P6 plus the option of numbered locking markers. Anyone who has sewn a "17" onto a 1.5 in bauble
will thank you, and it costs you a page instead of 24 more instruction blocks.

### The hanger (P17) — the part that justifies $15

- Ring: `5 tr` foundation, join, `*2 dc, ch 2*` around for 12 points. Stiffen by threading floral wire
  through the ch-2 arcs, then wrap the wire in green yarn and stitch down.
- **24 attachment points** = 12 ring points × 2 loops each. Space them with a written row chart
  ("loop A into arc 1, loop B into arc 1 at 3 dc offset"), *not* by eye — uneven spacing is the #1
  complaint on hanging advent pieces and the only fix is not eyeballing it.
- Two hanging methods, both shipped: 6-ch loop + 5mm jump ring, **or** button-and-loop with no
  hardware. Makers feel strongly, and the no-hardware version is what sells to parents.
- Video (12 min, phone, no music edit needed): wire-threading the corner, and counting loops. It is
  the only step where a still photo genuinely loses people.

### Risk register

| Risk | Mitigation |
|---|---|
| 24 minis turns into 24 different constructions; nobody finishes | The shared-body rule and the "two additions" ceiling. Enforce in editing |
| Photographing 24 tiny objects is a huge shoot | 8 hero minis + one daylight flatlay of all 24. **Do not render 24 objects you haven't made** |
| Buyers expect it to survive to next December | Say it on P3 and in the listing: clip off, box, restring. Reusability is the price justification |
| "24 minis" overwhelms a first-day buyer | Add the FAQ line "start with days 1–4 this week" — it converts the hesitators |

---

## N2 · Crochet Christmas Table Runner — motifs joined as you go

**Promise:** 15-page PDF · 2 lengths (48 in, 68 in) at 14 in wide · poinsettia motifs joined without
seaming · reindeer border written and charted · 4 place-card holders + napkin rings in the same file
· blocking/care notes · 20-minute video on the join.

### Page plan — 15

| # | Page content |
|---|---|
| P1 | Cover: runner on a real set table, plates and napkins, not floating on white |
| P2 | Contents, what you get, skill line, and one paragraph explaining why there is no seaming |
| P3 | Materials per length, DK yardage by colour, hooks, notions |
| P4 | Gauge + the sizing-your-own-table formula |
| P5 | Poinsettia motif, rounds 1–5, written |
| P6 | Poinsettia photo strip: petal in progress, correct vs. puckered tension |
| P7 | **Join-as-you-go.** The most important page. 6 photos, end-to-end sequence |
| P8 | Layout chart: motif counts for 48 in and 68 in, row offsets, where the short rows go |
| P9 | Reindeer border, written |
| P10 | Reindeer border, charted |
| P11 | Edging, and doubling the short ends so it hangs straight |
| P12 | Place-card holders ×4 (one motif + a ring; deliberately short) |
| P13 | Napkin rings |
| P14 | Blocking, washing, gravy: care for a table textile |
| P15 | Sizing table for other lengths, colour substitutions, licence, contact |

### Grading math — what buyers check before they trust you

At the stated gauge (4.0mm, DK) one joined motif block squares to **7 in**.

| Table | Motifs across | Rows | Finished length |
|---|---:|---:|---|
| 4 ft bistro | 6 | 2 | 42 in |
| 6 ft standard | 9 | 2 | 63 in |
| 8 ft banquet | 12 | 2 | 84 in |

Publish the rule, not just two sizes: **motifs across = round(table length ÷ 7)**, rows fixed at 2 for
a 14 in width, rows = 3 for 20 in. That one line turns a 2-size listing into a custom-size listing
without a second pattern — and it is the answer to the "will this fit my table?" message you'd
otherwise have to send by hand.

### The join (P7)

Last round of each new motif: work the first **3 stitches normally**, then `*sc into next st of this
motif, sl st into the corresponding st of the finished neighbour*` around. The 3 free stitches are
not decoration — they give the corner slack, and skipping them is why people's grids buckle. Photograph
the **first** three stitches and the corner, not just mid-round: mid-round is the easy part.

---

## N3 · Crochet Mini Stockings — 24 for an advent garland

**Promise:** 9-page PDF · 24 mini stockings · 2 sizes (2.5 in advent, 4 in name set) · 6 cuff variations ·
built-in gift-tag loop · A–Z monogram chart · 12-mini version at the end · yardage per stocking so one
50g ball covers a set.

### Page plan — 9

| # | Page content |
|---|---|
| P1 | Cover: all 24 mini stockings on a garland, real wood, daylight, a chocolate coin in one for scale |
| P2 | What you get, skill line, both sizes side by side |
| P3 | Materials, colour plan for 24, hooks, the 50g-ball math |
| P4 | Gauge, stuffing firmness rule, and "which way does the toe point" orientation note |
| P5 | **2.5 in stocking**, cuff → leg → heel → foot → toe, written |
| P6 | **4 in stocking**, same structure with extra rounds marked, heel photo strip |
| P7 | The 6 cuff variations: ribbed · folded · scalloped · contrast · striped · plain-for-painting |
| P8 | A–Z monogram chart sized for a stocking leg, plus tag-loop options |
| P9 | 12-mini version, yardage table, care, licence, contact |

### Scaffold — 2.5 in stocking (worsted 4, 3.25mm, spiral)

```
Cuff (contrast):  ch 11, join, sc 11 × 3 rnds. Change to main.
Leg:              R1  sc 11 (11)
                  R2  sc 4, inc, sc 5 (12)
                  R3–R5 sc 12 (3 rnds)
Heel (short rows): R6  sc 7, turn · R7  dec, sc 5 (6) · R8  sc 2, dec, sc 1 (4)
                  R9  sc 4, turn, pick up 4 unworked sts (8) → resume in the round
Foot:             R10 (2sc,dec)×2 (6) · R11 dec×3 (3) · close. Stuff firmly through the leg.
Tag loop:         ch 6, sl st into round 2 of the cuff on the back side. Do not cut.
```

**Why this shape works at this scale.** Eleven stitches around the cuff is the smallest count that
still takes a finger without tearing, and a short-row heel is the only way to get a real ankle at 12
sts — increasing instead leaves a hole you'll photograph and then apologise for. Test one: foot
riding up → work R10 once more before the decreases; floppy → you are under-stuffing, which is the
single most common fix and the answer to two-thirds of your future messages.

**4 in version:** same build at `ch 15 / 15 sts` cuff, inc to 18, leg 5 rounds, heel short rows over
9 sts, foot `(4sc,dec)` ×3. Publish both columns side by side on P6 so nobody flips pages mid-round.

**12-mini version (P9):** halve the leg to 2 rounds and drop the heel. At 2 in a heel is decoration,
and saying "the small version is straight-legged on purpose" pre-empts the "is this a typo?" message.

---

## N4 · Year of the Goat / Lamb — one body, two faces

**Promise:** 11-page PDF · 2 sizes (4 in plush, 2.5 in charm) · one body with horns optional ·
loop-stitch fleece · red-and-gold auspicious colourway · optional coin/tassel charm · standing vs
sitting instructions · under 100 yds for the 4 in goat.

**Timing, restated because it changes the product:** Chinese New Year 2027 is **February 6**, and the
animal is the **Fire Goat**. The Horse wave passed in February 2026. Launch Dec 1, ride through
Feb 20 (Lantern Festival), then relist the same file as an Easter lamb in March — one pattern, two
seasons, no dead inventory.

### Page plan — 10

| # | Page content |
|---|---|
| P1 | Cover: goat and lamb together, red/gold scarf on the goat, real fabric background |
| P2 | What you get, skill line, and the "one body, two faces" idea drawn as a fork diagram |
| P3 | Materials, colourway chart (cream · Fire Goat red/gold · Easter pastel), yardage |
| P4 | Gauge, stuffing firmness for standing, loop-stitch yarn warning (it hides dropped stitches) |
| P5 | Head + body, one piece, written |
| P6 | Legs + tail, and the stand-vs-sit decision with two photos |
| P7 | **Loop-stitch fleece.** 6-photo strip: hook under both loops, yo twice, pull through all four |
| P8 | Horns (wire core) + lamb face (no horns, shorter loops) + ears |
| P9 | Face embroidery chart: eye placement, muzzle stitch, where the ears land (rounds 3–4 back) |
| P10 | Saddle colourwork band, charted: the red/gold motif over rounds 13–16, one symbol per round |
| P11 | 2.5 in charm scaling table, tassel + coin charm, care, licence, contact |

### Scaffold — 4 in goat, worsted 4, 3.25mm

```
Head + body (one piece, top-down):
  MR · R1 6sc (6) · R2 inc×6 (12) · R3 (1sc,inc)×6 (18) · R4 (2sc,inc)×6 (24)
  R5–R8   sc 24 (4 rnds)                 ← head
  R9      (6sc,dec)×3 (21) · R10 (4sc,dec)×3 (18)
  R11     (1sc,inc)×6 (24)               ← neck flare: stops the balloon-head look
  R12–R17 sc 24 (6 rnds)                 ← body
  R18     (2sc,dec)×6 (18) · stuff firm
  R19     (1sc,dec)×6 (12) · R20 dec×6 (6) · close
Legs ×4:  MR · R1 6sc · R2 inc×6 (12) · R3–R6 sc 12 (4 rnds) · stuff to top · 15in tail
Ears ×2:  MR · R1 6sc · R2 (1sc,inc)×3 (9) · sl st round, flatten, no stuff
Horns ×2: ch 10 around a 3in pipe cleaner, sl st back along the ch to coil
```

**Fleece placement, not full coverage:** loop stitch only on **R13–R16** of the body and **R5–R7** of
the head. All-over loops turn a 4 in animal into a shag carpet and cost an hour of ends; a fleece
blanket with clean legs and face reads as a goat at a third of the effort. Trim loops to 4–5mm — and
photograph before and after, because the after photo is what sells the pattern.

**Standing vs sitting (P6).** Standing at 4 in needs firm legs, a bead in the pelvis, and body fill
added **through the leg hole before closing** so weight sits low. For sitting: skip the bead, add two
rounds of extra fill behind R18. Give the numbers. "Stuff as desired" is what a free single says, and
it's why people think a paid pattern is no better.

---

# SPREADSHEETS

Shared build rules — all four, and the reason spreadsheet products get refunds:

- **One Setup tab. Everything reads from it.** Named ranges (`Guests`, `Budget`, `XmasDate`,
  `Currency`, `CutOffs`) and `SUMIFS` against them. Any tab where the user must type the same fact
  twice is a bug you should fix at build time, not in the FAQ.
- **Input vs formula colour coding** with a legend on row 1: blue = type here, grey = don't touch.
  Free, and it prevents most "my numbers broke" messages.
- **Protect formula cells** in Excel; use "view only ranges" in Sheets. Say in the listing that
  protection is removable — buyers fear locked sheets more than they fear formulas.
- **Ship sample rows.** Never a blank grid: nobody imagines their data into 40 empty rows. Row 2–4
  filled, with a note "select A5:Z500 and press Delete to start clean."
- **Both platforms from one build.** Build in Excel, `Save As xlsx`, open in Sheets, save a copy.
  Re-test `EOMONTH`, `NETWORKDAYS` and all date math after the copy — that's where drift appears.
- **Delivery:** one PDF containing thank-you + how to download, one copy link per file, licence text,
  support email, walkthrough link. No zips, no external drives, no "reply to get your file."
- **Column widths and freeze panes** on every tab, and a print area set on the tabs a buyer will
  print (labels, place cards, reveal slips, statements). Unprintable tabs are the #1 1-star driver
  on spreadsheet products.

## N6 · Christmas Dinner Planner — 7 tabs

| Tab | Columns (A→) | Logic to implement |
|---|---|---|
| `Setup` | adults, kids, servings per kid, budget, currency, dinner date, stores | Named: `Guests = adults + kids*servings_per_kid`, `Budget`, `DinnerDate` |
| `Menu` | dish, course, make-ahead?, reheatable, recipe, yield, cost per batch, batches, plated cost, notes | `batches = ROUNDUP(Guests/yield,0)` · `plated = cost/batch ÷ yield × Guests_share` |
| `Scaling` | recipe, base yield, target yield, factor, ingredient, unit, base qty, **round to**, scaled qty | `factor = target/base` · `scaled = CEILING(base*factor, round_to)` |
| `Shopping` | aisle, item, qty, unit, est cost, store, bought? | header total: `=SUMIFS(cost, bought, "<>yes")` = "still to buy" |
| `Budget` | category, expected, actual, variance, % used, flag | `flag = IF(actual>expected,"OVER","")` + CF on the word |
| `Timeline` | T-minus hours, task, who, hours, depends on, ready by | `T-minus = (DinnerDate+serve_time) - start`, sorted descending so it reads backwards from dinner |
| `Potluck` | guest, dish promised, qty, dietary, confirmed | deliberately dumb — must be fillable on a phone at 11pm |

**Two build details that decide whether this is good.**

1. **Scale to a cookable number.** Raw multiplication gives 2.31 turkey breasts. Every `Scaling` row
   needs a `round to` column (1 / 0.5 / 12) and `=CEILING(base*factor, round_to)`. This one column is
   the difference between a spreadsheet and a tool.
2. **Kids are not zero and not one.** Default `servings per kid = 0.5`, exposed in `Setup` (never
   hard-coded), because the number is the argument in every household that hosts.

Video (10 min) covers exactly two things: the `round to` logic and the potluck sharing link.

## N7 · Christmas Card List & Mailing Tracker — 7 tabs

| Tab | Columns (A→) | Logic |
|---|---|---|
| `Setup` | households this year, budget for cards/stamps, country, **cut-off table last-updated date**, printer label size | Named: `CardsBudget`, `Country`, `LabelSize` |
| `Address Book` | household, contact, street, city, postcode, email, kids' names, notes, evergreen? | the master; other tabs reference by household ID |
| `This Year` | household, sending? ✓, card design, gift enclosed, **postmark by**, mail-by status, received? ✓ | see cut-off logic below |
| `Postmark Table` | country, class, cut-off date, source URL, year | editable — see the honesty note |
| `Stamps & Supplies` | item, qty owned, qty needed, cost, where bought | feeds Budget |
| `Thank Yous` | gift received, from, thank-you due by, sent? ✓ | `due = IF(sent="no", gift_date+14, "")` shown as "14 days" convention |
| `Labels (print)` | mail-merge-ready grid, 2×4 layout, one row per household | print area + 10 rows/page, no formulas — this tab is a **print** artefact |

**The postmark feature — build it honestly.** A spreadsheet cannot know this year's postal cut-offs.
Ship a `Postmark Table` tab the buyer fills once per year (5 rows for the common cases, pre-filled
with last year's dates as examples, plus a "source" column) and compute:
```
mail_by   = VLOOKUP(country & class, PostmarkTable, cut_off_col, FALSE)
status    = IF(TODAY()>mail_by, "TOO LATE - use express", IF(mail_by-TODAY()<=3, "THIS WEEK", "fine"))
```
Display the table's `last updated` date on the tab so nobody blames your file for a stale USPS date.
**And change the listing line** from "postmark deadline calculator" to "postmark deadline planner —
you set this year's dates once in 2 minutes." Same value, no false automation promise. This is exactly
the class of overclaim that produced your 1-star; I'd rather trim my own copy than let you ship it.

## N8 · Secret Santa / White Elephant Organiser — 9 tabs

| Tab | Columns | Logic |
|---|---|---|
| `Setup` | group name, budget, gift exchange date, allow partners?, allow repeats within N years?, allow self-draw? | Named: `Budget`, `PartyDate`, flags |
| `People` | ID, name, email, partner-of ID, never-give-to IDs, wishlist link, must-not-buy, confirmed? | exclusions live here as text lists |
| `History` | year, giver ID, receiver ID | the engine for "no repeats within 3 years" |
| `Draw` | giver, receiver, status | filled by the script or the shuffle; **never typed by hand** |
| `Reveal Slips (print)` | one row per person: your name, you have, budget, deadline, wishlist | 2.625×3.75 business-card layout, 8 per page |
| `Wishlists` | person, item 1-3, link, price | giftee-visible only; keep columns wide, it's a phone tab |
| `Budget Log` | who, item, paid?, cost, over budget? | `=IF(cost>Budget,"OVER","")` |
| `White Elephant` | pick order, player, item claimed, steal #, round result | manual-entry tracker for the party; no formulas needed beyond counts |
| `Wrap & Deliver` | giver, wrapped?, tag?, delivered?, date | the 3% who forget are real; give them a tick box |

**Name draw that respects rules.** A pure-formula constrained draw is a research project; a 40-line
script is an evening. Provide **both**, and label them:

*Google Sheets — Extensions → Apps Script, paste, save. Buyers copy it in; document it in the video.*
```javascript
function runSecretSanta() {
  const ss = Spreadsheet.getActiveSpreadsheet();
  const P = ss.getSheetByName('People'), D = ss.getSheetByName('Draw'), H = ss.getSheetByName('History');
  const setup = {};
  ss.getSheetByName('Setup').getDataRange().getDisplayValues()
    .forEach(r => { if (r[0]) setup[String(r[0]).toLowerCase().trim()] = r[1]; });
  const allowSelf    = setup['allow self-draw'] === 'yes';
  const historyYears = Number(setup['no repeats within (years)'] || 0);
  const lastYear     = new Date().getFullYear();

  const banned = new Map();                       // giver -> Set of forbidden receivers
  const hist = H.getDataRange().getDisplayValues();
  const prior = new Map();
  for (let i = 1; i < hist.length; i++) {         // name -> set of past receivers
    const yr = Number(hist[i][0]);
    if (lastYear - yr <= historyYears) {
      if (!prior.has(hist[i][1])) prior.set(hist[i][1], new Set());
      prior.get(hist[i][1]).add(hist[i][2]);
    }
  }
  const people = P.getDataRange().getDisplayValues().slice(1)
    .filter(r => r[1] && String(r[9] || '').toLowerCase() === 'yes');   // confirmed only
  const names = people.map(r => r[1]);
  const partnerOf = {};
  people.forEach(r => { if (r[6]) partnerOf[r[1]] = r[6]; });

  const forbidden = (g, rcv) =>
    (!allowSelf && g === rcv) ||
    (partnerOf[g] && partnerOf[g] === rcv) ||
    (prior.get(g) && prior.get(g).has(rcv)) ||
    (people.find(p => p[1] === g)[8] || '').split(',').map(s => s.trim()).filter(Boolean).includes(rcv);

  for (let attempt = 0; attempt < 400; attempt++) {          // retry the whole draw, not each pair
    const pool = names.slice();
    for (let i = pool.length - 1; i > 0; i--) {               // Fisher-Yates
      const j = Math.floor(Math.random() * (i + 1));
      [pool[i], pool[j]] = [pool[j], pool[i]];
    }
    const pairs = names.map((g, i) => [g, pool[i]]);
    if (pairs.every(([g, r]) => !forbidden(g, r))) {          // valid derangement found
      D.getRange(2, 1, pairs.length, 2).setValues(pairs);
      return 'Assigned ' + pairs.length + ' pairs.';
    }
  }
  return 'Could not satisfy every rule. Loosen an exclusion or remove a past-year rule.';
}
```
Note what that returns on failure: a **message telling the organiser which rule to loosen**, not a
silent wrong result. Exclusion-heavy groups genuinely cannot always be satisfied; a spreadsheet that
pretends otherwise gets the 1-star.

*Excel fallback:* `=INDEX(People!B:B, RANDBETWEEN(1,n))` shuffle in a helper column with a
`IF(or(self,partner,prior),"try again","ok")` check column, plus the instruction "press F9 until every
row says ok." Ugly, honest, and it works — and it's why the sheet ships a `History` tab at all.

## N9 · New Year Financial Reset — 13 tabs

| # | Tab | Purpose / logic |
|---|---|---|
| 1 | `Start Here` | the 4-step order of operations, and an explicit "you can stop after step 2" line |
| 2 | `Audit` | last year's income, fixed, variable, debt paid, saved, net — 8 rows, entered from bank statements |
| 3 | `Decisions` | keep / stop / start, with a `£ or $ effect` column that **feeds** tab 5 |
| 4 | `Setup` | pay frequency, pay days, currency, household size, target savings % |
| 5 | `12 Months` | one row per month: income, bills, goal, actual, variance; Jan–Dec across columns so the year is visible at once |
| 6 | `Bills` | due day, amount, autopay?, category; `=EOMONTH(...)` for monthly rolling |
| 7 | `Paycheck Plan` | per pay date: gross, taxes, assigned, free. `free = gross - assigned` is the whole product |
| 8 | `Debt` | balance, rate, minimum, payoff plan snowball vs avalanche, `projected month` |
| 9 | `Emergency & Sinking` | goal, saved, per-month contribution, target date |
| 10 | `Net Worth` | assets, liabilities, monthly history row, sparkline-ready table |
| 11 | `Tax Prep` | deductible-ish categories, quarterly rollup, exportable summary |
| 12 | `Quarterly Reviews` | 4 blocks (Mar/Jun/Sep/Dec), each with 3 pre-written questions + a numbers-diff |
| 13 | `30-Day Challenge` | day 1–30, task, done?, cost found; `=SUMIF(done,"yes",found)` = money the reset actually produced |

**The design decisions that make it a reset and not another budget.**
- **Audit first, always.** Every tab is downstream of tab 2; if the user skips it the file still works
  but the plan is generic. Put that sentence on `Start Here`, because honesty about your own product
  is a differentiator in a category full of magic.
- **`Decisions` must feed `12 Months`.** `=SUMIF(Decisions!type,"stop",Decisions!effect)` reduces the
  target automatically, so a decision becomes a number. That single link is the reason the file is
  $9 and not $2.
- **Assume abandonment in week five.** `12 Months` needs to be readable cold: one screen, 12 columns,
  no sub-tabs, no scrolling. Most planners fail because finding your place takes 3 minutes.
- **30-day challenge with a money total**, not a habit grid. Buyers of "reset" products want proof the
  month did something; `=SUMIF` of found money is that proof, and it's what earns the review.
- **Video: 7 minutes**, three screens only — the audit tab, the Decisions→12 Months link, the
  challenge total. Anything longer and buyers skip it, then email you.
- Publish on **Dec 26**: catches the last week of Q4 intent and owns the dead first half of January.

---

# Packaging, licensing, and the authoring rules that generalise

## The 8-line spec every new listing must satisfy before you publish

1. Every object in the hero photo **exists and was made from your written instructions.**
2. Every number in the title appears in the PDF/spreadsheet (count the pages, count the tabs).
3. Every "included" claim has a page or tab number behind it in `Q4_BUILD_BRIEFS.md`.
4. Skill level names the actual stitches or the actual formulas. Never "easy."
5. Sizing/grading table present, plus the rule for making your own size.
6. Terms written in one sentence a non-lawyer understands.
7. Video, or a written "no video needed" line. Both are fine; silence is not.
8. **A test person made one.** Not "I checked it reads well." Someone else, with your words only.

## Versioning — the practice that turns a bad review into a 4.9 shop

Name files `pattern-slug-v1.0.pdf`. When a buyer reports a genuine error: fix it, bump to v1.1,
**message every buyer** with the update, and add one line to the listing description dated:
*"v1.1 (Sept 2026): gills and arms rewritten after buyer feedback."*

That line is worth more than the 1-star cost you, for three reasons: it proves the pattern was made by
a person, it proves you answer, and it tells the next buyer that if they find a problem it gets fixed.
Sellers with 40,000 reviews don't do this. At your size it is the cheapest possible moat.

## What to cut rather than build

If a brief above turns out to be more work than the price supports, **cut the promise, not the
quality.** A 12-mini advent calendar at $10 with honest photos beats a 24-mini one at $15 with
renders — and the listing copy is editable in `listing_pack.py` in ninety seconds. Re-run
`python3 listing_pack.py --check` after any edit and it will tell you if a title got too long or a
tag lost 3 characters of headroom.
