#!/usr/bin/env python3
"""Assemble PLAYBOOK.md from its parts, render PLAYBOOK.html and a print HTML.
Run:  python3 build_playbook.py && $CHROME --headless=new --no-sandbox --print-to-pdf=PLAYBOOK.pdf --no-pdf-header-footer PLAYBOOK.html
"""
import csv, html, re, markdown

body = open("playbook_body.md").read()
kit = open("outreach_kit.md").read()
appc = open("appendix_c.md").read()

# Appendix A: the outreach kit, demoted one heading level
kit_a = re.sub(r"^# Outreach Kit\s*", "", kit)
kit_a = re.sub(r"^## ", "### ", kit_a, flags=re.M)
kit_a = re.sub(r"^### (\d\.) ", r"### A.\1 ", kit_a, flags=re.M)
kit_a = re.sub(r"^### ([ABC])\. ", r"#### \1. ", kit_a, flags=re.M)
kit_a = "## Appendix A. Outreach kit\n\n" + kit_a

# Appendix B: priority-1 targets from the CSV
rows = list(csv.DictReader(open("target_list.csv")))
p1 = [r for r in rows if r["priority"] == "1"]
tbl = ["## Appendix B. Priority targets\n",
       f"{len(p1)} priority-1 accounts of {len(rows)} in `target_list.csv`. Offer numbers refer to §4.\n",
       "| Segment | Company | Base | Why now | Contact | Offers |", "|---|---|---|---|---|---|"]
for r in p1:
    tbl.append(f"| {r['segment']} | {r['company']} | {r['base']} | {r['why_now']} | {r['role_to_contact']} ({r['channel']}) | {r['offer_fit']} |")
appb = "\n".join(tbl) + "\n"

sources = """## Sources

Fugro H1 2026 (Baird Maritime, Windpower NL); Westwood on Taiwan Round 3.1 and on Aramco jack-ups; White & Case and Aegir Insights on Japan; Windtech International on Korea's H1 2026 auction; BCA Construction Prospects 2026; Corestaff hiring reports; URA and Malay Mail on Long Island and Tekong; JLL and Johor industrial news on JS-SEZ data centres; Ground Engineering and Offshore Energy on the HELMS–PETRONAS CCS contract; Offsnet on Malaysian decommissioning; Enerdata, ENR and SolarQuarter on Malaysian floating solar; Petroleum Australia and Offshore Energy on Bass Strait; Jobs and Skills Australia on geotechnical engineers; PEB guidelines for Specialist PE (Geotechnical); Masin and Expert Services International on expert-witness work; Construction Week on NEOM; iPS and crewbase on offshore day rates; Jobstreet and SalaryExpert on Singapore salaries; Expert Opportunities on expert-network rates. Full links are in `job_acquisition_plan.md` and `collaboration_assessment.md`.
"""

md = body + "\n" + kit_a + "\n" + appb + "\n" + appc + "\n" + sources
title_md = """# Guang Jie Geotech Playbook

**Prepared for:** Tuang Guang Jie · **Prepared by:** Laminar Flow · **Date:** 14 September 2026 · **Revision:** 1 · **Status:** for discussion

"""
open("PLAYBOOK.md", "w").write(title_md + md)

mdx = markdown.Markdown(extensions=["tables", "toc", "sane_lists"])
body_html = mdx.convert(md)

# rail: one strata band per h2
h2s = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
bands = []
for i, (hid, text) in enumerate(h2s):
    label = re.sub(r"<.*?>", "", text)
    short = re.sub(r"^(\d+|Appendix [ABC])\.\s*", "", label)
    num = re.match(r"^(\d+|Appendix ([ABC]))\.", label)
    key = (num.group(2) or num.group(1)) if num else "§"
    bands.append(f'<a class="band p{i%4}" href="#{hid}"><span class="k">{html.escape(key)}</span><span class="t">{html.escape(short)}</span></a>')
rail = "\n".join(bands)

