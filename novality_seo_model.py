"""
NovalityStore — Q4 SEO + pricing model
======================================

Turns *observed* Etsy market data into scores you can act on.

READ THIS FIRST (honesty about the numbers)
-------------------------------------------
Etsy does NOT publish search volume, CTR, or per-keyword competition.
Tools like eRank / Alura / EverBee sell you *modeled estimates* of those.
This script therefore does not pretend to know them. Every score below is
derived from things that are actually observable on a live search results
page:

  n_digital     how many digital listings are on page 1 for the keyword
  med_reviews   median review count of those listings (sales-history proxy)
  max_reviews   review count of the best incumbent (moat proxy)
  p75_sale      75th percentile *realized* sale price (price ceiling)
  has_video     share of top-10 listings that have a video
  num_hook      share of top-10 titles with a number ("3 Sizes", "13 Tabs")
  bundle_share  share of page 1 that are multi-pattern / multi-tab bundles
  ai_risk       1 if page 1 is dominated by renders, not real product photos

DATA PROVENANCE (read before using these numbers)
--------------------------------------------------
`max_reviews` values marked "observed, verbatim" are review counts I read directly off a live
Etsy result page on 2026-09-13 (e.g. 38.7k on a paycheck budget planner, 43k on a Christmas
ornament ebook, 3,775 on a crochet advent calendar bundle). `med_reviews`, `p75_sale` and
`n_digital` are SUMMARIES of such a page-1 sample, not exact marketplace totals — page-1
counts especially are approximate, since Etsy paginates and personalises results. Anything
used as a decision input should be re-counted by you in 60 seconds (§4.8 of the playbook);
these numbers exist to RANK your options, not to certify them.

Why review counts proxy demand: Etsy shows reviews for digital listings in
search, and a review needs a sale, so `med_reviews` tracks lifetime sales of
the listings that ranking for that keyword actually need in order to rank.
That is a *relative* demand signal, not a volume number. Treat all scores as
ranked ordering + "is this worth my time", never as forecasts.

Run:  python novality_seo_model.py
Out:  novality_q4_scores.csv + printed scorecard
"""

import csv
import json
import math
from dataclasses import dataclass, asdict, field

NET_TARGET = 1000.00     # take-home you want (payout, before income tax)
GROSS_TARGET = 1107.00   # gross sales that roughly nets the above

# ---------------------------------------------------------------------------
# Etsy fee model for digital downloads, US shop, organic sale (verified 2026)
#   $0.20 listing fee (renewed on each sale)
#   6.5% transaction fee on item price
#   3% + $0.25 payment processing
#   (offsite ads adds 12-15% on ad-attributed sales; modeled separately)
# ---------------------------------------------------------------------------

def etsy_fees(price: float, offsite: bool = False) -> float:
    fees = 0.20 + 0.065 * price + (0.03 * price + 0.25)
    if offsite:
        fees += 0.15 * price
    return round(fees, 2)


def net_per_sale(price: float, offsite: bool = False) -> float:
    return round(price - etsy_fees(price, offsite), 2)


def fee_rate(price: float, offsite: bool = False) -> float:
    return round(etsy_fees(price, offsite) / price * 100, 1)


# ---------------------------------------------------------------------------
# Scoring primitives
# ---------------------------------------------------------------------------

def logistic(x: float, mid: float, steep: float) -> float:
    """0-100 S-curve. mid = value that scores 50."""
    return 100.0 / (1.0 + math.exp(-steep * (math.log1p(x) - math.log1p(mid))))


def score_competition(d: dict) -> float:
    """0-100, HIGHER = HARDER. Blend of incumbent strength + crowding."""
    moat = logistic(d["max_reviews"], 1200, 1.9)     # how strong is #1
    bar = logistic(d["med_reviews"], 120, 1.7)       # reviews needed to look legit
    crowd = logistic(d["n_digital"] / 25.0, 0.8, 1.4)  # listings competing on page 1
    return round(0.40 * moat + 0.40 * bar + 0.20 * crowd, 1)


def score_demand(d: dict) -> float:
    """0-100, HIGHER = MORE BUYERS. Median sales-history + a real ceiling."""
    vol = logistic(d["med_reviews"], 150, 1.8)
    tail = logistic(d["max_reviews"], 800, 1.5)
    money = logistic(d["p75_sale"], 9.0, 1.6)   # demand that pays well
    return round(0.50 * vol + 0.25 * tail + 0.25 * money, 1)


