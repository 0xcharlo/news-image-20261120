#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026 (news.png).

A newspaper front page drawn with Pillow: navy masthead, one wide lead
story on GTA VI's record launch, a 2x2 grid of the day's other big
stories, and an ALSO TODAY briefs strip. No image generator is used, so
no text is garbled. Every headline was checked against live reporting.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 244, 236)
CARD = (255, 255, 255)
INK = (24, 24, 24)
NAVY = (13, 38, 68)
NAVY_DEEP = (9, 27, 50)
GOLD = (198, 158, 38)
GOLD_SOFT = (214, 178, 88)
GREY = (98, 98, 98)
RULE = (214, 208, 194)
CRIMSON = (172, 40, 46)
TEAL = (23, 96, 110)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def draw_lines(draw, x, y, lines, fnt, fill, step):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


# ------------------------------------------------------------------ scenes
def scene_vice_city(draw, x0, y0, x1, y1):
    """Wide Vice City sunset: orange sky, big sun, skyline, bay water."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y0 + h * 0.50], fill=(255, 148, 72))
    draw.rectangle([x0, y0 + h * 0.50, x1, y0 + h * 0.68], fill=(232, 92, 96))
    draw.rectangle([x0, y0 + h * 0.68, x1, y1], fill=(36, 52, 96))
    cx = x0 + (x1 - x0) * 0.30
    cy = y0 + h * 0.44
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(255, 214, 110))
    base = y0 + h * 0.68
    towers = [0.38, 0.58, 0.30, 0.66, 0.46, 0.60, 0.34, 0.52, 0.44, 0.62]
    bw = (x1 - x0) / len(towers)
    for i, frac in enumerate(towers):
        bx = x0 + i * bw
        top = base - frac * h * 0.50
        draw.rectangle([bx + 3, top, bx + bw - 3, base], fill=(28, 32, 44))
        for wy in range(int(top) + 9, int(base) - 5, 13):
            for wx in range(int(bx) + 7, int(bx + bw) - 9, 13):
                if (wx * 7 + wy * 3) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 5],
                                   fill=(255, 214, 110))
    for i, wdt in enumerate((96, 64, 40, 22)):
        yy = y0 + h * 0.76 + i * 10
        draw.rectangle([cx - wdt // 2, yy, cx + wdt // 2, yy + 3],
                       fill=(255, 214, 110))
    # palm silhouettes at both edges: curved trunk + drooping fronds
    for px, lean in ((x0 + 30, 1), (x1 - 30, -1)):
        top_x = px + lean * 16
        top_y = y0 + h * 0.22
        draw.line([(px, y1), (px + lean * 8, y0 + h * 0.60),
                   (top_x, top_y)], fill=(28, 32, 44), width=6)
        for ang, ln in ((-70, 34), (-35, 40), (0, 38), (35, 40), (70, 34)):
            import math
            rad = math.radians(ang)
            ex = top_x + int(math.sin(rad) * ln) * lean
            ey = top_y + int(math.cos(rad) * ln * 0.45) - 6
            draw.line([(top_x, top_y), (ex, ey)], fill=(28, 32, 44),
                      width=4)


def scene_white_house(draw, x0, y0, x1, y1):
    """The White House under a dusky blue sky."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(38, 64, 96))
    for sx, sy in ((0.10, 0.20), (0.24, 0.12), (0.82, 0.18), (0.68, 0.08)):
        draw.ellipse([x0 + (x1 - x0) * sx - 2, y0 + h * sy - 2,
                      x0 + (x1 - x0) * sx + 2, y0 + h * sy + 2],
                     fill=(240, 240, 230))
    cx = (x0 + x1) // 2
    base = y0 + h * 0.92
    draw.rectangle([x0, base, x1, y1], fill=(52, 92, 56))
    draw.rectangle([cx - 58, base - 26, cx + 58, base], fill=(238, 238, 226))
    draw.polygon([(cx - 58, base - 26), (cx + 58, base - 26),
                  (cx, base - 44)], fill=(238, 238, 226))
    for dx in (-44, -26, -8, 10, 28, 46):
        draw.rectangle([cx + dx - 3, base - 24, cx + dx + 3, base],
                       fill=(205, 205, 196))
    draw.rectangle([x0 + 24, base - 14, cx - 64, base], fill=(222, 222, 212))
    draw.rectangle([cx + 64, base - 14, x1 - 24, base], fill=(222, 222, 212))


