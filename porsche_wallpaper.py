"""Generate a phone wallpaper of a Porsche 911 Turbo S.

Draws the car as vector art (no external image assets), then rasterizes to PNG
at phone resolution. Run it and the PNG lands in wallpapers/.
"""

import math
import os

import cairosvg

W, H = 1290, 2796          # iPhone Pro class canvas
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wallpapers")

# Car is drawn in a 1000 x 287 local space, then scaled onto the canvas.
CAR_W = 1000.0
GROUND = 287.0
FRONT_AXLE, REAR_AXLE = 229.0, 769.0
AXLE_Y = 211.0
TIRE_R = 79.0


def wheel(cx, cy, r):
    """Tire, forged rim, carbon-ceramic disc and yellow caliper."""
    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0a0b0e"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 1}" fill="none" stroke="#3a3f47" stroke-width="1.4"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 17}" fill="#101216"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 21}" fill="url(#rimGrad)"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 27}" fill="#1b1e24"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 31}" fill="#2e333b"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 31}" fill="none" stroke="#454b55" stroke-width="1"/>',
    ]
    # Caliper sits upper-rear of the hub.
    parts.append(
        f'<path d="M {cx - 4},{cy - r + 28} a {r - 30},{r - 30} 0 0 0 -26,21 '
        f'l 10,8 a {r - 40},{r - 40} 0 0 1 20,-17 Z" fill="#edc63c"/>'
    )

    inner, outer = r - 29, r - 22
    n = 11
    for i in range(n):
        a = math.radians(i * 360.0 / n)
        twist = math.radians(8)
        half_o, half_i = math.radians(7.0), math.radians(3.4)
        pts = [
            (cx + outer * math.cos(a - half_o), cy + outer * math.sin(a - half_o)),
            (cx + outer * math.cos(a + half_o), cy + outer * math.sin(a + half_o)),
            (cx + inner * math.cos(a + twist + half_i), cy + inner * math.sin(a + twist + half_i)),
            (cx + inner * math.cos(a + twist - half_i), cy + inner * math.sin(a + twist - half_i)),
        ]
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        parts.append(f'<polygon points="{d}" fill="url(#spokeGrad)"/>')

    parts.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#c9ced7"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#8f0f18"/>')
    return "".join(parts)


TOP_EDGE = (
    "M 22,206 "
    "C 12,192 10,170 18,152 "        # low, round leading edge
    "C 30,128 56,110 92,100 "        # short nose
    "C 130,88 176,74 222,62 "        # fender crest climbs fast
    "C 256,54 288,50 312,52 "        # crest
    "C 322,54 328,58 332,62 "        # notch into the cowl
    "C 358,38 402,16 462,8 "         # windscreen, set forward
    "L 556,7 "                       # roof
    "C 648,13 744,23 838,37 "        # unbroken fastback
    "C 894,46 936,57 960,73 "
    "C 979,86 990,105 992,128 "      # tail shoulder
)


def arch(axle, sill=238.0):
    """Wheel-arch opening, drawn right to left. Clears the tyre top by ~90 mm."""
    half, top = 92.0, 110.0
    return (
        f"L {axle + half},{sill} "
        f"C {axle + 104},182 {axle + 62},{top} {axle},{top} "
        f"C {axle - 62},{top} {axle - 104},182 {axle - half},{sill} "
    )


