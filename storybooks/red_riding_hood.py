"""Little Red Riding Hood -- after Perrault and the Brothers Grimm."""

import math

from art import *          # noqa: F401,F403
from art import _rng, _ol, LINE, LW, P
from scenery import *      # noqa: F401,F403
import layout
from layout import W, H, BASE

SLUG = "little-red-riding-hood"
ACCENT = "#96291F"

TEXT = {
    "en": {
        "TITLE": "Little Red Riding Hood",
        "SUBTITLE": "an old fairy tale, told again",
        "BYLINE": "after Perrault and the Brothers Grimm",
        "BELONGS_TO": "This book belongs to",
        "THE_END": "The End",
        "COLOPHON": (
            "A retelling of the tale printed by Charles Perrault in 1697 "
            "and by the Brothers Grimm in 1812.\n"
            "Illustrations drawn as vector art. Made to be read aloud."),
        "BACK_QUOTE": ["“What big teeth you have!”",
                       "“All the better to EAT you with!”"],
        "PAGES": [
            # 1
            "Her grandmother had made her a red cloak with a hood, and she "
            "wore it every single day, and would not take it off even for "
            "dinner.\n"
            "So everybody called her Little Red Riding Hood.",
            # 2
            "“Grandma is poorly,” said her mother one morning. “Take her "
            "this cake and this little pot of butter.\n"
            "And Red — stay on the path.”",
            # 3
            "“I will,” said Red, and off she went into the wood, swinging "
            "the basket, with the trees going up and up on either side "
            "like the pillars of a church.",
            # 4
            "Halfway along, somebody stepped out from behind an oak.\n"
            "“Good morning,” said the Wolf, in his politest voice. “And "
            "where are we off to today?”",
            # 5
            "“To my grandmother's,” said Red, who had never been told not "
            "to talk to wolves. “The little house past the mill, with the "
            "blue door.”\n"
            "“How lovely,” said the Wolf.",
            # 6
            "“Look at all these flowers,” he said. “Wouldn't she like "
            "some?”\n"
            "And Red thought that she would, and stepped off the path "
            "without noticing that she had.",
            # 7
            "The Wolf went the short way, and ran, and ran, and got there "
            "first.",
            # 8
            "Tap, tap, tap on the blue door.\n"
            "Grandmother was old but she was not silly. She took one look "
            "through the window, hopped out of bed, and shut herself in "
            "the wardrobe.",
            # 9
            "So the Wolf let himself in, and put on her spare cap, and "
            "pulled the blanket up to his chin, and lay there feeling "
            "extremely pleased with himself.",
            # 10
            "Red came in with her flowers.\n"
            "“Grandma,” she said, “what big ears you have.”\n"
            "“All the better to hear you with, my dear.”",
            # 11
            "“And Grandma — what big eyes you have.”\n"
            "“All the better to see you with, my dear.”",
            # 12
            "“And Grandma,” said Red, backing towards the door, “what very "
            "big teeth you have.”\n"
            "“ALL THE BETTER TO EAT YOU WITH!” roared the Wolf, and came "
            "out of the bed like a thunderstorm.",
            # 13
            "Red screamed the loudest scream of her life.\n"
            "A woodcutter working at the end of the lane heard it, and "
            "came through that door with his axe before the Wolf had got "
            "his second foot on the floor.",
            # 14
            "The Wolf went out of the window and over the hill and did not "
            "stop, and nobody in that wood ever saw him again.\n"
            "Grandmother came out of the wardrobe. They ate the cake. Red "
            "told the story about nine hundred times.",
        ],
    },
}


# ----------------------------------------------------------- cast helpers ---

