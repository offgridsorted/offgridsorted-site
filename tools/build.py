#!/usr/bin/env python3
"""Builds Off-Grid Sorted's static pages from content fragments.

Run from the repo root:  python3 tools/build.py
- content/home.html            -> index.html
- content/guides/<slug>.html   -> guides/<slug>.html   (listed in GUIDES below)
- guides/index.html            -> built from GUIDES
- about/disclosure/privacy     -> from content/<name>.html
The Power Planner (planner.html) is hand-written; this script only refreshes its header and footer.
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "Off-Grid Sorted"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Caveat:wght@500;700&family=Permanent+Marker&family=Kalam:wght@700&display=swap" rel="stylesheet">')

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

NAV = [("planner.html", "Power Planner"), ("guides/index.html", "Guides"), ("about.html", "About")]


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
    <a class="logo" href="{pre}index.html" aria-label="Off-Grid Sorted home">{logo(118)}</a>
    <nav class="nav" aria-label="Main menu">{links}<a class="cta" href="{pre}planner.html">Plan my setup</a></nav>
    <details class="menu-toggle"><summary>Menu</summary><div class="drop">{drop}<a href="{pre}planner.html"><b>Plan my setup →</b></a></div></details>
  </div>
</header>
'''


def footer(pre):
    live = [g for g in GUIDES if g[4] == "live"]
    glinks = "".join(f'<a href="{pre}guides/{g[0]}.html">{html.escape(g[1].split(":")[0])}</a>' for g in live)
    return f'''<footer class="site-footer">
  <div class="in">
    <div class="about">
      <div style="color:var(--ink)">{logo(130, "F")}</div>
      <p>Plain-English help to get the power setup in your van, caravan or 4WD sorted. Independent and Australian.</p>
      <p class="small">Some links earn us a small commission at no cost to you. <a href="{pre}disclosure.html" style="display:inline;color:var(--sign)">How we make money</a>.</p>
    </div>
    <div><h4>Tools</h4><a href="{pre}planner.html">Power Planner</a><a href="{pre}planner.html#check">Check what I've got</a></div>
    <div><h4>Guides</h4>{glinks}<a href="{pre}guides/index.html">All guides</a></div>
    <div><h4>Off-Grid Sorted</h4><a href="{pre}about.html">About</a><a href="{pre}disclosure.html">Disclosure &amp; disclaimer</a><a href="{pre}privacy.html">Privacy</a><a href="https://www.instagram.com/offgridsorted" rel="noopener">Instagram</a></div>
  </div>
  <p class="small" style="max-width:1080px;margin:0 auto;padding:0 18px 24px">© 2026 Off-Grid Sorted. Estimates only. Always have a licensed auto electrician install or check your system.</p>
</footer>
'''


def page(path, title, desc, body, active=""):
    pre = "../" * path.count("/")
    out = head(title, desc, pre) + header(pre, active) + body.replace("{pre}", pre) + footer(pre) + "</body>\n</html>\n"
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(out)


def read(p):
    with open(os.path.join(ROOT, p)) as f:
        return f.read()


def guide_card(g, pre):
    slug, title, tag, blurb, status = g
    if status == "live":
        return f'<a href="{pre}guides/{slug}.html"><span class="tag">{tag}</span><h3>{html.escape(title)}</h3><span class="small">{html.escape(blurb)}</span></a>'
    return f'<div class="soon"><span class="tag">{tag} · coming soon</span><h3>{html.escape(title)}</h3><span class="small">{html.escape(blurb)}</span></div>'


def build():
    # Home
    page("index.html", SITE, "Free plain-English power planner and guides for Australian vans, caravans and 4WDs. Work out the battery, solar and charger you need.", read("content/home.html"))
    # Guides hub
    hub = '<main class="page"><div class="crumbs"><a href="{pre}index.html">Home</a> › Guides</div>'
    hub += '<h1 style="font-size:3rem;margin:4px 0 8px">Guides</h1><p class="hint" style="margin-bottom:22px">Plain-English guides to off-grid power. New ones land every week. Start at the top if you\'re new to all this.</p>'
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
        wrapped = f'<main class="article"><div class="crumbs"><a href="{{pre}}index.html">Home</a> › <a href="{{pre}}guides/index.html">Guides</a> › {tag}</div>{body}{rel}</main>'
        page(f"guides/{slug}.html", title.split(":")[0], blurb, wrapped, "guides/index.html")
    # Info pages
    for name, title, desc in [("about", "About", "Who is behind Off-Grid Sorted, and why it exists."),
                              ("disclosure", "Affiliate disclosure & disclaimer", "How Off-Grid Sorted earns money, and the limits of our advice."),
                              ("privacy", "Privacy", "How Off-Grid Sorted handles your information.")]:
        page(f"{name}.html", title, desc, '<main class="article"><div class="crumbs"><a href="{pre}index.html">Home</a> › ' + title + '</div>' + read(f"content/{name}.html") + '</main>', f"{name}.html" if name == "about" else "")
    # Refresh planner chrome
    p = read("planner.html")
    p = re.sub(r'<header class="site-header">.*?</header>\n', lambda m: header("", "planner.html"), p, flags=re.S)
    p = re.sub(r'<footer class="site-footer">.*?</footer>\n', lambda m: footer(""), p, flags=re.S)
    with open(os.path.join(ROOT, "planner.html"), "w") as f:
        f.write(p)


if __name__ == "__main__":
    build()
    print("built")