def scene_court(draw, x0, y0, x1, y1):
    """A courthouse front: pediment, columns, scales of justice."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(228, 228, 220))
    cx = (x0 + x1) // 2
    base = y0 + h * 0.94
    draw.polygon([(cx - 78, y0 + 4), (cx + 78, y0 + 4), (cx, y0 + 20)],
                 fill=NAVY)
    draw.rectangle([cx - 78, y0 + 20, cx + 78, y0 + 25], fill=NAVY)
    for dx in (-62, -32, -2, 28, 58):
        draw.rectangle([cx + dx - 5, y0 + 25, cx + dx + 5, base],
                       fill=(250, 250, 246))
    draw.rectangle([x0, base, x1, y1], fill=(150, 148, 138))
    # scales of justice, hanging between the middle columns
    sx = cx
    sy = y0 + h * 0.58
    draw.line([sx, sy - 13, sx, sy + 13], fill=GOLD, width=3)
    draw.line([sx - 18, sy - 13, sx + 18, sy - 13], fill=GOLD, width=3)
    draw.pieslice([sx - 26, sy + 5, sx - 10, sy + 19], 0, 180, fill=GOLD)
    draw.pieslice([sx + 10, sy + 5, sx + 26, sy + 19], 0, 180, fill=GOLD)
    draw.ellipse([sx - 3, sy - 17, sx + 3, sy - 11], fill=GOLD)


def scene_storm(draw, x0, y0, x1, y1):
    """A cyclone spiral over a dark sea and a coastline."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y0 + h * 0.55], fill=(70, 92, 110))
    draw.rectangle([x0, y0 + h * 0.55, x1, y1], fill=(24, 48, 70))
    cx = x0 + (x1 - x0) * 0.36
    cy = y0 + h * 0.30
    for r, col in ((30, (250, 250, 248)), (22, (205, 214, 220)),
                   (14, (250, 250, 248)), (7, (205, 214, 220))):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
    draw.arc([cx - 44, cy - 30, cx + 44, cy + 44], 200, 340,
             fill=(250, 250, 248), width=5)
    draw.arc([cx - 56, cy - 44, cx + 56, cy + 58], 160, 300,
             fill=(205, 214, 220), width=5)
    # coastline
    draw.polygon([(x0 + (x1 - x0) * 0.62, y0 + h * 0.55),
                  (x1, y0 + h * 0.55), (x1, y1),
                  (x0 + (x1 - x0) * 0.72, y1)], fill=(196, 178, 140))
    for i in range(4):
        yy = y0 + h * 0.72 + i * 10
        for wx in range(x0 + 12, x1 - 60, 52):
            draw.arc([wx, yy, wx + 34, yy + 10], 180, 360,
                     fill=(150, 190, 215))


def scene_chart(draw, x0, y0, x1, y1):
    """A rising bar chart with an arrow: a record market debut."""
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(232, 238, 240))
    base = y0 + h * 0.88
    bars = [0.22, 0.34, 0.28, 0.48, 0.42, 0.62, 0.78]
    bw = (x1 - x0) / (len(bars) + 1)
    for i, frac in enumerate(bars):
        bx = x0 + (i + 0.6) * bw
        top = base - frac * h * 0.72
        draw.rectangle([bx, top, bx + bw * 0.62, base],
                       fill=TEAL if i < len(bars) - 1 else GOLD)
    pts = []
    for i, frac in enumerate(bars):
        bx = x0 + (i + 0.6) * bw + bw * 0.31
        pts.append((bx, base - frac * h * 0.72 - 8))
    draw.line(pts, fill=CRIMSON, width=4)
    ex, ey = pts[-1]
    draw.polygon([(ex, ey - 12), (ex + 16, ey + 2), (ex - 2, ey + 10)],
                 fill=CRIMSON)
    draw.line([x0, base, x1, base], fill=INK, width=2)


