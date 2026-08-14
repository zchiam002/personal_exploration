"""
Reusable scene pieces: landscapes, interiors, buildings and props.

Anything that shows up in more than one book lives here. Individual titles
compose these into scenes and add their own one-off bits.
"""

import math

from art import *          # noqa: F401,F403
from art import _rng, _ol, _sack, _boot, _cat_hat, LINE, LW, P
from layout import W, H, BASE



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


# ------------------------------------------------ settings for the others ---

def night_sky(c, y0=0, top="night", bottom="night2", moon_at=(720, 490),
              stars=42, seed=9):
    sky(c, 0, y0, W, H - y0, top, bottom)
    rnd = _rng(seed)
    for _ in range(stars):
        sx, sy = rnd() * W, y0 + rnd() * (H - y0)
        r = 1.2 + 2.4 * rnd()
        sparkle(c, sx, sy, r, color="#FFF6DA", alpha=0.5 + 0.5 * rnd())
    if moon_at:
        mx, my = moon_at
        for k, al in ((2.6, 0.10), (1.9, 0.13), (1.4, 0.16)):
            circle(c, mx, my, 34 * k, fill="moonlight", alpha=al)
        circle(c, mx, my, 34, fill="moonlight")
        for dx, dy, rr in ((-11, 8, 6), (10, -4, 8), (2, 15, 4)):
            circle(c, mx + dx, my + dy, rr, fill="#E4DFC0", alpha=0.55)


def forest(c, horizon=320, back="#4E7A52", mid="#3F6845", floor="#6E8B5F",
           sky_top="#BBD9E8", sky_bot="#DCEBF2", n=13, seed=4, dusk=False):
    """A wall of conifers -- the wood between one place and another."""
    if dusk:
        sky(c, 0, horizon - 40, W, H - horizon + 40, "#F0C08A", "#F7DFC0")
    else:
        sky(c, 0, horizon - 40, W, H - horizon + 40, sky_top, sky_bot)
    rnd = _rng(seed)
    for layer, (cl, hs, yb) in enumerate(((back, 1.0, 26), (mid, 1.25, 0))):
        for i in range(n + layer * 2):
            tx = -40 + (W + 80) * (i + 0.35 * rnd()) / (n + layer * 2 - 1)
            th = (150 + 90 * rnd()) * hs
            tb = horizon - yb - 30 * rnd()
            taper(c, [(tx, tb - 20), (tx, tb + th * 0.3)], 8 * hs, 6 * hs,
                  fill="#6B4A2E")
            for k in range(4):
                w = (44 - k * 8) * hs
                yy = tb + th * (0.18 + k * 0.21)
                poly(c, [(tx - w, yy), (tx + w, yy), (tx, yy + th * 0.34)],
                     fill=cl)
    ground(c, 0, 0, W, horizon - 30, floor, shade(floor, 1.08))
    grass_tufts(c, 0, W, horizon - 54, n=18, seed=seed + 3, color=shade(floor, 0.8))


def mountains(c, y, h=150, near="#8E9AAE", far="#B4BECD", peaks=5, snow=True):
    for cl, k, off in ((far, 1.0, 0.0), (near, 0.78, 0.5)):
        pts = [(-30, y - 20)]
        for i in range(peaks + 1):
            t = (i + off) / peaks
            px = -30 + (W + 60) * t
            py = y + h * k * (0.45 + 0.55 * abs(math.sin(t * 5.2 + off)))
            pts.append((px, py))
        pts.append((W + 30, y - 20))
        poly(c, pts, fill=cl)
        if snow:
            for i in range(1, peaks + 1):
                t = (i + off) / peaks
                px = -30 + (W + 60) * t
                py = y + h * k * (0.45 + 0.55 * abs(math.sin(t * 5.2 + off)))
                poly(c, [(px, py), (px - 17, py - 26), (px - 6, py - 20),
                         (px + 4, py - 27), (px + 16, py - 24)],
                     fill="#F2F4F7")