def red(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#E4C9A8")
    kw.setdefault("hair", "#5E4630")
    kw.setdefault("hood", "red_cloak")
    kw.setdefault("cloak", "red_cloak")
    return draw_person(c, x, y, s, child=True, **kw)


def ma(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#7A8C9E")
    kw.setdefault("hair", "#6B4A2E")
    kw.setdefault("apron", "#EFE6D4")
    kw.setdefault("long_hair", True)
    return draw_person(c, x, y, s, **kw)


def granny(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#9C8FA8")
    kw.setdefault("hair", "#D8D2C8")
    kw.setdefault("hat", "bonnet")
    kw.setdefault("long_hair", True)
    return draw_person(c, x, y, s, **kw)


def woodcutter(c, x, y, s=1.0, **kw):
    kw.setdefault("robe", "#7A6248")
    kw.setdefault("hair", "#4E3A2A")
    kw.setdefault("beard", True)
    kw.setdefault("hat", "cap")
    return draw_person(c, x, y, s, **kw)


def granny_house(c, horizon=318, wall="#E4D6C0", floor="#A87E50"):
    interior(c, wall=wall, floor=floor, horizon=horizon, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    for bx in (150, 420, 690):
        rect(c, bx - 10, horizon, 20, H - horizon - 46, fill="#C6B49A")


def wardrobe(c, x, y, s=1.0, open_=False):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, -62, 0, 124, 216, fill="wood", stroke=LINE, lw=1.8)
    rect(c, -68, 212, 136, 18, fill="wood_dk", r=3, stroke=LINE, lw=1.6)
    if open_:
        rect(c, -54, 10, 52, 196, fill="#5E4632", r=3, stroke=LINE, lw=1.4)
        _ol(c, [(-2, 10), (46, 20), (48, 200), (-2, 206)], shade("wood", 0.9),
            tension=0.3)
        circle(c, 40, 108, 3.6, fill="gold_dk")
    else:
        for i in range(2):
            rect(c, -54 + i * 56, 10, 52, 196, fill=shade("wood", 0.9),
                 stroke=LINE, lw=1.4, r=3)
            circle(c, -6 + i * 12, 108, 3.6, fill="gold_dk")
    c.restoreState()


def blue_door_cottage(c, x, y, s=1.0):
    cottage(c, x, y, s, wall="#EFE2CA", roof="#9C6B58")
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, -14, 0, 28, 40, fill="#3F6FA8", r=13, stroke=LINE, lw=1.6)
    circle(c, 8, 20, 2.6, fill="gold_dk")
    c.restoreState()


# ----------------------------------------------------------------- scenes ---

def COVER_ART(c):
    forest(c, 300, back="#4E7A52", mid="#3F6845", floor="#6E8B5F",
           sky_top="#C9E2EE", sky_bot="#E8F2F6", n=11, seed=6)
    road(c, 262, color="#C6AE86")
    for fx in (100, 176, 700, 780):
        flower(c, fx, 236, 1.3, petal="#FFFFFF")
    basket(c, 528, 208, 1.5)
    red(c, 396, BASE, 2.35, arm_r="hold", expr="happy")
    draw_wolf(c, 700, 214, 1.05, pose="lurk", expr="sly", flip=True)
    for bx, by in ((196, 512), (250, 540)):
        bird(c, bx, by, 1.3, color="#5E6B52")


def NAMEPLATE_ART(c):
    c.saveState()
    c.translate(W / 2, 202)
    shadow(c, 0, 4, 130, 20, alpha=0.10)
    basket(c, -96, 0, 2.1)
    for i, (fx, fy) in enumerate(((70, 12), (120, 4), (96, 44), (146, 34))):
        flower(c, fx, fy, 2.2, petal=("#FFFFFF", "#F3B8C6", "#F6C453",
                                      "#FFFFFF")[i])
    c.restoreState()


def s01_the_red_cloak(c):
    meadow(c, 318, clouds=((210, 522, 1.0), (662, 498, 0.85)))
    blue_door_cottage(c, 726, 300, 1.2)
    tree(c, 74, 304, 1.2)
    grass_tufts(c, 0, W, 288, n=20, seed=3)
    for fx in (250, 320, 560):
        flower(c, fx, 268, 1.2, petal="#F3B8C6")
    granny(c, 508, BASE, 1.5, arm_r="reach", expr="happy")
    red(c, 342, BASE, 2.0, arm_r="up", expr="happy")


def s02_the_basket(c):
    interior(c, wall="#E4D6C0", floor="#A87E50", horizon=316, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    hearth_glow(c, 706, 396, 170)
    fireplace(c, 712, 316, 0.92)
    table(c, 300, 176, 1.35, w=120)
    basket(c, 300, 240, 1.5)
    ma(c, 174, BASE, 1.56, arm_r="point", expr="happy")
    red(c, 470, BASE, 2.05, arm_l="reach", expr="happy", flip=True)


def s03_into_the_wood(c):
    forest(c, 330, n=13, seed=9)
    road(c, 272, color="#C6AE86")
    for fx in (86, 150, 720, 800):
        flower(c, fx, 248, 1.2, petal="#FFFFFF")
    bush(c, 210, 252, 1.5, color="#4E7A52")
    bush(c, 660, 258, 1.3, color="#4E7A52")
    red(c, 430, BASE, 2.1, arm_r="hold", expr="happy", legs="stride")
    basket(c, 494, 214, 1.3)
    for bx, by in ((160, 500), (216, 528), (700, 480)):
        bird(c, bx, by, 1.2, color="#5E6B52")


def s04_the_wolf(c):
    forest(c, 326, n=12, seed=13, mid="#375C3E")
    road(c, 268, color="#C6AE86")
    bush(c, 128, 250, 1.6, color="#446B48")
    red(c, 296, BASE, 2.05, arm_r="hold", expr="surprised")
    basket(c, 356, 210, 1.25)
    draw_wolf(c, 606, 206, 1.28, pose="sit", expr="sly")
    for fx in (760, 810):
        flower(c, fx, 244, 1.2, petal="#F6C453")


def s05_the_blue_door(c):
    forest(c, 322, n=12, seed=17, mid="#375C3E")
    road(c, 264, color="#C6AE86")
    red(c, 262, BASE, 2.0, arm_r="point", expr="happy")
    draw_wolf(c, 616, 202, 1.3, pose="stand", expr="sly")
    # what he is picturing
    for k, al in ((1.0, 0.22), (0.62, 0.26)):
        ellipse(c, 690, 440, 130 * k, 84 * k, fill="#FFFFFF", alpha=al)
    c.saveState()
    c.translate(690, 402)
    c.scale(0.42, 0.42)
    blue_door_cottage(c, 0, 0, 1.0)
    c.restoreState()
    for i, (bx, by, br) in enumerate(((596, 356, 6), (620, 378, 8),
                                      (648, 400, 10))):
        circle(c, bx, by, br, fill="#FFFFFF", alpha=0.55)


def s06_the_flowers(c):
    forest(c, 330, n=12, seed=21, floor="#7A9668")
    road(c, 268, color="#C6AE86")
    rnd = _rng(31)
    for i in range(26):
        fx = 120 + rnd() * 640
        fy = 208 + rnd() * 54
        flower(c, fx, fy, 1.2 + 0.6 * rnd(),
               petal=("#FFFFFF", "#F3B8C6", "#F6C453", "#C9B8E4")[i % 4])
    red(c, 356, 214, 2.0, arm_r="reach", expr="happy", legs="stride")
    basket(c, 262, 206, 1.3)
    draw_wolf(c, 726, 236, 1.0, pose="lurk", expr="sly", flip=True)


def s07_the_short_way(c):
    forest(c, 318, n=13, seed=25, mid="#375C3E", floor="#66845A")
    road(c, 258, color="#C6AE86")
    blue_door_cottage(c, 760, 246, 0.9)
    draw_wolf(c, 380, 208, 1.5, pose="run", expr="grin")
    motion(c, 236, 262, 4, 84, 17, color="#FFFFFF", alpha=0.6)
    for bx, by in ((166, 506), (222, 534)):
        bird(c, bx, by, 1.2, color="#5E6B52")


def s08_tap_tap_tap(c):
    meadow(c, 314, sky_top="#CFE2EE", clouds=((216, 520, 0.95),))
    blue_door_cottage(c, 316, 296, 1.7)
    tree(c, 780, 300, 1.15)
    grass_tufts(c, 0, W, 284, n=16, seed=27)
    draw_wolf(c, 596, BASE, 1.42, pose="sit", expr="grin", flip=True)
    for i in range(3):
        stroke_path(c, [(470 - i * 16, 320 + i * 14), (440 - i * 16,
                                                       328 + i * 14)],
                    color="#FFFFFF", lw=3.0, alpha=0.6)
    layout.bold_left(c, 452, 430, "tap  tap  tap", 24, "#7A6A52")


def s09_in_the_bed(c):
    granny_house(c, 318)
    rect(c, 84, 372, 80, 150, fill="#BFE1F0", r=38, stroke="wood_dk", lw=3.2)
    wardrobe(c, 748, 200, 1.0)
    bed(c, 400, BASE - 8, 1.55, quilt="#7A8C9E")
    # the Wolf, tucked up and delighted with himself
    c.saveState()
    c.translate(392, 246)
    c.scale(0.92, 0.92)
    draw_wolf(c, 0, 0, 1.0, pose="sit", expr="sly", bonnet=True, shad=False)
    c.restoreState()
    _ol(c, [(300, 236), (400, 258), (500, 236), (500, 210), (300, 210)],
        "#7A8C9E", tension=0.7)
    sleep_z = None
    for i in range(4):
        sparkle(c, 560 + i * 20, 300 + (i % 2) * 22, 5, color="#F6E3B0",
                alpha=0.6)


def s10_what_big_ears(c):
    granny_house(c, 318)
    rect(c, 84, 372, 80, 150, fill="#BFE1F0", r=38, stroke="wood_dk", lw=3.2)
    wardrobe(c, 762, 200, 0.95)
    bed(c, 452, BASE - 8, 1.5, quilt="#7A8C9E")
    c.saveState()
    c.translate(444, 244)
    c.scale(0.9, 0.9)
    draw_wolf(c, 0, 0, 1.0, pose="sit", expr="sly", bonnet=True, shad=False)
    c.restoreState()
    _ol(c, [(352, 234), (452, 256), (552, 234), (552, 208), (352, 208)],
        "#7A8C9E", tension=0.7)
    red(c, 218, BASE, 2.0, arm_r="hold", expr="surprised")
    basket(c, 158, 206, 1.2)


def s11_what_big_eyes(c):
    granny_house(c, 318, wall="#DFCFB6")
    rect(c, 750, 372, 80, 150, fill="#BFE1F0", r=38, stroke="wood_dk", lw=3.2)
    bed(c, 496, BASE - 8, 1.55, quilt="#7A8C9E")
    c.saveState()
    c.translate(486, 248)
    c.scale(1.0, 1.0)
    draw_wolf(c, 0, 0, 1.0, pose="sit", expr="grin", bonnet=True, shad=False)
    c.restoreState()
    _ol(c, [(390, 238), (496, 260), (602, 238), (602, 210), (390, 210)],
        "#7A8C9E", tension=0.7)
    red(c, 232, BASE, 2.05, arm_r="up", expr="surprised")


def s12_what_big_teeth(c):
    granny_house(c, 318, wall="#D8C6AC")
    wardrobe(c, 96, 200, 0.95)
    bed(c, 470, BASE - 8, 1.5, quilt="#7A8C9E")
    for k, al in ((1.0, 0.14), (0.6, 0.18)):
        ellipse(c, 520, 330, 190 * k, 130 * k, fill="#C0392B", alpha=al)
    c.saveState()
    c.translate(536, 250)
    c.rotate(-16)
    draw_wolf(c, 0, 0, 1.35, pose="lurk", expr="grin", bonnet=True,
              shad=False)
    c.restoreState()
    red(c, 236, BASE, 2.05, arm_r="up", arm_l="up", expr="surprised",
        legs="stride")
    for i in range(4):
        stroke_path(c, [(340 + i * 16, 300 + i * 20), (302 + i * 16,
                                                       310 + i * 20)],
                    color="#FFFFFF", lw=3.4, alpha=0.55)


def s13_the_woodcutter(c):
    granny_house(c, 318, wall="#D8C6AC")
    rect(c, 96, 318, 150, 216, fill="#8A6743", stroke=LINE, lw=2.6)
    rect(c, 114, 318, 116, 196, fill="#7FA85E", stroke=LINE, lw=1.8)
    bed(c, 560, BASE - 8, 1.4, quilt="#7A8C9E")
    c.saveState()
    c.translate(596, 232)
    c.rotate(-24)
    draw_wolf(c, 0, 0, 1.2, pose="run", expr="surprised", shad=False)
    c.restoreState()
    woodcutter(c, 260, BASE, 1.72, arm_r="up", expr="surprised",
               legs="stride")
    axe(c, 300, 300, 1.7, rot=-28)
    red(c, 420, BASE, 1.95, arm_l="up", expr="surprised", flip=True)


def s14_the_cake(c):
    granny_house(c, 314, wall="#E4D6C0")
    hearth_glow(c, 720, 392, 160)
    fireplace(c, 726, 314, 0.88)
    wardrobe(c, 108, 196, 0.95, open_=True)
    table(c, 420, 176, 1.4, w=126)
    _ol(c, [(388, 240), (420, 252), (452, 240), (444, 224), (396, 224)],
        "#E8C58A", tension=0.8)
    _ol(c, [(392, 246), (420, 256), (448, 246), (420, 240)], "#F3B8C6",
        tension=0.85)
    for cx in (352, 490):
        circle(c, cx, 248, 12, fill="#DCEAF0", stroke=LINE, lw=1.2)
    granny(c, 268, BASE, 1.54, arm_r="reach", expr="happy")
    red(c, 556, BASE, 2.0, arm_l="up", expr="happy", flip=True)


def END_ART(c):
    meadow(c, 300, sky_top="#F5D6A0", sky_bot="#FDEFD6", sunpos=(126, 512),
           clouds=((480, 536, 0.85), (740, 502, 0.95)))
    blue_door_cottage(c, 640, 288, 1.15)
    ground(c, 0, 0, W, 250, "grass", "grass_lt")
    grass_tufts(c, 0, W, 228, n=20, seed=35)
    for fx in (90, 156, 300, 800):
        flower(c, fx, 214, 1.3, petal="#F3B8C6")
    granny(c, 396, 220, 1.46, arm_r="reach", expr="happy")
    red(c, 250, 220, 1.9, arm_r="wave", expr="happy")
    basket(c, 168, 212, 1.3)


def BACK_ART(c):
    forest(c, 200, n=11, seed=39, sky_top="#F0C08A", sky_bot="#FBE6C6",
           dusk=True, floor="#7A9668")
    for fx in (110, 180, 690, 776):
        flower(c, fx, 140, 1.3, petal="#FFFFFF")
    red(c, 380, 150, 1.9, arm_r="wave", expr="happy")
    draw_wolf(c, 640, 150, 0.95, pose="lurk", expr="sly", flip=True)


SCENES = [
    s01_the_red_cloak, s02_the_basket, s03_into_the_wood, s04_the_wolf,
    s05_the_blue_door, s06_the_flowers, s07_the_short_way, s08_tap_tap_tap,
    s09_in_the_bed, s10_what_big_ears, s11_what_big_eyes, s12_what_big_teeth,
    s13_the_woodcutter, s14_the_cake,
]
