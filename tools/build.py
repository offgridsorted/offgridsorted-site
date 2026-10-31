#!/usr/bin/env python3
"""Builds Off-Grid Sorted's static pages from content fragments.

Run from the repo root:  python3 tools/build.py
- content/home.html            -> index.html
- content/guides/<slug>.html   -> guides/<slug>.html   (listed in GUIDES below)
- guides/index.html            -> built from GUIDES
- about/disclosure/privacy     -> from content/<name>.html
The Power Planner (planner.html) is hand-written; this script only refreshes its header and footer.
"""
import os, re, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doodles import doodle, horizon, TAG_DOODLE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "Off-Grid Sorted"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@600;700;800&family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Caveat:wght@500;700&family=Permanent+Marker&family=Kalam:wght@700&display=swap" rel="stylesheet">')

# Guides: (slug, title, tag, blurb, status)  status "live" or "soon"
GUIDES = [
    ("van-power-basics", "Van power in plain English: the four parts and how they fit", "Start here",
     "Battery, solar, DC-DC charger and inverter, explained without the jargon.", "live"),
    ("lithium-vs-agm", "Lithium vs AGM: which battery should you get?", "Batteries",
     "The real difference, what it means for size, weight and cost, and when AGM still makes sense.", "live"),
    ("how-much-solar-australia", "How much solar do I need? By state and season", "Solar",
     "Why a Hobart winter and a Darwin winter need very different setups, with a table for every state.", "live"),
    ("dc-dc-chargers-explained", "DC-DC chargers explained: charging while you drive", "Charging",
     "What they do, what size you need, and why modern cars with smart alternators need one.", "soon"),
    ("caravan-power-setup", "Caravan power: getting charge through the trailer plug", "Caravans",
     "Why caravans lose charge over long cables, and how to fix it.", "soon"),
    ("4wd-dual-battery-basics", "4WD dual battery basics", "4WDs",
     "Under-bonnet or in the tray, smart alternators, and fitting solar on a 4WD.", "soon"),
    ("will-my-fridge-last", "Will my fridge last the weekend?", "Fridges",
     "How much power camping fridges really use, and how to make yours sip less.", "soon"),
    ("portable-power-stations", "Portable power stations vs a proper dual battery setup", "Batteries",
     "When an all-in-one box is all you need, and when it isn't.", "soon"),
]

LOGO = '''<svg viewBox="0 0 420 300" width="{w}" height="{h}" role="img" aria-label="Off-Grid Sorted">
<defs><filter id="rLogo{id}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"></feTurbulence><feDisplacementMap in="SourceGraphic" scale="3.2"></feDisplacementMap></filter></defs>
<g filter="url(#rLogo{id})" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M60 52l-12-18M110 38l-2-22M160 52l12-18M28 92l-20-6M192 92l20-6" stroke="#e0a12e" stroke-width="6"></path></g>
<g fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><rect x="34" y="70" width="152" height="86" rx="14" fill="#f5cb3c"></rect><path d="M186 98h12v30h-12" fill="currentColor"></path></g>
<g filter="url(#rLogo{id})" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M58 132v-34M80 132v-34M102 132v-34" stroke-width="7"></path><circle cx="138" cy="106" r="3.5" fill="currentColor"></circle><circle cx="160" cy="106" r="3.5" fill="currentColor"></circle><path d="M136 122c6 8 20 8 26 0"></path></g>
<text x="34" y="214" font-family="Kalam, cursive" font-weight="700" font-size="34" fill="#1d5c3a" letter-spacing="1">off-grid</text>
<text x="30" y="272" font-family="'Permanent Marker', cursive" font-size="66" fill="currentColor">SORTED</text>
<path d="M36 288c60-10 140-10 236 2" fill="none" stroke="#e0a12e" stroke-width="8" stroke-linecap="round" filter="url(#rLogo{id})"></path>
</svg>'''

NAV = [("kits/index.html", "Kits"), ("guides/index.html", "Guides"), ("about.html", "About")]


def logo(w=120, ident="H"):
    return LOGO.format(w=w, h=round(w * 300 / 420), id=ident)


