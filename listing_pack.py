"""
NovalityStore — Q4 listing pack
===============================

One source of truth for every rewritten listing, plus a VALIDATOR that
enforces Etsy's actual field limits before you paste anything into the
listing editor. If it prints PASS, it fits. If it prints FAIL, fix it —
Etsy will silently truncate or reject the rest.

Etsy field rules enforced here (2026):
  title        <= 140 chars; first 40-50 are all a mobile shopper sees
  tags         <= 13 tags, each <= 20 chars, lowercase, no dupes
  description  first ~160 chars are indexed for SEO; body should be 250-400 words
  price        list price is the anchor, sale price is what they pay

Run:   python listing_pack.py            -> validate + write Q4_LISTINGS.md + q4_listings.csv
       python listing_pack.py --check    -> validate only (exit 1 on failure)
"""

import csv
import json
import sys
import textwrap

from listings_copy import COPY

TITLE_MAX = 140
TAG_MAX = 20
TAG_COUNT = 13
MOBILE_VISIBLE = 47          # ~ where Etsy truncates titles in the app grid

# ---------------------------------------------------------------------------
# THE PACK.  Each entry is a finished listing: copy-paste ready.
# `k`  = primary keyword it is written to rank for
# `obs`= the market evidence behind the price (median page-1 sale price)
# ---------------------------------------------------------------------------

