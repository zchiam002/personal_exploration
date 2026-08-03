# Feasibility Assessment — JTC IDDTA "Digital Precast & Logistics Tracking" Solution

**Date:** 3 August 2026
**Inputs:** `jtc-precastreq.xlsx` (IDDTA self-assessment form, ~110 requirements — see `requirements_digest.md`), JTC IDDTA webpages, 9-agent research workflow (programme mechanics, competitors, market, hardware, build scope, business case, risk register, adversarial for/against).

---

## 1. Verdict

**Do not start the build today. Run a ≤S$10k, ~1-month gated de-risking track instead, and only commit to building if a paying pilot partner signs first.**

Three facts drive this:

1. **The certification door just closed for ~2 years.** All four incumbent vendors — Capps Solutions (CBOSS), LeapThought (FulcrumHQ), Novade, and Ynomia — were awarded certification on **17 July 2026** with 2-year validity (verified directly on JTC's certified-solutions page). The last known assessment window closed 14 Feb 2026 and no new window is published. The realistic next opening is **~mid-2028** — which, if we choose to pursue this, is actually enough runway to build *and* earn references, rather than entering cold.
2. **Certification is a whitelist, not a contract.** JTC pays nothing. Certified vendors get a Certified Product List entry that is "briefed to project partners during tender briefings" — the actual buyer is the winning main contractor or precaster, 6–18 months downstream. There is no public evidence certification is even mandatory.
3. **The economics don't clear the bar as a certification-led bet.** Estimated Singapore serviceable market: **~S$4–12M/yr total**, already split among four certified incumbents (one of which, LeapThought, also powers JTC's own OPTIMUS CDE). A 3-year P&L on the build-to-cert strategy loses S$1.0–1.9M cumulative even in the optimistic scenario.

**However** — the research surfaced one genuinely interesting gap (§6): Singapore's largest precast factories (Hong Leong Asia's ICPH, Greyform) already pay for digital platforms, but what they bought tracks *workers*, not *components*, and their vendor (Hubble) is not IDDTA-certified. The budget, buyer, and capability gap verifiably coexist. That is worth one month and S$10k to probe — not S$450k on faith.

---

## 2. What the project actually is

- **IDDTA** = Integrated Digital Delivery Technology Alliance, JTC's scheme to pre-certify construction-tech solutions as compliant with its digital requirements and integration standards with **OPTIMUS** (JTC's Connected Data Environment; "O2" in the form = OPTIMUS v2.0, which runs on LeapThought's FulcrumHQ platform).
- The solution: a platform that plans precast production schedules and tracks every component through **shop drawing approval → fabrication → storage → transport → delivery → installation**, with QR/RFID capture, offline-capable mobile apps, no-code workflows and dashboards (wallcharts, S-curves, RAG), QA/QC integration, RSS sign-off, and push integration into JTC's CDE.
- Process: self-assessment form + ACRA report via FormSG → shortlist → **20-min demo + 10-min Q&A** (webpage figure; form says 10-min — clarify) with a live demo environment and realistic datasets → certification valid 2 years.
- **Everything not marked [Desirable] is a critical requirement**, and the form explicitly states that open APIs *without an implemented, working connection* to hardware/CDE/QMS systems = **non-compliant**. No stub demos.

---

## 3. What we would need (the direct answer)

### People
| Role | Commitment |
|---|---|
| Lead/architect (core platform, workflow engine) | Full-time |
| Mobile engineer (React Native, offline-first sync) | Full-time |
| Backend/integrations engineer (RFID pipeline, CDE, exports) | Full-time |
| Frontend engineer (dashboard builder, wallchart) | Full-time |
| PM with construction/DfMA domain knowledge | ~0.5 FTE |
| DevOps | ~0.25 FTE |
| Precast/DfMA domain advisor (contract) | Retainer |
| Later: support org meeting 72-h response, ticketing, escalation | Post-launch |

With 2–3 engineers instead of 4, add 40–60% calendar time. This is effectively **the whole team, off all other work, for 6–16 months**.

### Build (38–60 person-months total; 22–30 PM to a certifiable demo)
- Core multi-tenant SaaS: RBAC, SSO, hash-chained audit log / immutability (4–6 PM)
- Component registry with immutable IDs, 5+ component types, dimensions/logistics constraints, delivery-order attachment (2.5–3.5 PM)
- QR label pipeline + scan-to-record (1–2 PM)
- **RFID fixed-checkpoint integration with a physical rig** — readers → MQTT → dedup/direction inference → platform, ≤60-min sync (3–5 PM) — *cannot be cut*
- **Offline-first mobile, iOS + Android**, photo/GPS metadata, digital signatures (5–8 PM) — *cannot be cut*
- **No-code workflow builder** + configurable QA/QC forms (6–9 PM) — *cannot be cut*
- Master Programme import, planned-vs-actual, Plan % auto-recalc incl. revisions (2–4 PM)
- **Code-free dashboard builder + custom wallchart/S-curve/RAG visuals** (5–8 PM) — *cannot be cut; no BI tool ships JTC's wallchart*
- Reports (PDF/XLSX/CSV bulk), open API + Power BI connectivity (3–5 PM)
- One **real** CDE integration (e.g. Autodesk ACC) + O2 push framework vs mock QAS gateway (2–3 PM)
- Media pipeline for 10k+ photos/project (1–2 PM)
- Load/acceptance testing at stated scale: 1,000 components, 10 isolated projects/tenant, 100 concurrent users (3–5 PM)

