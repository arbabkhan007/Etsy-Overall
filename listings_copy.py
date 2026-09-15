"""
NovalityStore — long-form description copy (all 33 live listings)
=================================================================

Merged into `listing_pack.py` at import. Keeps the short fields (title, tags,
price) in one file and the prose in another, because the prose is what you will
revisit every time Etsy's limits or your files change.

!! THE `verify` LISTS ARE NOT OPTIONAL READING !!
Every description below was written from your listing titles and market
research — NOT from your actual PDFs and .xlsx files. So the structure, the
benefits and the promises are mine, and the *numbers* (page counts, sizes,
yardage, tab counts, hook sizes) are plausible placeholders. Before you paste,
confirm each `verify` item against your own file or delete the sentence.
A description that promises 9 pages and ships 6 is how the last 1-star happened.

Shape convention (from Q4_PLAYBOOK.md §4.3):
  crochet     hook 2 lines → WHAT YOU GET → SKILL LEVEL → MATERIALS → MADE FOR
              → INSTANT DOWNLOAD → TERMS → SUPPORT
  spreadsheet hook 2 lines → WHAT IT DOES → WHY IT IS DIFFERENT → MADE FOR
              → HOW IT WORKS → TERMS → SUPPORT
"""

COPY = {

# ══════════════════════════════════════════════════════════════════════════
# CROCHET
# ══════════════════════════════════════════════════════════════════════════
"C4": dict(
 obs="Cluster has ~45 competing listings and a 43k-review Christmas ebook at $13.92 plus a 3.8k granny-square at $10.20. $5 is the realistic realised price for a single one-piece tree.",
 why="Keep it, raise it to $5 and make it the free-feeling third item in ornament bundles. Do not build a second tree pattern.",
 verify=["page count (I wrote 9)", "the three finished sizes 6/10/14 in", "approx 180 yds green for the 10 in tree",
         "that a separate-topper variant actually exists in your PDF", "US + UK terms both present"],
 desc="""One tree, one piece, nothing to sew together.

A crochet PDF pattern for a bobble Christmas tree worked in a continuous spiral from trunk to star, so there are no tiers to stack and no seams to hide. The bobbles do the decorating — they catch light like baubles, which is why the finished tree photographs better than it took to make.

WHAT YOU GET
- 9-page illustrated PDF, US and UK terms
- 3 finished heights from the same construction: 6 in tabletop, 10 in mantel, 14 in floor-corner
- The star worked in-line at the top, plus a separate detachable topper version if you prefer one
- The bobble written out stitch-by-stitch, with a photo of right-vs-wrong at the three places people drift
- Base stiffening options: cardboard disc, floral-wire ring, or nothing at all
- Yardage table per size so you can check your stash before you start

SKILL LEVEL
Beginner. Magic ring, single crochet, increase, decrease, front-post bobble, and one colour change from green to brown at the trunk. If you can make a ball, you can make this tree.

MATERIALS (10 in tree)
- Worsted 4 green, approx 180 yds, plus small scraps in brown and gold
- 3.5mm hook, fibre fill, yarn needle; optional 6 in cardboard disc for the base

MADE FOR
Tablescapes, dorm rooms, office desks, apartments where a full tree is absurd, and a row of them down a staircase. Also genuinely good craft-fair stock: one takes about four hours and sells in under a week in December.

INSTANT DOWNLOAD
Files unlock the moment payment confirms, on any device.

TERMS
Personal use of the pattern file. Sell your trees anywhere, in any quantity. Please do not resell, share, redistribute or reproduce the PDF, and do not use my photographs as your own listing images.

SUPPORT
If your bobbles start pulling the fabric inwards, send a photo of that round and I will tell you which stitch you are actually into. Most replies go out the same day."""),

"C7": dict(
 obs="No-sew amigurumi cluster: a 17.9k-review seller at $6.39 and a 2.4k-review duck at $2.01 with 75% off. Listings with 300-950 reviews realise $3.75-$5.99. Your $2.62 sits below every comparable listing and reads as a bad pattern, not a bargain.",
 why="Raise to $3.50 realised. This is a gift item, and $3.50 is still the second-cheapest thing on page 1.",
 verify=["that your pattern actually includes the orange-on-head detail before keeping it in the title",
         "finished height (I wrote 5.5 in)", "page count (I wrote 10)", "approx 120 yds for the body",
         "that no sewing is genuinely required"],
 desc="""The internet's calmest animal, made in an evening, with nothing to sew.

A no-sew capybara crochet PDF pattern — body, ears, nose and feet all worked continuously, so there is no appliqué to stitch on and no asymmetric ears to fix at the end.

WHAT YOU GET
- 10-page illustrated PDF, US and UK terms
- Two sizes from one construction: 5.5 in standard plush, 3 in keychain charm
- The no-sew ear method worked in place (this is the part people get wrong from other patterns)
- Optional orange to balance on the head, worked separately in 15 minutes — because of course
- Closed-base instructions so it sits properly on a shelf instead of flopping
- Yardage and fill table, plus a two-page colour variation list (classic brown, grey, strawberry)

SKILL LEVEL
Beginner. Magic ring, single crochet, sc2tog, increase, colour change, stuff and close. Six stitches, no sewing needle required beyond weaving in one end.

MATERIALS (5.5 in capybara)
- Worsted 4 in a brown or grey tone, approx 120 yds, plus a thumbnail of orange if you're doing the fruit
- 3.25mm hook, fibre fill, darning needle, 1 safety eye substitute (embroidered, so it's baby-safe)

MADE FOR
Gifts for people who own too much already, teen birthdays, teacher thank-yous, and anyone who has been put off amigurumi by the finishing stage. It's also the fastest thing in your shop to crochet start-to-finish — about three hours.

INSTANT DOWNLOAD
Your files are waiting the moment payment confirms — phone, tablet or laptop, print it if you prefer paper.

TERMS
Personal use of the pattern file. Sell your finished capybaras freely, in any quantity, anywhere. Do not resell, share, redistribute or reproduce the PDF, and please don't use my images as your listing photos.

SUPPORT
If your capybara looks more like a loaf than a capybara, send me a photo — it is nearly always the same two rounds, and I will tell you which. Same-day replies."""),

"C8": dict(
 obs="This is the listing that earned the 1-star about render images. Same cluster realises $3.75-$5.99; you're at $2.62. Fix trust first, price second.",
 why="Sequence matters: real photo of the actual gills and arms, a v1.1 note in the description, THEN reprice. Repricing a listing buyers don't trust just moves the distrust.",
 verify=["that the v1.1 arm/gill rewrite actually exists before claiming it", "finished length (I wrote 7 in)",
         "page count (I wrote 12)", "approx 140 yds main colour", "the standing-gill method you actually used"],
 desc="""A no-sew axolotl whose arms and gills are worked as part of the body — and a pattern that got revised because a buyer told me the first version didn't match its own photo.

That review was right. The gills and limbs in the original were where the render oversold the result, so they are now written stitch-by-stitch with photos at every stage, and the pattern is on v1.1. If you bought earlier, the update is free — message me.

WHAT YOU GET
- 12-page illustrated PDF, US and UK terms
- v1.1 arm and leg construction, worked in continuous rounds (no sewing on, no stitching into place)
- Six standing external gills per side, with the wire-free method that keeps them upright in photos
- 3 sizes: 4 in charm, 7 in plush, 10 in pillow-friend
- Tail-fin instructions that stop the fin from rolling
- Colour guide: wild type, leucistic pink, gold albino, and the dark "blue" morph

SKILL LEVEL
Beginner-plus. Magic ring, single crochet, increase, sc2tog, working a front-loop ridge for the fin, colour change. Nothing is sewn afterwards.

MATERIALS (7 in axolotl)
- Worsted 4 main colour, approx 140 yds; small amount in pink for gills
- 3.25mm hook, fibre fill, yarn needle. No safety eyes — embroidered face, so it's safe for a toddler's shelf.

MADE FOR
Aquarium people, kawaii plushie collectors, teachers' classroom reading buddies, and anyone who has abandoned an amigurumi at the sewing stage. One takes about four hours.

INSTANT DOWNLOAD
Files unlock as soon as payment confirms.

TERMS
Personal use of the pattern. Sell finished axolotls anywhere, in any quantity. Do not resell, share or reproduce the PDF, and don't use my photographs as your listing images.

SUPPORT
Send me a photo of a floppy gill or a lumpy arm and I will tell you what it needs. I answer fast, and I would rather fix your round 8 than read another honest 1-star."""),

"C9": dict(
 obs="Loaf-cat is a stable micro-niche; comparable no-sew plushies with 300-1,500 reviews realise $3-$5.",
 why="$3 keeps it a volume listing. The real upside is bundling three cats into a 'cat loaf family' at $6 - same work, double price.",
 verify=["finished dimensions (I wrote 3.5 x 5 in)", "page count (I wrote 8)", "approx 90 yds",
         "whether your pattern includes the tucked-paw variant", "embroidered-vs-safety-eye detail"],
 desc="""A cat, in a loaf, in about two hours — with nothing to sew on.

A no-sew amigurumi loaf cat crochet PDF pattern. Ears go in as you work, the tail comes out of the back without attaching, and the paws are tucked by shaping alone. It is the smallest, fastest thing in the shop and the one people make three of.

WHAT YOU GET
- 8-page illustrated PDF, US and UK terms
- One size: 3.5 x 5 in — the exact footprint of a real cat loaf
- In-the-round ear method, plus a folded-ear variation
- Tail worked continuously from the body (no stuffing a tube on afterwards)
- Tucked-paw shaping instructions
- Colour chart: tuxedo, ginger, grey tabby, calico, and the black one with the yellow eyes
- Bonus: same body scaled to a 2 in keychain in three fewer rounds

SKILL LEVEL
Absolute beginner, genuinely. Magic ring, single crochet, increase, decrease. Four moves. If you have ever thought "I'd try amigurumi if it weren't for the sewing", this is that.

MATERIALS
- Worsted 4, approx 90 yds total across colours (a single small skein of two colours works)
- 3.25mm hook, little fill, tapestry needle for the face only

MADE FOR
Gifts for cat people who have the photos and the mugs already, desk companions, market stock you can produce at volume in a weekend, and teaching one new person how to amigurumi without losing them at round six.

INSTANT DOWNLOAD
Unlocks the moment your payment clears.

TERMS
Personal use of the pattern file. Sell your loaves freely, anywhere, in any numbers. Do not resell, share, or reproduce the PDF, and please don't use my images as your own listing photos.

SUPPORT
If your cat has come out looking like a bagel, send a photo — it is the ear rounds nine times out of ten, and I will say which."""),

"C10": dict(
 obs="Dragon plushies with 130-1,500 reviews realise $3.29-$7. Your $7 list / $5.25 realised is at market; stop discounting through it.",
 why="Price is already right. The gap is the title: say what the wings do (fold, or bolt upright) because that's the #1 dragon-pattern complaint.",
 verify=["wings method (I wrote fold-flat)", "finished wingspan (I wrote 7 in)", "page count (I wrote 14)",
         "spike material (I wrote felt, not wire)", "approx 200 yds main colour"],
 desc="""A baby dragon that fits in a palm, with wings that actually fold.

An amigurumi baby dragon crochet PDF pattern — chunky body, oversized head, and fold-flat wings that tuck against the body instead of sticking out and getting crushed in a gift box.

WHAT YOU GET
- 14-page illustrated PDF, US and UK terms
- One finished size: 6 in tall, 7 in wingspan, sized for a child's hand and an adult's shelf
- Fold-flat wing construction (no wire armature, no bulging seams) — this is the section the pattern exists for
- 14 back spikes applied in a charted placement so they aren't randomly scattered
- Horn and tail-tip options: felt, crochet-only, or omitted entirely for under-3s
- Six colourways: forest, ember, ice, night, gold, and the grey-one-with-pink-belly
- Stuffing-density notes, because a dragon is 80% about how firm the chest is

SKILL LEVEL
Confident beginner. Magic ring, single crochet, half-double, increase, decrease, working both loops for the wing fold. No sewing beyond spike placement.

MATERIALS
- Worsted 4 main colour approx 200 yds; accent for belly and spikes
- 3.5mm hook, fibre fill, yarn needle, small felt scraps if you use horns

MADE FOR
Fantasy kids, D&D friends who want something on the desk that isn't a dice tower, baby-shower-for-the-cool-aunt gifts, and makers building a whole clutch of dragons in one litter's worth of colours.

INSTANT DOWNLOAD
Files unlock as soon as payment confirms, so you can start tonight.

TERMS
Personal use of the pattern file. Sell finished dragons anywhere you like. Do not resell, share, redistribute or reproduce the PDF, and do not use my photographs as your listing images.

SUPPORT
Wing won't fold right, or spikes sitting at odd angles? Send a photo of the row you're on. I will tell you which round drifted and how to bring it back."""),

"C11": dict(
 obs="Highland cow is evergreen giftable; adjacent no-sew plushies with 300-950 reviews realise $4.50-$5.99. Your $5.25 realised is right.",
 why="Cheapest new SKU available to you: a palm-sized variant is one scaling note away from this same body pattern, and 'highland cow' spawns gift, nursery and farmhouse buyers.",
 verify=["finished height (I wrote 6 in)", "page count (I wrote 13)", "fringe method (I wrote crochet fringe, not cut yarn)",
         "horn material (I wrote pipe cleaners)", "approx 150 yds for the body"],
 desc="""The shaggy fringe is the whole trick, and it's the part other patterns get wrong.

A highland cow amigurumi crochet PDF pattern with a proper crocheted fringe — not cut yarn glued on — so the coat looks like a coat after the third child has handled it.

WHAT YOU GET
- 13-page illustrated PDF, US and UK terms
- Two sizes: 6 in standard cow, 3 in palm cow for a bag clip
- Crochet fringe method (rows of loops you cut yourself, denser than a purchased version and permanently attached)
- Horns with a bendable core so you can point them out or tuck them down
- Wide fluffy fringe over the eyes, with the two-row version that lets you make it 'see'
- Four colourways: ginger, brindle, black, and the pale dun
- Farm bonus: same body scaled to a sheep and a goat in the last two pages

SKILL LEVEL
Confident beginner. Magic ring, single crochet, increase, decrease, back-loop-only rows for the fringe base, and cutting loops — which is the only unusual thing here.

MATERIALS
- Worsted 4 in ginger/brindle approx 150 yds; small cream for the underbelly
- 3.5mm hook, fibre fill, 2 short pipe cleaners or wire for horns, yarn needle

MADE FOR
Nursery shelves, farmhouse and Scandi interiors, gifts for people whose entire personality is highland cows, and market tables in October. The fringe is what makes people stop and pick it up.

INSTANT DOWNLOAD
Available the second your payment is confirmed.

TERMS
Personal use of the PDF. Sell your cattle freely, in any quantity, anywhere. Do not resell, share, redistribute or reproduce the pattern file, and don't use my images as your listing photos.

SUPPORT
Fringe too sparse, too long, or all on one side? Send a photo. There are exactly three ways this goes wrong and I will tell you which one you're in."""),

"C12": dict(
 obs="Halloween bundles with 150-250 reviews realise $3-$6; a 3-piece bundle at $6 is mid-market, not aggressive.",
 why="Timing is everything: this peaks Sep 15-Oct 20. Publishing the rewrite this week matters more than any wording in it.",
 verify=["that all three patterns exist in one PDF", "page count (I wrote 15)", "ornament sizes (I wrote 3 in each)",
         "that a keychain version is actually included", "approx 130 yds across all three"],
 desc="""Three Halloween ornaments, one bundle, one evening each.

A 3-in-1 Halloween crochet pattern bundle: ghost, pumpkin and bat, sized to hang on a branch, a doorframe, or a kid's backpack without looking like a sad lump. Buying them together costs less than one on its own, which is the entire point of a bundle.

WHAT YOU GET
- 15-page illustrated PDF, US and UK terms, all three patterns in one file
- Ghost: 3.5 in, with the weighted-bottom trick so it hangs straight instead of spinning upside down
- Pumpkin: 3 in, with a stem that stays upright and ribs that don't pucker
- Bat: 4 in wingspan, fold-flat wings so it survives a bag
- Each ornament also documented as a keychain/charm version with a shorter tail or no loop
- Yardage table for the whole set — three ornaments from about 130 yds of scraps
- A one-page assembly and blocking sheet so the set matches

SKILL LEVEL
Beginner. Magic ring, single crochet, half double crochet for the bat wings, increase, decrease, stuff, close, and one set of colour changes for the pumpkin ribs. No sewing.

MATERIALS (all three)
- Worsted 4: white/cream, orange, black — approx 130 yds total, or split stash
- 3.5mm hook, small amount of fill, 3 hanging loops or keychain rings

MADE FOR
Classroom door decorations, office desks that turn into Halloween in October, trick-or-treat bucket fillers that aren't plastic, craft-group swaps, and the maker who wants 20 ornaments for a market stall in a weekend.

INSTANT DOWNLOAD
Files unlock the moment payment confirms — which matters, because Halloween is a deadline and this is the pattern you can still finish in time.

TERMS
Personal use of the pattern file. Sell your ghosts, pumpkins and bats anywhere, in any quantity. Do not resell, share, redistribute or reproduce the PDF, and please do not use my photographs as your listing images.

SUPPORT
Bat wings not folding symmetrically? Ghost hanging crooked? Send a photo and I'll tell you the round. Fast replies, usually same day."""),

"C13": dict(
 obs="Turtle charms and keychains realise $2.50-$4 with 130-880 reviews. $3 keeps it impulsive; the '1 hour' claim is what justifies not dropping to $2.",
 why="The hook is TIME, not craft. Nobody searching 'crochet keychain pattern' wants a project — they want a make between episodes. Say so in the title (done) and price at the impulse threshold.",
 verify=["finished size (I wrote 2 in)", "that the shell is genuinely one piece", "approx 35 yds",
         "the time claim - measure your own sample before promising an hour", "keychain ring attachment method"],
 desc="""One hour, one scrap of yarn, one sea turtle for your bag.

A no-sew amigurumi sea turtle crochet PDF pattern built as a fast make: a 2 inch shell and body in one piece, four flippers worked in place, and a keychain loop you finish inside the last round. It is the pattern you start after dinner and wear out tomorrow.

WHAT YOU GET
- 6-page illustrated PDF, US and UK terms — deliberately short, because a 1-hour make shouldn't need a manual
- One finished size: 2 in shell, roughly 3 in nose to tail
- The no-sew flipper method (worked as an extension of the body, not sewn on)
- Two finishes: flat keychain charm, and lightly-stuffed plush version for a pencil case
- Shell pattern options: plain, honeycomb, and the green-and-black turtle with contrast scutes
- Two yarn-weight tables — worsted for the one-hour version, DK for a 1.5 in jewellery-scale one
- How to attach a jump ring so it doesn't tear out in a month

SKILL LEVEL
Total beginner. Magic ring, single crochet, increase, decrease. That is the whole pattern.

MATERIALS
- Under 40 yds worsted 4 — a genuine stash-buster, made from the ends of other projects
- 3.25mm hook, a pinch of fill (or none), 1 keychain ring or 5mm jump ring

MADE FOR
Bulk making: school fundraiser tables, market stalls, party favours, friend-of-a-friend gifts, and teacher appreciation by the dozen. Also a first project for someone who has never held a hook, because it ends before frustration starts.

INSTANT DOWNLOAD
Unlock the second payment clears. Crochet it tonight.

TERMS
Personal use of the pattern file. Sell as many finished turtles as you can crochet, anywhere. Do not resell, share, or reproduce the PDF, and please don't use my images as your own.

SUPPORT
If yours comes out looking less turtle and more pancake, send a photo — it is the flipper rounds, and there is a two-minute fix."""),

"C14": dict(
 obs="Baby lovey/blanket patterns with 200-5,300 reviews realise $2.95-$5.50. The shower-gift framing supports the top of that band.",
 why="You were selling a plushie. Sell a gift instead: 'baby shower gift' in the title changes who buys and how much they'll pay.",
 verify=["blanket dimensions (I wrote 12 x 12 in)", "page count (I wrote 11)", "yarn weight and yardage (I wrote 3.5mm/150 yds)",
         "that your head is machine-wash-safe (only promise it if true)", "bunny-ear method (I wrote worked in place)"],
 desc="""A lovey is the one crochet gift that gets used daily for three years — and it's two patterns in one file.

An amigurumi bunny lovey crochet PDF pattern: a bunny head worked onto a small blanket, sized for a newborn's hand to grip, with no loose parts and no reason to be nervous about it going in a cot.

WHAT YOU GET
- 11-page illustrated PDF, US and UK terms
- Finished size 12 x 12 in blanket with a 4 in bunny head — the standard lovey footprint, fits a nappy bag and a hospital bag
- Bunny ears worked in place (no sewing on, no asymmetry crisis at the end)
- Both blanket shapes: square (fast, beginner) and scalloped round (one extra round, photographs beautifully)
- Face options: embroidered only, so there are zero detachable parts
- Two weights: worsted 4 for a textured lovey, DK for a softer drape that's easier to grip
- Care notes — including the honest answer about machine washing a stuffed head, with the hand-wash alternative

SKILL LEVEL
Beginner for the bunny, confident beginner for the scalloped edge. Magic ring, single crochet, half double crochet, increase, decrease. Nothing is sewn.

MATERIALS
- Worsted or DK cotton/acrylic blend, approx 150 yds total
- 3.5mm hook for the head, 4mm for the blanket, small amount of fill, yarn needle

MADE FOR
Baby showers where everyone brings the same card, newborn photos, hospital-bag insurance, and the gift you give a friend in month seven of a pregnancy when you've run out of things to buy them. Also the highest-commission item a maker can produce per hour: about five hours' work.

INSTANT DOWNLOAD
Files unlock immediately after payment. Print the last page as a gift tag if you like.

TERMS
Personal use of the pattern file. Sell finished loveys freely — that's what people make them for. Do not resell, share, redistribute or reproduce the PDF, and don't use my photographs as your listing images.

SUPPORT
Worried the head is too bulky where it meets the blanket? That's the one real question on a lovey. Send a photo and I'll tell you exactly how much fill your version needs."""),

"C15": dict(
 obs="Chenille/velvet duck patterns sit at $2.25-$3.50 with only ~16 competing listings. Low ceiling, low competition — a keep, not a build.",
 why="Not worth a photo shoot. But chenille yarn is a distinct buyer with strong opinions about drool and softness, so name the yarn brands they actually use.",
 verify=["finished height (I wrote 5 in)", "page count (I wrote 9)", "that it works in chenille AND worsted",
         "approx 80 yds", "the 'low-sew' vs 'no-sew' wording - be exact, wings are a judgement call"],
 desc="""Soft in the way that makes people say something out loud when they pick it up.

A chenille duck crochet PDF pattern — an amigurumi duckling worked in velvet yarn for the specific squish people are chasing, with a low-sew finish. The wings are worked in place; the beak is embroidered, so nothing detaches in a toddler's mouth.

WHAT YOU GET
- 9-page illustrated PDF, US and UK terms
- One size: 5 in tall, the palm-size duckling that reads as a baby bird rather than a pillow
- Chenille-specific tension notes — velvet yarn lies and hides stitches, so the page counts differ from worsted, and I've written both
- Two yarn plans: chenille/velvet for the squish, and worsted 4 for a crisp, definable duck that survives a washing machine
- Wing method worked continuously, plus the folded-wing variation
- Beak and cheek embroidery charts with stitch counts
- Bonus: a 2 in egg-and-hatch version so you can gift it before the duck is 'born'

SKILL LEVEL
Beginner. Magic ring, single crochet, increase, decrease, embroider the face. Chenille makes dropped stitches invisible, which is either reassuring or infuriating depending on you.

MATERIALS
- Chenille or velvet yarn approx 80 yds (the classic white duck uses two colours); or worsted 4 in yellow plus a scrap of orange
- 4mm hook for chenille, 3.25mm for worsted, small amount of fill, tapestry needle

MADE FOR
Spring baskets, Easter, newborn gifts where the parent is a maker, and duck people, who are numerous and very sincere. Also the single best 'first soft toy' project — the yarn forgives everything.

INSTANT DOWNLOAD
Available the moment payment confirms.

TERMS
Personal use of the pattern file. Sell finished ducks anywhere, in any quantity. Do not resell, share, redistribute or reproduce the PDF, and please don't use my photographs as your listing images.

SUPPORT
If your duckling looks more pigeon than duck, it's the head-to-body ratio, and it's fixable in one round. Send a photo."""),

# ══════════════════════════════════════════════════════════════════════════
# SPREADSHEETS
# ══════════════════════════════════════════════════════════════════════════
"S3": dict(
 obs="17 listings on page 1, weak incumbents (~70 median reviews, ~500 max), price ceiling ~$13. Buyers describe it as 'giving' and 'membership' - your original title said 'donation'.",
 why="Right price, wrong vocabulary, and a thin market that a properly-worded listing can own outright.",
 verify=["tab list against your actual file", "whether multi-currency and export-to-PDF are really there - delete if not",
         "member count limits, if your sheet has any", "the walkthrough video's length"],
 desc="""Every gift, every member, one sheet your treasurer will actually keep using.

A church management spreadsheet that replaces the three documents your admin team is currently reconciling by hand: the membership roster, the giving log, and whatever the treasurer is doing in a second notebook.

WHAT IT DOES
- Google Sheets AND Excel versions, both in the download
- Member directory: household, contact, baptism/marriage status, ministry involvement, opt-out flags for directories, and a visit-log so pastoral follow-up isn't left to memory
- Giving register: date, member, fund (tithes, building, benevolence, missions), method, reference, and a running total per fund
- Envelope/offline giving entry with a batch total, so the Sunday counting adds itself
- Monthly and annual summaries per household — what you need for a year-end thank-you letter and for anyone who asks for a contribution statement
- Budget vs actual per ministry, with variance flagged rather than buried
- Attendance tab: service, adults, children, and a 12-month trend so you can see what September actually looked like
- Report-ready dashboard: one screen for the finance meeting, printable to PDF
- Multi-currency and annual rollover: it keeps last year's data and starts a clean sheet without a re-buy

WHY IT'S DIFFERENT
Most church sheets are a donation list with a logo. This one is built around the two things that actually break: funds not reconciling after a data-entry Sunday, and a new treasurer inheriting a file nobody documented. Every tab has an instructions row, and the whole thing is colour-coded for input cells only.

MADE FOR
Small and mid-size congregations, volunteer treasurers, church admins, and any committee that currently spends a meeting arguing about a number they could have looked up.

HOW IT WORKS
Buy, open the download, click your copy link, choose Excel or Google Sheets, add your funds and members. Setup takes about 20 minutes and there's a walkthrough video for the giving tab, which is where people stall.

TERMS
One-licence per church. Your whole finance team can use it. Please don't resell, share, redistribute, or rebrand the file.

SUPPORT
Tell me your fund structure and I'll show you how to lay it out. If your denomination counts giving differently, I'd rather adapt the guidance than have you fight the sheet."""),

"S4": dict(
 obs="15 listings, ~60 median / ~450 max reviews, and the highest ceiling in your catalogue at $26. Weak incumbents, professional buyer.",
 why="Price is right; the leak is a cover image that doesn't show the dashboard. This is the single listing where the photo fix is worth the most money.",
 verify=["tab names and count against your file", "that fee/instalment tracking really calculates balances",
         "whether staff HR fields exist", "data-validation features (dropdowns) if claimed", "video length"],
 desc="""A school runs on three spreadsheets nobody documented. This is the one that replaces them.

A school management spreadsheet for private schools, tutoring centres, academies and daycare owners — students, fees, attendance and staff, in one file with an actual dashboard on top.

WHAT IT DOES
- Excel template plus a Google Sheets copy, both included
- Student roster: admission date, grade/section, guardian contacts, medical flags, documents due, status (active, invoiced, graduated)
- Fees module: plan per student, instalment schedule, amount due, paid, balance, and overdue days — with an ageing view so you can see who owes what and since when
- Discount/scholarship field so your fee report reconciles with your intention, and a sibling rule that applies itself
- Attendance register by class and date, with a per-student month view and a percentage rollup for reports
- Staff directory: role, class load, contract dates, payroll reference, and document-expiry flags for certifications and first aid
- Classroom and capacity tracker, so enrolment targets aren't a guess
- Dashboard: enrolment, revenue billed vs collected, outstanding by family, attendance average by class
- Print-ready statements and a one-page dues reminder you can send without a screenshot

WHY IT'S DIFFERENT
School software costs per student per month and locks your data behind a login. This is a file you own, exports cleanly, and a part-time admin can learn in an afternoon. It is deliberately not trying to be an ERP — it is trying to be the four reports you actually run.

MADE FOR
Owners and administrators of schools from about 20 to 400 students, tuition centres, playgroups, music schools, and anyone still running fees on paper.

HOW IT WORKS
Buy, open the download, pick Excel or Google Sheets, load students, define fee plans. A 20-minute walkthrough covers the fee module specifically, because that's where the money is.

TERMS
One-licence per institution. Do not resell, share, redistribute, rebrand or bundle into a product you sell.

SUPPORT
If your fee structure is odd — termly with a transport add-on, say — send it to me and I'll tell you which tab to put it in before you build a second sheet."""),

"S7": dict(
 obs="46 listings deep with strong incumbents (2.6k reviews on a CRM-style sheet, 1.3k PLR sellers at $3-$10). You won't outrank them; you can still catch the long tail.",
 why="Do not spend a photo shoot here. Keep the rewrite, cross-link it from your niche sheets, and let it be the shop's landing page for 'bookkeeping'.",
 verify=["that Schedule C / quarterly tabs exist before naming them", "tab list vs your file",
         "whether a Shopify/eBay import really works", "mileage tracker existence", "video length"],
 desc="""The bookkeeping your accountant wishes you'd kept since January.

A small business bookkeeping spreadsheet for sole traders, makers and service businesses — income, expenses, profit and the tax prep you currently do in April with a shoebox.

WHAT IT DOES
- Google Sheets AND Excel, both in the download
- Income log: date, client, channel (Etsy, Shopify, in-person, invoice), gross, fees, shipping, net — so platform fees stop disappearing into "miscellaneous"
- Expense log with category, vendor, deductible flag, and receipt link fields
- Automatic P&L by month and by quarter, with gross margin and net margin rows
- Balance summary: cash in bank, receivables owed to you, payables you owe, inventory value
- Tax prep tab: quarterly totals, mileage log with dates and purpose, home-office and software subscriptions separated out
- KPI dashboard: revenue, expenses, profit, average order value, best month, best channel — one screen
- Multi-currency input with a rate column, and an annual rollover so last year stays intact
- Simple CSV import for platform exports, so a month of orders takes 40 seconds not four hours

WHY IT IS DIFFERENT
Bookkeeping templates are usually a budget with a business label. This one is organised the way a profit-and-loss statement is organised, because that is what gets reviewed — by you monthly, and by your accountant annually. Categories are editable, not hard-coded, and nothing needs a formula written.

MADE FOR
Solo operators under about $250k, makers at markets, freelancers, coaches, Etsy and Shopify sellers with more than one sales channel, and anyone who has ever said "I'll sort the books out later".

HOW IT WORKS
Buy, download, choose Excel or Google Sheets, paste your platform CSV into the import tab, categorise. A 12-minute walkthrough shows the import and the tax tab.

TERMS
Personal/business use for one owner. Do not resell, share, redistribute, rebrand or include in a course.

SUPPORT
Not sure which category a purchase falls into, or why your net doesn't match your bank? Send me the two rows and I'll tell you what's off."""),

"S9": dict(
 obs="42 listings, 1.2k median reviews, and a 38.7k-review incumbent at $1.92 on the single-file version. Bundles at $9-$17 do exist and convert.",
 why="'22 trackers' is the product and it was buried mid-title. Front the number, and reposition for the January reset.",
 verify=["the actual tab/sheet count - if it is 18, say 18", "which of these tabs genuinely exist in your bundle",
         "video library claim", "currency flexibility", "file sizes / any download limits"],
 desc="""Twenty-two money spreadsheets that agree with each other, instead of twenty-two files you'll abandon by March.

A personal finance spreadsheet bundle: the budget, the debt payoff, the savings goals and the net worth snapshot, all built on one shared setup so an income change updates all of them at once.

WHAT'S INSIDE (Excel and Google Sheets for every sheet)
- Paycheck budget, monthly budget, and the zero-based version for couples
- Bill calendar with due dates and a "paid" flag that feeds the month view
- Debt payoff with snowball and avalanche comparison side by side, and a projected payoff date you can watch move
- Emergency fund, sinking funds, big-purchase goal tracker
- Net worth statement: assets, liabilities, month-over-month change
- Spending tracker by category with a pie chart you don't have to build
- Subscription audit, medical/FSA log, kid-related costs, pet costs
- Savings challenge templates (52-week, no-spend month, round-up)
- Annual review and New Year reset worksheet
- Net-worth-for-two and a joint-accounts version for shared finances

HOW THEY CONNECT
There is one tab called Setup where you enter income, pay frequency, currency and household size. Everything else reads from it. Change your pay cheque once and every tracker in the bundle updates — which is the difference between a bundle and a zip file of unrelated sheets.

WHY IT IS DIFFERENT
Most bundles sell you volume: 200 templates, four of which you'll open. This is 22 that are wired together, and each one answers a question you actually have in the month you have it.

MADE FOR
Couples getting finances in one place before a move or a wedding, anyone rebuilding after a job change, the person who has started the app and the notebook and the spreadsheet and wants to stop, and anyone heading into January with intent.

HOW IT WORKS
Buy, open the download PDF, click the copy link for each tool. A short video library walks through Setup and the debt tab first, because those two run everything else.

TERMS
Personal use for your household. Do not resell, share, redistribute or rebrand.

SUPPORT
Send me your situation in two sentences — biweekly pay, one card, trying to kill a student loan — and I'll tell you which four tabs to start with. The rest can wait until February."""),

"S10": dict(
 obs="40 listings with brutal incumbents (12.6k at $9.25, 13.4k at $4.85) BUT also a 104-review seller at $13.71 and a 931-review at $21.38. Mid-size shops can charge here.",
 why="Your $11.99 was under-priced for what a bride will pay in the year she's not comparing. Lead with the tab count; it's your differentiation.",
 verify=["52 tabs - confirm the real count in your file", "which modules actually exist (delete any I've named that don't)",
         "currency-agnostic claim", "seating-chart drag/auto-fill behaviour", "video tutorial length"],
 desc="""Fifty-two tabs, one dashboard, and the reason you stopped answering the same question about the wedding.

A wedding planner spreadsheet built for the planning, not the Pinterest. Budget, guest list, seating, vendors, timeline and the day-of run sheet in one file that updates itself when a number changes.

WHAT IT DOES (Excel and Google Sheets, both included)
- Master dashboard: total budget, committed, invoiced, paid, remaining, and a red flag when a category is over
- Budget by category with % allocation guidance, plus a "quoted vs actual" column so a surprise becomes a line item, not a crisis
- Guest list: RSVP status, meal choice, side, plus-one logic, dietary notes, gift-received flag, and a seating chart that fills by assignment instead of by jigsaw
- Seating and table plan: capacity checks, kids' table, and a printable per-table list for the coordinator
- Vendor tracker: quote, deposit, balance due, contact date, delivery date, and a "nothing signed" warning list
- Timeline: 12-month checklist, 3-month, 1-month, week-of, and a day-of run sheet with times and responsible person
- Wedding party, ceremony, and rehearsal dinner tabs
- Payment schedule calendar and an instalment reminder column
- Honeymoon and post-wedding tabs (returns, thank-you notes, name-change checklist) so the file stays useful in January

WHY IT IS DIFFERENT
A wedding spreadsheet is only as good as the arithmetic under it. Here, changing headcount once updates catering cost, seating capacity, place cards and per-head budget — which is exactly what breaks in the free templates, usually in week forty of planning.

MADE FOR
Couples planning themselves, anyone with a strict total and soft per-category numbers, maid-of-honour squads running their own sheet, and planners who want a client-facing file that isn't a $400 subscription.

HOW IT WORKS
Buy, open the download file, click your copy link, then fill Setup: total budget, date, headcount. Everything else follows. A walkthrough video covers the guest list and seating chart together, since that's the pair that trips people up.

TERMS
One licence per wedding/party. Do not resell, share, redistribute or rebrand — and if you're a planner wanting to use it with clients, message me and I'll point you at the multi-client version.

SUPPORT
Something not matching your quote? Send me the two screenshots and I'll tell you which tab is double-counting. I answer quickly, including in the 11pm panic window."""),

"S11": dict(
 obs="38 listings, band $9-$37 for 50+-template mega bundles; the 3,000+ template junk packs at $1.59 have 3 reviews and go nowhere.",
 why="Your high-AOV anchor. The '2027 edition' refresh each November is how one file becomes a repeat sale.",
 verify=["exact template count", "which categories are really in the pack", "that both Excel and Google Sheets copies exist for every template",
         "file size / download instructions", "annual-edition plan if you advertise it"],
 desc="""Fifty finance spreadsheets, one setup screen, and no tab that contradicts another.

A budget spreadsheet bundle for people who want the whole system, not another single-file template that becomes useless the month their income changes.

WHAT'S IN THE PACK (Excel and Google Sheets for every template)
- Budgets: monthly, paycheck-by-paycheck, biweekly, zero-based, couple's, family, student, and a bare-bones one for people who hate budgeting
- Trackers: bills, expenses, income, savings, debt payoff, emergency fund, sinking funds, net worth, spending by category
- Planning: annual overview, quarterly review, tax prep, new-year reset, no-spend month, big purchase goal
- Business-adjacent: small-biz income/expense, invoice log, marketplace sales, freelance rates
- Household: groceries, meal plan, household calendar, home maintenance, car maintenance
- Lifestyle: habit, fitness, sleep, reading, cleaning schedule
- One Setup file: enter income, pay frequency, currency, household once — every sheet reads it, so one change updates fifty templates

WHY IT IS DIFFERENT
Mega bundles on Etsy are usually fifty unrelated files with one cover image. The value here isn't the count, it's the shared setup and consistent formatting — you learn one interface and every tab behaves the same way, with input cells marked and nothing requiring a formula.

MADE FOR
Anyone rebuilding their money system properly once, planners and coaches who want a client library, students, new households merging finances, and people who have bought a bundle before and used three files.

HOW IT WORKS
Buy, download the index PDF, click the copy links grouped by category. Setup video first (six minutes), then only what you need. Everything works offline in Excel and syncs when you use the Sheets copies.

TERMS
Personal use across your household. No reselling, sharing, redistributing, rebranding, or putting it inside another bundle.

SUPPORT
Tell me your pay schedule and your one problem; I'll name the three files to start with and which forty-seven can wait until spring."""),

"S14": dict(
 obs="29 listings, ~250 median / 2.6k max reviews, ceiling ~$8. Weak pricing power and no season urgency in Q4.",
 why="Keep it; don't build more travel SKUs. Best used as the bonus item that makes a bigger bundle look like a steal.",
 verify=["tab list vs your actual file", "whether the offline PDF export exists", "packing-list template count",
         "multi-trip support", "currency conversion behaviour"],
 desc="""Everything about the trip in one place, including the parts you currently keep in four apps.

A travel planner spreadsheet for the whole trip — the plan you make, the money you spend, and the list you write at 2am the night before.

WHAT IT DOES
- Google Sheets AND Excel versions
- Itinerary by day: date, city, activity, time, confirmation number, cost, and a notes column for the thing you'll otherwise forget at the desk
- Bookings register: flight, stay, transport, tours — with confirmation codes, payment status, and a "due to pay later" date so deposits don't sneak up
- Trip budget: total, per person, per day, planned vs actual, and a running currency-converted total when you're spending in a second currency
- Packing list that separates by traveller and by day count, with a pre-flight and post-shower checklist built in
- Expense log you can fill from your phone on a bus, that sums into the budget automatically
- Documents and links tab: passport expiry dates with a warning, insurance, emergency contacts, embassy numbers
- Multiple trips in one file via a dropdown — nothing overwrites last year
- Print-to-PDF day sheet, so the person who refuses to use an app still gets a page

WHY IT IS DIFFERENT
Travel apps hold your data hostage and die on bad signal. This is a file: it works on a plane, prints for a co-traveller, and keeps the receipts-linked totals that turn into a fair split when someone in the group paid for dinner four nights running.

MADE FOR
Family holidays where five people each booked something, group trips that need splitting, honeymooners, digital nomads, and anyone coordinating a multi-city itinerary with a partner who wants to see the numbers.

HOW IT WORKS
Buy, open the download, click your copy link, add a trip name in Setup. A short walkthrough shows the expense-to-budget link, which is the part people set up wrong.

TERMS
Personal use for your trips. Do not resell, share, redistribute or rebrand the file.

SUPPORT
Trip not structured like a normal holiday — rail passes, a cruise, ten people and three currencies? Send the shape of it and I'll tell you how to lay the tabs out."""),

"S15": dict(
 obs="The most crowded keyword you own: 46 listings, ~2,400 median reviews, 12.4k and 38.7k-review incumbents at $1.92-$9.59. Price fine; differentiation is not.",
 why="This needs dark mode and a 12-second dashboard video to be visible in that grid at all. Without them, no rewrite saves it.",
 verify=["whether dark mode exists (if not, drop that line or build it - it is a real differentiator now)",
         "which tabs exist: bills, debt, net worth, US tax prep", "recurring bills automation",
         "mobile-friendly claim", "video length"],
 desc="""A household budget that runs on autopay logic, not willpower.

A family budget spreadsheet for two-income households with recurring bills, a shared goal, and no appetite for maintaining a spreadsheet. Enter income and bills once; the month fills itself.

WHAT IT DOES
- Google Sheets AND Excel, both included
- Paycheck-budget view: money arrives, gets assigned, and shows you what's genuinely free this month — zero-based without the admin
- Bills calendar with due dates, autopay flags, and a "paid / scheduled / missed" status that drives the month-end number
- Recurring subscriptions audit: what it costs monthly, when it renews, and the annual cost you've never added up
- Spending tracker by category with a live over/under bar against what you said you'd spend
- Debt payoff with snowball vs avalanche side by side and a projected finish date
- Savings goals and sinking funds: car rego, school shoes, Christmas, insurance, vet
- Net worth tab: house, vehicles, accounts, owing — month over month
- US tax prep summary with deductible-ish categories split out for the file you hand over in April
- Dark mode version included, because it's a screen you look at at 10pm

WHY IT IS DIFFERENT
Budget templates assume one person, one income, no automation. This assumes two people, three paychecks, eleven recurring payments, and that nobody wants to be in the spreadsheet twice a week. Set it up once and it tells you the truth monthly.

MADE FOR
Couples merging finances, single parents running a tight month, anyone whose budget survives nine days, and households where "did we pay that?" is a repeated question.

HOW IT WORKS
Buy, download, click your copy link, choose Excel or Sheets, then fill two tabs: Income and Recurring. Everything downstream calculates. A 9-minute walkthrough shows the recurring-bills setup and the month-end close.

TERMS
Personal use for your household. Do not resell, share, redistribute or rebrand the file.

SUPPORT
If the maths doesn't match your bank, send me your Income tab and the two problem rows and I'll tell you what's double-assigned. Same-day replies."""),

"K4": dict(
 obs="Preschool activity/educational pages realise $2.50-$6 with far better ceilings than colouring pages. Dot-marker is an activity, not a colouring SKU - that is the whole reason this one survives.",
 why="The salvageable item from the colouring cluster. Re-angle as learning material, target parents AND teachers, and price at $3.",
 verify=["page count (I wrote 52)", "letter range and whether numbers 1-10 are included", "A4 vs US Letter",
         "that the high-contrast version exists", "licence: you may need a classroom-use tier for teachers"],
 desc="""Twenty-six letters, one dot marker, and a quiet fifteen minutes.

Alphabet dot-marker activity pages: a printable PDF where each letter gets a do-a-dot page with the uppercase and lowercase shape to trace, and three animals or objects starting with that letter to mark. Built for preschool hands, and for the specific parent who needs something that isn't a screen.

WHAT YOU GET
- 52-page printable PDF, US Letter and A4, black-and-white with a high-contrast version
- One page per letter, A to Z: dot grid over the letter, plus dot circles on three picture prompts
- Bonus number set 1-10 with dot markers, and a name-tracing page template
- Two difficulty tiers: chunky circles for age 2-3, smaller dots for 4-5
- Ink-friendly design — light grey outlines so the pages don't wreck a home printer
- A cover page and tab labels so it survives being a real workbook in a real classroom
- Finished pages double as a wall display, which is what teachers actually ask for

WHO IT'S FOR
Parents of 2-5 year olds, preschool and pre-K teachers building a letter-of-the-week unit, homeschool families starting formal work, occupational therapists and anyone working on pincer grip and hand-eye coordination, plus grandparents who want one activity that isn't candy.

WHY IT'S WORTH MORE THAN A COLOURING PAGE
It has a job. Colouring is filler; this is letter recognition, grip strength and following an instruction, in a format a three-year-old can finish without help — which is the reason it gets used twice instead of printed once.

HOW IT WORKS
Buy, download the PDF, print what you need. No cutting, no laminating required, though there's a reuse option on the last page for people who want to laminate. Print one page a day and you're through the alphabet in a school term.

TERMS
Personal and single-classroom use: one parent or one teacher, one licence. Please don't resell, share, redistribute or put it in another bundle. If you need multi-classroom or school-wide rights, message me and I'll set you up properly.

SUPPORT
Tell me the age and the tool — dabbers, markers, or coins — and I'll tell you which tier to print first. I answer same day."""),
}