LISTINGS = [
# ══════════════════════════════════════════════════════════════════════════
# TIER 1 — CROCHET, SEASONAL (these carry Q4)
# ══════════════════════════════════════════════════════════════════════════
dict(
 id="N1", prio="DO NOW",
 window="Oct 1 – Dec 2 (advent must be finished by Dec 1, so buyers are earliest)", new=True,
 k="crochet advent calendar pattern",
 title="Crochet Christmas Advent Calendar Pattern PDF, 24 Mini Amigurumi Ornaments, Hanging Tree Countdown, Beginner Friendly, Instant Download",
 tags=["advent crochet pdf", "advent calendar pdf", "christmas crochet", "24 mini amigurumi",
       "crochet ornament", "crochet pattern pdf", "countdown decor", "amigurumi pattern",
       "holiday crochet", "crochet gift idea", "beginner crochet", "christmas decor", "crochet xmas"],
 list_price=25.00, sale_price=15.00,
 obs="page 1: 18 listings, median 800 reviews, prices $9-$40 with real reviews at $15. Advent is the one Christmas-crochet sub-niche with genuine pricing power.",
 why="Highest net-per-sale in your whole shop ($13.12). 77 sales alone clears $1,000. Build this even if you build nothing else.",
 desc="""Count down to Christmas in 24 little hooks.

This is a complete crochet PDF pattern for a hanging advent calendar: 24 mini amigurumi ornaments (1.5-2 in each) plus the tree-shaped countdown hanger they clip onto. Open one a day, save them all, string them up again next December.

WHAT YOU GET
- 18-page illustrated PDF, US crochet terms
- 24 individual mini patterns, each with its own materials list
- The tree hanger + clipping assembly with row-by-row counts
- Full colour step-by-step for the tricky rounds (magic ring, 6-8 sc increases, invisible decrease)
- Printable numbering template so the days go in the right order
- Link to the free 12-minute video for the hanger corner

SKILL LEVEL
Confident beginner. You need magic ring, single crochet, increase, decrease, and changing colour. Nothing is sewn — the minis clip on, which is why the whole thing is a weekend project rather than a month of weaving in ends.

MATERIALS
- Light worsted (4) yarn, approx 30g total in Christmas colours
- 3.5mm hook, 2.25mm for the tight hanger corners
- 24 locking stitch markers or safety pins, small amount of fibre fill
- Finished mini: 1.5-2 in / 4-5 cm

MADE FOR
People who want the advent calendar to BE the decoration. Also very popular as a teacher gift, a craft-group exchange, and for families who want the kids off screens in December.

INSTANT DOWNLOAD
Files unlock the moment your payment clears — no shipping, no waiting, nothing to print at a shop. Download to phone or laptop and crochet off the screen.

TERMS
Pattern is for personal use. You may sell finished items you make from it, including at craft fairs and in your own shop. Please credit NovalityStore and never resell, share, redistribute or reproduce the PDF itself, and don't use my photos for your listings.

QUESTIONS?
Message me before you buy if the skill level isn't clear — I would rather talk you into the right pattern than have you stuck on round 4. I answer fast, usually same day."""),

dict(
 id="C1", prio="DO NOW",
 window="Oct 15 – Dec 12 (decor deadline is tree-buying weekend)", new=False,
 k="christmas tree skirt crochet pattern",
 title="Crochet Christmas Tree Skirt Pattern, Bobble Snowflake Tree Collar, 3 Sizes 42 54 66 Inch, Chunky Holiday Ruffle, PDF Download",
 tags=["christmas tree skirt", "tree skirt crochet", "crochet tree collar", "bobble stitch",
       "snowflake crochet", "christmas crochet", "tree ruffle skirt", "crochet pattern pdf",
       "holiday table decor", "beginner crochet", "amigurumi christmas", "xmas tree decor", "crochet gift"],
 list_price=12.00, sale_price=8.00,
 obs="page 1: 32 listings, median ~140 reviews, top $8. Ceiling is $8, so $11.99-type pricing here is a conversion leak; your current $8 list / $6 sale under-earns.",
 why="Tree skirts are a real, non-commodity keyword with 3 sizes as your differentiation. Raise realized to the $8 ceiling and stop discounting below market.",
 desc="""A tree skirt with actual texture — bobbles that read as snow from across the room.

This is a crochet PDF pattern for a bobble-and-snowflake tree skirt worked in 3 sizes, so it fits a 4 ft, 6 ft or 7+ ft tree without you guessing at gauge.

WHAT YOU GET
- 14-page illustrated PDF, US and UK terms included
- 3 finished sizes: 42 in / 107 cm, 54 in / 137 cm, 66 in / 168 cm diameter
- 12-spoke construction chart so the increases land evenly
- Bobble stitch written out AND charted, with a photo of a correct bobble vs the two ways people get it wrong
- Optional ruffled edge section
- Blocking notes for a flat, circular finish under a tree

SKILL LEVEL
Easy-intermediate. Comfortable with single crochet, double crochet and working in the round. The bobble is the only new stitch and it repeats every other round.

MATERIALS (largest size)
- Bulky 5 or two strands of worsted 4, approx 900-1200 yds
- 5.5mm hook, 5mm for the center
- Yarn needle. No stuffing, no sewing.

MADE FOR
Real trees, flocked trees, and the cone-table trees people build for apartments. Because it is a circle worked from the centre outward, you can also stop at any round for a smaller tree or a table topper.

INSTANT DOWNLOAD
Available the second your payment clears. Crochet off your phone or print it.

TERMS
Personal use only for the PDF. Sell anything you make from it, everywhere, forever — just do not resell or share the pattern file, and please do not use my photos as your listing images.

SUPPORT
Stuck on a bobble round? Send me a photo of your work and I will tell you what happened. Most replies go out the same day."""),

dict(
 id="C2", prio="PRIORITY",
 window="Oct 15 – Nov 30 (wreath goes up before Thanksgiving)", new=False,
 k="crochet christmas wreath pattern",
 title="Crochet Christmas Wreath Pattern PDF, Padded Tube Ring With Removable Ornaments, 3 Sizes, Front Door Holiday Decor, Instant Download",
 tags=["crochet xmas wreath", "wreath crochet pdf", "amigurumi wreath", "door wreath crochet",
       "poinsettia crochet", "christmas crochet", "removable decor", "crochet pattern pdf",
       "holiday door decor", "beginner crochet", "winter crochet", "crochet gift idea", "xmas wreath"],
 list_price=9.00, sale_price=6.00,
 obs="page 1: 28 listings but thin — median only ~30 reviews, real price ceiling ~$5. Demand is shallow; do not sink more design time here, just fix the listing.",
 why="Your differentiator (removable decor on a padded tube) is genuinely unusual and nobody else on page 1 says it in the title. Say it louder, price at market, move on.",
 desc="""A wreath you can restyle instead of replacing.

Crochet PDF pattern for a padded tube-ring Christmas wreath with ornaments that come off. Same wreath base, different look every year — and the minis work on a mantel, a chair back, or gift wrap when they are not on the ring.

WHAT YOU GET
- 12-page illustrated PDF, US terms
- 3 ring sizes: 14 in, 18 in, 24 in diameter
- The padded tube ring construction (no florist wire form to buy)
- 5 removable decor pieces: poinsettia, bell, holly sprig, bauble, star
- Loop-and-button attachment so pieces do not slide or fall
- Hanging instructions that keep it from tilting on a door

SKILL LEVEL
Confident beginner. Chains, single crochet, double crochet, working into a tube. The padding is stuffing, not structure.

MATERIALS
- Worsted 4 green, approx 500 yds for the 18 in ring
- Small amounts in red, cream, gold
- Polyfill, 5mm hook, sewing needle for the attachment loops only

MADE FOR
Apartments where you cannot drill, front doors, and anyone whose wreath looked great in December and terrible in storage. The tube ring packs flat and never dents like a grapevine form.

INSTANT DOWNLOAD
Unlocks immediately after purchase. No shipping, no craft-store run on December 20th.

TERMS
Personal use for the pattern file. Sell your finished wreaths freely. No redistributing, reselling or sharing the PDF, and please do not use my photos as your own listing images.

SUPPORT
If a size does not work for your door, message me — I will tell you which ring count to use instead of guessing."""),

dict(
 id="C3", prio="PRIORITY",
 window="Nov 1 – Dec 12 (ornament makers work late; gift buyers early)", new=False,
 k="christmas crochet ornament pattern bundle",
 title="Christmas Crochet Ornament Pattern Bundle, 3 in 1 Bauble Star Snowflake, Stash Buster Spiral Hanging Decor, PDF Download",
 tags=["ornament crochet pdf", "ornament pattern", "amigurumi ornament", "crochet bauble",
       "crochet snowflake", "stash buster", "christmas crochet", "crochet bundle pdf",
       "tree decor crochet", "beginner crochet", "spiral crochet", "crochet gift", "holiday crochet"],
 list_price=8.00, sale_price=5.50,
 obs="page 1: 40 listings, heavy bundles everywhere (14-in-1, 20-in-1, 450 patterns). Median 200 reviews. You cannot out-bundle them, so win on the ornament being a GIFT and price under the mega-packs.",
 why="You are competing against 20-in-1 packs at $2. Bundle of 3 at $5.50 is the honest position: cheaper than 3 singles, and better than a 450-pattern junk pack.",
 desc="""Three ornaments, one afternoon, one ball of leftover yarn.

Crochet PDF pattern bundle: bauble, star and snowflake, all built to use up the odd 20-30g you have left from other projects. They hang straight, they photograph well, and they make sense as a set on a tree instead of three random bits.

WHAT YOU GET
- 11-page illustrated PDF, US and UK terms
- 3 patterns: bauble (2.5 in), star (3 in), snowflake (3 in)
- Each in two finishes: stuff-flat ornament, and keychain/charm version
- Spiral-hang variation so the ornament spins in a doorway instead of sitting still
- Full stitch counts for every round, no charts required
- Yardage table so you can check your stash before you start

SKILL LEVEL
Beginner. Magic ring, single crochet, half double crochet, increase, decrease, stuff, close. Everything else is colour changes and reading a count.

MATERIALS (all three)
- Scraps, roughly 60g total worsted 4, or DK with a 3.5mm hook
- 3.5mm hook, fibre fill, darning needle, 3 jump rings or keychain rings if you want charms

WHY A BUNDLE
Buying these separately costs you more than three times this. Making all three takes about 90 minutes and one session of TV. Giving three matching ornaments to one person is the entire reason this pattern exists.

INSTANT DOWNLOAD
Files unlock the moment payment clears, on any device.

TERMS
Personal use of the pattern only. Sell finished ornaments anywhere — Etsy, craft fairs, school sales. Do not resell, share or reproduce the PDF, and do not use my photos as your listing images.

SUPPORT
Wrong size, floppy star, snowflake that curls? Send a photo and I will fix it with you. Replies usually same day."""),

dict(
 id="C5", prio="PRIORITY",
 window="Nov 1 – Dec 19 (stocking-stuffer size = last-minute-friendly)", new=False,
 k="christmas gnome crochet pattern",
 title="No Sew Christmas Gnome Crochet Pattern, One Piece Amigurumi Gnome, 3 Sizes, Stocking Stuffer Ornaments, PDF Instant Download",
 tags=["gnome crochet pdf", "no sew crochet", "amigurumi gnome", "gnome pattern pdf",
       "easy crochet", "crochet ornament", "stocking stuffer", "scandi gnome", "crochet pattern pdf",
       "beginner crochet", "nordic gnome", "holiday crochet", "crochet gift"],
 list_price=9.00, sale_price=6.10,
 obs="page 1: 38 listings, brutal incumbents (42k reviews at $6.10, 8.3k at $3.59). Median 500 reviews. Survivable only because gnomes are giftable and 'no sew' is your real hook.",
 why="One-piece = no sewing is the thing buyers of gnomes actually complain about. Lead with it, price at $6.10 where the market's proven winner sits.",
 desc="""No arms to sew on. No beard to attach. One piece, top to toe.

Crochet PDF pattern for the no-sew Christmas gnome — body, hat and face all worked continuously, so the only thing you weave in is the yarn tail at the start.

WHAT YOU GET
- 16-page illustrated PDF, US and UK terms
- 3 sizes: 3 in ornament, 6 in shelf gnome, 9 in mantel gnome
- Continuous construction with no seams, no applied beard, no safety eyes required
- Embroidered face chart with stitch counts, plus an embroidered-cheek-free version for toddlers
- Hat-brim stiffening options (floral wire, cardboard, or nothing)
- Yardage + fill table for every size

SKILL LEVEL
Beginner-friendly. Magic ring, single crochet, sc2tog, increase, colour change, and stuff as you go. If you can make a ball you can make this gnome.

MATERIALS (6 in version)
- Red or green worsted 4 for the hat, cream for the face, approx 180 yds total
- 3.5mm hook, fibre fill, one tapestry needle, embroidery floss for the face

MADE FOR
Gnome people, obviously. Also: stocking stuffers that are not candy, matching sets for a whole street of neighbours, and school-sale inventory because one gnome takes about 3 hours.

INSTANT DOWNLOAD
Unlocks the moment your payment clears. No shipping, no waiting, crochet tonight.

TERMS
Personal use of the pattern file. Sell your gnomes anywhere you like, in any quantity. Do not resell, share, redistribute or reproduce the PDF, and do not use my photographs as your listing images.

SUPPORT
If your hat point flops or your brim will not stand, message me with a photo — that is the most common question and I have three fixes depending on your yarn."""),

dict(
 id="C6", prio="PRIORITY",
 window="Nov 20 – Dec 19 + Feb 1 – Feb 14 (gift + Valentine desk-buddy)", new=False,
 k="emotional support crochet pattern",
 title="Emotional Support Crochet Pattern Bundle, 3 in 1 Mini Amigurumi, Sunflower Penguin Potato Plushie, Desk Buddy PDF Download",
 tags=["emotional support", "mini amigurumi", "sunflower crochet", "penguin crochet",
       "potato plushie", "desk buddy", "crochet bundle pdf", "amigurumi pattern", "no sew crochet",
       "beginner crochet", "crochet gift idea", "anxiety support", "kawaii crochet"],
 list_price=9.00, sale_price=6.00,
 obs="page 1: only 18 listings, median 400 reviews, prices to $6+. This keyword is genuinely thin and giftable — you can own it, which is why it beats your Christmas tree listing.",
 why="Low competition + high demand per listing + gift language. Your single best 'rewrite this week' crochet listing.",
 desc="""Three small friends who live on your desk and make absolutely no demands.

Crochet PDF pattern bundle for the emotional support mini set: a sunflower, a penguin, and a potato. Each one is palm-sized, weighted-optional, and built to sit on a monitor ledge, a nightstand or a work bag without toppling.

WHAT YOU GET
- 20-page illustrated PDF, US and UK terms
- 3 patterns: sunflower (3.5 in), penguin (4 in), potato (3 in)
- Each with two versions: fully amigurumi, and the no-sew one-piece build
- Optional micro-bead weight pocket so they sit upright on a desk
- Facial expression chart: content, sleepy, unbothered
- Yardage table — every one of these is a 25g stash-buster

SKILL LEVEL
Beginner. Magic ring, single crochet, increase, decrease, stuff, close. The sunflower petals are the only thing that takes a second look.

MATERIALS (all three)
- Worsted 4: mustard, brown, black, white, tan (approx 150g total, less if you split stash)
- 3.25mm hook, fibre fill, tapestry needle, optional 30g poly-pellets

WHY PEOPLE BUY THIS
Because it is a gift for someone who has everything and needs none of it. Coworker Secret Santa, teacher thank-you, 'saw this and thought of you'. Three plushies for the price of one pattern.

INSTANT DOWNLOAD
Available the second your payment confirms, on phone, tablet or laptop.

TERMS
Personal use of the pattern. Sell finished plushies freely, including in your own shop and at markets. Do not resell, share or reproduce the PDF, and do not use my photos for your listings.

SUPPORT
Message me if a version is unclear. If you tell me which one and send a photo, I will tell you exactly where it went sideways."""),

dict(
 id="N2", prio="DO NOW",
 window="Nov 1 – Dec 20 (Thanksgiving AND Christmas table)", new=True,
 k="christmas table runner crochet pattern",
 title="Crochet Christmas Table Runner Pattern PDF, Reindeer and Poinsettia Festive Runner, Christmas Dinner Decor, Instant Download",
 tags=["table runner crochet", "crochet table runner", "christmas runner", "poinsettia crochet",
       "reindeer crochet", "holiday table decor", "christmas crochet", "crochet placemat",
       "table setting decor", "intermediate crochet", "festive runner", "crochet pattern pdf", "xmas decor"],
 list_price=10.00, sale_price=7.00,
 obs="page 1: 20 listings, median ~300 reviews, ceiling ~$7. Adjacent 'linen stitch placemat' winner has 882 reviews at $5.53 — same buyer, more money per sale.",
 why="Nobody is buying this in December for fun — they are buying it for a specific dinner on a specific date. Seasonal urgency + a real object = you can charge $7 instead of $4.",
 desc="""The thing on the table that everyone photographs before they sit down.

Crochet PDF pattern for a Christmas table runner — an openwork band of poinsettia motifs joined by reindeer, sized for a 6 ft table with a shorter 4 ft version included.

WHAT YOU GET
- 15-page illustrated PDF, US and UK terms
- 2 lengths: 48 in / 122 cm and 68 in / 173 cm, both 14 in wide
- Poinsettia motif worked flat (no joining six petals by hand — it is built in rounds)
- Reindeer border chart, written and diagrammed
- Optional matching napkin ring and 4 place-card holder patterns included free in the same PDF
- Washing and blocking notes for something that will get gravy on it

SKILL LEVEL
Easy-intermediate. Chains, slip stitch, single and double crochet, working both sides of a foundation chain. If you have ever been annoyed by motifs that need seaming, this pattern solves that specifically.

MATERIALS (68 in runner)
- DK weight: cream 400 yds, forest green 150 yds, red 100 yds, brown 50 yds
- 4.0mm hook, blocking mats or towels and pins

MADE FOR
Christmas dinner, office holiday party tables, and anyone whose table has never once had anything on it besides plates. Also a genuine wedding or housewarming gift for the person who hosts everything.

INSTANT DOWNLOAD
Unlocks immediately after payment. Crochet it in a weekend if you start on Friday.

TERMS
Pattern is personal use. Sell finished runners anywhere. No reselling, sharing or reproducing the PDF, and please do not use my photos as your own listing images.

SUPPORT
Width wrong for your table? Message me your table length and I will tell you how many repeats to add."""),

# ══════════════════════════════════════════════════════════════════════════
# TIER 1 — SPREADSHEETS, SEASONAL + BUSINESS
# ══════════════════════════════════════════════════════════════════════════
dict(
 id="S1", prio="DO NOW",
 window="Sep 28 – Dec 20 (hard stop: a gift tracker after the 20th is useless)", new=False,
 k="christmas gift tracker spreadsheet",
 title="Christmas Gift Tracker Spreadsheet, Excel and Google Sheets Template, Holiday Gift Budget Planner, Countdown Dashboard, Instant Download",
 tags=["gift tracker pdf", "gift list template", "holiday budget sheet", "christmas budget",
       "gift planner excel", "secret santa list", "christmas planner", "google sheets",
       "gift ideas list", "holiday countdown", "budget tracker", "xmas planning", "gift organizer"],
 list_price=15.99, sale_price=9.99,
 obs="page 1: 36 listings, prices range $0.68 to $9.99 with 8.7k and 5.4k review sellers at $3-$5. Median ~700 reviews. Ceiling on page 1 is ~$5 for a bare tracker — your $11.99 only survives if the countdown dashboard is visibly a different product.",
 why="You are priced above the proven band for a 'tracker'. Either add enough to justify $9.99 (countdown + budget + wrapping log) or drop to $5. I recommend the former — you need the dollars.",
 desc="""Stop keeping Christmas in eleven notes apps.

A Christmas gift tracker built for the actual mess: who, what, what it costs, whether you bought it, whether you wrapped it, whether you spent more than you said you would.

WHAT IT DOES
- Google Sheets version AND Excel version, both included in one download
- Gift tracker: recipient, relationship, idea, link, store, budget, actual, status, wrap status, delivery date, address
- Budget by recipient AND by category, with over/under flagging that turns red the moment you cross your own number
- Live countdown to December 25 that counts down shopping days, not just calendar days
- Dashboard with donut + bar charts, no setup, no formulas to write
- Wrapping-station checklist and a returns/deadlines tab for online orders
- Secret Santa section: name, guess list, price cap, drawn-by date
- Cards tab: sent / received, so you can find out who forgot you
- Works on mobile. Filters, dropdowns and a colour-coded status column instead of a wall of text

WHAT MAKES IT DIFFERENT
Most gift trackers are a list. This one is a plan with a countdown attached. You set a total budget first, and every entry tells you what it costs you against what is left — which is the only reason anyone ever opens a spreadsheet in December.

MADE FOR
Households of two or more coordinating, anyone buying for 12+ people, teachers and nurses running classroom exchanges, and the friend who volunteers to organise the family gift swap every year and then loses their mind in week three of December.

HOW IT WORKS
1. Buy. 2. Download the PDF, which contains your copy links. 3. Open in Excel or Google Sheets. 4. Set your budget. That is the whole setup.

A 12-minute walkthrough video is included, plus a printable one-page gift list for the person in your house who will not look at a screen.

TERMS
Personal use. This is a financial planning tool, not a business template — do not resell, share, redistribute or rebrand the file itself.

SUPPORT
Something not calculating the way your data should? Send me your recipient row and a screenshot and I will fix it, usually the same day."""),

dict(
 id="N6", prio="DO NOW",
 window="Nov 1 – Dec 22 (hosting panic is the most price-insensitive week of the year)", new=True,
 k="christmas dinner planner spreadsheet",
 title="Christmas Dinner Planner Spreadsheet, Holiday Menu and Grocery Budget Google Sheets, Cooking Timeline Template, Excel Instant Download",
 tags=["xmas dinner planner", "holiday menu planner", "menu spreadsheet", "cooking timeline",
       "christmas budget", "grocery list", "holiday hosting", "google sheets",
       "potluck sign up", "excel planner", "recipe scaling", "christmas checklist", "meal planner"],
 list_price=13.99, sale_price=9.00,
 obs="page 1: 22 listings, median ~500 reviews, ceiling ~$9. Adjacent 'holiday meal planner' sellers price $6-$12. Real money, thin shelf.",
 why="December hosting panic is the most price-insensitive buyer you will meet all quarter. Nobody comparison-shops a spreadsheet at 9pm on December 22.",
 desc="""The Christmas dinner that does not live in your head.

A holiday hosting spreadsheet that turns 'everyone is coming on the 24th' into a menu, a budget, a shopping list and an hour-by-hour timeline, and then keeps them in sync when Aunt Linda changes her order.

WHAT IT DOES
- Google Sheets AND Excel, both in the download
- 7 tabs, and nothing gets typed twice: every tab reads its facts from Setup
- Menu tab: dish, cook, serve, who is bringing it, dietary notes, and a per-plate cost
- Guest + seating tab: headcount drives the recipe scaling automatically (double, triple, x1.5, x2)
- Grocery list that consolidates across dishes and sorts by store section so you walk the aisle once
- Budget: expected spend vs receipts, with a per-head cost so you know what the night actually costs you
- Cooking timeline: works backwards from serving time, in hours, and flags the three dishes that cannot be late
- Potluck invite list a guest can fill in themselves — one link, no group chat archaeology
- Leftovers and storage tab, because Christmas food safety matters and nobody plans for it

WHY A SPREADSHEET AND NOT AN APP
Because the guest count changes on the 22nd, and you should not have to re-do a whole plan because of it. Change headcount once, and quantities, cost-per-head and the shopping list update themselves.

MADE FOR
Whoever hosts. Also the 28-year-old hosting for the first time with five grocery stores and no idea how much turkey to buy.

HOW IT WORKS
Buy, open the PDF, click your copy link, pick Excel or Google Sheets, set your headcount. Four minutes, start to finish. A short walkthrough video is included.

TERMS
Personal use only. Do not resell, share, redistribute or rebrand the file.

SUPPORT
If a formula misbehaves on your version of Excel, send a screenshot and I will patch it. I answer fast."""),

dict(
 id="S13", prio="PRIORITY",
 window="Nov 17 – Dec 2 + Jan 2 – Jan 20 (Black Friday sellers + new-year shop starts)", new=False,
 k="etsy seller spreadsheet",
 title="Etsy Shop Spreadsheet, Sales, Fees, Profit and Inventory Tracker for Sellers, Excel and Google Sheets Template, Bookkeeping Dashboard",
 tags=["etsy spreadsheet", "etsy sales tracker", "craft fair tracker", "small business sheet",
       "profit tracker", "fee calculator", "etsy bookkeeping", "inventory tracker", "google sheets",
       "excel template", "maker business", "tax prep", "pricing calculator"],
 list_price=19.99, sale_price=12.99,
 obs="page 1: 25 listings, median ~300 reviews, ceiling ~$13. Competitor with 44 reviews at $4.99 is underpriced, not smarter. Your asset is better — price like it.",
 why="You are literally an Etsy seller; that credibility is the product. Highest-demand business keyword where your price is already right. Fix the copy, not the price.",
 desc="""Know what your shop actually made, before tax season reminds you.

An Etsy-focused bookkeeping and profit spreadsheet that accounts for the fees nobody remembers, and tells you per-listing whether an item pays you or just keeps you busy.

WHAT IT DOES
- Google Sheets AND Excel included
- Order log: date, listing, quantity, gross, Etsy fee, payment processing, shipping cost, materials, net profit, margin %
- Automatic Etsy fee + 6.5% + payment-processing calculation — stop doing this in your head
- Per-listing profitability ranking, so you can see which four listings pay for the shop
- Inventory + supply tracker with a reorder point, sized for a craft room not a warehouse
- Season and month view, plus Q4 prep numbers (what you earned last November vs what you need)
- Tax-ready summaries: gross sales, total fees, net by category, exportable for your accountant
- Craft-fair mode: booth fee, mileage, and cost-per-event so you stop saying yes to fairs that lose money
- Pricing calculator: what you must charge to hit a target margin after fees, materials and your time

WHY IT IS DIFFERENT
Most business trackers treat Etsy like a normal store. Etsy is not a normal store — the fee stack is the difference between profitable and pretending. This one models the stack.

MADE FOR
Handmade, print-on-demand, vintage, crafters at markets, and anyone who has ever thought 'I made $4,000 this month' and then panicked about what was left.

HOW IT WORKS
Buy, open the download PDF, choose Excel or Google Sheets, paste in your Etsy CSV order export (10-second import, no column matching). Watch the dashboard build itself.

A 15-minute walkthrough video covers the CSV import specifically, because that is where people stall.

TERMS
Personal use for your own shop. Please do not resell, share, redistribute or rebrand the template — it is one shop licence per purchase.

SUPPORT
Send me a screenshot of the row that looks wrong and I will tell you what is off. Usually same day."""),

dict(
 id="S6", prio="DO NOW",
 window="Mar 1 – Jun 30 + Sep 28 – Nov 30 (renovation season, and people plan in autumn)", new=False,
 k="home renovation budget spreadsheet",
 title="Home Renovation Budget Spreadsheet, Remodel Cost Tracker and Contractor Quote Comparison, Excel Google Sheets Template, Instant Download",
 tags=["renovation budget", "remodel cost tracker", "contractor quote", "reno budget sheet",
       "construction budget", "renovation planner", "project cost sheet", "excel template",
       "google sheets", "house flip", "budget overrun", "kitchen remodel", "home improvement"],
 list_price=24.99, sale_price=17.00,
 obs="page 1: 19 listings, median ~110 reviews, real ceiling ~$17-$22. Buyers here are spending $30k-$120k on the project; $17 is a rounding error and they treat it like one.",
 why="Best price elasticity in your catalogue: high-ticket life event, low price sensitivity, thin competition. This is a '3 sales a month' listing, not a '40 sales a month' listing — and it needs fewer visits.",
 desc="""Before the contractor asks for a deposit, know what this should cost.

A home renovation budget spreadsheet built to catch the two things that actually ruin a remodel: comparing quotes that are not comparable, and the small overruns that nobody writes down.

WHAT IT DOES
- Google Sheets AND Excel, both included
- Room-by-room budget with target vs actual and a live variance bar
- Quote comparison tab: line-item the same scope across up to 5 contractors, so a 'cheaper' bid that excludes electrical stops fooling you
- Change-order log with running impact on total and timeline
- Material list with quantities, unit prices, and a supplier column for the three different stores
- Contingency tracker with a recommended 10-20% band and a warning when your overrun is eating it
- Permit, inspection and timeline tracker with dependencies
- Payment schedule by milestone — never pay on a date, pay on a completed stage
- Finance mode: cash, HELOC and loan scenarios with interest cost
- Cost-per-sqft and % -of-home-value sanity checks so you can see if you are over-improving

WHY IT IS WORTH $17
The average kitchen remodel overrun is in the thousands. If this catches one line you would otherwise have approved, it paid for itself forty times over.

MADE FOR
DIY-ers managing their own trades, first-time renovators, flippers costing a job, and anyone whose spouse said 'let's get three quotes' and is about to compare three different projects.

HOW IT WORKS
Buy, open the download, click your copy link. Pick Excel or Google Sheets. Enter your rooms. Everything else calculates.

Includes a 10-minute walkthrough plus a printable contractor questions sheet to take to the site visit.

TERMS
Personal use for your own project. Do not resell, share, redistribute or rebrand the file.

SUPPORT
If your scope is weird — whole-house, basement only, no contractor — message me and I will tell you which tabs to ignore."""),

dict(
 id="S8", prio="PRIORITY",
 window="evergreen — 30% off on the 1st of each month (investors buy on month-end analysis)", new=False,
 k="rental property analysis spreadsheet",
 title="Rental Property Analysis Spreadsheet, Cap Rate Cash Flow DSCR and 1% Calculator, Real Estate Investor Excel Template, Instant Download",
 tags=["rental analysis", "cap rate calculator", "cash flow sheet", "real estate analysis",
       "dscr calculator", "1 percent rule", "rental property", "real estate investor", "excel template",
       "property valuation", "noi calculator", "rental income", "flip calculator"],
 list_price=17.99, sale_price=12.00,
 obs="page 1: 22 listings, median ~200 reviews, ceiling ~$12. Buyers are evaluating six-figure purchases; this is the cheapest due diligence they will do that week.",
 why="Highest-value-per-minute buyer in your shop and the market already pays $12. Merge your two rental listings into one and stop splitting the reviews.",
 desc="""Two minutes per deal, instead of a calculator and a gut feeling.

A rental property analysis spreadsheet that runs the numbers lenders, syndicators and serious private buyers actually underwrite on — with the assumptions visible so you can argue with them.

WHAT IT DOES
- Excel template plus a Google Sheets copy
- Deal entry: price, down payment, rate, term, rent, taxes, insurance, HOA, vacancy, maintenance, capex, management, utilities
- Outputs: monthly cash flow, annual cash flow, Cap Rate, Cash-on-Cash, GRM, Total Return, 1% Rule check, DSCR, and Debt Yield
- NOI built the right way — with a real operating-expense stack, not 'rent minus taxes'
- Rent-compare row so you can test $1,850 vs $2,000 and see what it does to your cash-on-cash
- Sensitivity grid: rate ±1.0%, vacancy ±5%, price ±10%, all at once, so you can see which variable actually hurts
- Financing scenarios: conventional, FHA 203k, hard money, seller carry — same property, four answers
- Flip / BRRRR mode: rehab budget, holding costs, ARV, exit fees, and profit-per-flip
- Expense assumption defaults by property type (SFR, duplex, triplex, condo) so you are not guessing at maintenance

WHY IT IS DIFFERENT
Most templates on Etsy are a budget with a house on it. This one is an underwriting sheet: the inputs are the ones a lender's appraisal package will use, and every rate is editable and labelled instead of hidden inside a formula.

MADE FOR
First investment property buyers, house-hackers, flippers, and anyone who has been burned by a 'cash flowing' deal that was not.

HOW IT WORKS
Buy, download, open in Excel (or copy to Google Sheets). Enter 14 numbers. Read the answer. Duplicate the tab for deal #2.

Includes a 9-minute walkthrough and a one-page 'questions to ask the seller' checklist.

TERMS
Personal use for evaluating and closing your own properties. Do not resell, share, redistribute, rebrand, or bundle this into a course.

SUPPORT
If your market's numbers are unusual, message me with the deal and I will tell you which assumptions to change. I answer fast."""),

dict(
 id="S2", prio="PRIORITY",
 window="evergreen — 25% off Jan 2 – Jan 31 (licences and New Year bakery launches)", new=False,
 k="cottage bakery business spreadsheet",
 title="Cottage Bakery Business Spreadsheet, Order Form and Pricing Calculator with Recipe Costing, Bakery Profit Tracker Google Sheets Excel",
 tags=["cottage bakery", "bakery spreadsheet", "recipe costing", "baking business", "cake pricing",
       "order tracker", "cottage food", "bakery profit", "google sheets", "excel template",
       "home bakery", "food cost calculator", "baker business"],
 list_price=14.99, sale_price=9.99,
 obs="page 1: 20 listings, thin (median ~90 reviews), ceiling ~$11. Your two identical listings each have ~1 review — split reviews, split ranking. Merge them.",
 why="You already have 5-star reviews with a customer thanking you by name on this one. That's social proof for a $10 product in a thin niche. Consolidate and it becomes your best evergreen listing.",
 desc="""Price your cakes so you keep money.

A cottage bakery spreadsheet that solves the specific thing that breaks home bakeries: charging $45 for a three-tier cake that cost you $38 in butter, boxes and time.

WHAT IT DOES
- Google Sheets AND Excel, both included
- Recipe costing: enter ingredients once with unit prices, and every recipe tells you its true cost per batch and per unit
- Cake and cookie pricing calculator with margin targets (choose 3x, 4x, 5x) and your hourly labour rate included
- Order book: client, event date, item, deposit, balance due, pickup or delivery, and a status that turns red when a balance is unpaid 7 days out
- Seasonal price list you can print or screenshot for Instagram — one button, clean version
- Ingredient inventory with reorder levels, so you find out about the vanilla in October not December
- Sales, expenses and profit by month, with cost-of-goods broken out
- Cottage-food tax summary: gross sales, ingredient cost, packaging, mileage, net
- Wedding/quote builder: quote a client in one screen and send it as a PDF

WHY IT IS DIFFERENT
Most bakery templates are an order list. This one is built around costing first, because the reason home bakeries quit is not demand — it is finding out in month six that they were paying to work.

MADE FOR
Cottage-food and home bakers, cake decorators, cookie shops at market, and anyone who has priced a wedding by guessing.

HOW IT WORKS
Buy, open the download, click your copy link. Load your 10 core ingredients. Price your top 5 items. Start taking orders.

Includes a 14-minute walkthrough on recipe costing specifically, since that is where everyone's maths quietly goes wrong.

TERMS
Personal use for your own bakery. Do not resell, share, redistribute or rebrand the template.

SUPPORT
Send me a recipe and I will cost it with you. If the margin is bad I will tell you that too — which is the point of the sheet."""),

dict(
 id="S5", prio="PRIORITY",
 window="Nov 24 – Dec 1 (contractors do their books and buy tools at Black Friday)", new=False,
 k="construction estimate spreadsheet",
 title="Construction Estimate Spreadsheet Bundle, Contractor Bid Template, Job Cost Tracker and AIA Progress Billing, Excel Google Sheets",
 tags=["construction cost", "contractor bid", "aia invoice", "job costing", "estimate template",
       "builder spreadsheet", "change order log", "renovation estimate", "excel template",
       "google sheets", "progress billing", "subcontractor bid", "construction budget"],
 list_price=62.50, sale_price=37.50,
 obs="page 1: 14 listings only, median ~80 reviews, ceiling $38+. This is a professional tool, not a printable — buyers are comparing against $200 software.",
 why="At $33.94 net you need only 30 sales in 13 weeks for $1,000 from this listing alone. Your single highest-leverage existing asset. It is currently priced like a $14 hobby file.",
 desc="""Bid the job, cost the job, invoice the job.

A three-part construction spreadsheet bundle for contractors and small builders who are done estimating in a notes app and invoicing in a word document.

WHAT IS IN THE BUNDLE
1. ESTIMATE / BID TEMPLATE
   Line-item takeoff sheet: division, description, quantity, unit, material cost, labour hours, rate, markup, subtotal. Prints to a client-facing bid with your logo on it, terms at the bottom, and an accept-by date.

2. JOB COSTING
   The same line items, once you have the actuals: quoted vs actual on materials, labour and equipment, with variance by division and a gross-margin number that updates as you spend. This is the tab that shows you which type of job you should stop bidding.

3. PROGRESS BILLING (AIA-style)
   Schedule of values, % complete per line, requisition, retainage held and released, and a running pay-app summary. Structured to match how AIA G702/G703 style billing actually works, without needing $200 software.

PLUS
- Change order log with cumulative impact on contract value and schedule
- Subcontractor bid comparison sheet — scope the same way across three subs so the low bid means something
- Project timeline with milestone payment triggers
- Works in Excel and Google Sheets

MADE FOR
Remodellers, handymen scaling up, specialty subs (roofing, HVAC, concrete, electrical), and anyone billing against a schedule of values for the first time.

INSTANT DOWNLOAD
Buy once, use on every job. The download contains links for your own copy of all three tools plus a 20-minute setup walkthrough on reading a job's real margin.

TERMS
One-business licence. Use it on unlimited jobs. Do not resell, share, redistribute, rebrand, or offer it as part of a course or coaching product.

SUPPORT
Your trade bills slightly differently — tell me which and I will tell you how to use the SOV tab for it. I answer same day, and I would rather talk to you before the bid than after the loss."""),
]

