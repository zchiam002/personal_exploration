"""
Builds `Puss-in-Boots.pdf` -- a printable picture book.

    python3 book.py

Page size is A4 landscape, one scene per page, full-bleed art with a cream
text panel across the foot of the page.
"""

import math
import os

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from art import *          # noqa: F401,F403  -- the illustration toolkit
from art import _rng, _ol, _sack, _boot, _cat_hat   # not exported by *
import story
import story_zh

W, H = landscape(A4)       # 841.89 x 595.28 pt
BASE = 200                 # ground line: where characters put their feet
HERE = os.path.dirname(os.path.abspath(__file__))

pdfmetrics.registerFont(TTFont(
    "Story", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont(
    "Story-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
# WenQuanYi Zen Hei is the one CJK face on this box; it ships only a regular
# weight, so headings in the Mandarin edition are emboldened by overprinting.
pdfmetrics.registerFont(TTFont(
    "Han", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))

LANGS = {
    "en": dict(txt=story, font="Story", bold="Story-Bold", faux=False,
               size=16.5, lead=24.5, cjk=False, out="Puss-in-Boots.pdf"),
    "zh": dict(txt=story_zh, font="Han", bold="Han", faux=True,
               size=18.5, lead=31, cjk=True, out="Puss-in-Boots-zh.pdf"),
}

TXT = story                # current text module
F, FB = "Story", "Story-Bold"
FAUX_BOLD = False
BODY_SIZE, BODY_LEAD, CJK = 16.5, 24.5, False


def set_lang(lang):
    global TXT, F, FB, FAUX_BOLD, BODY_SIZE, BODY_LEAD, CJK
    cfg = LANGS[lang]
    TXT, F, FB = cfg["txt"], cfg["font"], cfg["bold"]
    FAUX_BOLD, CJK = cfg["faux"], cfg["cjk"]
    BODY_SIZE, BODY_LEAD = cfg["size"], cfg["lead"]
    return cfg


def bold_centred(c, x, y, text, size, color):
    """Heading text; overprinted when the face has no real bold."""
    c.setFont(FB, size)
    c.setFillColor(col(color))
    c.drawCentredString(x, y, text)
    if FAUX_BOLD:
        for dx, dy in ((0.8, 0), (0, 0.6), (0.8, 0.6)):
            c.drawCentredString(x + dx, y + dy, text)


def bold_left(c, x, y, text, size, color):
    c.setFont(FB, size)
    c.setFillColor(col(color))
    c.drawString(x, y, text)
    if FAUX_BOLD:
        for dx, dy in ((0.8, 0), (0, 0.6), (0.8, 0.6)):
            c.drawString(x + dx, y + dy, text)


# ------------------------------------------------------------------ text ---

# punctuation that may not begin a line, and that may not end one
NO_LINE_START = "\u3002\uff0c\u3001\uff1b\uff1a\uff1f\uff01\uff09\u300b\u300d\u300f\u201d\u2019\uff65\u2014\u2026"
NO_LINE_END = "\uff08\u300a\u300c\u300e\u201c\u2018"


def wrap(text, font, size, maxw):
    """Word-wrap, honouring explicit newlines in the source text."""
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = f"{line} {word}".strip()
            if pdfmetrics.stringWidth(trial, font, size) <= maxw:
                line = trial
            else:
                if line:
                    out.append(line)
                line = word
        out.append(line)
    return out


def wrap_cjk(text, font, size, maxw):
    """Break Chinese text by character, keeping punctuation off line starts."""
    out = []
    for para in text.split("\n"):
        line = ""
        for ch in para:
            if pdfmetrics.stringWidth(line + ch, font, size) <= maxw:
                line += ch
                continue
            # the character does not fit: push the line, but never let a
            # closing mark start the next one, nor an opening mark end this one
            if ch in NO_LINE_START and line:
                out.append(line[:-1])
                line = line[-1] + ch
            elif line and line[-1] in NO_LINE_END:
                out.append(line[:-1])
                line = line[-1] + ch
            else:
                out.append(line)
                line = ch
        out.append(line)
    return out


def text_panel(c, text, size=None, lead=None, pad=22, margin=None, bottom=30):
    """Cream card across the foot of the page holding the story text."""
    size = BODY_SIZE if size is None else size
    lead = BODY_LEAD if lead is None else lead
    margin = (54 if CJK else 62) if margin is None else margin
    maxw = W - 2 * margin - 2 * pad
    lines = (wrap_cjk if CJK else wrap)(text, F, size, maxw)
    h = len(lines) * lead + 2 * pad - (lead - size) + 4
    x, y = margin, bottom

    c.saveState()
    c.setFillColorRGB(0, 0, 0, 0.10)
    c.roundRect(x + 3, y - 4, W - 2 * margin, h, 20, stroke=0, fill=1)
    c.restoreState()
    rect(c, x, y, W - 2 * margin, h, fill="cream", r=20,
         stroke="#E3D3B0", lw=1.4)

    c.setFillColor(col("ink"))
    c.setFont(F, size)
    ty = y + h - pad - size * 0.86
    for ln in lines:
        c.drawCentredString(W / 2, ty, ln)
        ty -= lead
    return y + h


def folio(c, n):
    """Discreet page number."""
    c.setFont(F, 10)
    c.setFillColor(col("#9C8B76"))
    c.drawCentredString(W / 2, 18, str(n))


# ----------------------------------------------------------- scene pieces ---

def meadow(c, horizon=250, sky_top="sky_day", sky_bot="sky_soft",
           g1="grass", g2="grass_lt", clouds=((150, 470, 1.0), (640, 505, 0.8)),
           sunpos=(735, 495)):
    sky(c, 0, horizon - 10, W, H - horizon + 10, sky_top, sky_bot)
    if sunpos:
        sun(c, *sunpos)
    for cx, cy, s in clouds:
        cloud(c, cx, cy, s)
    hills(c, -20, horizon - 46, W + 40, 60, "#A9CE8E", bumps=4, seedoff=0.6)
    hills(c, -20, horizon - 34, W + 40, 44, "grass_dk", bumps=3, seedoff=2.1)
    ground(c, 0, 0, W, horizon, g1, g2)


def interior(c, wall="#E8D6B8", floor="wood", horizon=250, beams=True):
    rect(c, 0, horizon - 10, W, H - horizon + 10, fill=wall)
    rect(c, 0, 0, W, horizon, fill=floor)
    for i in range(-1, 14):
        stroke_path(c, [(i * 64 - 20, 0), (i * 64 + 40, horizon)],
                    color=shade("wood", 0.86), lw=2.0)
    rect(c, 0, horizon - 16, W, 16, fill=shade("wood", 0.7))
    if beams:
        for bx in (120, 420, 720):
            rect(c, bx - 13, horizon, 26, H - horizon, fill="wood_dk")
        rect(c, 0, H - 42, W, 42, fill="wood_dk")


def stone_hall(c, horizon=250):
    rect(c, 0, horizon - 10, W, H - horizon + 10, fill="stone")
    for row in range(7):
        yy = horizon + 20 + row * 50
        off = 0 if row % 2 == 0 else 44
        for i in range(11):
            rect(c, i * 88 + off - 60, yy, 84, 44, fill=shade("stone", 0.97),
                 stroke=shade("stone", 0.88), lw=1.2)
    rect(c, 0, 0, W, horizon, fill="#B9A98F")
    for i in range(-1, 14):
        rect(c, i * 70 - 20, 0, 66, horizon - 6, fill=shade("#B9A98F", 0.95),
             stroke=shade("#B9A98F", 0.86), lw=1.2)


def banner(c, x, y, w=54, h=120, color="cape", emblem="gold"):
    poly(c, [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h),
             (x, y - h + 18), (x - w / 2, y - h)], fill=color,
         stroke=LINE, lw=1.4)
    circle(c, x, y - h * 0.45, w * 0.26, fill=emblem, stroke=LINE, lw=1.3)


def throne(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, -54, 0, 108, 22, fill="wood_dk", r=4, stroke=LINE, lw=1.5)
    _ol(c, [(-46, 20), (-50, 120), (0, 138), (50, 120), (46, 20)], "cape_dk")
    _ol(c, [(-38, 24), (-40, 96), (0, 108), (40, 96), (38, 24)], "cape")
    for sx in (-1, 1):
        rect(c, sx * 48 - 9, 20, 18, 66, fill="gold_dk", r=5, stroke=LINE, lw=1.4)
        circle(c, sx * 48, 92, 9, fill="gold", stroke=LINE, lw=1.4)
    rect(c, -48, 42, 96, 12, fill="gold", r=4, stroke=LINE, lw=1.3)
    c.restoreState()


def fireplace(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, -110, 0, 220, 190, fill="stone_dk", stroke=LINE, lw=1.6)
    for row in range(6):
        for i in range(5):
            rect(c, -106 + i * 43 + (0 if row % 2 else 20), 6 + row * 30, 40, 27,
                 fill="stone", stroke=shade("stone", 0.87), lw=1.1)
    rect(c, -120, 186, 240, 20, fill="wood_dk", r=4, stroke=LINE, lw=1.6)
    _ol(c, [(-70, 0), (-76, 96), (0, 118), (76, 96), (70, 0)], "#3A3330")
    for i, (rr, cl) in enumerate(((34, "#C0392B"), (25, "#E8862F"),
                                  (15, "#F6C453"))):
        blob(c, [(0, 6 + rr * 2.1), (rr * 0.72, 6 + rr * 0.7), (rr * 0.5, 6),
                 (-rr * 0.5, 6), (-rr * 0.72, 6 + rr * 0.7)], fill=cl,
             tension=0.75)
    for lx in (-40, -12, 18):
        rect(c, lx, 4, 46, 11, fill="wood_dk", r=5, stroke=LINE, lw=1.2)
    c.restoreState()


def cushion(c, x, y, s=1.0, color="cape"):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    _ol(c, [(-40, 4), (-44, 20), (0, 28), (44, 20), (40, 4), (0, -2)], color,
        tension=0.8)
    for sx in (-1, 1):
        for sy in (0, 1):
            star(c, sx * 34, 8 + sy * 12, 4, fill="gold")
    c.restoreState()


def cupboard(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, -60, 0, 120, 210, fill="wood", stroke=LINE, lw=1.8)
    rect(c, -66, 205, 132, 18, fill="wood_dk", r=3, stroke=LINE, lw=1.6)
    for i in range(2):
        rect(c, -52 + i * 54, 12, 48, 88, fill=shade("wood", 0.88),
             stroke=LINE, lw=1.4, r=3)
        rect(c, -52 + i * 54, 112, 48, 84, fill=shade("wood", 0.88),
             stroke=LINE, lw=1.4, r=3)
        circle(c, -32 + i * 54, 56, 3.6, fill="gold_dk")
        circle(c, -32 + i * 54, 154, 3.6, fill="gold_dk")
    c.restoreState()


def road(c, y=BASE, color="path"):
    blob(c, [(-20, y - 70), (W * 0.3, y - 34), (W * 0.66, y - 10),
             (W + 20, y + 8), (W + 20, y - 96), (W * 0.5, y - 108),
             (-20, y - 132)], fill=color, tension=0.85)


def gift_pile(c, x, y):
    """Partridges, fish and a rabbit heaped on a palace table."""
    rect(c, x - 96, y, 192, 14, fill="wood", r=4, stroke=LINE, lw=1.5)
    for dx in (-84, 84):
        rect(c, x + dx - 6, y - 52, 12, 54, fill="wood_dk", stroke=LINE, lw=1.4)
    # fish
    for i, (dx, dy) in enumerate(((-58, 20), (-34, 16))):
        c.saveState()
        c.translate(x + dx, y + dy)
        c.rotate(-8 + i * 12)
        _ol(c, [(0, 0), (22, 10), (44, 2), (22, -10)], "#9FC3D8", tension=0.8)
        poly(c, [(44, 2), (58, 12), (58, -8)], fill="#7FA8C4", stroke=LINE, lw=1.2)
        circle(c, 12, 2, 2.2, fill="ink")
        c.restoreState()
    # partridge
    c.saveState()
    c.translate(x + 34, y + 16)
    _ol(c, [(0, 0), (20, 8), (30, 24), (14, 32), (-8, 24), (-14, 10)],
        "#B98A5E")
    circle(c, 24, 34, 9, fill="#CBA37A", stroke=LINE, lw=1.3)
    poly(c, [(32, 34), (44, 31), (32, 28)], fill="gold_dk", stroke=LINE, lw=1.1)
    circle(c, 27, 36, 1.9, fill="ink")
    c.restoreState()
    draw_rabbit(c, x + 86, y + 14, 0.72, flip=True)


def sparkles_around(c, cx, cy, r=90, n=9, seed=4):
    rnd = _rng(seed)
    for i in range(n):
        a = i * 2 * math.pi / n + rnd() * 0.4
        rr = r * (0.65 + 0.45 * rnd())
        sparkle(c, cx + rr * math.cos(a), cy + rr * math.sin(a),
                4 + 4 * rnd(), color="#FFF3C4", alpha=0.9)


def motion(c, x, y, n=3, w=54, dy=13, color="#FFFFFF", alpha=0.55):
    for i in range(n):
        stroke_path(c, [(x, y + i * dy), (x - w * (0.7 + 0.3 * (i % 2)),
                                          y + i * dy + 3)],
                    color=color, lw=4.0, alpha=alpha)


# ----------------------------------------------------------------- scenes ---

def cover(c):
    sky(c, 0, 250, W, H - 250, "#F7C98B", "#FDE9C4")
    sun(c, 690, 500, 50)
    for cx, cy, s in ((140, 520, 1.2), (430, 556, 0.75), (720, 396, 0.9)):
        cloud(c, cx, cy, s, fill="#FFF6E4")
    for bx, by in ((238, 500), (292, 522), (342, 490)):
        bird(c, bx, by, 1.4, color="#B08A5E")
    hills(c, -20, 236, W + 40, 86, "#B9D69A", bumps=4, seedoff=0.3)
    hills(c, -20, 210, W + 40, 70, "grass_dk", bumps=3, seedoff=2.4)
    castle(c, 726, 262, 0.5, wall="#D8CFC0", roof="#8E5A6B", flag="#C05A6B")
    ground(c, 0, 0, W, 266, "grass", "grass_lt")
    grass_tufts(c, 0, W, 240, n=28, seed=7)
    tree(c, 82, 214, 1.35)
    bush(c, 786, 186, 1.4)
    for fx in (58, 128, 700, 792):
        flower(c, fx, 202, 1.3, petal="#FFFFFF")
    for fx in (172, 646):
        flower(c, fx, 148, 1.4, petal="#F6C453")

    draw_puss(c, 404, 108, 2.05, expr="proud", arm_r="hip", arm_l="doff",
              sword=True, tail="curl", legs="stride")
    sparkles_around(c, 404, 300, 216, 7, seed=11)

    c.saveState()
    c.setFillColorRGB(0, 0, 0, 0.12)
    c.roundRect(147, 464, 548, 112, 26, stroke=0, fill=1)
    c.restoreState()
    rect(c, 144, 468, 548, 112, fill="cream", r=26, stroke="#D9BE8A", lw=2.6)
    rect(c, 156, 480, 524, 88, fill="cream", r=20, stroke="#E7D3AC", lw=1.2)
    bold_centred(c, W / 2 - 5, 512, TXT.TITLE, 52, "#7A3B2E")
    c.setFillColor(col("ink_soft"))
    c.setFont(F, 15)
    c.drawCentredString(W / 2 - 5, 486, TXT.SUBTITLE)
    for sx in (-1, 1):
        star(c, W / 2 - 5 + sx * 232, 524, 9, fill="gold")


def nameplate(c):
    rect(c, 0, 0, W, H, fill="#FBF3E2")
    rect(c, 44, 40, W - 88, H - 80, fill=None, stroke="#DCC69B", lw=3.0, r=18)
    rect(c, 56, 52, W - 112, H - 104, fill=None, stroke="#E8D6B4", lw=1.4, r=12)
    for cx, cy in ((44, 40), (W - 44, 40), (44, H - 40), (W - 44, H - 40)):
        star(c, cx, cy, 11, fill="#DCC69B")

    bold_centred(c, W / 2, 486, TXT.TITLE, 32, "#7A3B2E")
    c.setFillColor(col("ink_soft"))
    c.setFont(F, 13.5)
    c.drawCentredString(W / 2, 458, TXT.BYLINE)

    c.saveState()
    c.translate(W / 2, 236)
    shadow(c, 0, 4, 168, 24, alpha=0.10)
    c.saveState()
    c.translate(-104, 48)
    c.scale(2.7, 2.7)
    c.rotate(6)
    _cat_hat(c)
    c.restoreState()
    c.saveState()
    c.translate(92, 20)
    c.scale(3.1, 3.1)
    c.rotate(-6)
    _boot(c, 0, 0, 0)
    c.restoreState()
    c.restoreState()

    c.setFillColor(col("ink_soft"))
    c.setFont(F, 16)
    c.drawCentredString(W / 2, 168, TXT.BELONGS_TO)
    stroke_path(c, [(W / 2 - 200, 130), (W / 2 + 200, 130)],
                color="#C9BA88", lw=1.8)
    c.setFont(F, 12 if CJK else 10.5)
    c.setFillColor(col("#9C8B76"))
    for i, ln in enumerate(TXT.COLOPHON.split("\n")):
        c.drawCentredString(W / 2, 92 - i * 17, ln)


def s01_three_sons(c):
    meadow(c, 330)
    windmill(c, 108, 316, 1.25)
    cottage(c, 742, 300, 1.1)
    tree(c, 596, 308, 1.0)
    grass_tufts(c, 0, W, 286, n=22, seed=3)
    horse(c, 452, BASE, 0.86, body="#B9B1A6", mane="#6B6058")
    draw_person(c, 214, BASE, 1.5, robe="#8C7A62", hair="hair_brown",
                arm_r="point", expr="happy")
    draw_person(c, 372, BASE, 1.46, robe="#7F8C6A", hair="#5E4630",
                arm_r="hold", expr="happy", flip=True)
    draw_person(c, 636, BASE, 1.52, robe="jack_old", hair="hair_brown",
                expr="sad", arm_r="down", arm_l="down")
    draw_puss(c, 736, BASE, 1.0, hat=False, cape=False, boots=False,
              legs="sit", tail="down", expr="happy", arm_r="down",
              arm_l="down", flip=True)


def s02_a_talking_cat(c):
    meadow(c, 318, clouds=((190, 520, 0.95),), sunpos=None)
    cottage(c, 132, 302, 1.3)
    tree(c, 782, 306, 1.25)
    bush(c, 660, 288, 1.3)
    grass_tufts(c, 0, W, 288, n=20, seed=9)
    for fx in (300, 352, 540):
        flower(c, fx, 268, 1.2, petal="#FFFFFF")
    rect(c, 350, 176, 116, 36, fill="wood_dk", r=9, stroke=LINE, lw=1.8)
    draw_person(c, 408, 212, 1.52, robe="jack_old", expr="surprised",
                arm_l="out", arm_r="out", legs="stride")
    draw_puss(c, 616, BASE, 1.28, hat=False, cape=False, boots=False,
              expr="sly", arm_r="point", arm_l="hip", tail="swish", flip=True)
    for bx, by, br in ((528, 370, 11), (558, 402, 7.5), (582, 428, 5)):
        circle(c, bx, by, br, fill="#FFFFFF", alpha=0.85, stroke="#E0D3BC",
               lw=1.2)


def s03_the_boots(c):
    meadow(c, 314, clouds=((700, 520, 0.95),))
    cottage(c, 742, 298, 1.15)
    grass_tufts(c, 0, W, 284, n=18, seed=12)
    for i in range(26):
        rnd = _rng(i + 2)
        sx = 110 + rnd() * 540
        stroke_path(c, [(sx, 196), (sx + 16, 204), (sx + 32, 196)],
                    color="wheat_dk", lw=2.2)
    draw_puss(c, 330, BASE, 1.95, expr="proud", arm_r="hip", arm_l="out",
              tail="up", legs="stand", hat=False)
    sparkles_around(c, 330, 340, 200, 8, seed=5)
    draw_person(c, 612, BASE, 1.5, robe="jack_old", expr="surprised",
                arm_l="up", arm_r="up", flip=True)


def s04_feather_in_his_hat(c):
    meadow(c, 322, sky_top="#C9E6F4", clouds=((170, 528, 1.05), (630, 488, 0.75)))
    tree(c, 82, 306, 1.3)
    tree(c, 778, 310, 1.1)
    grass_tufts(c, 0, W, 292, n=24, seed=15)
    for fx in (232, 292, 620, 686):
        flower(c, fx, 272, 1.2, petal="#F6C453")
    ellipse(c, 508, 202, 138, 30, fill="water", alpha=0.6)
    ellipse(c, 508, 202, 118, 22, fill="#A8D8EC", alpha=0.7)
    draw_puss(c, 386, 224, 2.0, expr="proud", arm_r="chin", arm_l="hip",
              tail="perk", legs="stand")
    sparkles_around(c, 386, 380, 208, 8, seed=21)
    for bx, by in ((650, 494), (700, 518)):
        bird(c, bx, by, 1.3)


def s05_the_rabbit(c):
    meadow(c, 336, g1="#93C973", g2="#ADD98C",
           clouds=((200, 524, 1.05), (672, 540, 0.85)))
    for i in range(44):
        rnd = _rng(i + 30)
        gx = rnd() * W
        gh = 30 + 34 * rnd()
        stroke_path(c, [(gx, 196), (gx + 10, 196 + gh * 0.6),
                        (gx + 20, 196 + gh)], color="grass_dk", lw=2.6)
    bush(c, 214, 244, 2.0)
    bush(c, 754, 250, 1.7)
    draw_puss(c, 340, BASE, 1.5, expr="sly", legs="sit", tail="swish",
              arm_r="hold", arm_l="down")
    _sack(c, 486, 252, 1.9)
    draw_rabbit(c, 664, 200, 2.5, flip=True)
    for i in range(3):
        stroke_path(c, [(566 - i * 26, 264 + i * 10),
                        (578 - i * 26, 278 + i * 10)],
                    color="#FFFFFF", lw=3.2, alpha=0.6)
    grass_tufts(c, 0, W, 190, n=22, seed=6)


def s06_before_the_king(c):
    stone_hall(c, 330)
    for bx in (130, 726):
        banner(c, bx, H - 42, 74, 186, "cape", "gold")
    rect(c, 372, 372, 108, 152, fill="#7FB6D4", r=54, stroke="stone_dk", lw=3.4)
    stroke_path(c, [(426, 372), (426, 524)], color="stone_dk", lw=2.8)
    stroke_path(c, [(372, 448), (480, 448)], color="stone_dk", lw=2.8)
    throne(c, 648, BASE, 1.35)
    draw_person(c, 648, BASE + 30, 1.5, robe="king_robe", crown=True,
                hair="hair_grey", beard=True, expr="happy", arm_r="hold",
                arm_l="down", flip=True)
    poly(c, [(104, 40), (238, BASE - 4), (566, BASE - 4), (516, 40)],
         fill="cape_dk")
    poly(c, [(126, 40), (252, BASE - 8), (552, BASE - 8), (498, 40)],
         fill="cape")
    draw_puss(c, 318, BASE, 1.42, expr="sly", arm_r="doff", arm_l="hold",
              lean=13, legs="bow", tail="curl")
    _sack(c, 392, 274, 1.25)


def s07_gifts_every_week(c):
    stone_hall(c, 326)
    banner(c, 104, H - 42, 70, 178, "#3F6FA8", "gold")
    banner(c, 762, H - 42, 70, 178, "#3F6FA8", "gold")
    throne(c, 200, BASE, 1.26)
    draw_person(c, 200, BASE + 28, 1.44, robe="king_robe", crown=True,
                hair="hair_grey", beard=True, expr="happy", arm_r="clasp",
                arm_l="down")
    gift_pile(c, 520, BASE + 10)
    draw_puss(c, 736, BASE, 1.34, expr="sly", arm_r="out", arm_l="hip",
              tail="curl", flip=True)
    bold_left(c, 262, 452, "?", 46, "#6B5A52")
    bold_left(c, 308, 490, "?", 32, "#6B5A52")


def s08_run_home(c):
    meadow(c, 312, clouds=((230, 532, 1.05), (620, 500, 0.8)))
    cottage(c, 752, 296, 1.2)
    tree(c, 76, 302, 1.2)
    wheat_field(c, 0, 196, W, 96, seed=8, n=40)
    grass_tufts(c, 0, W, 268, n=18, seed=4)
    draw_puss(c, 320, BASE, 1.72, expr="surprised", arm_r="point", arm_l="up",
              legs="run", tail="swish", lean=-8)
    motion(c, 218, 268, 3, 88, 18, color="#FFFFFF", alpha=0.7)
    draw_person(c, 674, BASE, 1.46, robe="jack_old", expr="surprised",
                arm_l="up", arm_r="down", flip=True)


def s09_into_the_river(c):
    sky(c, 0, 318, W, H - 318, "#BFE1F0", "#DDF0F8")
    sun(c, 118, 528, 42)
    cloud(c, 330, 540, 0.95)
    cloud(c, 706, 506, 0.8)
    hills(c, -20, 282, W + 40, 66, "#A9CE8E", bumps=4, seedoff=1.2)
    ground(c, 0, 0, W, 322, "grass", "grass_lt")
    river(c, 0, 176, W, 148)
    grass_tufts(c, 0, W, 300, n=20, seed=11)
    # Jack, up to his shoulders, well clear of the text panel
    circle(c, 470, 290, 21, fill="skin", stroke=LINE, lw=2.0)
    _ol(c, [(470, 314), (491, 302), (494, 288), (480, 296), (470, 299),
            (460, 296), (446, 288), (449, 302)], "hair_brown", tension=0.75)
    for dx in (-7.5, 7.5):
        circle(c, 470 + dx, 293, 2.8, fill="ink")
    ellipse(c, 470, 281, 4.0, 5.0, fill="#8E3B3F")
    for sx, ax in ((-1, 424), (1, 516)):
        taper(c, [(470 + sx * 16, 276), (ax, 292), (ax + sx * 16, 326)],
              8.0, 6.0, fill="skin", stroke=LINE, lw=1.7)
        circle(c, ax + sx * 16, 326, 7.0, fill="skin", stroke=LINE, lw=1.5)
    for i, (sx, sr) in enumerate(((-1, 62), (1, 70))):
        ellipse(c, 470 + sx * sr, 270, 34 - i * 4, 10, fill="#FFFFFF", alpha=0.65)
    # the stone, with the old clothes tucked underneath
    _ol(c, [(146, 246), (192, 272), (244, 262), (254, 234), (202, 222),
            (150, 226)], "stone_dk", tension=0.8)
    _ol(c, [(228, 240), (282, 248), (302, 232), (264, 222), (228, 228)],
        "jack_old", tension=0.8)
    draw_puss(c, 712, 244, 1.66, expr="surprised", arm_r="up", arm_l="up",
              tail="up", legs="stride", flip=True)
    for i in range(3):
        stroke_path(c, [(636 - i * 20, 424 + i * 14),
                        (606 - i * 20, 436 + i * 14)],
                    color="#FFFFFF", lw=3.6, alpha=0.6)
    coach(c, 128, 338, 0.5)


def s10_pulled_out(c):
    sky(c, 0, 320, W, H - 320, "#BFE1F0", "#E4F2F9")
    cloud(c, 190, 534, 0.9)
    cloud(c, 636, 552, 1.0)
    sun(c, 774, 496, 40)
    hills(c, -20, 286, W + 40, 60, "#A9CE8E", bumps=4, seedoff=0.9)
    ground(c, 0, 0, W, 324, "grass", "grass_lt")
    river(c, 0, 188, W * 0.28, 122, sparkles=False)
    grass_tufts(c, W * 0.30, W, 288, n=16, seed=13)
    coach(c, 736, 268, 0.8)
    draw_person(c, 150, BASE, 1.5, robe="jack_new", hair="hair_brown",
                expr="surprised", arm_l="out", arm_r="up", wet=True)
    draw_person(c, 386, BASE, 1.56, robe="king_robe", crown=True,
                hair="hair_grey", beard=True, expr="happy", arm_r="point")
    draw_person(c, 566, BASE, 1.44, robe="princess", hair="hair_gold",
                long_hair=True, hat="tiara", expr="happy", arm_r="clasp")
    draw_puss(c, 268, BASE, 1.2, expr="sly", arm_r="point", arm_l="hip",
              tail="curl")


def s11_the_golden_coach(c):
    meadow(c, 322, sky_top="#C6E6F4", clouds=((190, 534, 1.05), (712, 512, 0.85)))
    hills(c, -20, 280, W + 40, 56, "grass_dk", bumps=3, seedoff=3.0)
    road(c, 300)
    tree(c, 62, 296, 1.2)
    tree(c, 792, 300, 1.05)
    grass_tufts(c, 0, W, 262, n=14, seed=17)
    coach(c, 168, 178, 1.15, passengers=True)
    horse(c, 408, 190, 1.12)
    draw_puss(c, 690, 196, 1.5, expr="proud", arm_r="point", arm_l="out",
              legs="run", tail="swish", lean=-6)
    motion(c, 606, 252, 3, 74, 17, color="#FFFFFF", alpha=0.6)


def s12_the_haymakers(c):
    meadow(c, 330, sky_top="#F3DFAE", sky_bot="#FBEFD2", sunpos=(140, 526),
           clouds=((520, 536, 0.95),))
    hills(c, -20, 292, W + 40, 52, "#C7B771", bumps=4, seedoff=1.5)
    wheat_field(c, 0, 0, W, 292, seed=2, n=72)
    _ol(c, [(178, 214), (238, 242), (288, 224), (280, 190), (220, 180),
            (176, 190)], "stone_dk", tension=0.8)
    draw_puss(c, 232, 228, 1.48, expr="proud", arm_r="point", arm_l="hip",
              tail="up", legs="stand")
    for i, (px, ps, fl) in enumerate(((520, 1.36, False), (650, 1.44, True),
                                      (772, 1.30, False))):
        draw_person(c, px, 202, ps,
                    robe=("#C9A874", "#A8B98A", "#C08C6A")[i],
                    hat="straw", hair="#6B4A2E", expr="happy",
                    arm_r="reach" if not fl else "hold", flip=fl)
    for sx in (566, 706):
        stroke_path(c, [(sx, 214), (sx + 38, 264), (sx + 72, 276)],
                    color="wood_dk", lw=4.6)
        stroke_path(c, [(sx + 72, 276), (sx + 104, 254)], color="#B9BEC4",
                    lw=5.0)


def s13_the_ogres_castle(c):
    sky(c, 0, 300, W, H - 300, "#9FB6D4", "#CBDCEB")
    for cx, cy, s in ((176, 536, 1.15), (676, 500, 0.95)):
        cloud(c, cx, cy, s, fill="#E8EEF5")
    for bx, by in ((292, 544), (344, 564)):
        bird(c, bx, by, 1.4, color="#5E5A6B")
    hills(c, -20, 266, W + 40, 66, "#7E9A78", bumps=3, seedoff=2.0)
    ground(c, 0, 0, W, 302, "#89A874", "#9CBB84")
    castle(c, 612, 290, 1.05, wall="#B7AFA2", roof="#5B4A66",
           flag="#6B4A7A", windows="#3E4C63")
    grass_tufts(c, 0, W, 276, n=18, seed=19, color="#6B8A5E")
    tree(c, 80, 274, 1.25, leaf="#5E7A52", leaf2="#6E8B5F")
    draw_ogre(c, 456, BASE, 2.35, expr="grin", arm_l="down", arm_r="hip",
              flip=True)
    draw_puss(c, 194, BASE, 1.28, expr="sly", arm_r="doff", arm_l="hip",
              lean=8, legs="bow", tail="curl")


def s14_the_lion(c):
    interior(c, wall="#D8C6A8", floor="#9C7449", horizon=314)
    rect(c, 84, 368, 122, 156, fill="#5E7A98", r=60, stroke="wood_dk", lw=4.4)
    stroke_path(c, [(145, 368), (145, 524)], color="wood_dk", lw=3.2)
    cupboard(c, 722, 196, 1.02)
    draw_lion(c, 372, 196, 1.95)
    draw_puss(c, 722, 410, 1.0, expr="surprised", arm_r="hug", arm_l="hug",
              tail="up", legs="sit", flip=True)
    for i in range(4):
        stroke_path(c, [(536 + i * 24, 400 + i * 18),
                        (580 + i * 24, 390 + i * 18)],
                    color="#C0392B", lw=3.6, alpha=0.5)


def s15_the_mouse(c):
    """POOF -- and the great Ogre is a very small mouse."""
    interior(c, wall="#DDCBAD", floor="#A87E50", horizon=314)
    cupboard(c, 104, 214, 1.02)
    for dx, dy, rr, al in ((0, 74, 76, 0.85), (-64, 118, 54, 0.7),
                           (66, 128, 50, 0.7), (-20, 182, 40, 0.5),
                           (42, 192, 32, 0.45)):
        circle(c, 548 + dx, 232 + dy, rr, fill="#EFE6D8", alpha=al)
    for i in range(6):
        a = i * math.pi / 3
        sparkle(c, 548 + 118 * math.cos(a), 316 + 94 * math.sin(a), 11,
                color="#F6E3B0", alpha=0.85)
    draw_mouse(c, 548, BASE, 2.2)
    draw_puss(c, 268, BASE, 1.62, expr="sly", arm_r="hip", arm_l="chin",
              legs="stand", tail="perk")
    bold_left(c, 640, 452, TXT.POOF, 34, "#9C8B76")


def s16_out_the_door(c):
    """Down the steps and away over the hill."""
    interior(c, wall="#DDCBAD", floor="#A87E50", horizon=314)
    cupboard(c, 92, 210, 0.98)
    rect(c, 612, 314, 196, 262, fill="#8A6743", stroke=LINE, lw=2.6)
    rect(c, 632, 314, 156, 236, fill="#BFE1F0", stroke=LINE, lw=1.8)
    hills(c, 632, 314, 156, 54, "#A9CE8E", bumps=2, seedoff=1.0)
    poly(c, [(632, 314), (788, 314), (838, 118), (588, 118)], fill="#FBEFCF",
         alpha=0.55)
    draw_puss(c, 372, BASE, 1.68, expr="scheme", arm_r="out", arm_l="up",
              legs="run", tail="swish", lean=-12)
    draw_mouse(c, 604, BASE + 6, 1.9, flip=True)
    for i in range(3):
        stroke_path(c, [(536 + i * 22, 218 + i * 12),
                        (502 + i * 22, 210 + i * 12)],
                    color="#9C8B76", lw=2.8, alpha=0.55)
    motion(c, 282, 300, 3, 72, 18, color="#FFFFFF", alpha=0.5)


def s17_welcome(c):
    meadow(c, 326, sky_top="#F5D6A0", sky_bot="#FDEFD6", sunpos=(112, 524),
           clouds=((420, 546, 0.85), (712, 508, 0.95)))
    hills(c, -20, 288, W + 40, 56, "grass_dk", bumps=3, seedoff=1.1)
    castle(c, 566, 306, 1.02, wall="#DED5C6", roof="#B0566B", flag="#C86B7E")
    road(c, 306)
    grass_tufts(c, 0, W, 268, n=14, seed=23)
    coach(c, 96, 176, 1.05, passengers=True)
    horse(c, 286, 188, 1.02)
    draw_puss(c, 452, 194, 1.56, expr="proud", arm_r="doff", arm_l="out",
              lean=10, legs="bow", tail="curl")
    for bx, by in ((648, 498), (700, 526), (604, 476)):
        bird(c, bx, by, 1.3, color="#A88A6E")
    sparkles_around(c, 452, 300, 158, 6, seed=31)


def s18_happily_ever_after(c):
    interior(c, wall="#E4D2B4", floor="#A87E50", horizon=316, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    fireplace(c, 138, 316, 1.10)
    for bx in (626, 792):
        banner(c, bx, H - 58, 66, 152, "cape", "gold")
    for i in range(11):
        x0 = 300 + i * 42
        poly(c, [(x0, 500 - abs(i - 5) * 3), (x0 + 34, 500 - abs(i - 5.6) * 3),
                 (x0 + 17, 470 - abs(i - 5) * 3)],
             fill=("#C0392B", "#F6C453", "#5E9BC4")[i % 3], stroke=LINE, lw=1.2)
    stroke_path(c, [(296, 504), (508, 482), (720, 504)], color="wood_dk", lw=2.2)
    cushion(c, 352, 178, 1.3)
    draw_puss(c, 352, 202, 1.14, expr="closed", arm_r="hug", arm_l="hug",
              legs="sit", tail="curl")
    draw_person(c, 542, BASE, 1.56, robe="jack_new", hair="hair_brown",
                expr="happy", arm_r="reach", arm_l="down")
    draw_person(c, 690, BASE, 1.54, robe="princess", hair="hair_gold",
                long_hair=True, hat="tiara", expr="happy", arm_l="reach",
                arm_r="down", flip=True)
    for hx, hy, hs in ((616, 462, 1.5), (572, 496, 1.0), (662, 494, 0.9)):
        c.saveState()
        c.translate(hx, hy)
        c.scale(hs, hs)
        blob(c, [(0, -10), (12, 4), (7, 14), (0, 8), (-7, 14), (-12, 4)],
             fill="#E4708A", stroke=LINE, lw=1.2, tension=0.8)
        c.restoreState()


def the_end(c):
    interior(c, wall="#E0CDAE", floor="#A87E50", horizon=310, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    fireplace(c, 676, 310, 1.12)
    c.saveState()
    c.translate(320, 118)
    shadow(c, 0, -6, 168, 24, alpha=0.14)
    _ol(c, [(-124, 0), (-132, 152), (-102, 214), (102, 214), (132, 152),
            (124, 0)], "cape_dk")
    _ol(c, [(-102, 30), (-106, 162), (0, 182), (106, 162), (102, 30)], "cape")
    _ol(c, [(-124, 20), (-136, 98), (-102, 110), (-89, 30)], "cape_dk")
    _ol(c, [(124, 20), (136, 98), (102, 110), (89, 30)], "cape_dk")
    rect(c, -115, 0, 36, 26, fill="wood_dk", r=6, stroke=LINE, lw=1.5)
    rect(c, 79, 0, 36, 26, fill="wood_dk", r=6, stroke=LINE, lw=1.5)
    c.restoreState()
    draw_puss(c, 320, 196, 1.38, expr="sleep", arm_r="hug", arm_l="hug",
              legs="sit", tail="curl", hat=False, shad=False)
    c.saveState()
    c.translate(320, 322)
    c.scale(1.38, 1.38)
    c.rotate(-13)
    _cat_hat(c)
    c.restoreState()
    for zx, zy, zs in ((470, 402, 24), (506, 444, 31), (548, 494, 39)):
        bold_left(c, zx, zy, "z", zs, "#8A7A66")

    c.saveState()
    c.setFillColorRGB(0, 0, 0, 0.10)
    c.roundRect(W / 2 - 155, 56, 320, 76, 22, stroke=0, fill=1)
    c.restoreState()
    rect(c, W / 2 - 158, 60, 320, 76, fill="cream", r=22, stroke="#D9BE8A",
         lw=2.2)
    bold_centred(c, W / 2 + 2, 88, TXT.THE_END, 34, "#7A3B2E")


def back_cover(c):
    sky(c, 0, 0, W, H, "#F7C98B", "#FDE9C4")
    for cx, cy, s in ((180, 486, 1.05), (664, 516, 0.85)):
        cloud(c, cx, cy, s, fill="#FFF6E4")
    hills(c, -20, 168, W + 40, 78, "#B9D69A", bumps=4, seedoff=0.3)
    hills(c, -20, 142, W + 40, 62, "grass_dk", bumps=3, seedoff=2.4)
    ground(c, 0, 0, W, 190, "grass", "grass_lt")
    grass_tufts(c, 0, W, 166, n=24, seed=27)
    tree(c, 104, 152, 1.25)
    tree(c, 748, 158, 1.05)
    draw_puss(c, 420, 156, 1.86, expr="wink", arm_r="doff", arm_l="hip",
              tail="curl", legs="stand")
    for i, ln in enumerate(TXT.BACK_QUOTE):
        bold_centred(c, W / 2, 534 - i * 30, ln, 22, "#7A3B2E")
    for sx in (-1, 1):
        star(c, W / 2 + sx * 300, 520, 10, fill="gold")

SCENES = [
    s01_three_sons, s02_a_talking_cat, s03_the_boots, s04_feather_in_his_hat,
    s05_the_rabbit, s06_before_the_king, s07_gifts_every_week, s08_run_home,
    s09_into_the_river, s10_pulled_out, s11_the_golden_coach, s12_the_haymakers,
    s13_the_ogres_castle, s14_the_lion, s15_the_mouse, s16_out_the_door,
    s17_welcome, s18_happily_ever_after,
]


# ------------------------------------------------------------------ build ---

def build(lang="en", path=None):
    cfg = set_lang(lang)
    path = path or os.path.join(HERE, cfg["out"])
    c = Canvas(path, pagesize=(W, H))
    c.setTitle(TXT.TITLE)
    c.setAuthor("retold after Charles Perrault")
    c.setSubject("A printable picture book")

    cover(c)
    c.showPage()
    nameplate(c)
    c.showPage()

    assert len(SCENES) == len(TXT.PAGES), (
        f"{len(SCENES)} scenes vs {len(TXT.PAGES)} texts")

    for i, text in enumerate(TXT.PAGES):
        SCENES[i](c)
        text_panel(c, text)
        folio(c, i + 1)
        c.showPage()

    the_end(c)
    c.showPage()
    back_cover(c)
    c.showPage()

    c.save()
    return path


if __name__ == "__main__":
    import sys
    langs = sys.argv[1:] or ["en", "zh"]
    for lg in langs:
        print("wrote", build(lg))
