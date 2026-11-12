#!/usr/bin/env python3
"""Generate a hand-crafted pixel-art banner SVG for the GitHub profile README.

A retro night-coding room: neon handle sign, contribution-grid poster, window
with a crescent moon, dual monitors, steaming mug, and a little green snake
crawling along the floor. Dark theme with the profile's cyan/violet neon accents.

Output: assets/banner.svg
"""

import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "banner.svg"

W, H = 960, 300

# palette
WALL = "#131735"
WALL_STRIPE = "#171c40"
FLOOR = "#0c102c"
FLOOR_TILE = "#101638"
BASEBOARD = "#1b2150"
FRAME = "#262e5e"
SKY = "#0a0e26"
STAR = "#cfe3ff"
MOON = "#e8ecff"
PANEL = "#0a0e24"
SCREEN_BG = "#0f1430"
CODE_GRAY = "#3b4261"
CYAN = "#22d3ee"
VIOLET = "#a78bfa"
GREEN = "#4ade80"
YELLOW = "#e0af68"
DESK_WOOD = "#6e4a30"
DESK_EDGE = "#57391f"
DESK_TOP = "#7f5939"
LEG = "#3a2812"
GRID_EMPTY = "#1b2145"
L1, L2, L3, L4 = "#0e4429", "#006d32", "#26a641", "#39d353"
SNAKE_BODY = "#26a641"
SNAKE_HEAD = "#39d353"
TONGUE = "#fb7185"
POT = "#b4552e"
POT_RIM = "#cf6a3a"
LEAF1, LEAF2, LEAF3 = "#16a34a", "#22c55e", "#15803d"
MUG = "#e5484d"
MUG_RIM = "#f37070"
STEAM = "#c7d2fe"
FONT = "'JetBrains Mono','Fira Mono',Consolas,monospace"

E: list[str] = []


def rect(x, y, w, h, fill, opacity=None, rx=None):
    o = f' opacity="{opacity}"' if opacity is not None else ""
    r = f' rx="{rx}"' if rx is not None else ""
    E.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{o}{r}/>')


def anim_star(x, y, dur, begin):
    E.append(
        f'<rect x="{x}" y="{y}" width="2" height="2" fill="{STAR}">'
        f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        "</rect>"
    )


def anim_steam(x, y, dur, begin):
    E.append(
        f'<g opacity="0.8">'
        f'<rect x="{x}" y="{y}" width="4" height="4" fill="{STEAM}"/>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -20" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.8;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        "</g>"
    )


# ---------------------------------------------------------------- background
rect(0, 0, W, 270, WALL)
for x in range(24, W, 48):
    rect(x, 0, 2, 270, WALL_STRIPE)
rect(0, 266, W, 4, BASEBOARD)
rect(0, 270, W, 30, FLOOR)
for x in range(0, W, 40):
    rect(x, 270, 20, 30, FLOOR_TILE)
rect(0, 150, W, 150, "url(#fade)")

# -------------------------------------------------------------------- window
rect(756, 96, 152, 148, FRAME)
rect(762, 102, 140, 136, SKY)
rect(828, 102, 6, 136, FRAME)
rect(762, 164, 140, 6, FRAME)
rect(748, 244, 168, 10, FRAME)
rect(748, 254, 168, 3, BASEBOARD)
# stars
for sx, sy in ((784, 118), (846, 132), (880, 118), (802, 206), (884, 196), (812, 182)):
    rect(sx, sy, 2, 2, STAR)
anim_star(788, 148, 2.6, 0)
anim_star(856, 186, 3.4, 1.2)
anim_star(872, 206, 2.2, 0.6)
# blocky crescent moon + glow
rect(844, 112, 36, 36, MOON, opacity=0.06)
cx, cy, r = 860, 128, 7
for yy in range(cy - r, cy + r + 1, 2):
    half = int((r * r - (yy - cy) ** 2) ** 0.5)
    rect(cx - half, yy, half * 2, 2, MOON)
rect(862, 114, 16, 26, SKY)  # cut -> crescent

# ------------------------------------------------------------------- poster
rect(60, 100, 176, 104, FRAME)
rect(66, 106, 164, 92, GRID_EMPTY.replace("1b2145", "0d1130"))
levels = {
    (2, 0): L2, (5, 0): L1,
    (0, 1): L1, (3, 1): L3, (4, 1): L1,
    (1, 2): L2, (6, 2): L1,
    (2, 3): L1, (4, 3): L2, (5, 3): L4,
    (0, 4): L1, (3, 4): L2, (6, 4): L3,
}
gx, gy = 94, 114
for col in range(7):
    for row in range(5):
        rect(gx + col * 16, gy + row * 16, 12, 12, levels.get((col, row), GRID_EMPTY))

# --------------------------------------------------------------- neon sign
rect(320, 20, 320, 80, CYAN, opacity=0.04)
E.append(
    '<g shape-render="auto">'
    f'<rect x="326" y="28" width="308" height="56" rx="10" fill="none" stroke="{CYAN}" stroke-width="2">'
    '<animate attributeName="opacity" values="0.35;0.75;0.35" dur="3.5s" repeatCount="indefinite"/>'
    "</rect>"
    '<g text-anchor="middle" font-family="' + FONT + '" font-size="30" font-weight="700" letter-spacing="6" fill="none" stroke="' + CYAN + '">'
    '<text x="484" y="70" stroke-width="10" opacity="0.10">0xrafiKaji</text>'
    '<text x="484" y="70" stroke-width="4" opacity="0.22">'
    '<animate attributeName="opacity" values="0.12;0.3;0.12" dur="3.5s" repeatCount="indefinite"/>'
    "0xrafiKaji</text>"
    f'<text x="484" y="70" fill="{CYAN}" stroke="none">0xrafiKaji</text>'
    "</g></g>"
)

