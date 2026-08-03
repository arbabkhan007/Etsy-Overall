"""
Etsy Niche Research — 2-phase pipeline using headless Camoufox

Phase 1 : Reddit (r/EtsySellers + r/Etsy) → extract niche keyword ideas
Phase 2 : Etsy search validation per keyword:
            - digital listing count (competition)
            - top listing titles / prices / review counts (demand signal)

Note: eRank requires login and has been excluded.

Output:
  etsy_research.json   — full structured data
  etsy_research.txt    — ranked niche scorecard
"""

import json
import re
import sys
import time
from datetime import datetime
from camoufox.sync_api import Camoufox

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_JSON = "etsy_research.json"
OUT_TXT  = "etsy_research.txt"

SEED_NICHES = [
    "hashimoto symptom tracker",
    "ibs fodmap meal planner",
    "ibs symptom tracker",
    "chronic illness tracker printable",
    "adhd daily planner printable",
    "perimenopause symptom tracker",
    "endometriosis pain tracker",
    "sobriety tracker printable",
    "fertility tracking chart printable",
    "grief journal printable",
    "mother of the bride gift printable",
    "movie themed baby shower printable",
    "small business packaging sticker sheet",
    "trail running training plan printable",
    "neurodivergent meal planner printable",
    "wedding budget spreadsheet",
    "home buying checklist printable",
    "autism routine chart printable",
    "menopause symptom tracker printable",
    "fibromyalgia flare tracker printable",
]

REDDIT_SUBREDDITS = ["EtsySellers", "passive_income", "sidehustle"]
REDDIT_QUERIES    = [
    "etsy digital download niche what's selling",
    "etsy passive income digital products",
    "best selling etsy printable niche 2025",
]

DELAY = 2.5

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1 — Reddit
# ─────────────────────────────────────────────────────────────────────────────

def reddit_search(page, subreddit, query) -> list[dict]:
    url = (f"https://old.reddit.com/r/{subreddit}/search"
           f"?q={query.replace(' ', '+')}&sort=top&t=year&restrict_sr=on")
    posts = []
    try:
        page.goto(url, timeout=25000, wait_until="domcontentloaded")
        try:
            page.wait_for_selector("div.search-result-link", timeout=7000)
        except Exception:
            return posts
        time.sleep(1.0)
        for link in page.query_selector_all("div.search-result-link a.search-title")[:8]:
            try:
                title = link.inner_text().strip()
                href  = link.get_attribute("href") or ""
                if title and href:
                    posts.append({"title": title, "url": href, "subreddit": subreddit})
            except Exception:
                continue
    except Exception as e:
        print(f"    Reddit error r/{subreddit}: {e}")
    return posts


def scrape_post(page, url) -> str:
    try:
        if "old.reddit.com" not in url:
            url = url.replace("www.reddit.com", "old.reddit.com")
        page.goto(url, timeout=25000, wait_until="domcontentloaded")
        try:
            page.wait_for_selector("#siteTable", timeout=7000)
        except Exception:
            return ""
        time.sleep(1.2)
        # post selftext
        thing = page.query_selector("#siteTable > .thing.self")
        text = ""
        if thing:
            body_el = thing.query_selector(".usertext-body .md")
            if body_el:
                t = body_el.inner_text().strip()
                if not t.lower().startswith("welcome to r/"):
                    text = t[:2000]
        # top comments
        comments = []
        for el in page.query_selector_all("div.commentarea > div.sitetable > div.thing.comment")[:5]:
            try:
                b = el.query_selector(".usertext-body .md")
                if b:
                    ct = b.inner_text().strip()
                    if ct and ct not in ("[deleted]", "[removed]"):
                        comments.append(ct[:300])
            except Exception:
                continue
        return text + "\n".join(comments)
    except Exception:
        return ""


NICHE_PATTERNS = [
    r'([a-z][a-z\s]{4,40}?)\s+(?:tracker|planner|journal|worksheet|template|checklist|printable)\b',
    r'(?:selling|sold|works?|niche)[:\s]+([a-z][a-z\s]{4,45}?)(?:\s+on etsy|\s+digital|[,.\n])',
]
def extract_niches(text: str) -> list[str]:
    text = text.lower()
    found = set()
    for pat in NICHE_PATTERNS:
        for m in re.finditer(pat, text):
            c = m.group(1).strip().strip("'\"")
            if 5 < len(c) < 50 and c.count(" ") < 6:
                found.add(c)
    return list(found)


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2 — Etsy scraper (fresh browser per keyword)
# ─────────────────────────────────────────────────────────────────────────────

