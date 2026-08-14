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
    # extra story palettes
    "red_cloak":   "#C0392B",
    "red_dk":      "#96291F",
    "wolf":        "#8A8F98",
    "wolf_dk":     "#666C76",
    "wolf_lt":     "#B8BDC6",
    "beast_fur":   "#8B5E3C",
    "beast_dk":    "#63421F",
    "beast_mane":  "#5B3A22",
    "cn_red":      "#C0392B",
    "cn_red_dk":   "#8E2A20",
    "cn_gold":     "#E9B949",
    "cn_jade":     "#4E9E8F",
    "night":       "#2B3A66",
    "night2":      "#485C93",
    "moonlight":   "#F3EFD2",
    "vine":        "#5FA347",
    "vine_dk":     "#3F7A36",
    "thorn":       "#5E6B4A",
    "rose":        "#D6455C",
    "steel":       "#96A2B0",
    "steel_dk":    "#6E7A88",
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


def shade(hex_or_name, k=0.82):
    """Darken (k<1) or lighten (k>1) a palette colour."""
    h = P.get(hex_or_name, hex_or_name)
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    f = lambda v: max(0, min(255, int(v * k if k < 1 else v + (255 - v) * (k - 1))))
    return "#%02X%02X%02X" % (f(r), f(g), f(b))


RICH = True          # set False for the flat v1 look
SOFT_LINE = 0.52     # outline = fill darkened this much (v2 soft look)


def paint(c, fill=None, stroke=None, lw=1.6, alpha=None):
    """
    Set fill/stroke state; returns (do_fill, do_stroke) for path drawing.

    Alpha is always written, never left at whatever the previous shape used --
    otherwise one translucent blob quietly washes out everything drawn after
    it, including gradient fills.
    """
    a = 1.0 if alpha is None else alpha
    if fill is not None:
        c.setFillColor(col(fill, alpha))
        c.setFillAlpha(a)
    if stroke is not None:
        if RICH and stroke == "ink_line" and fill is not None:
            # soft look: outline in a darkened version of the fill colour
            # rather than one uniform dark brown
            stroke = shade(fill, SOFT_LINE)
        c.setStrokeColor(col(stroke))
        c.setStrokeAlpha(a)
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


# --------------------------------------------------------------- shading ---
#
# v2 render pass. Flat fills read as clip-art; the same silhouettes with a
# gentle top-to-bottom gradient, a rim light and a contact shadow read as
# painted. Everything below is additive -- no shape changes, only rendering.

MIN_GRAD = 9.0       # shapes shorter than this stay flat (keeps the PDF small)


def _mkpath(c, pts, closed=True, tension=1.0):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for c1, c2, end in _catmull(pts, closed, tension):
        p.curveTo(c1[0], c1[1], c2[0], c2[1], end[0], end[1])
    if closed:
        p.close()
    return p


def grad_fill(c, pts, fill, closed=True, tension=1.0, lift=1.18, drop=0.84,
              alpha=None):
    """Fill a smooth shape with a soft vertical gradient."""
    ys = [p[1] for p in pts]
    y0, y1 = min(ys), max(ys)
    if not RICH or (y1 - y0) < MIN_GRAD or alpha is not None:
        blob(c, pts, fill=fill, alpha=alpha, closed=closed, tension=tension)
        return
    c.saveState()
    c.setFillAlpha(1.0)
    c.setStrokeAlpha(1.0)
    c.clipPath(_mkpath(c, pts, closed, tension), stroke=0, fill=0)
    c.linearGradient(0, y0, 0, y1,
                     [col(shade(fill, drop)), col(fill),
                      col(shade(fill, lift))], extend=True)
    c.restoreState()


def grad_disc(c, cx, cy, rx, ry, fill, lift=1.22, drop=0.82, hx=-0.35,
              hy=0.35):
    """A round shape lit from the upper left -- heads, foliage, fruit."""
    if not RICH or max(rx, ry) < MIN_GRAD * 0.5:
        ellipse(c, cx, cy, rx, ry, fill=fill)
        return
    c.saveState()
    c.setFillAlpha(1.0)
    c.setStrokeAlpha(1.0)
    p = c.beginPath()
    p.ellipse(cx - rx, cy - ry, rx * 2, ry * 2)
    c.clipPath(p, stroke=0, fill=0)
    c.radialGradient(cx + hx * rx, cy + hy * ry, max(rx, ry) * 1.45,
                     [col(shade(fill, lift)), col(fill),
                      col(shade(fill, drop))], extend=True)
    c.restoreState()


def rim(c, pts, color="#FFFFFF", alpha=0.22, lw=2.6, frac=0.45, tension=1.0):
    """A soft highlight along the upper-left edge of a shape."""
    if not RICH:
        return
    n = max(2, int(len(pts) * frac))
    seg = pts[:n + 1]
    c.saveState()
    c.setLineCap(1)
    c.setStrokeColor(col(color, alpha))
    c.setStrokeAlpha(alpha)
    c.setLineWidth(lw)
    c.drawPath(_mkpath(c, seg, False, tension), stroke=1, fill=0)
    c.restoreState()


