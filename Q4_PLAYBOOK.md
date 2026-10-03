# NovalityStore — Q4 SEO + Pricing Playbook
### Your shop, the market data behind it, and how to get to $1,000 by December 28

Written for MAK, NovalityStore (Washington, US) · 36 listings · 9 sales · 3 months old · 3.7★ (3 reviews)
Prepared 2026-09-13. All competitor numbers were read off live Etsy result pages that day.

**The four files, and what each is for**

| File | What it is | When you open it |
|---|---|---|
| `Q4_PLAYBOOK.md` | this document — diagnosis, market data, method | once a month, and whenever you're tempted to copy a competitor |
| `Q4_LISTINGS.md` | **43 listings**: complete copy for **35 of your 36** live listings (the 36th is the duplicate Cottage Bakery posting, which S2's merge note resolves) plus **8 new-build listings** to make, each with title, 13 tags, full description, price, scheduled sale window and a *verify* checklist. 5 colouring listings get archive cards instead of copy — deliberately. Every field validated against Etsy's limits | now, to paste; then per new listing |
| `q4_listings.csv` | the same in spreadsheet form (import, sort, share with a VA) | when you want it in Sheets |
| `Q4_BUILD_BRIEFS.md` | **how to make the 8 new products**: page plans, round-by-round scaffolds, tab schemas, the actual formulas, the Secret Santa script | while building each one |
| `check_promises.py` | machine check — every countable claim in a description must match a spec; exits 1 on drift | after any copy edit, before publishing |
| `q4_weekly_tracker.csv` + `q4_tracker.py` | 13 weeks, one job per week, targets vs. your actuals (regenerate from the model) | every Sunday, 10 minutes |
| `novality_seo_model.py` / `novality_q4_scores.csv` | the scoring engine and its 47-keyword output, incl. both portfolio scenarios | when you want to judge a *new* idea instead of asking me |

Every listing in `Q4_LISTINGS.md` carries a **verify checklist** — the specific numbers in the copy that
I inferred from your titles and market research rather than read from your files (page counts, finished
sizes, yardage, tab counts, hook sizes). Tick them or delete the sentence. I wrote you a description that
promises "12-page illustrated PDF" because that is what a pattern like yours usually contains; if yours is
6 pages, that promise is how the next 1-star gets written. The copy is 95% yours the moment you check it.

```bash
python3 listing_pack.py       # rebuild Q4_LISTINGS.md + validate every field (0 problems = safe to paste)
python3 novality_seo_model.py # re-score the market; prints both portfolio scenarios
python3 q4_tracker.py         # regenerate the weekly plan from whatever the model currently says
```

---

## 0. Read this before anything else

You asked me to be your SEO specialist **and your teacher**. So this document is written to make you
dangerous without me. Two rules apply to everything below:

**Rule 1 — I am not going to lie to you about what can be measured.**
Etsy does not publish search volume, competition, or click-through rate for any keyword. Not to you,
not to eRank, not to Alura, not to EverBee. Every "search volume" number you see in those tools is a
**modelled estimate**, and every "CTR" number is a **relative index** — a 0–100 bar that says *more/less
than this other keyword*, never a percentage. If someone shows you "8,100 searches/mo, 3.2% CTR" they
are selling you a guess with decimals on it.

What *is* measurable, and what this playbook actually uses:

| Measurable on a live search page | What it tells you |
|---|---|
| # of digital listings on page 1 | how crowded the fight is |
| review counts on page 1 | how much sales history you're competing against |
| realized sale prices on page 1 | the price ceiling a buyer will accept |
| % of page 1 with video | how much CTR you can win for free |
| % of page 1 with a number in the title | a cheap, high-value gap |
| your own Shop Stats | CTR, conversion, traffic sources — **the only real CTR you will ever get** |

**Rule 2 — your problem is not SEO.** I looked at your 36 listings, your reviews, and the market. You
have a *product-trust* problem and a *unit-economics* problem, and SEO on top of those just buys you
more visitors who don't buy. Section 1 fixes that. Do it first.

---

## 1. Diagnosis — five things costing you money right now

### 1.1 The one-star review is the most valuable thing in your shop
> *"I'm sick of this AI crap infiltrating etsy! … modified the pattern to actually LOOK like the picture
> used … This product is very misleading. Use a REAL photo."* — Kim, Aug 13, on your axolotl pattern

This is not a bad customer. This is a free audit of your conversion problem, from exactly your target
buyer (an experienced crocheter). Read it the way a stranger does: you land on your listing, see a
beautiful object, click to a shop with a 3.7★ rating, and the first review says the photos are fake.
No title or tag fixes that. **Nothing else on this list matters until you fix it.**

The fix, in order of effectiveness:

1. **Crochet your own samples.** A phone photo of a real object on a real table beats any render. Your
   15 crochet patterns need 15 real objects. That is a weekend each, and the objects then become gift
   photos, video B-roll, and shop-banner material. This is the highest-ROI weekend of your quarter.
2. **Get a test-crocheter.** Message three crocheters in your niche and offer free patterns for testing.
   You get (a) proof the instructions work — which is the #1 pre-purchase fear on a pattern, (b) real
   photos in varied yarn, (c) a line in your description that no AI-shop can copy:
   *"Test-crocheted by 4 makers in 3 yarn weights before release."*
3. **Until you have real photos, label the renders.** Put *"Renders — sample not yet stitched"* on the
   image. It converts worse than a real photo and infinitely better than a lied-about one, and it stops
   the next 1★.
4. **Answer the review publicly, today.** Not defensively. Something like: *"Fair hit, Kim. That listing
   used a render for the arms I hadn't stitched yet. I've since crocheted the full sample — the photos
   are real now and the arm rounds were rewritten (v1.1, free to everyone who bought). Thank you for
   being the reason."* Future buyers read seller replies more carefully than reviews. That reply is
   worth more than the review did cost you.

> **Lesson:** on digital products, the photo *is* the product. A buyer cannot hold a PDF, so your image is
> their only evidence that the thing you describe exists. Etsy's own policy also prohibits misleading
> listing images. This is a revenue fix and a risk fix at once.

### 1.2 You are a $1.50 shop, and that is a strategy — the wrong one
Your realized prices today: $1.50 (coloring), $2.25–$3.75 (crochet), $8.99–$26 (spreadsheets). And
**all 36 listings are on sale 25%, permanently.** Two problems:

**(a) The unit math.** Here's the exact fee stack on a US digital sale (2026): $0.20 listing fee
(charged again at each sale) + 6.5% transaction + 3% + $0.25 processing.

| Realized price | Etsy takes | You keep | You keep % | Sales to net $1,000 | Per week (13 wks) |
|---:|---:|---:|---:|---:|---:|
| $1.50 | $0.59 | $0.91 | 60% | **1,102** | 84.8 |
| $2.62 | $0.70 | $1.92 | 73% | 521 | 40.1 |
| $3.50 | $0.78 | $2.72 | 78% | 368 | 28.3 |
| $5.99 | $1.02 | $4.97 | 83% | 202 | 15.5 |
| $9.99 | $1.40 | $8.59 | 86% | 117 | 9.0 |
| $15.00 | $1.88 | $13.12 | 88% | 77 | 5.9 |
| $37.50 | $4.01 | $33.49 | 89% | 30 | 2.3 |

*(These are computed by `novality_seo_model.py` — `python3 -c "from novality_seo_model import *"` then
`etsy_fees(9.99)`. Don't trust any fee table, including this one, without checking your own Etsy receipt.)*

You have sold 9 items in 90 days. **$1,000 at $1.50 needs 85 sales a week.** At $15 it needs 6. Same shop, same files, same traffic. The
number of listings you have is not the constraint — the price per sale is.

**(b) The anchor.** A permanent 25% off on 100% of a shop means the sale price *is* your price and the
$2.00 strikethrough is decorative. Buyers who comparison-shop (and on patterns they do) read a
forever-sale as "this shop is not selling." Meanwhile the discount you'll need for Black Friday is
already spent.

> **Lesson:** price is the only lever that raises revenue without needing more traffic. Discounts are
> ammunition — spend them on a date, not on a permanent basis.

### 1.3 Thirty-six listings is not a catalogue, it's four thin ones
You have 6 coloring, 15 crochet, 13 spreadsheet, 2 travel. New Etsy listings take roughly **4–12 weeks**
to accumulate enough click/conversion data to rank, and seasonal listings need to be **live 6–8 weeks
before peak**. Listing 36 things once is how nothing ranks. Listing 12 things, watching them, and
rewriting the ones that don't convert is how things rank.

Worse: two of your clusters are actively bad.

- **Coloring pages: retire this cluster.** It is the single most commoditised category in digital
  downloads. Observed on the adult-coloring result pages: a **5,900**-review seller at $1.20, a
  **4,300** at $5.50, and three separate **3,100**-review listings at $1.85, $1.87 and $3.70. Your 6
  listings at $1.50 are in that knife fight with 0 reviews.
  The model scores the ceiling at $2–2.50 and the verdict is `KILL — price-war tier`. Keep the files,
  stop spending any hour on them.
- **Spreadsheets: your best cluster by price ceiling and worst by incumbency.** Top budget-spreadsheet
  sellers sit at 10.7k–38.7k reviews for $1.92–$5.55. Do **not** fight them for "budget spreadsheet."
  Your spreadsheet listings that *can* win are the specific, professional, unglamorous ones: church,
  school, cottage bakery, contractor, rental analysis — 14–20 page-1 listings, weak incumbents, $11–$38
  ceilings. Generic "family budget" is 46 listings deep at 2,400 median reviews.

> **Lesson:** you don't need a better keyword, you need a keyword where page 1 has fewer than ~25
> listings and no seller with 10,000 reviews. That single filter is most of Etsy SEO for a new shop.

### 1.4 Your title/tags are decent; your *first 47 characters* are the part that sells
Compare your listing to the one winning your category:

```
YOURS     Crochet Christmas Tree Skirt Pattern, Bobble Snowflake 12-Spoke…
WINNER    12 Christmas Granny Square Crochet Patterns | Holiday Crochet…
```
Yours front-loads the product; theirs front-loads a **number**. On the mobile grid, ~47 characters is
all a shopper sees before truncation. The three highest-leverage additions to any of your titles are,
in order: a **number** (3 Sizes / 13 Tabs / 24 Minis / 42-54-66 Inch), a **differentiator buyers fear
lacking** (No-Sew, Beginner, US+UK Terms), and the **format promise** (PDF, Instant Download).

Also: your titles use "Colouring" while your URL slugs use "coloring". Etsy stems/normalizes, so it
isn't a ranking disaster — but a US buyer seeing British spelling in a screenshot feels the mismatch,
and it tells you the copy was written without a target market. Pick **US spelling** for a US shop, and
use "Colouring" only inside a tag if you want UK/AU traffic.

### 1.5 Your About section advertises products you don't sell
The shop description promises *"fleece-lined sublimation socks, DTF apparel, natural rubber yoga mats,
stainless steel mugs."* Your shop contains 36 digital downloads. A buyer who reads that and finds no
socks concludes one of two things, both bad: that you're a reseller dropping products in randomly, or
that the shop is not carefully run. It also muddies the shop-level signals Etsy's personalisation uses
to decide who to show you to.

> **Fix:** rewrite About to say what you actually are — a digital studio making *test-crocheted* crochet
> patterns and *working* business spreadsheets. Two categories, both credible. If you later add physical
> goods, open a second shop; do not mix a crochet-pattern buyer with a sock buyer.

---

## 2. The market data (what I actually observed on September 13)

**Provenance, stated plainly.** The review counts and prices below were read directly off live Etsy
search/market pages filtered to digital on 2026-09-13 — e.g. 38.7k reviews at $1.92 on a paycheck
budget planner, 43k at $13.92 on a Christmas ornament ebook, 3,775 at $15.00 on a crochet advent
calendar bundle. Those are **verbatim observations**. The `p1` listing counts and the med/max
*summaries* are my reading of a page-1 sample, not Etsy totals — Etsy paginates and personalises, so
treat them as "roughly how crowded", and re-count anything you're about to spend a week on (§4.9 shows
how, in about 60 seconds per keyword). Nothing here is search volume, because nobody has search volume.

### Crochet — your seasonal high ground

| Keyword cluster | p1 | med rev | max rev | Realized $ band | Read this as |
|---|---:|---:|---:|---|---|
| christmas tree skirt crochet | 32 | ~140 | ~900 | $4–$8 | **Beatable.** Ceiling $8. You're at $6. |
| crochet advent calendar | 18 | ~800 | 3,800 | **$8–$40** | **Best niche you can enter.** $15 is normal here. |
| crochet christmas wreath | 28 | ~30 | ~900 | $2–$5 | Thin but shallow. Don't over-invest. |
| christmas crochet ornament bundle | 40 | ~200 | 17,900 | $1.62–$3.99 | Bundle-inflated. Win on gift angle, not count. |
| christmas tree crochet pdf | 45 | ~300 | 43,000 | $2.88–$6.13 | Crowded. Keep, don't build more. |
| christmas gnome crochet | 38 | ~500 | 42,400 | $3.00–$6.13 | Deep moats; no-sew is your only door in. |
| emotional support crochet | 18 | ~400 | 9,000 | $4–$7 | **Thin + giftable. Rewrite this week.** |
| no sew amigurumi (general) | 30 | ~350 | 2,400 | $2.01–$6.50 | 17.9k-review seller at $6.39 proves $5–6 is fine. |
| capybara / axolotl / loaf cat | 24–30 | 150–400 | 900–2,000 | $2.50–$5 | Fine at $4–5. Your $2.62 is a gift to competitors. |
| halloween crochet bundle | 34 | ~400 | 18,000 | $2–$8 | Past peak on Sep 13 — hold to Oct 1, then let it run. |

### Spreadsheets — two different markets wearing one hat

| Keyword cluster | p1 | med rev | max rev | Realized $ band | Read this as |
|---|---:|---:|---:|---|---|
| **budget spreadsheet (generic)** | 70 | 3,000 | 38,700 | $1.76–$17 | **AVOID.** Commodity. You will never rank here. |
| personal finance bundle | 42 | 1,200 | 38,700 | $1.92–$17 | AVOID as a primary; fine as a listing you own. |
| wedding planner spreadsheet | 40 | 900 | 13,400 | $1.06–$21.38 | Crowded but **104-review seller at $13.71** — mid-size shops *can* charge here. |
| etsy seller spreadsheet | 25 | ~300 | 3,400 | $4.99–$23 | **Good.** Your price is already right. Fix copy only. |
| construction estimate / AIA | 14 | ~80 | 900 | $20–$62 | **Best ceiling in your shop.** Needs 30 sales for $1k. |
| school / church management | 15–17 | 60–70 | 450–500 | $13–$35 | **Weak incumbents, high price.** Under-served; these are your moat. |
| cottage bakery | 20 | ~90 | 600 | $9–$12 | Thin, and you have real 5★ reviews on it. Consolidate & push. |
| home renovation budget | 19 | ~110 | 1,400 | $16–$22 | High-ticket life event = low price sensitivity. |
| rental analysis (cap/DSCR) | 22 | ~200 | 2,200 | $8–$12 | Solid. Merge your two rental listings into one. |
| christmas gift tracker | 36 | ~700 | 11,800 | $0.68–$9.99 | Race to the bottom *unless* you add a countdown/budget dashboard. |
| travel planner | 29 | ~250 | 2,600 | $6–$8 | Weak. Keep, don't build more. |

### What buyers reward in these two markets (patterns I saw repeated on page 1)
- **Numbers in titles.** "12 Christmas Granny Squares", "52 tabs", "26 tabs", "42/54/66 inch", "20-in-1".
- **"Excel & Google Sheets" both named** — it's a filter and a fear-remover.
- **"Dark mode"** showing up as a *product feature* in budget spreadsheets. Genuinely. Steal it.
- **Video walkthrough as an included asset** — the sellers charging 2× your price mention a YouTube
  walkthrough in the *title*, not the description.
- **Aggressive first-year discounts** ($2.00 from $7.99 = 75% off) on new-but-good listings to buy the
  velocity that gets them on page 1 — then the discount is walked back to 25–35%.

---

## 3. The plan to $1,000

### 3.1 Where the money comes from — two ways to get there, one of them real
Run `python3 novality_seo_model.py`. It scores 46 keyword targets (your 36 listings + 9 new candidates
+ 2 "avoid" benchmarks) and prints **two** plans. Comparing them *is* the lesson:

| | Scenario A — everything eligible | Scenario B — only listings that pay ≥$7 net |
|---|---|---|
| Sales needed | 196 | **104** |
| Per week | 15.1 | **8.0** |
| Listings carrying it | 26 | **10** |
| Blended realized price | $6.61 | **$11.32** |
| Blended net per sale | $5.54 | **$9.80** |
| Visits required @2.5% CVR | ~7,840 | **~4,160** |
| Lands | $1,085 net | $1,019 net |

Same revenue. **Half the sales, half the traffic, because the average price doubled.** Nothing else in
this document will move your quarter as far as that line does, and it cost zero new products — it is
purely the repricing in `Q4_LISTINGS.md`.

Scenario B is the one to run. Your 16 cheap crochet listings are still worth keeping (favourites,
browse, cross-sells, the occasional December winner) — they just don't get to be *the plan*.

That 8/week is still ~11× your trailing rate (9 sales in 13 weeks). It will not come from SEO. It comes
from three things stacked:

| Lever | Effect | Cost |
|---|---|---|
| Price: $1.50–3.75 → $6–17 on the same files | 2.5–4× revenue per sale | an afternoon, zero new work |
| Photos: renders → real samples + video | CTR and CVR; the reviews that make the next 9 months work | 6–10 weekends |
| Volume: 12 strong listings → 26, all seasonal-timed | more impressions, more shots on goal | the quarter |

If you do only the first, a realistic Q4 is **$300–450**. First + second: **$700–1,100**. All three:
$1,000 with margin, and a shop that starts January with momentum. That's the honest distribution.

### 3.2 The week-by-week

**Now → Sep 27 · Stop the bleeding (no new listings this week)**
- [ ] Reply publicly to the 1★ on the axolotl listing (§1.1.4).
- [ ] Delete the permanent 25% sitewide sale. Then set a **scheduled** sale (§4.4).
- [ ] Reprice all listings per `Q4_LISTINGS.md` (36 rows, list/sale pairs given). One hour, and it is the highest-value hour of the quarter.
- [ ] Retire the 5 colouring listings (keep only the dot-marker activity SKU, re-angled) → archive, don't delete (keeps any history).
- [ ] Merge the two Cottage Bakery listings into the one with reviews. Split the two rental listings by intent (S8 = analysis before you buy, S16 = management after you own) and cross-link them — see S16's note.
- [ ] Rewrite About: two categories, no socks, no yoga mats.
- [ ] Add the real-photo disclaimer to every render-only listing.
- [ ] Turn on Etsy's *"include me in Etsy Ads"* for your top 8 only, $3/day (you're under $10k so ads
      are optional and offsite-ads enrolment is your choice — decide deliberately).

