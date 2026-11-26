#!/usr/bin/env python3
"""Draw a one-page newspaper front page summing up the world news of
Thursday 26 November 2026, and save it as entry.png (1024x1024, < 1 MiB).

Everything is drawn from scratch with PIL primitives and system fonts;
no network, no downloaded assets. Deterministic: the same input always
produces the same bytes.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (22, 22, 22)
SOFT = (74, 74, 74)
NAVY = (24, 52, 92)
RED = (178, 28, 28)
GOLD = (176, 132, 24)
RULE = (150, 140, 120)
PANEL = (255, 253, 246)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after the last line."""
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hrule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_bars(draw, x, y, w, h, data, color=NAVY, hi=RED):
    """Simple vertical bar chart. data: list of (label, value)."""
    n = len(data)
    gap = 14
    bw = (w - gap * (n - 1)) // n
    top = max(v for _, v in data)
    base = y + h - 26
    for i, (label, value) in enumerate(data):
        bx = x + i * (bw + gap)
        bh = int((h - 40) * value / top)
        c = hi if value == top else color
        draw.rectangle([bx, base - bh, bx + bw, base], fill=c)
        draw.text((bx + bw / 2, base - bh + 8), str(value) + "%",
                  font=font(SANS_B, 19), fill=(255, 255, 255), anchor="ma")
        draw.text((bx + bw / 2, base + 5), label,
                  font=font(SANS, 16), fill=SOFT, anchor="ma")
    draw.line([(x, base), (x + w, base)], fill=INK, width=2)


def draw_planet(draw, cx, cy, r):
    r = 36
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 120, 178))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    for dx, dy, wr in ((-r * 0.45, -r * 0.2, r * 0.5),
                       (r * 0.35, r * 0.35, r * 0.35)):
        draw.ellipse([cx + dx - wr, cy + dy - wr * 0.6,
                      cx + dx + wr, cy + dy + wr * 0.6],
                     fill=(140, 185, 220))
    draw.arc([cx - r - 22, cy - 12, cx + r + 22, cy + 12],
             start=200, end=340, fill=GOLD, width=5)
    # little rocket climbing away
    rx, ry = cx + r - 10, cy - r - 2
    draw.polygon([(rx, ry - 16), (rx - 8, ry + 8), (rx + 8, ry + 8)],
                 fill=RED)
    draw.rectangle([rx - 8, ry + 8, rx + 8, ry + 18], fill=INK)
    draw.polygon([(rx - 8, ry + 18), (rx - 14, ry + 30), (rx - 2, ry + 22)],
                 fill=GOLD)
    draw.polygon([(rx + 8, ry + 18), (rx + 14, ry + 30), (rx + 2, ry + 22)],
                 fill=GOLD)


def draw_cross_memorial(draw, cx, cy, s):
    # a small memorial: cross above three bars
    draw.line([(cx, cy - s), (cx, cy + s * 0.4)], fill=INK, width=7)
    draw.line([(cx - s * 0.55, cy - s * 0.55), (cx + s * 0.55, cy - s * 0.55)],
              fill=INK, width=7)
    for i, hgt in enumerate((0.5, 0.8, 0.62)):
        bx = cx - s + i * s
        draw.rectangle([bx, cy + s * 0.9 - s * hgt, bx + s * 0.62,
                        cy + s * 0.9], fill=NAVY)


def draw_burst(draw, cx, cy, r, color=RED):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
                 fill=GOLD)


def draw_drone(draw, cx, cy, s):
    draw.line([(cx - s, cy - s), (cx + s, cy + s)], fill=INK, width=5)
    draw.line([(cx - s, cy + s), (cx + s, cy - s)], fill=INK, width=5)
    for px, py in ((cx - s, cy - s), (cx + s, cy - s),
                   (cx - s, cy + s), (cx + s, cy + s)):
        draw.ellipse([px - 13, py - 13, px + 13, py + 13],
                     outline=INK, width=4, fill=PANEL)
    draw.rectangle([cx - 12, cy - 9, cx + 12, cy + 9], fill=NAVY)


def draw_chip(draw, cx, cy, s):
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(30, 30, 34))
    draw.rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55],
                   outline=(180, 190, 205), width=3)
    for i in (-1, 0, 1):
        off = i * s * 0.55
        draw.line([(cx + off, cy - s - 12), (cx + off, cy - s)], fill=INK, width=4)
        draw.line([(cx + off, cy + s), (cx + off, cy + s + 12)], fill=INK, width=4)
        draw.line([(cx - s - 12, cy + off), (cx - s, cy + off)], fill=INK, width=4)
        draw.line([(cx + s, cy + off), (cx + s + 12, cy + off)], fill=INK, width=4)
    draw.polygon([(cx + s * 0.7, cy + s * 0.55), (cx + s * 0.95, cy + s * 0.8),
                  (cx + s * 0.45, cy + s * 0.8)], fill=RED)