def head(title, desc, pre):
    full = f"{title} · {SITE}" if title != SITE else f"{SITE} · Off-grid power for Australian vans, caravans and 4WDs"
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{pre}assets/site.css">
</head>
<body>
'''


def header(pre, active=""):
    links = "".join(
        f'<a href="{pre}{href}"{" aria-current=\"page\"" if active == href else ""}>{label}</a>' for href, label in NAV)
    drop = "".join(f'<a href="{pre}{href}">{label}</a>' for href, label in NAV)
    return f'''<header class="site-header">
  <div class="in">
    <a class="logo" href="{pre}index.html" aria-label="Off-Grid Sorted home">{logo(170)}</a>
    <nav class="nav" aria-label="Main menu">{links}<a class="cta" href="{pre}planner.html"{' aria-current="page"' if active == "planner.html" else ""}>Power Planner</a></nav>
    <details class="menu-toggle"><summary>Menu</summary><div class="drop"><a href="{pre}planner.html"><b>Power Planner →</b></a>{drop}</div></details>
  </div>
</header>
'''


def footer(pre):
    live = [g for g in GUIDES if g[4] == "live"]
    glinks = "".join(f'<a href="{pre}guides/{g[0]}.html">{html.escape(g[1].split(":")[0])}</a>' for g in live)
    return f'''<footer class="site-footer">
  {horizon()}
  <div class="in">
    <div class="about">
      <div style="color:var(--ink)">{logo(130, "F")}</div>
      <p>Plain-English help to get the power setup in your van, caravan or 4WD sorted. Independent and Australian.</p>
      <p class="small">Some links earn us a small commission at no cost to you. <a href="{pre}disclosure.html" style="display:inline;color:var(--sign)">How we make money</a>.</p>
    </div>
    <div><h4>Tools</h4><a href="{pre}planner.html">Power Planner</a><a href="{pre}planner.html#check">Check what I've got</a><a href="{pre}kits/index.html">Ready-made kits</a></div>
    <div><h4>Guides</h4>{glinks}<a href="{pre}guides/index.html">All guides</a></div>
    <div><h4>Off-Grid Sorted</h4><a href="{pre}about.html">About</a><a href="{pre}disclosure.html">Disclosure &amp; disclaimer</a><a href="{pre}privacy.html">Privacy</a><a href="https://www.instagram.com/offgridsorted" rel="noopener">Instagram</a></div>
  </div>
  <p class="small" style="max-width:1080px;margin:0 auto;padding:0 18px 24px">© 2026 Off-Grid Sorted. Estimates only. Always have a licensed auto electrician install or check your system.</p>