def cloud_floor(c, y, color="#F2F6FA", shade_color="#D8E4EE"):
    """The billowing ground of the country above the beanstalk."""
    rect(c, 0, 0, W, y - 26, fill=shade_color)
    rnd = _rng(6)
    for i in range(16):
        cx = -30 + (W + 60) * i / 15.0
        circle(c, cx, y - 26 + 14 * rnd(), 44 + 26 * rnd(), fill=color)
    rect(c, 0, 0, W, y - 58, fill=color)


def beanstalk(c, x, y0, y1, w=17, leaves=True, seed=2):
    """A great twisting vine climbing off the top of the page."""
    n = 9
    spine = [(x + 34 * math.sin(i * 0.85), y0 + (y1 - y0) * i / (n - 1))
             for i in range(n)]
    taper(c, spine, w, w * 0.62, fill="vine_dk", stroke=LINE, lw=LW)
    twist = [(px + 9, py) for px, py in spine]
    taper(c, twist, w * 0.42, w * 0.3, fill="vine")
    if leaves:
        for i, (px, py) in enumerate(spine[1:], 1):
            sx = -1 if i % 2 else 1
            sc = 1.0 + 0.25 * ((i % 3) - 1)
            _ol(c, [(px, py), (px + sx * 38 * sc, py + 20 * sc),
                    (px + sx * 56 * sc, py + 2 * sc),
                    (px + sx * 34 * sc, py - 16 * sc)], "vine", tension=0.9)
            stroke_path(c, [(px, py), (px + sx * 48 * sc, py + 2 * sc)],
                        color="vine_dk", lw=1.8)
        for i, (px, py) in enumerate(spine[::3]):
            _ol(c, [(px - 12, py + 8), (px - 4, py + 16), (px + 4, py + 8),
                    (px - 4, py + 2)], "#B7D98E", tension=0.9)


def thorn_hedge(c, x0, x1, y, h=190, color="thorn", seed=8, flowers=False):
    """The briar wall that grows up around the sleeping castle."""
    rnd = _rng(seed)
    base = P.get(color, color)
    # a lumpy mass rather than a smooth dome
    pts = [(x0 - 20, y - 20), (x0 - 20, y + h * 0.30)]
    n = 7
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t,
                    y + h * (0.55 + 0.45 * math.sin(t * 4.1 + seed))))
    pts += [(x1 + 20, y + h * 0.28), (x1 + 20, y - 20)]
    blob(c, pts, fill=base, tension=0.75)
    blob(c, [(p[0], p[1] - 26) for p in pts], fill=shade(base, 0.86),
         tension=0.75)
    # the brambles themselves
    for _ in range(110):
        bx = x0 - 10 + (x1 - x0 + 20) * rnd()
        t = (bx - x0) / max(1.0, (x1 - x0))
        top = y + h * (0.55 + 0.45 * math.sin(t * 4.1 + seed))
        by = y + (top - y) * rnd()
        ln = 22 + 40 * rnd()
        ang = -1.5 + 3.0 * rnd()
        ex, ey = bx + ln * math.cos(ang), by + ln * abs(math.sin(ang)) * 1.2
        cl = shade(base, 0.62 if rnd() > 0.5 else 1.28)
        stroke_path(c, [(bx, by), ((bx + ex) / 2 + 7, (by + ey) / 2 + 4),
                        (ex, ey)], color=cl, lw=1.9)
        for tt in (0.4, 0.75):
            tx = bx + (ex - bx) * tt
            ty = by + (ey - by) * tt + 3
            poly(c, [(tx, ty), (tx + 5.5, ty + 3.5), (tx + 1, ty + 8)],
                 fill=shade(base, 0.55))
        if flowers and rnd() > 0.7:
            for k in range(5):
                a = k * 2 * math.pi / 5
                circle(c, ex + 3.6 * math.cos(a), ey + 3.6 * math.sin(a), 3.0,
                       fill="#F3B8C6")
            circle(c, ex, ey, 2.2, fill="#D6455C")


