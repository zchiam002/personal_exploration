"""Jack and the Beanstalk -- after the English folk tale."""

import math

from art import *          # noqa: F401,F403
from art import _rng, _ol, _sack, LINE, LW, P
from scenery import *      # noqa: F401,F403
import layout
from layout import W, H, BASE

SLUG = "jack-and-the-beanstalk"
ACCENT = "#2F6B4F"

TEXT = {
    "en": {
        "TITLE": "Jack and the Beanstalk",
        "SUBTITLE": "an old fairy tale, told again",
        "BYLINE": "after the English folk tale",
        "BELONGS_TO": "This book belongs to",
        "THE_END": "The End",
        "COLOPHON": (
            "A retelling of the English folk tale, printed in many "
            "versions since 1734.\n"
            "Illustrations drawn as vector art. Made to be read aloud."),
        "BACK_QUOTE": ["“Fee, fi, fo, fum —", "I smell the breakfast of an "
                       "Englishman!”"],
        "PAGES": [
            # 1
            "Jack lived with his mother in a small house at the edge of a "
            "field. They had no money at all, and nothing left to sell — "
            "except Milky-White, the cow.",
            # 2
            "“Take her to market,” said his mother, “and mind you get a "
            "good price.”\n"
            "So Jack took the rope, and off the two of them went down the "
            "lane.",
            # 3
            "On the road he met an old man with a hat like a chimney pot.\n"
            "“Five beans for your cow,” said the old man. “They are magic "
            "beans. Plant them tonight and see.”\n"
            "Jack thought that sounded much more interesting than money.",
            # 4
            "His mother did not think so.\n"
            "“Beans!” she cried, and threw them straight out of the "
            "window. And there was no supper for anybody.",
            # 5
            "But in the morning the garden had gone dark, and green, and "
            "very quiet.\n"
            "A beanstalk had grown in the night — up past the roof, up past "
            "the birds, up past the clouds.",
            # 6
            "So Jack climbed.\n"
            "He climbed past the swifts, and past the rain, and past the "
            "top of the sky, until the whole world below was a small green "
            "handkerchief.",
            # 7
            "At the top was a road of cloud, and at the end of it a castle "
            "with a door as tall as a tree.\n"
            "A very large woman was sweeping the step. “You poor thin "
            "thing,” she said, and gave him bread and milk.",
            # 8
            "Then the floor began to shake.\n"
            "“Fee, fi, fo, fum!” came a voice like a landslide. “Quick,” "
            "whispered the woman, “into the pot!”\n"
            "Jack got in and pulled the lid over his head.",
            # 9
            "The Giant sat down and counted his gold — one hundred, two "
            "hundred, three hundred — and his head grew heavy, and his "
            "chin came down on his chest, and he began to snore like a "
            "storm at sea.",
            # 10
            "Jack came out on tiptoe, took one bag of gold, and went down "
            "the beanstalk faster than he had ever gone down anything.\n"
            "His mother forgave him about the cow.",
            # 11
            "The gold lasted a good while. When it ran out, Jack climbed "
            "again — and this time he came home with a little brown hen "
            "who laid, whenever you asked her nicely, an egg of solid "
            "gold.",
            # 12
            "The third time, he took the golden harp.\n"
            "But the harp was an enchanted harp, and it opened one eye and "
            "sang out: “Master! Master! Somebody is stealing me!”",
            # 13
            "Down the beanstalk went Jack with the harp under his arm, and "
            "after him came the Giant, shaking every leaf.\n"
            "“Mother!” shouted Jack. “The axe! Bring the axe!”",
            # 14
            "Chop went the axe, and chop, and CHOP — and the great "
            "beanstalk came down across the field like a falling mast.\n"
            "The Giant never came down it again, and Jack and his mother "
            "were never hungry after that.",
        ],
    },
}


# ----------------------------------------------------------- cast helpers ---