def vignette(c, w, h, strength=0.18, warm="#2A1E14"):
    """Darken the page edges a little so the eye lands in the middle."""
    edge_shade(c, w, h, strength, warm)


def edge_shade(c, w, h, strength=0.18, warm="#2A1E14", bands=30):
    """Soft inward falloff from all four page edges."""
    if not RICH or strength <= 0:
        return
    dx, dy = w * 0.30, h * 0.36
    for i in range(bands):
        t = 1.0 - i / bands                       # 1 at the edge
        a_ = strength * (t ** 1.7) / bands * 3.0
        sx, sy = dx / bands, dy / bands
        rect(c, 0, i * sy, w, sy, fill=warm, alpha=a_)
        rect(c, 0, h - (i + 1) * sy, w, sy, fill=warm, alpha=a_)
        rect(c, i * sx, 0, sx, h, fill=warm, alpha=a_)
        rect(c, w - (i + 1) * sx, 0, sx, h, fill=warm, alpha=a_)


def glow(c, cx, cy, r, color="#FFF0B8", strength=0.30, rings=7):
    """A broad soft light -- sunlight spilling across a scene."""
    if not RICH:
        return
    for i in range(rings):
        k = 1.0 - i / rings
        circle(c, cx, cy, r * k, fill=color, alpha=strength / rings)


def light_wash(c, w, h, cx=None, cy=None, color="#FFF3CE", strength=0.16,
               rings=8):
    """A broad warm highlight, as if the whole page were lit from above."""
    if not RICH:
        return
    cx = w * 0.62 if cx is None else cx
    cy = h * 0.86 if cy is None else cy
    for i in range(rings):
        k = 1.0 - i / rings
        ellipse(c, cx, cy, w * 0.82 * k, h * 0.78 * k, fill=color,
                alpha=strength / rings)


def grain(c, w, h, n=900, seed=97, alpha=0.030):
    """Barely-there speckle so large flats read as paper, not screen."""
    if not RICH:
        return
    rnd = _rng(seed)
    for _ in range(n):
        r = 0.7 + 1.5 * rnd()
        circle(c, rnd() * w, rnd() * h, r,
               fill="#3A2A1E" if rnd() > 0.45 else "#FFFFFF", alpha=alpha)


def speckle(c, x, y, w, h, color, n=70, seed=1, r0=1.0, r1=2.6, alpha=0.16):
    """Faint dappling -- keeps big flat areas from looking like paper."""
    if not RICH:
        return
    rnd = _rng(seed)
    for _ in range(n):
        circle(c, x + w * rnd(), y + h * rnd(), r0 + (r1 - r0) * rnd(),
               fill=color, alpha=alpha)


def stroke_path(c, pts, color="ink", lw=2.0, tension=1.0, cap=1, alpha=None):
    """Smooth open line (whiskers, ropes, motion lines...)."""
    c.saveState()
    c.setLineCap(cap)
    c.setStrokeColor(col(color, alpha))
    c.setStrokeAlpha(1.0 if alpha is None else alpha)
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
    ry = ry if ry is not None else rx * 0.26
    ellipse(c, cx, cy, rx * 1.14, ry * 1.14, fill="#2A1E14", alpha=alpha * 0.55)
    ellipse(c, cx, cy, rx, ry, fill="#2A1E14", alpha=alpha)
    ellipse(c, cx, cy - ry * 0.12, rx * 0.62, ry * 0.6, fill="#2A1E14",
            alpha=alpha * 0.5)


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
    c.setFillAlpha(1.0)
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
    lobes = ((-26, -2, 17), (-6, 6, 23), (18, 0, 18), (34, -6, 13))
    if RICH and alpha >= 0.9:
        # rounded, top-lit lobes over a soft shaded base
        for dx, dy, rr in lobes:
            ellipse(c, cx + dx * s, cy + dy * s - rr * s * 0.2, rr * s,
                    rr * s * 0.6, fill=shade(fill, 0.90))
        for dx, dy, rr in lobes:
            grad_disc(c, cx + dx * s, cy + dy * s, rr * s, rr * s * 0.82,
                      fill, lift=1.04, drop=0.90, hx=-0.25, hy=0.5)
        rect(c, cx - 40 * s, cy - 12 * s, 82 * s, 12 * s, fill=fill)
        ellipse(c, cx - 2 * s, cy - 11 * s, 39 * s, 5 * s,
                fill=shade(fill, 0.90), alpha=0.6)
    else:
        for dx, dy, rr in lobes:
            ellipse(c, cx + dx * s, cy + dy * s, rr * s, rr * s * 0.82,
                    fill=fill, alpha=alpha)
        rect(c, cx - 40 * s, cy - 12 * s, 82 * s, 13 * s, fill=fill,
             alpha=alpha)