# ---------------------------------------------------------------------------
# Tier-1 listings already ship full copy; these are the specs I inferred from
# your titles/market research that must be confirmed against your real files.
# Merge-only-verify entries: no desc, so the writer is not overwritten.
# ---------------------------------------------------------------------------
COPY.update({
 "N1": dict(verify=["mini count (I wrote 24) and that they are all in one PDF", "page count (18)",
        "that a hanger/video link exists before promising it", "yarn weights and 30g total claim",
        "finished mini size 1.5-2 in", "locking-marker vs button attachment method"]),
 "C1": dict(verify=["the three diameters 42/54/66 in", "that US AND UK terms are both written out",
        "12-spoke increase chart exists", "yardage 900-1200 yds", "optional ruffle section exists"]),
 "C2": dict(verify=["three ring sizes 14/18/24 in", "number of decor pieces (I wrote 5)",
        "that the loop-and-button attachment is really in the pattern", "500 yds figure", "no florist form needed - confirm"]),
 "C3": dict(verify=["ornament dimensions per piece", "that keychain variants exist", "page count (11)",
        "60g total yarn claim", "spiral variation is actually documented"]),
 "C5": dict(verify=["three sizes 3/6/9 in", "that it is genuinely one-piece with no applied beard",
        "embroidered face chart exists", "180 yds figure", "hat-stiffening options documented"]),
 "C6": dict(verify=["which three designs are actually in the bundle", "page count (20)",
        "that a no-sew version exists for each", "poly-pellet weight pocket documented", "size claims"]),
 "N2": dict(verify=["both lengths 48/68 in and the 14 in width", "that napkin rings/place cards are really in the PDF",
        "DK yardage figures", "no-seaming motif claim", "skill level wording vs your pattern"]),
 "S1": dict(verify=["every tab named - delete any that does not exist", "multi-currency support",
        "countdown-to-Christmas formula actually present", "video length (12 min)", "wrapping and cards tabs exist",
        "that both Excel and Sheets copies are delivered"]),
 "N6": dict(verify=["this is a NEW build - write the PDF first, then re-check every tab name here", "count the actual tabs, the listing says 7",
        "recipe scaling really auto-calculates", "potluck share-link exists or delete the line",
        "video length", "both Excel and Sheets versions"]),
 "S13": dict(verify=["automatic Etsy fee fields vs manual entry", "that Etsy CSV import really works",
        "craft-fair mode exists", "per-listing profitability tab exists", "video length (15 min)"]),
 "S6": dict(verify=["quote-comparison for 5 contractors - if 3, say 3", "contingency band advice",
        "change-order log exists", "loan/HELOC scenario tab exists or delete", "printable questions sheet is real"]),
 "S8": dict(verify=["which ratios are actually calculated (DSCR and debt yield are the risky claims)",
        "flip/BRRRR mode exists or delete the line", "sensitivity grid exists", "assumption defaults by property type",
        "both Excel and Sheets delivered"]),
 "S2": dict(verify=["recipe costing really drives pricing", "quote-builder-to-PDF claim", "order book fields",
        "ingredient inventory reorder logic", "that the two duplicate listings are merged before this ships"]),
 "S5": dict(verify=["AIA G702/G703 - say 'AIA-style' unless you genuinely mirror the format",
        "that all three tools are in the bundle", "retainage calculation exists", "subcontractor comparison sheet exists",
        "video length (20 min)", "one-business licence wording matches your intent"]),
})