def spinning_wheel(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 2, 46, 10, alpha=0.14)
    for dx in (-30, 26):
        taper(c, [(dx, 30), (dx + dx * 0.2, 4)], 4.5, 3.5, fill="wood_dk")
    rect(c, -40, 26, 78, 9, fill="wood", r=3, stroke=LINE, lw=1.4)
    taper(c, [(-26, 32), (-24, 70), (-22, 104)], 4.5, 3.5, fill="wood_dk",
          stroke=LINE, lw=1.2)
    circle(c, -22, 104, 34, fill=None, stroke=LINE, lw=3.0)
    circle(c, -22, 104, 31, fill=None, stroke="wood", lw=4.5)
    for i in range(12):
        a = i * math.pi / 6
        stroke_path(c, [(-22, 104), (-22 + 30 * math.cos(a),
                                     104 + 30 * math.sin(a))],
                    color="wood", lw=2.0)
    circle(c, -22, 104, 5, fill="wood_dk", stroke=LINE, lw=1.2)
    taper(c, [(30, 32), (32, 62), (33, 88)], 4.0, 3.0, fill="wood_dk",
          stroke=LINE, lw=1.2)
    _ol(c, [(28, 88), (40, 92), (44, 78), (32, 74)], "wheat", tension=0.85)
    stroke_path(c, [(-22, 104), (16, 96), (33, 90)], color="#E8DCC0", lw=1.6)
    # the spindle, pointed and gleaming
    taper(c, [(33, 90), (46, 100), (56, 108)], 3.0, 0.8, fill="steel",
          stroke=LINE, lw=1.0)
    sparkle(c, 58, 110, 6, color="#FFF6DA")
    c.restoreState()


def rose_bell(c, x, y, s=1.0, petals="rose", falling=1):
    """The enchanted rose under its glass."""
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    _ol(c, [(-30, 0), (-33, 8), (33, 8), (30, 0)], "wood_dk", tension=0.5)
    taper(c, [(0, 8), (-2, 40), (0, 62)], 3.0, 2.4, fill="vine_dk")
    for sx in (-1, 1):
        _ol(c, [(0, 34), (sx * 16, 44), (sx * 22, 36), (sx * 10, 28)],
            "vine", tension=0.9)
    for i in range(7):
        a = i * 2 * math.pi / 7
        ellipse(c, 9 * math.cos(a), 72 + 9 * math.sin(a), 11, 9,
                fill=petals, stroke=LINE, lw=1.2)
    circle(c, 0, 72, 8, fill=shade(P.get(petals, petals), 0.8), stroke=LINE,
           lw=1.2)
    for i in range(falling):
        _ol(c, [(22 + i * 12, 12 + i * 7), (32 + i * 12, 18 + i * 7),
                (36 + i * 12, 10 + i * 7), (26 + i * 12, 6 + i * 7)],
            shade(P.get(petals, petals), 0.85), tension=0.9)
    # glass dome
    c.setStrokeColor(col("#FFFFFF"))
    c.setLineWidth(2.6)
    p = c.beginPath()
    p.moveTo(-36, 6)
    p.curveTo(-40, 76, -22, 108, 0, 108)
    p.curveTo(22, 108, 40, 76, 36, 6)
    c.drawPath(p, stroke=1, fill=0)
    blob(c, [(-36, 6), (-40, 76), (-22, 108), (0, 108), (22, 108), (40, 76),
             (36, 6)], fill="#CFE7F3", alpha=0.22, tension=0.9)
    stroke_path(c, [(-22, 22), (-28, 62), (-16, 90)], color="#FFFFFF", lw=3.0,
                alpha=0.75)
    circle(c, 0, 112, 5, fill="#DCEDF6", stroke="#FFFFFF", lw=2.0)
    c.restoreState()


def bed(c, x, y, s=1.0, quilt="cape", sheets="#F6EFE0", posts=True):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 2, 120, 16, alpha=0.14)
    if posts:
        for dx in (-108, 104):
            rect(c, dx, 0, 14, 118, fill="wood_dk", r=4, stroke=LINE, lw=1.5)
            circle(c, dx + 7, 122, 9, fill="wood", stroke=LINE, lw=1.4)
    _ol(c, [(-110, 34), (-114, 84), (-96, 92), (-92, 34)], "wood",
        tension=0.6)
    rect(c, -104, 20, 200, 26, fill=sheets, r=6, stroke=LINE, lw=1.5)
    _ol(c, [(-104, 46), (-40, 56), (40, 52), (96, 44), (96, 22), (-104, 22)],
        quilt, tension=0.85)
    for i in range(5):
        stroke_path(c, [(-84 + i * 40, 24), (-84 + i * 40, 52)],
                    color=shade(P.get(quilt, quilt), 0.85), lw=1.6)
    _ol(c, [(-96, 62), (-58, 70), (-40, 58), (-70, 48), (-94, 50)],
        sheets, tension=0.85)
    c.restoreState()