def hills(c, x, y, w, base_h, color="grass_dk", bumps=3, seedoff=0.0, alpha=None):
    pts = [(x - 10, y - 6)]
    for i in range(bumps + 1):
        t = i / bumps
        px = x + w * t
        py = y + base_h * (0.55 + 0.45 * math.sin(seedoff + t * 3.1))
        pts.append((px, py))
    pts.append((x + w + 10, y - 6))
    if alpha is None:
        grad_fill(c, pts, color, tension=0.9, lift=1.10, drop=0.92)
    else:
        blob(c, pts, fill=color, alpha=alpha, tension=0.9)


def ground(c, x, y, w, h, color="grass", top_color=None):
    if RICH and h > MIN_GRAD:
        c.saveState()
        c.setFillAlpha(1.0)
        c.setStrokeAlpha(1.0)
        p = c.beginPath()
        p.rect(x, y, w, h)
        c.clipPath(p, stroke=0, fill=0)
        c.linearGradient(0, y, 0, y + h,
                         [col(shade(color, 0.86)), col(shade(color, 1.06))],
                         extend=True)
        c.restoreState()
    else:
        rect(c, x, y, w, h, fill=color)
    if top_color:
        blob(c, [(x - 5, y + h - 14), (x + w * 0.25, y + h - 4),
                 (x + w * 0.55, y + h - 16), (x + w * 0.8, y + h - 5),
                 (x + w + 5, y + h - 12), (x + w + 5, y - 5), (x - 5, y - 5)],
             fill=top_color, tension=0.8)
        speckle(c, x, y, w, h * 0.92, shade(color, 0.82), n=int(w / 9) + 20,
                seed=int(abs(y)) + 3, r0=1.2, r1=3.4, alpha=0.13)


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
        grad_disc(c, x + dx * s, y + dy * s, rr * s, rr * s * 0.9, cl,
                  lift=1.16, drop=0.86)


def bush(c, x, y, s=1.0, color="grass_dk"):
    for dx, dy, rr in ((-14, 2, 14), (0, 8, 17), (15, 1, 13)):
        grad_disc(c, x + dx * s, y + dy * s, rr * s, rr * s * 0.85, color,
                  lift=1.15, drop=0.87)


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




