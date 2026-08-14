"""Beauty and the Beast -- after Madame de Villeneuve / Madame Leprince de Beaumont."""

import math

from art import *          # noqa: F401,F403
from art import _rng, _ol, LINE, LW, P
from scenery import *      # noqa: F401,F403
import layout
from layout import W, H, BASE

SLUG = "beauty-and-the-beast"
ACCENT = "#7A2F4E"

BACK_ACCENT = "#F6E3B0"

TEXT = {
    "en": {
        "TITLE": "Beauty and the Beast",
        "SUBTITLE": "an old fairy tale, told again",
        "BYLINE": "after Madame Leprince de Beaumont",
        "BELONGS_TO": "This book belongs to",
        "THE_END": "The End",
        "COLOPHON": (
            "A retelling of “La Belle et la Bête”, published by "
            "Madame Leprince de Beaumont in 1756.\n"
            "Illustrations drawn as vector art. Made to be read aloud."),
        "BACK_QUOTE": ["“I am not handsome,” said the Beast,",
                       "“but I do have a very good heart.”"],
        "PAGES": [
            # 1
            "A merchant had three daughters. The two eldest liked ribbons "
            "and mirrors and being agreed with.\n"
            "The youngest liked books, and roses, and being out of doors — "
            "and everybody called her Beauty.",
            # 2
            "One winter the merchant's ships were lost at sea, and the "
            "family had to move to a small cold house at the edge of a "
            "wood.",
            # 3
            "When at last he had to travel again, he asked what he should "
            "bring back.\n"
            "“A silk gown,” said the first. “A pearl comb,” said the "
            "second.\n"
            "“One rose,” said Beauty. “I should like a rose.”",
            # 4
            "He found no fortune, and coming home in the snow he lost the "
            "road altogether.\n"
            "Between the trees stood a castle with every window lit. The "
            "doors opened by themselves. Supper was already laid.",
            # 5
            "In the morning he saw roses growing in the snow, and "
            "remembered his promise, and picked one.\n"
            "A voice like thunder came out of the garden. “I gave you "
            "everything,” said the Beast, “and you take my rose?”",
            # 6
            "The merchant told him about Beauty, and about the promise.\n"
            "The Beast was quiet for a long time. “Go home,” he said at "
            "last. “But someone must come back in your place.”",
            # 7
            "So Beauty came herself.\n"
            "She was frightened of him — anybody would have been — but she "
            "curtseyed all the same, and the Beast bowed, which he had not "
            "done for a hundred years.",
            # 8
            "Every evening he asked her the same question: “Beauty, will "
            "you marry me?”\n"
            "And every evening she said, as kindly as she could, “No.” "
            "And he said, “Then goodnight,” and went away.",
            # 9
            "But the days were not unhappy. They walked in the garden. He "
            "showed her a library with every book anybody had ever "
            "written, and he listened when she read the good bits out "
            "loud.",
            # 10
            "One day, in a mirror, she saw her father lying ill.\n"
            "“Go to him,” said the Beast. “Take this ring. Turn it when "
            "you wish to come back — only come back, or I shall die of "
            "it.”",
            # 11
            "At home everybody was so glad to see her that a week went by, "
            "and then another, and Beauty kept meaning to go and not "
            "going.",
            # 12
            "Then one night she dreamt of the Beast lying still in his own "
            "garden, under the rose tree.\n"
            "She woke, and turned the ring.",
            # 13
            "She found him exactly as she had dreamt, and knelt down in "
            "the wet grass and put her hand on his great head.\n"
            "“Don't die,” she said. “I never knew until now — I love you.”",
            # 14
            "The garden filled with light.\n"
            "And where the Beast had been there was a prince, blinking, "
            "who said: “That is the kindest thing anyone has said to me "
            "in a hundred years.”",
        ],
    },
}


# ----------------------------------------------------------- cast helpers ---

