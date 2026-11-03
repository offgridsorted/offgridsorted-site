"""Pinterest pins for guides (1000 x 1500).

Usage: python3 tools/pins.py <slug> [out.html]
Writes the pin as an HTML page. Render it at 1000x1500 with Playwright (inline the
brand fonts as @font-face if Google Fonts is blocked), save as assets/pins/<slug>.jpg
(JPEG quality ~86) and add a row to social/pinterest-pins.csv.
Add each new guide to PINS below: (big headline, short handwritten note).
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import build as b

PINS = {
    'van-power-basics': ("Van power, explained in plain English", "the 4 parts & how they fit together"),
    'lithium-vs-agm': ("Lithium or AGM?", "which one should you get?"),
    'how-much-solar-australia': ("How much solar do I need?", "it depends on your state & season"),
    'dc-dc-chargers-explained': ("DC-DC chargers, explained", "charge your battery while you drive"),
    'caravan-power-setup': ("Why your caravan battery isn't charging on the tow", "the long-cable problem, & the fix"),
    '4wd-dual-battery-basics': ("4WD dual battery basics", "under the bonnet or in the tray?"),
    'will-my-fridge-last': ("How long will a 100Ah battery run my fridge?", "real numbers, not guesses"),
    'portable-power-stations': ("Power station or a proper dual battery?", "when the box is all you need"),
    'battery-size-for-12v-fridge': ("What size battery for a 12V fridge?", "with a simple table"),
    'fridge-flattening-battery': ("Fridge flattening your battery?", "check these 5 things, in order"),
    'lithium-under-the-bonnet': ("Lithium battery under the bonnet?", "why most don't belong there"),
    'smart-alternator-check': ("Does my car have a smart alternator?", "2 quick checks to find out"),
    'caravan-not-charging-while-driving': ("Caravan not charging while driving?", "a step-by-step fix"),
    'solar-blanket-vs-fixed-panel': ("Solar blanket or fixed panel?", "who each one suits"),
    'winter-solar-not-keeping-up': ("Why isn't my solar keeping up in winter?", "it's probably not your panel"),
}
THEMES = [("#f3f0e8", "#1c1f1b", "#1d5c3a", "#f5cb3c"), ("#f5cb3c", "#1c1f1b", "#1d5c3a", "#1d5c3a"), ("#1d5c3a", "#f3f0e8", "#f5cb3c", "#f5cb3c")]


def pin_html(slug):
    live = [g for g in b.GUIDES if g[4] == "live"]
    i = [g[0] for g in live].index(slug)
    _, title, tag, blurb, _ = live[i]
    head, note = PINS[slug]
    bg, ink, acc, hl = THEMES[i % 3]
    logo = re.search(r'(<svg viewBox="0 0 420 300".*?</svg>)', open(os.path.join(b.ROOT, "index.html")).read(), re.S).group(1)
    dd = b.doodle(b.TAG_DOODLE.get(tag, "sun"), 400, cls="dd")
    size = 118 if len(head) < 26 else (100 if len(head) < 40 else 86)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0}}body{{width:1000px;height:1500px;background:{bg};color:{ink};font-family:'Source Serif 4';position:relative;overflow:hidden}}
.k{{position:absolute;left:80px;top:96px;font-family:Barlow;font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:30px;color:{acc}}}
h1{{position:absolute;left:80px;right:80px;top:150px;margin:0;font-family:Bitter;font-weight:800;font-size:{size}px;line-height:1.04;letter-spacing:-.01em}}
.u{{display:block;width:300px;height:22px;margin-top:22px}}
.dd{{position:absolute;left:230px;top:760px;width:540px;height:auto;color:{ink}}}
.n{{position:absolute;left:80px;right:80px;top:640px;font-family:Caveat;font-weight:700;font-size:64px;line-height:1.05;transform:rotate(-2deg)}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:230px;background:#1c1f1b;display:flex;align-items:center;justify-content:space-between;padding:0 70px;box-sizing:border-box}}
.foot .lg{{color:#1c1f1b;background:#f3f0e8;border-radius:24px;padding:10px 16px}}
.foot .lg svg{{width:190px;height:auto;display:block}}
.foot p{{margin:0;text-align:right;font-family:Barlow;font-weight:600;font-size:34px;color:#f3f0e8;line-height:1.3}}
.foot b{{font-family:Bitter;font-weight:800;font-size:42px;color:#f5cb3c}}
</style></head><body>
<div class="k">Free guide · {html.escape(tag)}</div>
<h1>{html.escape(head)}<svg class="u" viewBox="0 0 300 22"><path d="M4 14c60-10 140-12 292-4" fill="none" stroke="{hl}" stroke-width="10" stroke-linecap="round"/></svg></h1>
<div class="n">{html.escape(note)} ↓</div>
{dd}
<div class="foot"><div class="lg">{logo}</div><p>Plain-English, Aussie prices<br><b>offgridsorted.com.au</b></p></div>
</body></html>'''


if __name__ == "__main__":
    slug = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/pin-{slug}.html"
    open(out, "w").write(pin_html(slug))
    print(out)
