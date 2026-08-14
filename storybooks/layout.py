"""
Page furniture shared by every book in the series.

A title supplies text and a set of scene functions; this module owns the page
geometry, the fonts, the cream text panel, and the cover / nameplate / end /
back-cover plates so all the books look like they belong on one shelf.
"""

import os

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from art import col, rect, stroke_path, star, shadow

W, H = landscape(A4)       # 841.89 x 595.28 pt
BASE = 200                 # ground line: where characters put their feet
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "pdf")

pdfmetrics.registerFont(TTFont(
    "Story", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont(
    "Story-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
# WenQuanYi Zen Hei is the one CJK face on this box; it ships only a regular
# weight, so headings in Chinese editions are emboldened by overprinting.
pdfmetrics.registerFont(TTFont(
    "Han", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))

LANGS = {
    "en": dict(font="Story", bold="Story-Bold", faux=False,
               size=16.5, lead=24.5, cjk=False, suffix=""),
    "zh": dict(font="Han", bold="Han", faux=True,
               size=18.5, lead=31, cjk=True, suffix="-zh"),
}

TXT = {}                   # current text dict
F, FB = "Story", "Story-Bold"
FAUX_BOLD = False
BODY_SIZE, BODY_LEAD, CJK = 16.5, 24.5, False


def set_lang(lang, txt):
    global TXT, F, FB, FAUX_BOLD, BODY_SIZE, BODY_LEAD, CJK
    cfg = LANGS[lang]
    TXT = txt
    F, FB = cfg["font"], cfg["bold"]
    FAUX_BOLD, CJK = cfg["faux"], cfg["cjk"]
    BODY_SIZE, BODY_LEAD = cfg["size"], cfg["lead"]
    return cfg


# ------------------------------------------------------------------ text ---

def bold_centred(c, x, y, text, size, color):
    """Heading text; overprinted when the face has no real bold cut."""
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


# punctuation that may not begin a line, and that may not end one
NO_LINE_START = "。，、；：？！）》」』”’—…"
NO_LINE_END = "（《「『“‘"


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


# ---------------------------------------------------------------- plates ---

def title_plate(c, title, subtitle, y=468, accent="#7A3B2E", size=52):
    """The cream banner carrying the book's name on the cover."""
    while size > 22 and pdfmetrics.stringWidth(title, FB, size) > 404:
        size -= 1
    c.saveState()
    c.setFillColorRGB(0, 0, 0, 0.12)
    c.roundRect(147, y - 4, 548, 112, 26, stroke=0, fill=1)
    c.restoreState()
    rect(c, 144, y, 548, 112, fill="cream", r=26, stroke="#D9BE8A", lw=2.6)
    rect(c, 156, y + 12, 524, 88, fill="cream", r=20, stroke="#E7D3AC", lw=1.2)
    bold_centred(c, W / 2 - 5, y + 44, title, size, accent)
    c.setFillColor(col("ink_soft"))
    c.setFont(F, 15)
    c.drawCentredString(W / 2 - 5, y + 18, subtitle)
    for sx in (-1, 1):
        star(c, W / 2 - 5 + sx * 232, y + 56, 9, fill="gold")


def nameplate(c, txt, vignette=None, accent="#7A3B2E"):
    """Second page: title, byline, a small still life, and a name line."""
    rect(c, 0, 0, W, H, fill="#FBF3E2")
    rect(c, 44, 40, W - 88, H - 80, fill=None, stroke="#DCC69B", lw=3.0, r=18)
    rect(c, 56, 52, W - 112, H - 104, fill=None, stroke="#E8D6B4", lw=1.4, r=12)
    for cx, cy in ((44, 40), (W - 44, 40), (44, H - 40), (W - 44, H - 40)):
        star(c, cx, cy, 11, fill="#DCC69B")

    bold_centred(c, W / 2, 486, txt["TITLE"], 32, accent)
    c.setFillColor(col("ink_soft"))
    c.setFont(F, 13.5)
    c.drawCentredString(W / 2, 458, txt["BYLINE"])

    if vignette:
        vignette(c)

    c.setFillColor(col("ink_soft"))
    c.setFont(F, 16)
    c.drawCentredString(W / 2, 168, txt["BELONGS_TO"])
    stroke_path(c, [(W / 2 - 200, 130), (W / 2 + 200, 130)],
                color="#C9BA88", lw=1.8)
    c.setFont(F, 12 if CJK else 10.5)
    c.setFillColor(col("#9C8B76"))
    for i, ln in enumerate(txt["COLOPHON"].split("\n")):
        c.drawCentredString(W / 2, 92 - i * 17, ln)


def end_plate(c, text, accent="#7A3B2E"):
    c.saveState()
    c.setFillColorRGB(0, 0, 0, 0.10)
    c.roundRect(W / 2 - 155, 56, 320, 76, 22, stroke=0, fill=1)
    c.restoreState()
    rect(c, W / 2 - 158, 60, 320, 76, fill="cream", r=22, stroke="#D9BE8A",
         lw=2.2)
    bold_centred(c, W / 2 + 2, 88, text, 34, accent)


def back_quote(c, lines, y=534, accent="#7A3B2E"):
    for i, ln in enumerate(lines):
        bold_centred(c, W / 2, y - i * 30, ln, 22, accent)
    for sx in (-1, 1):
        star(c, W / 2 + sx * 300, y - 14, 10, fill="gold")


# ------------------------------------------------------------------ build ---

def build(book, lang="en", outdir=None):
    """
    Render one title.

    `book` is a module exposing:
        TEXT     {lang: {...}}      the words
        SCENES   [fn(c), ...]       one illustration per story page
        COVER_ART, END_ART, BACK_ART, NAMEPLATE_ART   page furniture art
        ACCENT   (optional)         heading colour
    """
    txt = book.TEXT[lang]
    cfg = set_lang(lang, txt)
    accent = getattr(book, "ACCENT", "#7A3B2E")
    outdir = outdir or OUT
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"{book.SLUG}{cfg['suffix']}.pdf")

    c = Canvas(path, pagesize=(W, H))
    c.setTitle(txt["TITLE"])
    c.setAuthor(txt["BYLINE"])
    c.setSubject("A printable picture book")

    book.COVER_ART(c)
    title_plate(c, txt["TITLE"], txt["SUBTITLE"], accent=accent)
    c.showPage()

    nameplate(c, txt, getattr(book, "NAMEPLATE_ART", None), accent)
    c.showPage()

    assert len(book.SCENES) == len(txt["PAGES"]), (
        f"{book.SLUG}: {len(book.SCENES)} scenes vs {len(txt['PAGES'])} texts")
    for i, page in enumerate(txt["PAGES"]):
        book.SCENES[i](c)
        text_panel(c, page)
        folio(c, i + 1)
        c.showPage()

    book.END_ART(c)
    end_plate(c, txt["THE_END"], accent)
    c.showPage()

    book.BACK_ART(c)
    back_quote(c, txt["BACK_QUOTE"],
               accent=getattr(book, "BACK_ACCENT", accent))
    c.showPage()

    c.save()
    return path