def _ol(c, pts, fill, lw=LW, tension=1.0, shine=True):
    """Filled + outlined smooth shape -- the house style for characters."""
    grad_fill(c, pts, fill, tension=tension)
    if shine:
        rim(c, pts, alpha=0.21, lw=lw * 1.6, tension=tension)
    ln = shade(fill, SOFT_LINE) if RICH else LINE
    blob(c, pts, fill=None, stroke=ln, lw=lw, tension=tension)


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
    blob(c, [(-5, 9), (-1, 18), (3, 9)], fill="#FFFFFF", alpha=0.22, tension=0.7)
    circle(c, 9, 3.5, 1.6, fill="#FFFFFF", alpha=0.38)
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
                cloak=None, hood=None, armour=False, braid=False,
                wings=None, wand=False, apron=None, child=False):
    """A friendly storybook human, ~120 units to the crown of the head."""
    c.saveState()
    c.translate(x, y)
    if child:
        s *= 0.78
    c.scale(-s if flip else s, s)
    if shad:
        shadow(c, 0, 2, 28, 7.5, alpha=0.13)

    sleeve = shade(robe, 0.86)

    if wings:
        for sx in (-1, 1):
            _ol(c, [(sx * 8, 66), (sx * 30, 92), (sx * 44, 74),
                    (sx * 34, 52), (sx * 14, 50)], wings, tension=0.9, lw=1.2)
            blob(c, [(sx * 14, 64), (sx * 30, 78), (sx * 36, 68),
                     (sx * 22, 58)], fill="#FFFFFF", alpha=0.35, tension=0.9)

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
    if apron:
        _ol(c, [(-13, 62), (13, 62), (16, 30), (18, 12), (-18, 12), (-16, 30)],
            apron, tension=0.85)
    if armour:
        _ol(c, [(-18, 68), (0, 72), (18, 68), (20, 34), (0, 28), (-20, 34)],
            "steel", tension=0.85)
        for row in range(3):
            for i in range(4):
                rect(c, -16 + i * 8.5, 34 + row * 11, 7.5, 9.5,
                     fill=shade("steel", 0.92), stroke="steel_dk", lw=0.9, r=1.5)
        _ol(c, [(-21, 70), (0, 76), (21, 70), (18, 62), (0, 67), (-18, 62)],
            "cn_red", tension=0.7)
        for sx in (-1, 1):
            _ol(c, [(sx * 14, 72), (sx * 26, 68), (sx * 27, 56),
                    (sx * 15, 58)], "steel_dk", tension=0.8)
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
    grad_disc(c, 0, 93, 15, 15, skin, lift=1.10, drop=0.90)
    circle(c, 0, 93, 15, fill=None, stroke=LINE, lw=LW)

    if braid:
        taper(c, [(-13, 100), (-24, 84), (-27, 62), (-22, 46)], 5.5, 3.0,
              fill=hair, stroke=LINE, lw=1.3)
        for i, by in enumerate((86, 70, 54)):
            circle(c, -25 + i * 1.4, by, 3.4, fill=shade(hair, 0.88))
        _ol(c, [(-24, 48), (-19, 40), (-25, 38), (-28, 44)], "cn_red",
            tension=0.8)
    if long_hair:
        _ol(c, [(0, 110), (18, 100), (21, 72), (13, 66), (11, 88), (0, 94),
                (-11, 88), (-13, 66), (-21, 72), (-18, 100)], hair, tension=0.8)
    _ol(c, [(0, 110), (15, 101), (17, 90), (10, 97), (0, 100), (-10, 97),
            (-17, 90), (-15, 101)], hair, tension=0.75)

    if hood:
        # cowl over the shoulders, then the hood, then a face-shaped opening
        for sx in (-1, 1):
            _ol(c, [(sx * 22, 84), (sx * 30, 60), (sx * 19, 55),
                    (sx * 13, 76)], shade(hood, 0.88), tension=0.85)
        _ol(c, [(0, 124), (22, 113), (25, 90), (18, 76), (0, 72), (-18, 76),
                (-25, 90), (-22, 113)], hood, tension=0.9)
        _ol(c, [(0, 111), (13, 104), (15, 92), (9, 83), (0, 81), (-9, 83),
                (-15, 92), (-13, 104)], skin, tension=0.9)

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
    elif hat == "helmet":
        _ol(c, [(-17, 100), (-15, 116), (0, 124), (15, 116), (17, 100),
                (0, 106)], "steel", tension=0.85)
        _ol(c, [(-19, 102), (0, 108), (19, 102), (17, 95), (0, 100),
                (-17, 95)], "steel_dk", tension=0.7)
        stroke_path(c, [(0, 124), (0, 134)], color="steel_dk", lw=2.4)
        _ol(c, [(0, 134), (7, 144), (0, 151), (-7, 144)], "cn_red", tension=0.9)
        for sx in (-1, 1):
            _ol(c, [(sx * 17, 100), (sx * 21, 86), (sx * 14, 82),
                    (sx * 12, 96)], "steel_dk", tension=0.8)
    elif hat == "nightcap":
        _ol(c, [(-17, 100), (-15, 114), (2, 122), (18, 112), (17, 99),
                (0, 104)], "#EFE6D8", tension=0.85)
        taper(c, [(10, 118), (26, 124), (36, 116)], 7, 4, fill="#EFE6D8",
              stroke=LINE, lw=1.3)
        circle(c, 37, 115, 4.5, fill="#DCCFBB", stroke=LINE, lw=1.2)
    elif hat == "bonnet":
        _ol(c, [(-18, 98), (-16, 114), (0, 121), (16, 114), (18, 98),
                (0, 103)], "#F0E4D0", tension=0.85)
        _ol(c, [(-21, 100), (0, 106), (21, 100), (19, 92), (0, 98),
                (-19, 92)], "#E2D3BA", tension=0.7)
    elif hat == "cone":
        poly(c, [(-13, 104), (13, 104), (0, 146)], fill=robe, stroke=LINE,
             lw=1.3)
        rect(c, -14, 100, 28, 6, fill="gold", r=2, stroke=LINE, lw=1.1)
        stroke_path(c, [(0, 146), (16, 138), (28, 120), (24, 104)],
                    color="#FFFFFF", lw=3.0, alpha=0.8)
    elif hat == "mianguan":
        _ol(c, [(-16, 100), (-14, 112), (0, 118), (14, 112), (16, 100),
                (0, 105)], "#2E2620", tension=0.85)
        rect(c, -30, 116, 60, 8, fill="#1E1A16", r=2, stroke=LINE, lw=1.2)
        rect(c, -30, 124, 60, 5, fill="#C9A227", r=1.5)
        for dx in (-24, -12, 0, 12, 24):
            stroke_path(c, [(dx, 116), (dx, 100)], color="#C9A227", lw=1.2)
            for k in range(3):
                circle(c, dx, 112 - k * 5, 2.0, fill="#E9D9A8")
    elif hat == "cap":
        _ol(c, [(-16, 100), (-13, 112), (0, 116), (14, 110), (16, 99),
                (0, 104)], robe, tension=0.85)

    if wand:
        c.saveState()
        c.translate(30, 74)
        c.rotate(28)
        rect(c, 0, -1.4, 30, 2.8, fill="#E8DCC0", r=1.4, stroke=LINE, lw=1.0)
        star(c, 33, 0, 8, fill="gold")
        for i in range(4):
            sparkle(c, 40 + i * 7, 6 + (i % 2) * 9, 3.5, color="#FFF6DA")
        c.restoreState()

    c.restoreState()