def basket(c, x, y, s=1.0, cloth="#E8D9C0", weave="#C9A15E"):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    _ol(c, [(-20, 0), (-24, 24), (24, 24), (20, 0)], weave, tension=0.5)
    for i in range(4):
        stroke_path(c, [(-23 + i * 0.6, 5 + i * 5), (23 - i * 0.6, 5 + i * 5)],
                    color=shade(weave, 0.8), lw=1.6)
    for dx in (-12, 0, 12):
        stroke_path(c, [(dx, 1), (dx, 23)], color=shade(weave, 0.8), lw=1.6)
    _ol(c, [(-20, 30), (0, 26), (20, 30), (20, 22), (0, 18), (-20, 22)],
        shade(weave, 0.85), tension=0.6)
    c.setStrokeColor(col(weave))
    c.setLineWidth(3.4)
    p = c.beginPath()
    p.moveTo(-16, 26)
    p.curveTo(-14, 54, 14, 54, 16, 26)
    c.drawPath(p, stroke=1, fill=0)
    _ol(c, [(-17, 28), (-6, 36), (8, 34), (18, 26), (0, 22)], cloth,
        tension=0.9)
    c.restoreState()


def harp(c, x, y, s=1.0, gold_="gold", face=True):
    """A small frame harp: soundbox, pillar, curved neck and strings."""
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 4, 2, 34, 9, alpha=0.14)
    dark = shade(P.get(gold_, gold_), 0.78)
    # soundbox, leaning back to the left
    _ol(c, [(4, 6), (20, 8), (-8, 92), (-22, 86)], gold_, tension=0.4)
    # front pillar
    taper(c, [(30, 8), (27, 54), (22, 96)], 5.5, 4.2, fill=gold_,
          stroke=LINE, lw=1.4)
    # curved neck joining the two
    taper(c, [(22, 98), (4, 108), (-14, 96)], 5.0, 4.2, fill=gold_,
          stroke=LINE, lw=1.4)
    # strings
    for i in range(8):
        t = i / 7.0
        bx, by = -20 + t * 22, 84 - t * 62
        tx, ty = -12 + t * 32, 97 + 8 * math.sin(t * 3.0)
        stroke_path(c, [(bx, by), (tx, ty)], color="#F6E7B8", lw=1.2)
    # foot
    _ol(c, [(-4, 10), (36, 10), (34, 0), (-2, 0)], dark, tension=0.4)
    circle(c, 22, 100, 4.5, fill=dark, stroke=LINE, lw=1.2)
    if face:
        for dx in (-8, -1):
            circle(c, dx, 52, 1.8, fill="ink")
        stroke_path(c, [(-10, 44), (-4, 41), (2, 44)], color="ink", lw=1.4)
    c.restoreState()


def hen(c, x, y, s=1.0, egg=True, body="#F2EDE4"):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 2, 22, 6, alpha=0.13)
    for dx in (-5, 6):
        taper(c, [(dx, 12), (dx, 3)], 2.0, 1.6, fill="gold_dk")
        stroke_path(c, [(dx - 3, 2), (dx + 4, 2)], color="gold_dk", lw=1.6)
    _ol(c, [(0, 30), (18, 22), (20, 10), (2, 4), (-16, 10), (-18, 24)], body)
    taper(c, [(-16, 26), (-30, 34), (-34, 24)], 7, 3, fill=shade(body, 0.9),
          stroke=LINE, lw=1.2)
    circle(c, 15, 34, 9, fill=body, stroke=LINE, lw=1.3)
    _ol(c, [(10, 42), (14, 50), (18, 42), (22, 48), (24, 40)], "#C0392B",
        tension=0.8)
    poly(c, [(23, 34), (32, 31), (23, 28)], fill="gold_dk", stroke=LINE, lw=1.0)
    circle(c, 19, 36, 1.8, fill="ink")
    _ol(c, [(19, 28), (24, 24), (18, 22)], "#C0392B", tension=0.8)
    if egg:
        _ol(c, [(-26, 2), (-32, 12), (-26, 20), (-18, 12), (-20, 2)],
            "gold", tension=0.95)
        sparkle(c, -30, 18, 5, color="#FFF6DA")
    c.restoreState()


