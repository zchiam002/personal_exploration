# Getting Him Jobs First — a 30-Day Plan

**Date:** 14 September 2026
**Goal:** paid work for Tuang Guang Jie within 30–60 days. Product ideas (see `collaboration_assessment.md`) wait until he is billing again.
**Laminar Flow's role:** build the demand radar, the target list and the outreach machine; he does the calls and the engineering.

---

## 1. Verdict

**The fastest route to income is not offshore wind and not a product. It is trigger-based direct outreach into the pockets of the market that are hiring now, backed by registrations with the four or five agencies that actually place offshore geotechnical client reps, plus expert-network calls for cash flow.** Laminar Flow's contribution is to make his outreach specific and timely: a daily feed of contract awards and campaign starts, a named target list, and drafted messages that reference the trigger. Generic "open to work" posts do not compete with laid-off Fugro engineers. A message that says "you just won the Petronas CCS soil-investigation frame; I have done jack-up assessments and driveability in Sarawak waters" does.

Income sequencing, fastest first:

| Horizon | Channel | Why it pays first |
|---|---|---|
| 1–2 weeks | Expert-network calls (GLG, AlphaSights, Guidepoint, Dialectica, Coleman) | Investors are trying to understand the offshore-wind slump and APAC supply chains; USD 200–500/hour, no mobilisation |
| 2–6 weeks | Agency-placed client rep / QC rotations (Atlas Professionals, NES Fircroft, Airswift, Brunel, SA World) | These agencies hold the framework contracts with developers and contractors; freelancers are placed from their pools |
| 3–8 weeks | Direct outreach to contractors and marine-warranty firms on live triggers | Fewer competitors per message; he has the credentials for third-party review and SSA |
| 4–12 weeks | Singapore public and nearshore work (Long Island, Tekong, Tuas; GeBIZ soil-investigation term contracts) | Local, onshore/nearshore, no vessel dependency; needs a contractor or consultant to hire him as engineer/QC |

---

## 2. Where the work is right now (evidence)

The offshore-wind pipeline is the slow part. These are not:

- **Malaysia CCS.** HELMS Geomarine won a 3+2-year offshore soil-investigation frame from PETRONAS CCS Solutions (June 2026), explicitly covering drilling and sampling, downhole CPTu, lab testing, **pile capacity and jack-up assessments, driveability and reporting**. HELMS also ran geotechnical drilling in Sarawak waters (Jan–Mar 2026) for jack-up P&A campaigns. This is his CV, line for line. ExxonMobil is advancing offshore CO2 storage in both Indonesia and Malaysia; Japan–Malaysia cross-border CCS is being planned.
- **Malaysia decommissioning.** PETRONAS Carigali is tendering removal of up to 31 platforms across Sarawak, Sabah and Peninsular Malaysia; ~35 platforms exceed 40 years old. Every jack-up or heavy-lift positioning next to an old platform needs a site-specific assessment and often a client rep.
- **Australia decommissioning.** Allseas is preparing Bass Strait lifts (12 topsides, 11 jackets, ~60,000 t) for 2027, with ABL doing vessel suitability surveys; the Northern Endeavour Phase 3a tender was published 14 Aug 2026. Geotechnical support for vessel positioning and mooring is a 2026–27 need.
- **Oil-and-gas drilling.** Aramco restarting eight suspended jack-ups in 2026; Malaysia needs ~9 jack-ups in 2026 (Chevron's North Malay campaign on NAGA 8 from Aug 2026); PETRONAS launched its 2026 bid round with exploration drilling to follow. India's ONGC has cancelled four jack-up tenders since 2024 over pricing, so treat India as unpredictable.
- **Offshore wind survivors.** Fugro is running the FengMiao II (CIP, Taiwan Round 3.2) SI campaign through Q3 2026; Ørsted's Incheon 1.4 GW surveys were completed by Fugro UST21; Korea awarded 1.786 GW in H1 2026 and will designate preliminary zones by end-2026; Japan's Round 3 winners (Aomori South, Yuza) need site investigation. Fewer jobs, but the ones that exist need client reps and QC.
- **Singapore nearshore.** Long Island preparatory works (800 ha) start end-2026 west of Bedok Jetty; Pulau Tekong's 800 ha polder reclamation; Northern Tuas Basin reclamation instrumentation. Nearshore SI, instrumentation monitoring and reclamation QC are onshore-adjacent roles he already lists.
- **Subsea cables.** Singapore has cable landings scheduled for 2026–28 to SE Asia, the US/Guam, the Middle East and Australia; route surveys need geotechnical client reps and burial-assessment reviewers.

Sources in §8.

---

## 3. What Laminar Flow builds (this week)

### 3.1 Opportunity radar — built, in this folder

`opportunity_radar.py` pulls seven industry feeds (offshore-energy.biz, OE Digital, Ground Engineering, Hydro International, Windpower NL, Rigzone, Baird Maritime), gates on geotechnical content, weights triggers (awards, rig moves, decommissioning, CCS, cables, reclamation), geography and named buyers, and prints a ranked digest. Standard library only; run it daily from cron and forward the digest.

Known limits of v0, to fix next:
- Free RSS feeds are Europe-heavy. Add Asia sources: PETRONAS media releases, Offshore Energy's Asia-Pacific tag, Upstream/Energy Voice Asia, GeBIZ e-mail alerts for "soil investigation" and "site investigation", AusTender keyword alerts, Esgian/Westwood rig-move round-ups, and LinkedIn saved-search e-mails (parse the mailbox, not the site).
- Scoring is keyword-based. Once there are ~50 labelled hits, replace with an LLM pass that extracts {company, project, location, scope, phase} and drafts the outreach message in one step.

### 3.2 Target account list (spreadsheet, ~80 rows, owner: us; he corrects it)

Columns: company, segment, why-now trigger, role that hires (ops manager / geotech dept head / project manager / MWS lead), named contact if known, channel (agency / direct / LinkedIn), status, last touch.

Seed segments:
- **SEA geotechnical contractors:** HELMS Geomarine (KL), Asian Geos (Gardline partner), Fugro Singapore/Malaysia, Geoquip Marine, Gardline, Benthic, EGS, Horizon Geosciences, Sinotech/TSI (Taiwan), Fugro UST21 (Korea).
- **Marine warranty and rig-move consultancies:** ABL, DNV, Global Maritime, LOC, Cathie, Ryder Engineering, Noble Denton legacy teams. They subcontract independent SSA reviewers.
- **Drilling contractors and rig movers active in SEA/ME:** Velesto, Borr, Valaris, Shelf Drilling, Japan Drilling, ADES, Sapura.
- **Decommissioning:** PETRONAS Carigali decom team and its EPRD contractors; Allseas and ABL (Bass Strait); Northern Endeavour Phase 3a bidders.
- **CCS:** PETRONAS CCS Solutions; ExxonMobil Indonesia/Malaysia CCS; Pertamina; Japanese off-takers' engineering contractors (JGC, Chiyoda).
- **Offshore wind developers with live SI in APAC:** CIP (Taiwan), Ørsted (Korea), Corio, JERA/Tohoku (Aomori), Marubeni/bp (Yuza), Equis/Vena.
- **Singapore nearshore:** HDB/URA Long Island consultants and main contractors once appointed; Tekong polder contractors; PUB coastal; Tuas instrumentation contractors; local SI firms (FOSTA, Geospecs, Soil & Foundation, GIE).
- **Cable:** SubCom, ASN, NEC, HMN Tech route-survey subcontractors landing in Singapore; Sun Cable / AAPowerLink route-survey contractors.

### 3.3 Outreach kit (owner: us, he approves)

- **Two CVs.** One for client rep / QC (leads with 7 years as client rep, rig moves, offshore drilling supervision, Commando leadership). One for engineering analysis (leads with SSA, pile capacity, driveability, ageing, mudmat, tools).
- **One-page capability statement** (PDF) with a fixed-price menu so he can be hired without a vessel: leg-penetration assessment, independent report review, driveability check, mudmat stability check, 48-hour turnaround.
- **LinkedIn rewrite.** Headline with searchable terms ("Offshore Geotechnical Client Representative | Jack-up SSA | Pile Design | Available 14 days"), "Open to work" set for recruiters, location set to Singapore with willingness to travel, skills section matching agency Boolean searches (CPT, AGS, ISO 19905, API RP 2GEO, GRLWEAP, gINT).
- **Trigger-based messages.** For each radar hit, a 5-line message naming the project, one relevant past job, availability, and one concrete offer. We draft, he edits and sends from his own accounts.

### 3.4 Registrations (owner: him, 1 day)

Atlas Professionals / Atlas NextWave; NES Fircroft (Singapore, Malaysia, Japan offices); Airswift; Brunel; SA World (client rep geophysical/geotechnical); Spencer Ogden; Rigzone profile. Expert networks: GLG, AlphaSights, Guidepoint, Dialectica, Coleman, Third Bridge. Pitch topic list for the networks: APAC offshore-wind SI supply chain and vessel utilisation, jack-up SSA practice, CCS site characterisation, Singapore reclamation.

---

## 4. Weekly cadence and targets

| Week | Him | Us | Target |
|---|---|---|---|
| 1 | Register with agencies and expert networks; approve CVs and LinkedIn rewrite | Deliver CVs, capability statement, target list v1, radar running daily | 6 agency registrations, 3 expert-network profiles live |
| 2 | 10 trigger-based direct messages; 3 recruiter calls | Draft messages from radar hits; add Asia sources | 10 sent, 3 replies |
| 3 | 10 more messages; follow-ups at day 7 | Add LLM extraction; maintain tracker | 1 expert call booked, 2 interviews or scoping calls |
| 4 | Same; price the first fixed-price job | Review pipeline; adjust segments that are not responding | 1 paid engagement of any size |

If by day 30 there is no reply from a segment, drop it and double the segments that replied.

---

## 5. Honest constraints

- **Local content.** PETRONAS and Indonesian work favours nationals; his edge there is third-party review and SSA delivered remotely from Singapore, not offshore rotations. Taiwan and Korea similarly favour local partners; go through Fugro Taiwan/UST21 or the developer's owner's-engineer rather than direct.
- **Competition.** Fugro is laying up 5–7 vessels and cutting €50 M; experienced engineers are entering the same freelance pool. Speed and specificity of outreach are the only durable advantages.
- **Rates.** Day rates will be under pressure; the fixed-price menu protects him from pure day-rate competition.
- **He must do the selling.** The radar and drafts remove the research and writing burden, not the sending. Confirm in week 1 that he will send 10 messages a week.
- **Feeds.** The v0 radar under-covers Asia. Treat the first two weeks of digests as calibration.

---

## 6. Message templates

**Agency registration note**
> Offshore geotechnical engineer, 20 years, Singapore-based, available on 14 days' notice. Client representative and QC on offshore, nearshore and onshore soil investigations since 2018; earlier lead engineer and site manager on rig moves and SI campaigns across SE Asia, Australia, India and the Gulf of Mexico; Fugro-trained. Analyses: jack-up leg penetration (ISO 19905-1), pile capacity and driveability, pile ageing, mudmat stability, conductor setting depth. Also available for remote third-party review.

**Trigger-based direct message (example, HELMS/PETRONAS CCS)**
> Congratulations on the PETRONAS CCS soil-investigation frame. The scope you announced (downhole CPTu, jack-up assessments, driveability, reporting) is what I have delivered as lead engineer and client rep across SE Asia since 2012, including Sarawak and Sabah campaigns. I am Singapore-based, can mobilise in 14 days, and can also take remote leg-penetration or driveability packages at a fixed price if your engineering team is stretched during the campaign season. Happy to send a one-page capability statement.

**Expert-network profile line**
> Independent offshore geotechnical engineer; 20 years across oil and gas, offshore wind and CCS site investigation in APAC; can speak to survey-vessel supply and demand, SI contractor landscape, jack-up assessment practice, and the effect of the 2025–26 offshore-wind slowdown on APAC geotechnical contractors.

---

## 7. What this sets up

Once he is billing, the fixed-price analysis menu becomes the wedge for the leg-penetration product in `collaboration_assessment.md`, and the radar becomes the sales pipeline for it. Nothing built here is wasted if the product never happens.

---

## 8. Sources

- HELMS / PETRONAS CCS contract: [Ground Engineering](https://www.geplus.co.uk/news/contract-news/helms-awarded-offshore-soil-investigation-contract-for-petronas-ccs-business-30-06-2026/), [Offshore Energy](https://www.offshore-energy.biz/local-company-to-carry-out-soil-investigations-for-malaysian-ccs-developments/), [Carbon Herald](https://carbonherald.com/petronas-taps-helms-geomarine-to-conduct-soil-surveys-for-ccs-projects/)
- Malaysia decommissioning 2026: [Offsnet](https://offsnet.com/content/asia-pacific/malaysias-offshore-decommissioning-accelerates-in-2026)
- ExxonMobil CCS Indonesia/Malaysia: [Oil & Gas Today](https://thaioilgas.com/exxonmobil-indonesia-and-malaysia-advance-large-scale-offshore-carbon-storage-projects/); Japan–Malaysia CCS: [Carbon Herald](https://carbonherald.com/malaysia-and-japan-advance-cross-border-ccs-plan/)
- Australia decommissioning: [Petroleum Australia](https://petroleumaustralia.com.au/news_article/australia-begins-its-largest-offshore-decommissioning-campaign-in-the-bass-strait/), [Offshore Energy on Allseas](https://www.offshore-energy.biz/allseas-begins-prep-work-for-australias-largest-ever-offshore-decommissioning-job/), [Offsnet Australia](https://offsnet.com/content/australia)
- Jack-up market: [Westwood on Aramco suspensions](https://www.westwoodenergy.com/news/westwood-insight-saudi-aramco-jackup-suspensions-and-the-story-so-far), [Offshore Magazine](https://www.offshore-mag.com/rigs/article/55136383/report-jackup-market-remains-resilient-despite-saudi-aramcos-rig-releases), [Focus Malaysia on PETRONAS drilling cycle](https://focusmalaysia.my/petronas-ramps-up-seismic-work-as-malaysia-drilling-cycle-nears-turning-point/), [PETRONAS Bid Round 2026](https://www.petronas.com/media/media-releases/petronas-launches-malaysia-bid-round-2026-strengthening-malaysia-energy), [ONGC tender cancellations](https://www.business-standard.com/companies/news/jack-up-rigs-tender-cancelled-due-to-steep-price-escalation-clarifies-ongc-126042200595_1.html)
- Offshore wind APAC: [Fugro FengMiao II](https://www.fugro.com/news/business-news/2026/fugro-awarded-a-large-geotechnical-site-investigation-contract-for-cip-s-wind-farm-in-taiwan), [Ørsted Incheon surveys](https://www.offshore-energy.biz/geotechnical-surveys-wrap-up-at-orsteds-1-4-gw-offshore-wind-project-in-south-korea/), [Korea H1 2026 auction](https://www.windtech-international.com/industry-news/korea-selects-1-786-gw-in-first-half-2026-offshore-wind-auction), [Japan Round 3](https://www.whitecase.com/insight-alert/japan-offshore-wind-update-round-3-results)
- Singapore nearshore: [URA Long Island](https://www.ura.gov.sg/land-planning/planning-strategies/urban-resilience/long-island/), [Malay Mail on prep works](https://www.malaymail.com/news/singapore/2026/03/30/singapore-begins-preparatory-works-for-long-island-coastal-project-before-full-reclamation-phase/214454), [Tekong polder](https://www.malaymail.com/news/singapore/2025/09/08/singapore-reclaims-800ha-at-pulau-tekong-in-first-below-sea-level-project-to-cut-sand-use/190428), [Northern Tuas Basin instrumentation](https://www.business.gov.uk/export-opportunities/opportunities/instrument-monitoring-works-for-proposed-reclamation-at-northern-tuas-basin), [GeBIZ guide](https://jorpex.com/sources/gebiz/)
- Subsea cables: [CSIS Singapore case study](https://www.csis.org/analysis/strategic-future-subsea-cables-singapore-case-study), [Australia–Singapore interconnector study](https://link.springer.com/article/10.1007/s41825-020-00032-z)
- Agencies and expert networks: [Atlas NextWave client rep vacancy](https://atlasnextwave.com/job/client-rep-geotechnical/), [SA World client rep](https://www.sa-world.com/open-vacancies/open-vacancies-operations/client-representative-geophysical-geotechnical.html), [NES Fircroft Singapore](https://www.nesfircroft.com/regions/recruitment-in-asia/singapore-jobs/), [Expert-network rates](https://expertopportunities.com/expert-network-hourly-rates/), [GrowthMentor expert networks 2026](https://www.growthmentor.com/blog/expert-networks)
- Fugro H1 2026 (competition for freelance pool): [Baird Maritime](https://www.bairdmaritime.com/offshore/renewables/offshore-wind/fugro-says-offshore-wind-slump-has-worsened-recovery-may-take-until-2027)
