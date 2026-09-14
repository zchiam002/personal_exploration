#!/usr/bin/env bash
# Render the PRD documents in this folder to PDF (A4, footer with page numbers):
#   PRD.md                -> PRD.pdf                (stylesheet prd.css)
#   PRD-plain-language.md -> PRD-plain-language.pdf (stylesheet prd-plain.css)
# Requires:
#   - pandoc >= 2.x with the gfm reader and --pdf-engine=weasyprint support (apt install pandoc)
#   - weasyprint on PATH (pip install weasyprint) plus its system libs: pango, cairo, gdk-pixbuf
#     (apt install libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf-2.0-0)
#   - fonts-liberation (body font) and fonts-dejavu (glyph fallback)
#   - a C.UTF-8 locale (present on Ubuntu/Debian); see LC_ALL below
# The 'gfm' reader is deliberate: PRD.md has bullet lists directly under bold label lines
# with no blank line, which pandoc's default markdown reader does not parse as lists.
set -euo pipefail
export LC_ALL=C.UTF-8   # pandoc decodes CLI args with the locale; keep the em dash in the title intact
cd "$(dirname "$0")"

render() { # render <input.md> <output.pdf> <stylesheet.css> <title>
  pandoc "$1" \
    --from gfm \
    --to html5 \
    --standalone \
    --columns=400 \
    --metadata pagetitle="$4" \
    --css "$3" \
    --pdf-engine=weasyprint \
    --output "$2"
  echo "Wrote $(pwd)/$2"
}

render PRD.md PRD.pdf prd.css "Bridge Vibration Monitoring Platform — PRD v0.1"
render PRD-plain-language.md PRD-plain-language.pdf prd-plain.css "Bridge Vibration Monitoring Platform — PRD v0.1, plain-language edition"