def parse_listings(body: str) -> list[dict]:
    """
    Parse Etsy inner text. Each digital listing block looks like:
      Digital download\n\n[TITLE]\n\nBy [SHOP]\nFrom shop [SHOP]\n\n[PRICE]\n...
    Reviews appear as standalone "(NN)" lines; rating as "N.N" before them.
    """
    listings = []
    # Split on "Digital download" boundary
    blocks = re.split(r"Digital download\s*\n+", body)
    for block in blocks[1:]:   # skip content before first listing
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue

        title = lines[0]
        if len(title) < 5 or title.lower().startswith(("by ", "from ", "add to", "more like")):
            continue

        # Price — first $N.NN in block (sale price or regular)
        price_m = re.search(r"\$\s*([\d.]+)", block)
        price = float(price_m.group(1)) if price_m else 0.0

        # Review count — "(NN)" patterns; pick largest (avoids "25% off" style)
        review_nums = [int(x) for x in re.findall(r"\((\d+)\)", block)
                       if not block[block.find(f"({x})") - 1].isdigit()
                       and int(x) > 0 and int(x) < 100000]
        reviews = max(review_nums) if review_nums else 0

        # Rating — "4.9" before the review count
        rating_m = re.search(r"\b([45]\.\d)\b", block)
        rating = float(rating_m.group(1)) if rating_m else 0.0

        listings.append({
            "title":   title[:100],
            "price":   price,
            "reviews": reviews,
            "rating":  rating,
        })

        if len(listings) >= 12:
            break

    return listings


def etsy_search(keyword: str) -> dict:
    """Open a fresh Camoufox browser, search Etsy, parse results, close."""
    result = {
        "keyword":           keyword,
        "digital_count":     0,
        "avg_price":         0.0,
        "avg_reviews":       0.0,
        "max_reviews":       0,
        "top_listings":      [],
        "success":           False,
    }

    url = (f"https://www.etsy.com/search"
           f"?q={keyword.replace(' ', '+')}&listing_type=digital&explicit=1")

    with Camoufox(headless=True) as browser:
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(3.5)

            body_el = page.query_selector("body")
            body = body_el.inner_text() if body_el else ""

            # Retry once with longer wait if body is too thin
            if len(body) < 2000:
                time.sleep(3.0)
                body_el = page.query_selector("body")
                body = body_el.inner_text() if body_el else ""

            if len(body) < 500:
                print(f"    WARNING: body too short ({len(body)} chars) — possible bot block")
                return result

            # Count digital listings visible on page
            digital_count = body.count("Digital download")
            result["digital_count"] = digital_count

            # Parse top listings
            listings = parse_listings(body)
            result["top_listings"] = listings

            if listings:
                prices  = [l["price"]   for l in listings if l["price"]   > 0]
                reviews = [l["reviews"] for l in listings if l["reviews"] > 0]
                result["avg_price"]   = round(sum(prices)  / len(prices),  2) if prices  else 0.0
                result["avg_reviews"] = round(sum(reviews) / len(reviews), 1) if reviews else 0.0
                result["max_reviews"] = max(reviews) if reviews else 0

            result["success"] = True

        except Exception as e:
            print(f"    Etsy error for '{keyword}': {e}")
        finally:
            page.close()

    return result


# ─────────────────────────────────────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────────────────────────────────────

