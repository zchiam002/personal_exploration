# Collaborating with an Offshore Geotechnical Freelancer — a Laminar Flow Assessment

**Date:** 14 September 2026
**Subject:** Tuang Guang Jie (cousin), freelance offshore/nearshore/onshore geotechnical engineer, ~20 years, Singapore. Reports work is slow.
**Question:** Is there a collaboration that makes sense from a Laminar Flow perspective, and if so, which one first?

> **Working assumption.** "Laminar Flow" is taken to mean our own venture: ML, optimization and physics-informed modelling applied to engineering and industrial systems, in the style of the water-treatment and JTC precast assessments in this repo. Nothing in the repo or mailbox defines it, so if the venture's positioning is narrower than that, re-read §4 with that lens.

---

## 1. Verdict

**Yes, but not as an "AI project". The first collaboration should be a plain automation product wrapped around one calculation he already sells: jack-up leg penetration assessment. Budget it as a 6-week, near-zero-cash probe, gated on him pre-selling two jobs.**

Four facts drive this:

1. **His slowdown is cyclical and sector-specific, not a verdict on him.** Offshore wind, which absorbed most APAC geotechnical survey capacity from 2021–2024, is in a documented slump. Fugro's offshore-wind backlog is down 47 % year-on-year and the company says recovery may not arrive before 2027. Taiwan's Round 3.1 shrank from 8.7 GW awarded to ~2.3 GW proceeding; Japan cancelled 1.7 GW of Round 1 and postponed Round 4; Korea is still designating zones. Freelance day-rate roles are the first line item cut and the first restored. **The trough is likely 12–18 months. The right use of it is building assets, not waiting.**
2. **The oil-and-gas jack-up market is flat, not falling.** Global marketed jack-up utilization is ~88–90 % and forecast flat through 2026, with demand concentrated in the Middle East, India, Asia Pacific and NW Europe. Every rig move to a new location needs a site-specific leg-penetration assessment under ISO 19905-1. That is a steady, repeating, well-specified calculation that he has done for 14 years.
3. **The tooling for that calculation is locked inside consultancies.** Cathie (JACA, >1,500 assessments delivered), DNV, Ryder Engineering (in-house software) and CASK Software (Spudpen kernel) all sell the *service* or an enterprise licence. None of them sells an independent engineer a cheap, fast, data-to-report pipeline. That is a gap a two-person team can fill in weeks, because the value is automation and turnaround, not novel science.
4. **The "AI for geotech" headline market is real but academic, and mostly not his problem.** Published 2025–26 work (MapCPT for CPT stratigraphy, SchemaGAN, physics-informed drivability ML, Fugro's AI lab-testing) is either a research prototype or a Fugro-internal capability. A freelancer's binding constraint is *hours of unbilled manual work per job and sales reach*, not model accuracy. This mirrors the lesson from the water-treatment report: the biggest lever often needs no ML at all.

**Do not** start with a physics-informed ML research product (§4C). It is the most Laminar-Flow-shaped option and the least likely to pay him anything in 2026. Keep it as the second act, funded by the first.

---

## 2. Why work is slow right now (evidence)

| Signal | What it says | Source |
|---|---|---|
| Fugro H1 2026 | Revenue +4.3 % on oil & gas, infrastructure and water; 12-month backlog −13.9 %; **offshore wind backlog −47 %**; 5–7 vessels into winter layup; recovery "may take until 2027" | [Baird Maritime](https://www.bairdmaritime.com/offshore/renewables/offshore-wind/fugro-says-offshore-wind-slump-has-worsened-recovery-may-take-until-2027), [Windpower NL](https://windpowernl.com/2026/07/31/fugro-reports-stronger-first-half-margin-but-warns-of-weaker-second-half-as-offshore-wind-slowdown-continues/) |
| Taiwan Round 3.1 | 8.7 GW selected (Dec 2022) → ~2.3 GW proceeding; 2030 target cut 13.1 → 10.9 GW; Youde 700 MW contract being terminated (Aug 2026) | [Westwood](https://www.westwoodenergy.com/news/infographics/what-happened-in-taiwans-round-3-phase-1-leasing-round), [offshoreWIND.biz](https://www.offshorewind.biz/2026/08/26/taiwan-moves-to-terminate-contract-for-700-mw-offshore-wind-project/) |
| Japan | Mitsubishi consortium cancelled 1.7 GW of Round 1; Round 4 postponed pending auction reform | [White & Case](https://www.whitecase.com/insight-alert/japan-offshore-wind-update-round-3-results), [Aegir Insights](https://www.aegirinsights.com/outlook-for-offshore-wind-in-japan-in-2026) |
| Korea | 1.786 GW awarded in H1 2026 auction; first 2–3 GW of preliminary zones designated by end-2026 — survey demand is coming, not here yet | [Windtech International](https://www.windtech-international.com/industry-news/korea-selects-1-786-gw-in-first-half-2026-offshore-wind-auction) |
| Jack-ups (O&G) | Marketed supply 395 → 405 rigs; utilization 89 % → 90 %; "no drastic declines, no significant upticks" | [Westwood](https://www.westwoodenergy.com/news/westwood-insight/westwood-insight-as-2025-challenges-fade-offshore-rig-outlook-brightens), [Drilling Contractor](https://drillingcontractor.org/offshore-likely-to-remain-a-waiting-game-until-expected-uptick-in-2027-75703) |
| Singapore local | Long Island (800 ha) preparatory works from end-2026; Pulau Tekong 800 ha polder; Northern Tuas Basin reclamation instrumentation tenders | [URA](https://www.ura.gov.sg/land-planning/planning-strategies/urban-resilience/long-island/), [Malay Mail](https://www.malaymail.com/news/singapore/2026/03/30/singapore-begins-preparatory-works-for-long-island-coastal-project-before-full-reclamation-phase/214454) |

Reading: his offshore-wind pipeline has collapsed with everyone else's; oil-and-gas rig work is steady but competed; Singapore nearshore reclamation is a genuine 2027–2030 onshore/nearshore opportunity that fits the "Nearshore/Onshore" he already lists.

Market-size reports (e.g. Fortune Business Insights' USD 154 M global "geotechnical services for offshore wind" figure) are unaudited and should not be used for planning; they are noted here only because they will come up.

---

## 3. What each side brings

### 3.1 Him (from LinkedIn)

- **Repeat, codifiable analyses** he has delivered for 14 years as freelancer/lead engineer: jack-up leg penetration, pile capacity, pile driveability, pile ageing (set-up), mudmat stability for subsea structures, conductor setting depth, factual and interpretive reporting, third-party engineering QC.
- **Data literacy** at the source: soil classification, lab and in-situ test processing, Fugro in-house tools (JURIG3, APICAP, Uniplot, Geodin), gINT.
- **Client-side credibility**: client site representative and QC roles, tender support at FOSTA, PUB sewer project management, 9 years as a Commando platoon sergeant / CSM. He can sit opposite a rig mover or a developer's package manager and be believed.
- **Network**: Fugro alumni, "various offshore geotechnical companies" 2012–2016 and 2018–present, 809 followers. Small, but exactly the buyer list for §4A.
- **Availability**: 14-day mobilisation, currently idle capacity.

### 3.2 Us (Laminar Flow)

- Software and data engineering; can turn a spreadsheet method into a validated Python kernel with a report generator in weeks.
- Physics-informed ML and optimization; literature-synthesis and evidence-grading discipline (see the water-treatment and NeSy reviews).
- LLM tooling for document drafting and structured extraction.
- No geotechnical licence, no professional-indemnity cover, no offshore network. **Every deliverable that goes to a client must carry his name and review.**

---

## 4. Collaboration shapes, ranked

### A. Leg-penetration assessment as a productized service — **do this first**

**What:** A pipeline that takes the site investigation data (AGS 4 / CPT and borehole logs), the rig's spudcan geometry and preload, and produces an ISO 19905-1 spudcan penetration prediction (bearing capacity profile, punch-through and squeezing checks, backflow, predicted penetration band, extraction notes) plus a draft report in his template. He reviews, adjusts soil parameters, signs. Later extend to ISO 19905-4 (installation/removal), which is at FDIS stage.

**Why first:**
- Demand is steady (O&G jack-up utilization ~90 %) and independent of the wind slump.
- He has done it many times, so the method, sanity checks and edge cases are in his head; we only have to encode them.
- The calculation is well specified by a public standard; the failure modes (punch-through in sand-over-clay, squeezing in thin clay, sand plug formation) are documented, e.g. the City St George's jack-up conference papers.
- Competitors sell it as a consultancy service (Cathie's JACA, DNV, Ryder) or an enterprise kernel (CASK Spudpen). A fast, fixed-price, independent-engineer offering with a 48-hour turnaround is a real positioning, not a feature-parity fight.

**What Laminar Flow gets:** a first paying, shippable product in a physical-systems domain; a validation dataset of real assessments; a domain partner for offshore/marine work.

**Effort:** 3–5 weeks for a kernel plus report generator, if he supplies 3–5 past assessments (anonymised) as regression tests. No ML in v1.

**Kill criteria:** he cannot pre-sell two assessments to his contacts at a fixed price within 4 weeks of a working demo; or the past-job archive cannot be used because of client confidentiality (see §6).

### B. Factual-report and CPT-interpretation automation for SI contractors — **second**

**What:** For small and mid-size site-investigation contractors (the FOSTA tier in Singapore and SEA): AGS in → automated QC (unit checks, depth continuity, duplicate tests), Robertson SBT/Ic stratigraphy, parameter derivation tables, borehole logs and a draft factual report with LLM-drafted narrative sections, under his review. This is what MapCPT does for CPT, but end-to-end and for the buyer who actually pays: the contractor who owes a report in ten days.

**Why second:** more buyers, but longer sales cycles, and Bentley OpenGround / Datgel already cover the data-management half; we would compete on the "last mile" of report writing. The Singapore nearshore reclamation programme (Long Island, Tekong, Tuas) from end-2026 creates local demand he can walk into as client rep / QC, and a report-automation tool is what makes a one-person QC shop scale.

**Effort:** 6–10 weeks to a credible demo; needs one contractor as design partner.

### C. Physics-informed ML on installation data — **later, funded by A/B**

**What:** The Laminar-Flow-shaped research product: predicting pile driveability and set-up (ageing) from CPT with physics-guided features, or jack-up penetration bands with uncertainty from pooled assessments. There is fresh literature to stand on (2026 physics-informed feature engineering for offshore pile drivability from CPT; 143-monopile Chinese dataset with a physics-regularized network; ML-based CPTu stratigraphy).

**Why not first:** it needs data we do not own (installation records belong to contractors and developers), it pays nothing in 2026, and its buyers (developers, Tier-1 consultancies) are precisely the ones cutting spend. Its right form in the next 12 months is a **co-authored white paper or conference paper** built on the A/B datasets, used as marketing for both of us when the wind market returns in 2027.

### D. Consulting pairing: he becomes Laminar Flow's geotechnical/marine domain lead — **do this in parallel, costs nothing**

The JTC precast assessment in this repo explicitly budgeted a "domain advisor on retainer". He is that person for anything marine, foundations, reclamation or offshore. Concretely:
- He fronts geotechnical and marine bids where a PE-adjacent engineering face is needed; we front the data/software scope.
- We co-bid offshore-wind QC and data-management packages in Korea/Japan/Taiwan when tendering resumes in 2027.
- Revenue share per engagement, no salary, no equity until A or B has revenue.

### E. Training/knowledge product — **skip**

A course on jack-up SSA for young engineers would sell a few hundred dollars at a time to a tiny audience. Not worth either person's hours.

---

## 5. The 6-week probe

| Week | Step | Owner | Output |
|---|---|---|---|
| 1 | 2-hour structured interview: walk through his last 5 leg-penetration jobs, time per stage, where the hours go, what the client actually asks for | Both | Process map; list of inputs/outputs; the "must never get wrong" checks |
| 1 | Confidentiality triage: which past jobs can be used as anonymised regression cases | Him | 3–5 test cases |
| 2–3 | Build kernel v0: soil profile parametrisation, ISO 19905-1 bearing-capacity profile, punch-through and squeezing checks, penetration band | Us | Python package, tests against his cases |
| 3–4 | Report generator in his template; parameter-review UI (a notebook is fine) | Us | Draft report in <1 hour from AGS input |
| 4 | He runs one live or recent job through it in parallel with his manual method | Him | Discrepancy log |
| 5 | Price and pitch: fixed-price assessment, 48-hour turnaround; he contacts 5–10 rig movers / marine warranty surveyors / drilling contractors | Him | 2 pre-sold jobs or a no-go |
| 6 | Go/no-go; if go, agree the terms in §6 and start B | Both | Decision |

Cash cost is essentially zero. Time cost is ~3 weeks of ours and ~1 week of his.

---

## 6. Things to settle before anything ships (family plus money)

- **Liability.** The signed report is his. He should confirm his professional-indemnity position as a self-employed engineer before the first paid job. We supply a tool; we do not sign calculations.
- **Client confidentiality.** Past reports belong to the clients. Use them only in anonymised, geometry-perturbed form, or ask permission. Do not pool client data into a training set without written consent.
- **Standards.** ISO 19905-1:2023 and the API/ISO pile-design standards are paid documents; buy them, do not reproduce their text.
- **Split.** Suggest: assessment revenue split by hours contributed for the first six jobs, then a fixed per-job licence fee to Laminar Flow; tool IP stays with Laminar Flow, his templates and methods stay his. Write it down before job one.
- **Sales.** He is the only person who can sell this. If he does not want to make calls, option A dies regardless of the software; be honest about that in week 1.
- **Scope discipline.** The tool encodes *his* judgement. Every "the software should decide this" is a place where the engineer should decide and the software should show its working.

---

## 7. Message to send him (draft)

> Jie — I read through your profile properly. Work being slow is the whole offshore wind sector right now (Fugro's wind backlog is down nearly half and they're saying 2027 before it turns), so it's not you. Two ideas while it's quiet: (1) let me turn your leg-penetration assessment into a tool that takes the SI data and gives you a draft report in an hour, so you can sell fixed-price 48-hour assessments to the rig movers you know; (2) when tenders come back, we bid together — you on the engineering, me on the data and software side. Can we do a two-hour session next week where you walk me through your last few jack-up jobs? Bring any past reports you're allowed to share.

---

## 8. Sources

- Fugro H1 2026 and offshore-wind outlook: [Baird Maritime](https://www.bairdmaritime.com/offshore/renewables/offshore-wind/fugro-says-offshore-wind-slump-has-worsened-recovery-may-take-until-2027), [Marine Technology News](https://www.marinetechnologynews.com/news/fugro-forecasts-offshore-recovery-664748), [Windpower NL](https://windpowernl.com/2026/07/31/fugro-reports-stronger-first-half-margin-but-warns-of-weaker-second-half-as-offshore-wind-slowdown-continues/), [First Break](https://www.firstbreak.org/article-news-article/a-0002058---2026-07-31-11-56-47z-MCQM6EXSSYWJFAPGX652IHAMJPPE)
- Jack-up market: [Westwood Insight](https://www.westwoodenergy.com/news/westwood-insight/westwood-insight-as-2025-challenges-fade-offshore-rig-outlook-brightens), [Drilling Contractor](https://drillingcontractor.org/offshore-likely-to-remain-a-waiting-game-until-expected-uptick-in-2027-75703), [World Oil on Middle East jack-ups](https://www.worldoil.com/magazine/2026/february/special-focus-2026-forecast-review/middle-east-jackup-fleet-continues-to-shrink-following-saudi-suspensions/)
- APAC offshore wind status: [Westwood on Taiwan Round 3.1](https://www.westwoodenergy.com/news/infographics/what-happened-in-taiwans-round-3-phase-1-leasing-round), [offshoreWIND.biz on Youde termination](https://www.offshorewind.biz/2026/08/26/taiwan-moves-to-terminate-contract-for-700-mw-offshore-wind-project/), [offshoreindustry.co.uk on Taiwan Zone 3](https://offshoreindustry.co.uk/taiwan-offshore-wind-zone-3-project-delays-local-content-rules-and-the-developer-shakeout-in-asias-most-contested-market/), [White & Case on Japan Round 3](https://www.whitecase.com/insight-alert/japan-offshore-wind-update-round-3-results), [Aegir Insights on Japan 2026](https://www.aegirinsights.com/outlook-for-offshore-wind-in-japan-in-2026), [Windtech on Korea H1 2026 auction](https://www.windtech-international.com/industry-news/korea-selects-1-786-gw-in-first-half-2026-offshore-wind-auction), [Offshore Energy on Ørsted Incheon surveys](https://www.offshore-energy.biz/geotechnical-surveys-wrap-up-at-orsteds-1-4-gw-offshore-wind-project-in-south-korea/)
- Singapore reclamation: [URA Long Island](https://www.ura.gov.sg/land-planning/planning-strategies/urban-resilience/long-island/), [Malay Mail, Long Island prep works](https://www.malaymail.com/news/singapore/2026/03/30/singapore-begins-preparatory-works-for-long-island-coastal-project-before-full-reclamation-phase/214454), [Malay Mail, Pulau Tekong polder](https://www.malaymail.com/news/singapore/2025/09/08/singapore-reclaims-800ha-at-pulau-tekong-in-first-below-sea-level-project-to-cut-sand-use/190428), [Northern Tuas Basin monitoring tender](https://www.business.gov.uk/export-opportunities/opportunities/instrument-monitoring-works-for-proposed-reclamation-at-northern-tuas-basin)
- Jack-up SSA tooling and standard: [ISO 19905-1](https://www.iso.org/standard/34592.html), [ISO/FDIS 19905-4](https://www.iso.org/standard/86742.html), [Cathie SSA / JACA](https://cathiegroup.com/solutions/installation/jack-ups-site-specific-assessment/), [DNV jack-up engineering](https://www.dnv.com/services/jack-up-and-geotechnical-engineering-9466/), [Ryder Engineering](https://ryder.engineering/services/jack-up-analysis/), [CASK Software](https://www.casksoftware.com/), [City St George's jack-up papers: trapped soil plug](https://jack-up.citystgeorges.ac.uk/wp-content/uploads/2025/09/Jackup-2019-01.pdf), [leg penetration and extraction experience](https://jack-up.citystgeorges.ac.uk/wp-content/uploads/2025/09/Jackup-2017-10.pdf)
- AI/ML in geotechnics: [MapCPT (Sci. Rep. 2026, PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13338442/), [AI-enhanced soil classification with incomplete CPT data for offshore wind (Sci. Rep. 2026)](https://www.nature.com/articles/s41598-026-46356-6), [AI transformations in geotechnics review (Computers and Geotechnics 2025)](https://www.sciencedirect.com/science/article/pii/S0266352X25005531), [Fugro AI in soil lab testing](https://www.fugro.com/news/long-reads/2025/transforming-soil-lab-testing-with-ai-technology), [Physics-informed features for offshore pile drivability from CPT (2026)](https://www.sciencedirect.com/science/article/pii/S3050483X2600047X), [Physics-guided ML for monopile self-weight penetration (JMSE 2026)](https://www.mdpi.com/2077-1312/14/17/1607), [GRLWEAP](https://www.pile.com/products/grlweap/)
- Geotechnical data management: [Bentley OpenGround via Datgel](https://www.datgel.com/openground), [Datgel DGD Tool](https://www.datgel.com/datgel-dgd-tool-whats-new)
- Market-size reports (unaudited, for reference only): [Fortune Business Insights](https://www.fortunebusinessinsights.com/geotechnical-services-for-offshore-wind-market-108863)
