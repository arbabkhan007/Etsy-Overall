# etsy-niche-research

![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

A CLI pipeline for finding, writing, and posting profitable Etsy digital products — from niche discovery to live listing.

```
etsy_research.py  →  generate_listing.py  →  create_listing.py
  find niches          write copy w/ AI        post to Etsy
```

---

## Quick start

```bash
git clone https://github.com/moooosik/etsy-niche-research.git
cd etsy-niche-research
pip install -r requirements.txt
python -m camoufox fetch
```

Then run the full pipeline:

```bash
# Step 1 — find a niche
python etsy_research.py --skip-reddit --keywords "autism routine chart, trail running plan"

# Step 2 — generate listing copy with Claude AI
python generate_listing.py --keyword "autism routine chart printable" --data etsy_research.json

# Step 3 — post to Etsy
python create_listing.py --spec listing.json --file chart.pdf --image cover.jpg --draft
```

---

## Step 1 — etsy_research.py

Validates Etsy niches against live market data. Scores each keyword 0–100 based on competition, proven demand, and price.

**Phase 1 (optional):** scrapes Reddit (r/EtsySellers, r/passive_income, r/sidehustle) to surface keyword ideas from real seller discussions.

**Phase 2:** opens a fresh headless browser per keyword, searches Etsy filtered to digital listings only, and extracts competitor count, prices, and review counts.

### Example output

```
ETSY NICHE OPPORTUNITY SCORECARD
Generated: 2026-07-24 12:15
Keywords:  30
===========================================================================

#   KEYWORD                                SCORE  DL#   AVG $   MAX REV
---------------------------------------------------------------------------
1   autism routine chart printable         88.0   5     $10.12  148
2   perimenopause symptom tracker          68.0   6     $8.48   33
3   mother of the bride gift printable     83.0   4     $6.68   406
4   trail running training plan printable  78.0   6     $11.17  120
5   home buying checklist printable        75.0   6     $2.18   580
...

TOP 12 NICHES — FULL DETAIL
===========================================================================

Keyword     : autism routine chart printable
Score       : 88.0/100
Competition : 5 digital listings on page 1
Avg price   : $10.12
Max reviews : 148  (avg 52.3)
  [148 reviews]  $5.99  ADHD Autism Visual Schedule Cards, Daily Routine
  [ 73 reviews]  $3.39  Visual Schedule with Activity Icons - 5 Routine S
  [  9 reviews]  $2.50  Autism Daily Planner | Visual Schedule, Routine
```

`DL#` = digital-only listing count on page 1 (lower = less crowded). `MAX REV` = highest review count on page 1 (higher = proven buyers exist).

### Usage

```bash
python etsy_research.py                                       # full run (~25 min)
python etsy_research.py --skip-reddit                         # Etsy only, faster
python etsy_research.py --keywords "grief journal, sobriety tracker"
python etsy_research.py --add-keywords "PCOS symptom log"    # append to seed list
python etsy_research.py --output results_aug --top-n 20      # custom output + detail depth
```

### Scoring formula

```
base = 40

competition (DL# on page 1):
  ≤ 5  → +30    (underserved niche)
  ≤ 15 → +20    (low competition)
  ≤ 25 → +10    (moderate)
  > 25 → -5     (saturated)

demand (max reviews):
  > 500 → +15   (strong signal)
  > 100 → +10
  > 20  → +5
  = 0   → -10   (unproven)

revenue (avg price):
  > $20 → +15
  > $10 → +8
  > $5  → +3
```

---

## Step 2 — generate_listing.py

Calls the Claude API to write a fully optimized Etsy listing: title (≤140 chars), description (400–600 words), and exactly 13 SEO tags. When `etsy_research.json` is present, it feeds in competitor prices and review counts so the copy is positioned against the real market.

### Setup

```bash
export ANTHROPIC_API_KEY=your_key_here
```

### Usage

```bash
python generate_listing.py --keyword "autism routine chart printable"
python generate_listing.py --keyword "trail running plan" --data etsy_research.json
python generate_listing.py --keyword "perimenopause tracker" --output tracker.json
```

### Example output

```
Market data found: 88/100 score, $10.12 avg, 148 max reviews

Generating listing for: autism routine chart printable

✓ Saved → listing.json

  Title : Autism Routine Chart Printable | Visual Daily Schedule for Kids, ADHD Morning Routine Cards
  Price : $8.99
  Tags  : autism routine chart, visual schedule kids, adhd daily planner, morning routine printable,
          autism classroom, special needs chart, pecs visual cards, kids routine printable,
          autism mom gift, adhd printable, visual schedule autism, routine chart kids, autism tools

Next:
  python create_listing.py --spec listing.json --file product.pdf --image cover.jpg --draft
```

---

## Step 3 — create_listing.py

Posts a digital listing directly to Etsy via the API — title, description, tags, price, digital file upload, and optional cover image.

### Setup (one time)

1. Create an app at [etsy.com/developers](https://www.etsy.com/developers/register)
   - Set redirect URI to `http://localhost:3003/callback`
2. Create `etsy_config.json`:
   ```json
   {"client_id": "your_keystring_here"}
   ```
3. Authenticate (opens browser):
   ```bash
   python create_listing.py --auth
   ```

### Usage

```bash
# From a spec file (output of generate_listing.py)
python create_listing.py --spec listing.json --file product.pdf --draft

# Or fully inline
python create_listing.py \
  --title "Autism Routine Chart Printable | Visual Daily Schedule" \
  --tags "autism routine chart,visual schedule,adhd planner" \
  --price 8.99 \
  --file chart.pdf \
  --image cover.jpg \
  --draft
```

`--draft` saves without publishing so you can review on Etsy first.

---

## Notes

- Etsy occasionally returns short responses (bot protection). The script retries automatically with a backoff delay.
- `etsy_config.json` and `etsy_tokens.json` are gitignored — never commit them.
- Requires Python 3.10+
- `generate_listing.py` requires an [Anthropic API key](https://console.anthropic.com/)

---

## Q4 shop workbench (NovalityStore)

Five files built on top of the pipeline above, aimed at one shop's quarter rather than niche discovery.
Two checks matter before anything ships: `listing_pack.py --check` (does the field fit Etsy's limits?) and
`check_promises.py` (does the product actually contain what the copy says?).

```bash
python3 listing_pack.py        # validate + emit Q4_LISTINGS.md and q4_listings.csv
python3 novality_seo_model.py  # score 47 keyword targets; prints both portfolio scenarios
python3 q4_tracker.py          # regenerate q4_weekly_tracker.csv from the model's current answers
python3 check_promises.py      # fail if a listing promises a number the build spec doesn't deliver
```

| File | What it is |
|---|---|
| `Q4_PLAYBOOK.md` | diagnosis, live market data, method, and the funnel maths behind the plan |
| `Q4_LISTINGS.md` | paste-ready copy for all 36 live listings + 8 new builds: title, 13 tags, description, price, dated sale window, verify checklist |
| `Q4_BUILD_BRIEFS.md` | how to actually build the 8 new products: page plans, round scaffolds, tab schemas, formulas, the Secret Santa script |
| `check_promises.py` | the anti-refund check: every countable claim in the copy must have a spec behind it |
| `q4_listings.csv` | the same, in spreadsheet form |
| `novality_seo_model.py` | scoring engine: demand, competition, CTR headroom, price ceiling, unit math |
| `novality_q4_scores.csv` | 47 scored keyword targets with a verdict and a single "next move" each |
| `q4_weekly_tracker.csv` | 13-week plan: one job per week, targets vs. actuals |

`listing_pack.py` is also useful standalone: it enforces Etsy's real field limits (140-char titles,
13 tags of ≤20 characters, no singular/plural collisions, discount-band checks) before you paste copy
into the listing editor. Point `LISTINGS` at your own data (long-form copy lives in `listings_copy.py`) and it will tell you what
you got wrong — which is exactly how 24 over-length tags and 3 too-shallow discount badges got caught in
the first draft here. The validator never once let a broken field through to the output file.

Scoring is deliberately built from **observable** quantities only (page-1 listing counts, review counts,
realized prices). Etsy does not publish search volume or CTR, so anything claiming either is a model.
Replace the assumptions with your own Shop Stats numbers and the model gets honest about *your* shop.

---

## Support

If this saved you time, [GitHub Sponsors](https://github.com/sponsors/moooosik) is appreciated but never expected.

`make_brand_assets.py` draws the shop's brand kit (banner, icon, logos, section headers,
listing templates) at Etsy's real pixel specs, and `BRAND_KIT.md` explains the rules.
Deterministic on purpose: the assets have to survive being 160px in a search result.
