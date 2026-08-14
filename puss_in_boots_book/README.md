# Puss in Boots — a printable picture book

A 22-page children's picture book, generated from source. Every illustration is
original vector art drawn with reportlab paths, so there are no image files and
the PDFs print crisply at any size.

Two editions, same pictures:

| File | Language |
| --- | --- |
| `Puss-in-Boots.pdf` | English |
| `Puss-in-Boots-zh.pdf` | 简体中文 (Simplified Chinese) |

## Printing it

Page size is **A4 landscape**, one scene per sheet.

- Print **single-sided**, "actual size" or "fit to page" — both work.
- On US Letter, choose *Fit to page*; the margins are generous enough that
  nothing important is lost.
- Colour, on the heaviest paper your printer takes. Matte photo paper or
  120gsm+ makes a real difference to how the flat colours sit.
- Page 2 has a blank line for your child's name.

To make it feel like a book, punch two or three holes along the left edge and
tie it with ribbon, or run it through a comb binder.

## Rebuilding

```
pip install reportlab
python3 book.py          # writes both PDFs
python3 book.py en       # just the English one
python3 book.py zh       # just the Mandarin one
```

Fonts used are system fonts: DejaVu Serif for English, WenQuanYi Zen Hei for
Chinese. Both are already present on most Linux boxes.

## The files

- `art.py` — the illustration toolkit. Drawing primitives (`blob`, `taper`,
  `stroke_path`), scenery (`meadow`, `castle`, `coach`, `horse`) and the
  characters. `draw_puss` is parameterised by pose, expression, tail and
  costume so the same cat appears on every page.
- `book.py` — page layout, the text panel, and one function per scene.
- `story.py` / `story_zh.py` — the text, one entry per spread. Edit these to
  change the wording; the scenes are keyed to them by position.

## About the story

A retelling of Charles Perrault's *Le Maître Chat, ou le Chat Botté* (1697),
which is long out of copyright. The ogre is chased off over the hill rather
than eaten, and the cat's rabbit goes into a sack rather than anywhere worse —
this version is aimed at a young listener.