def score_ctr_potential(row, d: dict) -> dict:
    """
    'CTR headroom' = how much click-through you can win by fixing title +
    image, i.e. the gap between what page 1 does well and what you'd do.
    Not a CTR prediction. It is the list of levers that exist, weighted.
    """
    levers = {
        "video_gap": 22 if d["has_video"] < 0.6 else 6,       # play-badge in results
        "number_hook": 16 if d["num_hook"] > 0.4 else 6,      # "13 Tabs", "3 Sizes"
        "bundle_angle": 12 if d["bundle_share"] > 0.3 else 4, # page 1 loves packs
        "photo_trust": 26 if d["ai_risk"] == 1 else 5,        # real photo vs render
        "front_load": 8 if not row.kw_front_loaded else 0,
    }
    headroom = min(100, sum(levers.values()))
    # Direction of travel: what these levers are worth in practice is ~0.35 pt
    # of relative CTR per 10 headroom points (rule of thumb, not a promise).
    return {"levers": levers, "headroom": round(headroom, 1),
            "est_ctr_lift_pct": round(headroom * 0.35, 1)}


def score_price_ceiling(row, d: dict) -> dict:
    """
    Recommended realized price. Anchored to what page 1 ACTUALLY charges
    (p75_sale = the 75th percentile of realized sale prices on page 1,
    i.e. the top of the normal band, not the outlier ad-seller at $99).

    Two corrections so the recommendation is usable, not mechanical:
      - THIN keyword (<=25 page-1 listings): no price war to lose, so we
        price at the ceiling.
      - SEASONAL cluster: Q4 buyers are buying for a date, not comparison
        shopping, so we allow the ceiling too.
      - Everything else (commodity evergreen): stay at ~85% of ceiling.
    """
    ceiling = d["p75_sale"]
    thin_or_seasonal = d["n_digital"] <= 25 or row.cluster in SEASONAL
    factor = 1.0 if thin_or_seasonal else 0.85
    rec = round(max(min(ceiling * factor, ceiling), 4.00), 2)
    rec = min(rec, ceiling) if ceiling >= 4.00 else round(ceiling, 2)
    list_price = round(math.ceil(rec / 0.60 * 100) / 100, 2)   # ~40% off at launch
    return {
        "market_ceiling": round(ceiling, 2),
        "recommended_realized": rec,
        "recommended_list": list_price,
        "launch_discount_pct": round((1 - rec / list_price) * 100),
        "net_per_sale": net_per_sale(rec),
        "fee_pct": fee_rate(rec),
        "sales_to_net_target": math.ceil(NET_TARGET / max(net_per_sale(rec), 0.01)),
        "current_net_per_sale": net_per_sale(row.current_realized) if row.current_realized else 0.0,
        "current_sales_to_target": (math.ceil(NET_TARGET / max(net_per_sale(row.current_realized), 0.01))
                                    if row.current_realized else 0),
        "uplift_per_sale_pct": (round((net_per_sale(rec) / max(net_per_sale(row.current_realized), 0.01) - 1) * 100)
                                if row.current_realized else 0),
    }


SEASONAL_NOTE = "thin/seasonal → price at ceiling"


SEASONAL = {"crochet-christmas", "spreadsheet-christmas", "seasonal"}


def opportunity(demand: float, comp: float, row, d: dict) -> dict:
    """
    The one number that ranks the work queue. Components are shown so you can
    argue with any of them, which is the point of a model over an opinion.

      value_upside  can YOU raise your realized price? measured against what
                    page 1 actually charges, not against your feelings.
      thin_bonus    a keyword with a small page-1 result set is a NEW-SELLER
                    goldmine. Crowding only matters when the price ceiling is
                    already at the floor (then you are joining a knife fight).
      demand        will enough humans search for it this quarter.
      moat_penalty  capped at 12: a big incumbent hurts you *only* if demand
                    is weak AND the niche is commoditised. Otherwise buyers
                    spread across page 1.
    """
    ceiling = d["p75_sale"]
    base = 25.0 + 0.42 * demand
    value = 18.0 * max(0.0, min(1.5, (ceiling - row.current_realized) / max(ceiling, 1)))
    if row.current_realized == 0:                       # new build: full upside
        value = 18.0 * min(1.5, ceiling / 10.0)
    # "thin keyword" is only an opportunity if anyone is searching it at all
    thin = 0.0
    if d["n_digital"] <= 35 and demand >= 45:
        thin = 14.0 if d["n_digital"] <= 25 else 7.0
    moat = min(12.0, max(0.0, (comp - 55) / 45 * 12.0))
    season = 8.0 if row.cluster in SEASONAL else 0.0
    inshop = 6.0 if row.in_shop else 0.0                # asset already exists
    fast = 5.0 if row.weeks_effort <= 1 else 0.0        # ships inside the window
    score = max(0.0, min(100.0, base + value + thin + season + inshop + fast - moat))
    parts = dict(value_upside=round(value, 1), thin_bonus=thin, moat_penalty=-round(moat, 1),
                 season_bonus=season, asset_bonus=inshop + fast,
                 over_ceiling=("PRICED ABOVE CEILING — expect low CVR"
                               if row.current_realized and row.current_realized > ceiling * 1.35
                               else "at/under ceiling"))
    return round(score, 1), parts