def belle(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#E4B4C6")
    kw.setdefault("hair", "#7A4B2A")
    kw.setdefault("long_hair", True)
    return draw_person(c, x, y, s, **kw)


def merchant(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#5E6B8A")
    kw.setdefault("hair", "hair_grey")
    kw.setdefault("beard", True)
    return draw_person(c, x, y, s, **kw)


def sister(c, x, y, s=1.0, tone=0, **kw):
    kw.setdefault("robe", ("#C6A0D4", "#9CBBD6")[tone])
    kw.setdefault("hair", ("#4E3A2A", "#C9A05E")[tone])
    kw.setdefault("long_hair", True)
    return draw_person(c, x, y, s, **kw)


def snowfield(c, horizon=316, sky_top="#B9C6DC", sky_bot="#E4EAF2",
              snow="#F4F6FA", flakes=60, seed=5):
    sky(c, 0, horizon - 20, W, H - horizon + 20, sky_top, sky_bot)
    hills(c, -20, horizon - 46, W + 40, 58, "#DCE4EE", bumps=4, seedoff=1.1)
    ground(c, 0, 0, W, horizon - 16, snow, "#FFFFFF")
    rnd = _rng(seed)
    for _ in range(flakes):
        circle(c, rnd() * W, rnd() * H, 1.6 + 2.6 * rnd(), fill="#FFFFFF",
               alpha=0.5 + 0.4 * rnd())


def bare_tree(c, x, y, s=1.0, bark="#5E4A3C", snow=True):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    taper(c, [(0, 0), (-3, 40), (2, 80)], 9, 5, fill=bark, stroke=LINE, lw=1.4)
    for bx, by, ang in ((0, 54, 42), (0, 62, -38), (0, 74, 22), (0, 78, -20)):
        c.saveState()
        c.translate(bx, by)
        c.rotate(ang)
        taper(c, [(0, 0), (10, 22), (16, 44)], 4.5, 2.0, fill=bark,
              stroke=LINE, lw=1.2)
        c.restoreState()
    if snow:
        for sx, sy in ((-14, 92), (12, 96), (0, 104)):
            ellipse(c, sx, sy, 12, 5, fill="#FFFFFF", alpha=0.85)
    c.restoreState()


def rose_tree(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    taper(c, [(0, 0), (-4, 36), (2, 66)], 10, 6, fill="#5E4A3C", stroke=LINE,
          lw=1.4)
    for dx, dy, rr in ((-24, 82, 26), (22, 76, 22), (0, 100, 28)):
        ellipse(c, dx, dy, rr, rr * 0.88, fill="#4E7A52", stroke=LINE, lw=1.2)
    rnd = _rng(3)
    for _ in range(11):
        rx = -44 + 88 * rnd()
        ry = 60 + 62 * rnd()
        for i in range(5):
            a = i * 2 * math.pi / 5
            circle(c, rx + 4.4 * math.cos(a), ry + 4.4 * math.sin(a), 3.6,
                   fill="rose")
        circle(c, rx, ry, 2.8, fill="#B33049")
    c.restoreState()


def enchanted_hall(c, horizon=326, wall="#5E4A6B", floor="#4A3A55"):
    rect(c, 0, horizon - 10, W, H - horizon + 10, fill=wall)
    for i in range(6):
        rect(c, 40 + i * 132, horizon + 20, 78, 168, fill=shade(wall, 1.18),
             r=39, stroke=shade(wall, 0.8), lw=2.0)
        rect(c, 52 + i * 132, horizon + 34, 54, 140, fill="#2E2440", r=27)
        for k in range(3):
            circle(c, 79 + i * 132, horizon + 60 + k * 40, 5, fill="#F6C453",
                   alpha=0.8)
    rect(c, 0, 0, W, horizon, fill=floor)
    for i in range(-1, 15):
        rect(c, i * 66 - 20, 0, 62, horizon - 6, fill=shade(floor, 1.08),
             stroke=shade(floor, 0.86), lw=1.1)
    rect(c, 0, horizon - 16, W, 16, fill=shade(floor, 0.78))


def candelabra(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    _ol(c, [(-16, 0), (-18, 8), (18, 8), (16, 0)], "gold_dk", tension=0.5)
    taper(c, [(0, 6), (0, 44)], 4.5, 3.5, fill="gold")
    for dx in (-22, 0, 22):
        if dx:
            stroke_path(c, [(0, 40), (dx * 0.7, 48), (dx, 54)], color="gold",
                        lw=3.0)
        rect(c, dx - 3.5, 52 + (0 if dx else 8), 7, 20, fill="#F2EAD6", r=2,
             stroke=LINE, lw=1.0)
        fy = 72 + (0 if dx else 8)
        blob(c, [(dx, fy + 16), (dx + 5, fy + 4), (dx + 3, fy),
                 (dx - 3, fy), (dx - 5, fy + 4)], fill="#F6C453", tension=0.8)
        circle(c, dx, fy + 8, 9, fill="#F6C453", alpha=0.22)
    c.restoreState()


# ----------------------------------------------------------------- scenes ---

def COVER_ART(c):
    sky(c, 0, 240, W, H - 240, "#4E3A66", "#8A6E9E")
    for i in range(40):
        rnd = _rng(i + 4)
        sparkle(c, rnd() * W, 250 + rnd() * 340, 2 + 4 * rnd(),
                color="#FFF6DA", alpha=0.7)
    hills(c, -20, 214, W + 40, 62, "#3F3356", bumps=4, seedoff=1.0)
    castle(c, 700, 232, 0.6, wall="#6E5C82", roof="#3E3252", flag="#B5748A",
           windows="#F6C453")
    ground(c, 0, 0, W, 246, "#4A5C46", "#5A6E52")
    grass_tufts(c, 0, W, 224, n=20, seed=9, color="#3E5040")
    rose_tree(c, 128, 218, 1.25)
    draw_beast(c, 486, BASE - 26, 1.62, expr="kind", arm_l="down",
               arm_r="offer", flip=True)
    belle(c, 306, BASE - 26, 1.72, arm_r="reach", expr="happy")
    rose_bell(c, 712, 214, 0.9)
    for i in range(7):
        sparkle(c, 380 + i * 18, 300 + (i % 3) * 26, 6, color="#F6C453")


def NAMEPLATE_ART(c):
    c.saveState()
    c.translate(W / 2, 196)
    shadow(c, 0, 4, 130, 20, alpha=0.10)
    rose_bell(c, -80, 10, 1.25)
    mirror(c, 96, 14, 1.15)
    c.restoreState()


def s01_three_daughters(c):
    meadow(c, 320, sky_top="#D2E4F2", clouds=((640, 520, 0.9),))
    cottage(c, 726, 300, 1.35, wall="#E4D8C2", roof="#8A6B7A")
    tree(c, 68, 304, 1.2)
    grass_tufts(c, 0, W, 288, n=18, seed=5)
    for fx in (250, 320, 560):
        flower(c, fx, 268, 1.2, petal="#F0A8BC")
    sister(c, 262, BASE, 1.5, tone=0, arm_r="hip", hat="tiara")
    sister(c, 390, BASE, 1.48, tone=1, arm_r="hip")
    belle(c, 546, BASE, 1.5, arm_r="hold", expr="happy")
    rose_tree(c, 132, 214, 0.85)


def s02_the_small_house(c):
    snowfield(c, 316, flakes=52)
    bare_tree(c, 92, 296, 1.3)
    bare_tree(c, 774, 300, 1.15)
    cottage(c, 300, 292, 1.2, wall="#DCD2C2", roof="#7A6A72")
    ellipse(c, 300, 396, 78, 16, fill="#FFFFFF")
    merchant(c, 528, BASE, 1.52, expr="sad", arm_r="down", cloak="#4A5470")
    belle(c, 640, BASE, 1.48, arm_l="reach", expr="happy")
    for i in range(4):
        stroke_path(c, [(322, 424 + i * 12), (330, 452 + i * 12)],
                    color="#D8D2C8", lw=3.0, alpha=0.6)


def s03_one_rose(c):
    interior(c, wall="#D6C6B0", floor="#8A6743", horizon=318, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    hearth_glow(c, 132, 400, 170)
    fireplace(c, 132, 318, 0.95)
    merchant(c, 340, BASE, 1.56, arm_r="reach", cloak="#4A5470")
    sister(c, 546, BASE, 1.44, tone=0, arm_r="point")
    sister(c, 650, BASE, 1.42, tone=1, arm_r="up")
    belle(c, 762, BASE, 1.46, arm_l="reach", expr="happy", flip=True)
    for i in range(5):
        a = i * 2 * math.pi / 5
        circle(c, 432 + 8 * math.cos(a), 322 + 8 * math.sin(a), 7,
               fill="rose", stroke=LINE, lw=1.1)
    circle(c, 432, 322, 5.5, fill="#B33049")
    taper(c, [(432, 316), (436, 296), (430, 280)], 3.0, 2.2, fill="vine_dk")


def s04_the_lighted_castle(c):
    snowfield(c, 322, sky_top="#3E4A6B", sky_bot="#7E88A8", snow="#E8EEF6",
              flakes=70, seed=11)
    night_sky(c, 322, "#2E3A5E", "#5E6B90", moon_at=(140, 508), stars=30,
              seed=12) if False else None
    for i in range(26):
        rnd = _rng(i + 21)
        sparkle(c, rnd() * W, 340 + rnd() * 240, 2 + 3 * rnd(),
                color="#FFF6DA", alpha=0.55)
    bare_tree(c, 90, 300, 1.35, snow=True)
    bare_tree(c, 210, 296, 1.05)
    bare_tree(c, 800, 302, 1.2)
    castle(c, 560, 300, 1.0, wall="#6E5C82", roof="#3E3252", flag="#B5748A",
           windows="#F6C453")
    for wx in (488, 514, 606, 632):
        circle(c, wx, 356, 16, fill="#F6C453", alpha=0.18)
    merchant(c, 236, BASE, 1.54, expr="surprised", arm_l="up",
             cloak="#4A5470")


def s05_the_rose_and_the_beast(c):
    snowfield(c, 320, sky_top="#4E5A7E", sky_bot="#8E98B4", snow="#E8EEF6",
              flakes=44, seed=13)
    castle(c, 130, 300, 0.6, wall="#6E5C82", roof="#3E3252", flag="#B5748A",
           windows="#F6C453")
    rose_tree(c, 254, 214, 1.25)
    draw_beast(c, 630, BASE - 14, 1.9, expr="roar", arm_l="up", arm_r="out",
               flip=True)
    merchant(c, 404, BASE - 14, 1.5, expr="surprised", arm_r="up",
             cloak="#4A5470")
    for i in range(5):
        stroke_path(c, [(500 - i * 12, 380 + i * 18), (462 - i * 12,
                                                       390 + i * 18)],
                    color="#FFFFFF", lw=3.4, alpha=0.5)


def s06_someone_must_come(c):
    snowfield(c, 318, sky_top="#5E6B8E", sky_bot="#A2AAC2", snow="#EDF1F7",
              flakes=38, seed=17)
    bare_tree(c, 786, 298, 1.2)
    castle(c, 640, 298, 0.72, wall="#6E5C82", roof="#3E3252", flag="#B5748A",
           windows="#F6C453")
    rose_tree(c, 786, 212, 0.7)
    draw_beast(c, 386, BASE - 12, 1.86, expr="sad", arm_l="down",
               arm_r="offer", flip=True)
    merchant(c, 168, BASE - 12, 1.5, expr="sad", arm_r="clasp",
             cloak="#4A5470")
    horse(c, 258, BASE - 12, 0.8, body="#8A7A6E", mane="#5B4A3F")


def s07_beauty_comes(c):
    enchanted_hall(c, 326)
    candelabra(c, 108, 200, 1.3)
    candelabra(c, 748, 200, 1.3)
    poly(c, [(150, 40), (280, BASE - 4), (600, BASE - 4), (540, 40)],
         fill="#7A2F4E")
    poly(c, [(170, 40), (292, BASE - 8), (586, BASE - 8), (524, 40)],
         fill="#9C3F62")
    belle(c, 322, BASE, 1.62, arm_r="clasp", expr="surprised")
    draw_beast(c, 566, BASE, 1.72, expr="kind", arm_l="down", arm_r="offer",
               flip=True)
    for i in range(6):
        sparkle(c, 430 + i * 16, 300 + (i % 3) * 24, 5, color="#F6C453",
                alpha=0.75)


def s08_the_same_question(c):
    enchanted_hall(c, 320, wall="#54446B", floor="#443456")
    hearth_glow(c, 690, 400, 190)
    fireplace(c, 700, 320, 1.05)
    table(c, 260, 178, 1.3, w=120)
    candelabra(c, 260, 262, 0.85)
    belle(c, 372, BASE, 1.6, arm_r="clasp", expr="sad")
    draw_beast(c, 540, BASE, 1.7, expr="sad", arm_l="down", arm_r="down")
    rose_bell(c, 148, 262, 0.7)


def s09_the_library(c):
    interior(c, wall="#6B5546", floor="#4E3A2E", horizon=320, beams=False)
    rect(c, 0, H - 46, W, 46, fill="#3E2E24")
    # shelves of books, floor to ceiling
    for row in range(4):
        yy = 336 + row * 62
        rect(c, 40, yy, 330, 54, fill="#5B4436", stroke=LINE, lw=1.4)
        rect(c, 470, yy, 330, 54, fill="#5B4436", stroke=LINE, lw=1.4)
        rnd = _rng(row + 30)
        for side in (44, 474):
            bx = side
            while bx < side + 316:
                bw = 8 + 9 * rnd()
                bh = 34 + 14 * rnd()
                rect(c, bx, yy + 4, bw, bh,
                     fill=("#B5748A", "#7A9C86", "#C9A05E", "#6E7FA8",
                           "#A8705E")[int(rnd() * 5)], stroke=LINE, lw=0.8,
                     r=1.5)
                bx += bw + 2
    rect(c, 386, 330, 70, 260, fill="#2E4460", r=34, stroke=LINE, lw=2.4)
    circle(c, 421, 470, 30, fill="#F6E7B8", alpha=0.5)
    belle(c, 300, BASE, 1.6, arm_r="hold", expr="happy")
    draw_beast(c, 528, BASE, 1.72, expr="kind", arm_l="down", arm_r="down",
               flip=True)
    _ol(c, [(336, 274), (368, 280), (368, 258), (336, 252)], "#C9A05E",
        tension=0.4)


def s10_the_mirror(c):
    enchanted_hall(c, 322, wall="#54446B", floor="#443456")
    candelabra(c, 128, 200, 1.2)
    mirror(c, 480, 236, 2.1)
    # the father, seen in the glass
    c.saveState()
    c.translate(480, 300)
    c.scale(0.62, 0.62)
    bed(c, 0, -80, 0.62, quilt="#7A6E8F", posts=False)
    circle(c, -10, -22, 15, fill="skin", stroke=LINE, lw=1.5)
    _ol(c, [(-10, -6), (6, -14), (4, -34), (-10, -26), (-24, -34), (-26, -14)],
        "hair_grey", tension=0.8)
    c.restoreState()
    belle(c, 246, BASE, 1.6, arm_r="reach", expr="sad")
    draw_beast(c, 704, BASE, 1.7, expr="sad", arm_l="offer", arm_r="down",
               flip=True)
    for i in range(6):
        sparkle(c, 560 + i * 20, 380 + (i % 3) * 22, 6, color="#CFE7F3",
                alpha=0.7)


def s11_too_long_at_home(c):
    interior(c, wall="#D6C6B0", floor="#8A6743", horizon=316, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    hearth_glow(c, 700, 396, 170)
    fireplace(c, 706, 316, 0.92)
    table(c, 128, 176, 1.0, w=84)
    for cx in (96, 128, 160):
        circle(c, cx, 250, 11, fill="#EBDCC0", stroke=LINE, lw=1.2)
    circle(c, 128, 272, 7, fill=None, stroke="gold", lw=3.0)
    merchant(c, 302, BASE, 1.52, expr="happy", arm_r="reach")
    belle(c, 434, BASE, 1.58, arm_l="reach", expr="happy")
    sister(c, 578, BASE, 1.42, tone=0, arm_r="hip")
    sister(c, 690, BASE, 1.4, tone=1, arm_r="out", flip=True)


def s12_the_dream(c):
    night_sky(c, 240, "#22305C", "#4A5A8E", moon_at=(724, 486), stars=48)
    hills(c, -20, 216, W + 40, 56, "#2E3A56", bumps=3, seedoff=1.6)
    ground(c, 0, 0, W, 246, "#33405C", "#3E4C6B")
    bed(c, 250, BASE - 12, 1.35, quilt="#5E4A78")
    belle(c, 250, 204, 1.24, expr="surprised", arm_r="up", shad=False)
    # what she sees, floating above
    for k, al in ((1.0, 0.16), (0.7, 0.2)):
        ellipse(c, 618, 396, 150 * k, 96 * k, fill="#8A9CC4", alpha=al)
    c.saveState()
    c.translate(618, 350)
    c.scale(0.6, 0.6)
    rose_tree(c, -70, 0, 0.85)
    draw_beast(c, 40, 0, 1.1, expr="sad", arm_l="down", arm_r="down",
               shad=False)
    c.restoreState()
    for i in range(5):
        circle(c, 430 + i * 26, 330 + i * 18, 5 + i * 2, fill="#8A9CC4",
               alpha=0.35)


def s13_under_the_rose_tree(c):
    night_sky(c, 262, "#2A3A66", "#586A9C", moon_at=(132, 500), stars=40,
              seed=14)
    hills(c, -20, 232, W + 40, 56, "#2E4050", bumps=3, seedoff=2.2)
    castle(c, 726, 254, 0.66, wall="#5E4C72", roof="#362C48", flag="#8A5A72",
           windows="#F6C453")
    ground(c, 0, 0, W, 262, "#3E5648", "#4A6452")
    grass_tufts(c, 0, W, 240, n=18, seed=19, color="#35493C")
    rose_tree(c, 250, 232, 1.35)
    # the Beast, lying down
    shadow(c, 574, 214, 92, 17, alpha=0.2)
    c.saveState()
    c.translate(574, 214)
    c.rotate(-24)
    draw_beast(c, 0, 0, 1.6, expr="sad", arm_l="down", arm_r="out",
               shad=False, flip=True)
    c.restoreState()
    belle(c, 372, 216, 1.5, arm_r="reach", expr="sad", legs="stride")
    for i in range(6):
        sparkle(c, 452 + i * 16, 250 + (i % 3) * 18, 5, color="#F6C453",
                alpha=0.6)


def s14_the_prince(c):
    sky(c, 0, 262, W, H - 262, "#F0C08A", "#FDEBD2")
    sun(c, 700, 500, 46)
    for cx, cy, s in ((190, 520, 1.1), (450, 552, 0.8)):
        cloud(c, cx, cy, s, fill="#FFF6E4")
    hills(c, -20, 232, W + 40, 60, "#B9D69A", bumps=4, seedoff=0.7)
    castle(c, 706, 258, 0.7, wall="#E4DCCE", roof="#B0566B", flag="#C86B7E",
           windows="#7FB6D4")
    ground(c, 0, 0, W, 264, "grass", "grass_lt")
    grass_tufts(c, 0, W, 242, n=20, seed=23)
    rose_tree(c, 156, 232, 1.3)
    draw_person(c, 512, 224, 1.66, robe="#35558A", trim="gold",
                hair="#5E4630", hat="cap", arm_l="reach", expr="happy",
                flip=True)
    belle(c, 356, 224, 1.6, arm_r="reach", expr="happy")
    for i in range(14):
        rnd = _rng(i + 41)
        sparkle(c, 300 + rnd() * 280, 260 + rnd() * 230, 4 + 6 * rnd(),
                color="#FFF6DA", alpha=0.85)


def END_ART(c):
    sky(c, 0, 250, W, H - 250, "#F5D6A0", "#FDEFD6")
    sun(c, 140, 512, 42)
    for cx, cy, s in ((470, 536, 0.85), (730, 500, 0.95)):
        cloud(c, cx, cy, s, fill="#FFF6E4")
    hills(c, -20, 222, W + 40, 56, "#B9D69A", bumps=3, seedoff=1.3)
    castle(c, 616, 246, 0.78, wall="#E4DCCE", roof="#B0566B", flag="#C86B7E",
           windows="#7FB6D4")
    ground(c, 0, 0, W, 252, "grass", "grass_lt")
    grass_tufts(c, 0, W, 230, n=20, seed=27)
    rose_tree(c, 726, 220, 1.0)
    belle(c, 232, 220, 1.5, arm_r="reach", expr="happy")
    draw_person(c, 356, 220, 1.55, robe="#35558A", trim="gold",
                hair="#5E4630", hat="cap", arm_l="reach", expr="happy",
                flip=True)
    for fx in (96, 160, 470, 540):
        flower(c, fx, 208, 1.3, petal="#F0A8BC")


def BACK_ART(c):
    sky(c, 0, 0, W, H, "#5E4A78", "#A48EBE")
    for i in range(34):
        rnd = _rng(i + 51)
        sparkle(c, rnd() * W, 150 + rnd() * 420, 2 + 4 * rnd(),
                color="#FFF6DA", alpha=0.7)
    hills(c, -20, 150, W + 40, 64, "#463A5E", bumps=4, seedoff=0.8)
    ground(c, 0, 0, W, 176, "#4A5C46", "#57694F")
    grass_tufts(c, 0, W, 154, n=18, seed=33, color="#3E5040")
    rose_tree(c, 150, 148, 1.1)
    rose_bell(c, 690, 150, 1.15)
    draw_beast(c, 430, 148, 1.4, expr="kind", arm_l="down", arm_r="offer")


SCENES = [
    s01_three_daughters, s02_the_small_house, s03_one_rose,
    s04_the_lighted_castle, s05_the_rose_and_the_beast,
    s06_someone_must_come, s07_beauty_comes, s08_the_same_question,
    s09_the_library, s10_the_mirror, s11_too_long_at_home, s12_the_dream,
    s13_under_the_rose_tree, s14_the_prince,
]
