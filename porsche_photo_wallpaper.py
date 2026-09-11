"""Composite a photo with the 911 Turbo S illustration into one phone wallpaper.

The photo fills the upper frame, fades into a dark lower panel, and the car
sits in that panel under a warm glow. Rasterizes to PNG at phone resolution.
"""

import base64
import os
import sys

import cairosvg

import porsche_wallpaper as pw

W, H = 1290, 2796
PHOTO_H = 1960.0                 # photo occupies the top of the frame
CAR_GROUND = 2145.0
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wallpapers")

DEFAULT_PHOTO = "/root/.claude/uploads/051a95ce-5139-582f-a306-12d1c43b774f/34735274-image.jpg"


def photo_layer(path, src_w, src_h):
    """Cover-fit the photo to the top band, cropping toward the subject."""
    scale = PHOTO_H / src_h
    w = src_w * scale
    x = -(w - W) * 0.35          # subject sits right of centre, so crop the left harder
    mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return (
        f'<image x="{x:.1f}" y="0" width="{w:.1f}" height="{PHOTO_H:.1f}" '
        f'preserveAspectRatio="none" href="data:{mime};base64,{data}"/>'
    )


def jpeg_size(path):
    import struct
    d = open(path, "rb").read()
    i = 2
    while i < len(d):
        if d[i] != 0xFF:
            i += 1
            continue
        if d[i + 1] in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", d[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", d[i + 2:i + 4])[0]
    raise ValueError("no JPEG frame header")


def build_svg(photo_path):
    src_w, src_h = jpeg_size(photo_path)
    car_scale = 1.02
    car_x = (W - pw.CAR_W * car_scale) / 2.0
    car_y = CAR_GROUND - pw.GROUND * car_scale
    car = pw.car()

    return f'''<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="scrim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#07080b" stop-opacity="0"/>
      <stop offset="34%" stop-color="#07080b" stop-opacity="0.45"/>
      <stop offset="68%" stop-color="#07080b" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#07080b" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="topScrim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#07080b" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#07080b" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="heat" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff4a24" stop-opacity="0.30"/>
      <stop offset="55%" stop-color="#c22c12" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#c22c12" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0.06" y2="1">
      <stop offset="0%" stop-color="#f8fafd"/>
      <stop offset="10%" stop-color="#e0e5ed"/>
      <stop offset="26%" stop-color="#b2b9c5"/>
      <stop offset="40%" stop-color="#6a717f"/>
      <stop offset="50%" stop-color="#464d58"/>
      <stop offset="63%" stop-color="#939aa7"/>
      <stop offset="80%" stop-color="#9aa1ad"/>
      <stop offset="92%" stop-color="#565c66"/>
      <stop offset="100%" stop-color="#2a2e35"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#d4dae3"/>
      <stop offset="100%" stop-color="#3b4048"/>
    </linearGradient>
    <linearGradient id="haunchGrad" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.35"/>
    </linearGradient>
    <linearGradient id="fenderGrad" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.25"/>
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
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.26"/>
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

  <rect width="{W}" height="{H}" fill="#07080b"/>
  {photo_layer(photo_path, src_w, src_h)}

  <!-- keep the clock legible, and fade the photo into the lower panel -->
  <rect x="0" y="0" width="{W}" height="520" fill="url(#topScrim)"/>
  <rect x="0" y="1300" width="{W}" height="{PHOTO_H - 1300:.0f}" fill="url(#scrim)"/>

  <ellipse cx="700" cy="{CAR_GROUND - 70}" rx="820" ry="400" fill="url(#heat)"/>
  <rect x="0" y="{CAR_GROUND:.0f}" width="{W}" height="1.5" fill="#ffffff" opacity="0.10"/>

  <g mask="url(#reflectMask)" filter="url(#softBlur)">
    <g transform="translate({car_x:.1f},{CAR_GROUND + pw.GROUND * car_scale:.1f})
                  scale({car_scale},{-car_scale})">
      {car}
    </g>
  </g>

  <g transform="translate({car_x:.1f},{car_y:.1f}) scale({car_scale})">
    {car}
  </g>

  <g font-family="Liberation Sans, DejaVu Sans, sans-serif" text-anchor="middle">
    <text x="645" y="2418" fill="#ffffff" fill-opacity="0.96" font-size="88"
          font-weight="bold" letter-spacing="9">911 TURBO S</text>
    <text x="645" y="2470" fill="#ff4a24" fill-opacity="0.9" font-size="24"
          letter-spacing="14">640 HP  ·  0-60 IN 2.6s</text>
  </g>
</svg>'''


def main():
    photo = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PHOTO
    os.makedirs(OUT_DIR, exist_ok=True)
    svg = build_svg(photo)
    png_path = os.path.join(OUT_DIR, "porsche_photo_wallpaper.png")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=png_path,
                     output_width=W, output_height=H)
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
