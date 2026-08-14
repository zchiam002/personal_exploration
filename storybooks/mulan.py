"""Hua Mulan -- after the Ballad of Mulan (《木兰辞》), c. 5th-6th century."""

import math

from art import *          # noqa: F401,F403
from art import _rng, _ol, LINE, LW, P
from scenery import *      # noqa: F401,F403
import layout
from layout import W, H, BASE

SLUG = "hua-mulan"
ACCENT = "#9B2D22"

TEXT = {
    "en": {
        "TITLE": "Hua Mulan",
        "SUBTITLE": "an old ballad, told again",
        "BYLINE": "after the Ballad of Mulan",
        "BELONGS_TO": "This book belongs to",
        "THE_END": "The End",
        "COLOPHON": (
            "A retelling of the Ballad of Mulan, written down in China "
            "around the sixth century.\n"
            "Illustrations drawn as vector art. Made to be read aloud."),
        "BACK_QUOTE": ["“Two hares run side by side —",
                       "how can you tell which is which?”"],
        "PAGES": [
            # 1
            "Click, click, click went the loom by the window.\n"
            "But this morning there was no clicking. There was only Mulan, "
            "sitting still, and sighing.",
            # 2
            "“What are you thinking of?” asked her mother.\n"
            "“Nothing,” said Mulan. “Only the notice in the square.”",
            # 3
            "The Khan was calling for soldiers. Twelve scrolls of names, "
            "and her father's name on every one.\n"
            "But her father was old, and there was no elder brother — only "
            "a little brother, still losing his teeth.",
            # 4
            "So Mulan went out and bought a horse in the east market, and "
            "a saddle in the west, and a bridle in the south, and a long "
            "whip in the north.",
            # 5
            "In the morning she tied up her hair and put on her father's "
            "armour.\n"
            "It was heavy. She stood up straight anyway.",
            # 6
            "At dawn she said goodbye to her mother and father. That night "
            "she camped by the Yellow River.\n"
            "She could not hear her mother calling her any more. She could "
            "only hear the water going by.",
            # 7
            "At dawn she left the Yellow River. That night she camped on "
            "the Black Mountain.\n"
            "She could not hear her father calling her any more. She could "
            "only hear the horses of the northern hills.",
            # 8
            "Ten thousand miles she rode to the war, over passes and "
            "mountains, flying like a bird.",
            # 9
            "The cold air carried the sound of the watchman's rattle.\n"
            "The moon came out, and shone on all the iron coats, and "
            "everybody thought of home.",
            # 10
            "For twelve years she fought. Generals fell. Soldiers came "
            "back grey.\n"
            "And in all that time not one of them guessed.",
            # 11
            "When it was over she stood in front of the Emperor himself, "
            "who offered her a great office, and a thousand pieces of "
            "gold.",
            # 12
            "“I do not want an office,” said Mulan. “Lend me a fast camel "
            "and let me go home.”",
            # 13
            "Her mother and father came out to the gate to meet her. Her "
            "sister ran to put on her best dress. Her little brother — not "
            "so little now — sharpened the knife for the sheep.",
            # 14
            "She opened the door of her old room, and sat on her old bed, "
            "and took off her armour, and put on her yellow skirt, and did "
            "her hair at the window.\n"
            "When she came out, her comrades stared. Twelve years — and "
            "they had never known she was a girl.",
        ],
    },
}


# ----------------------------------------------------------- cast helpers ---

def mulan(c, x, y, s=1.0, soldier=False, **kw):
    if soldier:
        kw.setdefault("robe", "#6B5A4A")
        kw.setdefault("armour", True)
        kw.setdefault("hat", "helmet")
    else:
        kw.setdefault("robe", "#C0392B")
        kw.setdefault("braid", True)
    kw.setdefault("hair", "#2E2620")
    kw.setdefault("skin", "#F0C9A0")
    return draw_person(c, x, y, s, **kw)