# ---------------------------------------------------------------------------
# The remaining DO NOW / PRIORITY new builds. These products don't exist yet,
# which is why the copy ships early: for a new listing the description IS the
# build brief. Whatever you can't honestly ship, cut from the copy BEFORE you
# publish - not after someone points it out in a review.
# ---------------------------------------------------------------------------
COPY.update({
"S16": dict(
 obs="~22 listings, ~200 median / ~2,200 max reviews, ceiling near $12. Same band as your analyzer.",
 why="Two of your listings are circling one buyer. Split them by intent - buy-the-property vs run-the-property - and both get their own search space instead of competing inside your own shop.",
 verify=["tab list against your actual file", "whether rent-roll automation exists", "maintenance-log fields",
         "security-deposit tracking", "that both Excel and Sheets copies ship", "lease-renewal reminder logic"],
 desc="""What happens after the tenant signs: the rent ledger, the requests, and the deposit you still owe someone.\n\nA rental property management spreadsheet for self-managing landlords - the operational half that an analysis template never covers.\n\nWHAT IT DOES\n- Google Sheets AND Excel, both included\n- Property and unit register: address, type, purchase and mortgage reference, insurance, and per-unit notes\n- Tenant and lease tab: names, term start and end, rent, escalation, deposit held, contact details, and a renewal warning 60 days out\n- Rent ledger: due, paid, method, late fee applied, and an arrears view that colours itself when a payment is missing\n- Maintenance log: reported date, issue, vendor, cost, tenant-recoverable flag, status - and a per-property cost rollup so you can see which unit eats its margin\n- Expenses by category and year: taxes, insurance, management, repairs, supplies, mortgage interest\n- Rent-increase calculator with local-cap assumptions you set yourself, and a printable notice\n- Deposit tracking with deductions itemised at move-out\n- Owner dashboard: collected vs outstanding this month, annual net after expenses, and per-property profit\n\nWHY IT IS NOT THE ANALYSIS SHEET\nThe analyzer answers \"should I buy this?\" - underwriting, cap rate, cash flow before you own anything. This one answers \"am I being run ragged for $1,400 a month?\" Two different questions, two files, both yours if you need them.\n\nMADE FOR\nLandlords with 1-20 units, anyone who fired a management company, spousal teams where one person chases the rent, and the owner whose receipts live in a shoebox.\n\nHOW IT WORKS\nBuy, open the download, pick Excel or Google Sheets, add your units and tenants. Ledger totals and the dashboard build themselves from there. A short walkthrough covers the arrears view and the renewal warning.\n\nTERMS\nOne licence per landlord or entity. Use it across every property you own. Do not resell, share, redistribute or rebrand the file.\n\nSUPPORT\nLate fees, deposit deductions and tenant-recoverable costs are the three places landlords get their maths wrong. Send me your situation and I\u2019ll tell you which column to put it in."""),

"N3": dict(
 obs="~24 listings, ~400 median / ~2,000 max reviews, realised ceiling about $6.50. Adjacent advent-cluster sellers are holding $8-$25, so stockings at $6.50 is a value position, not a cheap one.",
 why="Cheapest real product in the DO NOW set: 24 tiny stockings is one weekend of stitching and it reuses the N1 mini vocabulary, so you can cross-sell the pair.",
 verify=["count (I wrote 24 and 12 - ship what you actually write)", "finished height 2.5 in", "page count",
         "that a name-tag/monogram option exists", "whether gift-tag loops are built in or added"],
 desc="""Twenty-four stockings the size of your thumb, and one of them can hold a chocolate coin.

A crochet pattern for 24 mini Christmas stockings sized to hang on a garland, a tree, a mirror or the side of a shelf, worked in the round from cuff to toe with no sewing shut.

WHAT YOU GET
- 9-page illustrated PDF, US and UK terms
- 24 stocking instructions in 2 sizes: 2.5 in for an advent garland, 4 in for a name-stockings set
- One base construction with 6 cuff variations (ribbed, folded, scalloped, contrast, striped, and plain for painting)
- Built-in gift-tag loop on the top edge, so a name tag or a chocolate coin hangs without a sewing job
- Optional monogram chart, A to Z, embroidered after blocking
- A 12-mini version for a smaller tree, at the end of the PDF
- Yardage per stocking so a single 50g ball covers a whole set

SKILL LEVEL
Beginner. Chain, single crochet, half double crochet, work-toe-forward shaping, and change colour at the cuff. The shaping is the only new idea and it's the same three rounds every time.

MATERIALS (whole set of 24)
- Scrap yarn in any Christmas colours, roughly 120g total across the batch
- 3.0mm hook, tapestry needle, 24 small gift tags or jump rings if you want them

MADE FOR
The advent calendar for people who don't want to crochet 24 presents, a garland that doubles as place cards at Christmas dinner, stocking-name gifts for a whole family at one price, and makers who want a market product that takes 40 minutes each.

INSTANT DOWNLOAD
Files unlock the moment payment clears.

TERMS
Personal use of the pattern file. Sell finished stockings anywhere, in any quantity. Do not resell, share, redistribute or reproduce the PDF, and please do not use my photographs as your own listing images.

SUPPORT
If your toe comes out lopsided, that's one round and it's fixable — send a photo and I'll tell you which. Same-day replies in December, because I know when you're making these."""),

"N4": dict(
 obs="~16 listings, ~350 median / ~900 max reviews, ceiling around $5. Zodiac-animal plushies with 190-210 reviews sold at $3.24-$4.99 in the February window - real, small, and timed.",
 why="Timing correction, stated plainly: Chinese New Year 2027 is February 6 and the animal is the FIRE GOAT, not the horse - the horse wave passed in February 2026. So this is a goat/lamb pattern with a zodiac front, which means it sells into Feb 6-20 and then again as a spring farm animal. A horse pattern published now would be a year late and dead in January.",
 verify=["whether you build goat, lamb, or one body with two faces - the copy assumes one body, two finishes",
         "finished size (I wrote 4 in)", "page count (I wrote 11)", "that the horns are optional (a lamb has none)",
         "red/gold colourway advice and any 'lucky' charm detail before promising it"],
 desc="""A soft, woolly goat for the Year of the Fire Goat — and the same body becomes a spring lamb.

A crochet PDF pattern for an amigurumi goat/lamb worked as one continuous body, published now so it's ready for Chinese New Year on February 6, 2027, and useful again as a farm-lamb pattern through Easter.

WHAT YOU GET
- 11-page illustrated PDF, US and UK terms
- Two finished sizes: 4 in shelf/plush size, and 2.5 in keychain charm
- One base body, two heads of options: horns for goat, none for lamb — no second pattern to buy
- Curly-top method for the fleece (a crochet loop stitch, not glued-on yarn), with a straight-hair variation for the goat face
- Blanket-and-saddle coat with a colourwork band, plus the red-and-gold auspicious colourway for Lunar New Year gifting
- Optional tassel or coin charm with a hanging loop, worked in place
- Standing-vs-sitting instructions — legs are where these patterns flop, literally
- Yardage table; the whole 4 in goat comes in under 100 yds

SKILL LEVEL
Beginner-friendly. Magic ring, single crochet, increase, decrease, half-double for the fleece loops, colour change, and stuffing firm. If you've made one amigurumi before, you have all of this.

MATERIALS (4 in goat)
- Worsted 4 cream or white approx 90 yds; small amounts in brown, red and gold
- 3.25mm hook, fibre fill, yarn needle, optional 5mm jump ring for the charm version

MADE FOR
Lunar New Year gifts and red-envelope plushies (buyers want these by early February), zodiac collectors, classroom spring units, Easter baskets, farm-themed nurseries, and anyone who has been asking for a goat since the capybara.

INSTANT DOWNLOAD
Files unlock the moment payment clears — which is the point of an early publish, because the people who need it for February 6 will shop in January.

TERMS
Personal use of the pattern file. Sell finished goats and lambs anywhere, in any quantity. Do not resell, share, redistribute or reproduce the PDF, and please don't use my photographs as your listing images.

SUPPORT
Horns not holding their curl, or the body won't sit up? Send a photo of the round you're on and I'll tell you what's short. Same-day replies in January, because I know when these are being made."""),

"N7": dict(
 obs="~26 listings, ~900 median / ~19,000 max reviews, but the realised ceiling is only about $4.50. Volume keyword with a low ceiling - a standalone card list can't carry money.",
 why="So don't sell it standalone. This exists to be the second half of the gift tracker at $4.50 more, and to catch the 'when do I mail my cards' search that your $9.99 tracker doesn't cover.",
 verify=["tab list against whatever you build", "that postmark/deadline logic really exists (build it if you promise it)",
         "US + international postage columns", "whether a printable address-label sheet is included - only claim it if you ship it",
         "Excel and Google Sheets both"],
 desc="""The card list that tells you, in November, that you're already behind.

A Christmas card and address tracker spreadsheet: one place for who's on your list, who sent you something, what you owe them back, and the last date you can realistically mail it.

WHAT IT DOES
- Google Sheets AND Excel, both in the download
- 7 tabs, including a printable 2x4 label grid that mails straight off the page
- Address book: household, street, emails, dietary/kids notes, and a 'written back yet' flag that doesn't reset itself
- This year's list: sent / received / pending, with a column for what they'd actually like (not 'gift card', again)
- Postmark deadline calculator: enter your country and mailing date and it flags standard vs. first-class cut-offs, so nothing arrives January 3rd
- Returned-address label sheet, printable on standard 2×4 label stock, generated from the same data
- Card-stash inventory: how many you bought, how many used, so you stop buying 40 and needing 55
- Thank-you tracker for gifts received, with a due-by date and a nudge column — this is the tab people email me about
- Budget line for cards/stamps/labels versus actual
- Year-over-year archive: keep every year's list, nothing gets overwritten

WHY IT'S A SEPARATE FILE
Because 'when do I send Christmas cards' is a different panic than 'what am I buying whom', and the seller who needs one will not always want the other. If you want both, the gift tracker bundle is the pair at less than the sum.

MADE FOR
Households sending 20-200 cards, anyone coordinating a family newsletter, small businesses doing client cards, and the person who has mailed a card on December 28 for the last four years running.

HOW IT WORKS
Buy, download, click your copy link, paste last year's list in. A short walkthrough covers the label print, because that's the part that fights you.

TERMS
Personal use for your household or small business. Do not resell, share, redistribute or rebrand the file.

SUPPORT
Label alignment off by a few millimetres, or your postage dates different from the defaults? Tell me your country and printer and I'll tell you what to change."""),

"N8": dict(
 obs="Only ~12 listings in this cluster, ~150 median / ~1,000 max reviews, ceiling around $5. Small but genuinely underserved, and office/Secret Santa buyers are not price-shoppers.",
 why="Thin-market volume play: it's a $5 listing that can appear in every office in December. Build it in a day from pieces you already own.",
 verify=["that name-draw automation really works before promising it", "price-cap and 'no repeat' rules exist",
         "how many participants the sheet handles", "Excel + Sheets both", "no email/sending integration - don't claim it"],
 desc="""Secret Santa without the group chat, the spreadsheet argument, or the person who drew their own name.

A Secret Santa / white elephant organiser spreadsheet that draws names fairly, enforces your rules, and hands each person a printable card telling them who they have and what the budget is.

WHAT IT DOES
- Google Sheets AND Excel, both included
- 9 tabs, and the same file runs next year's exchange and the one after
- Participant list with email, budget preference, a 'would never buy' list, and a size/taste note
- Name draw: one button, randomised, and it cannot pair someone with themselves or with a partner unless you allow it
- Exclusion rules: past two years, ex-colleagues, 'never my manager' — set once, respected in every draw
- Budget and deadline banner that prints onto each reveal card, so nobody has to ask the organiser for the third time
- Wishlists stay with the recipient, visible to their giftee only (one shared column, no DMs)
- White elephant mode: pick order, steal limits, and a round tracker for the party itself
- Completion log: bought / wrapped / delivered, for the 3% of people who will genuinely forget
- Print-and-cut reveal slips tab, and a 'results' tab for the group afterwards

WHY A SPREADSHEET AND NOT AN APP
Because apps charge per group, need everyone to install something, and lose the exclusions you set last year. This is a file you keep — the same one runs the office, the extended family and your book club, and remembers who drew whom.

MADE FOR
Office party organisers, friend groups of 8-30, family exchanges, church and sports-club swaps, and anyone who has been volunteered as Secret Santa organiser two years running.

HOW IT WORKS
Buy, open the download, pick Excel or Sheets, paste names in, set budget and exclusions, click draw, print the slips. Ten minutes, including the coffee.

TERMS
Personal use for your group(s). Do not resell, share, redistribute or rebrand the file.

SUPPORT
If your group has a rule the sheet doesn't expect — 'the two new hires draw each other', say — message me and I'll tell you the two cells to change."""),

"N9": dict(
 obs="~20 listings, ~400 median / ~5,000 max reviews, ceiling around $9 and higher for 'reset' framing in January. Q4's tail and January's head — same buyer, two months apart.",
 why="Publish Dec 26. It catches the last week of Q4 traffic (people planning 2027) and then carries the shop through the dead first half of January.",
 verify=["tab list vs what you build", "that January-to-December monthly view exists", "whether it links to your other sheets - only say so if the Setup tab really drives them",
         "debt payoff plan tab", "Excel + Sheets both"],
 desc="""The money plan you'd actually keep, written for the week you're motivated and the month you're not.

A New Year financial reset spreadsheet: one structured pass over last year's mess, a decision about the next twelve months, and a system simple enough to survive February.

WHAT IT DOES
- Google Sheets AND Excel, both in the download
- 13 tabs, ordered so you can stop after tab 2 and still have gained something
- 10-minute audit tab: what you earned, spent, owed and saved last year, from bank statements and one export
- Keep / stop / start worksheet with the number attached to each decision, so 'spend less' becomes a figure
- Twelve-month budget laid out January to December on one screen, with the obvious traps marked: December, birthdays, car rego, holidays
- Paycheck plan: what hits your account, what's already spent, what's genuinely yours
- Debt payoff with snowball and avalanche shown side by side, plus one 'if you add $50/month' line
- Emergency fund and sinking funds for the predictable surprises
- Net worth snapshot with a monthly history row, so the year shows up as a curve instead of a vibe
- Quarterly review prompts (March, June, September, December) with three questions each, pre-written
- January-only energy: a 30-day challenge tab you can finish and never reopen

WHY IT'S NOT JUST ANOTHER BUDGET
Most planners assume a steady monthly salary and no baggage. This one starts with the audit, because the reset is the hard part, and it assumes you'll abandon it by week five — so the layout is built to be picked back up cold in June without relearning it.

MADE FOR
Anyone starting 2027 with intent, couples merging finances after the holidays, the January-customer who bought your bundle in December and needs a different front door, and anyone who has downloaded a budget before and stopped using it in February.

HOW IT WORKS
Buy, download, click the copy link for Excel or Sheets. Do the audit tab first, in one sitting, before you touch the monthly view — that order is the whole method. A 7-minute walkthrough covers it.

TERMS
Personal use for your household. Do not resell, share, redistribute or rebrand.

SUPPORT
Send me your audit numbers in two lines and I'll tell you which two tabs matter most for your situation, and which to skip this year."""),
})
