#!/usr/bin/env bash
# Render docs/PRD.md -> docs/PRD.pdf (A4, footer with page numbers).
# Requires: pandoc, weasyprint (pip install weasyprint), fonts-liberation / fonts-dejavu.
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
