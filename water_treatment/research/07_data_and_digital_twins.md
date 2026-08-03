# 07 — Data Infrastructure, Digital Twins, and Deployment Reality for ML in Membrane Plants

Scope: what a UF/RO train actually measures, how that data moves through PLC/SCADA/historian stacks, what breaks it (drift, calibration, compression), how published digital twins for desalination/membrane plants are architected and recalibrated, and the MLOps, cybersecurity, human-factors, and regulatory constraints that decide whether any of it ships. Written for an engineer who wants to build this from scratch. Research date: 2026-08-01. Note: several primary pages (MDPI full texts, ScienceDirect, IWAponline) blocked scripted access; where a claim comes from a search-result abstract rather than a fetched full text, it is flagged.

---

## 1. The sensor layer of a real UF/RO train

### 1.1 What is actually installed

Vendors describe three instrumentation tiers for RO systems: (i) basic — local flow/pressure indicators plus a single permeate conductivity meter with analog output and manual valve adjustment; (ii) standard — adds a permeate flow transmitter, ORP and/or free-chlorine sensors (to protect polyamide membranes from oxidant attack), temperature and pH, with a VFD on the high-pressure pump; (iii) advanced — all analog instruments wired to a PLC/datalogger, frequency-controlled pumps, and a proportionally regulated concentrate valve (Lenntech, n.d., https://www.lenntech.com/processes/desalination/instrumentation/general/instrumentation-control.htm). A full SWRO or UF/RO municipal train typically carries, per train:

| Measurement | Location(s) | Typical technology | Order-of-magnitude installed cost (practitioner estimate unless cited) | Drift/reliability character |
|---|---|---|---|---|
| Conductivity | feed, permeate (per train, often per stage), product | toroidal/contacting cells | $1–3k/point | Most critical instrument for salt-passage monitoring; fouling of cell, temperature-compensation errors; frequent calibration required (AQUALITEK, https://www.aqualitek.com/blog/what-online-instruments-require-frequent-calibration-in-seawater-desalination-plants-aqualitek.html — search-summary sourced) |
| Pressure | feed, interstage, concentrate, permeate; differential across cartridge filters and each membrane stage | piezoresistive transmitters | $0.5–2k/point | Stable (±0.1% span class); zero drift over years; dP across stages is the fouling KPI so transmitter pairing/zeroing errors propagate directly into cleaning decisions |
| Flow | feed, permeate (per train), concentrate, CIP | electromagnetic (mag) meters; ultrasonic on large headers | $2–8k/point | Very stable; errors mostly from installation (straight-run) and entrained air |
| Temperature | feed (minimum), often permeate | RTD | $0.3–1k | Stable; but a 1 °C error biases normalized flow by ~3% via the temperature correction factor (see §2) |
| pH | feed (post-acid/antiscalant), permeate, product | glass electrode | $1–3k + electrode consumable | Fastest-drifting instrument class; glass electrodes age, foul, and drift; replacement every 6–18 months; buffer calibration weekly–monthly is common practice |
| ORP / free chlorine | upstream of RO (dechlorination verification) | ORP electrode / amperometric or DPD colorimetric chlorine analyzer | ORP $1–3k; chlorine analyzer $4–10k + reagents | ORP is cheap but only semi-quantitative; amperometric cells drift with flow/temperature; DPD analyzers consume reagents (~15-min cycle, not continuous). A missed dechlorination event destroys polyamide membranes, so these loops are usually hard-interlocked, not ML-mediated |
| Turbidity | raw water, UF filtrate | nephelometric (ISO 7027 / EPA 180.1) | $3–6k/point | Bubble and fouling artifacts; wiper-cleaned units; regulatory-grade instruments need routine primary-standard verification |
| SDI (Silt Density Index) | RO feed (post-UF/cartridge) | manual ASTM D4189 test rig or automated SDI unit | manual rig <$2k; automated $15–30k | Manual test done 1–3×/day at best — inherently sparse, discrete, operator-dependent; one of the five parameters recommended for daily monitoring (Water Tech Online, "5 key performance indicators in reverse osmosis operation", https://www.watertechonline.com/wastewater/article/15549752/5-key-performance-indicators-in-reverse-osmosis-operation — search-summary sourced) |
| TOC | feed and/or permeate/product | UV-persulfate or high-temp combustion + NDIR, or conductometric | lab analyzers $6k–$100k+; entry $6–15k, mid $15–35k, high-end $35k+; online/process units at a premium; consumables (reagents + calibration standards) $1.5–5k/yr, calibration standards alone $0.5–1.5k/yr, routine maintenance $0.5–2k/yr (Excedr, 2024, https://www.excedr.com/blog/how-much-does-a-toc-analyzer-cost) | NDIR accurate but expensive; conductometric cheaper but "may require additional validation"; reagent-dependent, drifts between standardizations |

Instruments identified by desalination O&M practice as needing the most frequent calibration attention: conductivity meters, pH analyzers, turbidity meters, chlorine analyzers, ORP analyzers, DO sensors, flow meters, pressure transmitters, temperature sensors — with conductivity singled out as the most critical because it continuously tracks salt concentration of feed, permeate, and product (AQUALITEK, https://www.aqualitek.com/blog/what-online-instruments-require-frequent-calibration-in-seawater-desalination-plants-aqualitek.html — search-summary sourced).

### 1.2 Consequences for ML feature engineering

- The five KPIs practitioners already compute daily — SDI, differential pressure, normalized permeate flow, percent rejection, pressure-drop coefficient (Water Tech Online, ibid.) — are *derived*, normalized quantities, not raw tags. Any ML system that ingests raw tags without replicating this normalization (§2) will mostly learn the temperature and feed-salinity seasonality, not membrane state.
- Sensor classes split into "trustworthy backbone" (pressure, mag flow, temperature, conductivity) and "drift-prone chemistry" (pH, ORP, chlorine, turbidity, TOC). Feature pipelines should weight/validate accordingly; a common pattern is to reconstruct chemistry values from the backbone via mass balance and flag divergence (data reconciliation, §5.2).
- SDI and lab samples (e.g., weekly ICP metals, membrane autopsy results) arrive at 10³–10⁵× lower frequency than SCADA tags. Aligning them requires asynchronous feature stores and forward-fill discipline with explicit staleness features.

---

## 2. Governing equations every membrane data pipeline must implement

Normalization to reference conditions (industry practice codified in ASTM D4516 for RO data normalization; equations below are the standard forms) is the single most important "feature engineering" step, and is also the core of model-plant mismatch detection.

Solution-diffusion transport (the physics basis used to generate training data in Daaboub et al. 2024, §4.2):

$$J_w = A\,(\Delta P - \Delta\pi), \qquad J_s = B\,(C_{fc} - C_p)$$

where $A$ [m s⁻¹ Pa⁻¹] is water permeability, $B$ [m s⁻¹] salt permeability, $\Delta P$ transmembrane pressure and $\Delta\pi$ osmotic pressure difference. Osmotic pressure via van 't Hoff: $\pi = i\,c\,R\,T$ (≈ 0.78 bar per 1000 mg/L NaCl at 25 °C).

Net driving pressure (per-stage):

$$NDP = P_f - \frac{\Delta P_{f\text{-}c}}{2} - P_p - \left(\pi_{fc} - \pi_p\right)$$

Temperature correction factor (polyamide, Arrhenius form):

$$TCF = \exp\!\left[K\left(\frac{1}{298.15} - \frac{1}{273.15+T}\right)\right],\quad K \approx 2500\text{–}3000\ \mathrm{K}$$

Normalized permeate flow and salt passage:

$$Q_{norm} = Q_{actual}\cdot\frac{NDP_{ref}}{NDP_{actual}}\cdot\frac{TCF_{ref}}{TCF_{actual}}, \qquad SP = \frac{C_p}{C_{fc}},\ \ R = 1 - \frac{C_p}{C_f}$$

Rules of thumb used to trigger cleans: 10–15% decline in $Q_{norm}$ or 15% rise in stage dP from the post-commissioning baseline.

UF side — transmembrane pressure and resistance-in-series:

$$TMP = \frac{P_{feed}+P_{conc}}{2} - P_{filtrate}, \qquad J = \frac{TMP}{\mu(T)\,(R_m + R_{rev} + R_{irr})}$$

with temperature-corrected specific flux (permeability) $L_p = J\cdot\mu(T)/TMP$, viscosity correction commonly approximated as $\mu_T = \mu_{20}\cdot 1.025^{(20-T)}$. UF fouling ML papers model exactly these quantities; e.g., statistical models predicting UF fouling in pilot and full-scale operation (Desalination and Water Treatment, 2021, DOI 10.5004/dwt.2021.27355).

Synauta's field trials normalized performance to standard seawater test conditions (25 °C, 32,000 ppm NaCl) before optimization — i.e., the commercial state of the art still runs on ASTM-style normalization underneath the ML (Synauta/Smart Water Magazine, 2020, https://smartwatermagazine.com/news/synauta/machine-learning-delivers-energy-savings-desalination).

---

## 3. Control and data stack: PLC → SCADA → historian → analytics

### 3.1 Typical stack

The canonical membrane-plant stack follows the Purdue/ISA-95 hierarchy: L0 field instruments (4–20 mA/HART, increasingly Modbus/Profibus/EtherNet-IP); L1 PLCs (Rockwell/Allen-Bradley, Siemens S7, Schneider) running interlocks, CIP sequencing, and UF backwash state machines; L2 SCADA/HMI (Wonderware/AVEVA System Platform, GE iFIX, Ignition); L3 plant historian; L3.5 DMZ; L4 enterprise/cloud analytics.

Historian reality: the dominant product is the PI System (OSIsoft, acquired by AVEVA 2021 — ARC Advisory, https://www.arcweb.com/blog/avevas-acquisition-osisoft-will-provide-new-opportunities-data-drive-digital-transformation). Its current architecture: AVEVA PI Server ("high-volume, real-time data storage, contextualization, analytics, and notification engine"), Edge Data Store for remote assets, PI Interfaces/Connectors/Adapters providing vendor-neutral collection over "hundreds" of protocols, PI Vision for visualization, PI DataLink for Excel, PI Integrator for Business Analytics for feeding data lakes/ML, and the CONNECT platform for edge-to-cloud hybrid deployment; sub-second granularity with store-and-forward buffering against network loss; 1000+ power utilities as installed base (AVEVA, 2025, https://www.aveva.com/en/products/aveva-pi-system/). Inductive Automation's Ignition (SQL-backed tag historian, unlimited-tag licensing) is the common choice at smaller municipal plants; the Jacobs/PUB digital twin (§4.4) reads "near real-time" SCADA historian data through a secured connection (Jacobs, 2020, https://www.jacobs.com/newsroom/press-release/jacobs-creating-first-digital-twin-pubs-changi-water-reclamation-plant).

OPC-UA (IEC 62541) is the de facto northbound protocol from PLC/SCADA to historians and ML gateways: platform-independent, certificate-secured sessions, information modeling — the practical mechanism by which a Python service subscribes to plant tags without touching the control network directly.

### 3.2 Sampling rates and data quality problems

- Typical scan/storage rates: control loops 100 ms–1 s at the PLC; historian storage 1–60 s for pressures/flows/conductivity; analyzers (chlorine DPD, TOC) 2–15 min cycles; SDI 1–3×/day manual; lab data daily–weekly. An ML pipeline must therefore handle 4–5 decades of timescale spread.
- **Compression artifacts.** PI-style historians apply exception reporting at the interface and swinging-door compression (CompDev/CompMax settings) at the archive: only points that deviate beyond a configured band from a linear reconstruction are stored. The classic quantitative study showed that compression materially corrupts data-driven analysis — minimum-variance control benchmarks, spectral features, and oscillation detection degrade once the compression factor exceeds roughly 3, and mean-nonlinearity measures are disturbed at even lower factors; the authors recommend archiving key loops uncompressed for analytics (Thornhill, Shoukat Choudhury & Shah, 2004, *Journal of Process Control* 14:389–398, DOI 10.1016/j.jprocont.2003.06.003). Symptom in membrane data: staircase-interpolated conductivity that fakes flatlines and destroys derivative features (fouling-rate estimates).
- **Sensor drift and calibration steps.** Drift-prone analyzers (§1) produce slow ramps that alias as process degradation; calibrations produce step discontinuities. Both must be modeled: maintain a calibration-event log as a first-class dataset and either segment training windows at calibration events or include "time since calibration" as a feature. Disambiguation of sensor drift vs true membrane degradation is exactly what mass-balance data reconciliation (§5.2) provides.
- **Missing data and quality flags.** Historians store value + validity status + timestamp; DCS "bad quality" flags, comms dropouts, and manual-entry lab values all coexist. Digital-twin deployments put explicit validation checks between historian and simulator: the PUB Changi twin runs automated data validation before values enter the simulation (Jacobs, 2020, ibid.).
- **Operating-mode pollution.** CIP events, integrity tests, standby, and train swaps must be labeled; otherwise "fouling models" learn CIP schedules. UF direct integrity tests (pressure-decay) occur daily by regulation (§8) and generate structured excursions in every pressure tag.

---

## 4. Digital twin architectures for desalination/membrane plants — published cases

A 2025 review defines water-sector DTs as virtual replicas enabling real-time monitoring, simulation, and predictive control across treatment, networks, and reuse, and catalogs case studies, technical challenges, and gaps (Ghorbani Bam, Rezaei, …, Villez, Rosso, 2025, *Water* 17(20):2957, https://www.mdpi.com/2073-4441/17/20/2957 — abstract; full text blocked). The published membrane-plant cases split into four architecture families:

### 4.1 Mechanistic (first-principles) online twins

- **gPROMS-based SWRO twins (Siemens PSE).** Equation-based white-box models capture physics, chemistry, control philosophy, and operating procedures; run in *online* mode (connected to plant control, delivering real-time optimal setpoints) or *offline* mode (scenario exploration, soft sensing to reduce physical sensor count, operator training). Sichel argues high-fidelity mechanistic twins "optimize to the highest possible level of performance" whereas pure ML "optimizes to the best 'experienced' level" — i.e., data-driven models cannot exceed the historical operating envelope; context: SWRO SEC has fallen from >5 kWh/m³ historically to 2–2.5 kWh/m³ today against a thermodynamic floor of 0.8–1.5 kWh/m³ (Sichel/Siemens, Smart Water Magazine, https://smartwatermagazine.com/blogs/dr-cosima-sichel/optimizing-plant-performance-a-case-digital-twins-desalination).
- **Santa Barbara (Charles E. Meyer) SWRO twin, LBNL + NETL, 2021.** Built on ProteusLib (now **WaterTAP**, the DOE/NAWI open-source Python platform on IDAES/Pyomo — https://github.com/watertap-org/watertap) with unit models for pumps, filters, mixers, splitters, RO units and a seawater property model. Two-step configuration against plant data: (1) **data reconciliation** — adjust measurements to satisfy material/energy balances, $\min \sum_i \left(\frac{\hat{x}_i - x_i^{meas}}{\sigma_i}\right)^2$ s.t. balance constraints; (2) **parameter estimation** — iteratively refine model parameters (membrane $A$, $B$, fouling factors, pump efficiencies) to match observed conditions; objective output is diagnostic/predictive analysis of specific energy consumption (kWh/acre-foot) (Gunter, Amusat, Bartholomew, Drouven, 2021, DOE OSTI Technical Report, DOI 10.2172/1831427, https://www.osti.gov/biblio/1831427). This is the most replicable published blueprint because the entire toolchain is open source.

### 4.2 Data-driven surrogate twins

- **Daaboub, Echeverria Rovira & Rubion Soler, 2024** (DOI 10.3233/FAIA240403, https://ebooks.iospress.nl/volumearticle/69380): trained 11 ML algorithms (ensemble and non-ensemble) on **18,816 scenarios generated by a solution-diffusion transport model** of an SWRO train; targets: permeate flow, permeate salinity, SEC. XGBoost, CatBoost, and ANN were the most accurate; SHAP analysis confirmed the surrogates learned physically sensible drivers. Pattern to note: physics model generates the corpus, gradient-boosted trees serve as the fast online twin — the standard surrogate-twin recipe when plant data alone can't cover the operating envelope.
- **Seminal anchor:** Libotean, Giralt, Rallo, Wolfe & Cohen, 2009, "Neural network approach for modeling the performance of reverse osmosis membrane desalting," *Journal of Membrane Science* 326:408–419 (DOI 10.1016/j.memsci.2008.10.028) — the field's reference point for ANN prediction of full-scale RO permeate flow/salinity from plant operating data, predating the "digital twin" label by a decade.
- **Full-scale drinking-water forecasting with dosing lags:** XGBoost with time-feature engineering beat deep models and a naive-mean baseline by 3–4 percentage points MAPE forecasting four effluent quality variables at a 12 h horizon, from influent quality + reagent dosages + effluent history at a full-scale plant; the 12 h lag structure was needed to capture delayed dosing effects; SHAP used for interpretability (Pang, Ben, Cao, Qu & Hu, 2024/2025, *Water Research*, DOI 10.1016/j.watres.2024.122777). Lesson for membrane twins: dose→response deadtimes of hours must be explicit features.

### 4.3 Asset-degradation twins (maintenance decision support)

- **Carlsbad SWRO membrane-wear twin.** van Rooij, Scarf & Do, 2021 (*Desalination*, DOI 10.1016/j.desal.2021.115214) built a decision-support system whose engine is a DT of **wear and restoration of individual membrane elements within an RO pressure vessel**, modeled as a multi-component system (elements can be swapped/replaced individually) rather than the usual lumped single-system treatment. Parameters estimated statistically from operating data at the Carlsbad Desalination Plant, California — which suffers biofouling from seasonal algal blooms; observed vs modeled wear-states fit well, and competing restoration policies were compared on risk, cost, downtime, and stoppage count, projecting "significant cost-saving" without compromising integrity. This is the published exemplar for optimizing element replacement/rotation strategy.

### 4.4 Utility-scale plant twins (PUB Singapore and EPC programs)

- **PUB Changi Water Reclamation Plant twin (Jacobs, from 2020).** First whole-plant application of its kind: Replica™ platform for hydraulics + control simulation, Sumo© for process simulation, fed near-real-time SCADA historian data over a secured connection with automated validation checks; crucially, it "employs machine learning to continuously adjust its calibrations within defined ranges to match the plant's observed performance" without staff intervention — i.e., bounded online auto-recalibration as a designed-in feature; also used for what-if analysis and customizable operator-training scenarios; funded by NRF Singapore and PUB (Jacobs, 2020, https://www.jacobs.com/newsroom/press-release/jacobs-creating-first-digital-twin-pubs-changi-water-reclamation-plant).
- **PUB Tuas Water Reclamation Plant.** Jacobs managed design across 17 contract packages on Bentley iTwin (plus ProjectWise, SYNCHRO, OpenPlant, LumenRT/Omniverse) as a "single source of truth" construction/BIM twin intended to hand over into digital asset management for O&M (Bentley Year in Infrastructure, https://yii.bentley.com/project/tuas-water-reclamation-plant-twrp/). Note the distinction: this is an *asset/BIM* twin, not a process twin — most utility "digital twin programs" start here.
- **Acciona.** (a) **Maestro** AI platform at the Umm Al Houl SWRO plant (Qatar), funded by Acciona's decarbonization fund, optimizing operations with estimated emissions reduction of ~12,000 t CO₂/yr (ACCIONA, https://www.acciona.com/updates/articles/acciona-decarbonization-fund-maestro-ai-platform-umm-al-houl-desalination-plant-qatar — search-summary sourced; page blocked scripted fetch). (b) **Dual-Model Optimization System**: ACRRO® (simulation-based optimization model) + Insight (real-time ML tool trained on operational data), deployed at an Acciona plant in Qatar, with "measurable improvements in specific energy consumption and throughput consistency, particularly under fluctuating salinity and temperature" (ACCIONA ME / Zawya press release, 2025, https://www.acciona-me.com/updates/news/acciona-launches-dual-model-ai-technology-to-transform-desalination-efficiency — search-summary sourced). The mechanistic+ML *pair* is the emerging commercial pattern: physics model for global optimality, ML model for real-time tracking.
- **Siemens + Acciona Middle East SWRO twin**: virtual commissioning, real-time monitoring, fault detection; reported improved productivity, reduced downtime, and pre-startup operator training in the virtual environment (EcoMENA, 2024, https://www.ecomena.org/rethinking-desalination-through-digital-twins/).
- **ACWA Power** partners with Aleph Tech on AI energy optimization for large-scale desalination, alongside UCLA/MIT work on batch RO (Smart Water Magazine, 2025, https://smartwatermagazine.com/news/smart-water-magazine/acwa-advances-desalination-innovation-new-research-and-technology — search-summary sourced). **Tedagua** ran a Digital Twin Platform for Desalination Plants program (2022–2024) to standardize a DT ecosystem for RO plants (Smart Water Magazine, https://smartwatermagazine.com/news/tedagua/digital-twins-and-ai-future-efficiency-and-security-seawater-desalination-plants — search-summary sourced).
- **Tariff-aware operation twin:** a 2025 IWA *Journal of Water Reuse and Desalination* paper builds a DT to minimize electricity cost of a desalination plant under time-of-use tariffs (production scheduling against tariff windows) (IWA Publishing, 2025, DOI 10.2166/wrd.2025.039 — full text blocked; title/venue verified).

### 4.5 Reinforcement learning inside twins (frontier, not deployed)

A 2025 survey of RL in desalination DTs reports: QMIX/VDN multi-agent RL on two-stage RO beat a single-agent baseline on SEC; a cascade of DDPG (continuous pump pressure) + a discrete agent (time-of-day pricing); CNN-enhanced Soft Actor-Critic outperforming DDPG/PPO/TD3 for renewable-powered RO (entropy-regularized exploration robust to solar variability); a Korean study calibrated its simulator against real industrial-plant data (reaching ~TRL 4 vs TRL 2–3 for the field); membrane-cleaning RL showed a 16.13% operating-cost reduction and 139.5% increase in RO operating time; targets below 2 kWh/m³ vs a 3.5 kWh/m³ benchmark. Every commercial twin surveyed operates in **advisory mode**; required safety architecture is a supervisory constraint layer (hard limits on pressure, recovery, salinity, flux) filtering agent actions; no desalination RL work has yet addressed domain randomization or sim-to-real transfer; estimated 3–5 years to supportive deployments and 5–10 years to closed loop (Smart Water Magazine, 2025, https://smartwatermagazine.com/news/smart-water-magazine/when-plant-learns-run-itself-reinforcement-learning-agents-desalination).

---

## 5. Model-plant mismatch and online recalibration

### 5.1 Why mismatch is structural

Feedwater quality fluctuates, membranes age monotonically (irreversible fouling, oxidation), elements get swapped, and fouling develops in ways simulators don't capture — the explicitly stated core obstacle to autonomous control (SWM RL survey, 2025, ibid.). A twin calibrated at commissioning diverges within weeks.

### 5.2 The working recipe (as published)

1. **Normalize first** (§2): work in $Q_{norm}$, normalized SP, normalized dP. Mismatch in normalized space isolates membrane-state change from operating-condition change.
2. **Data reconciliation** before every calibration cycle: enforce flow/salt balances across the flowsheet to detect and correct biased sensors (Santa Barbara twin step 1; Gunter et al., 2021, DOI 10.2172/1831427).
3. **Windowed parameter estimation**: re-estimate a small, identifiable parameter set — membrane $A(t)$, $B(t)$, a fouling resistance or fouling factor per stage, pump efficiency — by weighted least squares over a moving window (Santa Barbara twin step 2, ibid.). Keep the rest of the model frozen.
4. **Bounded auto-recalibration**: allow the automatic loop to adjust calibrations only "within defined ranges" (PUB Changi twin; Jacobs, 2020) so a failing sensor cannot drag the model into nonsense; out-of-bound corrections raise an engineering review instead.
5. **Drift vs degradation disambiguation**: a fouling event moves $A$ down and stage dP up *coherently*; a conductivity-sensor drift moves apparent $B$ with no hydraulic signature. Residual-pattern logic (or a CUSUM on reconciliation residuals, $S_t = \max(0, S_{t-1} + (r_t - k))$) is the practical discriminator.
6. **Element-level state tracking** where maintenance optimization is the goal: model the vessel as a multi-component system with per-element wear states estimated statistically (van Rooij et al., 2021, DOI 10.1016/j.desal.2021.115214).

---

## 6. MLOps for membrane plants: edge vs cloud, cadence, cybersecurity

### 6.1 Deployment topology

- **Edge**: inference next to the historian (L3/L3.5) for anything advisory-to-control; PI Edge Data Store / AVEVA hybrid edge-to-cloud data infrastructure is the vendor-supported route (AVEVA, https://www.aveva.com/en/products/aveva-pi-system/). Ignition's architecture supports the same pattern at smaller plants.
- **Cloud**: model training, fleet benchmarking, and non-latency-critical optimization. Synauta's commercial deployments required **no new hardware**, ran off historian exports, and delivered recommendations as **three setpoints via daily email** (HP pump flow, PX booster flow, PX drain valve), with optional SCADA/DCS integration — i.e., the minimum-viable topology skips OT integration entirely (Smart Water Magazine/Synauta, 2020, https://smartwatermagazine.com/news/synauta/machine-learning-delivers-energy-savings-desalination).
- Retrofitting via "a layer of IoT sensors and a gateway to the cloud" rather than replacing control equipment is the vendor-described pattern for older plants (WaterTech, 2025, https://www.watertechsh.com/ai-for-reverse-osmosis-optimization-redefining-efficiency-in-water-treatment/).

### 6.2 Monitoring and retraining cadence

Published cadences: Changi twin recalibrates continuously within bounds (Jacobs, 2020); Synauta issued daily recommendations and refined constraints in a phased rollout beginning with a historical-data audit (Synauta, 2020, ibid.); its cleaning optimizer improved iteratively with operator feedback at a food-and-beverage deployment targeting 10–15% chemical reduction (Synauta, 2021, https://smartwatermagazine.com/news/synauta/ml-optimizes-ro-membrane-cleans-62-more-permeate-production-challenging-conditions). Practical monitoring set: input-drift stats per tag (population-stability or KS tests against training window), prediction-vs-normalized-actual residuals, and constraint-violation counts; retrain triggers on membrane replacement events and seasonal feed transitions rather than fixed calendars.

### 6.3 Cybersecurity constraints that shape everything (IEC 62443)

IEC 62443 is the governing IACS security framework for water utilities. Structure: 62443-1-x (concepts/terminology), 62443-2-x (program requirements; 2-4 covers service-provider capabilities during integration/maintenance — directly applicable to ML vendors), 62443-3-3 (system requirements + four security levels), 62443-4-1/4-2 (secure development lifecycle and component requirements). Security levels: SL1 casual/unintentional; SL2 intentional, simple means; SL3 sophisticated, moderate resources; SL4 state-level. Seven foundational requirements: identification/authentication control, use control, system integrity, data confidentiality, restricted data flow, timely incident response, resource availability. The operative design concept is **zones and conduits**: group assets with equal security requirements into zones, force all inter-zone traffic through defined, monitored conduits (Fortinet, https://www.fortinet.com/resources/cyberglossary/iec-62443; Rockwell Automation, https://www.rockwellautomation.com/en-us/company/news/blogs/iec-62443-security-guide.html).

Consequences for ML architecture: (1) the model may **read** from the historian in the DMZ but must never open inbound connections into the control zone — data flows outward through a conduit (or one-way diode at high-security sites); (2) closed-loop writes require the ML host to be certified as part of the control zone at that zone's SL, which is why virtually all deployments stay advisory; (3) vendor remote access falls under 62443-2-4; (4) the Jacobs/PUB "secured connection" from SCADA historian to the twin (Jacobs, 2020) is the canonical compliant pattern. Microsegmentation within OT further limits lateral movement (Elisity whitepaper, https://www.elisity.com/resources/wp/iec-62443-segmentation-white-paper).

---

## 7. Human factors: trust, advisory vs closed loop, alarm fatigue

- **All commercial desalination twins run advisory (open-loop)**, "recommending actions rather than taking them," with operators "firmly in the loop"; trust is built "one carefully monitored step at a time"; projected 3–5 years to supportive deployments, 5–10 to autonomy (SWM RL survey, 2025, https://smartwatermagazine.com/news/smart-water-magazine/when-plant-learns-run-itself-reinforcement-learning-agents-desalination).
- Successful advisory design in the field: Synauta's Western Australia trial reduced the operator's task to entering three emailed setpoints "in a matter of seconds," retained full manual override, and needed no new hardware — adoption reached "operators depending on the machine learning with only minor validation" in the OBS cleaning trial (Synauta, 2020/2021, ibid.). Low-dimensional, physically meaningful recommendations with visible normalization logic are what operators accept.
- **Alarm fatigue** is the negative baseline ML must not worsen: ISA-18.2/IEC 62682 and EEMUA 191 govern alarm-system design (standards enumerated in Wikipedia's alarm-management overview, https://en.wikipedia.org/wiki/Alarm_management); EEMUA 191's widely used benchmarks (from the standard itself, not fetched) target on the order of ~1 alarm per 10 min steady-state per operator, with >10 alarms in 10 min constituting a flood. Any ML anomaly detector routed into the alarm system must obey the plant's alarm philosophy (rationalization, prioritization, shelving) or it will be suppressed by operators within weeks.
- Twins double as **operator-training simulators**: customizable training scenarios were an explicit deliverable of the PUB Changi twin (Jacobs, 2020) and the Siemens/Acciona twin trained personnel virtually before physical changes (EcoMENA, ibid.) — in practice this is the trust-building on-ramp for later advisory control.

---

## 8. Validation and acceptance in regulated drinking-water contexts

- **Compliance monitoring is non-negotiable and ML-independent.** Under US EPA's LT2/membrane framework (EPA Membrane Filtration Guidance Manual, EPA 815-R-06-009, 2005 — standard reference, not fetched), UF log-removal credit rests on daily direct integrity testing (pressure-decay) plus continuous indirect monitoring (filtrate turbidity); an ML system may *supplement* but never replace these. Same for chlorine/ORP interlocks protecting RO membranes.
- **Acceptance testing pattern that worked commercially:** controlled A/B train trials — Synauta's cleaning optimization ran a 2-month field trial on a 2,700 m³/day Australian brackish plant (3 trains, 60 vessels, 4 elements/vessel), one optimized train vs a control train, yielding +6.2% permeate, 4 fewer cleans, 8.7% EDTA cost saving, and ~doubled projected membrane life (Synauta, 2021, https://smartwatermagazine.com/news/synauta/ml-optimizes-ro-membrane-cleans-62-more-permeate-production-challenging-conditions); its energy product ran a 6-month trial at a 4×1,000 m³/day SWRO plant (isobaric ERD, 14 vessels/train, 6 elements, 99.7% rejection membranes) achieving 18% instantaneous / 9.7% six-month-average energy savings ≈ $65,000/yr OPEX at that 4,000 m³/day site (Synauta, 2020, ibid.). Broader claims: up to 15% energy and up to 25% cleaning-chemical savings (Alberta Innovates / Cybera profiles, https://albertainnovates.ca/news/digital-innovation-machine-learning-for-optimizing-reverse-osmosis/, https://www.cybera.ca/improving-access-to-clean-water-around-the-world-through-machine-learning/ — search-summary sourced); AI-advisor adopters in adjacent sectors report 10–15% reduction in total cost of water (WaterTech, 2025, ibid.).
- **Regulatory horizon:** the EU AI Act classifies AI in critical-infrastructure treatment processes as high-risk with a December 2027 compliance deadline, but no regulator has yet published guidance specific to RL/ML control of treatment (SWM RL survey, 2025, ibid.). Expect conformity assessment, logging, human-oversight, and robustness documentation obligations for EU-deployed advisory systems.
- **Payback data are thin.** No source fetched reports an explicit payback period; the strongest inferable figure is Synauta's software-only $65k/yr on a small SWRO plant (sub-year payback at typical SaaS pricing) and Acciona's fleet-level 12,000 t CO₂/yr at Umm Al Houl. Treat vendor "10–15% TCO" claims as upper bounds pending A/B validation on your own trains.

---

## Implementation notes

**Data you need (minimum viable, per train):** feed/permeate/concentrate flows; feed, interstage, concentrate, permeate pressures; feed + permeate conductivity; feed temperature; pump VFD speed/power (or a power meter — SEC is the objective function); CIP/backwash/integrity-test event log; membrane element inventory with install dates and swap history; calibration log for every analyzer; lab data (SDI, TOC, ion panels) with timestamps. One year of history spanning a full seasonal feed cycle is the realistic floor; Synauta's rollout began with a historical-data audit before any optimization (Synauta, 2020).

**Extraction stack:** historian → analytics via OPC-UA or vendor egress (PI Web API / PI Integrator; Ignition SQL). Land raw tags with quality flags into Parquet/TimescaleDB. Store *raw* + *reconciled* + *normalized* as separate layers. Disable or minimize compression (CompDev→0) on the ~30 tags feeding the twin, per Thornhill et al. (2004) — this is a one-line historian config change that removes a whole class of silent bias.

**Math to implement (in order):** (1) ASTM D4516-style normalization — TCF, NDP, $Q_{norm}$, normalized salt passage (§2); (2) mass-balance data reconciliation as a weighted least-squares problem with flow/salt balances (Pyomo/IPOPT, ~50 lines); (3) solution-diffusion flowsheet with per-stage $A$, $B$, fouling factor — use **WaterTAP** (https://github.com/watertap-org/watertap): open-source, DOE/NAWI-funded, IDAES/Pyomo-based, with RO/pump/ERD unit models, parameter estimation, and costing; the Santa Barbara report (DOI 10.2172/1831427) is a worked example of reconciliation + estimation against a real plant; (4) moving-window re-estimation of $\{A, B, f_{foul}\}$ with bounds and CUSUM on residuals for drift-vs-fouling discrimination; (5) only then a data-driven layer: gradient-boosted trees (XGBoost/CatBoost) on physics-normalized features — the consistent winner over deep nets at plant scale (Daaboub et al., 2024; Pang et al., 2024) — optionally trained on a simulator-generated corpus (≈10⁴–10⁵ scenarios, cf. 18,816 in Daaboub et al.) plus plant data, with SHAP for operator-facing explanation.

**Deployment:** run inference at L3/DMZ, read-only from the historian, outbound-only conduits (IEC 62443 zones/conduits; SL-target per plant risk assessment). Ship recommendations as a small number of named setpoints with predicted effect and confidence, into a dashboard or even email (proven at Synauta scale) — not into the alarm system. Keep manual override and log operator accept/reject as labeled feedback. Plan acceptance as a control-train A/B trial (2–6 months) with success metrics fixed in advance: Δ SEC (kWh/m³, normalized), Δ cleans per quarter, Δ chemical spend, Δ normalized permeate flow. Never touch compliance instrumentation (integrity tests, chlorine interlocks, turbidity reporting).

**Tools shortlist:** WaterTAP + IDAES/Pyomo + IPOPT (mechanistic twin, reconciliation, optimization); gPROMS or Sumo/Replica as commercial equivalents (Sichel; Jacobs/PUB); XGBoost/CatBoost + SHAP (surrogate/forecasting); OPC-UA client (open62541 / python-opcua); AVEVA PI or Ignition historian; MLflow or equivalent for model registry; drift monitors (KS/PSI) on input tags; CUSUM on reconciliation residuals.

**What the literature does not yet give you:** publicly reported RMSE/R² for full-scale commercial twins (vendors report % savings, not error metrics); payback periods; any closed-loop deployment in drinking water; sim-to-real methodology for RL in desalination (explicitly absent per the 2025 RL survey). Budget your own baselining accordingly.