**Sep 28 – Oct 12 · Ship the copy**
- [ ] Paste the rewritten listings: 35 shop + 8 new builds, titles, 13 tags, descriptions (`python3 listing_pack.py` → `Q4_LISTINGS.md`). Work in three sittings of ~14 and tick each listing's **verify** boxes as you go, not after.
- [ ] Start sample #1 (tree skirt). One real photo set = 10 slots filled.
- [ ] Build **N1 Crochet Advent Calendar (24 minis)**. This is your quarter's single best decision. `Q4_BUILD_BRIEFS.md` is the build spec — page by page,
mini by mini. Build to the promise, or cut the promise first, then `python3 check_promises.py` to prove
the two still agree.
- [ ] Build **N6 Christmas Dinner Planner spreadsheet** (fastest asset you own: you already have 90% of
      the plumbing in the Family Budget sheet).
- [ ] Publish Nov-1-window listings *now*, not on Nov 1. The newness window needs the runway.

**Oct 13 – Nov 2 · Volume + proof**
- [ ] Recruit 2–3 pattern testers; ship them every Christmas pattern.
- [ ] 5 new listings: table runner (N2), mini stockings, Christmas card/address tracker, Secret Santa
      tracker, holiday countdown wall sheet.
- [ ] Refresh the Halloween set's *photos and tags* — don't renew it, edit it (renewing resets nothing;
      editing keeps accumulated engagement).
