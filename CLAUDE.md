# Off-Grid Sorted: house rules

Off-Grid Sorted is an independent Australian website that helps people work out the power setup (battery, solar, DC-DC charger, inverter) for campervans, caravans/camper trailers and 4WDs, and later homes. It earns through affiliate links, email and its own digital products. Owner: Kiran. Hosted as a static site on Netlify from this repository.

## Voice
- Plain English, very layman's terms. Explain every technical term the first time, or use the tap-to-explain words.
- Friendly, honest and practical. Use everyday comparisons and metaphors to explain ideas (the person likes them), but never let a metaphor replace the real number.
- Australian spelling and terms (colour, metres, ute, servo, BCF). Prices in AUD.
- No em dashes. Short sentences. No hype words ("ultimate", "game-changer").
- Never pretend to first-hand experience the owner hasn't had. Leave a clearly marked placeholder like [Kiran's note: ...] where her own story or photo should go.
- The reader is like Kiran: curious and keen to understand, but big technical words make their brain shut down. Use the everyday word first ("the charger that fills your battery while you drive"), then name the technical term once if they'll meet it in shops.
- Empower, never compare. No "know more than most people", no digs at other sites or other campers.
- Say "Aussie" in friendly spots (labels, headings); keep "Australian" in page titles, descriptions and the hero intro for search.
- Spell things out: "Bureau of Meteorology", not BOM.
- Be straight about money: we earn a small commission on some links, it never decides what we recommend. Never word anything so it sounds like we take no commission.
- Talk about the tool doing the maths when that's what happens, but a friendly "we'll tell you" is fine on the homepage.
- Write "Kiran, Mitch & Ziggy". The Hiace is their weekender (drive there, set up camp, come home), not a home on wheels.
- The three kits are Weekender (drive there, set up camp, come home), Road trips, and Living in it.

## Safety and honesty (non-negotiable)
- Every guide that touches wiring says to have a licensed auto electrician install or check the system, and never to work on 240V wiring yourself.
- Numbers are estimates; say so. Cite sources (BOM for sun, manufacturer specs for products).
- Recommend products by fit, not commission. Show budget / mid-range / premium options and what the extra money gets you.
- Every page with affiliate links links to disclosure.html.
- Only recommend products we can link to at a real online shop. If there is no linkable pick for a size or type, say so plainly and point to an option that has one (never show a brand name with no link).
- Product notes are read one price level at a time: never say "below", "above" or "the X" for a product in another level without naming the level (e.g. "the mid-range Victron").
- Sale prices: a product shows its old price crossed out next to the sale price (the "was" field on a store, or "rrp"). Only keep a "was" price the shop shows today (Shopify: compare_at_price in the product .js), re-check it on every price check, and delete it when the sale ends or it can't be confirmed.
- No "wait for a sale" timing advice. "Good to know" notes are for real product limits (warranty, weight, missing features).

## Brand
- Logo: the smiling sunny battery with "off-grid SORTED" (Permanent Marker for the word SORTED only).
- Colours (Nov 2026 refresh, "coastal bush": soft, outdoorsy, not bright): paper #f3f0e8, ink #1c1f1b, eucalyptus green #3a7560 (buttons, links; darker edge #285443), soft sun yellow #ecc55c (second buttons, accents; edge #c49d3c), sand band #f5edd6, sea-sage band #e2ece6, sea blue #4a8aa0 (small accents only), grey text #454942. The logo keeps its original sunshine #f5cb3c and marigold #e0a12e.
- Type: Bitter (headings), Source Serif 4 (body), Barlow (UI), Caveat (small handwritten notes). The logo uses Kalam for "off-grid" and Permanent Marker for "SORTED".

## Look and layout (the homepage is the reference)
- Calm and uncluttered. Show only what the reader needs right now. One clear main action per screen.
- Break the page into sections with soft colour bands (sand and sea-sage alternating). No boxes around everything, no tilted or wonky "sticker" styling, nothing that looks too perfect or busy.
- Buttons are chunky and friendly: rounded, with a darker edge underneath so they look pressable, and an arrow on the main one. Main action eucalyptus green; on a sage background, use the yellow button. Small links inside cards are small outlined buttons.
- Generous spacing: a clear gap under every heading, between paragraphs, above every button, and between the hero heading, intro, button and notes.
- Section headings sit at the top of their band; the little line drawing sits top right without pushing anything down.
- Hand-drawn touches in black ink (Caveat), never blue: short notes, arrows, the yellow underline under a key word. Highlighter behind a note is very faint (about 10% yellow).
- Grey text is #454942, never lighter. Logo at least 120px wide on phones.
- Trust comes early: the green trust banner (Independent, Made for Australia, Plain English, Safety first) sits straight after the first set of choices. Pages end with one calm call to action, not a loud block.
- Lead with pictures where we can: dramatic Aussie location photos that are obviously not us, plus our own line drawings. Real photos of Kiran, Mitch & Ziggy only where it's really them.
- Phones first: check every change at 390px wide. No single words left alone on the last line.
- Evidence-based: every number is worked out (planner maths, Bureau of Meteorology sun data, real product specs and prices) and says it's an estimate.

## Site structure
- Pages are built by `python3 tools/build.py` from `content/`. Edit content, run the build, commit the generated HTML too (Netlify has no build step).
- index.html: homepage (from content/home.html).
- planner.html: the Power Planner calculator, hand-written (the build only refreshes its header and footer).
- guides/: one page per guide. Write the body in content/guides/<slug>.html and add it to GUIDES in tools/build.py (status "live" or "soon").
- about.html, disclosure.html, privacy.html (from content/).
- assets/site.css: shared styles.

## Deploying (Kiran's rule, 7 Nov 2026)
- Never push to main (the live site) unless Kiran says to deploy in this conversation. Commit locally or push a branch / pull request instead, and tell her what's ready.

## Saving Netlify credits
- Netlify's free plan gives 300 credits a month and every push to main is a production deploy costing 15 credits (about 20 deploys a month).
- So: commit work locally or on a branch, and push to main in one batch at the end of a session, not after every change.
- For Kiran to preview before it goes live, push a branch and open a pull request: deploy previews are free.

## Workflow for scheduled guide runs
- Write new guides on a branch and open a pull request for Kiran to review. Do not push guides straight to main unless she has said auto-publish is on.
- Price and link checks: approved by Kiran on 3 Nov 2026 to commit straight to main without asking. Run them twice a week (Monday and Thursday), and only push when something actually changed (a price, stock, or a dead link), so it stays within the Netlify credit budget.