Hardest four: the two no-code builders, offline sync colliding with immutability/attribution rules, tenant isolation through the embedded BI layer, and the demonstrable RFID rig.

Suggested stack (boring, fast): Postgres+RLS · NestJS · React · React Native + PowerSync · S3 Object Lock · Keycloak · AWS ap-southeast-1 · SurveyJS (buy) for forms · Metabase Pro/Superset embedded for generic dashboards, custom wallchart · constrained React Flow + XState workflow editor (build).

### Hardware
- **Bench demo rig (the minimum for compliance):** 2 UHF readers (Impinj R700 / Zebra FX9600, ~US$1.5k each), antennas, ~50 concrete-rated tags, MQTT→ingest — **US$3–5k, 2–3 weeks, one engineer**
- Full deployment (1 ICPH + 1 site, ~2,000 components): 4 gate lanes, tags (US$1.50–4 each), edge boxes, printer, 8 rugged handhelds — **US$35–60k** (QR-only variant US$10–15k)
- Physics note: deep-embedded tags won't read through a drive-through gate; surface-mount/shallow cast-in at checkpoints is the workable pattern. Singapore ICPHs today are **QR-first** (Hubble deployments), with RFID mainly in pilots.

### Money
| Item | Estimate |
|---|---|
| Cert-ready build (6–8 mo, 4 eng @ ~S$12k/mo loaded + PM/DevOps) | **~S$340–460k** |
| Production-ready total (38–60 PM) | ~S$0.9–1.4M |
| Demo hardware | ~US$8k |
| Run cost pre-production | ~US$1.5–2.5k/mo |
| Run cost production (incl. VAPT S$15–25k/yr amortised) | ~US$3–4.5k/mo |
| De-risking track (§7) | **≤S$10k** |

### Partnerships & non-technical
- **A paying pilot partner (precaster/ICPH or main contractor) — the load-bearing requirement.** Without it: no Singapore deployment evidence (Table 5), no credible demo against incumbents' live references, no revenue path. Targets: Teambuild, Soilbuild, CKR, Jurong Port's upcoming shared ICPH, mid-tier contractors. Caveat: Greyform and Hong Leong Asia are Hubble reference customers; Soilbuild is a LeapThought case study.
- Singapore entity + **ACRA report** for the application; FormSG submission in an open window.
- A demo environment with realistic seeded datasets.
- One real CDE integration and third-party QMS record retrieval, actually working.
- For O2: the exact schema is only issued to vendors *selected by a winning tenderer* — pre-certification, the maximum honest position is a spec-compliant OAuth2/GCC-gateway push framework demoed against a mock, declared as "Future Development" where applicable.

---

## 4. Market reality