page = f"""<title>Guang Jie Geotech Playbook</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--paper:#F2F4F3;--ink:#1B262C;--mute:#5B6B70;--line:#C6D0CD;--sea:#0D6E6A;--soil:#A9631C;--tint:#E4E9E7;--tint2:#D9E6E4;--tint3:#EFE4D6;--tint4:#E8E2DA}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--paper:#121A1D;--ink:#E3EAE8;--mute:#98A8AC;--line:#2A383D;--sea:#3FC1BB;--soil:#DB9A4A;--tint:#1B262B;--tint2:#183034;--tint3:#2B241B;--tint4:#262A28}}}}
:root[data-theme="dark"]{{--paper:#121A1D;--ink:#E3EAE8;--mute:#98A8AC;--line:#2A383D;--sea:#3FC1BB;--soil:#DB9A4A;--tint:#1B262B;--tint2:#183034;--tint3:#2B241B;--tint4:#262A28}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,"Times New Roman",serif;font-size:17px;line-height:1.55;padding-inline:20px;padding-block:32px 80px}}
.wrap{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr;gap:32px}}
@media (min-width:960px){{.wrap{{grid-template-columns:150px minmax(0,1fr)}}}}
h1,h2,h3,h4{{font-family:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;line-height:1.1;text-wrap:balance;margin:0}}
h1{{font-size:clamp(34px,5vw,52px);font-weight:700;letter-spacing:-.01em}}
h2{{font-size:28px;font-weight:600;margin-top:56px;padding-top:14px;border-top:2px solid var(--ink);display:flex;gap:12px;align-items:baseline}}
h2::before{{content:"";width:14px;height:14px;flex:none;background:var(--sea);transform:translateY(-1px)}}
h2:nth-of-type(2n)::before{{background:var(--soil)}}
h3{{font-size:21px;font-weight:600;margin-top:32px;color:var(--ink)}}
h4{{font-size:17px;font-weight:600;margin-top:22px;color:var(--sea);text-transform:uppercase;letter-spacing:.04em}}
p,li{{max-width:68ch}} p{{margin:14px 0}}
ul,ol{{padding-left:22px;margin:12px 0}} li{{margin:6px 0}}
a{{color:var(--sea);text-decoration-thickness:1px;text-underline-offset:2px}}
strong{{font-weight:600}}
code{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:.86em;background:var(--tint);padding:1px 5px;border-radius:3px}}
blockquote{{margin:14px 0;padding:10px 16px;border-left:3px solid var(--soil);background:var(--tint);max-width:68ch;font-style:italic}}
blockquote p{{margin:0}}
.tbl{{overflow-x:auto;margin:18px 0;border-top:1px solid var(--ink)}}
table{{border-collapse:collapse;width:100%;font-family:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;font-size:15.5px;line-height:1.35;font-variant-numeric:tabular-nums}}
th{{text-align:left;font-weight:600;text-transform:uppercase;letter-spacing:.05em;font-size:12.5px;color:var(--mute);padding:8px 10px 6px;border-bottom:1px solid var(--line);vertical-align:bottom}}
td{{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
td:first-child{{white-space:nowrap}}
tr:hover td{{background:var(--tint)}}
/* title block, drawn like a drawing title block */
.tb{{border:1.5px solid var(--ink);display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin:22px 0 8px}}
.tb div{{padding:8px 12px;border-right:1px solid var(--line);border-top:1px solid var(--line)}}
.tb div:first-child{{grid-column:1/-1;border-top:0;padding:14px 12px 10px}}
.tb .l{{display:block;font-family:"Barlow Semi Condensed",Arial,sans-serif;font-size:11.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--mute)}}
.tb .v{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:14px}}
.lede{{font-size:19px;max-width:66ch;color:var(--ink);margin-top:18px}}
/* borehole-log rail */
.rail{{display:none}}
@media (min-width:960px){{.rail{{display:block;position:sticky;top:24px;align-self:start}}
.rail .scale{{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--mute);display:flex;justify-content:space-between;padding:0 2px 4px;border-bottom:1px solid var(--ink)}}
.band{{display:flex;flex-direction:column;justify-content:center;gap:2px;min-height:52px;padding:6px 8px;border:1px solid var(--line);border-top:0;text-decoration:none;color:var(--ink);background-color:var(--tint)}}
.band.p0{{background-image:repeating-linear-gradient(45deg,transparent 0 6px,rgba(13,110,106,.18) 6px 7px)}}
.band.p1{{background-image:radial-gradient(rgba(169,99,28,.35) 1px,transparent 1.5px);background-size:8px 8px}}
.band.p2{{background-image:repeating-linear-gradient(0deg,transparent 0 5px,rgba(13,110,106,.16) 5px 6px)}}
.band.p3{{background-image:repeating-linear-gradient(-45deg,transparent 0 6px,rgba(169,99,28,.22) 6px 7px)}}
.band:hover,.band:focus-visible{{outline:2px solid var(--sea);outline-offset:-2px}}
.band .k{{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--mute)}}
.band .t{{font-family:"Barlow Semi Condensed",Arial,sans-serif;font-size:13px;font-weight:600;line-height:1.15}}
.rail .foot{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;color:var(--mute);padding:6px 2px;border-top:1px solid var(--ink)}}}}
:focus-visible{{outline:2px solid var(--sea);outline-offset:2px}}
@media (prefers-reduced-motion:no-preference){{html{{scroll-behavior:smooth}}}}
@media print{{.rail{{display:none}} .wrap{{display:block}} body{{padding:0;font-size:11pt;background:#fff;color:#111}} h2{{break-after:avoid}} tr{{break-inside:avoid}} a{{color:inherit}}}}
</style>
<div class="wrap">
<nav class="rail" aria-label="Sections">
<div class="scale"><span>LOG</span><span>SECTION</span></div>
{rail}
<div class="foot">Strata are sections, not soils.</div>
</nav>
<main>
<h1>Guang Jie Geotech Playbook</h1>
<div class="tb">
<div><span class="l">Project</span><span class="v">Paid work for an independent geotechnical engineer, 2026–27</span></div>
<div><span class="l">Prepared for</span><span class="v">Tuang Guang Jie</span></div>
<div><span class="l">Prepared by</span><span class="v">Laminar Flow</span></div>
<div><span class="l">Date</span><span class="v">14 Sep 2026</span></div>
<div><span class="l">Revision</span><span class="v">1 · for discussion</span></div>
</div>
<p class="lede">Where the soil work is this year, what each job pays, the nine things his skills sell as, the directions worth exploring, and a 30-day outreach plan with the radar, target list and drafts already built.</p>
{body_html}
</main>
</div>
"""
page = page.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
open("PLAYBOOK.html", "w").write(page)