def score_niche(r: dict) -> float:
    """
    Opportunity score 0-100:
      Demand:      reviews on top listings (more = proven buyers exist)
      Competition: digital listing count on page 1 (fewer = easier to rank)
      Revenue:     avg price (higher = more $ per sale)
    """
    score = 40.0

    # Competition: fewer listings on page 1 = less crowded
    n = r.get("digital_count", 0)
    if   n == 0:   score += 0     # no results = possibly no market
    elif n <= 5:   score += 30    # tiny niche — potentially underserved
    elif n <= 15:  score += 20    # low competition
    elif n <= 25:  score += 10    # moderate
    else:          score -= 5     # saturated page 1

    # Demand: review counts prove real purchases happened
    max_rev = r.get("max_reviews", 0)
    if   max_rev > 500: score += 15   # strong demand signal
    elif max_rev > 100: score += 10
    elif max_rev > 20:  score += 5
    elif max_rev == 0:  score -= 10   # no reviews = unproven

    # Revenue potential
    avg_price = r.get("avg_price", 0)
    if   avg_price > 20: score += 15
    elif avg_price > 10: score += 8
    elif avg_price > 5:  score += 3

    return round(min(max(score, 0), 100), 1)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def run():
    print("=" * 65)
    print("ETSY NICHE RESEARCH — Reddit + Etsy Pipeline")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 65)

    # ── Phase 1: Reddit ──────────────────────────────────────────────────
    print("\n[PHASE 1] Reddit — new niche keywords")
    print("-" * 45)

    reddit_posts   = []
    reddit_niches  = []
    seen_urls: set = set()

    with Camoufox(headless=True) as browser:
        search_page = browser.new_page()
        for sub in REDDIT_SUBREDDITS:
            for query in REDDIT_QUERIES[:2]:
                print(f"  r/{sub}: '{query[:50]}'")
                posts = reddit_search(search_page, sub, query)
                for p in posts:
                    if p["url"] not in seen_urls:
                        seen_urls.add(p["url"])
                        reddit_posts.append(p)
                time.sleep(DELAY)
        search_page.close()

        print(f"\n  Reading {len(reddit_posts)} posts...")
        for i, post in enumerate(reddit_posts, 1):
            print(f"  [{i}/{len(reddit_posts)}] {post['title'][:60]}")
            rpage = browser.new_page()
            body  = scrape_post(rpage, post["url"])
            rpage.close()
            post["body"] = body
            niches = extract_niches(post["title"] + " " + body)
            post["extracted_niches"] = niches
            reddit_niches.extend(niches)
            time.sleep(1.0)

    # Merge seeds + Reddit discoveries, deduplicate
    all_kw = list(dict.fromkeys(
        SEED_NICHES + [n.strip() for n in reddit_niches if 5 < len(n.strip()) < 50]
    ))[:30]
    print(f"\n  Keywords to research: {len(all_kw)}")

    # ── Phase 2: Etsy (fresh browser per keyword) ────────────────────────
    print("\n[PHASE 2] Etsy validation — fresh browser per keyword")
    print("-" * 45)

    niche_results = []
    for i, kw in enumerate(all_kw, 1):
        print(f"\n[{i}/{len(all_kw)}] '{kw}'")
        data = etsy_search(kw)
        score = score_niche(data)
        data["opportunity"] = score
        data["keyword"] = kw
        niche_results.append(data)
        print(f"    digital={data['digital_count']}  "
              f"avg_price=${data['avg_price']}  "
              f"max_reviews={data['max_reviews']}  "
              f"score={score}")
        time.sleep(1.0)   # breath between browser launches

    niche_results.sort(key=lambda x: x["opportunity"], reverse=True)

    # ── Save JSON ────────────────────────────────────────────────────────
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({
            "generated":    datetime.now().isoformat(),
            "reddit_posts": reddit_posts,
            "niches":       niche_results,
        }, f, indent=2, ensure_ascii=False)

    # ── Save scorecard ───────────────────────────────────────────────────
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("ETSY NICHE OPPORTUNITY SCORECARD\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Keywords: {len(niche_results)}\n")
        f.write("=" * 75 + "\n\n")

        # Quick table
        f.write(f"{'#':<3} {'KEYWORD':<38} {'SCORE':<6} {'DL#':<5} {'AVG $':<7} {'MAX REV'}\n")
        f.write("-" * 75 + "\n")
        for i, n in enumerate(niche_results, 1):
            f.write(f"{i:<3} {n['keyword'][:37]:<38} {n['opportunity']:<6} "
                    f"{n['digital_count']:<5} ${n['avg_price']:<6} {n['max_reviews']}\n")

        # Detail for top 12
        f.write("\n\n" + "=" * 75 + "\n")
        f.write("TOP 12 NICHES — FULL DETAIL\n")
        f.write("=" * 75 + "\n\n")
        for n in niche_results[:12]:
            f.write(f"Keyword     : {n['keyword']}\n")
            f.write(f"Score       : {n['opportunity']}/100\n")
            f.write(f"Competition : {n['digital_count']} digital listings on page 1\n")
            f.write(f"Avg price   : ${n['avg_price']}\n")
            f.write(f"Max reviews : {n['max_reviews']}  (avg {n['avg_reviews']})\n")
            listings = n.get("top_listings", [])
            if listings:
                f.write("  Top listings:\n")
                for l in listings[:5]:
                    rev_str = f"{l['reviews']} reviews" if l["reviews"] else "no reviews"
                    f.write(f"    [{rev_str:>12}]  ${l['price']:.2f}  {l['title'][:55]}\n")
            f.write("\n")

    print(f"\n{'='*65}")
    print(f"Done. {len(niche_results)} niches scored.")
    print(f"  -> {OUT_JSON}")
    print(f"  -> {OUT_TXT}")
    print()
    print("TOP 10:")
    for n in niche_results[:10]:
        print(f"  {n['opportunity']:>5}/100  {n['keyword']:<38}"
              f"  DL:{n['digital_count']}  MaxRev:{n['max_reviews']}  ${n['avg_price']}")


if __name__ == "__main__":
    run()