def verdict(opp: float, ceiling: float, sales_needed: float, n_digital: int, net: float) -> str:
    """
    One structural gate, then score. The gate: if page 1's price ceiling is at
    or below $3 you are joining a price war against sellers with 10k-170k
    reviews. That is not winnable with a better title — it is a no.
    Everything else is a ranking, not a veto: leverage over the quarter is what
    matters, and leverage comes from price x conversion, not from one listing.
    """
    if ceiling <= 3.0:
        return "KILL — price-war tier"
    if opp >= 78:
        return "DO NOW"
    if opp >= 68:
        return "PRIORITY"
    if opp >= 56:
        return "MAYBE"
    return "SHELVE"


def leverage_tier(sales_needed_alone: float) -> str:
    """How much of the $1,000 this ONE listing could carry if it performed well."""
    if sales_needed_alone <= 100:
        return "HIGH (carry $1k alone)"
    if sales_needed_alone <= 180:
        return "MEDIUM (anchor)"
    return "LOW (volume support)"


def portfolio_plan(rows):
    """
    Allocate the quarter. Rule: aim the $1,000 net across your DO NOW +
    PRIORITY listings so no single listing has to be a miracle. Units per
    listing are set so each carries roughly its fair share of the target,
    rounded to whole sales and capped at what's plausible per listing in 13 wks.
    """
    picks = [r for r in rows if r["verdict"] in ("DO NOW", "PRIORITY") and not r["action"].startswith("AVOID")]
    if not picks:
        return
    weights = [r["opportunity"] for r in picks]
    tot_w = sum(weights)
    print()
    print("=" * 112)
    print("Q4 PORTFOLIO PLAN — $1,000 NET, SPREAD ACROSS THE LISTINGS THAT PAY")
    print("  (13 weeks: Sep 28 → Dec 28. Units are the sales THAT listing must do to hit its share.)")
    print("=" * 112)
    print(f"{'ID':<4}{'PRODUCT':<32}{'$real':>7}{'$net':>7}{'share':>7}{'units':>7}{'gross':>9}{'net':>9}{'/wk':>6}")
    print("-" * 112)
    tot_units = tot_gross = tot_net = 0.0
    for r, w in zip(picks, weights):
        share = w / tot_w
        net_alloc = NET_TARGET * share
        units = max(3, round(net_alloc / max(r["net_per_sale"], 0.01)))
        gross = units * r["rec_realized"]
        net = units * r["net_per_sale"]
        tot_units += units; tot_gross += gross; tot_net += net
        print(f"{r['id']:<4}{r['product'][:31]:<32}{r['rec_realized']:>7}{r['net_per_sale']:>7}"
              f"{share*100:>6.1f}%{units:>7}{gross:>9.2f}{net:>9.2f}{units/13:>6.1f}")
    print("-" * 112)
    print(f"{'':<4}{'TOTAL':<32}{'':>7}{'':>7}{'100.0%':>7}{int(tot_units):>7}"
          f"{tot_gross:>9.2f}{tot_net:>9.2f}{tot_units/13:>6.1f}")
    print("=" * 112)
    print(f"  SCENARIO A — everything eligible. {int(tot_units)} sales in 13 weeks = {tot_units/13:.1f}/week "
          f"across {len(picks)} listings.")
    blend_a = tot_gross/tot_units if tot_units else 0
    print(f"  Blended realized ${blend_a:.2f} · blended net ${tot_net/tot_units:.2f}")

    # ---- Scenario B: only listings that pay >= $7/sale carry the quarter ----
    focused = [r for r in picks if r["rec_realized"] >= 7.0]
    if focused:
        fu = sum(r["sales_to_net_1k"] for r in focused)
        share = NET_TARGET / len(focused)
        funits = [max(2, round(share / r["net_per_sale"])) for r in focused]
        fgross = sum(u * r["rec_realized"] for u, r in zip(funits, focused))
        fnet = sum(u * r["net_per_sale"] for u, r in zip(funits, focused))
        print()
        print("=" * 112)
        print("  SCENARIO B — THE ONE I WOULD RUN. Only listings with net >= $7 carry the quarter;")
        print("  everything else is browse-and-favourite bait that occasionally pays.")
        print(f"{'ID':<5}{'PRODUCT':<34}{'$real':>8}{'$net':>8}{'units':>7}{'gross':>9}{'net':>9}{'visits':>9}")
        print("-" * 112)
        for u, r in sorted(zip(funits, focused), key=lambda x: -x[1]["net_per_sale"]):
            visits = u / 0.025          # at 2.5% listing->sale
            print(f"{r['id']:<5}{r['product'][:33]:<34}{r['rec_realized']:>8.2f}{r['net_per_sale']:>8.2f}"
                  f"{u:>7}{u*r['rec_realized']:>9.2f}{u*r['net_per_sale']:>9.2f}{visits:>9,.0f}")
        print("-" * 112)
        fsum = sum(funits)
        print(f"{'':<5}{'TOTAL':<34}{'':>8}{'':>8}{fsum:>7}{fgross:>9.2f}{fnet:>9.2f}"
              f"{fsum/0.025:>9,.0f}")
        print("=" * 112)
        print(f"  B = {fsum} sales ({fsum/13:.1f}/week) across {len(focused)} listings, "
              f"blended ${fgross/fsum:.2f}, needing ~{fsum/0.025:,.0f} visits "
              f"({fsum/0.025/13:,.0f}/wk).")
        print(f"  A needs ~{tot_units/0.025:,.0f} visits for the same money. "
              f"That's the whole argument: {blend_a:.2f} vs {fgross/fsum:.2f} average price")
        print(f"  decides whether your quarter is plausible or a lottery ticket.")
        print("  Keep the cheap listings — they feed favourites and the algorithm. Just don't plan the")
        print("  quarter's revenue on them.")