</footer>
'''


def page(path, title, desc, body, active=""):
    pre = "../" * path.count("/")
    body = re.sub(r"\[\[d:([\w-]+):(\d+)\]\]", lambda m: doodle(m.group(1), int(m.group(2))), body)
    out = head(title, desc, pre) + header(pre, active) + body.replace("{pre}", pre) + footer(pre) + "</body>\n</html>\n"
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(out)


def read(p):
    with open(os.path.join(ROOT, p)) as f:
        return f.read()


def guide_card(g, pre):
    slug, title, tag, blurb, status = g
    if status == "live":
        return f'<a href="{pre}guides/{slug}.html">{doodle(TAG_DOODLE.get(tag, "sun"), 64)}<span class="tag">{tag}</span><h3>{html.escape(title)}</h3><span class="small">{html.escape(blurb)}</span></a>'
    return f'<div class="soon">{doodle(TAG_DOODLE.get(tag, "sun"), 64)}<span class="tag">{tag} · coming soon</span><h3>{html.escape(title)}</h3><span class="small">{html.escape(blurb)}</span></div>'


# ---------- Ready-made kits ----------
TIERS = {
    "battery": ("Adventure Kings or VoltX lithium", "Renogy or iTechworld lithium", "REDARC, Enerdrive or Victron lithium",
                "Fine for weekends and lighter use; shorter warranty, fewer smarts.", "The sweet spot: app, cold-weather protection, longer warranty.", "Built for heavy use and big inverters, local support, longest warranties."),
    "allinone": ("Adventure Kings lithium power box", "iTechworld or Projecta all-in-one box", "REDARC or Enerdrive all-in-one system",
                 "Easiest start; smaller built-in chargers.", "Bigger chargers, a display or app, more plugs.", "A complete managed system, close to a pro fit-out."),
    "dcdc": ("Kings or Projecta DC-DC", "Renogy or Projecta DC-DC with solar input", "REDARC BCDC or Victron Orion",
             "Charges while you drive; often no solar input.", "Solar input built in, adjustable settings.", "App monitoring, handles heat and smart alternators well."),
    "solar": ("Kings folding blanket or fixed panels", "Renogy or Baintech panels", "REDARC or Victron panels",
              "Does the job; a bit heavier and less efficient.", "More power from the same size, copes with heat better.", "Most durable and efficient, long warranties."),
    "inverter": ("Projecta or Giandel pure sine", "Renogy pure sine", "Victron or Enerdrive pure sine",
                 "Fine for laptops and short use.", "Handles start-up surges like coffee machines better.", "Most efficient and quiet, built to run all day."),
    "monitor": ("Kings battery monitor", "Renogy shunt monitor", "Victron SmartShunt",
                "Shows a percentage; can drift.", "A shunt counts power in and out, so it's reliable.", "Very accurate, phone app with hours left and history."),
}

KITS = [
    {"slug": "weekender", "name": "Weekender", "doodle": "tent", "preset": "weekender",
     "who": "Two or three nights away, a medium fridge, lights and phones. You drive somewhere most days.",
     "runs": ["Medium 35 to 50L fridge", "4 LED lights, about 4 hours a night", "2 phones charging", "A 12V fan overnight", "Water pump"],
     "daily": "about 50Ah a day",
     "parts": [("Battery", "100Ah lithium", "battery", "Holds about two days of your use with no charging. About 11kg."),
               ("DC-DC charger", "25A, with solar input", "dcdc", "Driving 2 to 3 hours puts back more than you use in a day."),
               ("Solar", "150 to 200W portable blanket", "solar", "Optional, but handy for days you stay put. Point it at the sun and park in the shade."),
               ("Inverter", "Not needed", None, "Everything here runs on 12V or USB.")],
     "easy": "This size is perfect for an <b>all-in-one power box</b>: battery, DC-DC charger and solar input in one box you can move between cars. No installer needed for the box itself, just a proper Anderson plug lead from your engine battery.",
     "south": "Southern winters barely change this kit, because driving does most of the charging. If you often stay put in Victoria or Tasmania in winter, go for the 200W blanket."},
    {"slug": "long-trips", "name": "Long trips", "doodle": "van", "preset": "long",
     "who": "A week or more away, a bigger fridge and a laptop. Some days driving, some days parked up.",
     "runs": ["Large 55 to 75L fridge", "4 LED lights", "2 phones charging", "A laptop on a 12V or USB-C charger, about 3 hours a day", "A 12V fan overnight", "Water pump"],
     "daily": "about 65 to 75Ah a day",
     "parts": [("Battery", "200Ah lithium", "battery", "Two days of buffer for grey days. About 22kg."),
               ("DC-DC charger", "40A, with solar input", "dcdc", "Refills fast on driving days, and doubles as your solar regulator."),
               ("Solar", "200 to 300W fixed roof panels", "solar", "About 150W keeps up in Queensland; Victorian winters need closer to 250 to 300W."),
               ("Battery monitor", "Shunt type", "monitor", "Your fuel gauge, so you know exactly how many days you've got left."),
               ("Inverter", "Optional: 300 to 600W", "inverter", "Only if you'd rather use a normal laptop charger or charge camera batteries.")],
     "easy": "Separate parts suit this kit best, fitted by an auto electrician. Fixed roof panels are set-and-forget, and the 200Ah battery gives room to add a small inverter later.",
     "south": "In a Victorian or Tasmanian winter, plan on the bigger end of the solar range, or add a 200W blanket for long parked spells."},
    {"slug": "living-in-it", "name": "Living in it", "doodle": "cup", "preset": "living",
     "who": "Full-time or close to it. Fridge-freezer, working from the van, a diesel heater, Starlink and a morning coffee.",
     "runs": ["Big 80 to 100L fridge-freezer", "6 LED lights", "2 phones, a laptop about 5 hours a day", "Starlink Mini about 6 hours a day", "Diesel heater electrics", "12V fan and water pump", "A 1,300W coffee machine, once a day"],
     "daily": "about 120Ah a day",
     "parts": [("Battery", "460Ah lithium (or 2 × 230Ah)", "battery", "Three days of buffer, about 51kg. A serious system, priced like one."),
               ("DC-DC charger", "50A, with solar input", "dcdc", "Big battery, big charger, so driving days count."),
               ("Solar", "550 to 600W fixed roof panels", "solar", "Keeps up most of the year up north. Fills most van roofs."),
               ("Inverter", "2,000W pure sine", "inverter", "Handles the coffee machine's start-up surge. Needs thick cables and a proper fit."),
               ("Battery monitor", "Shunt type", "monitor", "Essential at this size.")],
     "easy": "This is a full install job: separate parts, fitted and fused by an auto electrician. Ask them about a lithium-ready battery charger too, for when you plug in at a campsite.",
     "south": "<b>Southern winters are the catch.</b> In a Victorian winter this setup would want about 1,150W of solar, which won't fit on a van roof. Plan on a 200 to 400W portable blanket, plugging in at a powered site every few days, or a small inverter generator for grey spells."},
]


def tier_cards(key):
    t = TIERS[key]
    out = '<div class="tiers">'
    for i, label in enumerate(["Budget", "Mid-range", "Premium"]):
        out += f'<a href="#" data-affiliate="placeholder" onclick="return false"><b>{label}</b><span class="pick">{t[i]}</span><span class="tn">{t[i+3]}</span></a>'
    return out + '</div>'


def build_kits():
    os.makedirs(os.path.join(ROOT, "kits"), exist_ok=True)
    cards = ''.join(f'<a class="card" href="{{pre}}kits/{k["slug"]}.html">[[d:{k["doodle"]}:110]]<h3>{k["name"]}</h3><p>{k["who"]}</p><span class="go">See the full kit →</span></a>' for k in KITS)
    hub = ('<main class="page"><div class="crumbs"><a href="{pre}index.html">Home</a> › Kits</div>'
           '<div class="sec-head"><h1 style="font-size:3rem;margin:4px 0 8px">Ready-made kits</h1>[[d:fridge:100]]</div>'
           '<p class="hint" style="margin-bottom:26px">Three tried-and-tested sizes. Pick the one that sounds most like you, see everything in it, then fine-tune it in the Power Planner.</p>'
           f'<div class="cards">{cards}</div>'
           '<div class="aside" style="margin-top:30px">Not quite you? The <a href="{pre}planner.html" style="color:var(--sign)">Power Planner</a> sizes a kit around exactly what you run and where you travel.</div></main>')
    page("kits/index.html", "Ready-made kits", "Three ready-made power kits for Australian vans, caravans and 4WDs: Weekender, Long trips and Living in it.", hub, "kits/index.html")
    for k in KITS:
        parts = ""
        for name, size, key, note in k["parts"]:
            parts += f'<div class="kit-part"><div class="kp-head"><h3>{name}</h3><span class="kp-size">{size}</span></div><p>{note}</p>{tier_cards(key) if key else ""}</div>'
        body = (f'<main class="article"><div class="crumbs"><a href="{{pre}}index.html">Home</a> › <a href="{{pre}}kits/index.html">Kits</a> › {k["name"]}</div>'
                f'[[d:{k["doodle"]}:150]]'.replace('<svg class="doodle"', '<svg class="doodle guide-doodle"') +
                f'<h1>The {k["name"]} kit</h1><div class="meta"><span>Uses {k["daily"]}</span><span>Sized for a campervan</span><a href="{{pre}}disclosure.html">How we make money</a></div>'
                f'<p class="hint" style="font-size:1.15rem">{k["who"]}</p>'
                '<div class="tldr"><h2>What it runs</h2><ul>' + ''.join(f'<li>{r}</li>' for r in k["runs"]) + '</ul></div>'
                f'<h2>What\'s in the kit</h2>{parts}'
                '<div class="kit-part"><div class="kp-head"><h3>The bits that hold it together</h3></div><ul><li>Battery box or mount, to hold it firmly in place</li><li>Correctly sized cables and lugs</li><li>Fuses or circuit breakers on every circuit</li><li>An isolator switch</li><li>Anderson plugs and a fuse block</li></ul><p class="small">Your auto electrician sizes these for your exact install.</p></div>'
                f'<h2>Easiest way to build it</h2><p>{k["easy"]}</p>'
                f'<h2>Travelling south in winter?</h2><p>{k["south"]}</p>'
                f'<div class="cta-box"><p>Change anything you like: your fridge, your state, how much you drive. The Power Planner starts from this kit.</p><a class="btn-link" href="{{pre}}planner.html#{k["preset"]}">Customise this kit</a></div>'
                '<div class="aside" style="margin:24px 0"><b>Get a pro to wire it in.</b> Have a licensed auto electrician install or check your setup, with the right cable sizes and fuses. Sizes here are estimates for typical use.</div>'
                '<p class="small">Product links are placeholders while we finalise our store partners. Brands are examples of each price level.</p>'
                '</main>')
        page(f"kits/{k['slug']}.html", f"The {k['name']} kit", f"Everything in the {k['name']} power kit for an Australian campervan: battery, solar, DC-DC charger and more, with budget to premium options.", body, "kits/index.html")


def build():
    # Home
    page("index.html", SITE, "Free plain-English power planner and guides for Australian vans, caravans and 4WDs. Work out the battery, solar and charger you need.", read("content/home.html"))
    # Guides hub
    hub = '<main class="page"><div class="crumbs"><a href="{pre}index.html">Home</a> › Guides</div>'
    hub += '<div class="sec-head"><h1 style="font-size:3rem;margin:4px 0 8px">Guides</h1>[[d:road:120]]</div><p class="hint" style="margin-bottom:22px">Plain-English guides to off-grid power. New ones land every week. Start at the top if you\'re new to all this.</p>'
    hub += '<div class="guide-list">' + "".join(guide_card(g, "{pre}") for g in GUIDES) + '</div></main>'
    page("guides/index.html", "Guides", "Plain-English guides to batteries, solar, DC-DC chargers and inverters for Australian vans, caravans and 4WDs.", hub, "guides/index.html")
    # Each live guide
    for i, g in enumerate(GUIDES):
        slug, title, tag, blurb, status = g
        if status != "live":
            continue
        body = read(f"content/guides/{slug}.html")
        others = [x for x in GUIDES if x[0] != slug][:4]
        rel = '<div class="related"><h2 style="font-size:1.4rem;margin:0 0 12px">Keep reading</h2><div class="guide-list">' + "".join(guide_card(x, "{pre}") for x in others) + '</div></div>'
        dd = doodle(TAG_DOODLE.get(tag, "sun"), 130, cls="doodle guide-doodle")
        wrapped = f'<main class="article"><div class="crumbs"><a href="{{pre}}index.html">Home</a> › <a href="{{pre}}guides/index.html">Guides</a> › {tag}</div>{dd}{body}{rel}</main>'
        page(f"guides/{slug}.html", title.split(":")[0], blurb, wrapped, "guides/index.html")
    # Info pages
    for name, title, desc in [("about", "About", "Who is behind Off-Grid Sorted, and why it exists."),
                              ("disclosure", "Affiliate disclosure & disclaimer", "How Off-Grid Sorted earns money, and the limits of our advice."),
                              ("privacy", "Privacy", "How Off-Grid Sorted handles your information.")]:
        page(f"{name}.html", title, desc, '<main class="article"><div class="crumbs"><a href="{pre}index.html">Home</a> › ' + title + '</div>' + read(f"content/{name}.html") + '</main>', f"{name}.html" if name == "about" else "")
    build_kits()
    # Refresh planner chrome
    p = read("planner.html")
    p = re.sub(r'<header class="site-header">.*?</header>\n', lambda m: header("", "planner.html"), p, flags=re.S)
    p = re.sub(r'<footer class="site-footer">.*?</footer>\n', lambda m: footer(""), p, flags=re.S)
    with open(os.path.join(ROOT, "planner.html"), "w") as f:
        f.write(p)


if __name__ == "__main__":
    build()
    print("built")