def pagoda(c, x, y, s=1.0, wall="#E6D7BC", roof="cn_red", tiers=3):
    """A tiled-roof hall for the Mulan pages."""
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    for t in range(tiers):
        w = 108 - t * 24
        yy = t * 62
        rect(c, -w, yy, w * 2, 46, fill=wall, stroke=LINE, lw=1.5)
        for i in range(int(w / 22)):
            rect(c, -w + 10 + i * 24, yy + 8, 14, 26, fill="#8A5C36",
                 stroke=LINE, lw=1.1, r=2)
        _ol(c, [(-w - 26, yy + 46), (-w * 0.5, yy + 62), (0, yy + 66),
                (w * 0.5, yy + 62), (w + 26, yy + 46), (w + 14, yy + 40),
                (0, yy + 52), (-w - 14, yy + 40)], roof, tension=0.75)
        for i in range(9):
            stroke_path(c, [(-w + i * (w / 4.2), yy + 47),
                            (-w * 0.6 + i * (w / 5.2), yy + 60)],
                        color=shade(P.get(roof, roof), 0.78), lw=1.5)
    circle(c, 0, tiers * 62 + 12, 7, fill="cn_gold", stroke=LINE, lw=1.3)
    c.restoreState()


def cn_banner(c, x, y, w=44, h=150, color="cn_red", glyph=True):
    _ol(c, [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h),
            (x, y - h + 16), (x - w / 2, y - h)], color, tension=0.4)
    if glyph:
        for i in range(3):
            rect(c, x - 9, y - 40 - i * 34, 18, 4, fill="cn_gold", r=1.5)
            rect(c, x - 2, y - 52 - i * 34, 4, 26, fill="cn_gold", r=1.5)


def tent(c, x, y, s=1.0, cloth="#D8CBAE"):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    _ol(c, [(-58, 0), (-40, 70), (0, 92), (40, 70), (58, 0)], cloth,
        tension=0.75)
    _ol(c, [(-16, 0), (-12, 44), (0, 54), (12, 44), (16, 0)],
        shade(cloth, 0.72), tension=0.8)
    stroke_path(c, [(0, 92), (0, 104)], color="wood_dk", lw=2.4)
    poly(c, [(0, 104), (24, 99), (0, 94)], fill="cn_red", stroke=LINE, lw=1.1)
    c.restoreState()