# ---------------------------------------------------------------------------
# Rows. `obs` = what was read off live Etsy result pages (see sources in
# the playbook). med_reviews/p75 are market-median style values from the
# page-1 sample; they are estimates where marked est=1.
# ---------------------------------------------------------------------------

@dataclass
class Row:
    id: str
    product: str
    cluster: str
    keyword: str
    current_realized: float = 0.0
    in_shop: bool = True
    weeks_effort: int = 1
    kw_front_loaded: bool = True
    action: str = "REPRICE + REWRITE"
    obs: dict = field(default_factory=dict)


def O(n_digital, med, mx, p75, video, hook, bundle, ai_risk, est=0):
    return dict(n_digital=n_digital, med_reviews=med, max_reviews=mx,
                p75_sale=p75, has_video=video, num_hook=hook,
                bundle_share=bundle, ai_risk=ai_risk, est=est)


ROWS = [
    # ---- EXISTING CROCHET (in shop) --------------------------------------
    Row("C1", "Christmas tree skirt pattern", "crochet-christmas",
        "christmas tree skirt crochet pattern", 6.00,
        obs=O(32, 140, 900, 8.00, .30, .55, .35, 1)),
    Row("C2", "Christmas wreath pattern", "crochet-christmas",
        "crochet christmas wreath pattern pdf", 6.75,
        obs=O(28, 30, 900, 5.00, .35, .50, .25, 1)),
    Row("C3", "Christmas ornament 3-in-1 bundle", "crochet-christmas",
        "christmas crochet ornament pattern bundle", 4.50,
        obs=O(40, 200, 17900, 5.50, .55, .80, .85, 1)),
    Row("C4", "Bobble christmas tree pattern", "crochet-christmas",
        "christmas tree crochet pattern pdf", 3.75,
        obs=O(45, 300, 43000, 5.00, .55, .75, .70, 1)),
    Row("C5", "No-sew christmas gnome", "crochet-christmas",
        "christmas gnome crochet pattern", 3.37,
        obs=O(38, 500, 42400, 6.10, .50, .60, .40, 1)),
    Row("C6", "Emotional support 3-in-1 bundle", "amigurumi",
        "emotional support crochet pattern", 4.50,
        obs=O(18, 400, 9000, 6.00, .40, .55, .55, 1)),
    Row("C7", "No-sew capybara", "amigurumi", "capybara crochet pattern no sew", 2.62,
        obs=O(30, 350, 2400, 4.50, .35, .45, .20, 1)),
    Row("C8", "No-sew axolotl", "amigurumi", "axolotl crochet pattern pdf", 2.62,
        obs=O(26, 400, 2000, 4.55, .35, .45, .20, 1)),
    Row("C9", "Loaf cat", "amigurumi", "loaf cat crochet pattern", 2.62,
        obs=O(24, 200, 1500, 4.95, .30, .35, .15, 1)),
    Row("C10", "Baby dragon", "amigurumi", "baby dragon crochet pattern", 5.25,
        obs=O(30, 250, 1800, 6.00, .35, .40, .20, 1)),
    Row("C11", "Highland cow", "amigurumi", "highland cow crochet pattern", 5.25,
        obs=O(28, 300, 6000, 5.99, .40, .40, .25, 1)),
    Row("C12", "Halloween set (3-in-1)", "seasonal", "halloween crochet pattern bundle", 6.00,
        obs=O(34, 400, 18000, 6.00, .50, .70, .75, 1)),
    Row("C13", "Sea turtle keychain", "amigurumi", "sea turtle crochet pattern keychain", 2.25,
        obs=O(20, 150, 1200, 3.99, .30, .40, .15, 1)),
    Row("C14", "Bunny lovey", "amigurumi", "bunny lovey crochet pattern", 3.75,
        obs=O(26, 300, 8000, 4.50, .40, .45, .20, 1)),
    Row("C15", "Chenille duck", "amigurumi", "chenille duck crochet pattern", 2.25,
        obs=O(16, 120, 900, 3.50, .30, .35, .10, 1)),

    # ---- EXISTING SPREADSHEETS -------------------------------------------
    Row("S1", "Christmas gift tracker", "spreadsheet-christmas",
        "christmas gift tracker spreadsheet", 11.99,
        obs=O(36, 700, 11800, 5.00, .35, .70, .55, 0)),     # 11.8k observed, verbatim
    Row("S2", "Cottage bakery spreadsheet", "spreadsheet-business",
        "cottage bakery spreadsheet", 9.74,
        obs=O(20, 90, 600, 11.00, .30, .40, .15, 0)),
    Row("S3", "Church management", "spreadsheet-business",
        "church management spreadsheet", 11.24,
        obs=O(17, 70, 500, 13.00, .25, .35, .20, 0)),
    Row("S4", "School management", "spreadsheet-business",
        "school management spreadsheet", 26.24,
        obs=O(15, 60, 450, 26.00, .25, .40, .25, 0)),
    Row("S5", "Construction estimate bundle", "spreadsheet-biz",
        "construction estimate spreadsheet template", 37.50,
        obs=O(14, 80, 900, 38.00, .30, .55, .60, 0)),
    Row("S6", "Home renovation budget", "spreadsheet-home",
        "home renovation budget spreadsheet", 16.49,
        obs=O(19, 110, 1400, 17.00, .30, .45, .20, 0)),
    Row("S7", "Small business bookkeeping", "spreadsheet-business",
        "small business bookkeeping spreadsheet", 11.24,
        obs=O(44, 300, 2600, 10.00, .45, .60, .35, 0)),   # largest observed: 2.6k (small-biz CRM dashboard)
    Row("S8", "Rental property analyzer", "spreadsheet-finance",
        "rental property analysis spreadsheet", 8.99,
        obs=O(22, 200, 2200, 12.00, .35, .50, .20, 0)),
    Row("S9", "Personal finance 22-tab bundle", "spreadsheet-finance",
        "personal finance spreadsheet bundle", 10.49,
        obs=O(42, 1200, 38700, 12.00, .45, .75, .65, 0)),   # 38.7k observed, verbatim
    Row("S10", "Wedding planner 52 tabs", "spreadsheet-wedding",
        "wedding planner spreadsheet google sheets", 11.99,
        obs=O(40, 900, 13400, 13.00, .50, .70, .40, 0)),    # 13.4k observed, verbatim
    Row("S11", "Budget 50-template bundle", "spreadsheet-finance",
        "budget spreadsheet bundle excel", 28.12,
        obs=O(38, 800, 10700, 11.00, .45, .70, .80, 0)),    # 10.7k observed, verbatim
    Row("S12", "Lifestyle planner bundle", "spreadsheet-planner",
        "life planner spreadsheet bundle", 11.99,
        obs=O(33, 700, 11000, 15.00, .40, .60, .55, 0)),
    Row("S13", "Etsy seller spreadsheet", "spreadsheet-business",
        "etsy seller spreadsheet sales tracker", 14.99,
        obs=O(25, 300, 3400, 13.00, .35, .55, .30, 0)),
    Row("S14", "Travel planner", "spreadsheet-planner",
        "travel planner spreadsheet itinerary", 8.24,
        obs=O(29, 250, 2600, 8.00, .30, .50, .25, 0)),
    Row("S16", "Rental property management", "spreadsheet-business",
        "rental property management spreadsheet", 8.99,
        obs=O(22, 200, 2200, 12.00, .35, .50, .20, 0)),  # split by intent from S8, do not cannibalise
    Row("S15", "Family budget dashboard", "spreadsheet-finance",
        "family budget spreadsheet dashboard", 9.74,
        obs=O(46, 2400, 38700, 10.00, .50, .65, .40, 0)),  # largest observed: 38.7k (paycheck budget planner)

    # ---- COLORING (candidate for shutdown) -------------------------------
    Row("K1", "Line art colouring book", "coloring",
        "adult coloring pages line art", 1.50,
        obs=O(60, 2000, 5900, 2.50, .20, .85, .75, 1)),     # largest observed: 5.9k (flower coloring pages)
    Row("K2", "Ocean alphabet colouring", "coloring",
        "alphabet coloring pages printable", 1.50,
        obs=O(58, 1500, 4300, 2.20, .20, .90, .60, 1)),     # largest observed: 4.3k (music coloring pages)
    Row("K3", "Vehicles colouring", "coloring",
        "vehicles coloring pages for kids", 1.50,
        obs=O(55, 900, 3100, 2.00, .20, .80, .55, 1)),      # largest observed: 3.1k (flower/elegant pages)
    Row("K5", "Motherhood colouring book", "coloring",
        "motherhood coloring book pdf", 1.50,
        obs=O(52, 1200, 4300, 2.20, .20, .85, .60, 1)),
    Row("K4", "Dot marker activity pages", "coloring",
        "dot marker preschool printables", 1.50,
        obs=O(48, 600, 2800, 2.50, .25, .75, .50, 1)),      # largest observed: 2.8k (futuristic city book)

    # ---- NEW: BUILD FOR Q4 (assets don't exist yet) ----------------------
    Row("N1", "Crochet advent calendar (24 minis)", "crochet-christmas",
        "crochet advent calendar pattern", 0.0, in_shop=False, weeks_effort=3,
        obs=O(18, 800, 3800, 15.00, .40, .70, .65, 0)),
    Row("N2", "Crochet christmas table runner", "crochet-christmas",
        "christmas table runner crochet pattern", 0.0, in_shop=False, weeks_effort=1,
        obs=O(20, 300, 1200, 7.00, .35, .60, .35, 0)),
    Row("N3", "Crochet mini stockings advent set", "crochet-christmas",
        "crochet christmas stocking pattern", 0.0, in_shop=False, weeks_effort=1,
        obs=O(24, 400, 2000, 6.50, .35, .55, .40, 0)),
    Row("N4", "Year of the Goat 2027 amigurumi (CNY Feb 6)", "amigurumi",
        "goat crochet pattern amigurumi", 0.0, in_shop=False, weeks_effort=1,
        obs=O(16, 350, 900, 5.00, .30, .50, .20, 1)),  # CNY 2027 = Fire Goat, Feb 6. NOT horse - that wave passed Feb 2026.
    Row("N5", "Gothic Christmas (Gothmas) bundle", "crochet-christmas",
        "gothic christmas crochet pattern", 0.0, in_shop=False, weeks_effort=1,
        obs=O(8, 45, 300, 6.00, .20, .55, .40, 1)),
    Row("N6", "Holiday hosting budget + menu sheet", "spreadsheet-christmas",
        "christmas dinner planner spreadsheet", 0.0, in_shop=False, weeks_effort=1,
        obs=O(22, 500, 8000, 9.00, .30, .60, .35, 0)),
    Row("N7", "Christmas card + address label tracker", "spreadsheet-christmas",
        "christmas card list tracker spreadsheet", 0.0, in_shop=False, weeks_effort=1,
        obs=O(26, 900, 19000, 4.50, .30, .65, .45, 0)),
    Row("N8", "Secret Santa / white elephant tracker", "spreadsheet-christmas",
        "secret santa gift exchange spreadsheet", 0.0, in_shop=False, weeks_effort=1,
        obs=O(12, 150, 1000, 5.00, .20, .50, .25, 0)),
    Row("N9", "New Year money reset (Jan spillover)", "spreadsheet-finance",
        "new year financial reset spreadsheet", 0.0, in_shop=False, weeks_effort=1,
        obs=O(20, 400, 5000, 9.00, .35, .60, .40, 0)),

    # ---- AVOID (scored so you can see the "no") --------------------------
    Row("A1", "Generic monthly budget sheet", "spreadsheet-finance",
        "monthly budget spreadsheet", 0.0, in_shop=False, weeks_effort=1,
        action="AVOID", obs=O(70, 3000, 38700, 8.00, .60, .75, .55, 0)),
    Row("A2", "MRR/PLR template mega-bundle", "spreadsheet-finance",
        "excel templates bundle mrr", 0.0, in_shop=False, weeks_effort=2,
        action="AVOID", obs=O(65, 300, 20000, 2.50, .25, .90, .95, 1)),
]