def draw_ogre(c, x, y, s=1.0, flip=False, expr="grin", arm_l="out",
              arm_r="hip", shad=True, skin="ogre_skin", skin_dk="ogre_dk",
              cloth="ogre_cloth", cloth_dk="#4E3459", hair="#3E3A2E",
              tusks=True, beard=False):
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
              fill=skin_dk, stroke=LINE, lw=LW)
        _ol(c, [(sx * 18 - 12, 6), (sx * 18 - 13, 0), (sx * 18 + 13, 0),
                (sx * 18 + 12, 6)], "#4C3A2E", tension=0.4)

    pts = [(-px - 28, py + 70) for px, py in al]
    taper(c, pts, 10, 7.5, fill=skin_dk, stroke=LINE, lw=LW)
    circle(c, pts[-1][0], pts[-1][1], 8.5, fill=skin_dk, stroke=LINE, lw=1.3)

    _ol(c, [(0, 86), (34, 72), (42, 42), (34, 22), (0, 16), (-34, 22),
            (-42, 42), (-34, 72)], cloth)
    blob(c, [(-41, 32), (0, 24), (41, 32), (39, 42), (0, 34), (-39, 42)],
         fill=cloth_dk, tension=0.6)

    pts = [(px + 28, py + 70) for px, py in ar]
    taper(c, pts, 10.5, 8, fill=skin, stroke=LINE, lw=LW)
    circle(c, pts[-1][0], pts[-1][1], 9, fill=skin, stroke=LINE, lw=1.3)

    grad_disc(c, 0, 106, 27, 27, skin, lift=1.10, drop=0.90)
    circle(c, 0, 106, 27, fill=None, stroke=LINE, lw=LW)
    for sx in (-1, 1):
        _ol(c, [(sx * 26, 112), (sx * 34, 106), (sx * 26, 98), (sx * 22, 105)],
            skin, tension=0.6)
    _ol(c, [(0, 131), (19, 124), (25, 113), (12, 118), (0, 120), (-12, 118),
            (-25, 113), (-19, 124)], hair, tension=0.75)
    for sx in (-1, 1):
        stroke_path(c, [(sx * 4, 116), (sx * 10, 118), (sx * 16, 114)],
                    color=hair, lw=3.2)
        if expr == "surprised":
            circle(c, sx * 10, 107, 6.0, fill="#FFFFFF", stroke=LINE, lw=1.2)
            circle(c, sx * 10, 107, 3.0, fill="ink")
        else:
            ellipse(c, sx * 10, 107, 5.4, 5.0, fill="#FFFFFF", stroke=LINE, lw=1.2)
            circle(c, sx * 10, 106.6, 2.6, fill="ink")
    ellipse(c, 0, 99, 6.5, 5, fill=skin_dk)
    if expr == "grin":
        _ol(c, [(-14, 93), (0, 83), (14, 93), (0, 90)], "#5E2B2B", tension=0.7)
        if tusks:
            for dx in (-8, 8):
                poly(c, [(dx - 3.2, 92), (dx + 3.2, 92), (dx, 83)],
                     fill="#FFFFFF", stroke=LINE, lw=1.0)
    elif expr == "surprised":
        ellipse(c, 0, 90, 6.5, 7.5, fill="#5E2B2B", stroke=LINE, lw=1.2)
    else:
        stroke_path(c, [(-11, 91), (0, 88), (11, 91)], color="#5E2B2B", lw=2.8)
    if beard:
        _ol(c, [(-23, 97), (-19, 70), (0, 57), (19, 70), (23, 97), (0, 91)],
            hair, tension=0.75)
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
    grad_disc(c, 30, 58, 24, 24, "#E3B370", lift=1.12, drop=0.90)
    circle(c, 30, 58, 24, fill=None, stroke=LINE, lw=LW)
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


# ------------------------------------------------- creatures for the rest ---

