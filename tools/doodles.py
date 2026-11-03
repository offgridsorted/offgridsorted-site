"""Hand-drawn style line doodles for Off-Grid Sorted.

Same look as the van sketch: dark ink lines, round ends, the odd splash of sunshine yellow.
Each doodle is an inline SVG using currentColor, so it follows the text colour.
Use doodle(name, width) to get the markup.
"""

Y = "#f5cb3c"   # sunshine
M = "#e0a12e"   # marigold

_D = {
    # name: (viewBox, inner)
    "sun": ("0 0 100 100", f'<circle cx="50" cy="50" r="18" fill="{Y}"/><path d="M50 14v-9M50 95v-9M14 50H5M95 50h-9M24 24l-6-6M82 82l-6-6M24 76l-6 6M82 18l-6 6"/>'),
    "panel": ("0 0 130 80", '<path d="M22 22h96l-12 36H10z"/><path d="M54 22l-10 36M86 22l-10 36M16 40h96"/><path d="M60 58v14M46 72h28"/>'),
    "battery": ("0 0 130 90", f'<rect x="10" y="18" width="100" height="58" rx="10" fill="{Y}"/><path d="M110 37h9v20h-9"/><path d="M28 62V34M42 62V34" stroke-width="5"/><path d="M78 42v5M96 42v5M76 56c5 6 17 6 22 0"/>'),
    "fridge": ("0 0 120 100", '<rect x="16" y="30" width="88" height="58" rx="8"/><path d="M16 46h88M46 22h28v8H46"/><path d="M60 56v22M50 61l20 12M70 61L50 73" stroke-width="3"/>'),
    "kettle": ("0 0 110 100", '<path d="M30 40h46l8 44H22z"/><path d="M76 50c14 0 18 8 18 18M30 50L14 38"/><path d="M38 40c0-12 30-12 30 0"/><path d="M50 16c-4 6 4 8 0 14M62 12c-4 6 4 8 0 14" stroke-dasharray="3 5"/>'),
    "van": ("0 0 160 90", f'<path d="M14 66V30c0-6 4-10 10-10h82c10 0 17 4 22 11l16 21c3 4 4 7 4 12v2z"/><path d="M108 22l0 26h32"/><path d="M48 14l5-8h40l-5 8z" fill="{Y}"/><circle cx="44" cy="68" r="11" fill="var(--paper, #f3f0e8)"/><circle cx="118" cy="68" r="11" fill="var(--paper, #f3f0e8)"/><circle cx="44" cy="68" r="3"/><circle cx="118" cy="68" r="3"/>'),
    "caravan": ("0 0 170 90", '<path d="M20 64V30c0-10 8-16 18-16h82c12 0 22 10 22 22v28z"/><rect x="36" y="28" width="30" height="16" rx="3"/><path d="M84 30h16v34H84"/><path d="M142 58h20M6 64h14"/><circle cx="64" cy="68" r="10" fill="var(--paper, #f3f0e8)"/><circle cx="64" cy="68" r="3"/>'),
    "4wd": ("0 0 160 90", f'<path d="M14 62V40l10-18h70l14 18h30c6 0 10 4 10 10v12z"/><path d="M28 22V14h60v8M40 14V8M76 14V8"/><path d="M60 22v18M24 40h84"/><circle cx="42" cy="64" r="13" fill="var(--paper, #f3f0e8)"/><circle cx="120" cy="64" r="13" fill="var(--paper, #f3f0e8)"/><circle cx="42" cy="64" r="4" fill="{Y}"/><circle cx="120" cy="64" r="4" fill="{Y}"/>'),
    "tent": ("0 0 140 90", '<path d="M10 78h120M22 78L64 14l42 64"/><path d="M64 14l0 64M52 78l12-26 12 26"/><path d="M106 78l18-30 6 30"/>'),
    "road": ("0 0 160 90", f'<path d="M6 54l30-34 22 22 26-30 34 42"/><circle cx="130" cy="20" r="9" fill="{Y}"/><path d="M60 88l14-34M100 88L86 54M80 86v-6M80 72v-6M80 60v-4"/>'),
    "plug": ("0 0 140 90", f'<rect x="12" y="24" width="38" height="40" rx="8" fill="{Y}"/><path d="M22 24V10M40 24V10M31 64v6c0 16 30 18 48 6s40-12 52 2"/>'),
    "bulb": ("0 0 100 100", f'<path d="M50 14c-18 0-28 14-28 28 0 12 8 18 12 26h32c4-8 12-14 12-26 0-14-10-28-28-28z" fill="{Y}"/><path d="M36 76h28M38 86h24M46 46l4 10 4-10"/><path d="M14 20l-6-4M86 20l6-4M50 4v-2" stroke-dasharray="3 4"/>'),
    "pin": ("0 0 90 100", f'<path d="M45 90S16 58 16 38a29 29 0 0 1 58 0c0 20-29 52-29 52z"/><circle cx="45" cy="38" r="10" fill="{Y}"/>'),
    "gauge": ("0 0 120 90", f'<path d="M14 74a46 46 0 0 1 92 0"/><path d="M26 74h10M84 74h10M60 30v8M34 42l6 6M86 42l-6 6"/><path d="M60 74l22-26" stroke-width="5"/><circle cx="60" cy="74" r="6" fill="{Y}"/><path d="M22 86h14M84 86h14" stroke-dasharray="2 4"/>'),
    "spanner": ("0 0 110 100", '<path d="M70 14a20 20 0 0 0-16 30L18 80a8 8 0 0 0 12 12l36-36a20 20 0 0 0 30-16l-12 4-10-10 4-12a20 20 0 0 0-8-2z"/>'),
    "cup": ("0 0 110 100", f'<path d="M20 40h56l-6 46H26z" fill="{Y}"/><path d="M76 50c14 0 16 18 0 20M14 92h68"/><path d="M38 30c-4-6 4-8 0-14M56 30c-4-6 4-8 0-14" stroke-dasharray="3 5"/>'),
    "fire": ("0 0 110 100", f'<path d="M55 16c10 16 24 22 24 42a24 24 0 0 1-48 0c0-12 8-18 10-26 4 8 8 10 14 12-2-10 0-20 0-28z" fill="{Y}"/><path d="M18 90l74-18M18 72l74 18"/>'),
    "tick": ("0 0 100 100", f'<path d="M18 52l20 20 44-46" stroke-width="7" stroke="{M}"/>'),
    "arrow": ("0 0 140 60", '<path d="M8 44c30-30 80-34 118-20"/><path d="M112 12l16 12-18 10"/>'),
}

