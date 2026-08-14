"""Sleeping Beauty -- after Charles Perrault's "La Belle au bois dormant" (1697)."""

import math

from art import *          # noqa: F401,F403
from art import _rng, _ol, LINE, LW, P
from scenery import *      # noqa: F401,F403
import layout
from layout import W, H, BASE

SLUG = "sleeping-beauty"
ACCENT = "#5B3A7A"

BACK_ACCENT = "#F6E3B0"

TEXT = {
    "en": {
        "TITLE": "Sleeping Beauty",
        "SUBTITLE": "an old fairy tale, told again",
        "BYLINE": "after the story by Charles Perrault",
        "BELONGS_TO": "This book belongs to",
        "THE_END": "The End",
        "COLOPHON": (
            "A retelling of “La Belle au bois dormant”, printed by "
            "Charles Perrault in 1697.\n"
            "Illustrations drawn as vector art. Made to be read aloud."),
        "BACK_QUOTE": ["“She will sleep a hundred years,",
                       "and then somebody will come.”"],
        "PAGES": [
            # 1
            "A King and a Queen had wished for a child for a very long "
            "time, and at last one came.\n"
            "They were so pleased that they invited the whole kingdom to "
            "the christening.",
            # 2
            "Seven fairies were asked to be godmothers, and each was given "
            "a gold plate and a gold spoon, and each one leaned over the "
            "cradle to give a gift.",
            # 3
            "“She shall be kind,” said the first. “She shall be clever,” "
            "said the second.\n"
            "Dancing, said the third. Singing, said the fourth. Music, "
            "said the fifth. And laughing, said the sixth — “which is "
            "worth more than all of it.”",
            # 4
            "Then the door banged.\n"
            "In came a very old fairy that nobody had invited, because "
            "everybody had thought she was dead, or abroad, or both.",
            # 5
            "“Here is my gift,” she said. “One day the Princess will prick "
            "her finger on a spindle. And that will be that.”\n"
            "Then she went out, and the door banged again.",
            # 6
            "But the seventh fairy had not given her gift yet.\n"
            "“I cannot undo it,” she said. “But I can soften it. She will "
            "not die. She will sleep a hundred years — and then somebody "
            "will come.”",
            # 7
            "The King had every spindle in the kingdom collected and "
            "burnt, and made a law about it, and felt a good deal better.",
            # 8
            "Sixteen years went by.\n"
            "One afternoon the Princess was running up a staircase she had "
            "never been up before, and at the top she found a little room, "
            "and in it an old woman, spinning.",
            # 9
            "“What is that?” said the Princess, who had never seen a "
            "spindle in her life.\n"
            "“Try it,” said the old woman.\n"
            "She touched it — and fell asleep before she reached the "
            "floor.",
            # 10
            "The seventh fairy came at once. “She will be lonely,” she "
            "said, “waking up on her own.”\n"
            "So she put the whole castle to sleep: the King, the Queen, "
            "the cook, the dogs, the fire in the grate and the birds on "
            "the roof.",
            # 11
            "And a wood grew up around it. Not a nice wood. Thorns as "
            "thick as your arm, and brambles over the top, until the "
            "highest tower looked like the last mast of a sinking ship.",
            # 12
            "A hundred years later a prince came riding by and asked what "
            "was behind the thorns.\n"
            "An old man told him what his grandfather had told him. So the "
            "prince got down off his horse and walked up to the hedge.",
            # 13
            "And the thorns opened, all by themselves, and closed again "
            "behind him.\n"
            "He went through the sleeping castle, past the sleeping cook "
            "and the sleeping dogs, and up the little staircase.",
            # 14
            "She opened her eyes. “Oh,” she said. “Is it you? You have "
            "been a very long time.”\n"
            "And all over the castle the fire crackled, and the dogs "
            "barked, and the cook went on basting the chicken exactly "
            "where he had left off.",
        ],
    },
}


# ----------------------------------------------------------- cast helpers ---