- [ ] Check Stats weekly. Log in `q4_weekly_tracker.csv`.

**Nov 3 – Dec 2 · Black Friday, where spreadsheets earn**
- [ ] Nov 24 – Dec 1: 35–40% off **business** spreadsheets only. Contractors and shops buy tools then;
      nobody buys a budget planner on Black Friday.
- [ ] Push N1 + C1 + C5 (advent/tree skirt/gnome) hard; these are the December earners.
- [ ] Add video — Etsy caps listing video at 5–15 seconds, so plan the shot: one slow pan over the
      finished object, or one 12-second scroll of the dashboard. No talking, no music edit needed.

**Dec 3 – Dec 28 · Harvest, then hand off to January**
- [ ] Dec 12 is the practical cut-off for "make this before Christmas" patterns. After that, sell the
      *planning* products (gift tracker → Dec 20; New Year money reset → Dec 26).
- [ ] Publish the New Year reset (N9) on Dec 26 — Q4's free tail, and January's head start.
- [ ] Dec 27–28: pull every Q4 listing's stats into one sheet. Kill nothing before Jan 15 (small
      samples lie), rewrite the bottom half in January.

---

## 4. Lessons — the craft, so you can do this without me

### 4.1 Title formula (140 chars, three tiers of importance)
```
[Buyer's exact phrase] + [number/spec differentiator] + [use or gift context] + [format promise]
 └─ chars 1–47: decides the click. Put the noun phrase + number HERE.
```
Do: `Crochet Christmas Tree Skirt Pattern, Bobble Snowflake Tree Collar, 3 Sizes 42 54 66 Inch, …`
Don't: `Christmas Tree Skirt Crochet Pattern PDF, Bobble Snowflake 12-Spoke Circle, 3 Sizes, Instant Download`
— the second is *almost* right; it's the one you have now. The difference is "Tree Collar" (a second
search phrase) and the concrete inches (the thing buyers actually check before adding to cart).