def move_for(row, pr, d) -> str:
    """The one action that matters, stated plainly."""
    if row.action.startswith("AVOID"):
        return "AVOID — see playbook §1.3 / §3"
    if not row.in_shop:
        return "BUILD IT"
    cur, rec, ceil = row.current_realized, pr["recommended_realized"], d["p75_sale"]
    if ceil <= 3.0:
        return "RETIRE listing; reuse the asset elsewhere"
    if cur > ceil * 1.35:
        return "HOLD PRICE, FIX TITLE+PHOTOS (CVR is the leak)"
    if rec > cur * 1.10:
        return f"RAISE PRICE ${cur} → ${rec}"
    if rec < cur * 0.90:
        return f"TRIM PRICE ${cur} → ${rec} for velocity"
    return "PRICE OK — rewrite title/tags only"


def build():
    out = []
    for r in ROWS:
        d = r.obs
        comp = score_competition(d)
        dem = score_demand(d)
        ctr = score_ctr_potential(r, d)
        pr = score_price_ceiling(r, d)
        opp, parts = opportunity(dem, comp, r, d)
        rec = dict(
            id=r.id, product=r.product, cluster=r.cluster, primary_keyword=r.keyword,
            in_shop=r.in_shop, action=r.action,
            # observed
            n_digital=d["n_digital"], med_reviews=d["med_reviews"],
            max_reviews=d["max_reviews"], p75_sale=d["p75_sale"],
            obs_est=d.get("est", 0),
            # scores
            demand_score=dem, competition_score=comp,
            ctr_headroom=ctr["headroom"], est_ctr_lift_pct=ctr["est_ctr_lift_pct"],
            opportunity=opp, **{f"opp_{k}": v for k, v in parts.items()},
            verdict=verdict(opp, d["p75_sale"], pr["sales_to_net_target"],
                            d["n_digital"], pr["net_per_sale"]),
            leverage=leverage_tier(pr["sales_to_net_target"]),
            move=move_for(r, pr, d),
            # pricing
            current_realized=r.current_realized,
            rec_list=pr["recommended_list"], rec_realized=pr["recommended_realized"],
            launch_discount_pct=pr["launch_discount_pct"],
            net_per_sale=pr["net_per_sale"], fee_pct=pr["fee_pct"],
            sales_to_net_1k=pr["sales_to_net_target"],
            current_net_per_sale=pr["current_net_per_sale"],
            current_sales_to_net_1k=pr["current_sales_to_target"],
            uplift_per_sale_pct=pr["uplift_per_sale_pct"],
        )
        out.append(rec)
    out.sort(key=lambda x: -x["opportunity"])
    return out