FAIRY_COLOURS = ("#8FBF9E", "#9CB6DE", "#E4A8C4", "#EFD08A", "#B79CD6",
                 "#8FC9C4", "#F0B49A")


def fairy(c, x, y, s=1.0, tone=0, **kw):
    kw.setdefault("robe", FAIRY_COLOURS[tone % len(FAIRY_COLOURS)])
    kw.setdefault("hair", ("#7A4B2A", "#C9A05E", "#4E3A2A")[tone % 3])
    kw.setdefault("hat", "cone")
    kw.setdefault("wings", "#DCEBF6")
    kw.setdefault("long_hair", True)
    return draw_person(c, x, y, s, **kw)


def old_fairy(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#4E3F5E")
    kw.setdefault("hair", "#C6C0B8")
    kw.setdefault("hat", "cone")
    kw.setdefault("cloak", "#3A2F48")
    kw.setdefault("long_hair", True)
    return draw_person(c, x, y, s, **kw)


def princess(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#E9A0BC")
    kw.setdefault("hair", "hair_gold")
    kw.setdefault("long_hair", True)
    kw.setdefault("hat", "tiara")
    return draw_person(c, x, y, s, **kw)


def king(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "king_robe")
    kw.setdefault("hair", "hair_grey")
    kw.setdefault("beard", True)
    kw.setdefault("crown", True)
    return draw_person(c, x, y, s, **kw)


def queen(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#7A5A9E")
    kw.setdefault("hair", "#5E4630")
    kw.setdefault("long_hair", True)
    kw.setdefault("crown", True)
    return draw_person(c, x, y, s, **kw)


def prince(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#35558A")
    kw.setdefault("trim", "gold")
    kw.setdefault("hair", "#5E4630")
    kw.setdefault("hat", "cap")
    return draw_person(c, x, y, s, **kw)


def cradle(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 2, 56, 12, alpha=0.14)
    _ol(c, [(-52, 44), (-46, 8), (0, 0), (46, 8), (52, 44), (0, 34)],
        "wood", tension=0.85)
    _ol(c, [(-46, 34), (0, 26), (46, 34), (40, 52), (0, 44), (-40, 52)],
        "#F6EFE0", tension=0.8)
    _ol(c, [(-58, 6), (-40, -2), (0, -8), (40, -2), (58, 6), (0, 2)],
        "wood_dk", tension=0.7)
    circle(c, 0, 52, 11, fill="#F0C9A0", stroke=LINE, lw=1.3)
    for dx in (-3.5, 3.5):
        stroke_path(c, [(dx - 2, 53), (dx, 54.4), (dx + 2, 53)], color="ink",
                    lw=1.2)
    stroke_path(c, [(-3, 47), (0, 49), (3, 47)], color="ink", lw=1.3)
    c.restoreState()


def great_hall(c, horizon=330, wall="#D6CCBC"):
    stone_hall(c, horizon)
    for i, bx in enumerate((132, 356, 580, 780)):
        banner(c, bx, H - 40, 56, 160,
               ("cape", "#3F6FA8", "cape", "#3F6FA8")[i], "gold")


def sleep_z(c, x, y, n=3, size=20, color="#8A7A9E"):
    for i in range(n):
        layout.bold_left(c, x + i * 26, y + i * 30, "z", size + i * 7, color)


# ----------------------------------------------------------------- scenes ---

def COVER_ART(c):
    sky(c, 0, 236, W, H - 236, "#4A3A6B", "#8A76A8")
    for i in range(42):
        rnd = _rng(i + 3)
        sparkle(c, rnd() * W, 250 + rnd() * 330, 2 + 4 * rnd(),
                color="#FFF6DA", alpha=0.7)
    hills(c, -20, 212, W + 40, 60, "#3E3358", bumps=4, seedoff=1.2)
    castle(c, 640, 232, 0.72, wall="#B7A8C4", roof="#4A3A66", flag="#8A6AA8",
           windows="#3E3258")
    ground(c, 0, 0, W, 244, "#3E4A58", "#4A5766")
    thorn_hedge(c, 470, W + 40, 200, 210, color="#3E4A3C", seed=9,
                flowers=True)
    thorn_hedge(c, -40, 210, 200, 180, color="#3E4A3C", seed=13, flowers=True)
    princess(c, 366, BASE - 22, 1.86, expr="closed", arm_r="clasp")
    for i in range(9):
        sparkle(c, 300 + (i % 4) * 34, 290 + i * 22, 6, color="#F6C453",
                alpha=0.85)


def NAMEPLATE_ART(c):
    c.saveState()
    c.translate(W / 2, 200)
    shadow(c, 0, 4, 140, 20, alpha=0.10)
    spinning_wheel(c, -104, 0, 0.86)
    for i, (rx, ry) in enumerate(((92, 30), (140, 16), (116, 66))):
        for k in range(5):
            a = k * 2 * math.pi / 5
            circle(c, rx + 8 * math.cos(a), ry + 8 * math.sin(a), 6.4,
                   fill="#F3B8C6", stroke=LINE, lw=1.1)
        circle(c, rx, ry, 5, fill="#D6455C")
    c.restoreState()


def s01_the_christening(c):
    great_hall(c, 330)
    rect(c, 372, 386, 100, 140, fill="#7FB6D4", r=50, stroke="stone_dk", lw=3.4)
    stroke_path(c, [(422, 386), (422, 526)], color="stone_dk", lw=2.8)
    poly(c, [(120, 40), (250, BASE - 4), (580, BASE - 4), (526, 40)],
         fill="cape_dk")
    poly(c, [(140, 40), (264, BASE - 8), (566, BASE - 8), (510, 40)],
         fill="cape")
    cradle(c, 422, BASE, 1.35)
    king(c, 258, BASE, 1.56, arm_r="reach", expr="happy")
    queen(c, 596, BASE, 1.52, arm_l="reach", expr="happy", flip=True)
    for i in range(8):
        sparkle(c, 352 + i * 22, 300 + (i % 3) * 26, 5, color="#F6C453",
                alpha=0.8)


def s02_seven_fairies(c):
    great_hall(c, 330, )
    cradle(c, 432, BASE, 1.2)
    for i, (fx, sc) in enumerate(((110, 1.24), (206, 1.3), (302, 1.26),
                                  (566, 1.28), (664, 1.24), (762, 1.3))):
        fairy(c, fx, BASE, sc, tone=i, arm_r="up" if i % 2 else "reach",
              expr="happy", flip=fx > 450)
    for i in range(12):
        rnd = _rng(i + 6)
        sparkle(c, 340 + rnd() * 190, 280 + rnd() * 160, 4 + 5 * rnd(),
                color="#F6C453", alpha=0.85)


def s03_the_gifts(c):
    great_hall(c, 330)
    cradle(c, 424, BASE, 1.3)
    for i, (fx, sc) in enumerate(((146, 1.3), (262, 1.26), (596, 1.3),
                                  (712, 1.26))):
        fairy(c, fx, BASE, sc, tone=i, arm_r="point", expr="happy",
              flip=fx > 450, wand=True)
    for k, al in ((1.0, 0.14), (0.66, 0.16)):
        ellipse(c, 424, 330, 190 * k, 120 * k, fill="#F6C453", alpha=al)
    for i in range(16):
        rnd = _rng(i + 11)
        sparkle(c, 300 + rnd() * 250, 250 + rnd() * 220, 3 + 6 * rnd(),
                color="#FFF6DA", alpha=0.9)


def s04_the_uninvited(c):
    great_hall(c, 330)
    rect(c, 66, 200, 150, 250, fill="#4A3A2E", r=6, stroke=LINE, lw=2.6)
    rect(c, 82, 200, 118, 226, fill="#2E2440", r=4)
    for i in range(5):
        stroke_path(c, [(238 - i * 14, 300 + i * 16), (300 - i * 14,
                                                       292 + i * 16)],
                    color="#8A7A9E", lw=3.0, alpha=0.5)
    old_fairy(c, 300, BASE, 1.7, arm_r="point", expr="sad")
    cradle(c, 566, BASE, 1.2)
    king(c, 700, BASE, 1.48, expr="surprised", arm_r="up", flip=True)
    queen(c, 790, BASE, 1.44, expr="surprised", arm_l="up", flip=True)


def s05_the_curse(c):
    great_hall(c, 330)
    for k, al in ((1.0, 0.16), (0.62, 0.2)):
        ellipse(c, 300, 320, 170 * k, 150 * k, fill="#5E4A7A", alpha=al)
    old_fairy(c, 300, BASE, 1.78, arm_r="point", arm_l="up", expr="sad")
    spinning_wheel(c, 616, 206, 1.15)
    for i in range(9):
        rnd = _rng(i + 17)
        sparkle(c, 400 + rnd() * 200, 260 + rnd() * 180, 4 + 5 * rnd(),
                color="#B79CD6", alpha=0.8)
    cradle(c, 132, BASE, 1.0)


def s06_the_seventh_fairy(c):
    great_hall(c, 330)
    cradle(c, 300, BASE, 1.3)
    for k, al in ((1.0, 0.16), (0.6, 0.2)):
        ellipse(c, 560, 330, 176 * k, 132 * k, fill="#8FC9C4", alpha=al)
    fairy(c, 560, BASE, 1.76, tone=5, arm_r="point", expr="happy", wand=True,
          flip=True)
    king(c, 116, BASE, 1.44, expr="sad", arm_r="clasp")
    queen(c, 760, BASE, 1.42, expr="sad", arm_l="clasp", flip=True)
    for i in range(12):
        rnd = _rng(i + 23)
        sparkle(c, 330 + rnd() * 240, 260 + rnd() * 200, 3 + 6 * rnd(),
                color="#CFE7F3", alpha=0.85)


def s07_burning_the_spindles(c):
    meadow(c, 316, sky_top="#F0C08A", sky_bot="#FBE6C6", sunpos=None,
           clouds=((680, 528, 0.85),))
    castle(c, 690, 300, 0.82, wall="#DED5C6", roof="#6B4A7A", flag="#8A6AA8")
    grass_tufts(c, 0, W, 288, n=16, seed=19)
    hearth_glow(c, 380, 268, 190)
    campfire(c, 380, 196, 1.9)
    for i, (sx, rot) in enumerate(((300, 24), (462, -18), (330, -40))):
        c.saveState()
        c.translate(sx, 210 + i * 12)
        c.rotate(rot)
        taper(c, [(0, 0), (30, 6), (58, 2)], 4.0, 1.4, fill="wood",
              stroke=LINE, lw=1.1)
        c.restoreState()
    king(c, 168, BASE, 1.56, arm_r="point", expr="happy")
    for i, gx in enumerate((560, 646)):
        draw_person(c, gx, BASE, 1.4, robe=("#6E7A88", "#7A6E5E")[i],
                    hair="#4E3A2A", arm_r="hold", flip=True)


def s08_the_little_room(c):
    interior(c, wall="#C6B79E", floor="#8A6743", horizon=320, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    # a narrow window, high up
    rect(c, 96, 380, 70, 150, fill="#8FB6D4", r=34, stroke="wood_dk", lw=3.4)
    # the staircase she had never been up
    for i in range(6):
        rect(c, 700 + i * 22, 200 + i * 30, 120 - i * 4, 26, fill="stone",
             stroke="stone_dk", lw=1.4)
    spinning_wheel(c, 292, 200, 1.4)
    draw_person(c, 190, BASE, 1.5, robe="#6B5A6E", hair="#C6C0B8",
                hat="bonnet", long_hair=True, arm_r="reach", expr="happy")
    princess(c, 528, BASE, 1.62, arm_l="reach", expr="surprised", flip=True)


def s09_the_spindle(c):
    interior(c, wall="#C6B79E", floor="#8A6743", horizon=320, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    rect(c, 700, 380, 70, 150, fill="#8FB6D4", r=34, stroke="wood_dk", lw=3.4)
    spinning_wheel(c, 560, 200, 1.4)
    for k, al in ((1.0, 0.14), (0.6, 0.18)):
        ellipse(c, 620, 330, 130 * k, 108 * k, fill="#B79CD6", alpha=al)
    for i in range(8):
        rnd = _rng(i + 29)
        sparkle(c, 560 + rnd() * 140, 280 + rnd() * 130, 4 + 5 * rnd(),
                color="#D8C4EE", alpha=0.85)
    # the Princess, gone down in a heap
    shadow(c, 300, 202, 96, 17, alpha=0.16)
    c.saveState()
    c.translate(300, 202)
    c.rotate(-78)
    princess(c, 0, 0, 1.6, expr="closed", arm_r="down", arm_l="down",
             shad=False)
    c.restoreState()
    sleep_z(c, 400, 300, 3, 20)


def s10_the_castle_sleeps(c):
    interior(c, wall="#B7A896", floor="#7A5A3C", horizon=326, beams=False)
    rect(c, 0, H - 46, W, 46, fill="#5E4632")
    hearth_glow(c, 156, 400, 150)
    fireplace(c, 156, 326, 0.94)
    table(c, 560, 176, 1.5, w=150)
    # the cook, asleep over the chicken
    _ol(c, [(520, 250), (556, 262), (592, 250), (570, 236), (536, 236)],
        "#C9A05E", tension=0.85)
    draw_person(c, 470, BASE, 1.48, robe="#D8CCBA", hair="#6B4A2E",
                apron="#F2ECE0", hat="cap", expr="closed", arm_r="reach")
    king(c, 700, BASE, 1.46, expr="closed", arm_r="down", flip=True)
    queen(c, 790, BASE, 1.42, expr="closed", arm_r="down", flip=True)
    for k, al in ((1.0, 0.10), (0.6, 0.12)):
        rect(c, 0, 0, W, H, fill="#6E7FA8", alpha=al)
    sleep_z(c, 300, 330, 3, 22)
    sleep_z(c, 620, 380, 3, 18)


def s11_the_thorns(c):
    sky(c, 0, 300, W, H - 300, "#6E7FA8", "#B4C2D6")
    for cx, cy, s in ((180, 528, 1.1), (700, 496, 0.9)):
        cloud(c, cx, cy, s, fill="#D8E2EE")
    hills(c, -20, 274, W + 40, 56, "#4E5E4A", bumps=4, seedoff=1.6)
    ground(c, 0, 0, W, 306, "#4A5A46", "#56674F")
    castle(c, 430, 306, 0.96, wall="#A8A090", roof="#4E4258", flag="#6E5C82",
           windows="#3E4458")
    thorn_hedge(c, -40, 430, 190, 300, color="#3E4A3C", seed=21)
    thorn_hedge(c, 400, W + 40, 190, 320, color="#44523F", seed=27)
    for bx, by in ((150, 520), (206, 548)):
        bird(c, bx, by, 1.3, color="#5E6B7A")


def s12_the_prince_asks(c):
    sky(c, 0, 296, W, H - 296, "#BFD8E8", "#E2EEF4")
    for cx, cy, s in ((220, 530, 1.0), (660, 500, 0.85)):
        cloud(c, cx, cy, s)
    hills(c, -20, 272, W + 40, 54, "#7E9A78", bumps=4, seedoff=0.9)
    ground(c, 0, 0, W, 300, "#7A9470", "#8AA47E")
    thorn_hedge(c, 470, W + 40, 196, 290, color="#44523F", seed=31)
    grass_tufts(c, 0, 470, 268, n=14, seed=33, color="#5E7A56")
    horse(c, 158, BASE, 1.05, body="#E4D8C4", mane="#8A7A62")
    prince(c, 336, BASE, 1.6, arm_r="point", expr="happy")
    draw_person(c, 452, BASE, 1.46, robe="#7A6E5E", hair="hair_grey",
                beard=True, arm_l="reach", expr="happy", flip=True)


def s13_the_thorns_open(c):
    sky(c, 0, 300, W, H - 300, "#CFE0EC", "#EAF2F6")
    for cx, cy, s in ((190, 534, 1.05), (690, 504, 0.9)):
        cloud(c, cx, cy, s, fill="#FFFFFF")
    hills(c, -20, 276, W + 40, 54, "#7E9A78", bumps=4, seedoff=1.4)
    ground(c, 0, 0, W, 304, "#7A9470", "#8AA47E")
    castle(c, 430, 304, 0.9, wall="#C6BEAE", roof="#6B5A7A", flag="#8A6AA8",
           windows="#5E6E8A")
    thorn_hedge(c, -40, 250, 194, 300, color="#44523F", seed=37, flowers=True)
    thorn_hedge(c, 620, W + 40, 194, 300, color="#44523F", seed=41,
                flowers=True)
    prince(c, 430, 200, 1.66, arm_l="up", expr="happy", legs="stride")
    for i in range(12):
        rnd = _rng(i + 43)
        sparkle(c, 300 + rnd() * 260, 230 + rnd() * 220, 4 + 6 * rnd(),
                color="#FFF6DA", alpha=0.85)


def s14_she_opened_her_eyes(c):
    interior(c, wall="#D6C6AE", floor="#8A6743", horizon=322, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    rect(c, 106, 380, 76, 156, fill="#BFE1F0", r=38, stroke="wood_dk", lw=3.4)
    circle(c, 144, 470, 34, fill="#F6E7B8", alpha=0.45)
    bed(c, 372, BASE - 6, 1.5, quilt="#E9A0BC")
    princess(c, 372, 244, 1.34, expr="happy", arm_r="up", shad=False)
    prince(c, 626, BASE - 6, 1.62, arm_l="reach", expr="happy", flip=True)
    for i in range(14):
        rnd = _rng(i + 47)
        sparkle(c, 260 + rnd() * 360, 250 + rnd() * 220, 4 + 6 * rnd(),
                color="#FFF6DA", alpha=0.85)


def END_ART(c):
    meadow(c, 300, sky_top="#F5D6A0", sky_bot="#FDEFD6", sunpos=(120, 512),
           clouds=((480, 536, 0.85), (730, 500, 0.95)))
    castle(c, 620, 288, 0.86, wall="#E4DCCE", roof="#B0566B", flag="#C86B7E",
           windows="#7FB6D4")
    ground(c, 0, 0, W, 252, "grass", "grass_lt")
    grass_tufts(c, 0, W, 230, n=20, seed=51)
    thorn_hedge(c, 760, W + 40, 214, 130, color="#5E7A56", seed=53,
                flowers=True)
    princess(c, 250, 220, 1.54, arm_r="reach", expr="happy")
    prince(c, 372, 220, 1.58, arm_l="reach", expr="happy", flip=True)
    for fx in (96, 160, 470, 540):
        flower(c, fx, 208, 1.3, petal="#F3B8C6")


def BACK_ART(c):
    sky(c, 0, 0, W, H, "#4A3A6B", "#9C88BE")
    for i in range(38):
        rnd = _rng(i + 57)
        sparkle(c, rnd() * W, 140 + rnd() * 430, 2 + 4 * rnd(),
                color="#FFF6DA", alpha=0.7)
    hills(c, -20, 148, W + 40, 62, "#3E3358", bumps=4, seedoff=1.0)
    ground(c, 0, 0, W, 174, "#3E4A58", "#4A5766")
    thorn_hedge(c, -40, 240, 150, 170, color="#3E4A3C", seed=59, flowers=True)
    thorn_hedge(c, 620, W + 40, 150, 180, color="#3E4A3C", seed=61,
                flowers=True)
    spinning_wheel(c, 430, 140, 1.15)


SCENES = [
    s01_the_christening, s02_seven_fairies, s03_the_gifts, s04_the_uninvited,
    s05_the_curse, s06_the_seventh_fairy, s07_burning_the_spindles,
    s08_the_little_room, s09_the_spindle, s10_the_castle_sleeps,
    s11_the_thorns, s12_the_prince_asks, s13_the_thorns_open,
    s14_she_opened_her_eyes,
]