# ------------------------------------------------------------------ page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    draw.rectangle([0, 112, W, 116], fill=GOLD)
    draw.text((W / 2, 12), "THE WORLD IN ONE IMAGE",
              font=load(SERIF_B, 54), fill=(255, 255, 255), anchor="ma")
    draw.text((W / 2, 74), "FRIDAY 20 NOVEMBER 2026",
              font=load(SANS_B, 24), fill=GOLD_SOFT, anchor="ma")

    # Lead story: GTA VI
    lx, ly, lw, lh = 24, 132, 976, 318
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD,
                   outline=RULE, width=1)
    scene_vice_city(draw, lx + 1, ly + 1, lx + lw - 1, ly + 156)
    draw.rectangle([lx, ly + 156, lx + lw, ly + 160], fill=GOLD)
    head = fit_lines(draw, "GTA VI SMASHES LAUNCH RECORDS",
                     load(SANS_B, 32), lw - 32)
    y = draw_lines(draw, lx + 16, ly + 170, head, load(SANS_B, 32),
                   NAVY, 38)
    body = fit_lines(
        draw,
        "An estimated 19.1 million copies sold on launch day, about "
        "$1.84 billion in sales \u2014 more than twice GTA V's first day, "
        "per Sensor Tower. Take-Two has not confirmed the figures.",
        load(SANS, 20), lw - 32)
    draw_lines(draw, lx + 16, y + 4, body, load(SANS, 20), INK, 26)

    # 2x2 grid of the day's other stories
    gx, gy = 24, 466
    cw, ch, gap = 476, 172, 16
    stories = [
        ("TRUMP PUTS IRAN DECISION OFF TO 2027",
         "No new strikes before the new year, he says: \u201cWe\u2019ll see "
         "what happens after January 1.\u201d",
         scene_white_house),
        ("WORLD COURT: MYANMAR COMMITTED GENOCIDE",
         "The ICJ finds Myanmar responsible for genocide against the "
         "Rohingya in 2017 and orders reparations.",
         scene_court),
        ("CYCLONE AKVAN HITS INDIA\u2019S EAST COAST",
         "The severe storm crosses the Odisha\u2013Andhra coast today; "
         "nearly 300,000 evacuated, 423 rescue teams deployed.",
         scene_storm),
        ("ANTHROPIC SOARS IN BIGGEST IPO ON RECORD",
         "Shares close up 17% on their Nasdaq debut; the $81.3 billion "
         "offering values the Claude maker near $1.5 trillion.",
         scene_chart),
    ]
    for i, (headline, body, scene) in enumerate(stories):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        draw.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD,
                       outline=RULE, width=1)
        scene(draw, cx + 1, cy + 1, cx + cw - 1, cy + 61)
        draw.rectangle([cx, cy + 61, cx + cw, cy + 65], fill=GOLD)
        h_lines = fit_lines(draw, headline, load(SANS_B, 20), cw - 24)
        y = draw_lines(draw, cx + 12, cy + 72, h_lines, load(SANS_B, 20),
                       NAVY, 24)
        b_lines = fit_lines(draw, body, load(SANS, 16), cw - 24)
        draw_lines(draw, cx + 12, y + 2, b_lines, load(SANS, 16), INK, 20)

    # ALSO TODAY briefs strip
    sy = 842
    draw.rectangle([24, sy, W - 24, sy + 114], fill=CARD,
                   outline=RULE, width=1)
    draw.rectangle([24, sy, W - 24, sy + 34], fill=NAVY)
    draw.text((40, sy + 6), "ALSO TODAY", font=load(SANS_B, 20),
              fill=(255, 255, 255))
    briefs = [
        "NASA confirms Voyager 1 is one light-day from Earth \u2014 16.1 "
        "billion miles out, the farthest any human-made object has flown.",
        "Cyclone Akvan: 69 trains cancelled and schools shut across "
        "India\u2019s east coast as the storm comes ashore.",
    ]
    y = sy + 44
    for brief in briefs:
        draw.ellipse([40, y + 7, 48, y + 15], fill=CRIMSON)
        lines = fit_lines(draw, brief, load(SANS, 17), W - 24 - 64 - 24)
        y = draw_lines(draw, 60, y, lines, load(SANS, 17), INK, 21)
        y += 5

    # Footer
    draw.text((W / 2, 974), "All events of Friday 20 November 2026, as reported.",
              font=load(SERIF, 17), fill=GREY, anchor="ma")

    img.save("news.png", optimize=True)
    print("saved news.png")


if __name__ == "__main__":
    main()