Rules: start with the exact phrase, not an adjective. Never `Digital Download` as your opener — every
competitor says it, so it's zero information at position 1. No ALL CAPS, no emoji, no `||` pipes
(Etsy's own guidance and most high-performers use commas; pipes are a legacy-Marmaleid habit).

### 4.2 Tags: 13 slots, 20 chars, and how to spend them
The mix that covers the most ground without wasting slots:
- **4 primary** — the product, phrased differently than the title (`tree skirt crochet`, `crochet tree collar`)
- **4 long-tail buyer-intent** — how a person types when they know what they want (`christmas tree decor`, `bobble stitch`)
- **3 occasion/audience** — (`beginner crochet`, `holiday crochet`, `crochet gift`)
- **2 discovery** — adjacent terms you'd honestly rank for (`amigurumi christmas`, `xmas tree decor`)

Mistakes that silently cost you:
1. **Singular/plural duplicates** — Etsy collapses them. `crochet pattern` + `crochet patterns` = one slot wasted.
2. **Exact title duplication** — a tag identical to a title phrase adds nothing; you already rank on it.
3. **Over-20-char tags** — the tag field caps at 20 characters, so a longer phrase is simply lost at the
   moment you paste it and the slot goes unfilled. This is why `listing_pack.py` validates length: **24 of
   my own first-draft tags were over the limit**, across 12 of 14 listings, and I only caught it because a
   script measured them. That's not an insult to me — it's why professionals use a checklist instead of a feeling.
4. **Irrelevant tags to mop up traffic.** Etsy tracks CTR *per tag*. A tag that gets shown and not
   clicked lowers your listing quality score for that query and, over time, the listing.

### 4.3 Description — write it for the second reader
Etsy reads your description for SEO but the *weight is lower than title+tags*. So write for the person
who is already interested and needs objections removed. The order that works for patterns:
1. **2 lines of voice** (indexed first 160 chars — put primary keywords in natural sentences here)
2. **WHAT YOU GET** — file count, terms (US+UK), sizes, what's *not* required
3. **SKILL LEVEL** — name the 5 stitches. This is the #1 pre-purchase question and most sellers hide it.
4. **MATERIALS** — yarn weight, yardage, hook. Give a "before you buy" so people don't bounce later.
5. **MADE FOR** — who gifts this / what occasion. This is where you convert the non-maker.
6. **INSTANT DOWNLOAD** — one line, removes the shipping anxiety.
7. **TERMS** — personal use, finished items sellable, no file sharing. Say it plainly; it prevents disputes.
8. **SUPPORT** — a promise to answer. For a 3-review shop, this line outsells a badge.

For spreadsheets, replace 3–4 with **WHAT IT DOES** (tab by tab), then **"Excel + Google Sheets"**, then
**"no formulas to write"**, then **video walkthrough included**. Buyers of spreadsheets fear two things:
that it's ugly, and that they'll have to build formulas. Answer both before they ask.

### 4.4 The discount ladder (how to use a sale without becoming a sale shop)
1. Set **list price = your real price × 1.4–1.7**. That's the anchor; nobody ever pays it, and it's not a
   lie — it *is* your price when no promotion runs.
2. **Schedule** sales with dates: launch week 45–55% (velocity buys rank), then 30–33% steady state,
   40% on Black Friday, and *no sale* in between. A listed, dated sale looks like an event; a
   permanent one looks like a clearance rack.
3. Use **coupons**, not sale prices, for the levers that need targeting: 15% off for first-time buyers
   (new-customer conversion), 20% off for abandoned carts (recovers 5–10% of a week's traffic),
   and **buy 1 get 2nd at 40%** — which is how you raise AOV in crochet, where people buy 2 patterns
   anyway. AOV is the quiet multiplier: 260 sales of one $6 pattern ≈ 150 sales of a $10 two-pack.
4. Never discount below the point where your net-per-sale stops mattering. $5.50 is roughly where
   fixed fees ($0.45 + $0.20) start eating the price instead of the margin.

### 4.5 Images — the actual CTR lever (and how to measure it)
10 slots, filled. Slot 1 is an ad, not a photo: object at 70–80% of frame, high contrast, ≤4 words of
text (the name, or "No-Sew · 3 Sizes"). Then: 2 in-context lifestyle, 3 close-up stitch/formula detail,
1 "what's included" card, 1 sizes/spec card, 1 review screenshot, 1 video.

**How to A/B a first image, given what Etsy actually shows you in 2026.** Verify before you trust anyone,
including this document:
- **Stats → Shop Traffic** gives views, visits, orders and conversion rate, and lists your listings *sorted
  by views*. Mind the definitions: one shopper opening 5 of your listings = 5 **views**, 1 **visit**. So
  views-per-listing is a *click* proxy, not an impression one.
- Etsy's old **Marketing → Search analytics** (the impressions-per-query table many blogs still cite) has
  been **removed from the seller toolset**. If a guide sends you there, it is out of date.
- The one place you *can* get impressions and click-through **per listing, per search term** is
  **Promoted Listings → click the link under a listing's title → search term analytics**. Two-day lag, and
  it needs enough ad traffic before it appears.

Practical method: change one listing's slot 1, then watch **that listing's share of total shop views** for
14 days. If its share moves after the image change, the change worked — that comparison is free and it is
yours. Below ~200 views, decide nothing; you are reading noise. This is also the real reason to run a
small launch ad (§4.7): **it is the only way to see the query data at all.**

### 4.6 The things that aren't keywords but still rank you
- **Attributes/category depth.** Pick the deepest subcategory available and fill *every* attribute. They
  feed the sidebar filters, which is traffic you get for free because most sellers skip them.
- **Video.** 5–15s, even a screen-record. Listings with video earn a play badge in the grid — pure CTR,
  near-zero effort, and most of your competition hasn't done it.
- **Shop activity.** Steady weekly publishing beats one 20-listing weekend. Etsy's model rewards recent
  engagement and a shop that looks alive. Two listings a week, every week.
- **Renew vs refresh.** Editing a live listing keeps its history; renewing (or re-listing) does not buy
  you a fresh boost worth having. Fix, don't repost.
- **Star Seller is reachable this quarter, and you should chase it deliberately.** Not 50 sales — the
  real bar is: 90 days since your first sale ✓, **5 orders + $300 in sales** in the rolling 3-month
  window, **4.8+ average rating**, and **95% of first messages replied within 24h**. Digital sellers
  skip the shipping/tracking metric entirely.
  - $300 at your Scenario-B average ($11.32) = **27 sales**. That is a mid-November badge, not a 2027 one.
  - The rating is the hard part and it's arithmetic, not vibes: your three reviews are 5, 5, 1 → 3.67.
    To reach 4.8 you need **~17 more five-star reviews** on a straight average (34 if new ones average
    4.9). Etsy weights recent reviews more heavily, so it arrives faster than the straight mean suggests —
    but budget 17 *perfect* reviews as your Q4 product goal and everything in §1.1 follows from it.
  - **And a rule that should terrify you right now:** under 40 total reviews, no more than **4** can be
    rated 3★ or lower. You already have one. Three more angry "the photo was a lie" reviews and the badge
    is mathematically gone for the year. That is the concrete cost of not photographing your samples.
  - Treat "request a review on every completed order" as a paid task, not a nice-to-have. A thank-you
    message with one line — *"if it came out well, a photo in the review helps other makers more than you
    know"* — is the cheapest conversion lever in your entire shop, because the badge lifts every listing at once.

### 4.7 Etsy Ads: the maths that says "mostly don't"
Run `python3 q4_tracker.py` — it prints this table, which is the single most
important thing to understand before you spend a dollar:

```
break-even CPC = net per sale × conversion rate
  net $5.54  →  $0.055 @1% CVR   $0.139 @2.5%   $0.277 @5%
  net $9.80  →  $0.098 @1% CVR   $0.245 @2.5%   $0.490 @5%
  net $15.00 →  $0.150 @1% CVR   $0.375 @2.5%   $0.750 @5%
Etsy's typical cost per click for digital: $0.15 – $0.45.
```

Read it sideways: **at your current $1.50–3.50 prices, every click is guaranteed to lose money**, and
there is no clever bid that fixes that. At a $15 net you break even around $0.375, which is winnable.
Pricing is not just revenue — it is what makes advertising possible at all.

So the correct ad policy is small and specific — and note what you are really buying. **Promoted
Listings is the only place Etsy hands you per-listing, per-query impressions and CTR**, so a tiny ad
budget is also your analytics budget. Without it you are optimising blind.
- **One listing at a time, launch week only.** $3–4/day on N1 (advent) when it publishes: that buys
  (a) the first 3–5 reviews, (b) the search-term report that tells you which queries you should have
  built the listing for. Then switch it off. You are buying *evidence*, not revenue.
- **Read that report at 7 days, not 1** (Etsy needs 2 days just to compute it). Sort by impressions, then
  look for the queries where clicks or sales show as *above average* — those become your next listing's
  title, and your next product.
- **Never spread $5/day across 20 listings** — you'll get 3 impressions each and learn nothing.
- **Kill rule:** $20 spent, 0 sales → the listing is wrong, not the audience. $20 spent, 1 sale,
  CVR <1% → fix images/price before spending again.
- **Offsite Ads:** you're under $10k, so enrolment is your choice. Opt *in* if you want the extra
  reach at 15% and your net-per-sale is >$10; opt *out* of the cheap listings. Decide per price tier,
  not for the shop as a whole — at $5 net, paying 15% for an attributed sale is $0.75 off a $5.54 margin
  for a sale that would likely have happened anyway.

### 4.8 Closing the traffic gap honestly (the part nobody puts in a plan)
The plan needs ~320 visits/week by October and ~470 by November. Your shop is currently getting roughly
35–60. **That gap is the real project**, and Etsy search alone will not close it in 13 weeks. What can:

| Source | Realistic multiplier | Cost | Do it? |
|---|---|---|---|
| Season (Oct–Dec Etsy holiday search surge) | 1.5–2.5× on gift keywords | free | automatic if you're live before Oct 15 |
| 12 more *targeted* listings (thin keywords, not more of the same) | 1.3–1.8× | your time | yes — the main lever |
| Real photos + video (CTR 0.6% → 1.0%+) | same impressions, 1.7× the visits | a weekend | **highest ROI on this list** |
| Pinterest: 3 pins/day from your sample photos, linked to listings | 10–40 visits/wk, compounds | free, tedious | yes — crochet + printables are Pinterest-native |
| 1 short reel per pattern (the making, not a slideshow) | volatile, occasionally big | free | 2/week max; stop if 0 views after 8 |
| Ravelry listing for every crochet pattern (free, with a link back) | small but perfectly-qualified | free | yes; expect some to buy there. Take it. |
| Etsy Ads | ~10–25 visits/wk, expensive | $30–120/mo | launch weeks only (§4.7) |
| Email/favourites drip: message buyers a 20% thank-you coupon for the *next* pattern | repeat buyers are your cheapest sale | free | yes, every order |

Stacked realistically, that's **3–5× your traffic**, which lands you at $500–800 net rather than $1,085 —
and that's the honest expected value of this plan if executed well. Two ways to close the rest:
**raise average price further** (the $30–38 business bundles need only 3–4 sales each; three more of
those is faster than ten more $6 patterns) or **extend the window** (Q4 into January's planner season,
which is why N9 exists).

> Set your own threshold now, before December, so you can't move it later: *"If I am under $700 net by
> Dec 14, I will not panic — I will ship 5 more business-spreadsheet listings in January, because that is
> where my price ceiling is $17 and my competition is 15 listings deep."*

### 4.9 What I could not tell you, and how to find out
I can't give you search volume for `christmas tree skirt crochet pattern`. You can get the next best
thing in ten minutes, for free, from Etsy itself:
1. Type your seed into Etsy's search bar and **write down all 10 autosuggestions in order** — that list is
   ranked by real searches. Anything in it has demand; anything you invented does not.
2. For each suggestion, search it with **digital-only** applied and count page-1 listings. <25 = your
   kind of keyword. 60+ = don't.
3. Sort that search by **Highest customer reviews** and record the top 10 prices + review counts. That's
   your ceiling and your bar.
4. Then run your repo's own scraper, which does exactly steps 2–3 for 20 keywords and scores them:
   ```bash
   pip install -r requirements.txt && python -m camoufox fetch
   python etsy_research.py --skip-reddit \
     --keywords "christmas tree skirt crochet, crochet advent calendar pattern, etsy seller spreadsheet, \
                 church management spreadsheet, cottage bakery spreadsheet, construction estimate spreadsheet, \
                 secret santa gift exchange spreadsheet, christmas dinner planner"
   ```
   Its `opportunity` score (0–100) rewards low page-1 count + real reviews + high price — the same three
   things §2 above graded you on. Trust it for *ordering*, not for absolute values.
5. Every two weeks, pull your own **Stats → Search terms** (queries that led to orders) and, if a listing
   is being promoted, **Promoted Listings → search term analytics** for that listing — that is the only
   place you will see real impressions and click-through per query. The day those numbers arrive, my
   estimates become *your* measurements and this document turns from a plan into a starting point.

---

## 5. Score model — what the numbers in `novality_q4_scores.csv` mean

| Column | Definition | Direction |
|---|---|---|
| `demand_score` | 0–100 from page-1 median/max review counts + price level. Relative buyers, not volume. | higher = more |
| `competition_score` | 0–100 from incumbent moat (max reviews), bar-to-look-legit (median), and crowding (p1 count). | **higher = harder** |
| `ctr_headroom` | 0–100 of unclaimed click levers on page 1: video, number-hooks, bundle angles, real photos, front-load. Not a CTR. | higher = more you can win |
| `est_ctr_lift_pct` | `headroom × 0.35` — a planning figure for "if I fix these", not a forecast | — |
| `p75_sale` | 75th percentile of realized page-1 prices = **your ceiling** | — |
| `rec_realized` | what I'd charge now (ceiling, or 85% of it in commodity clusters) | — |
| `net_per_sale` | after the 2026 fee stack | — |
| `sales_to_net_1k` | sales for **that one listing** to carry the whole $1,000 | lower = leverage |
| `verdict` | one gate (price ceiling ≤ $3 = joinable only by luck) + the ranking | `DO NOW → SHELVE` |
| `move` | the single action: `RAISE PRICE`, `BUILD IT`, `PRICE OK — rewrite only`, `RETIRE` | — |
| `leverage` | how much of the $1,000 this listing could carry alone: HIGH ≤100 sales, MEDIUM ≤180, LOW >180 | higher = fewer sales needed |
| `opp_value_upside` | points earned purely from "page 1 charges more than you do" | — |
| `opp_thin_bonus` | points for a keyword with ≤25 page-1 listings *and* real demand | — |
| `opp_moat_penalty` | capped at −12; a big incumbent hurts only if demand is weak *and* the niche is commoditised | — |

Two cautions so you don't over-trust it: review counts understate demand for *new* niches (nothing has
reviews yet) and they overstate what you need to *enter* (you need 5–15, not 400). The model's job is to
rank where your hours go, not to predict your December.

---

## 6. Weekly scorecard — fill this in, it's the whole feedback loop

`q4_weekly_tracker.csv` is pre-built with the 13 weeks. Six columns, ten minutes a week:

| Metric | Where | Healthy | Do this if unhealthy |
|---|---|---|---|
| Views | Stats → Shop Traffic | rising wk/wk | this is your only *free* per-listing signal. Flat views = not surfacing: publish 2 more, or the season hasn't turned |
| View **share** per listing | views ÷ total views | top 5 listings own 40–60% | a listing with 3% of views and 15% of listings = bad image or wrong keyword; rewrite slot 1 + first 47 chars |
| CTR | Promoted Listings → search term analytics (needs a live ad) | **≥1.0%**; 0.4–0.7% typical for render-only photos | replace slot-1 image, add number-hook to title, add video |
| Visits | Stats | — | — |
| Conversion | Stats → Shop Traffic | **1.5–3%** on digital | real photos, price is above the ceiling (§2), or reviews are scaring them |
| Orders | Stats | toward 8/wk (Scenario B) | check the funnel top-down; the leak is always one stage |
| Revenue | Finances | toward $1,000 cumulative | don't chase this column; it's the output |

**Kill rule (so you stop bleeding time):** a listing that after 3 weeks has **<2% of your shop's views**
and no favourites → rewrite image #1 + the first 47 characters. If CTR fixes and conversion is still <0.8% → the *offer* is wrong:
price down to the ceiling or bundle it into a stronger listing. Still dead at 8 weeks → archive it.
One rewrite per listing per fortnight; constant fiddling resets your own ability to read results.

---

## 7. The 80/20 of this entire document

1. **Real photos, then everything else.** You have one review saying why you don't convert, and the
   Star Seller math gives you a hard deadline on that: you can only afford **3 more** reviews rated 3★ or
   lower this year. Your product goal for Q4 is **17 five-star reviews**; everything else serves that.
2. **Stop selling at $1.50–3.75.** Reprice from `Q4_LISTINGS.md` today — same files, ~2.5× revenue.
3. **Build the advent calendar pattern** at $15 and the **Christmas dinner planner** at $9. Those two
   are the quarter's highest net-per-sale things within your actual skill set.
4. **Retire the coloring pages.** No keyword work saves a $2 ceiling against 3,100–5,900-review incumbents.
5. **Clear $300 / 5 orders in a rolling quarter = the Star Seller badge.** At Scenario-B pricing that is
   ~27 sales, which is a mid-November milestone — and the badge lifts conversion on all 36 listings at once.
6. **2 new listings + 1 rewrite a week, logged in the tracker.** Ranking is a lagging indicator — you
   are buying December's traffic with October's consistency.

You are not starting from nothing. You have 36 listings that prove you can *ship*, two review-bearing
spreadsheet listings, and 15 patterns in the one Q4 category (holiday crochet) where buyers still pay
$6–15 for a PDF. What's missing is evidence (real photos, reviews) and price discipline. Both are
fixable inside 13 weeks.
