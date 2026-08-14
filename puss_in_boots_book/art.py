"""
Vector illustration toolkit for the Puss in Boots picture book.

Everything here is drawn with plain reportlab paths -- no external images --
so the book is fully reproducible from source and prints crisply at any size.

Character helpers (`puss`, `person`, `ogre`) work in a local unit space where
the figure stands on y=0 and is roughly 120 units tall. Scenes place them with
`draw_puss(c, x, y, s=...)`, where `s` scales units to points.
"""

import math

from reportlab.lib.colors import HexColor

# --------------------------------------------------------------- palette ---

P = {
    # skies & grounds
    "sky_day":     "#BFE1F0",
    "sky_soft":    "#D9EEF7",
    "sky_warm":    "#FBD9A8",
    "sky_dusk":    "#F2B98C",
    "sky_night":   "#2E3A66",
    "cloud":       "#FFFFFF",
    "grass":       "#8CC26B",
    "grass_dk":    "#67A64E",
    "grass_lt":    "#A8D585",
    "wheat":       "#E9C46A",
    "wheat_dk":    "#D4A843",
    "path":        "#E3CBA4",
    "water":       "#78C0DC",
    "water_dk":    "#4E9FC4",
    # interiors
    "cream":       "#FDF6E7",
    "parchment":   "#F7EAD0",
    "wood":        "#B07B4F",
    "wood_dk":     "#8A5C36",
    "stone":       "#CFC6B8",
    "stone_dk":    "#AFA396",
    # the cat
    "fur":         "#E89A4C",
    "fur_dk":      "#CE7A32",
    "fur_lt":      "#F6C88E",
    "belly":       "#FBE6C8",
    "boot":        "#C4432F",
    "boot_dk":     "#9E3122",
    "hat":         "#4B3A6E",
    "hat_dk":      "#3A2C57",
    "feather":     "#F4E3B2",
    "cape":        "#B23A48",
    "cape_dk":     "#8E2B37",
    "belt":        "#7A4B2A",
    "gold":        "#E9B949",
    "gold_dk":     "#C99A2E",
    # people
    "skin":        "#F0C49B",
    "skin_dk":     "#D9A578",
    "hair_brown":  "#7A4B2A",
    "hair_grey":   "#D8D2C8",
    "hair_gold":   "#E8C46A",
    "jack_old":    "#9C8E7A",
    "jack_new":    "#4E7FBF",
    "king_robe":   "#7B3F8F",
    "king_trim":   "#F3EDE2",
    "princess":    "#E9A0BC",
    "ogre_skin":   "#7FA05A",
    "ogre_dk":     "#63823F",
    "ogre_cloth":  "#6B4A7A",
    # ink & shadow
    "ink":         "#3B2E2A",
    "ink_line":    "#4A3226",
    "ink_soft":    "#6B5A52",
    "shadow":      "#00000018",
    "shadow_hard": "#00000026",
}


def col(name_or_hex, alpha=None):
    """Look up a palette name (or pass a raw #hex) and return a reportlab color."""
    h = P.get(name_or_hex, name_or_hex)
    c = HexColor(h, hasAlpha=len(h) == 9)
    if alpha is not None:
        c = HexColor(h[:7], hasAlpha=False)
        c.alpha = alpha
    return c


def paint(c, fill=None, stroke=None, lw=1.6, alpha=None):
    """Set fill/stroke state; returns (do_fill, do_stroke) for path drawing."""
    if fill is not None:
        c.setFillColor(col(fill, alpha))
    if stroke is not None:
        c.setStrokeColor(col(stroke))
        c.setLineWidth(lw)
    return fill is not None, stroke is not None


# ------------------------------------------------------------ primitives ---

def ellipse(c, cx, cy, rx, ry, fill=None, stroke=None, lw=1.6, alpha=None):
    f, s = paint(c, fill, stroke, lw, alpha)
    c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, stroke=s, fill=f)


def circle(c, cx, cy, r, **kw):
    ellipse(c, cx, cy, r, r, **kw)


def rect(c, x, y, w, h, fill=None, stroke=None, lw=1.6, alpha=None, r=None):
    f, s = paint(c, fill, stroke, lw, alpha)
    if r:
        c.roundRect(x, y, w, h, r, stroke=s, fill=f)
    else:
        c.rect(x, y, w, h, stroke=s, fill=f)


def poly(c, pts, fill=None, stroke=None, lw=1.6, alpha=None, close=True):
    f, s = paint(c, fill, stroke, lw, alpha)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    if close:
        p.close()
    c.drawPath(p, stroke=s, fill=f)


def _catmull(pts, closed, tension=1.0):
    """Convert a point list into cubic bezier segments (Catmull-Rom)."""
    n = len(pts)
    if closed:
        idx = lambda i: pts[i % n]
        rng = range(n)
    else:
        ext = [pts[0]] + list(pts) + [pts[-1]]
        idx = lambda i: ext[max(0, min(len(ext) - 1, i + 1))]
        rng = range(n - 1)
    segs = []
    for i in rng:
        p0, p1, p2, p3 = idx(i - 1), idx(i), idx(i + 1), idx(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0 * tension,
              p1[1] + (p2[1] - p0[1]) / 6.0 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0 * tension,
              p2[1] - (p3[1] - p1[1]) / 6.0 * tension)
        segs.append((c1, c2, p2))
    return segs


def blob(c, pts, fill=None, stroke=None, lw=1.6, alpha=None,
         closed=True, tension=1.0):
    """Smooth organic shape through `pts`. The workhorse of this whole book."""
    f, s = paint(c, fill, stroke, lw, alpha)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for c1, c2, end in _catmull(pts, closed, tension):
        p.curveTo(c1[0], c1[1], c2[0], c2[1], end[0], end[1])
    if closed:
        p.close()
    c.drawPath(p, stroke=s, fill=f)


