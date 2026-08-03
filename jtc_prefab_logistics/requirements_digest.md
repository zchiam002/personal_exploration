# JTC Digital Precast & Logistics Tracking — Requirements Digest

Sources:
- JTC webpage: [Digital Precast and Tracking Solution](https://www.jtc.gov.sg/enhance-your-business/adopt-technology-solutions/leading-digital-transformation-in-singapore-built-environment/digital-precast-and-tracking-solution)
- `jtc-precastreq.xlsx` — IDDTA application form (self-assessment), 5 requirement tables
- Digest compiled: 2026-08-03

## What this is

JTC certifies vendors of **digital precast + logistics tracking platforms** under its IDDTA scheme. The Solution = a digital platform that plans prefabrication production schedules and digitally tracks production, delivery, and installation of prefabricated components across the lifecycle: **shop drawing approval → fabrication → storage → transportation → delivery → on-site installation**.

Process: complete the self-assessment form (Yes / No / N.A. per row: "Currently Exist" / "Future Development" / "No plans"), submit with **ACRA report** via FormSG before the closing date of the next assessment window. Shortlisted vendors give a product demo (form says 10-min demo + 10-min Q&A; webpage says 20-min demo + 10-min Q&A — clarify). Successful applicants receive **IDDTA certification** recognising compliance with JTC's digital requirements and integration standards. Contact: jtc_iddta@jtc.gov.sg.

**Key rule: everything not marked [Desirable] is a CRITICAL requirement.**

Note in form: "Solutions that offer open APIs *without any implemented connection* with the specified hardware and software systems shall be considered non-compliant" — i.e. integrations must actually be built and demonstrable, not just theoretically possible.

## Table 1 — Technology (25 rows; 3 desirable)

**Critical:**
- Unique, immutable **component ID** through the whole lifecycle; one component can be associated with multiple elements with data accurately linked.
- **Tracking** of status + movement per component via QR codes and/or IoT (either one or a combination; equivalent approaches considered):
  - **QR**: scan with smartphone/tablet → auto-capture location, update DB; QR uniquely linked to component record (type, location, manufacturing data, quality status, install progress); printed, durable, weather-resistant labels readable through handling/storage/transport/installation.
  - **IoT/RFID**: electronic tags read automatically at checkpoints (factory gate, truck loading, site entrance) without manual scanning; weather-resistant; uniquely linked to component record.
- **Location history**: milestone-based (user input or system triggers) and/or automated reader-based at control points; configurable recording frequency; all timestamped + attributed to source (user or device).
- **Mobile**: Android + iOS minimum; scan → instant access to up-to-date component info.
- **Fixed hardware option**: full, functional, implemented integration between checkpoint devices (e.g. RFID tags + gateways) and the platform (open-API-only = non-compliant).
- **Component types**: panels, beams, columns, slabs, staircases (at minimum).
- **Dimensions + logistics management**: compliance with transportation, craneage, site handling constraints.
- **Delivery Order attachment** as prerequisite for verifying/recording deliveries at site.
- **Installation documentation**: photo/video attached to checklists and install records, tagged with metadata (timestamp, user, component ID, GPS); **secure digital signatures** on install steps, checklists, completion records.

**Desirable:** dual Location/Position ID separate from Component ID (traceability to final resting position despite substitutions); Delivery Order generation in-platform (vehicles, drivers, destinations); as-built GPS capture at installation.

## Table 2 — Information Management (18 rows; 4 desirable)

**Critical:**
- **Low-code/no-code workflow builder**: authorised users design/modify/deploy tracking workflows and define stage statuses (Factory, Yard, Storage, In Transit, Delivered, Site, Installed) — for standardisation across vendors.
- **Real-time sync** for mobile/web capture whenever connectivity available (implies offline capability + sync); hardware checkpoint sync at configurable interval, **max 60 min**.
- **Audit + immutability**: all sync/data transfers auto-logged; recorded data cannot be altered/deleted by unauthorised user, system admin, or external process.
- **QA/QC workflow tracking** with CDE/DMS integration; configurable digital forms + checkpoints through status workflows; DB of all components each linked to quality documentation in structured format; pre-pour/post-pour inspection data retrievable via integration with third-party QMS or accessible links.
- **Scale (validated in acceptance tests, monitored):** ≥1,000 components/project; ≥10 concurrent projects per tenant with full data/workflow/reporting isolation; ≥100 concurrent field users; ≥10,000 photos/media per project with instant retrieval.

**Desirable:** enforced sequential installation workflow (block out-of-order steps); shop-drawing workflow tracking with CDE/DMS integration mapped per drawing revision → component; component records synced to latest approved design; field retrieval of latest approved drawing on mobile/web.

## Table 3 — Insights & Dashboards (37 rows; ~13 desirable)

**Critical:**
- **Live interactive dashboards**, web-accessible to all authorised stakeholders, updating from latest synced data.
- **Code-free dashboard configuration** by authorised users (RBAC), custom KPIs, filters, layouts — without vendor intervention.
- **Planned vs actual** everywhere: auto Plan % recalculation linked to approved Master Programme (incl. revisions); interactive breakdowns by type / zone / level; **wallchart** format (status by floor, unit, component type, common area readable at a glance) + S-curves.
- **KPI variance indicators**: % deviations, colour-coded arrows, RAG thresholds.
- **Four lifecycle-stage comparative insights** (planned vs actual quantities and dates, % completion):
  - A. Shop Drawing Approved [this stage desirable]
  - B. Produced (fabricated, passed factory QC, in storage ready for dispatch)
  - C. Delivered (received on site, acknowledged, inspected, cleared for install)
  - D. Installed — **requires formal RSS (Resident Site Supervisor) sign-off** before status change; final status.
- **Floor-level QA/QC drill-down**: click through to pre-pour/post-pour/delivery inspection records, download forms from external platforms.
- **Floor-level component readiness**: % walls/columns/stairs/PPVC produced/delivered/ready per floor; identify incomplete component sets delaying floors.
- **Reports**: on-demand PDF + XLSX from any dataset/dashboard; **bulk CSV export** (incl. inspection data) with integrity + traceability.
- **Metadata minimums** per tracked component per JTC's separate data-requirements spreadsheet (not in this file — obtain from JTC).

**Desirable:** configurable common-area categories in wallcharts; hover/click floor → planned-vs-actual detail; alternative visualisations for very large projects; shop-drawing RAG indicators + rejection/resubmission rates; predictive logistics (delivery windows, >2h late flags, laydown utilisation % with >80/90% congestion warnings); critical-path stage identification; predictive analytics (delay/bottleneck forecasting); project precast-% target tracking (e.g. 70% DfMA target).

## Table 4 — Integration & Data Exchange (18 rows; 1 desirable)

**Critical:**
- Structured, machine-readable data access (forms, checklists, inspections, workflows, field inputs); JSON/XML/CSV standards; no manual cleaning needed.
- **BI connectivity**: automated integration with data warehouses / Power BI via connectors, APIs, or scheduled exports; latest data available without post-processing; referential integrity preserved in exports.
- On-demand exports (PDF/Excel/approved formats) reflecting live data.
- Minimum: **standard CSV exports + open API**; integration with external **CDE platforms**.
- **JTC O2 CDE integration (push model)** — vendor is responsible for transmitting required datasets into JTC's CDE:
  - Must adhere to JTC's prescribed data schema (provided at integration if selected by a winning tenderer in JTC projects).
  - O2 APIs: RESTful, published on **GCC API Gateway**; OAuth 2.0 authentication at gateway; then local auth at O2 API (AWS API Gateway) with mandatory headers `x-apigw-api-id` + `x-api-key`; request fields case-sensitive.
  - Hosts: QAS `https://csp-api.jtcqas.gov.sg/`, Prod `https://csp-api.jtc.gov.sg/`.
- Configurable sync frequency: real-time / hourly / daily / custom.

**Desirable:** demonstrated integration with leading CDE platforms used in built environment (name which).

## Table 5 — Success Metrics & Service Levels (11 rows; ALL desirable)

Deployment schedule w/ milestones + progress reporting; **≤6-week** hardware+software delivery lead time from order confirmation; **99.5% uptime** over any 6-month window with public service logs; **72-hour** initial support response with resolution path, approved ticketing + automated escalation; biannual user-satisfaction surveys, **≥85%** score; demonstrated **Singapore project implementation experience**; understanding of local challenges (PPVC import disruption, site storage constraints, fragmented digital ecosystem); familiarity with Singapore precast/DfMA methods and standards.

## Immediate observations

1. **Certification ≠ contract.** Certification qualifies the solution as compliant for JTC projects; revenue presumably comes when winning tenderers adopt/procure a certified solution.
2. **Working hardware integration is mandatory** — a software-only MVP with "APIs for future RFID" fails Table 1 row 18 by explicit note.
3. The **scale + isolation requirements** (10 projects/tenant, 100 concurrent users, immutability, audit) are real multi-tenant SaaS engineering, not a demo app.
4. **Ambiguity to clarify with JTC**: whether QR-only tracking satisfies Table 1 (row 4/16 say "either or combination", row 18 note implies implemented fixed-hardware integration is required); demo duration discrepancy (10 vs 20 min).
5. Table 5 (all desirable) heavily favours incumbents with **existing Singapore deployments** — a new entrant can still pass criticals but scores weaker.
6. A separate **data-requirements self-assessment spreadsheet** (metadata schema) exists and is referenced — we don't have it.