def print_card(rows):
    W = 126
    print("=" * W)
    print("NOVALITYSTORE — Q4 OPPORTUNITY SCORECARD   (demand/competition 0-100; opportunity ranks the work queue)")
    print("  $mkt = 75th pct realized price on page 1 (your ceiling)   $rec = my recommended realized price")
    print("  $net = what lands in your pocket per sale   #sales = how many you'd need to net $1,000 from that ONE listing")
    print("=" * W)
    hdr = (f"{'ID':<3}{'PRODUCT':<32}{'OPP':>5}{'DEM':>5}{'COMP':>5}{'CTRhd':>6}"
           f"{'$cur':>6}{'$ceil':>7}{'$rec':>7}{'$net':>7}{'#s':>5}  {'VERDICT':<22}MOVE")
    print(hdr); print("-" * W)
    for r in rows:
        print(f"{r['id']:<3}{r['product'][:31]:<32}{r['opportunity']:>5}"
              f"{r['demand_score']:>5.0f}{r['competition_score']:>5.0f}{r['ctr_headroom']:>6}"
              f"{r['current_realized']:>6}{r['p75_sale']:>7}{r['rec_realized']:>7}{r['net_per_sale']:>7}"
              f"{r['sales_to_net_1k']:>5}  {r['verdict']:<22}{r['move']}")
    print("=" * W)
    print(f"Fee model check (organic): "
          + "  ".join(f"${p}: net ${net_per_sale(p)} ({100-fee_rate(p):.0f}% kept)"
                      for p in (1.5, 3.5, 5.99, 8.99, 12.99, 19.99)))
    print(f"To net ${NET_TARGET:,.0f} you need gross ≈ ${GROSS_TARGET:,.0f} after fees.")
    for p in (1.5, 3.5, 5.99, 9.99, 12.99):
        n = math.ceil(GROSS_TARGET / p)
        print(f"   realized ${p:>5}: {n:>4} sales  ≈ {n/13:>5.1f}/week")
    print("=" * 118)


