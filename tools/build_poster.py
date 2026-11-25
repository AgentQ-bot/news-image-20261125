#!/usr/bin/env python3
"""Build the news poster for make.fun news-image-20261125.

Draws a 1024x1024 newspaper-style poster with PIL only (no generated
artwork, so the whole image is reproducible from this script):
  masthead with the date -> drawn globe band -> six-story grid -> footer.
Every word on the poster is rendered in code with DejaVu Sans, so the
headlines stay crisp and legible at small size.
Output: ../entry.png (PNG, <= 1 MiB, <= 1024x1024).

Stories: six genuine 25 November 2026 stories, each corroborated by at
least two independent outlets on 25 Nov pages (SCMP, Reuters, UN News,
Qatar Tribune, WireMinute):
  1. Houthis hit a Riyadh financial-district tower again, 11 injured.
  2. Pakistan's first astronaut, Zeeshan Ali, flies on China's Shenzhou-24.
  3. Trump awards Rudy Giuliani the Medal of Freedom.
  4. UN chief Guterres urges talks on a global AI safety framework.
  5. Landmine casualties hit a five-year high of 7,000.
  6. Car bomb in a Colombian city wounds 20+ people.
The 24 Nov AFCON/CAS ruling was checked and DROPPED: it was first
reported on Tuesday 24 Nov, so it is not 25 Nov news.
"""
import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "entry.png"

W, H = 1024, 1024
NAVY = (13, 27, 62)
NAVY_LIGHT = (24, 48, 96)
AMBER = (232, 160, 32)
PAPER = (248, 244, 233)
INK = (22, 22, 22)
GREY = (74, 74, 74)
DIVIDER = (214, 208, 190)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         max_w: int) -> list[str]:
    """Greedy word wrap to max_w pixels."""
    lines: list[str] = []
    cur = ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    ("MIDDLE EAST", (178, 32, 32),
     "HOUTHIS HIT RIYADH TOWER AGAIN",
     "Second strike in under a week on the King Abdullah Financial District injures 11 people."),
    ("SPACE", (16, 70, 130),
     "PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
     "Zeeshan Ali flies aboard China's Shenzhou-24, a first for Pakistan's space programme."),
    ("USA", (120, 32, 96),
     "TRUMP HONOURS GIULIANI",
     "President awards Rudy Giuliani the Medal of Freedom, the top US civilian honour."),
    ("TECH", (8, 110, 110),
     "UN CHIEF SEEKS AI SAFETY PACT",
     "Guterres urges states to start talks on a global framework for managing AI risks."),
    ("GLOBAL", (31, 120, 76),
     "LANDMINE TOLL HITS 5-YEAR HIGH",
     "7,000 casualties in a year, the worst since 2021; Myanmar and Syria bear the brunt."),
    ("AMERICAS", (150, 80, 8),
     "CAR BOMB ROCKS COLOMBIA CITY",
     "Blast wounds more than 20 people amid a crackdown on the drug trade."),
]


def draw_globe_band(d: ImageDraw.ImageDraw, top: int, bottom: int) -> None:
    """Stylised globe: gold wireframe sphere on a navy band, with six
    gold dots marking the six stories' regions."""
    d.rectangle([0, top, W, bottom], fill=NAVY_LIGHT)
    cx, cy = W // 2, (top + bottom) // 2
    r = 130
    gold = AMBER
    # sphere outline + meridians / parallels
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=gold, width=4)
    for k in (1, 2, 3):
        d.ellipse([cx - r, cy - r // 3 * k, cx + r, cy + r // 3 * k],
                  outline=gold, width=2)
    for k in (1, 2):
        d.ellipse([cx - r // 3 * k, cy - r, cx + r // 3 * k, cy + r],
                  outline=gold, width=2)
    # faint stars
    for (sx, sy, sr) in [(90, 170, 3), (180, 420, 2), (830, 180, 3),
                         (920, 430, 2), (700, 470, 2), (320, 180, 2),
                         (60, 300, 2), (960, 300, 3)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255))
    # six story dots on the globe (rough world positions)
    spots = [(cx - 88, cy - 18), (cx + 62, cy + 8), (cx - 118, cy - 42),
             (cx + 8, cy - 62), (cx + 42, cy + 52), (cx - 52, cy + 66)]
    for (sx, sy) in spots:
        d.ellipse([sx - 7, sy - 7, sx + 7, sy + 7], fill=gold,
                  outline=(255, 255, 255), width=2)
    # side captions
    cap_f = font(True, 20)
    d.text((36, cy - 12), "SIX STORIES", font=cap_f, fill="white")
    d.text((36, cy + 14), "ONE DAY", font=cap_f, fill=AMBER)
    d.text((W - 36, cy - 12), "AROUND", font=cap_f, fill="white", anchor="ra")
    d.text((W - 36, cy + 14), "THE WORLD", font=cap_f, fill=AMBER, anchor="ra")


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead (0..132) ---
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.text((W // 2, 14), "THE WORLD IN ONE DAY", font=font(True, 54),
           fill="white", anchor="ma")
    d.text((W // 2, 80), "WEDNESDAY, 25 NOVEMBER 2026", font=font(True, 30),
           fill=AMBER, anchor="ma")
    d.rectangle([0, 130, W, 134], fill=AMBER)

    # --- globe band (134..500) ---
    draw_globe_band(d, 134, 500)

    # --- story grid (502..972): 2 cols x 3 rows ---
    grid_top, grid_bottom = 502, 972
    col_w, row_h = W // 2, (grid_bottom - grid_top) // 3
    for i, (tag, colour, headline, summary) in enumerate(STORIES):
        col, row = i % 2, i // 2
        cx, cy = col * col_w, grid_top + row * row_h
        if col == 1:
            d.line([col_w, cy, col_w, cy + row_h], fill=DIVIDER, width=2)
        if row > 0:
            d.line([0, cy, W, cy], fill=DIVIDER, width=2)
        px, py = cx + 18, cy + 14
        tag_f = font(True, 16)
        tw = d.textlength(tag, font=tag_f)
        d.rounded_rectangle([px, py, px + tw + 18, py + 26], radius=4, fill=colour)
        d.text((px + 9, py + 4), tag, font=tag_f, fill="white")
        hl_f = font(True, 23)
        hl_lines = wrap(d, headline, hl_f, col_w - 36)[:2]
        hy = py + 36
        for line in hl_lines:
            d.text((px, hy), line, font=hl_f, fill=INK)
            hy += 28
        sm_f = font(False, 18)
        sm_lines = wrap(d, summary, sm_f, col_w - 36)[:3]
        sy = hy + 4
        for line in sm_lines:
            d.text((px, sy), line, font=sm_f, fill=GREY)
            sy += 23

    # --- footer (972..1024) ---
    d.rectangle([0, 972, W, H], fill=NAVY)
    d.text((W // 2, 990),
           "25 NOVEMBER 2026  \u2022  As reported by SCMP, Reuters, UN News and others  "
           "\u2022  make.fun news-image-20261125",
           font=font(False, 16), fill="white", anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {img.size} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