# Which doodle goes with which guide tag
TAG_DOODLE = {"Start here": "bulb", "Batteries": "battery", "Solar": "panel", "Charging": "plug",
              "Caravans": "caravan", "4WDs": "4wd", "Fridges": "fridge"}


def doodle(name, width=80, cls="doodle", label=None):
    vb, inner = _D[name]
    _, _, w, h = map(float, vb.split())
    height = round(width * h / w)
    a11y = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return (f'<svg class="{cls}" viewBox="{vb}" width="{width}" height="{height}" {a11y} fill="none" '
            f'stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')


def horizon():
    """Footer scene: hills, a road, the sun and a little van driving along."""
    return ('<svg class="horizon" viewBox="0 -30 1200 150" preserveAspectRatio="xMidYMax slice" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M0 100c120-40 180-60 260-30s150 10 230-30 170-30 260 10 160 30 250-10 140-20 200 10"/>'
            f'<circle cx="980" cy="38" r="20" fill="{Y}"/><path d="M980 6v-6M1018 38h6M948 14l-4-4M1012 14l4-4" />'
            '<path d="M0 112h1200" stroke-dasharray="14 12"/>'
            '<g transform="translate(560 64) scale(.42)"><path d="M14 66V30c0-6 4-10 10-10h82c10 0 17 4 22 11l16 21c3 4 4 7 4 12v2z" fill="var(--sand, #ebe4d3)"/><path d="M108 22l0 26h32"/>'
            f'<path d="M48 14l5-8h40l-5 8z" fill="{Y}"/><circle cx="44" cy="68" r="11" fill="var(--sand, #ebe4d3)"/><circle cx="118" cy="68" r="11" fill="var(--sand, #ebe4d3)"/></g>'
            '<path d="M520 92h-30M512 84h-40" stroke-dasharray="4 8"/>'
            '</svg>')