def draw_dove(draw, cx, cy, s):
    # stylised white dove with an olive sprig, on a navy disc
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=NAVY)
    draw.ellipse([cx - s * 0.55, cy - s * 0.05, cx + s * 0.55, cy + s * 0.5],
                 fill=(250, 250, 248))
    draw.ellipse([cx + s * 0.28, cy - s * 0.5, cx + s * 0.62, cy - s * 0.16],
                 fill=(250, 250, 248))
    draw.polygon([(cx + s * 0.6, cy - s * 0.38), (cx + s * 0.85, cy - s * 0.3),
                  (cx + s * 0.6, cy - s * 0.22)], fill=GOLD)
    draw.arc([cx - s * 0.5, cy - s * 0.45, cx + s * 0.35, cy + s * 0.25],
             start=300, end=90, fill=(200, 200, 195), width=5)
    draw.line([(cx - s * 0.55, cy + s * 0.35), (cx - s * 0.05, cy + s * 0.62)],
              fill=(90, 140, 70), width=4)
    for t in (0.25, 0.55, 0.85):
        lx = cx - s * 0.55 + t * s * 0.5
        ly = cy + s * 0.35 + t * s * 0.27
        draw.ellipse([lx - 7, ly - 4, lx + 7, ly + 4], fill=(90, 140, 70))


def story_panel(draw, x, y, w, h, kicker, headline, body, icon):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1, fill=PANEL)
    ix, iy = x + 12, y + 12
    icon(draw, ix + 50, iy + 50, 38)
    tx = x + 122
    draw.text((tx, y + 10), kicker, font=font(SANS_B, 19), fill=RED)
    yy = para(draw, tx, y + 36, headline, font(SERIF, 30), w - 136,
              leading=36)
    para(draw, tx, yy + 4, body, font(SANS, 17), w - 136, fill=SOFT,
         leading=20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin

    # ---- masthead ----
    d.text((W // 2, 14), "THE WORLD IN ONE DAY", font=font(SERIF, 64),
           fill=INK, anchor="ma")
    hrule(d, m, W - m, 96, width=3)
    d.text((W // 2, 104), "THURSDAY  26  NOVEMBER  2026",
           font=font(SANS_B, 30), fill=RED, anchor="ma")
    d.text((W // 2, 140), "One day's news from every region — trade, war, space, tech",
           font=font(SERIF_REG, 22), fill=SOFT, anchor="ma")
    hrule(d, m, W - m, 170, width=2)

    # ---- lead story: tariffs ----
    ly = 182
    d.text((m, ly), "TRADE  •  WASHINGTON", font=font(SANS_B, 20), fill=RED)
    yy = para(d, m, ly + 30, "Trump's tariff salvo hits 14 partners; markets slide",
              font(SERIF, 48), 600, leading=54)
    para(d, m, yy + 8,
         "Washington proposes duties of up to 40% on China and 15% on the EU, "
         "Japan and South Korea. The Nasdaq fell about 4% as AI stocks sold off.",
         font(SANS, 22), 600, fill=SOFT, leading=28)
    # chart panel, right of the lead
    cx0, cy0, cw, ch = 664, ly - 4, 332, 212
    d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], outline=RULE, width=1,
                fill=PANEL)
    d.text((cx0 + cw // 2, cy0 + 12), "PROPOSED HEADLINE RATES",
           font=font(SANS_B, 19), fill=INK, anchor="ma")
    draw_bars(d, cx0 + 22, cy0 + 46, cw - 44, ch - 76,
              [("China", 40), ("EU", 15), ("Japan", 15), ("Brazil*", 10)])
    d.text((cx0 + cw // 2, cy0 + ch - 26), "*Brazil aircraft  •  Nasdaq −4%",
           font=font(SANS, 16), fill=SOFT, anchor="ma")
    hrule(d, m, W - m, 414, width=2)

    # ---- six-story grid ----
    gx, gy = m, 428
    cw2, ch2 = (W - 2 * m - 18) // 2, 158
    stories = [
        ("UKRAINE WAR", "Russia's own toll: near 500,000 dead",
         "Moscow's own figures put its Ukraine war dead close to half a million.",
         draw_cross_memorial),
        ("SPACE", "Two firsts above the Earth",
         "First Pakistani joins Tiangong's crew; BepiColombo reaches Mercury.",
         draw_planet),
        ("GAZA", "Israeli strike kills senior Hamas official",
         "An airstrike kills a senior Hamas figure and his family in Gaza.",
         draw_burst),
        ("SUDAN", "Drone strikes kill 19 civilians",
         "Drone attacks in Blue Nile state kill 19 civilians in Sudan's war.",
         draw_drone),
        ("TECH", "Nvidia's Huang is back — stocks slide",
         "Huang returns as Nvidia chief after Trump's push; chip shares fall.",
         draw_chip),
        ("COLOMBIA", "Ten years since the peace accord",
         "A decade on, the UN warns key commitments remain unfinished.",
         draw_dove),
    ]
    for i, (kicker, head, body, icon) in enumerate(stories):
        px = gx + (i % 2) * (cw2 + 18)
        py = gy + (i // 2) * (ch2 + 12)
        story_panel(d, px, py, cw2, ch2, kicker, head, body, icon)

    # ---- footer strip ----
    fy = gy + 3 * ch2 + 2 * 12 + 10
    hrule(d, m, W - m, fy, width=2)
    para(d, m, fy + 10,
         "ALSO TODAY:  Norway's top court voids disputed oil licences  •  "
         "Bangladesh raises garment pay 36%  •  Cairo tanker fire kills 30  •  "
         "Ebola toll in DR Congo passes 5,300  •  US consumer confidence at a "
         "near two-year high.",
         font(SANS, 19), W - 2 * m, fill=SOFT, leading=25)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