def car():
    body = (
        TOP_EDGE
        + "C 994,158 990,188 980,209 "
        "C 971,227 957,237 941,238 "
        + arch(REAR_AXLE)
        + f"L {FRONT_AXLE + 92},238 "
        + arch(FRONT_AXLE)
        + "L 40,238 "
        "C 30,236 24,224 22,206 Z"
    )

    glass = (
        "M 346,58 "
        "C 378,36 418,18 470,10 "
        "L 552,8 "
        "C 618,15 684,25 742,38 "
        "Z"
    )

    g = []
    g.append('<ellipse cx="500" cy="284" rx="470" ry="12" fill="url(#shadowGrad)"/>')

    # Dark arch interiors sit behind the wheels so the openings read as cutouts.
    for axle in (FRONT_AXLE, REAR_AXLE):
        g.append(
            f'<path d="M {axle - 92},238 C {axle - 104},182 {axle - 62},110 {axle},110 '
            f'C {axle + 62},110 {axle + 104},182 {axle + 92},238 Z" fill="#050608"/>'
        )
    g.append(wheel(FRONT_AXLE, AXLE_Y, TIRE_R))
    g.append(wheel(REAR_AXLE, AXLE_Y, TIRE_R))

    # Deployed rear wing.
    g.append(
        '<path d="M 782,24 C 844,10 910,4 962,8 L 964,23 '
        'C 910,19 846,25 788,38 Z" fill="url(#wingGrad)" stroke="#090a0d" stroke-width="1.1"/>'
    )
    g.append('<path d="M 834,34 l 11,0 l -4,13 l -11,0 Z" fill="#14161b"/>')
    g.append('<path d="M 926,28 l 11,0 l -4,15 l -11,0 Z" fill="#14161b"/>')

    g.append(f'<path d="{body}" fill="url(#bodyGrad)"/>')

    # Rear haunch.
    g.append(
        '<path d="M 636,14 C 720,30 790,86 812,166 C 822,202 826,226 825,238 '
        'L 706,238 C 720,176 704,94 646,16 Z" fill="url(#haunchGrad)" opacity="0.40"/>'
    )
    # Front fender.
    g.append(
        '<path d="M 26,150 C 86,88 200,54 318,52 C 238,80 168,116 146,170 '
        'C 130,202 126,224 128,238 L 34,238 C 20,206 16,172 26,150 Z" '
        'fill="url(#fenderGrad)" opacity="0.30"/>'
    )
    # Arch lips.
    for axle in (FRONT_AXLE, REAR_AXLE):
        g.append(
            f'<path d="M {axle - 92},238 C {axle - 104},182 {axle - 62},110 {axle},110 '
            f'C {axle + 62},110 {axle + 104},182 {axle + 92},238 '
            f'L {axle + 83},238 C {axle + 94},184 {axle + 56},119 {axle},119 '
            f'C {axle - 56},119 {axle - 94},184 {axle - 83},238 Z" fill="#0a0b0e" opacity="0.55"/>'
        )
    # Rocker panel, sitting proud of the body sides.
    g.append(
        '<path d="M 316,238 L 682,238 C 652,222 578,214 500,214 '
        'C 422,214 348,222 316,238 Z" fill="#0c0e12" opacity="0.92"/>'
    )
    # Flank crease.
    g.append(
        '<path d="M 140,146 C 300,122 490,116 704,136" fill="none" '
        'stroke="#f6f9fd" stroke-opacity="0.2" stroke-width="2.8"/>'
    )

    g.append(f'<path d="{glass}" fill="url(#glassGrad)"/>')
    g.append(f'<path d="{glass}" fill="none" stroke="#090a0d" stroke-width="3"/>')
    g.append('<path d="M 552,8 L 538,27" fill="none" stroke="#090a0d" stroke-width="4.5"/>')
    g.append(
        '<path d="M 362,52 C 398,30 436,12 470,10 L 444,11 '
        'C 406,18 376,36 350,56 Z" fill="#d8e8fa" opacity="0.22"/>'
    )

    # Shut lines, handle, mirror.
    g.append('<path d="M 348,230 C 340,174 342,114 350,58" fill="none" stroke="#090a0d" stroke-opacity="0.5" stroke-width="2"/>')
    g.append('<path d="M 548,228 C 544,166 542,98 538,27" fill="none" stroke="#090a0d" stroke-opacity="0.5" stroke-width="2"/>')
    g.append('<rect x="398" y="72" width="38" height="7" rx="3.5" fill="#090a0d" opacity="0.6"/>')
    g.append('<path d="M 358,44 C 338,36 322,40 318,50 L 350,58 Z" fill="#1a1d23"/>')

    # Turbo intakes in the rear quarter.
    for i in range(3):
        x, y = 626 + i * 18, 56 + i * 5
        g.append(f'<path d="M {x},{y} l 32,10 l 0,8 l -32,-10 Z" fill="#090a0d" opacity="0.85"/>')

    # Front intake, splitter, headlight.
    g.append('<path d="M 22,180 C 46,168 78,158 110,152 L 114,176 C 82,182 50,192 30,202 Z" fill="#090a0d" opacity="0.92"/>')
    g.append('<path d="M 22,230 C 44,226 74,224 106,224 L 106,240 L 38,240 Z" fill="#0c0e12"/>')
    g.append('<ellipse cx="86" cy="96" rx="15" ry="21" transform="rotate(-32 86 96)" fill="url(#headGrad)"/>')
    g.append('<ellipse cx="86" cy="96" rx="15" ry="21" transform="rotate(-32 86 96)" fill="none" stroke="#090a0d" stroke-width="2.4"/>')
    g.append('<ellipse cx="82" cy="90" rx="6" ry="9" transform="rotate(-32 82 90)" fill="#ffffff" opacity="0.9"/>')

    # Tail light bar, diffuser, pipes.
    g.append('<path d="M 942,96 C 962,96 982,106 991,120 L 986,136 C 975,122 962,114 940,112 Z" fill="#ff2e1e" filter="url(#glow)"/>')
    g.append('<rect x="886" y="216" width="80" height="22" rx="5" fill="#090a0d"/>')
    g.append('<rect x="892" y="206" width="28" height="9" rx="4" fill="#2c3037"/>')
    g.append('<rect x="930" y="206" width="28" height="9" rx="4" fill="#2c3037"/>')

    g.append(
        f'<path d="{TOP_EDGE}" fill="none" stroke="#ffffff" stroke-opacity="0.6" '
        'stroke-width="2.4" stroke-linecap="round"/>'
    )
    return "".join(g)