def draw_wolf(c, x, y, s=1.0, flip=False, pose="stand", expr="sly",
              bonnet=False, shad=True):
    """
    The big bad wolf, facing +x.

    pose : 'stand' | 'sit' | 'run' | 'lurk'   (all four-footed)
    """
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    if shad:
        shadow(c, 0, 2, 56, 12, alpha=0.15)

    crouch = 0 if pose != "lurk" else -10
    # tail, behind everything
    taper(c, [(-46, 44 + crouch), (-70, 54 + crouch), (-84, 44 + crouch)],
          10, 5, fill="wolf_dk", stroke=LINE, lw=LW)
    circle(c, -84, 44 + crouch, 6, fill="wolf_lt", stroke=LINE, lw=1.2)

    # far legs
    for dx, fwd in ((-30, 0), (26, 0)):
        if pose == "run":
            fwd = -14 if dx < 0 else 12
        taper(c, [(dx, 40 + crouch), (dx + fwd * 0.5, 22), (dx + fwd, 5)],
              7, 5.5, fill="wolf_dk", stroke=LINE, lw=1.3)
        _ol(c, [(dx + fwd - 7, 5), (dx + fwd - 8, 0), (dx + fwd + 8, 0),
                (dx + fwd + 7, 5)], "wolf_dk", tension=0.5)

    # body
    if pose == "sit":
        _ol(c, [(-44, 58), (-6, 66), (30, 60), (40, 34), (10, 14), (-34, 18),
                (-48, 36)], "wolf")
    else:
        _ol(c, [(-46, 62 + crouch), (0, 70 + crouch), (36, 64 + crouch),
                (44, 44 + crouch), (10, 30 + crouch), (-34, 32 + crouch),
                (-50, 44 + crouch)], "wolf")
    blob(c, [(-30, 36 + crouch), (0, 32 + crouch), (26, 38 + crouch),
             (0, 46 + crouch)], fill="wolf_lt", alpha=0.75, tension=0.9)

    # near legs
    for dx, fwd in ((-22, 0), (34, 0)):
        if pose == "run":
            fwd = 14 if dx < 0 else -10
        if pose == "sit" and dx < 0:
            continue
        taper(c, [(dx, 42 + crouch), (dx + fwd * 0.5, 22), (dx + fwd, 5)],
              7.5, 6, fill="wolf", stroke=LINE, lw=1.4)
        _ol(c, [(dx + fwd - 7, 5), (dx + fwd - 8, 0), (dx + fwd + 9, 0),
                (dx + fwd + 8, 5)], "wolf_dk", tension=0.5)

    # neck and head
    taper(c, [(34, 58 + crouch), (48, 72 + crouch), (54, 84 + crouch)],
          13, 10, fill="wolf", stroke=LINE, lw=LW)
    hx, hy = 58, 92 + crouch
    for sx, ex in ((1, 4), (1, 20)):    # ears
        _ol(c, [(hx + ex - 8, hy + 8), (hx + ex - 3, hy + 26),
                (hx + ex + 8, hy + 9), (hx + ex, hy + 5)], "wolf",
            tension=0.5)
        blob(c, [(hx + ex - 4, hy + 9), (hx + ex - 1, hy + 20),
                 (hx + ex + 4, hy + 10)], fill="#C09A9A", tension=0.5)
    _ol(c, [(hx, hy + 14), (hx + 15, hy + 9), (hx + 18, hy - 4),
            (hx + 6, hy - 14), (hx - 12, hy - 12), (hx - 16, hy + 2)],
        "wolf")
    # snout
    _ol(c, [(hx + 8, hy + 2), (hx + 30, hy + 4), (hx + 40, hy - 3),
            (hx + 34, hy - 12), (hx + 10, hy - 12)], "wolf_lt", tension=0.9)
    _ol(c, [(hx + 40, hy + 1), (hx + 45, hy - 2), (hx + 42, hy - 7),
            (hx + 36, hy - 6)], "ink", tension=0.9)
    if expr == "surprised":
        ellipse(c, hx + 24, hy - 13, 7, 5, fill="#7A2E2E", stroke=LINE, lw=1.1)
    else:
        _ol(c, [(hx + 12, hy - 11), (hx + 24, hy - 17), (hx + 38, hy - 10),
                (hx + 24, hy - 12)], "#7A2E2E", tension=0.8)
        for dx in (16, 32):   # teeth
            poly(c, [(hx + dx - 3, hy - 11), (hx + dx + 3, hy - 11),
                     (hx + dx, hy - 18)], fill="#FFFFFF", stroke=LINE, lw=0.9)
    # eyes
    for ex in (2, 16):
        ellipse(c, hx + ex, hy + 3, 5.0, 5.4, fill="#F6E7A8", stroke=LINE,
                lw=1.2)
        ellipse(c, hx + ex + (1 if expr == "sly" else 0), hy + 2.6, 2.2, 3.6,
                fill="ink")
        circle(c, hx + ex - 1.4, hy + 4.4, 1.3, fill="#FFFFFF")
        if expr == "sly":
            blob(c, [(hx + ex - 6, hy + 4), (hx + ex, hy + 7),
                     (hx + ex + 6, hy + 3), (hx + ex + 6, hy + 12),
                     (hx + ex - 6, hy + 12)], fill="wolf", tension=0.6)
        stroke_path(c, [(hx + ex - 6, hy + 10), (hx + ex + 1, hy + 12),
                        (hx + ex + 7, hy + 9)], color="wolf_dk", lw=2.2)

    if bonnet:
        _ol(c, [(hx - 18, hy + 6), (hx - 14, hy + 26), (hx + 8, hy + 32),
                (hx + 24, hy + 22), (hx + 26, hy + 6), (hx + 4, hy + 14)],
            "#F0E4D0", tension=0.85)
        _ol(c, [(hx - 20, hy + 8), (hx + 4, hy + 16), (hx + 28, hy + 8),
                (hx + 26, hy - 1), (hx + 4, hy + 7), (hx - 18, hy - 1)],
            "#E2D3BA", tension=0.7)
        for fx in (-10, 2, 14):
            circle(c, hx + fx, hy + 26, 3.0, fill="#D9C7A8")
    c.restoreState()