# ---------------------------------------------------------------------------
# TIER 2 - the copy sheet. Every remaining live listing: title + 13 tags + price,
# validated to Etsy's field limits. Descriptions come from the §4.3 template in
# Q4_PLAYBOOK.md - writing 22 near-identical descriptions would help neither you
# nor the algorithm; writing YOURS from the template, with your own file details,
# is what actually converts.
# ---------------------------------------------------------------------------
LIGHT = [
    dict(id="C4", prio="MAYBE", new=False, light=True, k="christmas tree crochet pattern pdf",
         window="Nov 1 – Dec 12 (tree goes up early November; a pattern bought after the 12th isn't finished in time)",
         title="Crochet Christmas Tree Pattern PDF, Bobble Stitch One Piece Table Tree, 3 Sizes Easy Amigurumi Decor, US and UK Terms",
         tags=["xmas tree crochet", "crochet tree pattern", "bobble stitch", "amigurumi christmas", "one piece crochet", "mini tree crochet", "christmas decor", "beginner crochet", "crochet pattern pdf", "holiday crochet", "table centerpiece", "xmas tree decor", "easy crochet"],
         list_price=11.99, sale_price=8.0,
         desc="", note="~45 listings in the cluster, with a 43k-review Christmas ebook at $13.92 (and a 3.8k granny-square at $10.20). Keep it as bundle bait; do not build more trees."),
    dict(id="C7", prio="PRIORITY", new=False, light=True, k="capybara crochet pattern no sew",
         window='evergreen, 30% off on the 1st of each month (gift spikes: Feb 1–14, May 1–10, Sep 1–15 back-to-school)',
         title="No Sew Capybara Crochet Pattern, Easy Amigurumi Capybara Plushie With Orange, Beginner Friendly PDF, Instant Download",
         tags=["capybara crochet", "amigurumi capybara", "no sew crochet", "crochet plushie", "easy amigurumi", "kawaii crochet", "crochet pattern pdf", "beginner crochet", "yuzu capybara", "crochet animal", "cute crochet", "stash buster", "plushie pattern"],
         list_price=5.49, sale_price=3.5,
         desc="", note="Raise from $2.62. No-sew amigurumi sellers with 2k-18k reviews sit at $3.75-$6.39; $2.62 reads as a broken pattern, not a bargain."),
    dict(id="C8", prio="PRIORITY", new=False, light=True, k="axolotl crochet pattern pdf",
         window='Nov 20 – Dec 19 + Jul 1 – Aug 15 (teacher gifts and classroom reading buddies)',
         title="No-Sew Axolotl Crochet Pattern, Easy Amigurumi Axolotl Plushie PDF, Beginner Friendly Kawaii Sea Creature, Instant Download",
         tags=["axolotl crochet", "amigurumi axolotl", "no sew crochet", "kawaii crochet", "crochet plushie", "easy amigurumi", "beginner crochet", "crochet pattern pdf", "sea creature crochet", "cute animal pattern", "stash buster", "plushie pattern", "aquarium decor"],
         list_price=5.49, sale_price=3.5,
         desc="", note="This is the listing with the 1-star. Sequence: real photo of the actual arms -> v1.1 note in description -> then reprice. Not before."),
    dict(id="C9", prio="MAYBE", new=False, light=True, k="loaf cat crochet pattern",
         window='evergreen · 25% off only on Black Friday, it sells itself the rest of the year',
         title="Loaf Cat Crochet Pattern, No Sew Amigurumi Cat Loaf, Easy Kitty Plushie Tutorial, Beginner PDF Instant Download",
         tags=["loaf cat crochet", "amigurumi cat", "no sew crochet", "cat plushie", "kawaii crochet", "crochet kitten", "easy amigurumi", "beginner crochet", "crochet pattern pdf", "loaf cat", "cat lover gift", "cute animal pattern", "stash buster"],
         list_price=4.99, sale_price=3.0,
         desc="", note="Stable micro-niche. $3 is a volume price; the real upside is a 3-cat 'cat loaf family' pack at $6."),
    dict(id="C10", prio="MAYBE", new=False, light=True, k="baby dragon crochet pattern",
         window='Nov 20 – Dec 19 (kid gifts) + Jul (birthday-season plateau)',
         title="Baby Dragon Crochet Pattern, Amigurumi Dragon With Wings and Spikes, Easy Fantasy Plushie PDF, Beginner Friendly Download",
         tags=["baby dragon crochet", "amigurumi dragon", "dragon plushie", "fantasy crochet", "crochet wings", "easy amigurumi", "kawaii crochet", "beginner crochet", "crochet pattern pdf", "dragon gift", "mythical creature", "crochet plushie", "stash buster"],
         list_price=7.99, sale_price=5.0,
         desc="", note="You already list at $7; your realised $5.25 is at market. Stop discounting through it."),
    dict(id="C11", prio="MAYBE", new=False, light=True, k="highland cow crochet pattern",
         window="Nov 1 – Dec 12 (farmhouse/Scandi gift buying) + Mar 1 – Mar 17 (St Patrick's colourway traffic)",
         title="Highland Cow Amigurumi Crochet Pattern, Shaggy Fringe and Horns, Farm Animal Plushie PDF, Beginner Friendly Instant Download",
         tags=["highland cow crochet", "amigurumi cow", "farm animal crochet", "shaggy crochet", "cow plushie", "scandi decor", "easy amigurumi", "beginner crochet", "crochet pattern pdf", "nursery gift", "farmhouse decor", "crochet animal", "gift for her"],
         list_price=7.99, sale_price=5.0,
         desc="", note="Evergreen giftable. A palm/plushie variant is a second listing from the same body pattern - cheapest new SKU you can make."),
    dict(id="C12", prio="PRIORITY", new=False, light=True, k="halloween crochet pattern bundle",
         window="NOW – Oct 20 only. Set the sale to END Oct 21 and switch the listing to next year's queue after that.",
         title="Halloween Crochet Pattern Bundle, 3 in 1 Ghost Pumpkin Bat Amigurumi, Kawaii Trick or Treat Ornaments PDF Download",
         tags=["halloween crochet", "amigurumi halloween", "crochet pumpkin", "crochet ghost", "crochet bat", "halloween ornament", "kawaii crochet", "crochet bundle pdf", "easy amigurumi", "beginner crochet", "trick or treat", "spooky decor", "halloween craft"],
         list_price=8.99, sale_price=6.0,
         desc="", note="Timing: peaks Sep 15 - Oct 20. Rewrite THIS WEEK or the listing is dead for a year."),
    dict(id="C13", prio="MAYBE", new=False, light=True, k="sea turtle crochet pattern keychain",
         window='Apr 15 – Aug 31 (market/beach season, festival bag charms)',
         title="Sea Turtle Crochet Pattern, No Sew Amigurumi Turtle Keychain and Bag Charm, 1 Hour Quick Make PDF Instant Download",
         tags=["sea turtle crochet", "turtle keychain", "amigurumi turtle", "no sew crochet", "bag charm crochet", "crochet charm", "quick crochet", "beginner crochet", "crochet pattern pdf", "ocean theme", "sea creature", "stash buster", "beach gift"],
         list_price=4.99, sale_price=3.0,
         desc="", note="'1 Hour' is the whole hook for a keychain buyer and it was missing from your title. Add time, not adjectives."),
    dict(id="C14", prio="MAYBE", new=False, light=True, k="bunny lovey crochet pattern",
         window='evergreen — 30% off Feb 1 – Feb 28 and Sep 1 – Oct 15 (baby-shower season has two peaks)',
         title="Bunny Lovey Crochet Pattern, Amigurumi Baby Blanket With Bunny Head, Baby Shower Gift PDF, Beginner Friendly Download",
         tags=["bunny lovey", "amigurumi lovey", "baby blanket crochet", "crochet lovey", "shower gift crochet", "bunny baby blanket", "newborn gift", "easy crochet", "crochet pattern pdf", "nursery decor", "soft toy crochet", "bunny crochet", "gift for baby"],
         list_price=5.99, sale_price=4.0,
         desc="", note="The baby-shower angle supports more money than the plushie angle. Say 'baby shower gift' in the title and price it at $4-5."),
    dict(id="C15", prio="SHELVE", new=False, light=True, k="chenille duck crochet pattern",
         window='Feb 20 – Apr 10 (Easter and spring baskets), then let it rest',
         title="Chenille Duck Crochet Pattern, Low Sew Amigurumi Duckling in Velvet Yarn, Beginner Plushie PDF Instant Download",
         tags=["chenille duck", "duck crochet pattern", "amigurumi duck", "velvet yarn crochet", "no sew crochet", "crochet plushie", "beginner crochet", "easy amigurumi", "crochet pattern pdf", "spring decor", "farm animal", "cute animal pattern", "stash buster"],
         list_price=4.99, sale_price=3.0,
         desc="", note="16 listings, $3.50 median. Fine to own; not worth a photo shoot."),
    dict(id="S3", prio="MAYBE", new=False, light=True, k="church management spreadsheet",
         window='Jan 2 – Jan 31 (budget-setting month) + Sep 1 – Sep 15 (autumn program year)',
         title="Church Management Spreadsheet, Member Directory and Giving Tracker With Donation Reports, Excel and Google Sheets Template",
         tags=["church management", "church directory", "giving tracker", "tithe record", "church admin", "nonprofit sheets", "donation log", "member roster", "excel template", "google sheets", "small church", "ministry admin", "budget tracker"],
         list_price=15.99, sale_price=11.0,
         desc="", note="17 listings, weak incumbents, $13 ceiling. Buyers type 'giving' and 'membership', you wrote 'donation' - match their vocabulary."),
    dict(id="S4", prio="SHELVE", new=False, light=True, k="school management spreadsheet",
         window='Jul 1 – Aug 20 (before the school year) + Jan 2 – Jan 20 (second-semester enrolment)',
         title="School Management Spreadsheet, Student Roster, Fees and Attendance Tracker With Staff Dashboard, Excel Template Download",
         tags=["school management", "student tracker", "attendance sheet", "teacher spreadsheet", "tuition tracker", "school admin", "class roster", "grade book", "excel template", "google sheets", "homeschool admin", "private school", "fee ledger"],
         list_price=37.99, sale_price=26.0,
         desc="", note="Highest ceiling in your shop ($26) on 15 listings with ~60 median reviews. Price is right - the leak is a cover image that does not show the dashboard."),
    dict(id="S7", prio="MAYBE", new=False, light=True, k="small business bookkeeping spreadsheet",
         window='Dec 26 – Jan 15 (tax prep) + Mar 1 – Apr 10 (filing season, the highest-intent two weeks of the year)',
         title="Small Business Bookkeeping Spreadsheet, Income, Expense and Profit Tracker, P&L Dashboard for Excel and Google Sheets",
         tags=["bookkeeping sheet", "small business", "profit tracker", "expense tracker", "income tracker", "p and l", "business budget", "tax prep", "excel template", "google sheets", "cash flow", "bookkeeping template", "sole trader"],
         list_price=14.99, sale_price=10.0,
         desc="", note="46 listings deep; largest observed review count in the sample was 2.6k, plus a 1.3k PLR seller at $9.85. Do not chase this keyword - keep it as a landing page and cross-link from your niche sheets."),
    dict(id="S9", prio="MAYBE", new=False, light=True, k="personal finance spreadsheet bundle",
         window='Dec 20 – Jan 31 (New Year reset is the whole demand curve for this product)',
         title="Personal Finance Spreadsheet Bundle, 22 Budget, Debt Payoff and Net Worth Trackers, Excel and Google Sheets Templates",
         tags=["finance bundle", "debt payoff", "net worth tracker", "budget bundle", "money reset", "financial planner", "savings challenge", "bill tracker", "excel templates", "google sheets", "debt snowball", "net budget", "money goals"],
         list_price=14.99, sale_price=10.0,
         desc="", note="'22 Trackers' is the pitch and it was buried mid-title. Front it. Consider renaming as a January 'money reset kit'."),
    dict(id="S10", prio="PRIORITY", new=False, light=True, k="wedding planner spreadsheet",
         window='Jan 2 – Feb 14 (proposal-to-booking season) + May – Jun (summer-bride catch-up)',
         title="Wedding Planner Spreadsheet, 52 Tabs for Budget, Guest List, Seating Chart and Vendor Tracker, Excel Google Sheets Template",
         tags=["wedding planner", "wedding budget", "guest list", "seating chart", "vendor tracker", "wedding spreadsheet", "bridal budget", "rsvp tracker", "wedding checklist", "excel template", "google sheets", "wedding planning", "bride to be"],
         list_price=18.99, sale_price=13.0,
         desc="", note="A 104-review seller charges $13.71 here; you had $11.99. '52 Tabs' moves to the front - that number is the differentiation."),
    dict(id="S11", prio="MAYBE", new=False, light=True, k="budget spreadsheet bundle excel",
         window='Dec 20 – Jan 31 primary; 30% off Black Friday secondary; nothing else, it sells year-round',
         title="Budget Spreadsheet Bundle, 50 Finance Templates for Excel and Google Sheets, Bill, Debt and Savings Tracker Mega Pack",
         tags=["budget bundle", "excel templates", "bill tracker", "debt tracker", "savings tracker", "finance bundle", "budget planner", "money spreadsheet", "google sheets", "planner bundle", "net worth", "expense log", "mega pack"],
         list_price=39.99, sale_price=28.0,
         desc="", note="38 listings, band $9-37. Your high-AOV anchor. Add a dated '2027 edition' each November - that converts the same file twice."),
    dict(id="S14", prio="SHELVE", new=False, light=True, k="travel planner spreadsheet itinerary",
         window='May 1 – Jun 30 + Nov 15 – Dec 20 (summer planning and winter-escape booking)',
         title="Travel Planner Spreadsheet, Trip Itinerary, Vacation Budget and Packing List Template, Google Sheets and Excel Download",
         tags=["travel planner", "trip itinerary", "vacation budget", "packing list", "travel spreadsheet", "road trip planner", "holiday planner", "travel organizer", "google sheets", "excel template", "family vacation", "bucket list", "travel journal"],
         list_price=11.99, sale_price=8.0,
         desc="", note="Weak $8 ceiling, 29 listings. Keep; do not build more travel SKUs."),
    dict(id="S15", prio="MAYBE", new=False, light=True, k="family budget spreadsheet dashboard",
         window='Jan 2 – Jan 31 (this keyword belongs to January, not to Q4)',
         title="Family Budget Spreadsheet, Household Finance Dashboard With Paycheck Planner, Debt and Net Worth Tracker, Google Sheets",
         tags=["family budget", "household finance", "paycheck budget", "bill calendar", "debt tracker", "net worth sheet", "couple budget", "excel budget", "google sheets", "monthly budget", "savings plan", "expense tracker", "money budget"],
         list_price=13.99, sale_price=9.74,
         desc="", note="Most crowded keyword you own (46 listings, 2,400 median). Add dark mode + a 15s screen-record or it stays invisible in that grid."),
    dict(id="K1", prio="KILL", new=False, light=True, k="adult coloring pages line art",
         title="",
         tags=[],
         list_price=2.00, sale_price=1.5,
         desc="", note="ARCHIVE. Largest observed incumbents in the cluster: 5.9k at $1.20, 4.3k at $5.50, three separate 3.1k listings at $1.85/$1.87/$3.70. There is no path to $1,000 from a $2 ceiling; reuse the art as a free bonus inside a paid planner."),
    dict(id="K2", prio="KILL", new=False, light=True, k="alphabet coloring pages printable",
         title="",
         tags=[],
         list_price=2.00, sale_price=1.5,
         desc="", note="ARCHIVE (same reason as K1). Preschool *activity* pages price 2-3x colouring pages - that is the salvageable half of this cluster."),
    dict(id="K3", prio="KILL", new=False, light=True, k="vehicles coloring pages for kids",
         title="",
         tags=[],
         list_price=2.00, sale_price=1.5,
         desc="", note="ARCHIVE (same reason as K1)."),
    dict(id="K4", prio="MAYBE", new=False, light=True, k="dot marker preschool printables",
         window='Aug 1 – Sep 15 (back-to-school) + Jan 5 – Jan 20 (parents restarting routines)',
         title="Alphabet Dot Marker Activity Pages, Do A Dot Printable Worksheets, Preschool Letter Recognition PDF, 26 Pages Instant Download",
         tags=["dot marker pages", "do a dot printable", "letter recognition", "preschool worksheet", "alphabet activity", "kindergarten prep", "toddler learning", "printable activity", "homeschool admin", "early literacy", "preschool printables", "abc worksheet", "learning at home"],
         list_price=4.99, sale_price=3.0,
         desc="", note="The one education SKU worth keeping: activity/educational pages carry a real ceiling where colouring does not. Rename the SKU from 'colouring' to 'activity/workbook' language and it stops competing with the $2 cluster entirely."),
    dict(id="N3", prio="DO NOW", new=True, light=True, k="crochet christmas stocking pattern",
         title="Crochet Mini Stocking Pattern, 24 Christmas Stockings for an Advent Garland, Gift Tag Loop, Beginner Friendly PDF Download",
         tags=["mini stockings", "christmas stocking", "crochet stocking pdf", "advent garland", "stocking ornament", "24 stockings", "christmas crochet", "amigurumi christmas", "beginner crochet", "gift tag loop", "crochet pattern pdf", "holiday decor", "xmas stocking"],
         window="Oct 15 \u2013 Dec 12 (an advent piece has to be finished before December 1, so buyers shop in October)",
         list_price=9.99, sale_price=6.50,
         desc="", note=""),
    dict(id="N4", prio="DO NOW", new=True, light=True, k="goat crochet pattern amigurumi",
         title="Year of the Goat Crochet Pattern 2027, Amigurumi Fire Goat and Lamb, Lunar New Year Plushie PDF, Beginner Friendly Download",
         tags=["goat crochet pattern", "amigurumi goat", "year of the goat", "lunar new year", "chinese new year", "crochet lamb", "zodiac amigurumi", "beginner crochet", "crochet pattern pdf", "spring farm animal", "red and gold", "crochet plushie", "easter lamb"],
         window="Dec 1 \u2013 Feb 20, 2027 (CNY Feb 6, Lantern Festival Feb 20), then relist the same file as an Easter lamb in March",
         list_price=6.99, sale_price=5.00,
         desc="", note=""),
    dict(id="N7", prio="PRIORITY", new=True, light=True, k="christmas card list spreadsheet",
         title="Christmas Card List Spreadsheet, Address Book and Mailing Tracker With Printable Labels, Postmark Deadline Planner, Excel",
         tags=["christmas card list", "address tracker", "card tracker", "christmas planner", "mailing deadline", "address labels", "holiday spreadsheet", "thank you tracker", "excel template", "google sheets", "christmas budget", "family newsletter", "small business"],
         window="Nov 1 \u2013 Dec 10 only (this dies on December 12; that searcher needs a different product)",
         list_price=6.99, sale_price=4.50,
         desc="", note=""),
    dict(id="N8", prio="MAYBE", new=True, light=True, k="secret santa gift exchange spreadsheet",
         title="Secret Santa Spreadsheet, Name Draw Generator With Budget Rules and Exclusions, White Elephant Party Tracker, Excel Sheets",
         tags=["secret santa", "secret santa game", "white elephant", "gift exchange", "party planner", "office party", "gift tracker", "santa spreadsheet", "christmas game", "group gift", "name draw", "excel template", "google sheets"],
         window="Nov 10 \u2013 Dec 15 (office-party season; buyers need it the week the party is set)",
         list_price=6.99, sale_price=5.00,
         desc="", note=""),
    dict(id="N9", prio="DO NOW", new=True, light=True, k="new year financial reset spreadsheet",
         title="New Year Financial Reset Spreadsheet, 12-Month Money Audit, Budget, Debt Payoff and Net Worth Planner, Google Sheets Excel",
         tags=["new year reset", "financial reset", "money audit", "budget spreadsheet", "debt payoff plan", "net worth tracker", "savings goals", "annual budget", "money goals", "excel template", "google sheets", "quarterly review", "2027 planner"],
         window="Dec 26 \u2013 Jan 31 hard window (publish Dec 26; the demand is January and it is gone by February)",
         list_price=12.99, sale_price=9.00,
         desc="", note=""),
    dict(id="S16", prio="PRIORITY", new=False, light=True, k="rental property management spreadsheet",
         title="Rental Property Management Spreadsheet, Rent Ledger, Maintenance Requests and Tenant Tracker, Landlord Excel Google Sheets",
         tags=["rental property mgmt", "rent ledger", "tenant tracker", "landlord spreadsheet", "maintenance log", "rental income", "property manager", "lease tracker", "excel template", "google sheets", "security deposit", "rent increase", "landlord tools"],
         window="Jan 2 \u2013 Jan 31 + Jul 1 \u2013 Aug 15 (lease-renewal and fall-move-in season)",
         list_price=15.99, sale_price=11.99,
         desc="", note="SPLIT THESE, DO NOT MERGE. You run 'Rental Property Analyzer' at $8.99 and 'Rental Property Management' at $8.99 - two listings, half the reviews each, competing with each other in your own shop. Analysis (pre-purchase) and management (ongoing) are genuinely different products, so the right move is: keep BOTH but split them by intent, and put a cross-link in each description. Do not merge if the two files really differ - merge only if one is a subset of the other."),
    dict(id="K5", prio="KILL", new=False, light=True, k="motherhood coloring book pdf",
         title="",
         tags=["", "", "", "", "", "", "", "", "", "", "", "", ""],
         list_price=2.00, sale_price=1.50,
         desc="", note="ARCHIVE with the rest of the colouring cluster. Worth one sentence of nuance: 'mum life' humour colouring is the only flavour of this cluster that ever escapes the $2 floor, because it is bought as a gift for a specific person rather than as filler. If you ever revisit it, it needs real page photos and a gift angle - not a keyword change."),
]

