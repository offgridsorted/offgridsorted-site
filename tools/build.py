#!/usr/bin/env python3
"""Builds Off-Grid Sorted's static pages from content fragments.

Run from the repo root:  python3 tools/build.py
- content/home.html            -> index.html
- content/guides/<slug>.html   -> guides/<slug>.html   (listed in GUIDES below)
- guides/index.html            -> built from GUIDES
- about/disclosure/privacy     -> from content/<name>.html
The Power Planner (planner.html) is hand-written; this script only refreshes its header and footer.
"""
import json, os, re, html, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doodles import doodle, horizon, TAG_DOODLE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "Off-Grid Sorted"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@600;700;800&family=Barlow:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Caveat:wght@500;700&family=Permanent+Marker&family=Kalam:wght@700&display=swap" rel="stylesheet">')

# Guides: (slug, title, tag, blurb, status)  status "live" or "soon"
GUIDES = [
    ("van-power-basics", "Van power in plain English: the four parts and how they fit", "Start here",
     "Battery, solar, DC-DC charger and inverter, explained without the jargon.", "live"),
    ("lithium-vs-agm", "Lithium vs AGM: which battery should you get?", "Batteries",
     "The real difference, what it means for size, weight and cost, and when AGM still makes sense.", "live"),
    ("how-much-solar-australia", "How much solar do I need? By state and season", "Solar",
     "Why a Hobart winter and a Darwin winter need very different setups, with a table for every state.", "live"),
    ("dc-dc-chargers-explained", "DC-DC chargers explained: charging while you drive", "Charging",
     "What they do, what size you need, and why modern cars with smart alternators need one.", "live"),
    ("caravan-power-setup", "Caravan power: getting charge through the trailer plug", "Caravans",
     "Why caravans lose charge over long cables, and how to fix it.", "live"),
    ("4wd-dual-battery-basics", "4WD dual battery basics", "4WDs",
     "Under-bonnet or in the tray, smart alternators, and fitting solar on a 4WD.", "live"),
    ("will-my-fridge-last", "How long will a 100Ah battery run my fridge?", "Fridges",
     "How much power camping fridges really use, and how to make yours sip less.", "live"),
    ("portable-power-stations", "Portable power stations vs a proper dual battery setup", "Batteries",
     "When an all-in-one box is all you need, and when it isn't.", "live"),
    ("battery-size-for-12v-fridge", "What size battery do I need for a 12V fridge?", "Fridges",
     "Size your battery for your fridge: daily use, usable capacity and days without charging, with a simple table.", "live"),
    ("fridge-flattening-battery", "Why is my fridge flattening my battery?", "Fridges",
     "Fridge beeping or flattening your battery? Check charging, the battery, cut-out, cables and heat, in that order.", "live"),
    ("lithium-under-the-bonnet", "Can I put a lithium battery under the bonnet?", "Batteries",
     "Why most lithium batteries don't belong in a hot engine bay, which ones do, and better places to fit one.", "live"),
    ("smart-alternator-check", "Does my car have a smart alternator?", "Charging",
     "Two quick checks to spot a smart alternator, a list of common Aussie vehicles, and what to do if you have one.", "live"),
    ("caravan-not-charging-while-driving", "Caravan battery not charging while driving? A step-by-step fix", "Caravans",
     "A step-by-step checklist: tow bar power, cable size, Anderson plugs, alternator, DC-DC charger and battery.", "live"),
    ("solar-blanket-vs-fixed-panel", "Solar blanket vs fixed panel: which suits you?", "Solar",
     "Shade, driving, theft, weight, heat and cost per watt compared, plus who each one suits and why many get both.", "live"),
    ("winter-solar-not-keeping-up", "Winter solar: why your panels aren't keeping up", "Solar",
     "Short days, a low sun and long shadows, with BOM-based winter numbers for every state and what helps.", "live"),
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

FAQS = {
    "van-power-basics": [
        ("What do I need for off-grid power in a van?", "A battery to store power, solar panels and a DC-DC charger to fill it up, and an inverter only if you want normal 240V plugs. Size everything from one number: how much power you use in a day."),
        ("What does a DC-DC charger do?", "It charges your second battery from the car while you drive. It works properly with modern smart alternators, which a simple isolator doesn't."),
        ("Do I need an inverter in my van?", "Only if you want to run things with a normal 240V plug. Fridges, lights, fans and USB chargers run straight off 12V, which wastes less power."),
    ],
    "lithium-vs-agm": [
        ("Is lithium better than AGM for a van or caravan?", "For most vans, caravans and 4WDs, yes. You can use almost all of a lithium battery but only about half of an AGM, so AGM needs to be about twice the size and ends up around three to four times heavier. Lithium costs more upfront but lasts many more years."),
        ("What size AGM battery equals a 100Ah lithium?", "About 200Ah, because you can only use about half of an AGM's rated capacity without shortening its life."),
        ("Can a lithium battery charge in freezing weather?", "Most lithium batteries shouldn't be charged below 0°C. If you camp somewhere frosty, pick one with a built-in heater."),
    ],
    "how-much-solar-australia": [
        ("How do I work out how much solar I need?", "Work out how much power you use in a day, divide it by the peak sun hours where you'll be, then allow for real-world losses. Our Power Planner does this with Bureau of Meteorology averages for each state and season."),
        ("How much more solar do I need in winter?", "In southern Australia, winter can need two to four times more solar than summer for the same daily use."),
        ("What if the solar I need won't fit on my roof?", "Add a portable panel or solar blanket you can put in the sun while you park in the shade, or plan to drive or plug in more often."),
    ],
    "dc-dc-chargers-explained": [
        ("How much does a DC-DC charger charge per hour of driving?", "Roughly up to its amp rating. A 25A charger puts back about 22 to 25Ah for every hour you drive. Towing a caravan with the charger in the van, plan on about a third less."),
        ("Do I need a DC-DC charger with a smart alternator?", "Yes. Smart alternators lower their voltage to save fuel, so a simple isolator won't charge your second battery properly. A DC-DC charger fixes that."),
        ("Can a DC-DC charger take solar too?", "Most do. Many DC-DC chargers have a solar input built in, so one box handles both driving and solar."),
    ],
    "caravan-power-setup": [
        ("Can I charge my caravan battery through the trailer plug?", "Not well. The cable from the car to the caravan battery is long and usually thin, so a lot of charge is lost on the way. The trailer plug alone can't charge a caravan battery properly."),
        ("What's the best way to charge a caravan battery while driving?", "Run a heavy cable to an Anderson plug at the tow bar, and fit a DC-DC charger in the caravan, close to the battery. Have a licensed auto electrician fit it."),
        ("How much charge will my caravan get from driving?", "Plan on about a third less than the charger's label, because of the long cable between the car and the van."),
    ],
    "4wd-dual-battery-basics": [
        ("Do I need a DC-DC charger or an isolator in my 4WD?", "Many 4WDs built since about 2015 have a smart alternator, so you need a DC-DC charger rather than a simple isolator."),
        ("What size dual battery do I need for a weekend?", "For a fridge-and-lights weekend, around 100Ah of lithium with a 25A DC-DC charger is a common starting point."),
        ("Can a lithium battery go under the bonnet?", "It's best kept out of engine heat. If it has to go under the bonnet, choose a battery rated for it and get your auto electrician's advice."),
    ],
    "will-my-fridge-last": [
        ("How much power does a 12V camping fridge use?", "A typical 35 to 50 litre compressor fridge uses about 20 to 30Ah a day, depending mostly on how hot it is."),
        ("How long will a 100Ah battery run a fridge?", "A 100Ah lithium battery runs a typical 35 to 50 litre fridge on its own for about three days in summer with no charging. A 100Ah AGM gets you closer to two."),
        ("How can I make my fridge use less power?", "Pre-cool it at home, keep it full, keep it in the shade and set it to 3 to 4°C. Those four habits save more power than anything you can buy."),
    ],
    "portable-power-stations": [
        ("Can I charge a portable power station from my car?", "Yes, but charging from the cigarette socket is very slow, often around 100W, so a day of driving may not fill it."),
        ("Is a portable power station or a dual battery better?", "A power station is easiest but charges slowly from the car. A 12V power box charges several times faster while you drive and can still move between cars. A fixed dual battery costs the most but suits regular trips and bigger setups."),
        ("What's the difference between Wh and Ah?", "Watt-hours (Wh) are amp-hours (Ah) multiplied by the voltage. At 12V, a 1,000Wh power station holds roughly 80Ah, so don't compare the two numbers directly."),
    ],
    "battery-size-for-12v-fridge": [
        ("What size battery do I need for a 35 to 50L fridge?", "A medium fridge uses about 28Ah a day in summer. A 100Ah lithium battery runs it for about three days with no charging, and a 100Ah AGM for closer to two. These are estimates."),
        ("How much of an AGM or lithium battery can I use?", "About 50% of an AGM, because running it lower shortens its life. About 80 to 100% of a lithium battery depending on the brand, and our planner counts 90%."),
        ("Can I run my fridge off my car's starter battery?", "Not for long. A starter battery is built for a short burst to start the engine and can be damaged by being run down too often, and a flat one means the car won't start. Use a second, deep cycle battery."),
    ],
    "fridge-flattening-battery": [
        ("Why does my 12V fridge beep and switch off?", "Usually its low-voltage cut-out has kicked in because the voltage reaching it is too low. That can be a flat battery, a cut-out setting that's too high, or voltage lost on thin or long cables and plugs."),
        ("What battery protection setting should I use?", "Dometic recommends High or Medium when running from a starter battery, and Low for a second battery. Low suits lithium, but on an AGM it can let the battery get close to flat, so Medium or a battery monitor is safer."),
        ("Why does my battery go flat after a few days of camping?", "Most often the battery isn't getting enough charge back each day. A roof panel that looks big enough on paper can fall a little short every day, especially when you stay put or park in shade. A portable solar blanket you can aim at the sun helps."),
    ],
    "lithium-under-the-bonnet": [
        ("Can a lithium battery go in the engine bay?", "Usually not. Engine bays often sit around 50 to 60\u00b0C and go above 70\u00b0C on hot days, while many lithium batteries are rated to about 45 to 60\u00b0C. Only fit one there if the maker says in writing it's designed for the engine bay."),
        ("Will mounting lithium under the bonnet void the warranty?", "It can. REDARC notes battery makers won't warrant batteries mounted in high heat, and even batteries built for engine bays may carry a shorter under-bonnet warranty."),
        ("Where should I put a lithium battery instead?", "The canopy, tray, cabin or rear of a wagon or van, out of direct sun with good airflow. Mount the DC-DC charger close to the battery, ideally within about 1 metre, as REDARC recommends."),
    ],
    "smart-alternator-check": [
        ("How can I tell if my car has a smart alternator?", "Look for a battery sensor on the starter battery's terminals, usually the negative. REDARC says that sensor is the sign of a smart alternator. You can also check the voltage with a multimeter after a drive: readings that sag towards 12.5V or lower suggest a smart one."),
        ("Does the Ford Ranger have a smart alternator?", "Yes, CarsGuide lists the Ford Ranger as having a smart alternator. REDARC says a Ranger with Smart Charge doesn't need the system disabled, just a compatible DC-DC charger."),
        ("Can I use an isolator with a smart alternator?", "Not well. REDARC says a smart alternator's voltage is often as low as 12.3V, which is too low to charge a deep cycle battery, and recommends a DC-DC charger instead of its simple isolator."),
    ],
    "caravan-not-charging-while-driving": [
        ("Why is my caravan battery not charging from the car?", "The most common causes are a blown fuse or dead ignition trigger in the car, cable that's too thin for the distance, or a smart alternator with no DC-DC charger in the van. Work from the car back to the van to find it."),
        ("Why does my caravan battery only show 13.3V while driving?", "It may simply be full. REDARC says its BCDC chargers drop to a float voltage of 13.3V once the battery is full, so check the charger's lights or app first."),
        ("How much should my caravan charge while driving?", "Less than the charger's label. Our Power Planner counts about 65% of the charger's rated amps for a caravan, so a 25A charger putting in about 16A is in line with what we'd expect."),
    ],
    "solar-blanket-vs-fixed-panel": [
        ("Is a solar blanket better than a fixed panel?", "It depends on how you camp. A blanket lets you park in the shade and put the panel in the sun, but it can't charge while driving and is easy to steal. A fixed panel charges whenever there's sun, including on the road, with no setup."),
        ("Can a solar blanket charge while driving?", "No. REDARC says its solar blankets must be disconnected and securely stored when the vehicle is moving. Only fixed panels charge on the road."),
        ("Do solar panels lose power in the heat?", "Yes. SolarQuotes says a typical panel loses about 0.4% of its output for every degree above 25\u00b0C, so a 300W panel at 45\u00b0C gives about 276W."),
    ],
    "winter-solar-not-keeping-up": [
        ("Why is my solar not keeping up in winter?", "Shorter days, a low sun that hits flat roof panels at a glancing angle, and longer shadows. In southern Australia a winter day can hold only a quarter to a half of a summer day's sun, based on Bureau of Meteorology averages."),
        ("How much does a 200W solar panel make in winter?", "As a rough estimate after real-world losses, about 47Ah a day in Queensland, 34Ah in New South Wales, 22Ah in Victoria and 19Ah in Tasmania, using capital city averages."),
        ("How can I get more from my solar in winter?", "Point a portable panel or blanket at the sun and move it during the day, park in the open, keep panels clean, top up by driving through a DC-DC charger, and use a bit less power."),
    ],
}


NAV = [("kits/index.html", "Kits"), ("guides/index.html", "Guides"), ("about.html", "About")]


def logo(w=120, ident="H"):
    return LOGO.format(w=w, h=round(w * 300 / 420), id=ident)


BASE = "https://offgridsorted.com.au/"
BUILT = []


def git_date(rel):
    import subprocess
    try:
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except Exception:
        d = ""
    return d or datetime.date.today().isoformat()


LD = {}  # path -> list of JSON-LD objects
ORG_ID = BASE + "#org"
PEOPLE = [{"@type": "Person", "@id": BASE + "about.html#kiran", "name": "Kiran", "url": BASE + "about.html", "description": "Co-founder of Off-Grid Sorted. Van life since converting a Mitsubishi Delica in Japan about 15 years ago; the more electrical-minded half."},
          {"@type": "Person", "@id": BASE + "about.html#mitch", "name": "Mitch", "url": BASE + "about.html", "description": "Co-founder of Off-Grid Sorted. Road-trip co-pilot who handles the building side of van conversions."}]
ORG = {"@type": "Organization", "@id": ORG_ID, "name": "Off-Grid Sorted", "url": BASE,
       "logo": BASE + "favicon.svg", "sameAs": ["https://www.instagram.com/offgridsorted"], "email": "hello@offgridsorted.com.au",
       "founder": [{"@id": p["@id"]} for p in PEOPLE], "areaServed": "AU",
       "description": "Independent, plain-English help working out off-grid power (battery, solar, DC-DC charger, inverter) for Australian campervans, caravans and 4WDs."}


def ld_json(path):
    items = LD.get(path)
    if not items:
        return ""
    data = {"@context": "https://schema.org", "@graph": items}
    return '\n<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + '</script>'


def seo_tags(path, full, desc):
    url = BASE + ("" if path == "index.html" else path)
    t, d = html.escape(full), html.escape(desc)
    ogtype = "article" if path.startswith("guides/") and path != "guides/index.html" else "website"
    return (f'<!--seo--><link rel="canonical" href="{url}">\n'
            f'<meta property="og:type" content="{ogtype}">\n<meta property="og:site_name" content="Off-Grid Sorted">\n'
            f'<meta property="og:title" content="{t}">\n<meta property="og:description" content="{d}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{BASE}assets/og.png">\n'
            f'<meta property="og:locale" content="en_AU">\n<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="theme-color" content="#f3f0e8">{ld_json(path)}<!--/seo-->')


def head(title, desc, pre, path="index.html"):
    full = f"{title} · {SITE}" if title != SITE else f"{SITE} · Off-grid power for Australian vans, caravans and 4WDs"
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="commission-factory-verification" content="8343a658ff4a419980598ffe7dfdd01d">
{seo_tags(path, full, desc)}
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
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="in">
    <a class="logo" href="{pre}index.html" aria-label="Off-Grid Sorted home">{logo(170)}</a>
    <nav class="nav" aria-label="Main menu">{links}<a class="cta" href="{pre}planner.html"{' aria-current="page"' if active == "planner.html" else ""}>Power Planner</a></nav>
    <details class="menu-toggle"><summary>Menu</summary><div class="drop"><a href="{pre}planner.html"><b>Power Planner →</b></a>{drop}<a href="{pre}contact.html">Contact</a></div></details>
  </div>
</header>
'''


def footer(pre):
    live = [g for g in GUIDES if g[4] == "live"]
    short = {"van-power-basics": "Van power basics", "lithium-vs-agm": "Lithium vs AGM", "how-much-solar-australia": "How much solar?",
             "dc-dc-chargers-explained": "DC-DC chargers", "will-my-fridge-last": "Will my fridge last?"}
    glinks = "".join(f'<a href="{pre}guides/{g[0]}.html">{short[g[0]]}</a>' for g in live if g[0] in short)
    return f'''<footer class="site-footer">
  {horizon()}
  <div class="in">
    <div class="about">
      <div style="color:var(--ink)">{logo(130, "F")}</div>
      <p>Plain-English help to get the power setup in your van, caravan or 4WD sorted. Independent and Australian, made by Kiran and Mitch on the Gold Coast.</p>
      <p class="small">Some links earn us a small commission at no cost to you. <a href="{pre}disclosure.html" style="display:inline;color:var(--sign)">How we make money</a>.</p>
    </div>
    <div><p class="fh">Tools</p><a href="{pre}planner.html">Power Planner</a><a href="{pre}planner.html#check">Check what I've got</a><a href="{pre}kits/index.html">Ready-made kits</a><a href="{pre}embed.html">Put the planner on your site</a></div>
    <div><p class="fh">Guides</p>{glinks}<a href="{pre}guides/index.html">All guides</a></div>
    <div><p class="fh">Off-Grid Sorted</p><a href="{pre}about.html">About</a><a href="{pre}disclosure.html">Disclosure &amp; disclaimer</a><a href="{pre}privacy.html">Privacy</a><a href="{pre}contact.html">Contact</a><a href="https://instagram.com/offgridsorted" rel="noopener">Instagram</a></div>
  </div>
  <p class="small" style="max-width:1080px;margin:0 auto;padding:0 18px 24px">© 2026 Off-Grid Sorted. Estimates only. Always have a licensed auto electrician install or check your system.</p>
</footer>
'''


MENU_JS = """<script data-menu>
(function(){var m=document.querySelector('.menu-toggle');if(!m)return;var s=m.querySelector('summary');
function set(){s.textContent=m.open?'Close':'Menu';}m.addEventListener('toggle',set);
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&m.open){m.open=false;s.focus();}});
document.addEventListener('click',function(e){if(m.open&&!m.contains(e.target))m.open=false;});
m.querySelectorAll('.drop a').forEach(function(a){a.addEventListener('click',function(){m.open=false;});});})();
</script>
"""


def page(path, title, desc, body, active=""):
    pre = "../" * path.count("/")
    body = re.sub(r"\[\[d:([\w-]+):(\d+)\]\]", lambda m: doodle(m.group(1), int(m.group(2))), body)
    BUILT.append(path)
    body = body.replace("<main ", '<main id="main" ', 1)
    out = head(title, desc, pre, path) + header(pre, active) + body.replace("{pre}", pre) + footer(pre) + MENU_JS + "</body>\n</html>\n"
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(out)


def page_abs(path, title, desc, body):
    """Like page() but with root-absolute links, for pages served at any URL (404)."""
    BUILT.append(path)
    body = re.sub(r"\[\[d:([\w-]+):(\d+)\]\]", lambda m: doodle(m.group(1), int(m.group(2))), body)
    body = body.replace("<main ", '<main id="main" ', 1)
    out = head(title, desc, "/", path) + header("/") + body + footer("/") + MENU_JS + "</body>\n</html>\n"
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
# Real product picks live in data/products.json (main pick + other options per tier).
PRODUCTS = json.load(open(os.path.join(ROOT, "data", "products.json")))
TIER_NAMES = ["Budget", "Mid-range", "Premium"]

# Affiliate tracking, by shop website. data/products.json keeps the plain shop links
# (the price check needs them); the tracking wrapper is only added to the built pages.
# Add a shop here when its program approves us. {u} is the URL-encoded product link.
AFFILIATES = {
    "au.renogy.com": "https://renogy.sjv.io/c/8106624/1182656/14864?u={u}",  # Impact, approved 4 Nov 2026
}


def aff(url):
    from urllib.parse import urlparse, quote
    tpl = AFFILIATES.get(urlparse(url).netloc.lower())
    return tpl.format(u=quote(url, safe="")) if tpl else url


def apply_affiliates():
    for ps in PRODUCTS["cats"].values():
        for p in ps:
            if p.get("url"):
                p["url"] = aff(p["url"])
            for st in p.get("stores", []):
                if st.get("url"):
                    st["url"] = aff(st["url"])


apply_affiliates()


def normalise_products():
    """Give every product a sorted 'stores' list (in stock, then cheapest) and set
    price/store/url to the best one, so totals always use the cheapest in-stock shop."""
    for ps in PRODUCTS["cats"].values():
        for p in ps:
            st = p.get("stores") or [{"store": p["store"], "price": p.get("price"), "url": p.get("url"), "was": p.get("rrp")}]
            st = [x for x in st if x.get("url")]
            st.sort(key=lambda x: (x.get("in_stock") is False, x.get("price") is None, x.get("price") or 0))
            p["stores"] = st
            best = next((x for x in st if x.get("price") and x.get("in_stock") is not False), st[0] if st else None)
            if best:
                p["price"], p["store"], p["url"] = best.get("price") or p.get("price"), best["store"], best["url"]
                p["rrp"] = best.get("was")


normalise_products()


def money(n):
    return f"${n:,.0f}"


def pick_for(cat, tier, role="main"):
    return [p for p in PRODUCTS["cats"][cat] if p["tier"] == tier and p["role"] == role]


def facts(p):
    bits = []
    if p.get("warranty"):
        bits.append(f'{p["warranty"]}-yr warranty')
    if p.get("kg"):
        bits.append(f'{p["kg"]:g}kg')
    return " · ".join(bits)


def where_to_buy(p):
    st = p.get("stores") or []
    if len(st) < 2:
        return ""
    out = '<ul class="wtb">'
    for x in st:
        pr = money(x["price"]) if x.get("price") else "Check price"
        was = f' <s>{money(x["was"])}</s>' if x.get("was") and x.get("price") and x["was"] > x["price"] else ""
        sold = f' <em>{html.escape(x["label"])}</em>' if x.get("label") else (' <em>sold out</em>' if x.get("in_stock") is False else "")
        out += f'<li><a href="{html.escape(x["url"])}" target="_blank" rel="sponsored nofollow noopener">{html.escape(x["store"])}</a><span>{pr}{was}{sold}</span></li>'
    return out + '</ul>'


def product_line(p, main=True):
    multi = len(p.get("stores") or []) > 1
    price = ("About " if p.get("approx") else ("From " if multi else "")) + money(p["price"]) if p.get("price") else "Check price"
    was = f' <s>{money(p["rrp"])}</s>' if p.get("rrp") and p.get("price") and p["rrp"] > p["price"] and not multi else ""
    url = html.escape(p["url"]) if p.get("url") else "#"
    cls = "prod" if main else "prod alt"
    return (f'<div class="{cls}"><a class="pname" href="{url}" rel="sponsored nofollow noopener" target="_blank">{html.escape(p["name"])}</a>'
            f'<span class="price">{price}{was} <span class="store">at {html.escape(p["store"])}</span></span>'
            + (f'<span class="facts">{facts(p)}</span>' if facts(p) else "")
            + f'<span class="tn">{html.escape(p["why"])}</span>'
            + (f'<span class="tn down">Catch: {html.escape(p["downside"])}</span>' if p.get("downside") else "")
            + where_to_buy(p)
            + f'<button type="button" class="add-list" data-item="{html.escape(json.dumps({"n": p["name"], "p": p.get("price"), "s": p.get("store"), "u": p.get("url"), "a": bool(p.get("approx"))}))}">+ Add to my list</button>'
            + '</div>')


def tier_cards(cat):
    out = '<div class="tiers">'
    for t in TIER_NAMES:
        mains = pick_for(cat, t)
        if not mains:
            continue
        others = pick_for(cat, t, "other")
        out += f'<div class="tier"><b>{t}</b>{product_line(mains[0])}'
        if others:
            out += f'<details class="more"><summary>Other good options ({len(others)})</summary>' + ''.join(product_line(o, False) for o in others) + '</details>'
        out += '</div>'
    return out + '</div>'


def part_tag(part):
    return part[5] if len(part) > 5 else ""


def in_total(part):
    return bool(part[2]) and (len(part) < 5 or part[4])


def combo_totals(k):
    """Totals per tier for every combination of the kit's choices, keyed 'build=parts|solar=fixed'."""
    import itertools
    chs = k.get("choices") or []
    out = {}
    for combo in itertools.product(*[[o[0] for o in c[2]] for c in chs]) if chs else [()]:
        sel = {c[0]: v for c, v in zip(chs, combo)}
        key = "|".join(f"{g}={v}" for g, v in sel.items())
        tots, names = [], []
        for t in TIER_NAMES:
            tot = 0
            for p in k["parts"]:
                tag = part_tag(p)
                if not in_total(p) or not PRODUCTS["cats"].get(p[2]):
                    continue
                if tag and sel.get(tag.split(":")[0]) != tag.split(":")[1]:
                    continue
                m = pick_for(p[2], t)
                tot += (m[0].get("price") or 0) if m else 0
            tots.append(round(tot, -1))
        for p in k["parts"]:
            tag = part_tag(p)
            if in_total(p) and PRODUCTS["cats"].get(p[2]) and (not tag or sel.get(tag.split(":")[0]) == tag.split(":")[1]) and p[0] not in names:
                names.append(p[0])
        out[key] = {"t": tots, "n": " + ".join(names)}
    return out


def table_rows(parts, show_totals=True):
    core, extra = "", ""
    for part in parts:
        name, size, key, note = part[:4]
        if key and not PRODUCTS["cats"].get(key):
            continue
        tag = part_tag(part)
        attrs = f' data-g="{tag.split(":")[0]}" data-v="{tag.split(":")[1]}"' if tag else ""
        row = f'<tr{attrs}><th scope="row" class="ph"><b>{name}</b><span class="kp-size">{size}</span><span class="pn">{note}</span></th>'
        if not key:
            row += '<td class="none" colspan="3"></td></tr>'
        else:
            for i, t in enumerate(TIER_NAMES):
                mains, others = pick_for(key, t), pick_for(key, t, "other")
                cell = product_line(mains[0]) if mains else '<span class="tn">No pick at this level.</span>'
                if others:
                    cell += f'<details class="more"><summary>Other good options ({len(others)})</summary>' + ''.join(product_line(o, False) for o in others) + '</details>'
                row += f'<td class="c{i}"><span class="mlabel">{t}</span>{cell}</td>'
            row += '</tr>'
        if show_totals and not in_total(part) and key:
            extra += row
        else:
            core += row
    return core, extra


def kit_table(k):
    """Rows are parts, columns are Budget / Mid-range / Premium. On phones a tab picks one column."""
    tabs = ''.join(f'<button type="button" data-t="{i}"{" aria-pressed=\"true\"" if i == 1 else ""}>{t}</button>' for i, t in enumerate(TIER_NAMES))
    head = '<tr><th class="ph">Part</th>' + ''.join(f'<th class="c{i}">{t}</th>' for i, t in enumerate(TIER_NAMES)) + '</tr>'
    core, extra = table_rows(k["parts"])
    if extra:
        extra = '<tr class="sub"><th colspan="4">Extras (not in the totals)</th></tr>' + extra
    totals = combo_totals(k)
    default = "|".join(f"{c[0]}={c[3]}" for c in (k.get("choices") or []))
    d = totals[default]
    tot = ''.join(f'<td class="c{i}"><span class="mlabel">{t} total</span><span class="tot">{money(d["t"][i])}</span></td>' for i, t in enumerate(TIER_NAMES))
    return (f'<div class="kit-table" data-tier="1" data-totals="{html.escape(json.dumps(totals))}"><div class="tier-tabs" role="group" aria-label="Price level">{tabs}</div>'
            f'<table><thead>{head}</thead><tbody>{core}<tr class="totrow"><th scope="row" class="ph"><b>Kit total</b><span class="pn">Parts only: <span class="tot-names">{d["n"]}</span></span></th>{tot}</tr>{extra}</tbody></table></div>')


def gear_table(k):
    if not k.get("gear") or not any(PRODUCTS["cats"].get(g[2]) for g in k["gear"]):
        return ""
    tabs = ''.join(f'<button type="button" data-t="{i}"{" aria-pressed=\"true\"" if i == 1 else ""}>{t}</button>' for i, t in enumerate(TIER_NAMES))
    head = '<tr><th class="ph">Gear</th>' + ''.join(f'<th class="c{i}">{t}</th>' for i, t in enumerate(TIER_NAMES)) + '</tr>'
    core, _ = table_rows([g + (True, "") for g in k["gear"]], show_totals=False)
    return ('<h2>Complete your setup</h2><p class="small">Gear that suits this kit. Not counted in the totals above.</p>'
            f'<div class="kit-table" data-tier="1"><div class="tier-tabs" role="group" aria-label="Price level">{tabs}</div><table><thead>{head}</thead><tbody>{core}</tbody></table></div>')

def kit_totals(k):
    cats = [p[2] for p in k["parts"] if p[2] and (len(p) < 5 or p[4])]
    row = ""
    for t in TIER_NAMES:
        total = 0
        for c in cats:
            m = pick_for(c, t)
            total += (m[0].get("kit_price") or m[0].get("price") or 0) if m else 0
        row += f'<div><b>{t}</b><span>{money(round(total, -1))}</span></div>'
    return row


KITS = [
    {"slug": "weekender", "name": "Weekender", "doodle": "tent", "preset": "weekender",
     "who": "Two or three nights away, a medium fridge, lights and phones. You drive there, set up camp and stay put until it's time to head home.",
     "runs": ["Medium 35 to 50L fridge", "4 LED lights, about 4 hours a night", "2 phones charging", "A 12V fan overnight", "Water pump"],
     "daily": "about 50Ah a day",
     "parts": [("Battery", "100 to 120Ah lithium", "battery_100", "Holds about two days of your use with no charging. About 10 to 13kg.", True, "build:parts"),
               ("DC-DC charger", "25A, with solar input", "dcdc_25", "Fills the battery on the drive there, and again on the way home. A couple of hours behind the wheel puts back more than a day's use.", True, "build:parts"),
               ("Battery box", "For a 100Ah battery", "box_100", "Holds the battery firmly and gives you plugs to run things from.", True, "build:parts"),
               ("All-in-one power box", "Battery, charger and plugs in one", "powerbox_100", "The easy option. Battery, DC-DC charger and solar input in one box you can move between cars.", True, "build:box"),
               ("Wiring kit", "Engine battery to the back", "install_kit", "The heavy cable, fuses and plugs that let your engine charge the house battery. Your auto electrician fits it. The premium REDARC kit is made for their 40A and 50A chargers, so with a 25A the mid-range kit does the same job.", True, ""),
               ("Fuse block", "One fuse per circuit", "fuse_block", "Fuses stop a fault turning into a fire. Your auto electrician also fits a main fuse right at the battery.", True, "build:parts"),
               ("Isolator switch", "One off switch", "isolator", "Turns all the house power off when you park up or need to work on it.", True, "build:parts"),
               ("Solar", "160 to 240W portable blanket", "blanket_200", "Optional if you drive most days, handy when you stay put. Park in the shade and lay it in the sun.", True, "solar:blanket"),
               ("Solar", "200W fixed roof panel", "roof_200", "Set and forget: it charges whenever the van sits in the sun, and while you drive.", True, "solar:fixed"),
               ("Inverter", "Not needed", None, "Everything here runs on 12V or USB.")],
     "choices": [("build", "How do you want it built?", [("parts", "Separate parts"), ("box", "All-in-one box")], "parts"),
                 ("solar", "What kind of solar?", [("blanket", "Portable blanket"), ("fixed", "Fixed roof panel")], "blanket")],
     "gear": [("Fridge", "35 to 50L", "fridge_medium", "The kit is sized for a medium fridge like these."),
              ("Lights", "12V LED", "lights", "LEDs barely use anything."),
              ("Fan", "12V", "fans", "Cheap to run, even all night.")],
     "easy": "This size is perfect for an <b>all-in-one power box</b>: battery, DC-DC charger and solar input in one box you can move between cars. The box itself just straps in. The heavy lead that charges it from your engine battery should be run and fused by an auto electrician.",
     "fourwd": "Works well in a 4WD too. Use the solar blanket rather than roof panels, and if the battery goes under the bonnet, pick one rated for the heat. See <a href=\"{pre}guides/4wd-dual-battery-basics.html\">4WD dual battery basics</a>.",
     "install": "With a power box, the main job is the charging lead, so expect the lower end of that range.",
     "south": "Southern winters barely change this kit, because driving does most of the charging. If you often stay put in Victoria or Tasmania in winter, go for the 200W blanket."},
    {"slug": "long-trips", "name": "Long trips", "doodle": "van", "preset": "long",
     "who": "A week or more away, a bigger fridge and a laptop. Some days driving, some days parked up.",
     "runs": ["Large 55 to 75L fridge", "4 LED lights", "2 phones charging", "A laptop on a 12V or USB-C charger, about 3 hours a day", "A 12V fan overnight", "Water pump"],
     "daily": "about 65 to 75Ah a day",
     "parts": [("Battery", "200Ah lithium", "battery_200", "Two days of buffer for grey days. About 20 to 25kg.", True, ""),
               ("DC-DC charger", "40A, with solar input", "dcdc_40", "Refills fast on driving days, and doubles as your solar regulator.", True, ""),
               ("Battery box or mount", "For a 200Ah battery", "box_200", "Holds the battery firmly in place.", True, ""),
               ("Wiring kit", "Engine battery to the back", "install_kit", "The heavy cable, fuses and plugs between your engine battery and the house battery. Your auto electrician fits it.", True, ""),
               ("Fuse block", "One fuse per circuit", "fuse_block", "Fuses on every circuit, plus a main fuse at the battery that your auto electrician fits.", True, ""),
               ("Isolator switch", "One off switch", "isolator", "One switch to turn all the house power off.", True, ""),
               ("Solar", "200 to 300W fixed roof panels", "roof_200", "About 150W keeps up in Queensland and a Victorian winter needs 250 to 300W, so we've picked a 200W panel. Add a 100W panel if you head south.", True, "solar:fixed"),
               ("Solar", "160 to 240W portable blanket", "blanket_200", "Rather not drill the roof? Park in the shade and lay a blanket in the sun. It packs away when you leave.", True, "solar:blanket"),
               ("Battery monitor", "Shunt type", "monitor", "Your fuel gauge, so you know exactly how many days you've got left.", True, ""),
               ("Inverter", "300 to 800W", "inverter_600", "Only if you'd rather use a normal laptop charger or charge camera batteries.", False, "")],
     "choices": [("solar", "What kind of solar?", [("fixed", "Fixed roof panels"), ("blanket", "Portable blanket")], "fixed")],
     "gear": [("Fridge", "55 to 75L", "fridge_large", "The kit is sized for a large fridge like these."),
              ("Lights", "12V LED", "lights", "LEDs barely use anything."),
              ("Fan", "12V", "fans", "Cheap to run, even all night.")],
     "easy": "Separate parts suit this kit best, fitted by an auto electrician. Fixed roof panels are set-and-forget, and the 200Ah battery gives room to add a small inverter later.",
     "fourwd": "In a 4WD, roof space usually fits one 200W panel at most. Pair it with a folding blanket for parked days, and a canopy is a good home for the battery. See <a href=\"{pre}guides/4wd-dual-battery-basics.html\">4WD dual battery basics</a>.",
     "install": "A battery, DC-DC charger, roof panel and monitor is a typical mid-sized job.",
     "south": "In a Victorian or Tasmanian winter, plan on the bigger end of the solar range, or add a 200W blanket for long parked spells."},
    {"slug": "living-in-it", "name": "Living in it", "doodle": "cup", "preset": "living",
     "who": "Full-time or close to it. Fridge-freezer, working from the van, a diesel heater, Starlink and a morning coffee.",
     "runs": ["Big 80 to 100L fridge-freezer", "6 LED lights", "2 phones, a laptop about 5 hours a day", "Starlink Mini about 6 hours a day", "Diesel heater electrics", "12V fan and water pump", "A 1,300W coffee machine, once a day"],
     "daily": "about 120Ah a day",
     "parts": [("Battery", "400 to 460Ah lithium", "battery_400", "About three days of buffer, 40 to 50kg. One big battery or two linked together. A serious system, priced like one.", True, ""),
               ("DC-DC charger", "50A, with solar input", "dcdc_50", "Big battery, big charger, so driving days count.", True, ""),
               ("Battery mount", "Heavy-duty", "box_200", "At this weight the battery must be bolted down properly. Your auto electrician will advise.", True, ""),
               ("Wiring kit", "Engine battery to the back", "install_kit", "Heavy cable, fuses and plugs. At this size your auto electrician will size the cable for the job.", True, ""),
               ("Fuse block", "Big fuses and small", "fuse_block", "Essential with a big battery and inverter. The premium SafetyHub takes the big inverter fuse too.", True, ""),
               ("Isolator switch", "300A, to suit an inverter", "isolator", "With a 2000W inverter you need a 300A switch, so skip the budget 100A one and pick mid-range or premium.", True, ""),
               ("Solar", "About 600W fixed roof panels", "roof_600", "Keeps up most of the year up north. Fills most van roofs.", True, ""),
               ("Inverter", "2,000W pure sine", "inverter_2000", "Handles the coffee machine's start-up surge. Needs thick cables and a proper fit.", True, ""),
               ("Battery monitor", "Shunt type", "monitor", "Essential at this size.", True, ""),
               ("Add: a portable blanket", "160 to 240W blanket", "blanket_200", "Tops up the roof panels on grey days, or when you park in the shade.", False, "")],
     "choices": [],
     "gear": [("Fridge-freezer", "80 to 100L", "fridge_ff", "The kit is sized for a big fridge-freezer like these."),
              ("Lights", "12V LED", "lights", "LEDs barely use anything."),
              ("Fan", "12V", "fans", "A roof fan makes full-time living far more comfortable.")],
     "easy": "This is a full install job: separate parts, fitted and fused by an auto electrician. Ask them about a lithium-ready battery charger too, for when you plug in at a campsite.",
     "fourwd": "Full-time power in a 4WD is a squeeze. The battery alone weighs 40 to 50kg, which eats into your payload, and 600W of panels won't fit on the roof. Check your vehicle's GVM, and plan on blankets and regular driving.",
     "install": "With a 2,000W inverter, 600W of solar and a big battery bank, expect the top end of that range, or more.",
     "south": "<b>Southern winters are the catch.</b> In a Victorian winter this setup would want about 1,150W of solar, which won't fit on a van roof. Plan on a 200 to 400W portable blanket, plugging in at a powered site every few days, or a small inverter generator for grey spells."},
]


KIT_JS = """<script>
(function(){
  var box=document.querySelector('.kit-table'); if(!box) return;
  box.querySelectorAll('.tier-tabs button').forEach(function(b){
    b.addEventListener('click',function(){
      box.setAttribute('data-tier',b.dataset.t);
      box.querySelectorAll('.tier-tabs button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
    });
  });
  var key='ogs-cart:'+location.pathname, saved={};
  try{ saved=JSON.parse(localStorage.getItem(key)||'{}'); }catch(e){}
  document.querySelectorAll('.got input').forEach(function(c){
    if(saved[c.dataset.key]) c.checked=true;
    c.addEventListener('change',function(){
      document.querySelectorAll('.got input[data-key="'+c.dataset.key.replace(/"/g,'\\"')+'"]').forEach(function(o){o.checked=c.checked;});
      saved[c.dataset.key]=c.checked;
      try{ localStorage.setItem(key,JSON.stringify(saved)); }catch(e){}
    });
  });
})();
</script>"""


VEH = [("van", "Campervan"), ("caravan", "Caravan or camper trailer"), ("4wd", "4WD")]
CARAVAN_TIP = ("<b>Caravans and camper trailers:</b> fit the DC-DC charger in the van, close to the battery, fed by a heavy cable from the car through an Anderson plug. "
               "You'll get about a third less charge from driving than in a campervan because of the long cable, so lean on solar, and you'll usually have more roof space for it. "
               "A 240V battery charger for powered sites is worth adding (fitted by a licensed electrician). See <a href=\"{pre}guides/caravan-power-setup.html\">Caravan power</a>.")
VAN_TIP = "<b>Campervans:</b> these kits are sized for you. The battery usually lives inside, so it stays cool, and the wiring run from the engine is short."


def chips(group, label, opts, default):
    btns = ''.join(f'<button type="button" data-g="{group}" data-v="{v}" aria-pressed="{"true" if v == default else "false"}">{t}</button>' for v, t in opts)
    return f'<div class="kc"><span class="flabel">{label}</span><div class="seg" role="group" aria-label="{label}">{btns}</div></div>'


def build_kits():
    os.makedirs(os.path.join(ROOT, "kits"), exist_ok=True)

    def from_price(k):
        t = combo_totals(k)["|".join(f"{c[0]}={c[3]}" for c in (k.get("choices") or []))]["t"][0]
        return money(t)
    cards = ''.join(f'<a class="card kit-card" href="{{pre}}kits/{k["slug"]}.html">[[d:{k["doodle"]}:110]]<h3>{k["name"]}</h3><p class="kit-facts"><b>{k["parts"][0][1]}</b> · parts from {from_price(k)}</p><p>{k["who"]}</p><span class="go">See the full kit →</span></a>' for k in KITS)
    hub = ('<main class="page"><div class="crumbs"><a href="{pre}index.html">Home</a> › Kits</div>'
           '<div class="sec-head"><h1 style="font-size:3rem;margin:4px 0 8px">Ready-made kits</h1>[[d:fridge:100]]</div>'
           '<p class="hint" style="margin-bottom:18px">Three common setups, sized with the Power Planner. Tell us what you\'re powering, then pick the kit that sounds most like you.</p>'
           '<div class="kit-choices hub-choices">' + chips("veh", "What are you powering?", VEH, "van") + '</div>'
           f'<div class="cards">{cards}</div>'
           '<div class="aside" style="margin-top:30px">Not quite you? The <a href="{pre}planner.html" style="color:var(--sign)">Power Planner</a> sizes a kit around exactly what you run and where you travel.</div>'
           '<script src="{pre}assets/kits.js" defer></script></main>')
    page("kits/index.html", "Ready-made kits", "Three ready-made power kits for Australian vans, caravans and 4WDs: Weekender, Long trips and Living in it.", hub, "kits/index.html")
    for k in KITS:
        choice_ui = chips("veh", "What are you powering?", VEH, "van") + ''.join(chips(c[0], c[1], c[2], c[3]) for c in (k.get("choices") or []))
        tips = (f'<div class="veh-tip" data-for="van">{VAN_TIP}</div>'
                f'<div class="veh-tip" data-for="caravan" hidden>{CARAVAN_TIP}</div>'
                f'<div class="veh-tip" data-for="4wd" hidden><b>4WDs:</b> {k["fourwd"]}</div>')
        body = (f'<main class="article kitpage" data-preset="{k["preset"]}"><div class="crumbs"><a href="{{pre}}index.html">Home</a> › <a href="{{pre}}kits/index.html">Kits</a> › {k["name"]}</div>'
                f'[[d:{k["doodle"]}:150]]'.replace('<svg class="doodle"', '<svg class="doodle guide-doodle"') +
                f'<h1>The {k["name"]} kit</h1><div class="meta"><span>Uses {k["daily"]}</span><a href="{{pre}}disclosure.html">How we make money</a></div>'
                f'<p class="hint" style="font-size:1.15rem">{k["who"]}</p>'
                '<div class="tldr"><h2>What it runs</h2><ul>' + ''.join(f'<li>{r}</li>' for r in k["runs"]) + '</ul></div>'
                f'<h2>Make it yours</h2><div class="kit-choices">{choice_ui}</div>{tips}'
                f'<h2>What\'s in the kit</h2><p class="trust-strip"><span>✓ Picked for fit, not commission</span><span>✓ Aussie shops, AUD prices</span><span>✓ Estimates, not promises</span><span>✓ Auto electrician to wire it in</span><a href="../about.html#how-we-work">How we work</a></p><p class="small">Tap <b>+ Add to my list</b> on anything you want. Your list builds at the bottom of the page with a link to each shop. Links open in a new tab.</p>{kit_table(k)}'
                f'<div class="kit-total"><h2>What it costs all up</h2>'
                f'<p class="small">The kit total above is parts only, using our main pick at each level. Prices checked {PRODUCTS["checked_label"]}; they change often.</p><p class="small"><b>Installation:</b> auto electricians quote roughly $300 to $2,500 for a dual battery fit-out depending on the job (The Quote Yard 2026 price guide). {k["install"]} Get a written quote.</p></div>'
                + gear_table(k) +
                '<section class="my-list" id="my-list" aria-live="polite"></section>'
                f'<h2>Easiest way to build it</h2><p>{k["easy"]}</p>'
                f'<h2>Travelling south in winter?</h2><p>{k["south"]}</p>'
                f'<div class="cta-box"><p>Change anything you like: your fridge, your state, how much you drive. The Power Planner starts from this kit.</p><a class="btn-link" id="customise" href="{{pre}}planner.html#{k["preset"]}">Customise this kit</a></div>'
                '<div class="aside" style="margin:24px 0"><b>Get a pro to wire it in.</b> Have a licensed auto electrician install or check your setup, with the right cable sizes and fuses. Sizes here are estimates for typical use.</div>'
                '<p class="small">We pick products by how well they fit the job, not by what pays us. Some links earn us a small commission at no cost to you. <a href="{pre}disclosure.html">How we make money</a>.</p>'
                '<script src="{pre}assets/list.js" defer></script><script src="{pre}assets/kits.js" defer></script></main>')
        page(f"kits/{k['slug']}.html", f"The {k['name']} kit", f"Everything in the {k['name']} power kit for Australian vans, caravans and 4WDs: battery, solar, DC-DC charger, wiring and more, with budget to premium options.", body, "kits/index.html")


# ---------- Guides hub: start here, picture tiles, quick answers, then topics ----------
START_HERE = ["van-power-basics", "lithium-vs-agm", "how-much-solar-australia"]
TOPICS = [  # (anchor, heading, doodle, tags, one-liner)
    ("batteries", "Batteries", "battery", ["Batteries"], "Which battery, what size, where it can go."),
    ("solar", "Solar", "panel", ["Solar"], "How much solar, which type, and winter."),
    ("charging", "Charging while you drive", "plug", ["Charging"], "DC-DC chargers and smart alternators."),
    ("fridges", "Fridges", "fridge", ["Fridges"], "How long it runs and why it flattens things."),
    ("rigs", "Caravans & 4WDs", "caravan", ["Caravans", "4WDs"], "Trailer plugs, dual batteries, fixes."),
    ("trips", "Trips & planning", "road", ["Start here", "Trips"], "When to go and what to pack power-wise."),
]
QUICK = [  # short keyword-style questions that jump straight to the answer
    ("100Ah fridge runtime", "will-my-fridge-last"), ("Fridge flattening battery", "fridge-flattening-battery"),
    ("Smart alternator?", "smart-alternator-check"), ("Lithium under the bonnet", "lithium-under-the-bonnet"),
    ("Solar blanket vs fixed", "solar-blanket-vs-fixed-panel"), ("Winter solar", "winter-solar-not-keeping-up"),
    ("Caravan not charging", "caravan-not-charging-while-driving"), ("Power station vs dual battery", "portable-power-stations"),
]


def guides_hub():
    by = {g[0]: g for g in GUIDES}
    def row(g, num=None):
        slug, title, tag, blurb, status = g
        lead = f'<span class="n">{num}</span>' if num else doodle(TAG_DOODLE.get(tag, "sun"), 44)
        words = html.escape((title + " " + blurb + " " + tag).lower())
        if status != "live":
            return f'<li class="soon" data-words="{words}"><div>{lead}<span><b>{html.escape(title)}</b><span class="small">Coming soon</span></span></div></li>'
        return (f'<li data-words="{words}"><a href="{{pre}}guides/{slug}.html">{lead}<span><b>{html.escape(title)}</b>'
                f'<span class="small">{html.escape(blurb)}</span></span><span class="go-arrow" aria-hidden="true">→</span></a></li>')
    h = '<main class="page guides-hub"><div class="crumbs"><a href="{pre}index.html">Home</a> › Guides</div>'
    h += ('<div class="sec-head"><h1 style="font-size:3rem;margin:4px 0 8px">Guides</h1>[[d:road:120]]</div>'
          '<p class="hint">Plain-English answers about van, caravan and 4WD power. Read the first three if you\'re new, '
          'tap a picture to browse a topic, or search for your question.</p>')
    # 1. Start here
    h += ('<section class="band start-here" aria-labelledby="sh"><h2 id="sh">Start here</h2>'
          '<p class="hand-pick">new to all this? read these three in order</p><ol class="hub-list">'
          + "".join(row(by[s], f"{i}") for i, s in enumerate(START_HERE, 1) if s in by) + '</ol></section>')
    # 2. Picture tiles
    tiles = ""
    for a, name, d, tags, line in TOPICS:
        n = sum(1 for g in GUIDES if g[2] in tags and g[0] not in START_HERE)
        if n:
            tiles += f'<a class="tile" href="#{a}">{doodle(d, 70)}<b>{name}</b><span class="small">{n} guide{"s" if n != 1 else ""}</span></a>'
    h += f'<section class="band alt" aria-labelledby="bt"><h2 id="bt">Browse by topic</h2><div class="tiles">{tiles}</div></section>'
    # 3. Quick answers + search
    chips = "".join(f'<a class="chip" href="{{pre}}guides/{s}.html">{html.escape(t)}</a>' for t, s in QUICK if s in by and by[s][4] == "live")
    h += ('<section class="band find" aria-labelledby="qa"><h2 id="qa">Know what you\'re after?</h2>'
          '<label class="hub-search"><span class="visually-hidden">Search the guides</span>'
          '<input type="search" id="guide-search" placeholder="Try fridge, solar, alternator, caravan..." autocomplete="off"></label>'
          f'<p class="small" style="margin:14px 0 8px">Quick answers people look for most:</p><div class="chips">{chips}</div></section>')
    # 4. Topics
    for a, name, d, tags, line in TOPICS:
        gs = [g for g in GUIDES if g[2] in tags and g[0] not in START_HERE]
        if gs:
            h += (f'<section class="topic" id="{a}"><div class="topic-head">{doodle(d, 56)}<div><h2>{name}</h2>'
                  f'<p class="small">{line}</p></div></div><ul class="hub-list">' + "".join(row(g) for g in gs) + '</ul></section>')
    h += '<p class="small no-match" hidden>No guides match that yet. Try a simpler word, like <b>fridge</b> or <b>solar</b>.</p>'
    h += ('<script>(function(){var i=document.getElementById("guide-search");if(!i)return;var nm=document.querySelector(".no-match");'
          'i.addEventListener("input",function(){var q=i.value.trim().toLowerCase(),any=false;'
          'document.querySelectorAll(".topic,.start-here").forEach(function(sec){var shown=0;'
          'sec.querySelectorAll("li").forEach(function(li){var ok=!q||q.split(/\\s+/).every(function(w){return li.dataset.words.indexOf(w)>-1});li.hidden=!ok;if(ok)shown++});'
          'sec.hidden=!shown;if(shown)any=true});nm.hidden=any||!q;});})();</script>')
    return h + '</main>'


def build():
    # Home
    LD["index.html"] = [ORG, {"@type": "WebSite", "@id": BASE + "#site", "name": "Off-Grid Sorted", "url": BASE, "inLanguage": "en-AU", "publisher": {"@id": ORG_ID}}] + PEOPLE
    page("index.html", SITE, "Free plain-English power planner and guides for Australian vans, caravans and 4WDs. Work out the battery, solar and charger you need.", read("content/home.html"))
    # Guides hub
    hub = guides_hub()
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
        cta_href = {"Caravans": "planner.html#caravan", "4WDs": "planner.html#4wd"}.get(tag, "planner.html")
        body = body.replace('</ul></div>', f'</ul></div><p class="early-cta"><a href="{{pre}}{cta_href}">Want your own numbers? Open the Power Planner →</a> <span>or see the <a href="{{pre}}kits/index.html">ready-made kits</a></span></p>', 1)
        body = body.replace('<span>By Kiran and Mitch</span>', '<span>By <a href="{pre}about.html">Kiran and Mitch</a></span>', 1)
        faqs = FAQS.get(slug, [])
        if faqs:
            fq = '<section class="faq"><h2>Quick answers</h2>' + "".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faqs) + '</section>'
            body = body.replace("<h2>Sources</h2>", fq + "<h2>Sources</h2>", 1) if "<h2>Sources</h2>" in body else body.replace('<div class="aside" style="margin:24px 0"><b>Get a pro', fq + '<div class="aside" style="margin:24px 0"><b>Get a pro', 1)
        gurl = f"{BASE}guides/{slug}.html"
        LD[f"guides/{slug}.html"] = [
            {"@type": "Article", "@id": gurl + "#article", "headline": title, "description": blurb, "url": gurl,
             "inLanguage": "en-AU", "author": PEOPLE, "publisher": {"@id": ORG_ID}, "image": BASE + "assets/og.png",
             "dateModified": git_date(f"content/guides/{slug}.html"), "about": tag},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                {"@type": "ListItem", "position": 2, "name": "Guides", "item": BASE + "guides/index.html"},
                {"@type": "ListItem", "position": 3, "name": title.split(":")[0], "item": gurl}]},
            ORG] + ([{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}] if faqs else [])
        wrapped = f'<main class="article"><div class="crumbs"><a href="{{pre}}index.html">Home</a> › <a href="{{pre}}guides/index.html">Guides</a> › {tag}</div>{dd}{body}{rel}</main>'
        page(f"guides/{slug}.html", title.split(":")[0], blurb, wrapped, "guides/index.html")
    LD["about.html"] = [{"@type": "AboutPage", "url": BASE + "about.html", "name": "About Off-Grid Sorted", "about": {"@id": ORG_ID}, "mainEntity": PEOPLE}, ORG]
    # Info pages
    for name, title, desc in [("about", "About", "Who is behind Off-Grid Sorted, and why it exists."),
                              ("disclosure", "Affiliate disclosure & disclaimer", "How Off-Grid Sorted earns money, and the limits of our advice."),
                              ("privacy", "Privacy", "How Off-Grid Sorted handles your information."),
                              ("contact", "Contact", "How to get in touch with Off-Grid Sorted."),
                              ("embed", "Put the Power Planner on your site", "Add the free Off-Grid Sorted Power Planner to your own website, van build or auto electrical site. Copy and paste, no sign-up.")]:
        page(f"{name}.html", title, desc, '<main class="article"><div class="crumbs"><a href="{pre}index.html">Home</a> › ' + title + '</div>' + read(f"content/{name}.html") + '</main>', f"{name}.html" if name == "about" else "")
    build_kits()
    # Refresh planner chrome
    p = read("planner.html")
    p = re.sub(r'(<a class="skip"[^\n]*\n)?<header class="site-header">.*?</header>\n', lambda m: header("", "planner.html"), p, flags=re.S)
    pj = json.dumps(PRODUCTS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    p = re.sub(r'<script type="application/json" id="ogs-products">.*?</script>', lambda m: f'<script type="application/json" id="ogs-products">{pj}</script>', p, flags=re.S)
    p = re.sub(r'<footer class="site-footer">.*?</footer>\n(<script data-menu>.*?</script>\n)?', lambda m: footer("") + MENU_JS, p, flags=re.S)
    LD["planner.html"] = [{"@type": "WebApplication", "name": "Power Planner", "url": BASE + "planner.html",
        "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any web browser", "inLanguage": "en-AU",
        "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AUD"},
        "description": "Free calculator for Australian campervans, caravans and 4WDs. Tell it what you run and where you travel, and it works out the battery, solar, DC-DC charger and inverter you need, using Bureau of Meteorology sun averages.",
        "publisher": {"@id": ORG_ID}, "creator": PEOPLE}, ORG]
    seo = seo_tags("planner.html", "Power Planner · Off-Grid Sorted", "Free calculator for Australian vans, caravans and 4WDs: work out the battery, solar, DC-DC charger and inverter you need, with real products at three price levels.")
    if "<!--seo-->" in p:
        p = re.sub(r"<!--seo-->.*?<!--/seo-->", lambda m: seo, p, flags=re.S)
    else:
        p = p.replace('<link rel="icon"', seo + '\n<link rel="icon"', 1)
    with open(os.path.join(ROOT, "planner.html"), "w") as f:
        f.write(p)
    BUILT.append("planner.html")
    # 404 page (Netlify serves /404.html automatically)
    page_abs("404.html", "Page not found", "That page doesn't exist.",
             '<main class="article notfound"><svg class="flat" viewBox="0 0 130 90" width="120" height="83" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><rect x="10" y="18" width="100" height="58" rx="10"/><path d="M110 37h9v20h-9"/><path d="M28 62V34" stroke-width="5"/><path d="M78 44v4M96 44v4M76 62c5-5 17-5 22 0"/></svg><h1>Flat battery</h1>'
             '<p class="hint">We couldn\'t find that page. It may have moved, or the link has a typo.</p>'
             '<p><a class="btn-link solid" href="/planner.html">Open the Power Planner</a></p>'
             '<p><a href="/index.html">Home</a> · <a href="/guides/index.html">Guides</a> · <a href="/kits/index.html">Kits</a></p></main>')
    BUILT.remove("404.html")
    # llms.txt: a plain map of the site for AI tools
    lines = ["# Off-Grid Sorted", "", "> " + ORG["description"] + " Run by Kiran and Mitch on the southern Gold Coast. Prices in AUD; sun figures from Bureau of Meteorology averages. All numbers are planning estimates; have a licensed auto electrician install or check any system.", "",
             "## Tools", f"- [Power Planner]({BASE}planner.html): free calculator for battery, solar, DC-DC charger and inverter size, by state and season", "",
             "## Ready-made kits"] + [f"- [{k['name']}]({BASE}kits/{k['slug']}.html)" for k in KITS] + ["", "## Guides"] + \
            [f"- [{g[1]}]({BASE}guides/{g[0]}.html): {g[3]}" for g in GUIDES if g[4] == "live"] + ["", "## About", f"- [About us]({BASE}about.html)", f"- [Affiliate disclosure]({BASE}disclosure.html)", ""]
    with open(os.path.join(ROOT, "llms.txt"), "w") as f:
        f.write("\n".join(lines))
    # robots + sitemap
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    urls = "".join(f"  <url><loc>{BASE}{'' if p_ == 'index.html' else p_}</loc></url>\n" for p_ in sorted(set(BUILT)))
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')


if __name__ == "__main__":
    build()
    print("built")