def campfire(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    for k, cl in ((1.0, "#5B4A3F"), (0.7, "#7A6555")):
        for a in (-28, 0, 28):
            c.saveState()
            c.rotate(a)
            rect(c, -26 * k, -3, 52 * k, 6, fill=cl, r=3, stroke=LINE, lw=1.1)
            c.restoreState()
    for rr, cl in ((26, "#C0392B"), (18, "#E8862F"), (10, "#F6C453")):
        blob(c, [(0, 8 + rr * 2.0), (rr * 0.7, 8 + rr * 0.6), (rr * 0.45, 8),
                 (-rr * 0.45, 8), (-rr * 0.7, 8 + rr * 0.6)], fill=cl,
             tension=0.75)
    for i, (sx, sy) in enumerate(((-16, 66), (12, 78), (-4, 92))):
        sparkle(c, sx, sy, 4 + i, color="#F6C453", alpha=0.8)
    c.restoreState()


def loom(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 2, 60, 11, alpha=0.13)
    for dx in (-54, 48):
        rect(c, dx, 0, 12, 132, fill="wood_dk", r=3, stroke=LINE, lw=1.5)
    rect(c, -58, 126, 120, 12, fill="wood", r=3, stroke=LINE, lw=1.5)
    rect(c, -58, 30, 120, 10, fill="wood", r=3, stroke=LINE, lw=1.5)
    for i in range(13):
        stroke_path(c, [(-48 + i * 8, 40), (-48 + i * 8, 126)],
                    color="#E8DCC0", lw=1.5)
    _ol(c, [(-50, 40), (50, 40), (50, 76), (-50, 76)], "cn_jade", tension=0.3)
    for i in range(4):
        stroke_path(c, [(-50, 46 + i * 8), (50, 46 + i * 8)],
                    color=shade("#4E9E8F", 0.85), lw=1.6)
    c.restoreState()


def mirror(c, x, y, s=1.0, frame="gold", glass="#CFE7F3"):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    _ol(c, [(0, 96), (34, 74), (38, 32), (22, 4), (-22, 4), (-38, 32),
            (-34, 74)], frame, tension=0.9)
    _ol(c, [(0, 86), (26, 68), (29, 34), (16, 14), (-16, 14), (-29, 34),
            (-26, 68)], glass, tension=0.9)
    stroke_path(c, [(-14, 66), (-20, 40), (-10, 22)], color="#FFFFFF", lw=3.4,
                alpha=0.75)
    circle(c, 0, 100, 6, fill=shade(P.get(frame, frame), 0.85), stroke=LINE,
           lw=1.2)
    c.restoreState()


def table(c, x, y, s=1.0, top="wood", legs="wood_dk", w=110):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 2, w * 0.9, 10, alpha=0.13)
    for dx in (-w + 12, w - 22):
        rect(c, dx, 0, 12, 54, fill=legs, stroke=LINE, lw=1.3)
    rect(c, -w, 52, w * 2, 13, fill=top, r=4, stroke=LINE, lw=1.5)
    c.restoreState()


def axe(c, x, y, s=1.0, rot=0.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    c.rotate(rot)
    taper(c, [(0, 0), (28, 26), (54, 52)], 4.2, 3.4, fill="wood",
          stroke=LINE, lw=1.3)
    _ol(c, [(50, 48), (72, 62), (80, 48), (72, 34), (52, 42)], "steel",
        tension=0.85)
    _ol(c, [(50, 48), (60, 54), (60, 42)], "steel_dk", tension=0.7)
    c.restoreState()


def bean_pile(c, x, y, s=1.0, n=5, color="#7FA85E"):
    for i in range(n):
        a = i * 2.4
        _ol(c, [(x + 11 * math.cos(a) * s, y + 6 * math.sin(a) * s + 4 * s),
                (x + 11 * math.cos(a) * s + 7 * s,
                 y + 6 * math.sin(a) * s + 9 * s),
                (x + 11 * math.cos(a) * s + 13 * s,
                 y + 6 * math.sin(a) * s + 4 * s),
                (x + 11 * math.cos(a) * s + 7 * s,
                 y + 6 * math.sin(a) * s)], color, tension=0.95, lw=1.1)


def gold_bag(c, x, y, s=1.0, sack="#D9C89E", spill=True):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 2, 26, 7, alpha=0.13)
    _ol(c, [(0, 4), (24, 10), (28, 40), (0, 54), (-28, 40), (-24, 10)],
        sack, tension=0.9)
    blob(c, [(-12, 16), (-4, 26), (-14, 34)], fill=shade(sack, 0.9),
         tension=0.8)
    stroke_path(c, [(-14, 44), (0, 39), (14, 44)], color="belt", lw=3.4)
    _ol(c, [(-11, 46), (0, 58), (11, 46), (0, 49)], sack, tension=0.8)
    if spill:
        for dx, dy in ((-32, 2), (-22, 0), (30, 1), (22, 4), (38, 6)):
            circle(c, dx, dy + 4, 5.5, fill="gold", stroke=LINE, lw=1.1)
            circle(c, dx, dy + 4, 2.4, fill="gold_dk")
    c.restoreState()


def hearth_glow(c, x, y, r=150):
    for k, al in ((1.0, 0.10), (0.72, 0.10), (0.45, 0.12)):
        circle(c, x, y, r * k, fill="#F6C453", alpha=al)