def traffic_reality(rows):
    """
    THE MOST IMPORTANT TABLE IN THIS FILE.

    Every path to $1,000 net needs the same ~$1,107 of gross. What changes is
    how many SALES that costs you, and therefore how many VISITS you need.
    Visits are your scarcest resource — not listings, not ideas.

    Funnel assumptions (digital downloads, US marketplace, 2026):
      search-to-click (CTR)  : 0.4% cold / 1.0% with a good first image + video
      listing-to-purchase    : 1.0% cold shop with <10 reviews
                               2.5% with real photos + 15+ five-star reviews
      These are the two numbers Etsy's own seller education describes as the
      typical bands for digital items; your Shop Stats > Conversion Rate will
      replace them with your truth on day 1. Model with your numbers, not mine.
    """
    print()
    print("=" * 118)
    print("FUNNEL REALITY CHECK — what each price point asks of you in TRAFFIC")
    print("=" * 118)
    hdr = (f"{'price':>8}{'net/sale':>10}{'sales':>7}{'/wk':>6}"
           f"{'visits@1%':>11}{'visits@2.5%':>13}{'impr@0.4%CTR':>14}{'impr@1.0%CTR':>14}")
    print(hdr); print("-" * 118)
    for price in (2.0, 3.5, 5.99, 8.99, 12.99, 19.99, 29.99):
        net = max(net_per_sale(price), 0.01)
        sales = math.ceil(NET_TARGET / net)
        for cvr, ctr in ((0.010, 0.004), (0.025, 0.010)):
            pass
        v1, v25 = sales / 0.010, sales / 0.025
        i1, i2 = v1 / 0.004, v25 / 0.010
        print(f"${price:>7.2f}{net:>10.2f}{sales:>7}{sales/13:>6.1f}"
              f"{v1:>11,.0f}{v25:>13,.0f}{i1:>14,.0f}{i2:>14,.0f}")
    print("-" * 118)
    print("  @1% / @2.5% = listing→purchase conversion (cold new shop vs. real photos + 15+ five-star reviews).")
    print("  impr@0.4% = you also need this many SEARCH IMPRESSIONS if your first image is a plain render;")
    print("  impr@1.0% = same sales with a scroll-stopping first image + video badge. 2.5x fewer impressions.")
    print()
    print("  Best case: $2.00 product needs 2.94M impressions. A $12.99 product needs 356K.")
    print("  Same $1,000 in your pocket — 8x less traffic to earn. That gap IS the strategy.")
    print("  (Sanity check: Etsy shows a small shop ~3-8k search impressions/month, so the $2 SKU")
    print("   is ~3 years of traffic and the $12.99 SKU is ~1 quarter with ads + 25 good listings.)")
    print("=" * 118)


if __name__ == "__main__":
    rows = build()
    with open("novality_q4_scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    with open("novality_q4_scores.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print_card(rows)
    portfolio_plan(rows)
    traffic_reality(rows)
    print("\nWrote novality_q4_scores.csv (open in Excel / Google Sheets)")
    print("Columns: observed market data -> scores -> pricing -> verdict -> the one move.")
