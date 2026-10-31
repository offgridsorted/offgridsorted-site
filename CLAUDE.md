# Off-Grid Sorted: house rules

Off-Grid Sorted is an independent Australian website that helps people work out the power setup (battery, solar, DC-DC charger, inverter) for campervans, caravans/camper trailers and 4WDs, and later homes. It earns through affiliate links, email and its own digital products. Owner: Kiran. Hosted as a static site on Netlify from this repository.

## Voice
- Plain English, very layman's terms. Explain every technical term the first time, or use the tap-to-explain words.
- Friendly, honest and practical. Use everyday comparisons and metaphors to explain ideas (the person likes them), but never let a metaphor replace the real number.
- Australian spelling and terms (colour, metres, ute, servo, BCF). Prices in AUD.
- No em dashes. Short sentences. No hype words ("ultimate", "game-changer").
- Never pretend to first-hand experience the owner hasn't had. Leave a clearly marked placeholder like [Kiran's note: ...] where her own story or photo should go.

## Safety and honesty (non-negotiable)
- Every guide that touches wiring says to have a licensed auto electrician install or check the system, and never to work on 240V wiring yourself.
- Numbers are estimates; say so. Cite sources (BOM for sun, manufacturer specs for products).
- Recommend products by fit, not commission. Show budget / mid-range / premium options and what the extra money gets you.
- Every page with affiliate links links to disclosure.html.

## Brand
- Logo: the smiling sunny battery with "off-grid SORTED" (Permanent Marker for the word SORTED only).
- Colours: paper #f3f0e8, ink #1c1f1b, sunshine #f5cb3c, marigold #e0a12e, road-sign green #1d5c3a.
- Type: Barlow Condensed (headings), Source Serif 4 (body), Barlow (UI), Caveat/Kalam (small handwritten notes).

## Site structure
- index.html: the Power Planner calculator (single self-contained page).
- guides/: one HTML page per guide, linking back to the planner.
- about.html, disclosure.html, privacy.html.

## Workflow for scheduled guide runs
- Write new guides on a branch and open a pull request for Kiran to review. Do not push guides straight to main unless she has said auto-publish is on.
- Price and link checks may be committed directly once she approves that.