# -------------------------------------------------------------------- desk
rect(292, 258, 12, 38, LEG)
rect(676, 258, 12, 38, LEG)
rect(280, 248, 420, 10, DESK_WOOD)
rect(280, 255, 420, 3, DESK_EDGE)
rect(280, 248, 420, 2, DESK_TOP)

# ----------------------------------------------------------- main monitor
rect(408, 110, 248, 132, CYAN, opacity=0.05)
rect(420, 118, 224, 116, PANEL)
rect(428, 126, 208, 100, SCREEN_BG)
code = [
    (138, [(0, 34, CODE_GRAY), (40, 52, CYAN), (98, 40, VIOLET), (144, 28, CODE_GRAY)]),
    (152, [(10, 46, VIOLET), (62, 30, GREEN), (98, 62, CODE_GRAY)]),
    (166, [(0, 60, CYAN), (66, 24, CODE_GRAY), (96, 38, YELLOW)]),
    (180, [(10, 26, CODE_GRAY), (42, 44, GREEN), (92, 30, CYAN)]),
    (194, [(0, 36, VIOLET), (42, 52, CODE_GRAY)]),
]
for yy, segs in code:
    for dx, ww, col in segs:
        rect(438 + dx, yy, ww, 6, col)
E.append(
    f'<rect x="538" y="192" width="8" height="12" fill="{CYAN}">'
    '<animate attributeName="opacity" values="1;0" dur="1.1s" calcMode="discrete" repeatCount="indefinite"/>'
    "</rect>"
)
rect(526, 234, 12, 8, "#0d1228")
rect(498, 242, 68, 6, "#0d1228")
rect(530, 228, 4, 4, CYAN, opacity=0.7)

# ---------------------------------------------------------- snake monitor
rect(300, 150, 108, 84, PANEL)
rect(308, 158, 92, 68, "#0d1130")
mini = {(0, 1): L2, (2, 1): L3, (4, 2): L2, (1, 3): L3, (3, 3): L2, (5, 0): L3, (2, 4): L1}
mgx, mgy = 331, 173
for col in range(6):
    for row in range(5):
        rect(mgx + col * 8, mgy + row * 8, 6, 6, mini.get((col, row), GRID_EMPTY))
rect(348, 234, 12, 8, "#0d1228")
rect(326, 242, 56, 6, "#0d1228")

# ------------------------------------------------- keyboard, mouse, mug
rect(436, 236, 168, 12, "#1b2251", rx=2)
rect(444, 239, 152, 2, "#2a3160")
rect(444, 242, 152, 2, "#2a3160")
rect(470, 245, 100, 3, "#2f3770")
rect(614, 240, 16, 8, "#1b2251", rx=2)
rect(650, 226, 18, 22, MUG)
rect(650, 226, 18, 3, MUG_RIM)
rect(668, 230, 3, 14, MUG)
anim_steam(654, 214, 2.4, 0)
anim_steam(660, 208, 2.4, 0.8)
anim_steam(656, 202, 2.4, 1.6)

# ------------------------------------------------------------------- plant
rect(236, 272, 32, 24, POT)
rect(232, 268, 40, 6, POT_RIM)
rect(244, 246, 8, 26, LEAF1)
rect(252, 238, 8, 34, LEAF2)
rect(260, 248, 8, 24, LEAF1)
rect(238, 252, 8, 20, LEAF3)
rect(266, 254, 6, 18, LEAF3)
rect(250, 232, 8, 8, LEAF2)

# ------------------------------------------------------------------- snake
E.append(
    '<g transform="translate(0 0)">'
    f'<rect x="144" y="282" width="10" height="10" fill="{SNAKE_BODY}"/>'
    f'<rect x="156" y="282" width="10" height="10" fill="{SNAKE_BODY}"/>'
    f'<rect x="168" y="282" width="10" height="10" fill="{SNAKE_BODY}"/>'
    f'<rect x="180" y="280" width="12" height="12" fill="{SNAKE_HEAD}"/>'
    f'<rect x="184" y="283" width="3" height="3" fill="#0b1220"/>'
    f'<rect x="192" y="285" width="6" height="2" fill="{TONGUE}"/>'
    '<animateTransform attributeName="transform" type="translate" values="0 0;1080 0" dur="30s" repeatCount="indefinite"/>'
    "</g>"
)

# ------------------------------------------------------------------- output
svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    'role="img" aria-label="Pixel art night coding desk banner for 0xrafiKaji">'
    "<defs>"
    '<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#05081a" stop-opacity="0"/>'
    '<stop offset="1" stop-color="#05081a" stop-opacity="0.5"/>'
    "</linearGradient>"
    "</defs>"
    '<g shape-rendering="crispEdges">' + "".join(E) + "</g>"
    "</svg>"
)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg, encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