LISTINGS = LISTINGS + LIGHT

# ---------------------------------------------------------------------------
# Merge the long-form copy in from listings_copy.py. Rows that gain a real
# description stop being "light" and are validated as finished listings; the
# three archive rows have no title, so they stay notes-only on purpose.
# ---------------------------------------------------------------------------
for _l in LISTINGS:
    _c = COPY.get(_l["id"])
    if not _c:
        continue
    if _c.get("desc") and _l["title"]:
        _l["desc"] = _c["desc"]
        _l["light"] = False
    for _k in ("obs", "why", "verify"):
        if _k in _c:
            _l[_k] = _c[_k]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def check(l: dict):
    """-> (errors that block you, warnings that are judgement calls)."""
    errs, warn = [], []
    t = l["title"]
    if l.get("light"):
        # Archive row (no title): the note IS the deliverable.
        # Anything else that is still light means copy failed to merge.
        if not t:
            return [], [l["note"]]
        if not l.get("desc"):
            return [f"light row with a title but no description - copy merge failed for {l['id']}"], []
        # Copy-sheet row: only Etsy's hard field limits are gradeable. An empty
        # title is deliberate - it means "archive this listing", and the note is the output.
        real = [x for x in l["tags"] if x]
        out = []
        if len(t) > TITLE_MAX: out.append(f"title {len(t)} > {TITLE_MAX} chars")
        if len(real) != TAG_COUNT: out.append(f"{len(real)} usable tags, Etsy gives {TAG_COUNT}")
        for tg in real:
            if len(tg) > TAG_MAX: out.append(f"tag too long ({len(tg)}): '{tg}'")
            if tg != tg.lower(): out.append(f"tag not lowercase: '{tg}'")
            if tg != tg.strip(): out.append(f"tag has stray whitespace: '{tg}'")
        if len(set(real)) != len(real):
            out.append(f"duplicate tags: {sorted({x for x in real if real.count(x)>1})}")
        off = 1 - l["sale_price"]/l["list_price"] if l["list_price"] else 0
        if off < 0.24: out.append(f"badge only {off*100:.0f}% off")
        return out, [l["note"]]
    if len(t) > TITLE_MAX:
        errs.append(f"title {len(t)} chars, limit {TITLE_MAX} (over by {len(t)-TITLE_MAX})")
    if not t[0].isupper():
        errs.append("title should start capitalised")
    if t.count(",") < 2:
        errs.append("title has <2 comma-separated phrase clusters")
    if l["k"].split()[0] not in mobile_slice(t).lower():
        warn.append(f"head noun of '{l['k']}' is not in the mobile-visible title slice")

    tags = l["tags"]
    if len(tags) != TAG_COUNT:
        errs.append(f"{len(tags)} tags, Etsy gives exactly {TAG_COUNT}")
    for tg in tags:
        if len(tg) > TAG_MAX:
            errs.append(f"tag too long ({len(tg)}): '{tg}' — Etsy max {TAG_MAX}")
        if tg != tg.lower():
            errs.append(f"tag not lowercase: '{tg}'")
        if len(tg) < 4:
            errs.append(f"tag too generic/short: '{tg}'")
    tags = [x for x in l["tags"] if x]
    low = [x.lower() for x in tags]
    if len(set(low)) != len(low):
        dupes = sorted({x for x in low if low.count(x) > 1})
        errs.append(f"duplicate tags: {dupes}")
    warn = []
    for tg in low:
        if tg == l["k"]:
            warn.append(f"tag '{tg}' duplicates the primary keyword phrase (harmless, just redundant)")


    d = l["desc"]
    words = len(d.split())
    if not (230 <= words <= 460):
        errs.append(f"description {words} words — target 250-400")
    if len(d) < 400:
        errs.append("description too short to index")
    if l["sale_price"] >= l["list_price"]:
        errs.append("sale price must be below list price")
    off = 1 - l["sale_price"] / l["list_price"] if l["list_price"] else 0
    if off < 0.25:
        errs.append(f"badge is only {off*100:.0f}% off — page 1 shows 30-75%; under 25% the strikethrough is invisible")
    if off > 0.55:
        errs.append(f"{off*100:.0f}% off reads as desperation and traps your price floor")
    return errs, warn