def jack(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#4E7FBF")
    kw.setdefault("hair", "#C08A3E")
    return draw_person(c, x, y, s, child=True, **kw)


def mother(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#7A6E8F")
    kw.setdefault("hair", "#9C9186")
    kw.setdefault("apron", "#EFE6D4")
    return draw_person(c, x, y, s, **kw)


def giant(c, x, y, s=1.0, **kw):
    kw.setdefault("skin", "#E8B48E")
    kw.setdefault("skin_dk", "#CE9670")
    kw.setdefault("cloth", "#6B7A4A")
    kw.setdefault("cloth_dk", "#53613A")
    kw.setdefault("hair", "#8A6A4A")
    kw.setdefault("tusks", False)
    kw.setdefault("beard", True)
    return draw_ogre(c, x, y, s, **kw)


def giantess(c, x, y, s=2.3, **kw):
    kw.setdefault("robe", "#B5748A")
    kw.setdefault("hair", "#B0A498")
    kw.setdefault("apron", "#EFE6D4")
    kw.setdefault("hat", "bonnet")
    return draw_person(c, x, y, s, **kw)


# ----------------------------------------------------------------- scenes ---

def COVER_ART(c):
    sky(c, 0, 190, W, H - 190, "#BFE1F0", "#E6F3F8")
    sun(c, 130, 500, 44)
    for cx, cy, s in ((330, 520, 1.0), (620, 470, 0.85), (770, 552, 0.7)):
        cloud(c, cx, cy, s)
    hills(c, -20, 214, W + 40, 70, "#A9CE8E", bumps=4, seedoff=0.4)
    hills(c, -20, 192, W + 40, 56, "grass_dk", bumps=3, seedoff=2.2)
    ground(c, 0, 0, W, 240, "grass", "grass_lt")
    grass_tufts(c, 0, W, 214, n=24, seed=5)
    cottage(c, 742, 224, 0.9)
    beanstalk(c, 140, 30, H + 40, 19)
    jack(c, 372, BASE - 22, 2.0, arm_l="up", arm_r="up", expr="surprised",
         legs="stride")
    for fx in (96, 168, 640):
        flower(c, fx, 176, 1.3, petal="#FFFFFF")
    tree(c, 88, 190, 1.15)
    bean_pile(c, 560, 168, 1.9)


def NAMEPLATE_ART(c):
    c.saveState()
    c.translate(W / 2, 214)
    shadow(c, 0, 4, 150, 22, alpha=0.10)
    beanstalk(c, -110, 10, 210, 11)
    bean_pile(c, 60, 30, 3.0)
    hen(c, 170, 16, 1.5)
    c.restoreState()


def s01_the_cow(c):
    meadow(c, 322, clouds=((200, 520, 1.0), (660, 496, 0.8)))
    cottage(c, 138, 302, 1.25)
    tree(c, 786, 306, 1.1)
    grass_tufts(c, 0, W, 288, n=20, seed=3)
    draw_cow(c, 596, BASE, 1.35, flip=True)
    jack(c, 356, BASE, 1.85, expr="sad", arm_r="down")
    mother(c, 452, BASE, 1.5, expr="sad", arm_l="out", long_hair=True)


def s02_to_market(c):
    meadow(c, 316, sky_top="#C9E6F4", clouds=((240, 528, 1.0),))
    road(c, 296)
    tree(c, 74, 300, 1.15)
    tree(c, 792, 296, 1.0)
    bush(c, 640, 250, 1.4)
    grass_tufts(c, 0, W, 262, n=16, seed=7)
    jack(c, 300, BASE, 1.85, arm_r="reach", legs="stride")
    stroke_path(c, [(346, 288), (410, 276), (474, 268)], color="#B0987A",
                lw=2.6)
    draw_cow(c, 566, BASE, 1.4)
    mother(c, 112, BASE, 1.42, arm_r="wave", long_hair=True)


def s03_the_beans(c):
    meadow(c, 320, sky_top="#F3DFAE", sky_bot="#FBEFD2", sunpos=(140, 520),
           clouds=((540, 534, 0.85),))
    road(c, 300)
    tree(c, 806, 302, 1.05)
    bush(c, 92, 244, 1.5)
    grass_tufts(c, 0, W, 266, n=14, seed=11)
    draw_cow(c, 690, BASE, 1.28, flip=True)
    jack(c, 458, BASE, 1.85, arm_r="reach", expr="surprised")
    draw_person(c, 268, BASE, 1.68, robe="#6B5A7A", hair="hair_grey",
                beard=True, hat="miller", cloak="#4E4160", arm_r="reach",
                flip=True)
    bean_pile(c, 348, 268, 1.5)
    for i in range(5):
        sparkle(c, 330 + i * 16, 296 + (i % 2) * 14, 5, color="#F6E3B0")


def s04_out_the_window(c):
    meadow(c, 318, sky_top="#E9C9E0", sky_bot="#F7E3EE", sunpos=None,
           clouds=((680, 520, 0.9),))
    cottage(c, 258, 296, 1.55)
    grass_tufts(c, 0, W, 280, n=18, seed=13)
    bush(c, 700, 236, 1.4)
    mother(c, 336, BASE, 1.52, arm_r="up", arm_l="up", expr="surprised",
           long_hair=True)
    for i, (bx, by) in enumerate(((452, 346), (508, 330), (556, 300),
                                  (592, 260), (614, 218))):
        _ol(c, [(bx, by), (bx + 7, by + 6), (bx + 14, by), (bx + 7, by - 6)],
            "#7FA85E", tension=0.95, lw=1.2)
        stroke_path(c, [(bx - 22, by + 10), (bx - 6, by + 4)],
                    color="#FFFFFF", lw=2.2, alpha=0.5)
    jack(c, 726, BASE, 1.8, expr="sad", arm_r="down", flip=True)


def s05_the_beanstalk(c):
    sky(c, 0, 250, W, H - 250, "#F0C08A", "#FBE6C6")
    sun(c, 726, 512, 40)
    for cx, cy, s in ((160, 520, 1.1), (430, 556, 0.8)):
        cloud(c, cx, cy, s, fill="#FFF3E0")
    hills(c, -20, 226, W + 40, 60, "#B9CE93", bumps=4, seedoff=1.4)
    ground(c, 0, 0, W, 256, "#8CBE73", "#A4D18A")
    cottage(c, 720, 240, 1.15)
    grass_tufts(c, 0, W, 232, n=18, seed=17)
    beanstalk(c, 300, 40, H + 60, 22)
    jack(c, 566, BASE, 1.72, arm_l="up", expr="surprised", flip=True)
    mother(c, 664, BASE, 1.4, arm_r="up", expr="surprised", long_hair=True,
           flip=True)
    for bx, by in ((150, 470), (206, 502)):
        bird(c, bx, by, 1.3)


def s06_climbing(c):
    sky(c, 0, 0, W, H, "#9EC9E4", "#DDEEF7")
    for cx, cy, s, al in ((150, 130, 1.5, 0.9), (700, 196, 1.3, 0.85),
                          (400, 470, 1.7, 0.95), (760, 520, 1.1, 0.8),
                          (90, 400, 1.2, 0.8)):
        cloud(c, cx, cy, s, alpha=al)
    beanstalk(c, 380, -40, H + 60, 24)
    # the whole world, a long way down
    ellipse(c, 158, 224, 104, 30, fill="#8CBE73", alpha=0.5)
    for dx, dy, rw in ((-46, -4, 30), (12, 5, 36), (56, -7, 22)):
        ellipse(c, 158 + dx, 224 + dy, rw, 10, fill="#A4D18A", alpha=0.55)
    ellipse(c, 142, 220, 12, 5, fill="#C08A6A", alpha=0.6)
    jack(c, 416, 296, 1.78, arm_l="up", arm_r="up", legs="run", shad=False)
    for bx, by in ((690, 430), (742, 466), (640, 392)):
        bird(c, bx, by, 1.2)


def s07_the_castle_door(c):
    sky(c, 0, 200, W, H - 200, "#AFD3E8", "#DCEDF6")
    for cx, cy, s in ((180, 520, 1.2), (650, 486, 0.95)):
        cloud(c, cx, cy, s)
    cloud_floor(c, 250)
    castle(c, 590, 236, 1.35, wall="#CFC6B8", roof="#6B5A66", flag="#8A6A96",
           windows="#46566E")
    beanstalk(c, 92, 150, 470, 15)
    jack(c, 250, 224, 1.65, arm_l="up", expr="surprised")
    giantess(c, 424, 224, 2.5, arm_r="reach", expr="happy", flip=True)
    for i in range(5):
        sparkle(c, 700 + i * 22, 470 + (i % 2) * 26, 5, color="#FFFFFF",
                alpha=0.6)


def s08_fee_fi_fo_fum(c):
    interior(c, wall="#C9B69A", floor="#8A6743", horizon=318)
    rect(c, 76, 344, 140, 178, fill="#5E7A98", r=66, stroke="wood_dk", lw=5)
    stroke_path(c, [(146, 344), (146, 522)], color="wood_dk", lw=3.4)
    table(c, 600, 200, 1.5, w=150)
    giant(c, 470, 196, 2.5, expr="grin", arm_l="out", arm_r="up")
    # the great cooking pot, with a boy in it: he goes in first, then the pot
    shadow(c, 210, 198, 96, 17, alpha=0.15)
    jack(c, 210, 214, 1.55, expr="surprised", arm_l="hip", arm_r="hip",
         shad=False)
    c.saveState()
    c.translate(210, 196)
    _ol(c, [(-78, 6), (-88, 82), (0, 102), (88, 82), (78, 6)], "#565049",
        tension=0.85)
    _ol(c, [(-92, 88), (0, 112), (92, 88), (86, 76), (0, 98), (-86, 76)],
        "#6E6760", tension=0.7)
    c.restoreState()
    layout.bold_left(c, 96, 246, "FEE  FI  FO  FUM", 26, "#8A6A4A")


def s09_counting_gold(c):
    interior(c, wall="#C9B69A", floor="#8A6743", horizon=318)
    hearth_glow(c, 128, 400, 190)
    fireplace(c, 128, 318, 1.0)
    table(c, 540, 176, 1.6, w=170)
    for gx in (426, 520, 618):
        gold_bag(c, gx, 288, 1.15)
    giant(c, 470, 300, 2.45, expr="closed", arm_l="down", arm_r="down",
          shad=False)
    for i, (zx, zy, zs) in enumerate(((606, 486, 22), (642, 522, 29))):
        layout.bold_left(c, zx, zy, "z", zs, "#8A7A66")
    jack(c, 190, 200, 1.4, expr="surprised", arm_r="hip", legs="stride")


def s10_down_with_the_gold(c):
    sky(c, 0, 0, W, H, "#A8D0E8", "#E2F0F8")
    for cx, cy, s in ((170, 500, 1.4), (700, 430, 1.1), (420, 118, 1.2)):
        cloud(c, cx, cy, s)
    beanstalk(c, 360, -30, H + 50, 22)
    jack(c, 402, 268, 1.7, arm_l="up", arm_r="hold", legs="run", shad=False)
    _sack(c, 470, 330, 1.5, color="#E8D9B4")
    for i in range(6):
        sparkle(c, 496 + (i % 3) * 20, 250 + i * 16, 5, color="gold",
                alpha=0.85)
    ellipse(c, 690, 120, 120, 34, fill="#8CBE73", alpha=0.6)
    cottage(c, 690, 118, 0.5)


def s11_the_golden_hen(c):
    interior(c, wall="#D8C6A8", floor="#9C7449", horizon=310, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    hearth_glow(c, 700, 380, 170)
    fireplace(c, 706, 310, 0.92)
    table(c, 330, 172, 1.5, w=140)
    hen(c, 330, 268, 2.3)
    for i, ex in enumerate((196, 236)):
        _ol(c, [(ex, 180), (ex - 9, 192), (ex, 206), (ex + 9, 192)], "gold",
            tension=0.95)
        sparkle(c, ex + 12, 202, 6, color="#FFF6DA")
    jack(c, 128, BASE, 1.72, arm_r="up", expr="happy")
    mother(c, 530, BASE, 1.46, arm_l="up", expr="surprised", long_hair=True,
           flip=True)


def s12_the_harp(c):
    interior(c, wall="#C9B69A", floor="#8A6743", horizon=318)
    hearth_glow(c, 150, 400, 170)
    fireplace(c, 150, 318, 0.95)
    table(c, 560, 190, 1.45, w=150)
    harp(c, 560, 284, 1.7)
    for i in range(7):
        sparkle(c, 470 + i * 30, 340 + (i % 3) * 26, 6, color="#FFF6DA",
                alpha=0.85)
    giant(c, 786, 196, 2.4, expr="surprised", arm_l="up", arm_r="up",
          flip=True)
    jack(c, 330, BASE, 1.7, expr="surprised", arm_r="reach", legs="run")
    layout.bold_left(c, 300, 470, "Master!  Master!", 26, "#8A6A3E")


def s13_the_chase(c):
    sky(c, 0, 0, W, H, "#9EC0DC", "#DDEBF5")
    for cx, cy, s in ((130, 480, 1.3), (690, 520, 1.1)):
        cloud(c, cx, cy, s)
    cloud_floor(c, 560)
    beanstalk(c, 400, -40, H + 60, 25)
    giant(c, 470, 392, 1.9, expr="grin", arm_l="down", arm_r="down",
          shad=False)
    jack(c, 372, 176, 1.65, arm_l="up", arm_r="hold", legs="run", shad=False)
    harp(c, 452, 214, 1.0)
    for i in range(4):
        stroke_path(c, [(300 - i * 14, 250 + i * 22), (256 - i * 14,
                                                       262 + i * 22)],
                    color="#FFFFFF", lw=3.4, alpha=0.55)
    ellipse(c, 150, 96, 110, 30, fill="#8CBE73", alpha=0.6)


def s14_chop(c):
    meadow(c, 300, sky_top="#F0C08A", sky_bot="#FBE6C6", sunpos=(760, 508),
           clouds=((210, 528, 1.0),))
    cottage(c, 754, 284, 1.1)
    ground(c, 0, 0, W, 244, "grass", "grass_lt")
    grass_tufts(c, 0, W, 220, n=20, seed=23)
    # the great stalk, coming down across the field
    c.saveState()
    c.translate(196, 356)
    c.rotate(-74)
    beanstalk(c, 0, 0, 560, 21)
    c.restoreState()
    for i in range(7):
        sparkle(c, 300 + i * 34, 300 + (i % 3) * 30, 6, color="#EFE6C8",
                alpha=0.7)
    jack(c, 232, BASE, 1.82, arm_r="up", expr="happy", legs="stride")
    axe(c, 268, 300, 1.5, rot=-38)
    mother(c, 128, BASE, 1.44, arm_r="up", expr="surprised", long_hair=True)
    layout.bold_left(c, 366, 448, "CHOP!", 36, "#7A5A3E")


def END_ART(c):
    meadow(c, 300, sky_top="#F5D6A0", sky_bot="#FDEFD6", sunpos=(122, 512),
           clouds=((470, 536, 0.85), (720, 500, 0.95)))
    cottage(c, 620, 282, 1.35)
    ground(c, 0, 0, W, 250, "grass", "grass_lt")
    grass_tufts(c, 0, W, 226, n=22, seed=29)
    for fx in (86, 150, 250, 800):
        flower(c, fx, 214, 1.3, petal="#FFFFFF")
    draw_cow(c, 300, 232, 1.15, flip=True)
    hen(c, 470, 226, 1.5)
    jack(c, 132, 232, 1.6, arm_r="wave", expr="happy")
    harp(c, 760, 226, 1.05)


def BACK_ART(c):
    sky(c, 0, 0, W, H, "#BFE1F0", "#E6F3F8")
    for cx, cy, s in ((190, 470, 1.1), (664, 500, 0.9)):
        cloud(c, cx, cy, s)
    hills(c, -20, 158, W + 40, 74, "#B9D69A", bumps=4, seedoff=0.5)
    ground(c, 0, 0, W, 180, "grass", "grass_lt")
    grass_tufts(c, 0, W, 158, n=22, seed=31)
    beanstalk(c, 640, 60, 430, 15)
    tree(c, 120, 148, 1.15)
    bean_pile(c, 330, 150, 3.4)
    jack(c, 420, 150, 1.7, arm_r="wave", expr="happy")


SCENES = [
    s01_the_cow, s02_to_market, s03_the_beans, s04_out_the_window,
    s05_the_beanstalk, s06_climbing, s07_the_castle_door, s08_fee_fi_fo_fum,
    s09_counting_gold, s10_down_with_the_gold, s11_the_golden_hen,
    s12_the_harp, s13_the_chase, s14_chop,
]
