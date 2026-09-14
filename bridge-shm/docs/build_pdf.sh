#!/usr/bin/env bash
# Render docs/PRD.md -> docs/PRD.pdf (A4, footer with page numbers).
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
pandoc PRD.md \
  --from gfm \
  --to html5 \
  --standalone \
  --columns=400 \
  --metadata pagetitle="Bridge Vibration Monitoring Platform — PRD v0.1" \
  --css prd.css \
  --pdf-engine=weasyprint \
  --output PRD.pdf
echo "Wrote $(pwd)/PRD.pdf"
