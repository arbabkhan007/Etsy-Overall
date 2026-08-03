# etsy-niche-research

Two CLI tools for finding and listing digital products on Etsy.

- **`etsy_research.py`** — scrapes Reddit for niche ideas, validates each against live Etsy search data, and outputs a ranked opportunity scorecard
- **`create_listing.py`** — creates a digital Etsy listing from the command line (title, description, tags, price, file upload, image upload)

---

## etsy_research.py

Runs a 2-phase pipeline:

1. **Reddit** — searches r/EtsySellers, r/passive_income, r/sidehustle for niche keyword ideas
2. **Etsy** — validates each keyword: how many digital listings are on page 1, what are the prices, how many reviews do top listings have

Scores each niche 0–100 based on low competition + proven demand + price.

### Example output

```
ETSY NICHE OPPORTUNITY SCORECARD
Generated: 2026-07-24 12:15
Keywords: 30
===========================================================================

#   KEYWORD                                SCORE  DL#   AVG $   MAX REV
---------------------------------------------------------------------------
1   mother of the bride gift printable     83.0   4     $6.68   406
2   autism routine chart printable         80.0   5     $3.30   111
3   trail running training plan printable  78.0   6     $11.17  120
4   movie themed baby shower printable     75.0   6     $3.50   599
5   home buying checklist printable        75.0   6     $2.18   580
...

TOP 12 NICHES — FULL DETAIL
===========================================================================

Keyword     : mother of the bride gift printable
Score       : 83.0/100
Competition : 4 digital listings on page 1
Avg price   : $6.68
Max reviews : 406  (avg 258.5)
  Top listings:
    [ 406 reviews]  $8.25  Mother of the Bride Gift, Custom Photo Collage
    [ 111 reviews]  $4.99  Mother of Bride Gift Card, Personalized for Mom
    ...
```

`DL#` = number of digital-only listings on page 1 (lower = less crowded). `MAX REV` = highest review count among page-1 listings (higher = proven buyers exist).

### Requirements

```
pip install camoufox requests
python -m camoufox fetch
```

### Usage

```bash
python etsy_research.py
```

Outputs `etsy_research.txt` (human-readable scorecard) and `etsy_research.json` (full structured data). Takes ~20–30 minutes — Camoufox opens a fresh browser per keyword to avoid bot detection.

To target different niches, edit the `SEED_NICHES` list at the top of the script.

---

## create_listing.py

Creates a digital Etsy listing from the command line: title, description, tags, price, digital file upload, and optional cover image.

### Setup (one time)

1. Create an Etsy app at [etsy.com/developers](https://www.etsy.com/developers/register)
   - Set redirect URI to `http://localhost:3003/callback`
2. Create `etsy_config.json` in the same folder:
   ```json
   {"client_id": "your_keystring_here"}
   ```
3. Authenticate:
   ```bash
   python create_listing.py --auth
   ```
   Opens your browser, you approve, tokens and shop ID are saved automatically.

### Usage

```bash
# From a spec file
python create_listing.py --spec listing.json --draft

# Or inline
python create_listing.py \
  --title "8-Week Trail Running Plan | Printable PDF" \
  --tags "trail running,training plan,running printable,beginner running" \
  --price 12.99 \
  --file plan.pdf \
  --image cover.jpg \
  --draft
```

`--draft` saves without publishing so you can review on Etsy first. Drop it to go live immediately.

### listing.json format

```json
{
  "title":       "8-Week Trail Running Plan | Printable PDF",
  "description": "A week-by-week beginner trail running plan...",
  "tags":        ["trail running", "training plan", "running printable"],
  "price":       12.99,
  "file":        "plan.pdf",
  "image":       "cover.jpg",
  "taxonomy_id": 68887608
}
```

`taxonomy_id` defaults to `68887608` (Craft Supplies > Patterns > Printables). See [Etsy taxonomy](https://www.etsy.com/developers/documentation/getting_started/taxonomy) for other categories.

---

## Notes

- Etsy occasionally blocks automated searches (body too short warning) — re-running usually clears it
- `etsy_tokens.json` and `etsy_config.json` are gitignored — never commit them
- Both scripts require Python 3.10+

---

## Support

If this saved you time, [GitHub Sponsors](https://github.com/sponsors/moooosik) is appreciated but never expected.