def mobile_slice(t: str) -> str:
    return t[:MOBILE_VISIBLE] if len(t) <= MOBILE_VISIBLE else t[:MOBILE_VISIBLE].rsplit(" ", 1)[0] + "…"


def emit():
    errs_total = 0
    print(f"{'ID':<5}{'TITLE':>6}{'TAGS':>6}{'WORDS':>7}{'PRICE':>9}  STATUS")
    print("-" * 78)
    for l in LISTINGS:
        e, w = check(l)
        if e:
            errs_total += len(e)
            print(f"{l['id']:<5}  FAIL  {l['title'][:40]}")
            for x in e:
                print("      ✗", x)
        else:
            print(f"{l['id']:<5}{len(l['title']):>6}{len(l['tags']):>6}{len(l['desc'].split()):>7}"
                  f"{'$'+format(l['sale_price'],'.2f'):>9}  ok")
        for x in w:
            print("      ·", x)

    with open("Q4_LISTINGS.md", "w", encoding="utf-8") as f:
        f.write("# NovalityStore — Q4 Listing Pack\n\n")
        f.write("Every field validated against Etsy's real limits. Tags are lowercase and ≤20 chars; titles ≤140.\n")
        f.write("`PASTE THIS INTO THE LISTING EDITOR` sections are literal — no editing needed.\n\n")
        n_v = sum(1 for x in LISTINGS if x.get("verify"))
        n_items = sum(len(x.get("verify", [])) for x in LISTINGS)
        f.write(f"**Before you paste:** {n_items} product specifics across {n_v} listings were inferred from "
                f"your listing titles and market research, not from your PDFs and spreadsheets. Each block "
                f"lists exactly what to confirm. Anything you cannot verify, delete the sentence — an "
                f"over-promised spec is how a 1-star gets written.\n\n---\n\n")
        order = {"DO NOW": 0, "PRIORITY": 1, "MAYBE": 2}
        for l in sorted(LISTINGS, key=lambda x: (order.get(x["prio"], 3), x["id"])):
            new = " — **NEW BUILD (does not exist yet)**" if l.get("new") else ""
            f.write(f"## {l['id']} · {l['prio']}{new}\n\n")
            if not l["title"]:                                  # retire-this-listing row
                f.write("**Action: archive. No copy is being written for this one, on purpose.**\n\n")
                f.write(f"{l.get('note','')}\n\n")
                f.write(f"Current price: ${l['sale_price']:.2f} realized → ${l['net_per_sale'] if 'net_per_sale' in l else l['sale_price']-0.45-0.095*l['sale_price']:.2f} net. "
                        "Archive (don't delete, you keep any history), and reuse the artwork as a free "
                        "bonus inside a paid listing where the ceiling is real.\n\n---\n\n")
                continue
            f.write(f"**Target keyword:** `{l['k']}`\n\n")
            if l.get("note"):
                f.write(f"**⚠ Read first:** {l['note']}\n\n")
            if not l.get("light"):
                f.write(f"**Why this listing is worth the hour:** {l['why']}\n\n")
                f.write(f"**Market evidence:** {l['obs']}\n\n")
            f.write("### PASTE THIS INTO THE LISTING EDITOR\n\n")
            f.write(f"**Title** ({len(l['title'])}/140 chars)\n\n```\n{l['title']}\n```\n\n")
            f.write(f"*What a mobile shopper sees before truncation:* `{mobile_slice(l['title'])}`\n\n")
            f.write("**Tags** (13, each ≤20 chars)\n\n```\n" + "\n".join(l["tags"]) + "\n```\n\n")
            win = l.get("window", "")

            if win:
                f.write(f"**Run the sale:** {win}\n\n")
            f.write(f"**Pricing**\n\n| field | value |\n|---|---|\n| List price (the anchor) | ${l['list_price']:.2f} |\n"
                    f"| Sale price | ${l['sale_price']:.2f} ({round((1-l['sale_price']/l['list_price'])*100)}% off) |\n"
                    f"| Net per sale after Etsy fees | ${l['sale_price'] - (0.20+0.065*l['sale_price']+0.03*l['sale_price']+0.25):.2f} |\n\n")
            if l.get("verify"):
                f.write("**Verify against your file before publishing**\n\n")
                for v in l["verify"]:
                    f.write(f"- [ ] {v}\n")
                f.write("\n")
            f.write("**Description**\n\n```\n" + l["desc"].strip() + "\n```\n\n---\n\n")

    with open("q4_listings.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "priority", "new_build", "primary_keyword", "title", "title_chars",
                    "mobile_visible", "tags_pipe_separated", "tag_count", "list_price", "sale_price",
                    "discount_pct", "net_per_sale", "desc_words", "evidence", "rationale",
                    "description", "verify_before_publishing"])
        for l in LISTINGS:
            net = round(l["sale_price"] - (0.20 + 0.065*l["sale_price"] + 0.03*l["sale_price"] + 0.25), 2)
            w.writerow([l["id"], l["prio"], "yes" if l.get("new") else "", l["k"], l["title"],
                        len(l["title"]), mobile_slice(l["title"]), "|".join(l["tags"]), len(l["tags"]),
                        f"{l.get('list_price',0):.2f}", f"{l.get('sale_price',0):.2f}",
                        round((1-l["sale_price"]/max(l["list_price"],0.01))*100), net, len(l["desc"].split()),
                        l.get("obs",""), l.get("why") or l.get("note",""),
                        (l.get("desc") or "").strip().replace("\n", " ¶ "),
                        " ; ".join(l.get("verify", []))])

    print("-" * 78)
    print(f"{len(LISTINGS)} listings · {errs_total} blocking problems · 0 = safe to paste into Etsy")
    if "--check" in sys.argv:
        sys.exit(1 if errs_total else 0)
    print("Wrote Q4_LISTINGS.md  +  q4_listings.csv")


if __name__ == "__main__":
    emit()
    sys.exit(0)