def draw_beast(c, x, y, s=1.0, flip=False, expr="kind", arm_l="down",
               arm_r="down", shad=True, coat="#35558A", trim="gold"):
    """The Beast: big, shaggy, horned -- and, in the face, gentle."""
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    if shad:
        shadow(c, 0, 2, 52, 13, alpha=0.16)

    ARMS = {"down": [(0, 0), (13, -22), (18, -44)],
            "out":  [(0, 0), (26, -8), (46, -14)],
            "up":   [(0, 0), (18, 16), (28, 36)],
            "offer": [(0, 0), (24, -14), (44, -12)],
            "hip":  [(0, 0), (22, -18), (12, -34)]}
    al, ar = ARMS.get(arm_l, arm_l), ARMS.get(arm_r, arm_r)

    # tail
    taper(c, [(-34, 40), (-56, 34), (-66, 48)], 7, 4, fill="beast_dk",
          stroke=LINE, lw=1.4)
    circle(c, -66, 48, 6, fill="beast_mane", stroke=LINE, lw=1.2)

    # digitigrade legs
    for sx in (-1, 1):
        taper(c, [(sx * 15, 40), (sx * 20, 22), (sx * 17, 8)], 12, 10,
              fill="beast_dk", stroke=LINE, lw=LW)
        _ol(c, [(sx * 17 - 14, 8), (sx * 17 - 15, 0), (sx * 17 + 15, 0),
                (sx * 17 + 13, 8)], "beast_dk", tension=0.5)
        for k in (-7, 0, 7):
            poly(c, [(sx * 17 + k - 2, 1), (sx * 17 + k + 2, 1),
                     (sx * 17 + k, -3)], fill="#EFE3CC")

    pts = [(-px - 26, py + 74) for px, py in al]
    taper(c, pts, 10, 7, fill="beast_dk", stroke=LINE, lw=LW)
    circle(c, pts[-1][0], pts[-1][1], 8.5, fill="beast_dk", stroke=LINE, lw=1.3)

    # barrel chest in a princely coat
    _ol(c, [(0, 92), (30, 82), (38, 50), (30, 26), (0, 20), (-30, 26),
            (-38, 50), (-30, 82)], "beast_fur")
    _ol(c, [(-24, 86), (-32, 50), (-26, 24), (0, 20), (26, 24), (32, 50),
            (24, 86), (0, 78)], coat, tension=0.9)
    blob(c, [(0, 80), (13, 60), (12, 26), (-12, 26), (-13, 60)],
         fill="#EFE3CC", tension=0.9)
    _ol(c, [(-26, 32), (0, 26), (26, 32), (26, 22), (0, 16), (-26, 22)],
        trim, tension=0.7)

    pts = [(px + 26, py + 74) for px, py in ar]
    taper(c, pts, 10.5, 7.5, fill="beast_fur", stroke=LINE, lw=LW)
    circle(c, pts[-1][0], pts[-1][1], 9, fill="beast_fur", stroke=LINE, lw=1.3)
    for k in (-5, 0, 5):
        poly(c, [(pts[-1][0] + k - 2, pts[-1][1] - 7),
                 (pts[-1][0] + k + 2, pts[-1][1] - 7),
                 (pts[-1][0] + k, pts[-1][1] - 12)], fill="#EFE3CC")

    # mane
    for i in range(16):
        ang = i * 2 * math.pi / 16
        ellipse(c, 30 * math.cos(ang), 112 + 30 * math.sin(ang), 13, 11,
                fill="beast_mane", stroke=LINE, lw=1.1)
    _ol(c, [(0, 138), (22, 130), (28, 112), (22, 94), (0, 86), (-22, 94),
            (-28, 112), (-22, 130)], "beast_fur")
    # horns
    for sx in (-1, 1):
        taper(c, [(sx * 18, 130), (sx * 32, 144), (sx * 30, 160)],
              7, 3, fill="#D8CDB4", stroke=LINE, lw=1.3)
    # snout
    _ol(c, [(0, 104), (14, 100), (17, 90), (10, 83), (0, 82), (-10, 83),
            (-17, 90), (-14, 100)], "#C89A6A", tension=0.9)
    _ol(c, [(0, 98), (6, 95), (5, 90), (0, 88), (-5, 90), (-6, 95)],
        "ink", tension=0.9)
    if expr == "roar":
        _ol(c, [(0, 86), (11, 82), (12, 70), (0, 64), (-12, 70), (-11, 82)],
            "#7A2E2E", tension=0.9)
        for dx in (-6, 6):
            poly(c, [(dx - 3, 81), (dx + 3, 81), (dx, 72)], fill="#FFFFFF")
    elif expr == "sad":
        stroke_path(c, [(-7, 80), (0, 84), (7, 80)], color="ink", lw=2.0)
    else:
        stroke_path(c, [(-8, 84), (0, 79), (8, 84)], color="ink", lw=2.0)
    # eyes
    for sx in (-1, 1):
        ellipse(c, sx * 10, 112, 6.4, 6.8, fill="#FFFFFF", stroke=LINE, lw=1.3)
        dy = -1.2 if expr == "sad" else 0
        ellipse(c, sx * 10, 111 + dy, 3.0, 4.2, fill="#4E7FBF")
        circle(c, sx * 10, 110.6 + dy, 1.9, fill="ink")
        circle(c, sx * 10 - 1.6, 113 + dy, 1.5, fill="#FFFFFF")
        bw = (122, 119) if expr in ("kind", "sad") else (118, 123)
        stroke_path(c, [(sx * 4, bw[0]), (sx * 11, bw[1] + 1),
                        (sx * 18, bw[1] - 1)], color="beast_mane", lw=2.8)
    c.restoreState()