- Singapore construction demand: S$50.5B awarded 2025 (10-yr high); BCA forecasts S$47–53B for 2026, S$39–46B/yr 2027–2030; public sector ~55%. DfMA adoption 61% of new developments by GFA (2023) vs a 70%-by-2025 target — real but plateauing. 6 of 10 planned ICPHs built; one sat vacant ~2 years (factory overcapacity → cost-cutting mood, not software-buying mood).
- **Who pays:** the winning main contractor or the precaster — never JTC (JTC pays only for OPTIMUS). Precasters also buy factory-side directly (Hubble's customers).
- **Serviceable market estimate:** JTC projects S$0.6–3M/yr + HDB/BTO S$1.5–3.5M/yr + private PPVC/GLS S$0.5–2M/yr + precaster factory-side S$1.5–4M/yr ≈ **S$4–12M/yr**, assuming S$50–150k/deployment/yr — an assumption sitting *above* the only public price point (Novade ~US$29–35/user/mo ≈ US$10–42k/yr), so the true SAM may be smaller.
- Category economics sanity check: Hubble, the local category leader with real ICPH deployments, has raised only ~US$12M lifetime — this is a single-digit-million-ARR category split 5+ ways.
- Break-even for a lean org (~S$650–700k/yr) needs **~10–11 concurrent projects at S$65k/yr recurring** — a 10–25% sustained share of the entire market, from zero, against four entrenched incumbents. Base-case 3-yr P&L: **−S$1.5M cumulative**; optimistic: **−S$1.0M**.

## 5. Competition

| Vendor | Position | Why they're hard to beat |
|---|---|---|
| **LeapThought** (FulcrumHQ) | Structural incumbent | Powers JTC's own OPTIMUS v2.0 CDE (2,000+ users); Soilbuild precast case study; certified |
| **Novade** | Broad SG field-ops platform | Large SG contractor install base; QR/NFC + forms + dashboards; certified |
| **Capps** (CBOSS) | Local PPVC specialist | Closest analogue to what we'd build; certified |
| **Ynomia** (AU) | Automated hardware tracking | BLE-tracked 8,000+ Obayashi volumetric units Malaysia→SG — the "implemented hardware" requirement, proven at scale; certified |
| **Hubble.Build** | Uncertified but entrenched | QR wallchart precast module; runs digital ops at SG's largest ICPHs (workforce/OLS, not components) |

The requirement set reads like a codification of what these vendors already demo. Table 5's desirables (Singapore deployments, 99.5% uptime with public logs, ≥85% satisfaction surveys) are structurally impossible for a new entrant to evidence — expect to lose demo scoring on them.

## 6. The honest case for (staged wedge, not build-to-cert)

- **Revenue does not require certification.** Precasters already pay vendors directly, outside JTC's scheme.
- **The factory-floor gap is real:** the biggest ICPHs bought workforce/compliance tracking, not per-component lifecycle tracking — the exact thing JTC's spec codifies — and their vendor isn't certified.
- **The 2028 window is a schedule, not a wall:** all four certificates renew simultaneously ~July 2028; a challenger arriving with 12+ months of live ICPH deployment data enters that window credibly. 22 months runway vs a 6–8-month cert-ready build.
- **Neutrality pitch:** LeapThought is both JTC's CDE engine and a competitor; an independent tracking layer that pushes to O2 without feeding a rival's platform is a pitch no incumbent can make.
- **Differentiation matches a data-strong team:** the underserved Table 3 desirables — predictive delivery windows, laydown congestion warnings (>80/90% utilisation), delay/bottleneck forecasting — plus Johor→SG PPVC transit telemetry (demand proven by Ynomia/Obayashi; sole certified supplier is Melbourne-based).
- **The probe is cheap and the bet asymmetric:** ≤S$10k and ~1 month buys a fully informed go/no-go.

## 7. Decision gate — do these before anything else (~1 month, ≤S$10k)

1. **One email to jtc_iddta@jtc.gov.sg** (free, ~1–2 wk latency) asking:
   - When is the next assessment window for Digital Precast & Logistics Tracking, and are new applicants sought given four certified vendors?
   - Is certification (or will it become) a mandatory tender condition on JTC projects?
   - Is QR-only tracking sufficient, or is implemented fixed-hardware (RFID) integration required? (Table 1 rows 4/16 vs row 18's note)
   - Demo duration: 10 or 20 minutes?
   - Can we obtain the referenced metadata / data-requirements self-assessment spreadsheet?
   - Does k6-style load-test evidence satisfy "validated in acceptance tests"?
   **Kill if:** window >24 months out with no interim path, or category effectively closed.
2. **10–15 discovery calls** (2–3 weeks, ~S$0) with precasters/ICPH operators (Teambuild, Soilbuild, CKR, Jurong Port shared-hub team) and 2–3 mid-tier contractors: what do you use today, what does it cost, what breaks, would you pay to pilot component-level tracking? **Kill if:** no credible pilot interest.
3. **US$3–5k bench RFID portal** (2–3 weeks, one engineer): 2 readers + antennas + 50 concrete-rated tags + MQTT→ingest pipeline. Proves the hardest technical claim cheaply and arms the pilot pitch.

**Proceed to build only on a signed pilot LOI ≥ S$100k** that funds the cert-ready build — sequence: wedge (3–6 PM analytics/integration layer) → full platform → July 2028 certification window with a live reference site.

## 8. Top three kill risks

1. **Nobody pays us** (certification ≠ revenue; buyers already served) — near-certain severity ceiling; mitigated only by the LOI gate.
2. **Category saturated + window timing** — four incumbents locked in until mid-2028; entering the next window without a live Singapore reference repeats the losing position.
3. **"Implemented or non-compliant"** — RFID rig, real CDE integration, and QMS retrieval must genuinely work by demo day; build the bench rig in month 1, not month 6, and declare unproven scale claims as "Future Development" (self-declaring falsely creates acceptance-test liability later).

## 9. Key open facts

- Next assessment window date (nothing published after 14 Feb 2026 closing).
- Whether certification is/becomes a hard tender mandate — the single fact that would most flip this assessment.
- The metadata/data-requirements spreadsheet referenced by Table 3 (not public).
- O2/OPTIMUS API schema (issued only post-tenderer-selection).
- True deal sizes (5 of 7 rivals publish no pricing).

---

*Full agent outputs (9 agents, ~365k tokens of research): workflow run `wf_40fd1f1d-b6f`. Key sources: JTC IDDTA + certified-solutions pages (award dates verified 3 Aug 2026), BCA demand forecasts, Hubble/Novade/LeapThought/Ynomia public materials, RFID hardware pricing (AtlasRFIDStore, Zebra, Impinj), `requirements_digest.md`.*