def stroke_path(c, pts, color="ink", lw=2.0, tension=1.0, cap=1, alpha=None):
    """Smooth open line (whiskers, ropes, motion lines...)."""
    c.saveState()
    c.setLineCap(cap)
    c.setStrokeColor(col(color, alpha))
    c.setLineWidth(lw)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for c1, c2, end in _catmull(pts, False, tension):
        p.curveTo(c1[0], c1[1], c2[0], c2[1], end[0], end[1])
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def taper(c, pts, w0, w1, fill="fur", stroke=None, lw=1.4):
    """A limb/tail: a smooth spine swept with a width that tapers w0 -> w1."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        t = i / (n - 1)
        w = w0 + (w1 - w0) * t
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - pts[-2][0], y - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        m = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / m * w, dx / m * w
        left.append((x + nx, y + ny))
        right.append((x - nx, y - ny))
    blob(c, left + right[::-1], fill=fill, stroke=stroke, lw=lw, tension=0.6)


def shadow(c, cx, cy, rx, ry=None, alpha=0.13):
    """Soft contact shadow under a figure or object."""
    ellipse(c, cx, cy, rx, ry if ry is not None else rx * 0.26,
            fill="#000000", alpha=alpha)


def star(c, cx, cy, r, points=5, fill="gold", inner=0.45, rot=0.0):
    pts = []
    for i in range(points * 2):
        a = rot + math.pi / 2 + i * math.pi / points
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(c, pts, fill=fill)


def sparkle(c, cx, cy, r, color="#FFFFFF", alpha=0.9):
    poly(c, [(cx, cy + r), (cx + r * 0.22, cy + r * 0.22), (cx + r, cy),
             (cx + r * 0.22, cy - r * 0.22), (cx, cy - r),
             (cx - r * 0.22, cy - r * 0.22), (cx - r, cy),
             (cx - r * 0.22, cy + r * 0.22)], fill=color, alpha=alpha)


# ------------------------------------------------------------ background ---

def sky(c, x, y, w, h, top="sky_day", bottom="sky_soft", bands=64):
    """Vertical gradient wash."""
    ct, cb = col(top), col(bottom)
    for i in range(bands):
        t = i / (bands - 1)
        c.setFillColorRGB(ct.red + (cb.red - ct.red) * t,
                          ct.green + (cb.green - ct.green) * t,
                          ct.blue + (cb.blue - ct.blue) * t)
        c.rect(x, y + h - h * (i + 1) / bands, w, h / bands + 0.7,
               stroke=0, fill=1)


def sun(c, cx, cy, r=34, color="#FFF0B8", glow="#FFE79A"):
    for i, k in enumerate((2.5, 1.9, 1.4)):
        circle(c, cx, cy, r * k, fill=glow, alpha=0.10 + 0.05 * i)
    circle(c, cx, cy, r, fill=color)


def cloud(c, cx, cy, s=1.0, fill="cloud", alpha=0.95):
    for dx, dy, rr in ((-26, -2, 17), (-6, 6, 23), (18, 0, 18), (34, -6, 13)):
        ellipse(c, cx + dx * s, cy + dy * s, rr * s, rr * s * 0.82,
                fill=fill, alpha=alpha)
    rect(c, cx - 40 * s, cy - 12 * s, 82 * s, 13 * s, fill=fill, alpha=alpha)


def hills(c, x, y, w, base_h, color="grass_dk", bumps=3, seedoff=0.0, alpha=None):
    pts = [(x - 10, y - 6)]
    for i in range(bumps + 1):
        t = i / bumps
        px = x + w * t
        py = y + base_h * (0.55 + 0.45 * math.sin(seedoff + t * 3.1))
        pts.append((px, py))
    pts.append((x + w + 10, y - 6))
    blob(c, pts, fill=color, alpha=alpha, tension=0.9)


def ground(c, x, y, w, h, color="grass", top_color=None):
    rect(c, x, y, w, h, fill=color)
    if top_color:
        blob(c, [(x - 5, y + h - 14), (x + w * 0.25, y + h - 4),
                 (x + w * 0.55, y + h - 16), (x + w * 0.8, y + h - 5),
                 (x + w + 5, y + h - 12), (x + w + 5, y - 5), (x - 5, y - 5)],
             fill=top_color, tension=0.8)


def grass_tufts(c, x0, x1, y, n=14, color="grass_dk", h=9, seed=1):
    rnd = _rng(seed)
    for _ in range(n):
        gx = x0 + (x1 - x0) * rnd()
        gh = h * (0.6 + rnd())
        for k in (-1, 0, 1):
            stroke_path(c, [(gx + k * 2.4, y),
                            (gx + k * 4.5, y + gh * 0.6),
                            (gx + k * 6.5, y + gh)],
                        color=color, lw=1.7)


def tree(c, x, y, s=1.0, trunk="wood_dk", leaf="grass_dk", leaf2="grass"):
    taper(c, [(x, y), (x - 2 * s, y + 30 * s), (x + 1 * s, y + 58 * s)],
          7 * s, 4.5 * s, fill=trunk)
    for dx, dy, rr, cl in ((-20, 66, 24, leaf), (18, 62, 21, leaf),
                           (0, 84, 27, leaf2), (-8, 60, 20, leaf2)):
        ellipse(c, x + dx * s, y + dy * s, rr * s, rr * s * 0.9, fill=cl)


def bush(c, x, y, s=1.0, color="grass_dk"):
    for dx, dy, rr in ((-14, 2, 14), (0, 8, 17), (15, 1, 13)):
        ellipse(c, x + dx * s, y + dy * s, rr * s, rr * s * 0.85, fill=color)


def flower(c, x, y, s=1.0, petal="#FFFFFF", eye="gold"):
    stroke_path(c, [(x, y), (x + 1 * s, y + 7 * s)], color="grass_dk", lw=1.6 * s)
    for i in range(5):
        a = i * 2 * math.pi / 5
        circle(c, x + 3.4 * s * math.cos(a), y + 9 * s + 3.4 * s * math.sin(a),
               2.6 * s, fill=petal)
    circle(c, x, y + 9 * s, 1.9 * s, fill=eye)


def _rng(seed):
    """Tiny deterministic RNG so every build of the book is identical."""
    state = [seed * 7919 + 13]

    def nxt():
        state[0] = (1103515245 * state[0] + 12345) % 2147483648
        return state[0] / 2147483648.0
    return nxt

# ------------------------------------------------------------------ Puss ---
#
# Local unit space: feet on y=0, figure centred on x=0, ~140 units to the
# ear tips. Everything is outlined in a warm brown so the art keeps its shape
# when printed on a home inkjet.

LINE = "ink_line"
LW = 1.7


def shade(hex_or_name, k=0.82):
    """Darken (k<1) or lighten (k>1) a palette colour."""
    h = P.get(hex_or_name, hex_or_name)
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    f = lambda v: max(0, min(255, int(v * k if k < 1 else v + (255 - v) * (k - 1))))
    return "#%02X%02X%02X" % (f(r), f(g), f(b))


def _ol(c, pts, fill, lw=LW, tension=1.0):
    """Filled + outlined smooth shape -- the house style for characters."""
    blob(c, pts, fill=fill, stroke=LINE, lw=lw, tension=tension)


def _cat_hat(c):
    """Wide musketeer hat: swept brim, soft crown, one proud feather."""
    c.saveState()
    c.translate(0, 21)
    c.rotate(-7)
    # feather (behind the crown)
    blob(c, [(2, 6), (16, 22), (34, 32), (50, 27), (44, 14), (26, 7), (12, 2)],
         fill="feather", stroke=LINE, lw=1.4, tension=0.85)
    stroke_path(c, [(4, 6), (22, 17), (46, 23)], color=shade("feather", 0.78),
                lw=1.5)
    # crown
    _ol(c, [(-16, 2), (-13, 16), (0, 22), (13, 15), (16, 1), (0, 6)],
        "hat", tension=0.9)
    # brim, with an upturn on the left
    _ol(c, [(-29, 5), (-25, 11), (-12, 5), (0, 6), (16, 4), (28, -2),
            (14, -6), (0, -7), (-14, -5)], "hat_dk", tension=0.85)
    # band
    blob(c, [(-16, 3), (0, 7), (16, 2), (16, -1), (0, 4), (-16, 0)],
         fill="gold_dk", tension=0.6)
    circle(c, 11, 4, 3.0, fill="gold", stroke=LINE, lw=1.2)
    c.restoreState()


def _cat_head(c, expr="happy", hat=True, tilt=0.0):
    """Head assembly. Local origin sits at the base of the neck."""
    c.saveState()
    c.translate(0, 90)
    c.rotate(tilt)


    # skull
    _ol(c, [(0, 21), (17, 16), (21, 0), (14, -16), (0, -20),
            (-14, -16), (-21, 0), (-17, 16)], "fur")
    # cheek fluff
    for sx in (-1, 1):
        blob(c, [(sx * 13, -6), (sx * 22, -10), (sx * 17, -17), (sx * 9, -15)],
             fill="fur_lt", tension=0.7)
    # forehead tabby marks
    for dx, hh in ((-6, 6), (0, 7.5), (6, 6)):
        stroke_path(c, [(dx, 10), (dx * 1.2, 10 + hh)], color="fur_dk", lw=2.4)

    # muzzle
    blob(c, [(0, -3), (11, -5), (13, -12), (6, -17), (0, -15), (-6, -17),
             (-13, -12), (-11, -5)], fill="belly", tension=0.85)

    # eyes
    if expr in ("closed", "sleep"):
        for sx in (-1, 1):
            stroke_path(c, [(sx * 3.5, 3), (sx * 8, 6), (sx * 12.5, 3)],
                        color="ink", lw=2.0)
    else:
        look = {"sly": (1.2, -0.4), "scheme": (1.4, 0.0), "proud": (0, 0.9),
                "sad": (0, -1.0), "brave": (0, 0.4), "aside": (-1.6, -0.2)
                }.get(expr, (0, 0))
        ew, eh = (7.0, 8.2) if expr == "surprised" else (6.0, 7.0)
        for sx in (-1, 1):
            if expr == "wink" and sx == 1:
                stroke_path(c, [(4, 3), (8, 6.4), (12.5, 3)], color="ink", lw=2.0)
                continue
            ellipse(c, sx * 8.5, 2, ew, eh, fill="#FFFFFF", stroke=LINE, lw=1.2)
            ellipse(c, sx * 8.5 + look[0], 2 + look[1], 3.6, 5.0, fill="#3F8F5E")
            ellipse(c, sx * 8.5 + look[0], 1.6 + look[1], 2.2, 3.9, fill="ink")
            circle(c, sx * 8.5 + look[0] - 1.9, 4.4 + look[1], 1.7, fill="#FFFFFF")
            circle(c, sx * 8.5 + look[0] + 1.7, -0.4 + look[1], 0.9,
                   fill="#FFFFFF", alpha=0.85)
            if expr in ("sly", "scheme"):   # half-closed schemer lids
                blob(c, [(sx * 8.5 - ew - 0.6, 2.5), (sx * 8.5, 6.5),
                         (sx * 8.5 + ew + 0.6, 2.0), (sx * 8.5 + ew + 0.6, eh + 4),
                         (sx * 8.5 - ew - 0.6, eh + 4)], fill="fur", tension=0.6)
                stroke_path(c, [(sx * 8.5 - ew, 2.6), (sx * 8.5, 6.4),
                                (sx * 8.5 + ew, 2.1)], color=LINE, lw=1.5)
        if expr == "sad":
            for sx in (-1, 1):
                stroke_path(c, [(sx * 3, 12), (sx * 8, 10), (sx * 13, 11.5)],
                            color="ink_soft", lw=1.7)
        if expr == "surprised":
            for sx in (-1, 1):
                stroke_path(c, [(sx * 4, 13), (sx * 9, 15), (sx * 14, 13)],
                            color="ink_soft", lw=1.7)

    # nose & mouth
    poly(c, [(0, -4.5), (3.4, -0.6), (-3.4, -0.6)], fill="#D9727A", stroke=LINE,
         lw=1.1)
    if expr == "surprised":
        ellipse(c, 0, -10, 3.6, 4.6, fill="#8E3B3F")
    elif expr == "sad":
        stroke_path(c, [(-5, -11), (0, -8), (5, -11)], color="ink", lw=1.8)
    else:
        stroke_path(c, [(0, -4.5), (0, -7.5)], color="ink", lw=1.8)
        stroke_path(c, [(-6.5, -6.5), (-3.4, -10.2), (0, -8.0)], color="ink", lw=1.9)
        stroke_path(c, [(0, -8.0), (3.4, -10.2), (6.5, -6.5)], color="ink", lw=1.9)

    # whiskers
    for sx in (-1, 1):
        for dy, dr in ((-7, 3.0), (-10.5, 0.0)):
            stroke_path(c, [(sx * 12, dy), (sx * 20, dy + dr),
                            (sx * 28, dy + dr * 1.8)], color="ink_soft", lw=1.2)

    if hat:
        _cat_hat(c)

    # ears last, so the hat never swallows them
    for sx in (-1, 1):
        _ol(c, [(sx * 8, 13), (sx * 14, 31), (sx * 22, 12), (sx * 16, 6)],
            "fur", tension=0.45)
        blob(c, [(sx * 12, 13), (sx * 15, 24), (sx * 19, 12)],
             fill="#F2AE93", tension=0.45)
    c.restoreState()


def _boot(c, x, y, rot=0.0):
    """Red leather boot with a turned-down cuff, toe pointing +x."""
    c.saveState()
    c.translate(x, y)
    c.rotate(rot)
    _ol(c, [(-7.5, 4), (-8.5, 20), (7.5, 21), (6.5, 4)], "boot", tension=0.5)
    _ol(c, [(-9.5, 0), (-10.5, 7), (8, 8), (15, 5), (14, 0), (0, -2)],
        "boot", tension=0.5)
    _ol(c, [(-11, 17), (-12.5, 30), (11, 31), (10, 16)], "boot_dk", tension=0.5)
    rect(c, -10, 3.5, 18, 4.2, fill="gold_dk", r=1.8, stroke=LINE, lw=1.1)
    blob(c, [(-5, 9), (-1, 18), (3, 9)], fill="#FFFFFF", alpha=0.16, tension=0.7)
    c.restoreState()


def _sack(c, sx, sy, size=1.0, bulge=True, color="parchment"):
    c.saveState()
    c.translate(sx, sy)
    c.scale(size, size)
    if bulge:
        _ol(c, [(0, 0), (17, -9), (19, -30), (0, -41), (-19, -30), (-17, -9)],
            color)
        blob(c, [(-9, -15), (-2, -22), (-10, -28)], fill=shade(color, 0.92),
             tension=0.7)
    else:
        _ol(c, [(0, 0), (9, -9), (10, -26), (0, -32), (-10, -26), (-9, -9)],
            color)
    stroke_path(c, [(-9, -2), (0, -7), (9, -2)], color="belt", lw=3.2)
    _ol(c, [(-7, 1), (0, 9), (7, 1), (0, 3)], color, tension=0.7)
    c.restoreState()


def draw_puss(c, x, y, s=1.0, flip=False, expr="happy", hat=True,
              cape=True, boots=True, sack=None, sword=False,
              arm_l=None, arm_r=None, tail="curl", lean=0.0, tilt=0.0,
              legs="stand", shad=True):
    """
    Draw Puss in Boots.

    arm_l / arm_r : a named preset, or a list of (x, y) spine points in local
                    units measured from the shoulder. arm_l is his far arm.
    legs          : 'stand' | 'stride' | 'run' | 'sit' | 'leap' | 'bow'
    tail          : 'curl' | 'up' | 'swish' | 'down' | 'perk'
    """
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    if shad:
        shadow(c, 0, 2, 36, 9, alpha=0.14)
    c.rotate(lean)

    ARMS = {
        "down":  [(0, 0), (9, -14), (12, -28)],
        "out":   [(0, 0), (18, -6), (32, -6)],
        "up":    [(0, 0), (13, 12), (18, 28)],
        "point": [(0, 0), (20, 6), (36, 14)],
        "hip":   [(0, 0), (15, -11), (7, -22)],
        "hold":  [(0, 0), (14, -10), (24, -16)],
        "sweep": [(0, 0), (17, 4), (30, -6)],
        "chin":  [(0, 0), (14, -6), (9, 6)],
        "wave":  [(0, 0), (15, 11), (17, 28)],
        "hug":   [(0, 0), (13, -8), (4, -16)],
        "doff":  [(0, 0), (16, 8), (26, 22)],
    }
    al = ARMS.get(arm_l, arm_l) if arm_l is not None else ARMS["down"]
    ar = ARMS.get(arm_r, arm_r) if arm_r is not None else ARMS["hip"]

    # ---- tail, well clear of the body so it actually reads
    TAILS = {
        "curl":  [(-15, 38), (-33, 44), (-43, 62), (-38, 80)],
        "up":    [(-15, 38), (-31, 52), (-37, 74), (-28, 92)],
        "perk":  [(-15, 38), (-30, 56), (-25, 78), (-11, 90)],
        "swish": [(-15, 36), (-36, 32), (-55, 30), (-68, 44)],
        "down":  [(-15, 34), (-36, 24), (-53, 16)],
    }
    tp = TAILS.get(tail, TAILS["curl"])
    taper(c, tp, 6.2, 3.0, fill="fur", stroke=LINE, lw=LW)
    for i in (1, 2, 3):                      # tail rings
        if i < len(tp):
            px, py = tp[i]
            circle(c, px, py, 3.6 - i * 0.5, fill="fur_dk", alpha=0.55)
    circle(c, tp[-1][0], tp[-1][1], 3.2, fill="fur_lt", stroke=LINE, lw=1.2)

    # ---- cape, behind the body
    if cape:
        _ol(c, [(-19, 77), (-34, 63), (-32, 42), (0, 36), (32, 42),
                (34, 63), (19, 77)], "cape_dk", tension=0.85)
        blob(c, [(-13, 74), (-21, 60), (-18, 45), (7, 42), (9, 62), (3, 74)],
             fill="cape", tension=0.85)

    # ---- legs
    if legs == "run":
        legpts = [([(-8, 34), (-21, 20), (-33, 13)], -33, 13, -34),
                  ([(8, 34), (18, 18), (22, 5)], 22, 5, 20)]
    elif legs == "stride":
        legpts = [([(-8, 34), (-17, 19), (-23, 5)], -23, 5, -12),
                  ([(8, 34), (15, 19), (17, 5)], 17, 5, 7)]
    elif legs == "leap":
        legpts = [([(-8, 34), (-24, 30), (-37, 34)], -37, 34, -54),
                  ([(8, 34), (21, 25), (30, 27)], 30, 27, 32)]
    elif legs == "sit":
        legpts = [([(-9, 28), (-21, 16), (-29, 8)], -29, 8, -28),
                  ([(9, 28), (20, 15), (27, 7)], 27, 7, 24)]
    elif legs == "bow":
        legpts = [([(-9, 34), (-19, 19), (-26, 5)], -26, 5, -18),
                  ([(8, 34), (15, 19), (17, 5)], 17, 5, 5)]
    else:  # stand
        legpts = [([(-11, 34), (-15, 18), (-16, 4)], -16, 4, -4),
                  ([(11, 34), (15, 18), (16, 4)], 16, 4, 4)]
    for spine, bx, by, rot in legpts:
        taper(c, spine, 7.5, 6.0, fill="fur", stroke=LINE, lw=LW)
        if boots:
            _boot(c, bx, by, rot)
        else:
            ellipse(c, bx, by - 5, 8.5, 5.5, fill="fur_lt", stroke=LINE, lw=LW)

    # ---- far arm, behind the body
    pts = [(-px - 15, py + 63) for px, py in al]
    taper(c, pts, 5.2, 4.0, fill=shade("fur", 0.9), stroke=LINE, lw=LW)
    circle(c, pts[-1][0], pts[-1][1], 4.6, fill=shade("fur_lt", 0.92),
           stroke=LINE, lw=1.3)

    # ---- body
    _ol(c, [(0, 78), (18, 69), (22, 50), (18, 34), (0, 29),
            (-18, 34), (-22, 50), (-18, 69)], "fur")
    blob(c, [(1, 71), (11, 59), (13, 43), (6, 32), (-4, 32), (-10, 43),
             (-11, 59)], fill="belly", tension=0.9)
    for dy in (40, 50, 60):
        stroke_path(c, [(-20, dy), (-14, dy + 3), (-10, dy)],
                    color="fur_dk", lw=2.8)

    if cape:   # collar, in front
        _ol(c, [(-20, 74), (0, 68), (20, 74), (15, 80), (0, 75), (-15, 80)],
            "cape", tension=0.7)

    # ---- belt
    _ol(c, [(-19, 37), (0, 32), (19, 37), (19, 30), (0, 25), (-19, 30)],
        "belt", tension=0.6)
    rect(c, -5.5, 27, 11, 9, fill="gold", r=1.8, stroke=LINE, lw=1.2)

    if sword:
        c.saveState()
        c.translate(-20, 30)
        c.rotate(26)
        rect(c, 0, -1.8, 44, 3.6, fill="#C9CDD4", r=1.8, stroke=LINE, lw=1.1)
        rect(c, -9, -3, 10, 6, fill="belt", r=2.4, stroke=LINE, lw=1.1)
        circle(c, -10, 0, 3.6, fill="gold", stroke=LINE, lw=1.1)
        c.restoreState()

    # ---- near arm, over the body
    pts = [(px + 15, py + 63) for px, py in ar]
    taper(c, pts, 5.4, 4.2, fill="fur", stroke=LINE, lw=LW)
    circle(c, pts[-1][0], pts[-1][1], 4.8, fill="fur_lt", stroke=LINE, lw=1.3)

    _cat_head(c, expr=expr, hat=hat, tilt=tilt)

    if sack:
        _sack(c, *sack)
    c.restoreState()


# ---------------------------------------------------------------- people ---

def draw_person(c, x, y, s=1.0, flip=False, robe="jack_old", trim=None,
                hair="hair_brown", skin="skin", crown=False, hat=None,
                expr="happy", arm_l="down", arm_r="down", legs="stand",
                beard=False, long_hair=False, shad=True, wet=False,
                cloak=None):
    """A friendly storybook human, ~120 units to the crown of the head."""
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    if shad:
        shadow(c, 0, 2, 28, 7.5, alpha=0.13)

    sleeve = shade(robe, 0.86)

    ARMS = {
        "down":  [(0, 0), (9, -14), (12, -27)],
        "out":   [(0, 0), (16, -8), (28, -11)],
        "up":    [(0, 0), (11, 10), (14, 26)],
        "point": [(0, 0), (18, 3), (32, 9)],
        "hip":   [(0, 0), (12, -11), (5, -21)],
        "hold":  [(0, 0), (12, -13), (21, -18)],
        "wave":  [(0, 0), (12, 9), (13, 26)],
        "reach": [(0, 0), (18, 7), (32, 3)],
        "clasp": [(0, 0), (10, -14), (-2, -19)],
    }
    al, ar = ARMS.get(arm_l, arm_l), ARMS.get(arm_r, arm_r)

    if cloak:
        _ol(c, [(-17, 72), (-30, 44), (-27, 12), (0, 6), (27, 12), (30, 44),
                (17, 72)], cloak, tension=0.85)

    # legs
    if legs == "run":
        lp = [[(-5, 26), (-15, 17), (-24, 15)], [(5, 26), (13, 15), (16, 4)]]
    elif legs == "stride":
        lp = [[(-5, 26), (-12, 15), (-16, 5)], [(5, 26), (10, 15), (12, 4)]]
    else:
        lp = [[(-6, 26), (-7, 15), (-7, 5)], [(6, 26), (7, 15), (7, 5)]]
    for spine in lp:
        taper(c, spine, 5.6, 4.4, fill="#6B584B", stroke=LINE, lw=1.4)
        _ol(c, [(spine[-1][0] - 6, 5), (spine[-1][0] - 7, 0),
                (spine[-1][0] + 8, 0), (spine[-1][0] + 8, 5)],
            "#40342C", tension=0.4)

    # far arm
    pts = [(-px - 15, py + 62) for px, py in al]
    taper(c, pts, 5.4, 4.2, fill=shade(sleeve, 0.9), stroke=LINE, lw=1.4)
    circle(c, pts[-1][0], pts[-1][1], 4.6, fill=shade(skin, 0.93), stroke=LINE,
           lw=1.2)

    # tunic / robe -- shoulders, waist, hem
    _ol(c, [(0, 76), (16, 71), (14, 44), (24, 14), (0, 10), (-24, 14),
            (-14, 44), (-16, 71)], robe, tension=0.85)
    blob(c, [(0, 72), (7, 58), (6, 40), (9, 14), (-9, 14), (-6, 40), (-7, 58)],
         fill=shade(robe, 1.12), alpha=0.5, tension=0.85)
    if trim or crown:
        _ol(c, [(-24, 15), (0, 10), (24, 15), (22, 23), (0, 18), (-22, 23)],
            trim or "king_trim", tension=0.6)
    rect(c, -15, 38, 30, 7, fill=shade(robe, 0.72), r=3, stroke=LINE, lw=1.2)

    # near arm, over the robe
    pts = [(px + 15, py + 62) for px, py in ar]
    taper(c, pts, 5.6, 4.4, fill=sleeve, stroke=LINE, lw=1.4)
    circle(c, pts[-1][0], pts[-1][1], 4.8, fill=skin, stroke=LINE, lw=1.2)

    if wet:
        for dx in (-13, -3, 8, 17):
            stroke_path(c, [(dx, 20), (dx - 2, 12), (dx, 5)],
                        color="water_dk", lw=1.9, alpha=0.75)

    # neck + head
    rect(c, -5, 74, 10, 9, fill=shade(skin, 0.92))
    circle(c, 0, 93, 15, fill=skin, stroke=LINE, lw=LW)

    if long_hair:
        _ol(c, [(0, 110), (18, 100), (21, 72), (13, 66), (11, 88), (0, 94),
                (-11, 88), (-13, 66), (-21, 72), (-18, 100)], hair, tension=0.8)
    _ol(c, [(0, 110), (15, 101), (17, 90), (10, 97), (0, 100), (-10, 97),
            (-17, 90), (-15, 101)], hair, tension=0.75)

    # face
    for sx in (-1, 1):
        if expr == "closed":
            stroke_path(c, [(sx * 2.5, 95), (sx * 5.5, 96.8), (sx * 8.5, 95)],
                        color="ink", lw=1.6)
        else:
            circle(c, sx * 5.5, 95, 2.1, fill="ink")
            circle(c, sx * 5.5 - 0.8, 95.9, 0.9, fill="#FFFFFF")
    ellipse(c, -10, 89, 3.2, 2.1, fill="#E79A9A", alpha=0.6)
    ellipse(c, 10, 89, 3.2, 2.1, fill="#E79A9A", alpha=0.6)
    if beard:
        _ol(c, [(-12, 90), (-10, 76), (0, 70), (10, 76), (12, 90), (0, 87)],
            hair, tension=0.7)
    if expr == "sad":
        stroke_path(c, [(-4.5, 85), (0, 87.5), (4.5, 85)], color="ink", lw=1.7)
    elif expr == "surprised":
        ellipse(c, 0, 86, 3.0, 3.8, fill="#8E3B3F")
    else:
        stroke_path(c, [(-5.5, 88), (0, 84), (5.5, 88)], color="ink", lw=1.8)

    if crown:
        poly(c, [(-13, 106), (-13, 120), (-6.5, 112), (0, 122), (6.5, 112),
                 (13, 120), (13, 106)], fill="gold", stroke=LINE, lw=1.3)
        rect(c, -13.5, 103, 27, 5.5, fill="gold_dk", r=1.6, stroke=LINE, lw=1.2)
        for dx in (-7, 0, 7):
            circle(c, dx, 117, 2.1, fill="#C0392B")
    elif hat == "miller":
        _ol(c, [(-17, 107), (0, 120), (17, 107), (0, 111)], "#C9BBA4",
            tension=0.7)
    elif hat == "straw":
        _ol(c, [(-23, 105), (0, 110), (23, 105), (0, 100)], "wheat", tension=0.7)
        _ol(c, [(-11, 106), (0, 119), (11, 106)], "wheat_dk", tension=0.7)
    elif hat == "tiara":
        poly(c, [(-11, 106), (-5, 114), (0, 107), (5, 114), (11, 106)],
             fill="gold", stroke=LINE, lw=1.2)
        circle(c, 0, 110, 1.8, fill="#7FD4E8")

    c.restoreState()


def draw_ogre(c, x, y, s=1.0, flip=False, expr="grin", arm_l="out",
              arm_r="hip", shad=True):
    """A big, round, more-silly-than-scary ogre."""
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    if shad:
        shadow(c, 0, 2, 50, 13, alpha=0.16)

    ARMS = {"out":  [(0, 0), (24, -6), (42, -12)],
            "hip":  [(0, 0), (20, -16), (11, -30)],
            "up":   [(0, 0), (17, 15), (26, 34)],
            "down": [(0, 0), (11, -19), (14, -35)]}
    al, ar = ARMS.get(arm_l, arm_l), ARMS.get(arm_r, arm_r)

    for sx in (-1, 1):
        taper(c, [(sx * 13, 32), (sx * 17, 17), (sx * 18, 6)], 11, 9.5,
              fill="ogre_dk", stroke=LINE, lw=LW)
        _ol(c, [(sx * 18 - 12, 6), (sx * 18 - 13, 0), (sx * 18 + 13, 0),
                (sx * 18 + 12, 6)], "#4C3A2E", tension=0.4)

    pts = [(-px - 28, py + 70) for px, py in al]
    taper(c, pts, 10, 7.5, fill="ogre_dk", stroke=LINE, lw=LW)
    circle(c, pts[-1][0], pts[-1][1], 8.5, fill="ogre_dk", stroke=LINE, lw=1.3)

    _ol(c, [(0, 86), (34, 72), (42, 42), (34, 22), (0, 16), (-34, 22),
            (-42, 42), (-34, 72)], "ogre_cloth")
    blob(c, [(-41, 32), (0, 24), (41, 32), (39, 42), (0, 34), (-39, 42)],
         fill="#4E3459", tension=0.6)

    pts = [(px + 28, py + 70) for px, py in ar]
    taper(c, pts, 10.5, 8, fill="ogre_skin", stroke=LINE, lw=LW)
    circle(c, pts[-1][0], pts[-1][1], 9, fill="ogre_skin", stroke=LINE, lw=1.3)

    circle(c, 0, 106, 27, fill="ogre_skin", stroke=LINE, lw=LW)
    for sx in (-1, 1):
        _ol(c, [(sx * 26, 112), (sx * 34, 106), (sx * 26, 98), (sx * 22, 105)],
            "ogre_skin", tension=0.6)
    _ol(c, [(0, 131), (19, 124), (25, 113), (12, 118), (0, 120), (-12, 118),
            (-25, 113), (-19, 124)], "#3E3A2E", tension=0.75)
    for sx in (-1, 1):
        stroke_path(c, [(sx * 4, 116), (sx * 10, 118), (sx * 16, 114)],
                    color="#3E3A2E", lw=3.2)
        if expr == "surprised":
            circle(c, sx * 10, 107, 6.0, fill="#FFFFFF", stroke=LINE, lw=1.2)
            circle(c, sx * 10, 107, 3.0, fill="ink")
        else:
            ellipse(c, sx * 10, 107, 5.4, 5.0, fill="#FFFFFF", stroke=LINE, lw=1.2)
            circle(c, sx * 10, 106.6, 2.6, fill="ink")
    ellipse(c, 0, 99, 6.5, 5, fill="ogre_dk")
    if expr == "grin":
        _ol(c, [(-14, 93), (0, 83), (14, 93), (0, 90)], "#5E2B2B", tension=0.7)
        for dx in (-8, 8):
            poly(c, [(dx - 3.2, 92), (dx + 3.2, 92), (dx, 83)], fill="#FFFFFF",
                 stroke=LINE, lw=1.0)
    elif expr == "surprised":
        ellipse(c, 0, 90, 6.5, 7.5, fill="#5E2B2B", stroke=LINE, lw=1.2)
    else:
        stroke_path(c, [(-11, 91), (0, 88), (11, 91)], color="#5E2B2B", lw=2.8)
    c.restoreState()


def draw_lion(c, x, y, s=1.0, flip=False, shad=True):
    """The ogre showing off -- now a lion."""
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    if shad:
        shadow(c, 4, 2, 56, 13, alpha=0.16)
    taper(c, [(-44, 24), (-64, 32), (-72, 50), (-58, 56)], 6, 3.5,
          fill="#C98A3C", stroke=LINE, lw=1.4)
    circle(c, -60, 54, 6.5, fill="#8A5A2B", stroke=LINE, lw=1.3)
    for sx, dx in ((-1, -28), (1, 22)):
        taper(c, [(dx, 32), (dx + sx * 5, 17), (dx + sx * 7, 6)], 9.5, 7.5,
              fill="#D9A05B", stroke=LINE, lw=1.4)
        _ol(c, [(dx + sx * 7 - 10, 6), (dx + sx * 7 - 11, 0),
                (dx + sx * 7 + 11, 0), (dx + sx * 7 + 10, 6)], "#C98A3C",
            tension=0.4)
    _ol(c, [(0, 60), (30, 50), (38, 32), (26, 19), (-14, 17), (-36, 24),
            (-38, 42), (-22, 56)], "#D9A05B")
    for i in range(18):
        a = i * 2 * math.pi / 18
        ellipse(c, 30 + 27 * math.cos(a), 58 + 27 * math.sin(a), 11.5, 9.5,
                fill="#8A5A2B", stroke=LINE, lw=1.1)
    circle(c, 30, 58, 24, fill="#E3B370", stroke=LINE, lw=LW)
    for sx in (-1, 1):
        _ol(c, [(30 + sx * 17, 82), (30 + sx * 24, 76), (30 + sx * 15, 70)],
            "#C98A3C", tension=0.6)
        ellipse(c, 30 + sx * 8.5, 62, 5.0, 5.6, fill="#FFFFFF", stroke=LINE, lw=1.2)
        ellipse(c, 30 + sx * 8.5, 61, 2.6, 3.6, fill="ink")
    _ol(c, [(30, 56), (40, 52), (41, 45), (30, 41), (19, 45), (20, 52)],
        "#F3DDBE", tension=0.8)
    poly(c, [(30, 51), (34, 55), (26, 55)], fill="#8E4B4B", stroke=LINE, lw=1.1)
    _ol(c, [(18, 46), (30, 36), (42, 46), (30, 43)], "#7A2E2E", tension=0.7)
    for dx in (-5.5, 5.5):
        poly(c, [(30 + dx - 2.6, 45), (30 + dx + 2.6, 45), (30 + dx, 37)],
             fill="#FFFFFF", stroke=LINE, lw=1.0)
    for sx in (-1, 1):
        for dy in (-3, -6):
            stroke_path(c, [(30 + sx * 10, 48 + dy), (30 + sx * 20, 47 + dy)],
                        color="ink_soft", lw=1.2)
    c.restoreState()


def draw_mouse(c, x, y, s=1.0, flip=False, expr="worried"):
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    stroke_path(c, [(-10, 5), (-22, 3), (-29, 12)], color="#B9A9A0", lw=2.4)
    circle(c, -3, 15, 6.0, fill="#C4BCB6", stroke=LINE, lw=1.2)
    _ol(c, [(0, 13), (11, 9), (13, 2), (2, -1), (-10, 1), (-11, 8)], "#A9A19B")
    _ol(c, [(11, 8), (17, 11), (20, 6), (16, 1), (10, 2)], "#B9B1AB", tension=0.7)
    circle(c, 15, 8.5, 1.7, fill="ink")
    circle(c, 19.5, 4.5, 1.5, fill="#E79A9A")
    for dy in (5, 7):
        stroke_path(c, [(18, dy), (25, dy - 2)], color="ink_soft", lw=1.0)
    c.restoreState()


def draw_rabbit(c, x, y, s=1.0, flip=False):
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    for dx in (-4, 4):
        _ol(c, [(dx, 21), (dx + 3, 36), (dx + 8, 21), (dx + 4, 18)],
            "#D8CFC4", tension=0.6)
    _ol(c, [(0, 20), (13, 13), (12, 3), (-2, 0), (-14, 4), (-13, 15)],
        "#E3DCD2")
    circle(c, 8, 19, 8.5, fill="#EDE7DE", stroke=LINE, lw=1.3)
    circle(c, 12, 20, 1.8, fill="ink")
    circle(c, 15, 17, 1.4, fill="#E79A9A")
    circle(c, -13, 7, 5, fill="#FFFFFF", stroke=LINE, lw=1.2)
    c.restoreState()



# --------------------------------------------------------------- objects ---

def castle(c, x, y, s=1.0, wall="stone", roof="cape_dk", flag="cape",
           windows="#4E6A8A", grand=True):
    """Storybook castle with towers and pennants."""
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, -110, 0, 220, 96, fill=wall)
    rect(c, -110, 84, 220, 12, fill="stone_dk")
    for i in range(9):  # crenellations
        rect(c, -108 + i * 25, 96, 15, 12, fill=wall)
    towers = ((-118, 150), (0, 178), (118, 150)) if grand else ((-90, 120), (90, 120))
    for tx, th in towers:
        w = 40 if tx == 0 else 34
        rect(c, tx - w / 2, 0, w, th, fill=wall)
        rect(c, tx - w / 2 - 3, th, w + 6, 10, fill="stone_dk")
        for i in range(4):
            rect(c, tx - w / 2 + i * (w / 4) + 1, th + 10, w / 4 - 3, 9, fill=wall)
        poly(c, [(tx - w / 2 - 9, th + 19), (tx + w / 2 + 9, th + 19),
                 (tx, th + 19 + w * 1.25)], fill=roof)
        stroke_path(c, [(tx, th + 19 + w * 1.25), (tx, th + 30 + w * 1.4)],
                    color="wood_dk", lw=2.2)
        poly(c, [(tx, th + 30 + w * 1.4), (tx + 26, th + 25 + w * 1.4),
                 (tx, th + 20 + w * 1.4)], fill=flag)
        for wy in (th * 0.35, th * 0.68):
            rect(c, tx - 6, wy, 12, 17, fill=windows, r=6)
    rect(c, -26, 0, 52, 62, fill="wood_dk", r=24)
    rect(c, -21, 0, 42, 55, fill="wood", r=20)
    for dx in (-11, 0, 11):
        stroke_path(c, [(dx, 4), (dx, 50)], color="wood_dk", lw=2.0)
    circle(c, 0, 78, 13, fill=windows)
    for a in range(6):
        stroke_path(c, [(0, 78), (13 * math.cos(a * math.pi / 3),
                                  78 + 13 * math.sin(a * math.pi / 3))],
                    color="stone_dk", lw=1.8)
    for wx in (-72, -46, 46, 72):
        rect(c, wx - 7, 40, 14, 20, fill=windows, r=7)
    c.restoreState()


def cottage(c, x, y, s=1.0, wall="#EDDCC0", roof="#B5744A"):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    rect(c, -52, 0, 104, 58, fill=wall)
    poly(c, [(-64, 56), (64, 56), (0, 104)], fill=roof)
    poly(c, [(-64, 56), (64, 56), (0, 100)], fill="#9C603A", alpha=0.25)
    rect(c, 26, 74, 14, 30, fill="#9C603A")
    rect(c, -14, 0, 28, 40, fill="wood_dk", r=13)
    rect(c, -11, 0, 22, 35, fill="wood", r=10)
    for wx in (-33, 33):
        rect(c, wx - 10, 26, 20, 20, fill="#9CC4DC", r=3)
        stroke_path(c, [(wx, 26), (wx, 46)], color=wall, lw=2.4)
        stroke_path(c, [(wx - 10, 36), (wx + 10, 36)], color=wall, lw=2.4)
    c.restoreState()


def windmill(c, x, y, s=1.0):
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    blob(c, [(-40, 0), (-30, 60), (-24, 104), (24, 104), (30, 60), (40, 0)],
         fill="#E4D6BC", tension=0.4)
    rect(c, -40, 0, 80, 8, fill="#C9B896")
    poly(c, [(-32, 102), (32, 102), (0, 132)], fill="#8A5C36")
    rect(c, -10, 0, 20, 32, fill="wood_dk", r=8)
    for wx in (-16, 16):
        rect(c, wx - 6, 52, 12, 14, fill="#9CC4DC", r=2)
    c.saveState()
    c.translate(0, 104)
    c.rotate(18)
    for i in range(4):
        c.saveState()
        c.rotate(i * 90)
        rect(c, -4, 0, 8, 74, fill="wood_dk", r=2)
        rect(c, -13, 16, 26, 52, fill="#F3E9D2", r=2)
        stroke_path(c, [(-13, 16), (13, 16)], color="wood_dk", lw=1.6)
        c.restoreState()
    circle(c, 0, 0, 7, fill="wood")
    c.restoreState()
    c.restoreState()


def coach(c, x, y, s=1.0, body="king_robe", trim="gold", passengers=False):
    """Royal carriage, side view, facing right (the horse goes on the right)."""
    c.saveState()
    c.translate(x, y)
    c.scale(s, s)
    shadow(c, 0, 4, 92, 14, alpha=0.14)

    # wheels
    for wx, wr in ((-52, 30), (46, 22)):
        circle(c, wx, wr, wr, fill="#4E4038", stroke=LINE, lw=1.6)
        circle(c, wx, wr, wr - 6, fill="#7A6555")
        for i in range(8):
            ang = i * math.pi / 4
            stroke_path(c, [(wx, wr), (wx + (wr - 7) * math.cos(ang),
                                       wr + (wr - 7) * math.sin(ang))],
                        color="#4E4038", lw=2.2)
        circle(c, wx, wr, 5, fill=trim, stroke=LINE, lw=1.2)
    # axles + springs
    stroke_path(c, [(-52, 30), (0, 40), (46, 24)], color="#4E4038", lw=4.0)

    # cabin
    _ol(c, [(-74, 44), (-78, 92), (-52, 112), (24, 112), (44, 92), (40, 44),
            (-16, 36)], body, tension=0.85)
    _ol(c, [(-84, 104), (-16, 120), (52, 100), (46, 92), (-16, 110),
            (-80, 94)], trim, tension=0.75)
    # window with a gold frame
    rect(c, -60, 62, 74, 42, fill=trim, r=10, stroke=LINE, lw=1.5)
    rect(c, -55, 66, 64, 34, fill="#CFE7F3", r=7)
    if passengers:
        _coach_passengers(c, -23, 83)
    # door line + crest
    stroke_path(c, [(18, 44), (20, 104)], color=shade(body, 0.75), lw=2.0)
    circle(c, 30, 74, 9, fill=trim, stroke=LINE, lw=1.3)
    star(c, 30, 74, 6, fill="#FFF6DA")
    # driver's bench and shaft
    _ol(c, [(40, 92), (66, 96), (70, 78), (44, 74)], shade(body, 0.8),
        tension=0.6)
    stroke_path(c, [(58, 66), (120, 56), (196, 50)], color="wood_dk", lw=4.0)
    stroke_path(c, [(58, 52), (120, 46), (196, 44)], color="wood_dk", lw=3.0)
    c.restoreState()


def _coach_passengers(c, x, y):
    """Two little royals looking out of the carriage window."""
    circle(c, x - 13, y, 11, fill="skin", stroke=LINE, lw=1.3)
    _ol(c, [(x - 13, y + 12), (x - 3, y + 5), (x - 3, y - 4), (x - 13, y + 1),
            (x - 23, y - 4), (x - 23, y + 5)], "hair_grey", tension=0.7)
    poly(c, [(x - 22, y + 10), (x - 22, y + 20), (x - 17, y + 14),
             (x - 13, y + 21), (x - 9, y + 14), (x - 4, y + 20),
             (x - 4, y + 10)], fill="gold", stroke=LINE, lw=1.0)
    circle(c, x + 16, y - 3, 11, fill="skin", stroke=LINE, lw=1.3)
    _ol(c, [(x + 16, y + 9), (x + 27, y + 2), (x + 28, y - 15),
            (x + 20, y - 13), (x + 16, y - 3), (x + 12, y - 13),
            (x + 4, y - 15), (x + 5, y + 2)], "hair_gold", tension=0.75)
    for dx in (-3.5, 3.5):
        circle(c, x + 16 + dx, y - 2, 1.5, fill="ink")
        circle(c, x - 13 + dx, y + 1, 1.5, fill="ink")
    stroke_path(c, [(x - 17, y - 6), (x - 13, y - 4), (x - 9, y - 6)],
                color="ink", lw=1.2)
    stroke_path(c, [(x + 12, y - 8), (x + 16, y - 6), (x + 20, y - 8)],
                color="ink", lw=1.2)


def horse(c, x, y, s=1.0, flip=False, body="#C9A87C", mane="#6B4A32"):
    """A stout little cart horse, facing right."""
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    shadow(c, 0, 2, 48, 11, alpha=0.14)
    # far legs
    for dx in (-26, 22):
        taper(c, [(dx, 46), (dx + 3, 26), (dx + 5, 5)], 6.5, 5,
              fill=shade(body, 0.86), stroke=LINE, lw=1.3)
        _ol(c, [(dx + 1, 5), (dx, 0), (dx + 11, 0), (dx + 10, 5)],
            "#4E4038", tension=0.4)
    # tail
    taper(c, [(-40, 54), (-58, 44), (-64, 20)], 9, 4, fill=mane,
          stroke=LINE, lw=1.4)
    # barrel
    _ol(c, [(-38, 58), (0, 66), (34, 60), (42, 42), (30, 28), (-14, 26),
            (-40, 34)], body)
    # near legs
    for dx in (-18, 30):
        taper(c, [(dx, 44), (dx + 2, 24), (dx + 4, 5)], 7, 5.5, fill=body,
              stroke=LINE, lw=1.4)
        _ol(c, [(dx, 5), (dx - 1, 0), (dx + 11, 0), (dx + 10, 5)],
            "#3E332C", tension=0.4)
    # neck
    taper(c, [(30, 54), (44, 68), (50, 82)], 13, 10, fill=body,
          stroke=LINE, lw=1.5)
    # head
    _ol(c, [(44, 92), (58, 96), (74, 88), (76, 76), (62, 70), (46, 74),
            (40, 84)], body)
    ellipse(c, 72, 78, 8, 7, fill=shade(body, 0.92), stroke=LINE, lw=1.2)
    circle(c, 75, 76, 1.8, fill="#5E4A3E")
    circle(c, 58, 88, 2.4, fill="ink")
    circle(c, 57, 89, 0.9, fill="#FFFFFF")
    for dx in (44, 54):   # ears
        _ol(c, [(dx, 96), (dx + 3, 108), (dx + 8, 95), (dx + 4, 92)],
            body, tension=0.5)
    # mane down the neck
    taper(c, [(42, 100), (32, 82), (26, 62)], 8, 6, fill=mane)
    stroke_path(c, [(66, 84), (74, 83)], color=shade(body, 0.8), lw=1.4)
    c.restoreState()


def river(c, x, y, w, h, color="water", color2="water_dk", sparkles=True):
    blob(c, [(x, y + h * 0.7), (x + w * 0.3, y + h), (x + w * 0.62, y + h * 0.62),
             (x + w, y + h * 0.9), (x + w, y - 4), (x, y - 4)],
         fill=color, tension=0.8)
    for i, (fx, fy, fw) in enumerate(((0.12, 0.55, 0.16), (0.42, 0.35, 0.2),
                                      (0.7, 0.6, 0.14), (0.3, 0.72, 0.12))):
        stroke_path(c, [(x + w * fx, y + h * fy),
                        (x + w * (fx + fw / 2), y + h * fy + 5),
                        (x + w * (fx + fw), y + h * fy)],
                    color=color2, lw=2.6, alpha=0.8)
    if sparkles:
        rnd = _rng(5)
        for _ in range(12):
            sparkle(c, x + w * rnd(), y + h * rnd() * 0.9, 3.2,
                    color="#FFFFFF", alpha=0.5)


def wheat_field(c, x, y, w, h, seed=3, n=44):
    rect(c, x, y, w, h, fill="wheat")
    rnd = _rng(seed)
    for _ in range(n):
        sx = x + w * rnd()
        sy = y + h * rnd() * 0.85
        hh = 12 + 10 * rnd()
        stroke_path(c, [(sx, sy), (sx + 2, sy + hh * 0.6), (sx + 5, sy + hh)],
                    color="wheat_dk", lw=1.8)
        ellipse(c, sx + 5.5, sy + hh + 2, 2.6, 4.2, fill="#C79A38")


def bird(c, x, y, s=1.0, color="ink_soft"):
    stroke_path(c, [(x - 7 * s, y), (x - 3 * s, y + 4 * s), (x, y)],
                color=color, lw=1.8 * s)
    stroke_path(c, [(x, y), (x + 3 * s, y + 4 * s), (x + 7 * s, y)],
                color=color, lw=1.8 * s)


def speech(c, x, y, w, h, tail_x=None, tail_dir=-1, fill="#FFFFFF"):
    """Rounded speech bubble; returns the text-safe inner box."""
    rect(c, x, y, w, h, fill=fill, r=min(h / 2, 22))
    tx = tail_x if tail_x is not None else x + w * 0.3
    poly(c, [(tx, y + 4), (tx + 22, y + 6), (tx + 8 * tail_dir + 11, y - 20)],
         fill=fill)
    return (x + 14, y + 10, w - 28, h - 20)