def draw_cow(c, x, y, s=1.0, flip=False, shad=True, body="#F2EDE4",
             patch="#6B5344"):
    """Milky-white, the family cow. Facing +x."""
    c.saveState()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    if shad:
        shadow(c, 0, 2, 48, 11, alpha=0.14)
    taper(c, [(-40, 52), (-58, 40), (-60, 18)], 5, 3, fill=body,
          stroke=LINE, lw=1.3)
    circle(c, -60, 16, 6, fill=patch, stroke=LINE, lw=1.2)
    for dx in (-28, 20):
        taper(c, [(dx, 44), (dx + 2, 24), (dx + 4, 5)], 6.5, 5.5,
              fill=shade(body, 0.9), stroke=LINE, lw=1.3)
        _ol(c, [(dx + 1, 5), (dx, 0), (dx + 10, 0), (dx + 9, 5)],
            "#4E4038", tension=0.5)
    _ol(c, [(-40, 58), (0, 66), (34, 60), (42, 40), (28, 26), (-16, 24),
            (-42, 34)], body)
    for cx_, cy_, rr in ((-18, 46, 13), (12, 38, 10), (-2, 56, 8)):
        ellipse(c, cx_, cy_, rr, rr * 0.78, fill=patch)
    _ol(c, [(-8, 26), (8, 26), (7, 14), (-7, 14)], "#E9A7A7", tension=0.8)
    for dx in (-4, 4):
        taper(c, [(dx, 16), (dx, 9)], 2.0, 1.2, fill="#D98F8F")
    for dx in (-22, 26):
        taper(c, [(dx, 44), (dx + 2, 24), (dx + 4, 5)], 7, 6, fill=body,
              stroke=LINE, lw=1.4)
        _ol(c, [(dx + 1, 5), (dx, 0), (dx + 11, 0), (dx + 10, 5)],
            "#3E332C", tension=0.5)
    taper(c, [(30, 54), (44, 66), (50, 76)], 12, 10, fill=body,
          stroke=LINE, lw=1.4)
    _ol(c, [(42, 88), (58, 90), (70, 80), (66, 68), (48, 66), (38, 74)],
        body)
    ellipse(c, 66, 74, 9, 7.5, fill="#E9A7A7", stroke=LINE, lw=1.2)
    for dx in (63, 70):
        circle(c, dx, 74, 1.6, fill="#B87070")
    circle(c, 52, 84, 2.4, fill="ink")
    circle(c, 51, 85, 0.9, fill="#FFFFFF")
    for sx, ex in ((1, 40), (1, 58)):   # horns
        taper(c, [(ex, 92), (ex - 4, 102), (ex + 4, 106)], 3.4, 1.8,
              fill="#E4D9C0", stroke=LINE, lw=1.1)
    _ol(c, [(36, 86), (30, 94), (38, 96), (44, 90)], body, tension=0.7)
    # a bell on a collar
    stroke_path(c, [(40, 70), (52, 66)], color="cape_dk", lw=3.0)
    _ol(c, [(46, 66), (52, 66), (53, 58), (45, 58)], "gold", tension=0.7)
    circle(c, 49, 56, 2.0, fill="gold_dk")
    c.restoreState()
