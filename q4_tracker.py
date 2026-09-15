"""
NovalityStore — Q4 weekly tracker
=================================

Generates q4_weekly_tracker.csv from the SAME model that scored your listings,
so the plan and the weekly numbers can never drift apart. If you change a
price in novality_seo_model.py, re-run this and your targets move.

Run:  python q4_tracker.py
Out:  q4_weekly_tracker.csv  (open in Google Sheets; the YOUR_* columns are blank for you to fill)
"""

import csv
import datetime as dt

from novality_seo_model import build, net_per_sale

QUARTER_START = dt.date(2026, 9, 28)   # Monday of the first full week of Q4 prep
WEEKS = 13
NET_GOAL = 1000.00
PRICE_FLOOR = 7.00                      # only listings paying >= this carry the quarter
MIN_CVR, MAX_CVR = 0.010, 0.025         # listing -> sale, cold shop vs. warmed by reviews
CTR_EARLY, CTR_LATE = 0.006, 0.010      # search -> click, render photos -> real photos + video

# Ramp: October builds, November is Black Friday, early December is the peak,
# then Christmas-crochet dies on Dec 12 and only instant-download planning tools live.
WEIGHTS = [.04, .05, .06, .07, .08, .09, .10, .11, .12, .11, .08, .05, .04]

JOBS = {
 1: "Reprice every listing · archive 6 coloring listings · reply publicly to the 1-star · kill the permanent 25% sale",
 2: "Publish N1 advent calendar · paste 4 rewritten titles/tags · add real-photo disclaimer to renders",
 3: "Recruit 2-3 pattern testers · ship N6 dinner planner · first 2 real sample photo sets",
 4: "Rewrite top-5 spreadsheet descriptions · Halloween refresh (edit, do not renew) · merge duplicate listings · start the review request on every order",
 5: "Turn on Etsy Ads $3/day, top 5 only · publish N2 table runner + N3 stockings",
 6: "Video on your top 8 listings · 2 more new listings · fill all 10 photo slots everywhere",
 7: "BLACK FRIDAY sale ON: business sheets only, 40% off, ends Dec 1 · email your buyer list",
 8: "Harvest BF · add 2 gift bundles (raise AOV) · check every listing's CTR in Stats",
 9: "PEAK WEEK: ads on daily, replies under 2h, push N1/C1/C5 · $300 cumulative = Star Seller unlocked",
10: "Dec 12 cut-off: switch ads from make-it patterns to instant-download planners",
11: "Last-minute angle in titles: 'done in a weekend' · coupon 15% to abandoned carts",
12: "Publish N9 New Year reset Dec 26 · end sale Dec 28 · no re-listings during the holidays",
13: "Pull every stat into one sheet · write January's kill/rewrite list · thank your reviewers",
}


def focused_listings():
    """Scenario B from the model: only high-net listings carry the revenue."""
    rows = [r for r in build() if r["verdict"] in ("DO NOW", "PRIORITY")]
    keep = [r for r in rows if r["rec_realized"] >= PRICE_FLOOR]
    return sorted(keep, key=lambda r: -r["net_per_sale"])


def allocate(total, weights):
    """Largest-remainder rounding so the weekly units add up to exactly `total`."""
    raw = [total * w for w in weights]
    base = [max(1, int(x)) for x in raw]
    left = total - sum(base)
    order = sorted(range(len(raw)), key=lambda i: -(raw[i] - int(raw[i])))
    i = 0
    while left > 0:
        base[order[i % len(order)]] += 1; left -= 1; i += 1
    while left < 0:
        j = order[-(i + 1) % len(order)]
        if base[j] > 1:
            base[j] -= 1; left += 1
        i += 1
    return base


