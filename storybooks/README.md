# Storybooks — printable picture books

A small shelf of children's picture books, generated from source. Every
illustration is original vector art drawn with reportlab paths, so there are no
image files, nothing is downloaded, and the PDFs print crisply at any size.

`pdf/` holds the current **v2** artwork; `pdf/v1/` keeps the earlier flat
rendering for comparison.

| File | Title | Pages |
| --- | --- | --- |
| `pdf/puss-in-boots-v2.pdf` | Puss in Boots | 22 |
| `pdf/puss-in-boots-zh-v2.pdf` | 穿靴子的猫 (Simplified Chinese) | 22 |
| `pdf/jack-and-the-beanstalk-v2.pdf` | Jack and the Beanstalk | 18 |
| `pdf/beauty-and-the-beast-v2.pdf` | Beauty and the Beast | 18 |
| `pdf/hua-mulan-v2.pdf` | Hua Mulan | 18 |
| `pdf/sleeping-beauty-v2.pdf` | Sleeping Beauty | 18 |
| `pdf/little-red-riding-hood-v2.pdf` | Little Red Riding Hood | 18 |

## Printing

Page size is **A4 landscape**, one scene per sheet.

- Print **single-sided**, "actual size" or "fit to page" — both work.
- On US Letter, choose *Fit to page*; the margins are generous enough that
  nothing important is lost.
- Colour, on the heaviest paper your printer takes. Matte photo paper or
  120gsm+ makes a real difference to how the flat colours sit.
- Page 2 of every book has a blank line for your child's name.

To make it feel like a book, punch two or three holes along the left edge and
tie it with ribbon, or run it through a comb binder.

## Rebuilding

```
pip install reportlab
python3 build.py                  # every title, every language
python3 build.py hua-mulan        # just one
```

Fonts are system fonts: DejaVu Serif for English, WenQuanYi Zen Hei for
Chinese. Both are already present on most Linux boxes.

## v2 rendering

The shapes are unchanged from v1; what changed is how they are painted:

- **Gradient fills.** Every outlined character shape is filled with a soft
  vertical gradient instead of a flat colour, so bodies, clothing and props
  have volume. Round forms (heads, foliage) use a radial gradient lit from the
  upper left.
- **Rim light.** A faint highlight runs along the upper-left edge of each
  shape.
- **Deeper contact shadows.** Three stacked ellipses instead of one flat disc.
- **Ground and hills** are graded and lightly dappled rather than flat slabs.
- **Edge vignette** on every page so the eye lands in the middle.
- **An alpha bug fixed.** `paint()` never reset transparency, so any shape
  drawn after a translucent one inherited its alpha and rendered washed out.
  Colours across all six books are noticeably richer as a result.

Set `art.RICH = False` to get the flat v1 look back from the same source.

## How it is put together

- `art.py` — the illustration toolkit. Smooth-curve primitives (`blob` and
  `taper` build Catmull-Rom splines), then the cast: `draw_puss`,
  `draw_person`, `draw_ogre`, `draw_beast`, `draw_wolf`, `draw_cow`,
  `draw_lion`, `draw_mouse`, `draw_rabbit`. Characters are parameterised by
  pose, expression and costume, so one function covers a peasant, a king, a
  fairy, a soldier in lamellar armour and a girl in a red hood.
- `scenery.py` — anything that appears in more than one book: meadows,
  forests, interiors, castles, a coach, a beanstalk, a spinning wheel, a
  thorn hedge, a loom, a rose under glass.
- `layout.py` — page geometry, fonts, the cream text panel, and the cover /
  nameplate / end / back-cover furniture, so every book looks like it belongs
  on the same shelf. Also holds the language config: Chinese editions break
  lines per character and keep punctuation off line starts.
- One module per title (`beanstalk.py`, `beauty.py`, `mulan.py`,
  `sleeping_beauty.py`, `red_riding_hood.py`, `puss_in_boots.py`), each
  exposing `TEXT`, `SCENES` and the four page-furniture art functions.

To add a book, copy the smallest title module and fill in the text and scenes.

## About the stories

All six are out of copyright and retold here from the oldest versions rather
than from any film:

- **Puss in Boots** — Perrault, *Le Maître Chat, ou le Chat Botté* (1697)
- **Jack and the Beanstalk** — English folk tale, printed since 1734
- **Beauty and the Beast** — Leprince de Beaumont, *La Belle et la Bête* (1756)
- **Hua Mulan** — the Ballad of Mulan, China, c. 6th century. This follows the
  ballad: no dragon, no matchmaker; she buys her own horse, serves twelve
  years, refuses the Emperor's office and asks only to go home.
- **Sleeping Beauty** — Perrault, *La Belle au bois dormant* (1697)
- **Little Red Riding Hood** — Perrault (1697) and the Grimms (1812)

Endings are pitched at a young listener. The ogre is chased over the hill
rather than eaten; the wolf shuts nobody in his stomach — Grandmother hides in
the wardrobe and the wolf goes out of the window.