def build_svg():
    car_scale = 1.22
    car_x = (W - CAR_W * car_scale) / 2.0
    car_y = 1360.0
    car_body = car()

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0%" stop-color="#0e1116"/>
      <stop offset="45%" stop-color="#171b23"/>
      <stop offset="100%" stop-color="#07080b"/>
    </linearGradient>
    <radialGradient id="heat" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff4a24" stop-opacity="0.30"/>
      <stop offset="55%" stop-color="#c22c12" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#c22c12" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="cool" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5f8dff" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#5f8dff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0.06" y2="1">
      <stop offset="0%" stop-color="#f8fafd"/>
      <stop offset="10%" stop-color="#e0e5ed"/>
      <stop offset="26%" stop-color="#b2b9c5"/>
      <stop offset="40%" stop-color="#6a717f"/>
      <stop offset="50%" stop-color="#464d58"/>
      <stop offset="63%" stop-color="#939aa7"/>
      <stop offset="80%" stop-color="#bcc3ce"/>
      <stop offset="92%" stop-color="#6c727d"/>
      <stop offset="100%" stop-color="#363b43"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#d4dae3"/>
      <stop offset="100%" stop-color="#3b4048"/>
    </linearGradient>
    <linearGradient id="fenderGrad" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.25"/>
    </linearGradient>
    <linearGradient id="haunchGrad" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.35"/>
    </linearGradient>
    <linearGradient id="glassGrad" x1="0.1" y1="0" x2="0.7" y2="1">
      <stop offset="0%" stop-color="#2b3340"/>
      <stop offset="60%" stop-color="#12161d"/>
      <stop offset="100%" stop-color="#080a0d"/>
    </linearGradient>
    <linearGradient id="rimGrad" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="#9aa1ac"/>
      <stop offset="100%" stop-color="#3a3e46"/>
    </linearGradient>
    <linearGradient id="spokeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c9ced7"/>
      <stop offset="100%" stop-color="#5b606a"/>
    </linearGradient>
    <linearGradient id="headGrad" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="#f4f8ff"/>
      <stop offset="100%" stop-color="#6f7a8c"/>
    </linearGradient>
    <radialGradient id="shadowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <mask id="reflectMask">
      <rect x="0" y="0" width="{W}" height="{H}" fill="url(#fade)"/>
    </mask>
    <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <ellipse cx="900" cy="1560" rx="900" ry="620" fill="url(#heat)"/>
  <ellipse cx="240" cy="1180" rx="760" ry="560" fill="url(#cool)"/>

  <!-- horizon -->
  <rect x="0" y="1718" width="{W}" height="1.5" fill="#ffffff" opacity="0.10"/>

  <!-- reflection -->
  <g mask="url(#reflectMask)" filter="url(#softBlur)">
    <g transform="translate({car_x:.1f},{car_y + GROUND * car_scale * 2:.1f})
                  scale({car_scale},{-car_scale})">
      {car_body}
    </g>
  </g>

  <g transform="translate({car_x:.1f},{car_y:.1f}) scale({car_scale})">
    {car_body}
  </g>

  <g font-family="Liberation Sans, DejaVu Sans, sans-serif" text-anchor="middle">
    <text x="645" y="1214" fill="#ffffff" fill-opacity="0.30" font-size="34"
          letter-spacing="26">PORSCHE</text>
    <text x="645" y="2076" fill="#ffffff" fill-opacity="0.95" font-size="112"
          font-weight="bold" letter-spacing="10">911 TURBO S</text>
    <text x="645" y="2136" fill="#ff4a24" fill-opacity="0.9" font-size="30"
          letter-spacing="16">3.7 TWIN-TURBO FLAT-SIX</text>
    <rect x="485" y="2182" width="320" height="1" fill="#ffffff" opacity="0.18"/>
    <text x="645" y="2246" fill="#ffffff" fill-opacity="0.42" font-size="28"
          letter-spacing="8">640 HP  ·  0-60 IN 2.6s  ·  205 MPH</text>
  </g>
</svg>'''


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svg = build_svg()
    svg_path = os.path.join(OUT_DIR, "porsche_911_turbo_s.svg")
    png_path = os.path.join(OUT_DIR, "porsche_911_turbo_s.png")
    with open(svg_path, "w") as f:
        f.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=png_path,
                     output_width=W, output_height=H)
    print(f"wrote {svg_path}")
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
