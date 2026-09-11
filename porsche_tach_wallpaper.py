"""Generate a phone wallpaper of a 911 Turbo S tachometer.

Pure geometry: swept dial, tick band, redline arc, needle. Rasterizes to PNG
at phone resolution.
"""

import math
import os

import cairosvg

W, H = 1290, 2796
CX, CY, R = 645.0, 1400.0, 470.0
START_DEG, END_DEG = 140.0, 400.0      # lower-left, clockwise over the top
VMAX = 9.0                             # x1000 rpm
REDLINE = 7.0
NEEDLE_AT = 7.0

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wallpapers")


def ang(v):
    return math.radians(START_DEG + (END_DEG - START_DEG) * (v / VMAX))


def pt(v, r):
    a = ang(v)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def arc(v0, v1, r):
    x0, y0 = pt(v0, r)
    x1, y1 = pt(v1, r)
    large = 1 if (ang(v1) - ang(v0)) > math.pi else 0
    return f"M {x0:.1f},{y0:.1f} A {r},{r} 0 {large} 1 {x1:.1f},{y1:.1f}"


def dial():
    g = []

    # Tick band.
    steps = int(VMAX * 4)
    for i in range(steps + 1):
        v = i / 4.0
        major = abs(v - round(v)) < 1e-6
        r_in = 384 if major else 414
        w = 7 if major else 3
        col = "#ff2f20" if v >= REDLINE else "#e8ecf2"
        x0, y0 = pt(v, r_in)
        x1, y1 = pt(v, 438)
        g.append(
            f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
            f'stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
        )

    # Numerals.
    for i in range(int(VMAX) + 1):
        x, y = pt(float(i), 328)
        col = "#ff2f20" if i >= REDLINE else "#f2f5fa"
        g.append(
            f'<text x="{x:.1f}" y="{y + 26:.1f}" fill="{col}" font-size="74" '
            f'font-weight="bold" text-anchor="middle" '
            f'font-family="Liberation Sans, DejaVu Sans, sans-serif">{i}</text>'
        )

    # Redline band.
    g.append(
        f'<path d="{arc(REDLINE, VMAX, 448)}" fill="none" stroke="#ff2f20" '
        f'stroke-width="13" stroke-linecap="butt"/>'
    )
    g.append(
        f'<path d="{arc(REDLINE, VMAX, 448)}" fill="none" stroke="#ff2f20" '
        f'stroke-width="13" stroke-linecap="butt" filter="url(#glow)" opacity="0.85"/>'
    )

    # Needle, swept to the redline.
    a = ang(NEEDLE_AT)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    def P(along, across):
        return (CX + along * ux + across * px, CY + along * uy + across * py)
    tip_r, tip_l = P(406, 5.5), P(406, -5.5)
    tail_r, tail_l = P(-78, 17), P(-78, -17)
    g.append(
        f'<path d="M {tip_r[0]:.1f},{tip_r[1]:.1f} L {tail_r[0]:.1f},{tail_r[1]:.1f} '
        f'L {tail_l[0]:.1f},{tail_l[1]:.1f} L {tip_l[0]:.1f},{tip_l[1]:.1f} Z" '
        f'fill="url(#needleGrad)" filter="url(#glow)"/>'
    )

    # Hub.
    g.append(f'<circle cx="{CX}" cy="{CY}" r="48" fill="#14171c"/>')
    g.append(f'<circle cx="{CX}" cy="{CY}" r="48" fill="none" stroke="url(#chrome)" stroke-width="6"/>')
    g.append(f'<circle cx="{CX}" cy="{CY}" r="14" fill="#3a3f48"/>')
    return "".join(g)


def build_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="#0d1015"/>
      <stop offset="50%" stop-color="#15191f"/>
      <stop offset="100%" stop-color="#06070a"/>
    </linearGradient>
    <radialGradient id="face" cx="50%" cy="38%" r="62%">
      <stop offset="0%" stop-color="#23272f"/>
      <stop offset="62%" stop-color="#13161b"/>
      <stop offset="100%" stop-color="#090b0e"/>
    </radialGradient>
    <radialGradient id="heat" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff4a24" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#ff4a24" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="#e9edf3"/>
      <stop offset="38%" stop-color="#8b929d"/>
      <stop offset="60%" stop-color="#4a505a"/>
      <stop offset="100%" stop-color="#c4cad3"/>
    </linearGradient>
    <linearGradient id="needleGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff6a3d"/>
      <stop offset="100%" stop-color="#e01508"/>
    </linearGradient>
    <filter id="glow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="12" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <ellipse cx="{CX}" cy="{CY + 120}" rx="880" ry="760" fill="url(#heat)"/>

  <circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="url(#chrome)" stroke-width="16"/>
  <circle cx="{CX}" cy="{CY}" r="{R - 14}" fill="url(#face)"/>
  <circle cx="{CX}" cy="{CY}" r="{R - 14}" fill="none" stroke="#000000" stroke-opacity="0.6" stroke-width="3"/>

  {dial()}

  <g font-family="Liberation Sans, DejaVu Sans, sans-serif" text-anchor="middle">
    <text x="{CX}" y="{CY - 176}" fill="#ffffff" fill-opacity="0.5" font-size="32"
          letter-spacing="12">1/min x1000</text>
    <text x="{CX}" y="{CY + 232}" fill="#ffffff" fill-opacity="0.28" font-size="27"
          letter-spacing="9">PORSCHE</text>

    <text x="{CX}" y="2148" fill="#ffffff" fill-opacity="0.96" font-size="116"
          font-weight="bold" letter-spacing="10">911 TURBO S</text>
    <text x="{CX}" y="2210" fill="#ff3a25" fill-opacity="0.92" font-size="30"
          letter-spacing="16">3.7 TWIN-TURBO FLAT-SIX</text>
    <rect x="485" y="2258" width="320" height="1" fill="#ffffff" opacity="0.18"/>
    <text x="{CX}" y="2322" fill="#ffffff" fill-opacity="0.44" font-size="28"
          letter-spacing="8">640 HP  ·  0-60 IN 2.6s  ·  205 MPH</text>
  </g>
</svg>'''


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svg = build_svg()
    svg_path = os.path.join(OUT_DIR, "porsche_911_turbo_s_tach.svg")
    png_path = os.path.join(OUT_DIR, "porsche_911_turbo_s_tach.png")
    with open(svg_path, "w") as f:
        f.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=png_path,
                     output_width=W, output_height=H)
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