def main():
    keep = focused_listings()
    if not keep:
        raise SystemExit("No listings clear the floor — lower PRICE_FLOOR or reprice in the model.")
    per = NET_GOAL / len(keep)
    units_by_listing = [max(2, round(per / r["net_per_sale"])) for r in keep]
    total_units = sum(units_by_listing)
    blended_net = sum(u * r["net_per_sale"] for u, r in zip(units_by_listing, keep)) / total_units
    blended_price = sum(u * r["rec_realized"] for u, r in zip(units_by_listing, keep)) / total_units
    units = allocate(total_units, WEIGHTS)

    print(f"PLAN — {len(keep)} listings carry ${NET_GOAL:,.0f} net")
    print(f"{'ID':<5}{'LISTING':<36}{'price':>8}{'net':>8}{'units':>7}{'per wk':>8}")
    print("-" * 72)
    for u, r in sorted(zip(units_by_listing, keep), key=lambda x: -x[1]["net_per_sale"]):
        print(f"{r['id']:<5}{r['product'][:35]:<36}{r['rec_realized']:>8.2f}{r['net_per_sale']:>8.2f}"
              f"{u:>7}{u/13:>8.2f}")
    print("-" * 72)
    print(f"{'':<5}{'TOTAL':<36}{blended_price:>8.2f}{blended_net:>8.2f}{total_units:>7}"
          f"{total_units/13:>8.2f}")

    # ---- can you BUY the traffic? break-even CPC = net/sale x CVR ----
    print("\n" + "=" * 72)
    print("CAN ADS BRIDGE THE GAP?  break-even CPC = net per sale x conversion rate")
    print("=" * 72)
    print(f"{'net/sale':>10}{'CVR 1.0%':>11}{'CVR 2.5%':>11}{'CVR 5%':>10}   vs typical CPC $0.15-0.45")
    for n in (5.54, blended_net, 15.0):
        print(f"{n:>10.2f}" + "".join(f"{n*c:>11.3f}" if c != 0.05 else f"{n*c:>10.3f}" for c in (.01, .025, .05)))
    print("\n  If your break-even CPC is BELOW what Etsy charges, ads are a way to buy DATA, not revenue.")
    print("  So: ads on ONE listing only, launch week, to seed 3-5 reviews. Then off.")
    print("=" * 72 + "\n")

    hdr = ["week", "monday", "sunday", "THE_ONE_JOB_THIS_WEEK", "listings_live",
           "units_target", "net_target", "net_cumulative", "pct_of_goal",
           "visits_target", "visits_per_day", "impressions_target",
           "YOUR_impressions", "YOUR_clicks", "YOUR_ctr", "YOUR_visits", "YOUR_orders", "YOUR_net"]
    out = []
    cum_net = cum_units = 0
    live = 14
    for i, u in enumerate(units, 1):
        mon = QUARTER_START + dt.timedelta(weeks=i - 1)
        net = u * blended_net
        cum_net += net; cum_units += u
        live = min(30, live + 2)
        cvr = MIN_CVR + (MAX_CVR - MIN_CVR) * (i - 1) / (WEEKS - 1)
        ctr = CTR_EARLY if i <= 5 else CTR_LATE
        visits = u / cvr
        out.append([i, mon.isoformat(), (mon + dt.timedelta(days=6)).isoformat(), JOBS[i], live,
                    u, round(net, 2), round(cum_net, 2), f"{cum_net/NET_GOAL*100:.0f}%",
                    round(visits), round(visits / 7), round(visits / ctr), "", "", "", "", "", ""])
        if i == 1:
            print(f"Week 1: {u} sales needs {visits:,.0f} visits = {visits/ctr:,.0f} search impressions "
                  f"at a {ctr*100:.1f}% CTR. Compare that to your current ~35 visits/week (9 sales / 1% "
                  f"implied CVR over 13 wks) and you will see the gap is TRAFFIC, not copy.")
    with open("q4_weekly_tracker.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(hdr); w.writerows(out)
        w.writerow(["", "TOTAL", "", "", "", cum_units, round(cum_net, 2), round(cum_net, 2), "100%",
                    round(sum(r[9] for r in out)), "", round(sum(r[11] for r in out))])
    print(f"{'wk':<4}{'units':>6}{'net':>8}{'cum':>8}{'visits':>8}{'/day':>7}{'impr':>10}")
    for r in out:
        print(f"{r[0]:<4}{r[5]:>6}{r[6]:>8.0f}{r[7]:>8.0f}{r[9]:>8}{r[10]:>7}{r[11]:>10,}")
    print(f"\nTOTAL {cum_units} sales · ${cum_net:,.0f} net · "
          f"{cum_units/13:.1f}/week · blended ${blended_price:.2f}")
    print(f"Traffic: {sum(r[9] for r in out):,.0f} visits total = "
          f"{sum(r[9] for r in out)/13:,.0f}/week = {sum(r[9] for r in out)/13/7:,.0f}/day")
    print("Wrote q4_weekly_tracker.csv")


if __name__ == "__main__":
    main()