def father(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#5E6B5A")
    kw.setdefault("hair", "hair_grey")
    kw.setdefault("skin", "#EAC098")
    kw.setdefault("beard", True)
    return draw_person(c, x, y, s, **kw)


def ma(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#4E7A72")
    kw.setdefault("hair", "#3E332C")
    kw.setdefault("skin", "#F0C9A0")
    kw.setdefault("long_hair", True)
    return draw_person(c, x, y, s, **kw)


def emperor(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#C9A227")
    kw.setdefault("trim", "#8E2A20")
    kw.setdefault("hair", "hair_grey")
    kw.setdefault("skin", "#EAC098")
    kw.setdefault("beard", True)
    kw.setdefault("hat", "mianguan")
    return draw_person(c, x, y, s, **kw)


def soldier(c, x, y, s=1.0, tone=0, **kw):
    kw.setdefault("robe", ("#6B5A4A", "#5A5F52", "#6E5348")[tone])
    kw.setdefault("armour", True)
    kw.setdefault("hat", "helmet")
    kw.setdefault("hair", "#2E2620")
    kw.setdefault("skin", ("#EAC098", "#D9A87C", "#F0C9A0")[tone])
    return draw_person(c, x, y, s, **kw)


def cn_room(c, horizon=318, wall="#E4D6BC", floor="#9C7449"):
    interior(c, wall=wall, floor=floor, horizon=horizon, beams=False)
    rect(c, 0, H - 52, W, 52, fill="#8E2A20")
    for i in range(9):
        rect(c, 20 + i * 92, H - 52, 62, 52, fill="#A83B2C", r=3)
    rect(c, 0, horizon - 16, W, 16, fill=shade(floor, 0.74))


def lattice_window(c, x, y, w=130, h=160, glass="#BFDCEA"):
    rect(c, x - w / 2 - 8, y - 8, w + 16, h + 16, fill="#8A5C36", r=6,
         stroke=LINE, lw=1.6)
    rect(c, x - w / 2, y, w, h, fill=glass, r=3)
    for i in range(1, 4):
        stroke_path(c, [(x - w / 2 + i * w / 4, y),
                        (x - w / 2 + i * w / 4, y + h)],
                    color="#8A5C36", lw=3.0)
    for i in range(1, 5):
        stroke_path(c, [(x - w / 2, y + i * h / 5), (x + w / 2, y + i * h / 5)],
                    color="#8A5C36", lw=3.0)


def notice_board(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    for dx in (-52, 44):
        rect(c, dx, 0, 10, 150, fill="wood_dk", stroke=LINE, lw=1.4)
    rect(c, -62, 140, 128, 96, fill="#8A5C36", r=4, stroke=LINE, lw=1.6)
    rect(c, -52, 150, 108, 78, fill="#F2E7CE", r=2, stroke=LINE, lw=1.2)
    rnd = _rng(7)
    for i in range(6):
        rect(c, -44 + (i % 2) * 54, 210 - i * 11, 44, 5, fill="#6B5A52",
             r=1.5)
    rect(c, -44, 156, 20, 20, fill="#C0392B", r=2)
    c.restoreState()


# ----------------------------------------------------------------- scenes ---

def COVER_ART(c):
    sky(c, 0, 226, W, H - 226, "#F0C08A", "#FBE6C6")
    sun(c, 690, 500, 46)
    for cx, cy, s in ((180, 528, 1.1), (430, 552, 0.75)):
        cloud(c, cx, cy, s, fill="#FFF3E0")
    mountains(c, 236, 150, near="#8E7A72", far="#B4A296", peaks=5)
    ground(c, 0, 0, W, 240, "#A8B472", "#BCC888")
    grass_tufts(c, 0, W, 218, n=22, seed=5, color="#8A9658")
    pagoda(c, 748, 232, 0.7)
    cn_banner(c, 92, 470, 52, 190)
    horse(c, 268, BASE - 24, 1.15, body="#6E5A4E", mane="#3E332C")
    mulan(c, 500, BASE - 24, 2.0, soldier=True, arm_r="up", expr="happy")
    for i in range(9):
        sparkle(c, 560 + (i % 3) * 26, 300 + i * 22, 5, color="#F6E3B0",
                alpha=0.8)


def NAMEPLATE_ART(c):
    c.saveState()
    c.translate(W / 2, 200)
    shadow(c, 0, 4, 140, 20, alpha=0.10)
    c.saveState()
    c.translate(-118, 6)
    c.scale(1.5, 1.5)
    _ol(c, [(-17, 100), (-15, 116), (0, 124), (15, 116), (17, 100), (0, 106)],
        "steel", tension=0.85)
    _ol(c, [(-19, 102), (0, 108), (19, 102), (17, 95), (0, 100), (-17, 95)],
        "steel_dk", tension=0.7)
    stroke_path(c, [(0, 124), (0, 134)], color="steel_dk", lw=2.4)
    _ol(c, [(0, 134), (7, 144), (0, 151), (-7, 144)], "cn_red", tension=0.9)
    c.restoreState()
    loom(c, 96, -18, 0.72)
    c.restoreState()


def s01_the_loom(c):
    cn_room(c, 318)
    lattice_window(c, 700, 350, 150, 170)
    loom(c, 288, 190, 1.28)
    mulan(c, 496, BASE, 1.62, expr="sad", arm_r="clasp")
    for i, (bx, by, br) in enumerate(((588, 380, 10), (614, 410, 7),
                                      (636, 434, 5))):
        circle(c, bx, by, br, fill="#FFFFFF", alpha=0.8, stroke="#DCCFB6",
               lw=1.2)


def s02_what_are_you_thinking(c):
    cn_room(c, 318, wall="#E8DCC4")
    lattice_window(c, 128, 352, 130, 160)
    loom(c, 726, 188, 1.0)
    table(c, 400, 176, 1.1, w=88)
    for cx in (368, 400, 432):
        _ol(c, [(cx - 12, 244), (cx - 13, 262), (cx + 13, 262), (cx + 12, 244)],
            "#DCEAF0", tension=0.5)
    ma(c, 300, BASE, 1.6, arm_r="reach", expr="happy")
    mulan(c, 528, BASE, 1.6, expr="sad", arm_l="clasp", flip=True)


def s03_the_call_up(c):
    meadow(c, 316, sky_top="#E4D6B8", sky_bot="#F4EBD8", sunpos=None,
           clouds=((640, 522, 0.9),), g1="#B7B892", g2="#C8C8A4")
    pagoda(c, 128, 300, 0.86)
    cn_banner(c, 640, 520, 46, 168)
    cn_banner(c, 764, 520, 46, 168)
    grass_tufts(c, 0, W, 288, n=14, seed=9, color="#9C9E78")
    notice_board(c, 566, 198, 1.15)
    mulan(c, 350, BASE, 1.66, expr="sad", arm_r="clasp")
    father(c, 234, BASE, 1.56, expr="sad", arm_r="down")
    draw_person(c, 138, BASE, 1.0, child=True, robe="#7A9C86", hair="#2E2620",
                skin="#F0C9A0", arm_r="up", expr="happy")


def s04_the_four_markets(c):
    meadow(c, 320, sky_top="#F3DFAE", sky_bot="#FBEFD2", sunpos=(760, 520),
           clouds=((250, 532, 0.9),), g1="#B7B892", g2="#C8C8A4")
    pagoda(c, 700, 304, 0.66)
    pagoda(c, 96, 300, 0.58)
    for bx in (300, 470):
        cn_banner(c, bx, 524, 42, 150)
    grass_tufts(c, 0, W, 290, n=12, seed=11, color="#9C9E78")
    # a market stall
    rect(c, 178, 250, 190, 14, fill="wood", r=3, stroke=LINE, lw=1.4)
    for dx in (190, 344):
        rect(c, dx, 200, 10, 54, fill="wood_dk", stroke=LINE, lw=1.2)
    _ol(c, [(160, 262), (272, 288), (386, 262), (386, 250), (272, 274),
            (160, 250)], "cn_red", tension=0.6)
    for i, sx in enumerate((214, 262, 310)):
        _ol(c, [(sx - 16, 264), (sx - 18, 286), (sx + 18, 286), (sx + 16, 264)],
            ("#8A5C36", "#6E7A88", "#A8763E")[i], tension=0.5)
    horse(c, 606, BASE, 1.2, body="#6E5A4E", mane="#3E332C")
    mulan(c, 448, BASE, 1.64, arm_r="reach", expr="happy")


def s05_the_armour(c):
    cn_room(c, 316, wall="#DCCDB2")
    lattice_window(c, 132, 348, 126, 156)
    mirror(c, 700, 250, 1.5)
    table(c, 300, 176, 1.2, w=96)
    mulan(c, 452, BASE, 1.7, soldier=True, arm_r="hip", expr="brave"
          if False else "happy")
    father(c, 234, BASE, 1.5, expr="sad", arm_r="reach")
    for i in range(6):
        sparkle(c, 520 + (i % 3) * 22, 300 + i * 20, 5, color="#EFE3C4",
                alpha=0.7)


def s06_the_yellow_river(c):
    night_sky(c, 268, "#2A3560", "#5A6A96", moon_at=(148, 500), stars=44)
    mountains(c, 244, 110, near="#3A4560", far="#4E5A78", snow=False)
    ground(c, 0, 0, W, 252, "#3E4A50", "#48555C")
    river(c, 0, 168, W, 96, color="#4E6E92", color2="#39536E")
    tent(c, 654, 208, 1.15)
    campfire(c, 470, 206, 1.0)
    horse(c, 786, 202, 0.86, body="#5A4A42", mane="#2E2620", flip=True)
    mulan(c, 336, 206, 1.5, soldier=True, expr="sad", arm_r="clasp")
    for i in range(3):
        sparkle(c, 236 + i * 26, 300 + i * 18, 5, color="#CFE0F0", alpha=0.6)


def s07_the_black_mountain(c):
    night_sky(c, 300, "#222C4E", "#4A5578", moon_at=(720, 512), stars=50,
              seed=15)
    mountains(c, 250, 190, near="#2E3550", far="#3E4763", peaks=4, snow=False)
    ground(c, 0, 0, W, 258, "#333B44", "#3C444E")
    tent(c, 176, 210, 1.05)
    campfire(c, 330, 208, 0.9)
    horse(c, 560, 206, 0.94, body="#5A4A42", mane="#2E2620")
    mulan(c, 690, 206, 1.5, soldier=True, expr="sad", arm_r="clasp",
          flip=True)
    for i in range(4):
        stroke_path(c, [(430 + i * 30, 400 + (i % 2) * 20),
                        (476 + i * 30, 394 + (i % 2) * 20)],
                    color="#8A94AE", lw=2.2, alpha=0.5)


def s08_ten_thousand_miles(c):
    sky(c, 0, 270, W, H - 270, "#E8B98A", "#F8E2C4")
    sun(c, 132, 512, 44)
    mountains(c, 250, 170, near="#9C8272", far="#BCA694", peaks=6)
    ground(c, 0, 0, W, 262, "#B7A278", "#C6B48C")
    road(c, 250, color="#D9C69C")
    for bx, by in ((520, 500), (572, 528), (476, 466)):
        bird(c, bx, by, 1.4, color="#8A7A6E")
    for i, (hx, sc) in enumerate(((650, 1.05), (500, 0.9), (376, 0.78))):
        horse(c, hx, BASE - i * 14, sc, body=("#6E5A4E", "#7A6A5A",
                                              "#5A4A42")[i], mane="#2E2620",
              flip=True)
    mulan(c, 660, BASE - 4, 1.5, soldier=True, arm_r="up", expr="happy",
          flip=True)
    motion(c, 780, 250, 3, 78, 18, color="#FFFFFF", alpha=0.55)


def s09_the_moon_on_the_iron(c):
    night_sky(c, 276, "#1E2A4E", "#42506E", moon_at=(690, 500), stars=54,
              seed=19)
    mountains(c, 252, 120, near="#2A3450", far="#374260", snow=False)
    ground(c, 0, 0, W, 264, "#2E3742", "#37414D")
    for tx, ts in ((136, 1.1), (760, 0.95)):
        tent(c, tx, 214, ts)
    campfire(c, 300, 212, 0.95)
    hearth_glow(c, 300, 250, 120)
    soldier(c, 452, 214, 1.44, tone=1, expr="sad", arm_r="clasp")
    mulan(c, 570, 214, 1.46, soldier=True, expr="sad", arm_r="clasp",
          flip=True)
    for i in range(5):
        sparkle(c, 380 + i * 22, 330 + (i % 3) * 24, 4, color="#CFE0F0",
                alpha=0.5)


def s10_twelve_years(c):
    sky(c, 0, 286, W, H - 286, "#B7A8A0", "#D8CCC2")
    for cx, cy, s in ((200, 520, 1.2), (660, 486, 1.0)):
        cloud(c, cx, cy, s, fill="#C9BEB4", alpha=0.9)
    mountains(c, 262, 130, near="#7E7268", far="#9C9086", snow=False)
    ground(c, 0, 0, W, 274, "#8E8672", "#9C9480")
    for bx in (86, 756):
        cn_banner(c, bx, 520, 46, 168, color="#8E2A20")
    for i, (sx, sc, tn) in enumerate(((216, 1.34, 0), (330, 1.42, 1),
                                      (556, 1.4, 2), (684, 1.3, 0))):
        soldier(c, sx, 218, sc, tone=tn, expr="sad", arm_r="hold")
        stroke_path(c, [(sx + 22, 226), (sx + 26, 300), (sx + 24, 336)],
                    color="#7A6A5A", lw=3.4)
        poly(c, [(sx + 24, 336), (sx + 34, 356), (sx + 18, 356)],
             fill="steel", stroke=LINE, lw=1.1)
    mulan(c, 442, 218, 1.46, soldier=True, expr="sad", arm_r="hold")
    stroke_path(c, [(464, 226), (468, 300), (466, 336)], color="#7A6A5A",
                lw=3.4)
    poly(c, [(466, 336), (476, 356), (460, 356)], fill="steel", stroke=LINE,
         lw=1.1)


def s11_before_the_emperor(c):
    cn_room(c, 330, wall="#E9D3A8", floor="#8E5F3C")
    for bx in (108, 736):
        cn_banner(c, bx, H - 58, 58, 176)
    throne(c, 646, BASE, 1.3)
    emperor(c, 646, BASE + 28, 1.5, arm_r="reach", expr="happy", flip=True)
    poly(c, [(110, 40), (240, BASE - 4), (566, BASE - 4), (512, 40)],
         fill="#8E2A20")
    poly(c, [(130, 40), (254, BASE - 8), (552, BASE - 8), (496, 40)],
         fill="#C0392B")
    mulan(c, 330, BASE, 1.52, soldier=True, expr="happy", arm_r="clasp",
          legs="stride")
    for gx in (452, 512):
        gold_bag(c, gx, 210, 1.15, sack="#C9A227")


def s12_lend_me_a_camel(c):
    cn_room(c, 330, wall="#E9D3A8", floor="#8E5F3C")
    for bx in (100, 748):
        cn_banner(c, bx, H - 58, 58, 176)
    throne(c, 190, BASE, 1.22)
    emperor(c, 190, BASE + 24, 1.44, arm_r="out", expr="surprised")
    poly(c, [(280, 40), (400, BASE - 4), (700, BASE - 4), (648, 40)],
         fill="#8E2A20")
    poly(c, [(300, 40), (414, BASE - 8), (686, BASE - 8), (632, 40)],
         fill="#C0392B")
    mulan(c, 480, BASE, 1.56, soldier=True, expr="happy", arm_r="point")
    horse(c, 700, BASE, 1.05, body="#C9A87C", mane="#6B4A32", flip=True)


def s13_home_again(c):
    meadow(c, 314, sky_top="#F5D6A0", sky_bot="#FDEFD6", sunpos=(118, 520),
           clouds=((520, 536, 0.85),), g1="#A8B472", g2="#BCC888")
    pagoda(c, 690, 296, 0.92)
    for bx in (566, 812):
        cn_banner(c, bx, 500, 42, 150)
    grass_tufts(c, 0, W, 288, n=16, seed=21, color="#8A9658")
    horse(c, 180, BASE, 1.05, body="#C9A87C", mane="#6B4A32")
    mulan(c, 332, BASE, 1.56, soldier=True, arm_r="up", expr="happy")
    father(c, 486, BASE, 1.5, arm_l="reach", expr="happy", flip=True)
    ma(c, 578, BASE, 1.5, arm_l="reach", expr="happy", flip=True)
    draw_person(c, 664, BASE, 1.34, robe="#7A9C86", hair="#2E2620",
                skin="#F0C9A0", arm_l="up", expr="happy", flip=True)


def s14_the_yellow_skirt(c):
    cn_room(c, 316, wall="#E8DCC4")
    lattice_window(c, 154, 348, 130, 160)
    mirror(c, 320, 250, 1.5)
    bed(c, 660, 190, 0.9, quilt="#4E7A72", posts=False)
    # the armour, folded and set down at last
    table(c, 508, 178, 1.05, w=76)
    c.saveState()
    c.translate(508, 244)
    c.scale(1.25, 1.25)
    _ol(c, [(-24, 0), (-26, 26), (26, 26), (24, 0)], "steel", tension=0.6)
    for row in range(2):
        for i in range(4):
            rect(c, -20 + i * 10.5, 4 + row * 11, 9, 9.5,
                 fill=shade("steel", 0.92), stroke="steel_dk", lw=0.9, r=1.5)
    _ol(c, [(-26, 28), (0, 34), (26, 28), (24, 21), (0, 27), (-24, 21)],
        "cn_red", tension=0.7)
    c.saveState()
    c.translate(2, 40)
    c.scale(0.85, 0.85)
    _ol(c, [(-17, 0), (-15, 16), (0, 24), (15, 16), (17, 0), (0, 6)],
        "steel", tension=0.85)
    _ol(c, [(-19, 2), (0, 8), (19, 2), (17, -5), (0, 0), (-17, -5)],
        "steel_dk", tension=0.7)
    stroke_path(c, [(0, 24), (0, 34)], color="steel_dk", lw=2.4)
    _ol(c, [(0, 34), (7, 44), (0, 51), (-7, 44)], "cn_red", tension=0.9)
    c.restoreState()
    c.restoreState()
    mulan(c, 250, BASE, 1.62, arm_r="clasp", expr="happy")
    for i in range(7):
        sparkle(c, 356 + (i % 3) * 24, 300 + i * 20, 5, color="#F6E3B0",
                alpha=0.75)


def END_ART(c):
    meadow(c, 302, sky_top="#F5D6A0", sky_bot="#FDEFD6", sunpos=(724, 512),
           clouds=((190, 528, 0.95),), g1="#A8B472", g2="#BCC888")
    pagoda(c, 178, 288, 0.82)
    cn_banner(c, 470, 500, 44, 156)
    grass_tufts(c, 0, W, 268, n=18, seed=25, color="#8A9658")
    mulan(c, 570, 230, 1.5, arm_r="wave", expr="happy")
    ma(c, 686, 230, 1.44, arm_l="reach", expr="happy", flip=True)
    for i in range(2):
        draw_rabbit(c, 356 + i * 46, 226, 1.5, flip=bool(i))


def BACK_ART(c):
    sky(c, 0, 0, W, H, "#F0C08A", "#FBE6C6")
    for cx, cy, s in ((190, 486, 1.05), (660, 512, 0.85)):
        cloud(c, cx, cy, s, fill="#FFF3E0")
    mountains(c, 150, 120, near="#9C8272", far="#BCA694", peaks=5)
    ground(c, 0, 0, W, 168, "#A8B472", "#BCC888")
    grass_tufts(c, 0, W, 146, n=20, seed=29, color="#8A9658")
    for i in range(2):
        draw_rabbit(c, 372 + i * 60, 144, 1.9, flip=bool(i))
    pagoda(c, 764, 156, 0.6)
    cn_banner(c, 92, 420, 46, 160)


SCENES = [
    s01_the_loom, s02_what_are_you_thinking, s03_the_call_up,
    s04_the_four_markets, s05_the_armour, s06_the_yellow_river,
    s07_the_black_mountain, s08_ten_thousand_miles,
    s09_the_moon_on_the_iron, s10_twelve_years, s11_before_the_emperor,
    s12_lend_me_a_camel, s13_home_again, s14_the_yellow_skirt,
]