# print version: plain CSS that LibreOffice's HTML import understands
print_html = f"""<html><head><meta charset="utf-8"><title>Guang Jie Geotech Playbook</title>
<style>body{{font-family:Liberation Serif,serif;font-size:11pt;line-height:1.4}} h1{{font-family:Liberation Sans,sans-serif;font-size:22pt}} h2{{font-family:Liberation Sans,sans-serif;font-size:15pt;margin-top:22pt;border-top:1.5pt solid #000;padding-top:6pt}} h3{{font-family:Liberation Sans,sans-serif;font-size:12.5pt}} h4{{font-family:Liberation Sans,sans-serif;font-size:11pt;color:#0D6E6A}} table{{border-collapse:collapse;width:100%;font-family:Liberation Sans,sans-serif;font-size:9pt}} th,td{{border:0.5pt solid #999;padding:3pt 5pt;vertical-align:top;text-align:left}} th{{background:#e8e8e8}} blockquote{{margin:8pt 18pt;font-style:italic}} code{{font-family:Liberation Mono,monospace;font-size:9.5pt}}</style></head>
<body><h1>Guang Jie Geotech Playbook</h1>
<p><b>Prepared for:</b> Tuang Guang Jie &nbsp;|&nbsp; <b>Prepared by:</b> Laminar Flow &nbsp;|&nbsp; <b>Date:</b> 14 September 2026 &nbsp;|&nbsp; <b>Revision:</b> 1, for discussion</p>
{body_html}</body></html>"""
open("PLAYBOOK_print.html", "w").write(print_html)
print("built: PLAYBOOK.md, PLAYBOOK.html, PLAYBOOK_print.html;", len(h2s), "sections;", len(p1), "priority-1 targets")
