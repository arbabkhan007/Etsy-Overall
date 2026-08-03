"""
generate_listing.py — Use Claude AI to write an optimized Etsy listing.

Reads market context from etsy_research.json (if available) so the listing
copy is informed by real competitor prices and review counts.

Usage:
  python generate_listing.py --keyword "autism routine chart printable"
  python generate_listing.py --keyword "trail running plan" --data etsy_research.json
  python generate_listing.py --keyword "perimenopause tracker" --output tracker_listing.json

Output: listing.json (or --output path) — ready for create_listing.py --spec
"""

import argparse
import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are an expert Etsy SEO specialist and copywriter for digital printable products. You write listings that rank in Etsy search and convert browsers into buyers.

TITLE (max 140 chars):
- Put the exact keyword in the first 40 characters — Etsy weights the title start most heavily
- Add 2-3 natural variations after a | or comma
- Be specific: "8-Week Trail Running Plan | Beginner Printable PDF" beats "Running Plan Printable"
- Never keyword-stuff with commas; write like a human would read it

DESCRIPTION (400-600 words):
- First 160 chars are the search preview — open with the strongest hook
- Repeat the primary keyword naturally 3-5 times throughout
- Always include: "instant download", "printable PDF", "digital download"
- Structure:
    1. Hook (what it is + who it's for)
    2. Bullet list: exactly what's included (buyers scan, not read)
    3. How to use it
    4. Keyword-rich closing paragraph for SEO
- Speak directly to the buyer's pain point

TAGS (exactly 13, max 20 chars each):
- Multi-word phrases outperform single words ("trail running plan" > "running")
- Distribution: 3 exact-match, 5 long-tail variations, 3 broad category, 2 buyer persona
- Zero repeated words across all 13 tags — each tag should unlock different searches
- Count characters carefully: "printable planner" = 17 chars ✓, "neurodivergent planner" = 22 chars ✗

PRICE:
- Base on avg market price; go slightly above if the listing is clearly premium
- Round to .99 or .00

Output ONLY valid JSON with these exact keys:
{
  "title": "...",
  "description": "...",
  "tags": ["...", ...],  // exactly 13 items
  "price_suggestion": 0.00
}
No markdown, no explanation, no code fences."""


def find_market_data(keyword: str, data_path: Path) -> dict | None:
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        kw_lower = keyword.lower()
        for niche in data.get("niches", []):
            if niche.get("keyword", "").lower() == kw_lower:
                return niche
        # Fuzzy match: keyword is contained in niche key or vice versa
        for niche in data.get("niches", []):
            nk = niche.get("keyword", "").lower()
            if kw_lower in nk or nk in kw_lower:
                return niche
    except Exception:
        pass
    return None


def build_prompt(keyword: str, market_data: dict | None) -> str:
    lines = [f"Write an Etsy listing for this niche: {keyword}"]

    if market_data:
        lines.append(f"\nMarket data (from live Etsy scrape):")
        lines.append(f"  Opportunity score : {market_data.get('opportunity', '?')}/100")
        lines.append(f"  Avg price         : ${market_data.get('avg_price', 0):.2f}")
        lines.append(f"  Max reviews pg 1  : {market_data.get('max_reviews', 0)}")
        lines.append(f"  Competitors on pg1: {market_data.get('digital_count', 0)} digital listings")
        top = market_data.get("top_listings", [])
        if top:
            lines.append(f"\nTop competing listings (use these to differentiate, not copy):")
            for l in top[:4]:
                lines.append(f'  "${l["price"]:.2f}" | {l["reviews"]} reviews | "{l["title"]}"')

    lines.append("\nOutput JSON only.")
    return "\n".join(lines)


def generate(keyword: str, market_data: dict | None) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": build_prompt(keyword, market_data)}],
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def validate(listing: dict) -> list[str]:
    warnings = []
    title = listing.get("title", "")
    tags  = listing.get("tags", [])

    if len(title) > 140:
        warnings.append(f"Title is {len(title)} chars (max 140) — trim it")
    if len(tags) != 13:
        warnings.append(f"Got {len(tags)} tags (need exactly 13)")
    for tag in tags:
        if len(tag) > 20:
            warnings.append(f"Tag too long ({len(tag)} chars): \"{tag}\"")
    return warnings


def main():
    parser = argparse.ArgumentParser(description="Generate an Etsy listing with Claude AI")
    parser.add_argument("--keyword", required=True, help="Niche keyword to write a listing for")
    parser.add_argument("--data",    default="etsy_research.json", help="Path to etsy_research.json (default: etsy_research.json)")
    parser.add_argument("--output",  default="listing.json",       help="Output file (default: listing.json)")
    args = parser.parse_args()

    data_path   = Path(args.data)
    market_data = find_market_data(args.keyword, data_path) if data_path.exists() else None

    if market_data:
        print(f"  Market data found: {market_data.get('opportunity')}/100 score, "
              f"${market_data.get('avg_price')} avg, {market_data.get('max_reviews')} max reviews")
    else:
        print(f"  No market data — generating without context (run etsy_research.py first for better results)")

    print(f"\nGenerating listing for: {args.keyword}")
    listing = generate(args.keyword, market_data)

    warnings = validate(listing)
    for w in warnings:
        print(f"  ⚠ {w}")

    out = Path(args.output)
    out.write_text(json.dumps(listing, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n✓ Saved → {out}")
    print(f"\n  Title : {listing.get('title', '')}")
    print(f"  Price : ${listing.get('price_suggestion', 0)}")
    print(f"  Tags  : {', '.join(listing.get('tags', []))}")
    print(f"\nNext:")
    print(f"  python create_listing.py --spec {out} --file product.pdf --image cover.jpg --draft")


if __name__ == "__main__":
    main()
