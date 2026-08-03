# ML, Optimization and AI for Ultrafiltration and Reverse Osmosis Water Treatment
## A synthesis report and from-scratch implementation playbook

*Compiled 2026-08-02 from eleven primary research files — eight core files plus three gap-filling notes in the 09 series. Audience: an ML/software engineer who wants both a complete map of the field and a buildable system.*

**Drill-down index** — every claim below traces to one of these files, which contain the full citation sets, equation derivations and per-paper detail:

| File | Contents |
|---|---|
| [`research/01_physics_foundations.md`](research/01_physics_foundations.md) | Transport models, CP/mass transfer, ASTM normalization, fouling indices, Hermia laws, energy bounds, hybrid-model taxonomy |
| [`research/02_ml_ro_modeling.md`](research/02_ml_ro_modeling.md) | ML for RO: ANN/tree/RNN/TCN/TFT/PINN/GP, features, accuracies, RUL, data-leakage discipline |
| [`research/03_ml_uf_fouling.md`](research/03_ml_uf_fouling.md) | ML for UF/MF/MBR: TMP forecasting, fouling classification, backwash/CEB/CIP optimization, coagulant dosing, integrity monitoring, imaging |
| [`research/04_optimization_algorithms.md`](research/04_optimization_algorithms.md) | Design MINLP, RTO, tariff/renewable scheduling, batch/CCRO, CIP scheduling, surrogate optimization, solver ecosystems |
| [`research/05_control_mpc_rl.md`](research/05_control_mpc_rl.md) | Control hierarchy, control-oriented models, MPC/EMPC/Koopman, RL, FDI and multivariate SPC |
| [`research/06_commercial_landscape.md`](research/06_commercial_landscape.md) | Vendor-by-vendor products, disclosed mechanics, audited vs marketing savings, market size |
| [`research/07_data_and_digital_twins.md`](research/07_data_and_digital_twins.md) | Sensors, SCADA/historians, digital-twin architectures, recalibration, MLOps, IEC 62443, operator trust, regulatory |
| [`research/08_implementation_resources.md`](research/08_implementation_resources.md) | WaterTAP/IDAES/Pyomo, GEKKO/do-mpc/CasADi, OMLT, datasets, repos, synthetic simulator recipe, build sequence |
| [`research/09_gap_1.md`](research/09_gap_1.md) | **RO continuous chemical dosing**: scaling thermodynamics at the wall, induction-time kinetics and the dose→time transfer function, field-proven antiscalant step-down search, tagged antiscalants, equation-oriented scaling constraints (WaterTAP/Reaktoro), biofouling detection (MFS/BFI) and biocide limits |
| [`research/09_gap_2.md`](research/09_gap_2.md) | **Primary-source verification** of the headline savings claims: Shim CIP-RL, Gaublomme horizon, Veolia Hubgrade, Pani; evidence grading, independent peer-reviewed anchors, reproduction recipe |
| [`research/09_gap_3.md`](research/09_gap_3.md) | **Brine/concentrate economics and high recovery**: disposal-route $/m³ and cost models (USBR/TWDB), the disposal-cost-aware recovery optimum, LSRRO/OARO cost optimization (Atia 2023), MLD/ZLD commercial landscape |

---

## 1. Executive summary

### 1.1 What the field actually delivers

Membrane desalination is a mature, thermodynamically-bounded process. The thermodynamic minimum work of separation for 35 g/L seawater at 50 % recovery is **1.06–1.07 kWh/m³** (Lin & Elimelech; Elimelech & Phillip, *Science* 333:712, 2011, DOI 10.1126/science.1200488) — sources in this corpus quote 1.06 and 1.07 for the same quantity, and one vendor-side source widens the "practical floor" to 0.8–1.5 kWh/m³ (Sichel/Siemens PSE). Real SWRO trains run **2.5–4.0 kWh/m³** for the RO block and 3.5–4.5 kWh/m³ plant-wide; BWRO runs **0.36–1.51 kWh/m³**; the best new plants (Taweelah 2.81, Jubail 3A <2.80 kWh/m³) and the DESALRO 2.0 record of **1.861 kWh/m³** (Danfoss, May 2024) sit close to what hardware allows. **The addressable ML/optimization headroom at a modern, well-run plant is therefore single-digit percent, not tens of percent.** Any claim above ~20 % SEC reduction on a modern ERD-equipped SWRO train is a baseline artifact, a whole-process redesign, or marketing.

The credible, controlled numbers cluster tightly:

| Lever | Credible band | Best-evidenced single result |
|---|---|---|
| RO energy (setpoint/recovery RTO) | **4–10 %** | 4.2 % / 7.1 % / ~10 % field-measured on a two-stage BWRO (Gao, Jarma, Christofides & Cohen, *Water* 17:2363, 2025, https://doi.org/10.3390/w17162363); Synauta 9.7 % six-month average, 18 % instantaneous (https://smartwatermagazine.com/news/synauta/machine-learning-delivers-energy-savings-desalination) |
| RO energy at mega-scale | **~5 %** | Gradiant SmartOps at ENGIE Middle East SWRO >200,000 m³/d, **ISO-IPMVP-verified** (https://www.gradiant.com/success-stories/smartops-ai-desal-optimization/) |
| Plant-wide MILP-over-ANN energy | **~8 %** | H2Oaks BWRO, 14,542 hourly SCADA rows, CPLEX (Membranes/PMC 2022, https://pmc.ncbi.nlm.nih.gov/articles/PMC8879670/) |
| CIP/cleaning chemicals (RO) | **10–25 %** | Synauta A/B trial: 8.7 % EDTA, 4 fewer cleans, **+6.2 % permeate** vs a parallel control train (https://smartwatermagazine.com/news/synauta/ml-optimizes-ro-membrane-cleans-62-more-permeate-production-challenging-conditions) |
| CIP scheduling (forecast + RL) | **~16 % opex, simulated** | −16.13 % operating cost and +139.53 % run time at the cost-optimal CIP pressure threshold (Shim, Lee, Park, Moon, Lee & Cho, *Desalination* **614:119193**, 2025, DOI 10.1016/j.desal.2025.119193). **Now verified verbatim against the author-written abstract — but simulation-only, on an industrial UPW-grade RO train whose economics are dominated by cleaning chemicals and membrane replacement; the +139.53 % is the mechanism of threshold deferral, not a fouling-rate benefit** ([`research/09_gap_2.md`](research/09_gap_2.md) §1) |
| UF/MBR cleaning chemicals (demand-driven vs calendar) | **25–75 %** | Henriksdal pilot: 14.02 → 3.48 M SEK/yr, −95 % GWP (Membranes/PMC 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11205864/) |
| Coagulant dose (UF pretreatment) | **20–30 %** | −22 % dose ≈ 21 M KRW/yr, Conv1D+GRU on 5 yr of minute data (*Chemosphere* 2023, https://www.sciencedirect.com/science/article/abs/pii/S0045653523032599); −29 % via cycle-to-cycle resistance control (*Desalination* 2016, https://www.sciencedirect.com/science/article/abs/pii/S0011916416311870) |
| Backwash/permeate-pump energy (UF) | **4–31 %** | Pontryagin adaptive optimal control: 4–9 % hollow-fibre MF, 28–31 % flat-sheet UF (Membranes/PMC 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12195455/) |
| Batch/CCRO vs continuous | **37 % (CCRO) / 64 % (batch)**, modeled | Warsinger, Tow, Nayar, Maswadeh & Lienhard, *Water Research* 2016; OCWD pilot lifted recovery 85 % → 92 % |
| Design-time (superstructure/GA) | **7–20 %** | SPSP two-pass ≈7 % pumping energy (DuPont/FilmTec); species-conserving GA on module geometry −20.6 % SEC, +2.51 % rejection (PMC 2021) |
| **Antiscalant dose (RO, model-free step-down search)** | **26–90 %** | 2.0 → **0.2 mg/L** (Kamerik, NL) and 4.5 → **0.6 mg/L** (Brabrand, DK) on 80 %-recovery groundwater RO pilots, judged on flat temperature-corrected NDP, co-developed with Grundfos as a smart dosing pump (Mangal, Yangali-Quintanilla, Salinas-Rodríguez et al., *J. Membr. Sci.* 650:120717, 2022, https://doi.org/10.1016/j.memsci.2022.120717); **−26 %** via imaging-guided step-down at a 100-MGD reclamation facility (Rahardianto, Gu, Khan & Plumlee, *AWWA Water Sci.* 2:e1196, 2020, https://doi.org/10.1002/aws2.1196) |
| **Recovery at an inland BWRO with priced brine** | **≈$0.28 per m³ of product per +10 recovery points** at a $2/m³ disposal price | Disposal-term sensitivity of LCOW, larger than any published ML *energy* saving on BWRO; TWDB's natural experiment — same-size Texas plants at **$0.39/m³ (surface discharge) vs $0.86/m³ (evaporation ponds)** ([`research/09_gap_3.md`](research/09_gap_3.md) §1, §3.2) |

Two results sit outside the band for legitimate reasons: the AI+NSGA-II BWRO study reporting **>50 % energy reduction** did so by moving the plant from a fixed 15 % recovery to an optimized 50–70 % region (*Water Research* 2025) — that is a redesign, not tuning; and CCRO/batch RO savings are *process-architecture* savings, not control savings. (That NSGA-II result is better read as a *disposal-volume* result: 15 % → 65 % recovery drops brine per product from 5.67 to 0.54 m³/m³, worth ~$10 per m³ of product at $2/m³ disposal — an order of magnitude more than its energy saving.)

**Three corrections the gap-filling pass makes to the headline story:**

1. **At an inland plant, energy is the wrong headline.** The SEC-versus-recovery trade that dominates §2.9 and §4.2 is a coastal story. Inland, every m³ of concentrate is a priced liability at **$0.05–0.30/m³ (surface outfall), $0.32–0.66 (sewer), $0.54–2.65 (deep-well injection), $0.74–1.95 (land application), $3.28–10.04 (evaporation pond)** and ~$5+/m³ for thermal ZLD — one to three orders of magnitude above the marginal energy cost of one more m³ of permeate. Adding the disposal term to the objective moves the closed-form optimum from `Y* ≈ 41 %` (coastal, near-free outfall) to `Y* ≈ 96 %` (inland, $2/m³) — at which point the binding constraint is **scaling, not energy**. Any RTO that maximizes efficiency without `c_dis(1−Y)/Y` parks the plant at the wrong recovery. See §4.8.
2. **The largest un-modelled chemical lever is antiscalant, not CIP.** The state of practice is a **3–10× overdose**, and the dose–performance curve is **U-shaped** — 5.0 mg/L performed *worse* than 0.2 mg/L at 765 mg/L concentrate Ca²⁺ because calcium phosphonate precipitated. Fouling-related cost is ~**24 % of RO OPEX** across seven audited full-scale Dutch installations (Jafari et al., *Desalination* 2021), so this is not a petty-cash line. The lever needs no ML: a model-free step-down search on normalized NDP is field-proven. See §2.10 and §4.7.
3. **Two vendor bands in this report rested on numbers that do not survive primary-source checking.** Veolia's Hubgrade figures are all **activated-sludge aeration, sewer hydraulics and chemical precipitation — not membranes** — and cannot legitimately populate a UF/RO band; one widely-circulated €1.5 M/20 % claim traces only to an aggregator with a self-assigned evidence score and is removed here. Pani's own material contains a factor-of-two internal contradiction (2.2 % vs 4.2 % energy) and an arithmetic that does not close ($700 k energy savings against $260 k stated net OPEX savings). Details and the revised grading: §6.1–6.2 and [`research/09_gap_2.md`](research/09_gap_2.md).

### 1.2 Where the field is real, and where it is not

- **Real and deployed**: ASTM D4516 normalization; multi-loop PI and DMC/CMPC on RO trains (Alatiqi 1989 → Assef 1997 → Burden 2001); supervisory SEC optimization with PI execution (Gao 2025, field-tested); commercial ML *advisory* layers (Synauta, Gradiant, Veolia Smart Membranes, IDE Carlsbad twin); adaptive-dynamic PCA monitoring evaluated over 1–2 years of real SCADA (Hering/Newhart group); MPC and extremum-seeking control closed-loop on a CCRO **pilot**; the **model-free antiscalant step-down dose search**, run to convergence on two groundwater RO pilots with an arrestability proof-of-principle (jar, lab-cell and pilot) behind it; and the **Membrane Fouling Simulator** as a side-stream biofouling early-warning device.
- **Published but simulation-only**: essentially *all* reinforcement learning for RO — cascade DDPG/DQN (Golabi et al., *Applied Intelligence* 54:6333, 2024), multi-agent QMIX/VDN two-stage RO (*Desalination* 2025), CNN-SAC for PV-RO (Soleimanzade 2022), DDPG on TMP (Bonny 2022); Koopman EMPC (BSM1); LSTM-MPC for CCRO (offline replay). **No RL agent runs autonomously in a production desalination plant.** A 2025 survey of 147 water-sector digital-twin studies found only **4 addressed desalination** at all (https://www.mdpi.com/2073-4441/17/20/2957).
- **Genuinely missing from the literature**: a supervised classifier that labels UF fouling by chemical type (organic/bio/colloidal/scaling) from routine online SCADA alone; a substantial labelled corpus of CNNs on membrane-autopsy SEM images; RO-*element*-specific remaining-useful-life models; peer-reviewed payback periods for ML deployments; any published sim-to-real / domain-randomization methodology for desalination RL; **any ML controller for antiscalant dose** (targeted OpenAlex searches return essentially zero on-topic works); **any LSRRO/OARO cost optimization that includes mineral scaling** (the authors' own caveat) and any LSRRO pilot demonstration; and **DBNPA shock concentrations, contact times and frequencies**, which live in vendor bulletins rather than the open literature.

### 1.3 The six things that determine whether a project succeeds

1. **Normalize before you model.** ASTM D4516 / FilmTec normalization (TCF, NDP, normalized permeate flow and salt passage) turns confounded raw tags into the fouling signal itself. Every credible plant-facing result, academic and commercial, does this first — Synauta normalizes to 25 °C / 32,000 ppm before optimizing.
2. **Split by time, never by row.** Jeong et al. (*ES&T* 55:11348, 2021, https://pubs.acs.org/doi/abs/10.1021/acs.est.1c04041) showed random-split CV on near-duplicate experiments yields falsely high accuracy. R² = 0.99 on plant TMP is a leakage alarm, not a result.
3. **Gradient-boosted trees are the baseline to beat**, not the thing to skip: XGBoost/CatBoost beat ANNs on tabular RO (R² > 0.98), beat deep nets on full-scale forecasting by 3–4 pp MAPE, and beat NN/GPR on 426 days of UF data (R² 0.99).
4. **Physics is the sample-efficiency multiplier.** Serial hybrids (ML predicts a *parameter* of a mechanistic model) and PINNs are what extrapolate: PINN R² 0.96/0.97 on months of full-scale SWRO; Hermia+SVM on fluorescence at R² 0.87–0.99 with <10⁴ samples.
5. **Deploy advisory first.** Every commercial desalination twin surveyed runs open-loop; IEC 62443 zones-and-conduits makes closed-loop writes expensive, and the EU AI Act classifies treatment-process AI as high-risk with a **December 2027** deadline. Synauta captured most of its value by emailing three setpoints daily.
6. **Price the brine and the scaling constraint before you optimize anything.** Get a site-specific disposal price (sewer surcharge schedule, DWI quote, land + net-evaporation for ponds) and a Pitzer-based saturation profile at the **wall of the tail element** — not the feed, not the bulk concentrate. Those two numbers decide whether your project is an energy project, a recovery project or a chemistry project. At most inland plants they say "recovery", and a single correct recovery point is worth more than the entire ML energy stack.

---

## 2. Process fundamentals and physics models

Full derivations, correlation tables and source links: [`research/01_physics_foundations.md`](research/01_physics_foundations.md).

### 2.1 The modeling hierarchy

Five nested levels: (1) **membrane point model** — local water/salt flux; (2) **channel model** — spacer-filled hydrodynamics and concentration polarization; (3) **element model** — 8" spiral-wound, 37.2 m² (400 ft²) active area, integrated along the leaf; (4) **vessel/stage model** — 6–8 elements in series, tapered arrays, interstage boosters; (5) **plant model** — pretreatment, HP pumps, ERDs, post-treatment and economics. A twin that stops at level 1 misestimates stage-2 flux distribution and scaling risk; one that stops at level 4 cannot optimize energy or chemicals. Level 2 is not optional: CFD on a 2.05 m × 0.9 m leaf with a 0.86 mm channel showed removing the spacer raised wall concentration **84.67 %** over inlet vs **15.30 %** with it, `k` rising 7.95×10⁻⁵ → 1.59×10⁻⁴ m/s (Lin et al., Membranes 11(5):353, 2021).

### 2.2 RO transport

**Solution-diffusion (SD)**, the model inside every commercial projection tool and the mechanistic half of every published hybrid:

```
J_w = A[(P_f − P_p) − σ(π_m − π_p)]        σ ≈ 1 for high-rejection RO
J_s = B(c_m − c_p)
c_p = J_s/J_w = B·c_m/(J_w + B)            R_obs = 1 − c_p/c_b
```

`A` [L m⁻² h⁻¹ bar⁻¹], `B` [m s⁻¹]. WaterTAP's seawater defaults — useful order-of-magnitude anchors — are **A ≈ 4.2×10⁻¹² m/(s·Pa)** and **B ≈ 3.5×10⁻⁸ m/s**.

**`B` is not a membrane constant** — the single largest structural error in RO models. Measured rejection varies strongly with feed salinity (Wang, Elimelech et al., *ES&T* 55, 2021, https://pubs.acs.org/doi/10.1021/acs.est.1c05649), and water transport may be pore-flow rather than diffusive (Tong et al., *Science Advances* 9, 2023). The replacement is the **solution-friction analytical approximation**, trading salinity-indexed `B` for two salinity-invariant intrinsic parameters:

```
J_s = P(√(C² + c_m²) − √(C² + c_p²))
B_obs = P(√(C²+c_m²) − √(C²+c_p²))/(c_m − c_p)
```

validated on NaCl to **3.64 M**; NF90 gives C ≈ 0, P ≈ 3 L m⁻² h⁻¹ bar⁻¹, chlorinated NF90 P ≈ 99 (https://pmc.ncbi.nlm.nih.gov/articles/PMC12895524/). Three intrinsic parameters `(A, P, C)` replace a salinity lookup table for `B`.

**Spiegler–Kedem–Katchalsky** for NF and loose RO adds a reflection coefficient: `J_v = L_p(ΔP − σΔπ)`, `J_s = P_s Δc_s + (1−σ)J_v c_m`, `R_obs = σ(1−F)/(1−σF)`, `F = exp[−(1−σ)J_v/P_s]`. WaterTAP offers SD and SKK as a switch on the same unit model.

**Temperature.** `A` and `B` are both Arrhenius-activated with *different* activation energies — which is why rejection degrades in warm feed and why one TCF applied to both fluxes mispredicts summer permeate TDS. DuPont FilmTec:

```
TCF = exp[2640(1/298 − 1/T)]   T ≥ 298 K
TCF = exp[3020(1/298 − 1/T)]   T ≤ 298 K
```

(E_a ≈ 21.9 and 25.1 kJ/mol). Sources in this corpus quote the generic constant as **K ≈ 2500–3020** depending on membrane; ASTM D4516's fallback when vendor data are unavailable is `TCF = 1.03^(T−25)` (T in °C), matching the field rule of **2.5–3.0 % flow change per °C**. A 1 °C temperature-sensor error therefore biases normalized flow by ~3 %.

### 2.3 Osmotic pressure

- **van 't Hoff**: `π = i·C·R·T` (i = 1.9 for NaCl; R = 0.083145 L bar mol⁻¹ K⁻¹). Adequate to ~0.6 M. The engineering shorthand quoted across the corpus is **0.7–0.8 bar per g/L TDS** (0.75–0.8, 0.7854, 0.78 in different files); ~27–28 bar at 35,000 mg/L.
- **ASTM D4516 form** (mg/L, kPa): `π_fb = 0.2654·C_fb·(T+273.15)/(1000 − C_fb/1000)`.
- **FilmTec form** (psi): `π = 1.12(273+T)·Σm_j`.
- **Non-ideal**: OLI regression for NaCl `π = 5.94028C² + 37.4521C` (bar, mol/L) above 0.6 M. van 't Hoff and OLI cross near 1.9 M, agree within 5 % over 1.0–2.4 M, then diverge by up to **30 % in π** and >50 % in derived power density above 2.4 M.
- **Pitzer inside the element model**: discretizing a 6 m vessel into **300 axial elements** and solving Pitzer activities locally showed ideality **overestimates osmotic pressure by ~9 %**, sulfate activity coefficients fall up to **65 %** inlet-to-outlet, and activity-based calculation predicts scaling onset **1 m earlier** along the vessel (Ruiz-García et al., Membranes 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC8154145/).

Rule: van 't Hoff/ASTM for BWRO ≤10 g/L; Pitzer/OLI for SWRO brine, ZLD, and every saturation index. TEOS-10 (http://www.teos-10.org/) is the right source for ρ(T,S), μ(T,S), D(T,S) feeding the Sherwood correlations.

### 2.4 Concentration polarization and the correlation that moves your P&L

Film theory: `(c_m − c_p)/(c_b − c_p) = exp(J_w/k)`, `k = Sh·D/d_h`. Candidate correlations:

| Correlation | Form | Note |
|---|---|---|
| Schock & Miquel (1987) | `Sh = 0.065 Re^0.875 Sc^0.25`; `f = 6.23 Re^−0.3` | industry default for spacer-filled channels |
| Koutsou et al. | `Sh = 0.2 Re^0.57 Sc^0.40` | |
| WaterTAP default | `Sh = 0.46(Re·Sc)^0.36` | what the open-source stack ships |
| UCLA (Gao 2025 field study) | `Sh = 0.38 Re^0.54 Sc^0.33` | used in a field-validated controller |
| Generic literature fit | `Sh ∝ Re^0.68 Sc^0.20` | |

**Correlation choice is a first-order economic decision, not a detail.** Propagating Schock & Miquel vs Koutsou vs CFD-fitted correlations through one process model shifted predicted recovery by **−4.7 to +1.9 %**, pressure drop by **−53 to +83 %**, and specific energy by **−0.81 to +1.6 kWh/m³** (Membranes 11(5):338, 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC8147287/) — comparable in magnitude to the entire energy-optimization opportunity.

The same paper provides a **direct CP-modulus correlation that bypasses film theory**, fitted on 228 CFD cases (Re_c 1.12–274, Sc 111–4475, channel 0.2–1.4 mm, GR = L_f/D_f 2–6):

```
M_CP − 1 = C·Re_c^α·(10⁴·Re_t)^β·Sc^γ·GR^δ
```

| Spacer | C | α | β | γ | δ | MAPE |
|---|---|---|---|---|---|---|
| Cavity | 2.55e-4 | −0.350 | 1.11 | 0.611 | 5.40e-4 | 0.375 % |
| Submerged | 5.55e-3 | −0.422 | 1.09 | 0.672 | 0.536 | 0.516 % |
| Zigzag | 3.24e-4 | −0.394 | 1.12 | 0.597 | 2.18e-4 | 0.516 % |

with paired friction `f = C'·Re_c^α'·GR^δ' + ζ` at 0.97–1.48 % MAPE (cavity 14.8, −0.910, −0.525, 0.0256). Vendors instead collapse level 2 into element recovery via the widely reproduced `β = exp(0.7·Y_element)`, capped at 1.2, plus `Δp ≈ 0.01·q_avg^1.7` — convenient but spacer-specific, and flagged in the source file as "widely reproduced" rather than primary-verified.

### 2.5 Element, vessel and stage integration

March along the leaf coordinate (100–300 segments per vessel; the Pitzer study used 300):

```
dQ_f/dx = −J_w(x)·w
d(Q_f c_f)/dx = −J_s(x)·w
dP_f/dx = −f ρ u_c²/(2 d_h)
```

closed per segment by §2.2–2.4. Aggregates: `Y = Q_p/Q_f`; `CF = (1 − Y(1−R))/(1−Y)`; **log-mean feed-brine concentration** `C_fb = C_f·ln[1/(1−Y)]/Y` (the arithmetic mean is wrong at high recovery — a common bug). Hard constraints any optimizer must carry: lead-element flux ≤ ~30–35 LMH, element recovery ≤ ~15 %, minimum concentrate flow per 8" vessel ≥ ~3.6 m³/h, vessel Δp < ~4 bar, applied pressure ≤ 83 bar. Element-by-element models agree with ROSA to ~95 %. Lead elements run 2–3× tail flux — which is why fouling concentrates in stage 1 and scaling in the tail.

### 2.6 Normalization — the non-negotiable data layer

ASTM D4516 (https://www.astm.org/Standards/D4516.htm):

```
Q_ps = Q_pa · (P_fs − ΔP_fbs/2 − P_ps − π_fbs + π_ps)/(P_fa − ΔP_fba/2 − P_pa − π_fba + π_pa) · TCF_s/TCF_a
NDP  = P_f − ΔP_fc/2 − P_p − π̄_fc + π_p
SP_s = SP_a · (EPF_a/EPF_s)(CF_s/CF_a)(STCF_a/STCF_s)
```

D4516 applies temperature correction only to water production, not salt passage — a known limitation (Zhao & Taylor, *Desalination* 2005). Diagnostic rules a monitoring layer should encode:

- Normalized permeate flow ↓ >10–15 % → fouling/compaction → CIP trigger (DuPont uses 15 %; Toray tolerates up to 50 %).
- Normalized salt passage ↑ >10 % at steady flow → oxidation damage or o-ring leak.
- Both moving together → tail scaling.
- Stage Δp ↑ >15 % → colloidal/biofouling in the feed spacer.

**Calibration target for drift models**: a 5,000 m³/d SWRO plant in Gran Canaria (56 vessels × 7 elements, ~27,000 h over 4 years) lost **~30 % of A** and gained **~70 % in B**; recovery drifted 46 % → 38 %; SEC 3.75–4.25 kWh/m³ with HPP alone at ~3.04 (https://pmc.ncbi.nlm.nih.gov/articles/PMC8540465/). Use `B(t) = B₀(1 + βt)` with β ≈ 5–15 %/yr against a 20 %/yr replacement-factor economics.

### 2.7 Feedwater indices

- **SDI (ASTM D4189)**: `SDI₁₅ = 100(1 − t_i/t_f)/T`, 0.45 µm at 207 kPa dead-end; design limit <4 for RO feed. Not temperature- or pressure-corrected, non-linear in colloid concentration, measured manually 1–3×/day — a poor ML input as-is.
- **MFI** from cake-filtration theory: `t/V = μR_m/(ΔP·A) + μI/(2ΔP·A²)·V ≡ a + MFI·V`; pressure- and temperature-correctable. **UMFI** for low-pressure membranes: `1/J'_s = 1 + UMFI·V_s` [m²/L], valid in both constant-pressure and constant-flux modes.
- **Scaling**: LSI = pH − pHs (ASTM D3739 decomposition), computed on the **concentrate**, not the feed; above ~10,000 mg/L switch to Stiff & Davis. Modern antiscalants allow stable operation at concentrate LSI +1.8 to +2.5. For sulfates and silica use Pitzer/OLI saturation ratios. LSI is a thermodynamic tendency, not a rate — kinetics must be modelled or learned separately, which §2.10 now does.

### 2.8 Ultrafiltration physics

Darcy with resistance-in-series: `J = ΔP_TM/[μ(T)(R_m + R_cp + R_c + R_irr)]`, `TMP = (P_feed + P_conc)/2 − P_filtrate`, specific flux `L_p = J/TMP` temperature-corrected via `μ(T)/μ(20)` ≈ `1.025^(20−T)` to `1.03^(20−T)`. **Temperature normalization is the single most common failure in published UF ML work** — a model on raw TMP across a 5–25 °C seasonal swing spends most of its capacity learning the viscosity curve.

Cycling gives a free labelled decomposition every cycle, with no extra instrumentation:

```
R_rev^(k)  = R_end^(k) − R_PB^(k)                (backwash-recoverable)
ΔR_irr^(k) = R_PB^(k) − R_PB^(k−1)               (the chemical-cleaning target)
η_BW       = (R_end − R_PB)/(R_end − R_m)        (backwash efficiency label)
```

**Hermia blocking laws**: `d²t/dV² = k(dt/dV)^n`, equivalently `dJ/dt = −K J^(3−n)`, with n = 2 complete blocking, 1.5 standard, 1 intermediate, 0 cake. Constant-flux duals (the actual municipal operating mode), in TMP `p`: complete `p₀/p = 1 − K_br J₀V`; standard `(p₀/p)^0.5 = 1 − K_s²V`; intermediate `ln(p/p₀) = K_iV`; **cake `p/p₀ = 1 + K_c J₀V`** — TMP linear in cumulative specific volume, the workhorse for UF cycle models. Hermia's structural defect is that mechanisms cannot coexist.

Two fixes, both good ML insertion points:
- **Extended Hermia Model** lets `n` be continuous via `P = 2 − n`: `(J/J₀)^P ≈ 1/(1+kt)`, half-life `t½ = (0.5^P − 1)/k`. Across six datasets EHM RMSE was **0.0101–0.0682 vs 0.0287–0.1108** for the best classical mechanism; fitted P ranged 1.25–9.67, with P > 2 indicating mechanisms outside Hermia's four (https://pmc.ncbi.nlm.nih.gov/articles/PMC10056723). **Keep the functional form; let ML predict `k` and `P` from feedwater state.**
- **Field et al. (1995)** crossflow extension: `−dJ/dt = k(J − J*)J^(2−n)` with `J*` the critical/limiting flux. Definitions matter because setpoints are chosen against them: critical flux (`dm/dt = 0` below `J_c`), threshold flux (`dm/dt = a` below), boundary flux (`−α` below `J_b`, `−α + β(J − J_b)` above).

**Cycle economics**: `NWP = (J·t_f − J_bw·t_bw − V_CEB/A)/(t_f + t_bw + t_idle)`. Reported anchors: dead-end UF at 0.4 bar with 15-min interval and 30 s backwash gave the highest net flux (**27 LMH**) and lowest SEC (**146 Wh/m³**); flow-reversal backwash recovered 55 % of specific flux vs 53 % for chemically-assisted backwash at low dose.

### 2.9 Energy: the equation everything optimizes against

```
SEC       = ΔP(1 − η_E(1−Y))/(η_p·Y)
SEC_tr/π₀ = (1 − η_E(1−Y))/(Y(1−Y))          at the thermodynamic restriction ΔP ≥ π₀/(1−Y)
```

(Zhu, Christofides & Cohen, *I&EC Res.* 48, 2009, https://pubs.acs.org/doi/10.1021/ie9012826). Without an ERD this minimizes at **Y\* = 0.5 with SEC_tr = 4π₀** — the classic "optimal recovery is 50 %". With an efficient ERD it becomes monotonically increasing in Y, so energy-optimal recovery shifts **down** and the true optimum is set against membrane capital, pretreatment and brine-disposal cost; the RO-ERD closed form minimizes at **1.97 kWh/m³ at Y = 30 %**. Every RTO scheme in §4 tracks this minimizer as π₀(T,S) and A(t) drift. Hardware context: isobaric PX ERDs reach **98–99 % peak efficiency** to 83 bar with >35,000 units installed; HPP efficiency 88.5–90 % at 100,000 m³/d; ERD retrofit payback ≈ **1.3 years**.

### 2.10 Scaling kinetics — turning a saturation index into an operable rate constraint

Full derivations, parameter tables and validation conditions: [`research/09_gap_1.md`](research/09_gap_1.md).

§2.7 leaves LSI as a tendency. That is the gap that makes every recovery-pushing recommendation in this report unbounded, because real plants run concentrate LSI **+1.8 to +2.5** with antiscalant — i.e. deliberately and safely above the thermodynamic limit. Closing it takes three pieces.

**(a) Compute saturation at the right place.** `S_a,s = IAP_s/K_sp,s`, `SI_s = log₁₀ S_a,s`, with `IAP = Π(γ_i m_i)^ν_i` and activity coefficients from Debye–Hückel/Pitzer (OLI, PHREEQC or Reaktoro). The driving force lives at the **wall of the tail element**: `CF·β` with `CF = [1 − Y(1−R)]/(1−Y)` and `β = exp(J_w/k)`. Bulk concentrate understates it by β (typically 1.1–1.4, and **2–3× locally** in spacer regions, where polyamide roughness also creates flux hot-spots 3–6× the average). Reaktoro-in-WaterTAP evaluates scaling on the apparent species entering the RO plus the water removed *at the membrane interface*, `ṁ_H₂O^removed = ṁ_H₂O^in − ṁ_TDS^in·(ṁ_H₂O^interface/ṁ_TDS^interface)`, with a monotonicity constraint forcing the last node to hold the highest TDS.

**(b) Antiscalant does not lower saturation — it lowers the *rate*.** Vendor projection programs *display* a reduced saturation level with antiscalant, but the true saturation is unchanged; the inhibitor acts on nucleation and growth kinetics only (Mangal, IHE Delft/Twente PhD thesis, 2023). **Modelling antiscalant as a ΔSI credit is physically wrong and mis-locates the optimum.** The classical linearization is `ln t_ind = A + B/(ln S_w)²` with `B = β_g γ³ v_m²/(k_B T)³` — fit A, B per water and per scalant from jar tests or a scale-guard run, and that is the minimum viable kinetics model.

The most implementable closed form is Sagiv, Semiat & Shemer (Technion, *Applied Sciences* 14:4700, 2024, https://www.mdpi.com/2076-3417/14/11/4700), derived from a mass/momentum balance on a growing cluster (Stokes regime, `Re ≪ 1`) rather than from nucleation-rate proportionality:

```
n_c   = 32π V_m² γ³ / [3 (k_B T ln S_a)³]          S_a = C_f/C_e
dm/dt = 4 k_c A (C_f − C_e)^z / (4 + π u_f k_s)     (shear removal folded into k_s)
t_0A  = [(4 + π k_s u_f) M_w / (4 k_c N_A A(1)(C_f − C_e)^z)] · 3 n_c^(1/3)     (no antiscalant)
dθ/dt = k_a C_a(1−θ) − k_d θ  →  θ(t) = (a/b)(1 − e^{−bt}),  a = k_a C_a,  b = a + k_d
t_A   = (1/(b−a))[ b·t_0A − (a/b)(1 − e^{−b t_A}) ]                             (implicit; Newton in one variable)
```

`t_A → t_0A` as `C_a → 0` and is approximately linear in antiscalant concentration. **This is the missing dose→time transfer function.** Reported parameterization: γ = 9.25 mJ/m² (CaSO₄), z = 2, `k_c = 5.31×10⁻⁸` kg/(s·m²·mM²); fitted `k_s` = 1.73×10⁴ s/m (spiral-wound, Hasson), 2.43×10⁵ (spiral-wound, Li), 7.37×10⁴ (tubular); `k_a = 3.17×10⁻⁴` L/(mg·s), `k_d = 4.0×10⁻⁴` s⁻¹ for a phosphonic-acid sodium salt and `k_a = 1.0×10⁻³`, `k_d = 6.5×10⁻⁵` for a phosphinocarboxylic acid. Validation across six datasets: mean error **8.0 % (t_0A) and 8.7 % (t_A)**, individual range 0.4–20.0 %. The engineering payoff is the factorization: **`k_s` is the only system-specific parameter** (it absorbs channel geometry, spacer and local shear — characterize it once per element/spacer type), while `k_a, k_d` belong to the *scalant–antiscalant pair* and transfer.

**(c) The usable constraint** is that residence time in the supersaturated zone stays short relative to induction time:

```
t_A( S_a,wall(Y, J_w, pH), C_a )  ≥  λ · τ_res ,   τ_res ≈ L/u (+ recycle loops),   λ ≥ 10
```

evaluated on the **tail element, not the average**. For once-through RO `τ_res` is seconds, so nearly any dose passes and the real constraint is the residence time of *deposited* crystals in dead zones; for CCRO/batch RO the recycle makes `τ_res` the batch time and the constraint genuinely binds — which is also why batch RO's periodic desupersaturation resets the induction clock before nuclei reach critical size (Warsinger et al., *Water Research* 2018).

**Scalant-specific behaviour — one constraint cannot cover all four** (Tong et al., *Front. Environ. Sci. Eng.* 19(1):3, 2025, https://doi.org/10.1007/s11783-025-1923-9):

| Scalant | Control | Practical signature |
|---|---|---|
| **Gypsum** | crystallization-controlled, fast | SI 0.26 (ln convention) → ~50 % flux decline in 1,500 min; facet growth ~0.05 µm/min on [001] at SI ≈ 0.64; ~80 % flux recoverable by physical cleaning |
| **Silica** | polymerization-controlled, slow, effectively irreversible | needs SI 0.79 for the same decline; solubility 100–150 mg/L near neutral pH; pK_a ≈ 9.8 and polymerization **fastest at pH 8–9** — so high-pH boron designs are actively dangerous; not removable by physical cleaning |
| **Calcite** | pH-driven | in the FOCAPD optimization the calcite constraint was **active over the entire recovery range**: acid dose always sits at its scaling-limited value |
| **Calcium phosphate** | breaks the antiscalant assumption | above 80 % recovery on groundwater with **2.1 mg/L orthophosphate**, amorphous Ca-phosphate precipitated and phosphonates were *not effective*; the dose search could no longer converge |

**Screen the feed for orthophosphate and silica before promising high recovery** — they are the two ions that silently cap it.

**Where the knee is.** In the WaterTAP high-recovery study (Amusat, Dudchenko, Atia & Bartholomew, FOCAPD 2024), LCOW is essentially flat with recovery until the gypsum constraint activates and then rises steeply: **softening onset at 64–66 % recovery for brackish and 74 % for seawater**, both at 5,000 m³/d. Below the knee the only chemical lever is acid; above it, calcium removal dominates the cost stack.

### 2.11 Biofouling — the constraint no saturation index can see

Biofouling appears as **feed-channel pressure drop long before it appears in flux**, and it is a feed-*spacer* phenomenon (Vrouwenvelder et al., *Water Research* 2009). The clean quantitative index is Huisman, Franco-Clavijo, Vrouwenvelder & Blankert (*J. Membr. Sci.* 668:121400, 2023):

```
BFI = 1 / t_(Δp_rel = 100 %) ,      Δp_rel(t) = (Δp(t) − Δp₀)/Δp₀
```

— the inverse of the time to double clean-channel pressure drop, dimensionally a **fouling rate / required cleaning frequency**, so it drops straight into the renewal-reward CIP objective of §4.4 as `1/T_run`. Two findings carry: the index correlates with biofilm volume **independent of applied crossflow velocity**, and Δp must be scaled by the velocity at the **perimeter of a spacer cell**, not the average channel velocity, or cross-plant comparisons are meaningless. The measuring device is the **Membrane Fouling Simulator (MFS)** — a flat-sheet side-stream cell with the plant's own feed and the same channel height, spacer and crossflow as the spiral element, monitored on Δp, optionally with OCT.

**The penalty, and why rejection-based diagnostics miss it entirely**: in the modelled scenario of the npj Clean Water 2022 RO biofouling review, at constant 85 % recovery there is a **~10-day lag with negligible pressure change**, then feed pressure **+27 %** and brine pressure +13 % over 20 days, peak flux 9 → 7.3 µm/s, **SEC 0.4 → 0.5 kWh/m³ (+27 %)** — with permeate TDS essentially unchanged (rejection 99.72–99.76 %). **A diagnostic rule keyed on salt passage will not see biofouling at all**; use feed-channel Δp.

Offline biofouling-potential proxies (ATP, total direct cell count, AOC, biofilm formation rate) flag problem biofilm before any Δp rise but need sampling; reported AOC targets span <100 µg/L (LeChevallier) to ~50 (Bradford) to <10 (van der Kooij), with Hijnen's spiral-wound threshold at **~1 µg/L** — below routine assay capability, which is precisely why online Δp on an MFS is the practical instrument. Online flow cytometry is the emerging real-time substitute.

**Biocide constraints that bound any optimizer:**

- **Free chlorine is not an option on polyamide**: ~**1000 ppm·h** cumulative tolerance, continuous exposure **<0.1 ppm**; degradation is N-chlorination → irreversible Orton rearrangement → chain scission (one case gained 65 % flux while losing 7 % rejection). It also fails biologically (spore-formers survive, regrowth on chlorine-generated AOC) and makes DBPs.
- **Dechlorination placement is a control variable**: SMBS:free-chlorine ≈ 3:1, and moving the SMBS injection point *forward* along the pretreatment line **increased** biofouling, because upstream chlorination manufactures the AOC that feeds the biofilm.
- **Your antiscalant may be feeding the biofilm.** Phosphonate products supply phosphorus, usually the limiting nutrient; the 2022 review states polyphosphonates "most likely accelerated biofilm formation." A second, independent reason to run the *minimum* effective dose, and to prefer phosphorus-free polycarboxylates on P-limited feeds.
- **DBNPA** is the standard polyamide-compatible non-oxidizing shock biocide (highly rejected, field-demonstrated, expensive); chlorine dioxide is reported most effective in first-pass RO/NF; dichloroisocyanurate inactivated biofilm as well as chlorine while preserving flux and rejection where chlorine-exposed membranes fell from ~99 % to **80 %** rejection.
- **Shock dosing has an optimizable interior with a damage-side failure mode.** The best-quantified study is in membrane distillation but the structure transfers: 120 mg/L Cl₂ for 2 h quenched with NaHSO₃ at 2.5:1 cut 110-h flux loss from **49 %→18 % at 45 °C** and **67 %→21 % at 55 °C**, with biofilm 68–73 % thinner — while the *same* shock at 65 °C **caused failure** (pore wetting at 90 h). As with antiscalant overdose, the curve is U-shaped and the failure above the optimum is membrane damage, not under-treatment.
- Chlorinated feed also indirectly reduces scaling (sparser biofilms entrap less Ca/Mg), so **biofouling and scaling are coupled, not independent**.

---

## 3. Machine learning methods

Full per-paper detail: [`research/02_ml_ro_modeling.md`](research/02_ml_ro_modeling.md) (RO) and [`research/03_ml_uf_fouling.md`](research/03_ml_uf_fouling.md) (UF/MF/MBR).

### 3.1 Taxonomy

Five families, in increasing order of physics content (von Stosch et al., *Comput. Chem. Eng.* 60, 2014): (1) **pure data-driven static regression** — MLP, SVR, RF, XGBoost on tabular features; (2) **sequence models** — LSTM/GRU, TCN, ConvLSTM, TFT, Informer-family; (3) **serial hybrid (grey-box)** — ML predicts a *parameter* of a mechanistic model which produces the output, `NN(features) → R_f(t) → SD model → J_w, c_p`; best interpretability, accuracy capped by the white-box model's fidelity, and **the most sample-efficient hybrid available — the default below ~10⁴ samples**; (4) **parallel/residual hybrid** — `ŷ = f_phys(x;θ) + g_ML(x)`, robust when the physics is structurally right but biased; (5) **physics-constrained loss (PINN)** — `L = L_data + λ₁L_PDE + λ₂L_BC + λ₃L_monotonicity`, enforcing e.g. `J_w = A(T)(ΔP − Δπ)` and `∂rejection/∂T < 0` as soft constraints, with `A(T) = A_ref exp[−E_a/R(1/T − 1/T_ref)]` learned jointly.

### 3.2 The canonical feature set

Union across the RO literature: feed conductivity/TDS, temperature, pressure and flow; permeate flow and conductivity; concentrate pressure and flow; recovery; pH; ORP; turbidity/SDI; per-stage Δp; pump power/VFD frequency; **time since last CIP**; **membrane age** — plus 6–48 lagged steps of each for sequence models. For UF add feed turbidity, **UV254/TOC/DOC**, coagulant dose, backwash flow, valve/mode state, and per-cycle engineered features (`R_start`, `R_end`, `R_PB`, `η_BW`, cycle duration, permeate volume, mean flux, fitted Hermia `n` and `k`).

Two independent confirmations that the physics features are the right features: RFE + SHAP on a holistic RO framework identified **membrane age, feed temperature, feed pressure, feed flow and chloride** as dominant — the model rediscovered the ASTM D4516 normalization variables; and SHAP on a CatBoost/XGBoost SEC model recovered recovery, flux and feed salinity, matching the mechanistic SEC identity.

**Feature importances do not transfer between MBR and pressurized UF.** SHAP on AnMBR ranks SMPp/SMPc (0.281) > EPSp/EPSc (0.110) > organic loading rate (0.106); full-scale MBR ranks F/M ratio and MLSS. **None of these variables exist in surface-water or seawater UF.** What does transfer: target engineering (specific flux over raw TMP, per-cycle-phase models, ΔR_irr as the cleaning target), sequence-model pathologies and their fixes, the SHAP workflow, uncertainty quantification, the R_BP/R_cake resistance-decomposition control matrix with H_Target/H_Lim thresholds (*Water Research* 2026, https://www.sciencedirect.com/science/article/pii/S004313542600117X), and cleaning economics.

### 3.3 What each architecture achieves — reported accuracies

**Tabular / static (the strong default):**

| Study | Target | Result |
|---|---|---|
| Small-scale SWRO, Korea coasts (*Desalination* 2025) | salt rejection, energy | **XGBoost R² > 0.98**, beat RF and RNN |
| SEC of SWRO plants (*Desalination* 2025) | SEC | CatBoost/XGBoost beat NNs; SHAP recovers mechanism |
| Holistic RO framework (*Desalination* 2024) | RO performance | **XGBoost R² = 94.75, RMSE = 0.181** |
| UF pretreatment of SWRO, 426 days (*JWPE* 2025) | flow rate, membrane resistance | **Ensemble R² = 0.99, RMSE 3.08 L/min**; GPR 0.98–0.99 |
| AnMBR fouling factor (*JMS* 2023) | fouling factor | **RF R² = 0.906** vs ANN 0.800; ANN topology 14-9-6-1, RF 1200 trees |
| Full-scale MBR + XAI (*Processes* 13(8):2352, 2025) | **specific flux** (not TMP) | CatBoost R² = 0.8374 |
| Textile MBR (KAUST, *JWPE* 2025) | TMP | RF R² 0.95 train / **0.86 test**, RMSE 1.75/3.3 kPa — an honest gap |
| UF membrane design (Zhang et al., *ES&T* 2023) | permeability, removal, fouling ratios | XGBoost/CatBoost on 320 records × 21 features; test R² 0.83/0.84/0.78/0.62/0.73 |

Typical hyperparameters: 100–1000 trees, depth 4–8, lr 0.01–0.1, early stopping on a **chronological** validation block; SHAP near-universal post-2022.

**Sequence models.** **LSTM/GRU** were best for TMP and energy in a five-model comparison on high-salinity SWRO with NAOMI imputation (*Desalination* 2023), and stationarity is the decisive preprocessing step — pairing autoregressive LSTM/GRU with **ADF testing and first-order differencing** enables long-horizon TMP prediction from short-sequence inputs at **GRU R² = 0.890** on independent plant data (*JWPE* 2025). Difference the series, model ΔTMP, integrate back. A **TCN** of dilated 1-D convolutions forecasting pressures at both ends of the vessel beat LSTM, GRU and CNN-LSTM on **Carlsbad plant data** (Pham, Do & Do, PHM Society 2024), and a multivariate TCN on ~2 years of real RO operation reached **RMSE 0.023 (normalized Δp), 0.012 (permeate TDS), 0.007 (feed pressure), ρ 0.96–0.99** using **cleaning-history covariates** — time since last cleaning and number of cleanings (Karimanzira & Rauschenbach 2021). The **TFT** hit **R² = 0.9813 with its static-covariate encoder vs 0.8980 without and ~0.9364 for LSTM** on RO Δp (*JWPE* 2024), earning its keep when you have multiple trains with static metadata and need interpretable multi-horizon quantiles. **Informer-family long-sequence** models reached **R² 0.82 vs 0.65 for a 1D-CNN+LSTM** on the same industrial RO data — a clean head-to-head showing attention's advantage specifically at long horizons. **ConvLSTM** gave **R² = 0.960 (1-day) / 0.942 (7-day)** on full-scale ZLD RO (*ES&T* 2025), and **graph attention** (DMGTNet) is the right architecture when N parallel racks share a feed.

**Hybrid and physics-informed.** The canonical serial hybrid is **Gaublomme et al.** (*Desalination* 2023): a mechanistic SD core plus **RNN-LSTM** forecasting fouling-sensitive parameters (`A`, feed-spacer channel height, `B`) as functions of a learned membrane-resistance state, with feed properties, recovery setpoint and CIP events as inputs; RNN-LSTM clearly outperformed ARIMAX. **The horizon discrepancy carried in earlier drafts is now resolved from the Ghent green-OA full text** (*Desalination* **564:116756**, 2023, DOI 10.1016/j.desal.2023.116756, https://biblio.ugent.be/publication/01H8BH8GMBJQ4W31AWX75490QX): **8 months is the test partition** of the data-driven fouling model (train 2017 / val 01–04 2018 / test 05–12 2018, ≈50/15/35), while **2.5 months (15 Jun – 31 Aug 2018) is the hybrid-model simulation window, selected because fouling prediction was good there** — a favourable-conditions selection worth carrying as a caveat. The authors themselves claim only "a prediction horizon of several months," and **no error statistics are reported for the 2.5-month hybrid window**. Implementable detail now verified: FARYS (Belgium), Albert Canal surface water, 475,000 m³/yr across four double-pass lines at 23–25 m³/h, SUEZ AK-440 membranes, **58 months / ~2.56 M 1-minute records subsampled to 30 min**; the learned quantity is *additional* membrane resistance `R_m,a`, fed back into three mechanistic parameters — `L_p ← f(R_m)`, `h = h₀[1 + (R_m,a/R_m,0)f_h]` with **f_h = −0.58**, and `B = B₀[1 + (R_m,a/R_m,0)f_B]` with **f_B = 11.4**. That asymmetry is the paper's most transferable insight: **fouling hurts salt rejection roughly an order of magnitude more than it hurts flux.** Hyperparameters: one LSTM layer of **30 units**, dropout 0.1, batch 32, 60 epochs, lookback 50 steps (25 h); inputs feed temperature, feed conductivity, feed calcium, concentrate flow, recovery and CIP occurrence. **CIP feature encoding is the reusable result** — of `AfterCleaning`, `Long/ShortCleaning` and `NumberCleaning`, the Long/Short split (>1 day vs ≤1 day of downtime) won. RMSE on `R_m,a`: **RNN-LSTM 7.65 vs ARIMAX 13.31 vs flux-based mechanistic 14.84**. Note also what the paper does *not* do: **it never proposes or evaluates CIP timing optimization, so citing it for a scheduling business case is a misattribution.** The reference **PINN** is Helali, Albalawi & Bel Hadj Ali (*Water* 17(3):297, 2025): SD equations in the loss with temperature-dependent permeability and progressive fouling embedded, trained on months of full-scale SWRO data, reaching **R² = 0.96 (permeate TDS) and 0.97 (Δp)** — and, the actual selling point, retaining physical plausibility during feedwater excursions and post-CIP recovery where pure regressors produced non-physical predictions. A **CCRO PINN** with two mode-specific networks, time-adaptive domain decomposition and coarse-model pretraining cut **training time 18 h → 8 h** (*Desalination* 2024). For UF, the **Hermia-PINN** embeds all four blocking laws with **adaptive sigmoid weighting** for smooth stage transitions and a probabilistic loss over data fidelity, physics and initial conditions, *learning* mechanism weights and transition times and proving **notably more robust under data-scarce conditions** (*Sep. Purif. Technol.* 2026) — the current best answer to "which mechanism is running right now"; its sample-efficient cousin has an **SVM predict the Hermia parameters** from initial flux, organic load and three EEM fluorescence bands at **R² 0.87–0.99** (*ACS ES&T Water* 2024), a deployable feature set given commercial online fluorescence probes.

**Uncertainty:** GP with Matérn-5/2, `σ²(x*) = k** − k*ᵀ(K + σ_n²I)⁻¹k*`; exact GPs cap near 10⁴ points, so use SVGP inducing points at SCADA scale. The cleanest published template is **physics mean function + GP on the residual + aleatoric sensor error propagated alongside epistemic GP variance** (arXiv:2512.10457, forward osmosis, directly transferable). Alternatives: MC-dropout, deep ensembles, TFT's quantile loss `Σ_q max(q·e, (q−1)e)`.

### 3.4 The reference full-scale forecaster

**MBR-Net** (*ES&T* 2025, https://pubs.acs.org/doi/10.1021/acs.est.4c12835) is the design to copy. It predicts **one-day-ahead change in irreversible fouling** — not raw TMP — with **MAPE < 6.45 %, MAE < 3.71 LMH·bar⁻¹, R² > 0.87 on two independent test sets**. Three design choices carry:

1. Target = irreversible fouling *rate*, the quantity chemical cleaning acts on.
2. Desired flux and cleaning conditions are model **inputs**, making it counterfactual and actionable rather than merely predictive.
3. An explicit denoising stage precedes training, acknowledging that plant sensor noise can dominate the fouling signal.

### 3.5 Fouling classification, integrity monitoring and prognostics

**Reversible vs irreversible** is the operationally useful binary, and the cycle structure supplies it free. The key paper trains an **ensemble BPNN optimized by an adaptive evolutionary algorithm** on **4 years** of integrated UF–RO seawater operation, modelling resistance during **both filtration and backwash**, with a **Bayesian binary classifier** deciding backwash success/failure (*Desalination* 2021). Modelling the backwash leg — not just filtration — is what makes it usable for scheduling.

**Fouling-type attribution (organic/bio/colloidal/scaling) from routine online SCADA has no published supervised classifier** — a genuine literature gap, not a search failure. The constructive route is a **weak-label pipeline**: derive labels from physics (per-cycle Hermia exponent, η_BW, differential response to acid vs oxidant CEB — citric/oxalic recovery implicates inorganic/metal-oxide fouling, NaOCl recovery implicates organic/biofouling) and train an online-feature classifier to reproduce them. That is synthesis, not a citable method.

**Integrity monitoring** is fully specified and deployable via **AD-PCA** (Grimm/Newhart/Hering, *ACS ES&T Engineering* 4(6):1492, 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11184555/) on the Calabasas Pure Water Demonstration Facility: 14 tags at 15-min averages over 13 months (monitored: filtrate turbidity, filtrate ammonia, temperature-corrected permeability; explanatory: feed turbidity, temperature, filtrate pH, ORP, total chlorine, conductivity, TOC, backwash flow, flux); *dynamic* = lag-augmentation at each variable's highest partial autocorrelation; *adaptive* = rolling window retrained every 96 in-control observations; detrending by **adaptive lasso** (beat kNN/RF/XGBoost — the forests overfit). Tuned optimum **12-day window, α = 0.005, 5 consecutive exceedances** → T² flagged **75.8 % of fault periods vs 25.9 % in-control** (SPE 7.3 % vs 1.4 %), beating Shewhart charts and daily pressure-decay tests. **The honest reading of 25.9 % is that MSPC is a prioritization signal for operator review, not a silent alarm.** Companion SB-MBR evidence: 44 tags at 1 min over ~479k observations detected permeate-salinity drift in **109 minutes with no false alarms**.

**Rare-event failure mode**: conventional CNN and LSTM **failed** on turbidity spikes from UF membrane damage (**R² < 0.2351**); the fix was coupling **wavelet-decomposed signals** with raw inputs (*J. Cleaner Production* 2023). MSE-trained sequence models smooth away fibre breaks and bloom onsets by construction.

**Prognostics on four sensors** (Khaled, Genga & Kaymak, arXiv:2602.00659, 2026): Port Hueneme SWRO pretreatment, **422 days / 12,528 cycles / 373 runs**. Health index `HI = 0.30(1−R_m*) + 0.25(1−TMP*) + 0.30J* + 0.15Rec*`; 20-cycle window → 3 Gaussian membership functions per feature → **120-dim fuzzy signature**; fuzzy Jaccard retrieval with top-k = 10 as zero-order TSK rules, `R̂UL = ΣS_i r_i/ΣS_i`. **RUL MAE ≈ 4.1–4.5 cycles** (file 03: 4.08, RMSE 6.28; file 08: 4.50), best at the 6–15-cycle horizon (MAE 3.67), but 80 % intervals achieved only **68.6 % coverage**. Mean cycle 121 s → ~40–60 min of usable warning, with a human-readable IF-THEN rule per prediction.

### 3.6 Coagulant dosing, blooms and imaging

**Coagulation is the highest-leverage UF fouling knob and the area with the most credible savings.** Four results define the space: (i) a **forward + inverse MLP pair** replacing the jar test — forward (turbidity, alkalinity, temperature, pH, dose → treated quality; 15 neurons) and inverse (raw quality + *desired* treated quality → dose; 16 neurons) on **112 points over 2 years**, alkalinity R² 0.94, pH 0.85, residual Al 0.93, returning a dose in <1 min vs ~30 min in the lab (*DWES* 11:1, 2018) — the inverse model is what lets you set a target and solve rather than imitate operators; (ii) **Conv1D + GRU on five years of minute-resolution data**, −22 % dose ≈ **21 M KRW/yr** at sedimentation turbidity <1.0 NTU (*Chemosphere* 2023); (iii) **GAMTF** graph-attention forecasting, **R² 0.94 / RMSE 3.55 vs baselines at 0.63–0.89**, with the domain's only official open-source codebase (https://github.com/cbhua/coagulant-forecast); (iv) **closed-loop cycle-to-cycle control** minimizing the incremental post-backwash resistance change by tracking `∂(ΔR_PB)/∂dose`, cutting dose **~29 %** on a pilot UF–RO seawater plant (*Desalination* 2016).

That last paper establishes the mechanism every dose model must respect: **higher dose promotes faster cake formation but improves backwash efficiency** — dose trades reversible fouling rate against irreversible accumulation, so the objective is *not* "minimize fouling rate". A non-ML pilot found PACl at **0.5 mg/L produced 65 % less irreversible fouling than 6 mg/L**: the fouling-optimal dose can be an order of magnitude below the turbidity-optimal dose. Enabling instruments: **UV254** (feedforward on NOM — NOM, not turbidity, drives irreversible fouling), **streaming current** (feedback on charge neutralization), online **fluorescence/EEM** (unlocks the Hermia+SVM hybrid). The RO train's *continuous* chemical levers — antiscalant, acid/pH and biocide — are the mirror image of this section and are treated in §2.10–2.11 and §4.7; note the asymmetry in evidence, since coagulant dosing has several credible ML controllers while **antiscalant dosing has none, and its best-proven controller is model-free**.

**Blooms.** Transparent exopolymer particles (TEP) are the primary irreversible UF foulant and the primary RO biofouling precursor; colloidal exceeds particulate, **in-line coagulation + MF/UF removes only 70–75 % of TEP**, and the residual passes to the RO. **Turbidity is nearly useless as a bloom-fouling predictor** — the informative features (chlorophyll-a, particulate and colloidal TEP, AOM/biopolymer by LC-OCD, UV254/SUVA, algal counts, SDI, MFI-UF) are nearly all offline, which is the gap hyperspectral soft sensors fill (CNN/RF predicting SDI/MFI/TOC/TEP/algae density, ~600 nm critical for chlorophyll; *Desalination* 2024, extended to UAV mapping in *Water Research* 2026).

**Imaging.** OCT + deep learning is mature — 13,708 OCT images → DNN+CNN at **R² = 0.99 for both fouling growth (RMSE 2.82 µm) and flux decline (RMSE 0.30 LMH)** (Park et al., *JMS* 2019) — while **planar camera images alone** give 90 % classification accuracy and biofilm thickness to ±24 % (*npj Clean Water* 2025), the realistic way to instrument a sacrificial canary module. **Membrane-autopsy SEM classification is the gap**: the technique is ready, the labelled corpus does not exist.

### 3.7 Data volumes, preprocessing and the discipline that separates real from fake

**Data-volume regimes observed across the corpus:**

| Regime | Scale | Appropriate models |
|---|---|---|
| Lab RSM/ANN | 16–88 points | RSM, tiny MLP (3-10-1, 4-9-1). Near-unity R² here is design smoothness, not skill |
| Small municipal | 100–200 daily records (Boujdour: 195, five inputs, SMOGN → ~2000, 39 real held-out) | SVR, RF, regularized linear |
| Pilot campaign | 10³–10⁴ (Lakner: 4500 raw → **104 independent**) | trees, GPs, per-cycle RF |
| Full SCADA | 10⁵–10⁶ (Carlsbad TCN, PINN SWRO, 5-yr minute-resolution coagulation) | LSTM/GRU/TCN/TFT, ConvLSTM |

**Rule of thumb: deep sequence models only beat trees/GPs above ~10⁴ effective samples spanning a full seasonal cycle and ≥2 CIP cycles.**

**Preprocessing pipeline, in order**: hard sensor-range and rate-of-change filters → **mode segmentation** (filtration/backwash/CEB/CIP/idle by valve state or flow threshold; one published system used 15 gpm on backwash flow) → per-cycle feature extraction → temperature correction / ASTM D4516 normalization → imputation (NAOMI for multiresolution gaps; for gappy historians, Moon, Jeong, Chae, Shim, Kim, Cho & Park, *Desalination* 603:118678, 2025, report **RMSE 0.375 on TMP and 0.218 on energy (LSTM), 0.173 on permeate flow (CNN-LSTM) explicitly under sensor-dropout conditions** on a 1,000 m³/d high-salinity SWRO plant) → ADF stationarity check and first-differencing → scaling fit on the training block only → **chronological blocked splits** → augmentation (SMOGN) only in small-data regimes and only on training folds.

**The model to beat before any deep forecaster is justified**: Lakner & Lakner's probabilistic linear baseline (*Membranes* 2025) — 4500 measurements over 75 days reduced to 104 independent samples, Arrhenius-compensated to 20 °C, giving **TMP growth 0.020 ± 0.002 bar/day**, expected fouling time to a 25 % TMP rise of **130 ± 15 days (95 % CI 100–160)**, and a closed-form cost-optimal cleaning interval `C_year/C₀ = (365/t_main)(1 + Φ(t_main)(C_foul/C₀ − 1))` giving 103–117 days. The consolidated failure-mode list is in §8.8; one calibration point belongs here — Tent-SSA-BP's reported 97.4 % accuracy came from a **spreadsheet simulation**, MBR-Net's MAPE <6.45 % from a plant, and only the latter is a planning number.

**Benchmarks to hold yourself to**: XGBoost R² > 0.98 (tabular RO KPIs); TFT R² 0.981 vs LSTM 0.936 (Δp); PINN R² 0.96/0.97 (TDS/Δp); GPR/ensemble R² 0.98–0.99 (UF soft sensors); GRU R² 0.890 (independent-plant TMP); MBR-Net MAPE <6.45 % (irreversible fouling); MTCN ρ 0.96–0.99, RMSE ≤0.023 normalized; UF RUL MAE ≤4.5 cycles.

---

## 4. Optimization

Formulations, solver notes and reported savings: [`research/04_optimization_algorithms.md`](research/04_optimization_algorithms.md).

### 4.1 Design-time: superstructure MINLP

Descends from El-Halwagi's 1992 state-space formulation (AIChE J 38:1185): four boxes — pressurization/depressurization stream distribution, pump/turbine matching, RO stream distribution, RO matching — whose combinatorics encode every split, mix, bypass and recycle. Canonical statement:

```
min_{y,x}  TAC = CRF·(Σ_i c_mod n_i + C_PV + C_pump(Ẇ) + C_ERD)
                 + c_e ∫SEC dV + C_chem + r_repl·C_memb

s.t.  element flux/balance equations (§2) for every candidate stage/pass
      interconnection balances with binaries y_jk ∈ {0,1}, big-M linking Q_jk ≤ M y_jk
      lead-element flux ≤ 30–35 LMH ;  element recovery ≤ ~15 %
      minimum concentrate flow per vessel ;  vessel Δp ≤ ~4 bar
      applied pressure ≤ 83 bar (SWRO elements)
      c_p ≤ c_p^max (e.g. 500 mg/L TDS) ;  c_B ≤ 0.5–1 mg/L boron
      ERD selection (PX vs Pelton) as discrete alternatives
      CRF = i(1+i)^n/((1+i)^n − 1) ;  r_repl ≈ 10–20 %/yr
```

Lineage: Voros et al. (1996) simplified to two-box networks; Lu et al. (2007) added membrane-type selection as discrete decisions; Saif, Elkamel & Pritzker (2008) achieved deterministic **global** optimization by branch-and-bound with convex relaxations; a 2019 extension enforces feasibility across seasonal scenarios (one design, multiple operating states).

Two design-space results worth hard-coding as priors: **split-partial second pass** — send low-TDS front-element permeate straight to product and treat only rear permeate in pass 2, for **≈7.0 % pumping energy** plus smaller pass-2 capital (DuPont/FilmTec); and **boron/high-pH single pass** — RO on decarbonated, high-pH seawater makes single-pass feasible and saves **0.41 kWh/m³** vs two-pass (*Comput. Chem. Eng.* 2022), because borate B(OH)₄⁻ is charged and larger than boric acid, making pass-2 pH (8.8–10.5) itself a design variable.

**Multi-objective**: NSGA-II is the reference (non-dominated sorting O(MN²), crowding distance, binary tournament, SBX + polynomial mutation, population 100–200 over 200–500 generations); the 2024 comprehensive superstructure MOO maps the Pareto surface over **recovery, specific water cost, SEC and CO₂** (*IECR* 2024). Deterministic alternative: lexicographic + augmented ε-constraint (AUGMECON), `min f₁ − δΣ_k s_k/r_k` s.t. `f_k + s_k = ε_k`, which yields only Pareto-efficient points and reaches nonconvex segments the weighted sum cannot.

**Rule of thumb**: deterministic MINLP (GAMS DICOPT/SBB/BARON, Pyomo+MindtPy) when the model is algebraic and you need feasibility guarantees; NSGA-II/PSO when the evaluator is a black-box simulator. **Always benchmark a metaheuristic against the deterministic solution of the same algebraic model — on smooth RO models, IPOPT from a good start typically matches NSGA-II's best point at 100–1000× less compute.**

### 4.2 Operation-time: real-time optimization of setpoints

The problem solved every 15–60 min as feed temperature/salinity and fouling drift:

```
min_{ΔP₁, ΔP₂, Y₁, Y}   SEC(ΔP_i, Y_i ; π₀(T,S), A(t), η_p(q), η_E)
s.t.  Q_p = Q_p^target
      c_p ≤ c_p^max
      ΔP ≥ π₀/(1−Y)                    ← thermodynamic restriction, MUST be explicit
      J_w ≤ J_w^max
```

The thermodynamic restriction is not optional: without it, optimizers exploit infeasible low-pressure corners. **Nor, on any plant pushing recovery, is the scaling constraint** — every recommendation this formulation can make is bounded by a saturation or biofouling limit, and §4.7 supplies the missing pieces (wall-referenced saturation, the induction-time constraint that legitimately relaxes `SI ≤ 1`, and the dose bound that keeps the relaxation honest). At an inland plant, add the disposal term of §4.8 to the objective before reading anything off this one.

**The best-documented plant-scale implementation** is the H2Oaks BWRO study (San Antonio; Membranes/PMC 2022, https://pmc.ncbi.nlm.nih.gov/articles/PMC8879670/): 3-stage plant, Dow FilmTec BW30-400/34, max recovery 90 %. ANN surrogates trained on **14,542 hourly SCADA records (Jan 2017 – mid 2018, 70/15/15)**: an ERD Δp model (1 input, one 3-node ReLU layer, **R² = 0.9983**) and a permeate-concentration model (5 inputs including the previous concentration, one 3-node ReLU layer, **R² = 0.895**); retentate pressure closed by linear correlations at R² > 0.99. The ReLU nets were **exactly reformulated as MILP** via big-M binaries and solved in CPLEX. Results: optimized annual RO energy 1,392.9 vs 1,516.9 actual (**≈8 % below actual pump consumption**), and a Pareto curve linearized as **SEC = 0.753·WR − 0.1326 (R² = 0.998)** — recovery 50 → 85 % costs **2.07× the energy**, which is exactly the trade an operator can schedule against. Note the accuracy lesson: **R² = 0.895 on permeate concentration was sufficient for energy RTO** — the accuracy budget should be set by the optimum's sensitivity, not by prediction benchmarks.

### 4.3 Tariff, storage and renewables

Seminal formulation: Ghobeity & Mitsos (2010), *Desalination* 263:76–88 — an MINLP minimizing daily electricity cost for fixed daily production with PX ERDs, VFD part-load curves, CP, temperature and fouling. The standard scheduling MILP:

```
min Σ_t (p_t^buy E_t^grid − p_t^sell E_t^exp)
s.t. V_{t+1} = V_t + Δt Σ_i q_{i,t} − D_t          (product storage = the flexibility battery)
     V^min ≤ V_t ≤ V^max
     q_{i,t} ∈ {0} ∪ [q_i^min, q_i^max]·u_{i,t}     (semicontinuous trains)
     ramp / min-up / min-down on u_{i,t}
```

Reported results: rescheduling **~60 % of daily load** into a 23:00–06:00 off-peak window; variable operation plus time-varying conveyance raising **PV share of load to 72 %**; and renewable-colocated dispatch (50 MW PV at Najran, α_r = 166.67 m³/MWh, net metering $270/MWh import and $100/MWh export) earning **$119,180/day vs $112,850 (passive-thermal benchmark) and $99,872 (max-RO heuristic)** — a 5.6–19 % profit improvement that reduces to a **four-threshold policy computable offline** (arXiv 2026, https://arxiv.org/pdf/2601.02243).

**The binding caveat**: a Southern California brackish case study finds tariff savings materialize **only** with aggressive tariffs and a facility *designed* for flexibility (oversized/parallel positive-displacement pumps, storage). **Flexibility is a design-time decision consumed at operation time** — do not build the tariff MILP for a plant that cannot turn down.

### 4.4 Cleaning and maintenance as optimization

**Industry baseline any optimizer must beat**: trigger CIP at 10 % normalized-flux decline, 5–10 % salt-passage increase, or 15 % differential-pressure rise vs commissioning, computed on ASTM-normalized data. The *deployed* industrial baseline is slightly more sophisticated and is worth reproducing verbatim as your control arm — Ecolab USA (Dörries, Hicks & Krack), **US20250296050A1**, "Membrane monitoring and clean-in-place control" (filed 21 Mar 2025, published 25 Sep 2025, https://patents.google.com/patent/US20250296050A1/en): fit a first- or higher-order polynomial trend to time-, area- and pressure-normalized flux `F/(t·A·p)` across production cycles, extrapolate to the predicted capacity-loss date, schedule the deep clean at that date **minus a 1–6 week safety margin**, declare a cleaning ineffective when it fails to restore the trend slope by **5–25 %**, establish the trend over **2 weeks to 4 months** post-installation, and exclude CIP and idle phases from the fit. No savings are quantified in the patent — but **an RL policy that cannot beat a polynomial trend plus a 1–6 week margin is not deployable.**

**Renewal-reward formulation**:

```
min_θ  [ C_CIP + ∫₀^{T(θ)} c_e·SEC(t)·Q_p(t) dt + C_repl·1[irreversible] ] / ∫₀^{T(θ)} Q_p(t) dt
```

with `T(θ)` the run length to the trigger and `A(t)` from a forecast model. The strongest published result raised the CIP pressure threshold (cleaning later but at higher-value moments, with chemical and replacement costs in the reward) and performed **CIP twice at the highest threshold studied: −16.13 % operating cost, +139.53 % operating time** vs the incumbent policy (Shim, Lee, Park, Moon, Lee & Cho, *Desalination* **614:119193**, 2025, DOI 10.1016/j.desal.2025.119193).

**Read that result correctly** — the verification pass ([`research/09_gap_2.md`](research/09_gap_2.md) §1) confirms both figures verbatim from the author-written abstract and confirms the surrogate accuracies (**attention-based LSTF R² = 0.82 vs 1D-CNN+LSTM R² = 0.65**), but adds three constraints on how they may be used. (i) The plant is an **industrial ultrapure-water RO pre-treatment train**, and the conclusion that higher thresholds win is driven entirely by the ratio of chemical + membrane-replacement cost to energy cost — **it will invert at a plant with cheap chemicals and expensive energy**, so re-derive it from your own purchase records. (ii) These are **RL-policy objective values evaluated inside a learned forecasting environment**, not a measured before/after; two decimal places are a floating-point artifact and should be rounded before entering a business case. (iii) **+139.53 % run time is the mechanism, not the benefit** — raising the trigger lengthens each run almost definitionally; the genuine claim is that the *cost* of that deferral (faster terminal fouling, more energy, some irreversible permeability loss) is outweighed by avoided chemical and replacement spend, netting −16.1 %.

**Do the threshold sweep before the RL.** Enumerate CIP trigger thresholds `ΔP*` on a grid, roll the forecaster forward under each, count CIP events, and evaluate `C_total = c_E Σ SEC_t Q_p,t Δt + n_CIP·c_CIP + c_mem/L({a}) + c_lost Σ_{t∈CIP} Q_p Δt` where `L({a})` is membrane life as a function of the cleaning policy. That is cheap, auditable, produces the %opex-versus-threshold curve directly, and is what the published result actually amounts to; RL is the second step, not the first.

**The correct UF analogue for a business case is not Shim but Park et al.** (Park, Shim, Yoon, Lee, Kwak, Lee, Kim, Son & Cho, *Chemosphere* 308:136364, 2022, DOI 10.1016/j.chemosphere.2022.136364): an LSTM surrogate of a UF system as the DRL environment, the agent controlling **operating pressure, cleaning time and cleaning concentration**, delivering **SEC −20.9 %**, mean flux **39.5 → 43.7 LMH** and operating pressure **0.617 → 0.540 bar**.

**UF backwash** — decision variables are interval (or TMP trigger), duration, flux and CEB frequency, maximizing `V_net = (∫₀^{t_f} J dt − J_bw t_b)/(t_f + t_b)`. Three approaches, in increasing sophistication:

1. **Response surface / direct search at engineering scale** (OSTI/DOE 2023, https://www.osti.gov/pages/biblio/2329273). Backwash **durations of 45/65/85 s performed identically** (~63 m³/day, ~91 % recovery) — duration is a weak lever; sweeping the **TMP trigger 62–145 kPa found a clear optimum at 103 kPa** (63 m³/day, ~92 % recovery) — the trigger is the strong lever. Reducing scheduled CEB frequency from 1-in-3 to 1-in-6 or 1-in-12 **decreased recovery**, and **total CEB count stayed approximately constant regardless of scheduled frequency** — encode that as a hard constraint or your RL agent will "save" chemicals the membrane then demands anyway. A seawater RSM study (interval 30–90 min, flow 10–34 L/min, duration 15–45 s) likewise found fouling controlled primarily by interval, with season-dependent optima ~65 min dry / 55 min wet.
2. **Learn-a-model-then-optimize** — the canonical architecture (Zhang, Kotsalis, Khan, Xiong, Igou, Lan & Chen, Georgia Tech, *JMS* 612, 2020): ML (LR vs ANN vs RF, compared head-to-head) learns backwash foulant-removal efficiency and foulant accumulation rate; that learned map becomes the transition function for **stochastic dynamic programming** over backwash timing, beating fixed-interval operation on cost *and* terminal membrane resistance.
3. **Pontryagin optimal control with online re-identification** — the strongest quantified energy result in the UF literature (Membranes/PMC 2025). Cake-deposition model with attachment `ṁ = δQ_out(C_Xi X_i + C_Si S_i)` and exponential detachment during backwash; PMP yields a **singular control giving an optimal fouling mass m̄** and the corresponding filtration/backwash duration ratio, recomputed each cycle from real-time parameter identification. Experimentally validated: **4–9 % on hollow-fibre MF, 28–31 % on flat-sheet UF, 7–30 % overall**.

**Membrane replacement** is thinly treated as a formal stopping problem — most work folds it into annualized cost or an RL reward. The exception: van Rooij, Scarf & Do (2021, *Desalination*, DOI 10.1016/j.desal.2021.115214) model Carlsbad's vessels as **multi-component systems with per-element wear states**, comparing swap/rotation policies on risk, cost, downtime and stoppage count. Industry practice remains 3–5 year element life, condition-based rather than calendar-based.

### 4.5 Batch and closed-circuit RO

Continuous RO must apply exit-brine pressure to the **entire** feed; batch ramps pressure with instantaneous concentration, approaching `SEC_ideal = −π₀ln(1−Y)/Y`. Warsinger et al. (MIT, 2016) model **up to 37 % (CCRO, semi-batch) and 64 % (true batch)** savings vs continuous single-stage RO — the CCRO gap is the entropy of mixing recirculated brine with fresh feed, which you must model or you will overestimate savings by the difference between the two bounds. Commercial CCRO (Desalitech → DuPont) reaches **90–98 % recovery** with CIP cut from ~monthly to ~6-monthly; OCWD's potable-reuse pilot lifted recovery **85 % → 92 %** over two years. Two optimization layers have been demonstrated on CCRO hardware: **MPC** minimizing integrated SEC (§5.3), and model-free **extremum-seeking control** perturbing the upper conductivity limit that terminates each closed-circuit phase (dither 0.15 mS/cm over a 5-cycle period, high-pass filter to isolate the gradient, `J = SEC + α·SBV`) for a **6.5–6.8 % cost-metric improvement** in 70 cycles (~35 h) after an economics change and 150 cycles (~85 h) after a +50 % salinity step, using only flow/pressure/conductivity/power sensors — the cleanest published template for "RTO without a model", whose tens-of-hours convergence is exactly why it cannot handle fast disturbances.

### 4.6 Surrogate-based optimization: four production patterns

1. **Exact MILP embedding of ReLU networks.** Each neuron `y = max(0, wᵀx + b)` becomes `y − s = wᵀx + b`, `y ≤ Mz`, `s ≤ M(1−z)`, `y,s ≥ 0`, `z ∈ {0,1}`. H2Oaks did this by hand in CPLEX; **OMLT** (Ceccon et al., JMLR 23, 2022, https://github.com/cog-imperial/OMLT) auto-translates Keras/ONNX networks and GBTs into Pyomo blocks with selectable big-M / complementarity / partition formulations (248/308/428 constraints for one example net). **Tighten big-M by per-neuron interval arithmetic or solve times explode.**
2. **Kriging/GP Bayesian optimization** with `EI = (μ − f*)Φ(z) + σφ(z)`, `z = (μ − f*)/σ` — when each evaluation is an experiment or an expensive simulation.
3. **Trust-region filter methods** (IDAES TRF) embedding black-box units in an equation-oriented flowsheet, rebuilding local surrogates each iteration with convergence safeguards — the rigorous route without losing feasibility guarantees.
4. **Aggressively linearized physics surrogates** — H2Oaks again: linear P_r–P_f correlations and a linear SEC objective sufficed.

**The dominant failure mode of ML-in-the-loop RTO is surrogate extrapolation outside the training hull.** Add explicit box constraints on surrogate inputs and retrain on drift — fouling shifts the input distribution over months.

### 4.7 Continuous chemical dosing: antiscalant, acid and biocide as decision variables

Formulations, parameter values and field results: [`research/09_gap_1.md`](research/09_gap_1.md).

§4.2's RTO optimizes pressure and recovery against energy. It is bounded by a scaling or biofouling constraint that this report previously never wrote down, and it ignores three continuous chemical levers with their own economics.

**The dose search that needs no model and no ML.** The state of practice is a 3–10× overdose, and the fix is an extremum-seeking step-down on a *normalized* signal, not raw pressure. Monitoring equations (Hydranautics practice + ASTM D4516-00): `K_w = Q_p/(NDP·A_M)·1/TCF_t`, `TCF = exp[2700(1/298 − 1/(273+T))]`, `NDP = P_f − ΔP_fc/2 − P_p − π_fc + π_p`, `NDP_T = NDP × TCF`. Procedure: start at the supplier dose; step **down** on a fixed schedule watching `d(NDP_T)/dt` of the **last stage** (better: the last element, or an external scale-guard) — Kamerik used 9 steps of 0.2 mg/L at 12 h dwell, Brabrand 0.5 mg/L steps at 24 h dwell; the dose at which `ΔNDP/Δt` turns positive is the **underdose**, the lowest dose holding `NDP_T` flat is the **optimum**; step back up and hold on any detected rise. Encode the vocabulary the thesis is careful about: *underdose < optimum ≤ safe dose < overdose*.

**Why the loop is safe** — the non-obvious part, verified three ways at LSI 2.0–2.2: in jar tests, no-antiscalant induction time was ~15 min, 2.0 mg/L extended it to >1 week, and adding 2.0 mg/L *after* a 0.1-unit pH drop **halted** further decline for >1 week even with seed crystals present; in a lab RO cell, restoring 2.0 mg/L after a **27 % permeability drop** stopped further decline; on the pilot, NDP rose immediately at 0 mg/L in three separate windows and the rise ceased each time dose was restored. **Underdose-induced scaling is arrestable, which is what makes a descending search legitimate** — but set a conservative stop-loss (abort and restore at >5 % normalized permeability loss) since the 27 % evidence is a single system.

**Overdose is a failure mode, not just a cost.** At 5.0 mg/L feed dose (33.3 mg/L in concentrate, 765 mg/L Ca²⁺) permeability fell *faster than at 0.2 mg/L*; SEM showed an amorphous film rather than calcite cubes, and ESI-TOF/ICP-MS identified **calcium phosphonate**. The Danish pilot reproduced it at 6.0 mg/L. **Bound the dose from above**, `C_a ≤ C_a^overdose(Ca²⁺_conc)`.

**Two known weaknesses to fix in your implementation.** The published decision tree ratchets up and never re-tries downward, so one transient upset permanently inflates the setpoint (the Danish unit jumped to 6.0 mg/L on a disturbance and settled at 1.2 where 0.6 sufficed). Add (a) a **CUSUM disturbance gate** on the `NDP_T` residual against a fouling-free model, gated on stable feed T/conductivity/flux, before accepting any increase; (b) a **scheduled re-descent** with finer 0.1–0.2 mg/L steps after a stable period; and (c) run the search on an **external scale-guard** — an extra element fed with last-stage concentrate so it scales first — so no experiment ever risks the production train.

**Closing the delivered-dose loop.** NDP feedback tells you whether the dose is sufficient, not what was actually delivered (pump slip, dilution, degradation). Fluorescent-tagged antiscalants close it: dose the tagged product at a fixed ratio, measure fluorescence inline on feed and concentrate, and you get delivered-dose verification, an independent recovery estimate from the concentrate/feed ratio, and an early flag when inhibitor is being consumed by the deposit. Ecolab/Nalco's **3D TRASAR for membranes** is the commercial instance but publishes neither tracer chemistry nor quantified savings; the open-literature counterpart is Popov's naphthalimide-tagged aminophosphonate **ADMP-F** at **80–100 % scale-inhibition efficacy at 1–3 mg/L** (*IJMS* 24:3087, 2023).

**Putting scaling inside the NLP.** Two published routes, both equation-oriented and both in WaterTAP:

1. **PySMO RBF surrogates on OLI equilibrium sweeps** (Amusat, Dudchenko, Atia & Bartholomew, FOCAPD 2024), minimizing LCOW over (Na₂CO₃ dose, acid dose, recovery, RO pressure) subject to `ŜT_s(d) ≤ 1` for CaSO₄, CaCO₃ and gypsum, solved with **IPOPT + HSL MA27**. Accuracy: softening pH and CaCO₃ **R² ≈ 1.00**, post-acidification pH R² = 0.99 on 100 training points, scaling-tendency surrogates **>99.2 % classification accuracy** — and *classification accuracy at ST = 1 is the right metric*, since the optimizer only needs the feasible/infeasible boundary, not a regression score.
2. **Implicit-function / external grey-box models via Reaktoro-PSE** (Akkor, Amusat, Vecchiarelli, Gounaris, Knueven & Dudchenko, *ACS ES&T Eng.* 2026, https://github.com/watertap-org/reaktoro-pse), where Reaktoro solves equilibrium externally and returns outputs **and their derivatives** to Pyomo. This eliminates the surrogate-retraining burden — the prior neural-network route needed **~2 million PHREEQC samples** — and lets you add chemicals without regenerating data.

**Four results from those studies that belong in any plant model:**

- **Acid choice is not a unit-price decision.** H₂SO₄ adds sulfate, which drives gypsum and forces **2–41 % additional calcium removal** in softening; HCl wins on total cost over the 66–76 % recovery band and loses again above 76 %. CO₂ is the most expensive acid in both waters (**up to 49 % costlier than H₂SO₄** for brackish, 11.5 % for seawater) because it needs >3× the dose and forces a lower target pH. Brackish acid demand is **4–6× seawater** (7–10× for CO₂) from bicarbonate buffering. Safety inverts the cost ranking: HCl needs the largest on-site storage, CO₂ is safest.
- **The optimizer's cheapest scaling lever is often hydraulics, not chemistry.** Reaktoro-PSE finds a four-regime structure, and **Regime 2 is the one this report was missing**: over a band of recoveries (74–75 % SW, 56–64 % USBR brackish) the optimizer *lowers average permeate flux and raises crossflow velocity* to cut concentration polarization and hence wall gypsum SI — acid dose actually **falls**. **Flux and crossflow are scaling-control variables, not just energy variables.** Regime 1 is acid-only (to 74 % SW / 56–59 % brackish), Regime 3 lime-only over a narrow band, Regime 4 soda-ash-dominated; a hard water (1501 mg CaCO₃/L) sits in Regime 4 at *all* recoveries.
- **Antiscalant enters this framework by relaxing the right-hand side above 1.0** — stated explicitly by the FOCAPD authors. That single line is the bridge from §2.10: **the kinetic model tells you how far above 1.0 you may go for a given dose and residence time.**
- **Softening is expensive enough to make the antiscalant lever obvious**: chemical softening runs **LCOW $0.96/m³ at 6.3 kWh/m³** on Kay Bailey Hutchison BWRO brine, and where non-carbonate hardness dominates, **85–95 % of its operating cost is chemicals**. Buying kinetic headroom with a few tenths of a mg/L of antiscalant beats buying it with soda ash.

**The coupled RTO layer.** Decisions `d = (Y, J_w, u, pH, C_a, shock schedule)`:

```
min_d   c_e·SEC(Y,J_w)·Q_p  +  c_AS·C_a·Q_f  +  c_acid·ṁ_acid(pH)  +  c_bio·ṁ_bio
        +  (C_CIP + C_repl)/T_run

s.t. 1)  S_a,s^wall(Y, J_w, u, pH) ≤ S_s^max          thermodynamic screen (Reaktoro/OLI/PHREEQC or RBF surrogate)
     2)  t_A(S_a,s^wall, C_a) ≥ λ·τ_res(Y,u)          the kinetic constraint — what *permits* S^max > 1
     3)  C_a^min ≤ C_a ≤ C_a^overdose(Ca²⁺_conc)      the U-shape
     4)  T_run ≤ 1/BFI(AOC, u, T, biocide)            biofouling-limited run length from the MFS
     5)  ∫C_Cl₂ dt ≤ 1000 ppm·h over element life ;   continuous free chlorine < 0.1 ppm
     6)  ΔP ≥ π₀/(1−Y) ;  crossflow ≤ 25 cm/s ;  ≤85 bar per BWRO element
```

**Constraint 2 is the piece that was missing.** Without it an optimizer either treats `SI ≤ 1` as hard — leaving 5–20 points of recovery unclaimed, since real plants run concentrate LSI +1.8 to +2.5 — or relaxes it with an arbitrary constant credit and eventually scales the tail.

**Where ML actually fits here.** Be honest: there is **no published ML antiscalant-dose controller**. What is proven is (1) model-free feedback search, (2) ML/RBF surrogates of the thermodynamics inside the optimizer, and (3) — the genuinely open, publishable slot — **a learned residual on the kinetics**, fitting `t_0A`/`k_s` from the plant's own scale-guard history so the induction model tracks feedwater drift.

### 4.8 Brine disposal economics and the disposal-cost-aware recovery optimum

Cost models, worked examples and the MLD/ZLD landscape: [`research/09_gap_3.md`](research/09_gap_3.md).

Desalination produces ~141.5 million m³/day of brine — about 50 % more brine than product water. For a coastal SWRO plant the marginal cost of an outfall is a few cents per m³ and recovery is genuinely an energy/capital trade. **Inland, it is not.** The Texas Water Development Board's survey of nine real plants contains an accidental controlled experiment: **City of Roscoe** (0.432 MGD, 3,800 mg/L feed, surface-water concentrate discharge) produces water at **$0.39/m³**, while **Fort Hancock WCID** (0.4 MGD, *easier* 1,600–2,400 mg/L feed, but forced onto evaporation ponds) lands at **$0.86/m³** — same size, same era, and the disposal route alone **more than doubles both unit capital and total production cost**. Across 96 U.S. municipal desalting plants (Mickley/USBR Report 123): surface discharge 41 %, sewer 31 %, deep-well injection 17 %, evaporation pond 2 %, land application 2 % — and the two cheap routes covering 72 % of plants are exactly the ones now capacity- or permit-limited for new inland capacity, which is why the MLD/ZLD market exists.

**Marginal disposal cost is piecewise, and each piece behaves differently in an optimizer:**

| Route | $/m³ brine | Cost structure the optimizer must respect |
|---|---|---|
| Surface / ocean outfall | 0.05–0.30 | NPDES/WET permits, plume limits; effectively capped, not priced |
| Sewer (with surcharge) | 0.32–0.66 | POTW TDS/flow caps; surcharge escalation risk |
| Deep-well injection | 0.54–2.65 | **Step-fixed**: `C_cap = −288,000 + 145,900·d_tube[in] + 754·depth[ft]` (USBR 35-case regression; 16", 3,400 ft → **$4.61 M** in 2001$, ×1.7–1.9 for today). Diameter matters surprisingly little. Amortized at CRF 0.094 the *same well* costs **$0.31/m³ at 1 MGD and >$3/m³ at 0.1 MGD** — model it as binary well-count × capital, never as $/m³, or the optimizer will fractionally build wells |
| Land application | 0.74–1.95 | Blending to irrigation salinity; land-intensive; small flows |
| Evaporation pond | 3.28–10.04 | **Linear in volume, no economy of scale**; `$/acre = 5406 + 465·t_liner[mil] + 1.07·C_land + 0.931·C_clear + 217.5·h_dike[ft]`, `A_tot = 1.2·A_evap(1 + 0.155 h_dike/√A_evap)`; area is hyperbolic in recovery (`A ∝ (1−Y)/Y`), so **report pond-acres-saved per recovery point** to make the business case legible |
| Thermal ZLD | ~$3/m³ in 2001$ ≈ **$5–5.5/m³ today** | Brine concentrator **20–25 kWh/m³** (~$1,400 per m³/d installed), crystallizer **52–66 kWh/m³** (~$14,000 per m³/d — 10× the BC per unit flow). `C_annual = −2,722,800 + 4,035,700·Q[MGD] + 37,720·reject[%] + 28,591,000·c_e` |

**The objective, and the closed form worth memorizing.** Per m³ of product, with feed-referred cost `c_f` and disposal price `c_dis`:

```
LCOW(Y, ΔP, …) = CRF·C_cap(Y,ΔP)/V_p  +  c_e·SEC(Y,ΔP)  +  c_dis·(1−Y)/Y  +  c_f/Y
```

At the thermodynamic limit with an ideal ERD (`SEC = π₀/(1−Y)`), `∂LCOW/∂Y = 0` gives

```
Y* ≈ 1 − √( c_e·π₀ / (c_dis + c_f) )
```

Two plug-ins reproduce industry behaviour from first principles. **Inland BWRO** (2 g/L feed, π₀ ≈ 1.5 bar, $0.07/kWh, DWI at `c_dis + c_f` = $2/m³): `Y* ≈ 96 %` — the energy term is *three orders of magnitude* too small to stop you, and the true stop is gypsum/silica saturation (at Y = 0.96 the brine is 25× concentrated, π_b ≈ 39 bar). **Coastal SWRO** (π₀ ≈ 27 bar, outfall at ≈$0.15/m³): `Y* ≈ 41 %` — the observed 40–50 % SWRO recovery falls straight out of the same formula. **For inland BWRO the recovery optimum is disposal- and scaling-limited, never SEC-limited.**

**Treat-versus-dispose is the master decision.** Let the plant buy down brine volume with a concentration technology `t` (UHP-RO, LSRRO, OARO, CFRO, MVC): `min_chain Σ_t LCOW_t·V_t + c_dis·V_b,final − p_w·V_w,recovered`, i.e. **concentrate further only while marginal concentration cost < (avoided disposal + water value)**. The chain optimum for most inland MLD projects lands at primary RO → softening → UHP-RO/LSRRO to 120–250 g/L → a small pond or crystallizer for the residue, because the membrane segment's $0.7–7/m³ undercuts thermal's $5+/m³ up to ~125 g/L feed.

**LSRRO/OARO — the implementable reference formulation** is Atia, Allen, Young, Knueven & Bartholomew, *Desalination* 551:116407 (2023), full text at https://www.osti.gov/pages/servlets/purl/1958140. LSRRO is one conventional RO stage followed by n−1 low-salt-rejection stages whose saline permeate is recycled to the previous stage's inlet; deliberate salt passage keeps transmembrane Δπ low enough to run at ≤65 bar on (potentially) commercial NF or oxidant-treated modules. The model is an **NLP in WaterTAP minimizing LCOW, IPOPT + MA27**, stage count as a discrete outer loop, with the novelty being **per-stage optimization of the salt permeability B**. Cost-optimal results at 1 kg/s feed: 35 g/L @ 70 % → 2 stages, SEC **3.93 kWh/m³**, LCOW **$0.70/m³**; 70 g/L @ 55 % → 3 stages, 8.38 kWh/m³, **$1.89/m³**; 125 g/L @ 35 % → 4 stages, 30.39 kWh/m³, **$7.41/m³**. Forcing a *single* B across LSR stages — as all prior work did — raises LCOW by 1.1–5.1 % in the base cases and **28 % for a 70 g/L / 75 % recovery case** (membrane area ×2.3): per-stage selectivity optimization is the difference between viable and not. The full 131k-solve application map (feed 5–220 g/L, recovery 30–90 %, 1–8 stages) spans LCOW **$0.32–41.5/m³** and SEC **1.1–171.2 kWh/m³**, with single-stage RO still cost-optimal to 65 g/L at 30 % recovery. **Pressure rating beats membrane price**: raising RO max pressure 85 → 125 bar cuts LCOW 10–44 % and drops stage counts, while today's 40-bar low-rejection modules add ~54 %; doubling LSR membrane price only adds 2–19 %. Versus alternatives, LSRRO beats MVC decisively at moderate salinity (68 g/L @ 75 %: **$3.8 vs $10.3/m³**), splits with OARO (OARO cheaper at low recovery and ≥125 g/L; LSRRO cheaper at higher recovery/lower salinity), and loses to evaporative above ~125 g/L. OARO's own cost anchor is **$1.7–8.8/m³** at 75–150 g/L, 30–50 % recovery (Bartholomew, Siefert & Mauter, *ES&T* 52:11813, 2018). **Caveats the authors flag and you must carry: pure NaCl with no scaling model, no LSRRO pilot exists, and permeate spec 1,000 ppm (tightening to 500 adds 2–13 %).**

Both flowsheets ship in WaterTAP (`watertap/flowsheets/lsrro`, `.../oaro`), and the **zero-order `deep_well_injection` unit closes the disposal term inside the same Pyomo model** — so a single NLP can carry membranes plus disposal and find the §4.8 optimum directly rather than post-hoc.

---

## 5. Advanced control, reinforcement learning and fault detection

Full formulations, parameter values and deployment-status flags: [`research/05_control_mpc_rl.md`](research/05_control_mpc_rl.md).

### 5.1 The three-layer hierarchy you must slot into

- **L0 — drive/regulatory (ms–s)**: VFD speed loops on HP/booster/recirculation pumps, concentrate-valve positioners, PLC interlocks. Universally PI/PID at 0.1–1 s.
- **L1 — unit regulatory (s–min)**: feed flow, feed pressure, permeate flow, crossflow velocity, recovery — classically 2–3 SISO PI loops. Historical baseline: Alatiqi, Ghabris & Ebrahim (1989, *Desalination* 75:119) step-test ID → Robertson et al. (1996) DMC → Assef et al. (1997) constrained MPC → Burden et al. (2001) CMPC on a Permasep pilot, where PI could not hold product quality while manipulating pH.
- **L2 — supervisory/economic (min–h)**: recovery split, SEC minimization, CIP scheduling, cycle sequencing, load shifting. **This is where MPC, EMPC, ESC and RL actually live — almost always as setpoint generators for the L1 PI loops, not as direct actuator controllers.**

MVs: HP pump VFD speed (or feed-flow setpoint), concentrate throttle, interstage booster, PX booster flow, PX valve-to-drain, recirculation speed, three-way filtration/drain valve, antiscalant and coagulant dose, backwash/CIP timing. CVs: system pressure, flux, recovery, crossflow velocity, permeate and concentrate conductivity, TMP, SEC.

### 5.2 How much model-based control beats PID — measured

On the UCLA WaTeR Center rig (0.1 s sampling, valve full-stroke ~45 s), for a 1.5 → 3 gpm retentate setpoint step at 5400 ppm NaCl: a **P controller left ~20 % steady offset with sustained limit cycles**, while a **feedback-linearizing nonlinear controller settled at ~3–4 % offset** (Bartman, Christofides & Cohen, *IECR* 48:6126, 2009). The mechanism is loop interaction — opening the valve drops pressure, the pressure loop raises feed flow, retentate flow rises again — and the limit cycle propagates into pump speed and shortens pump life. This is the cleanest published justification for model-based control at the RO regulatory layer.

For disturbance rejection at 91 % recovery under a 24 h feed-concentration disturbance, **two PI loops failed outright**; Lyapunov bounded feedback only marginally damped the oscillation; only **feedback plus model-based feed-forward on measured C_f** rejected it (McFall et al., *IECR* 47:6698, 2008). Their framing is worth internalizing: for RO, feedback is not needed for *stability* (the plant is open-loop stable and fast) — it is needed for **performance, constraint keeping and fault tolerance**.

Control-oriented model, UCLA lumped form (fitted ρ = 1007 kg/m³, V = 0.6 m³, A_p = 1.27×10⁻⁴ m², A_m = 15.6 m², K_m = 9.7×10⁻⁹ s/m):

```
0   = (A_p²)/(A_m K_m V)(v_f − v_r) + (A_p/ρV)Δπ − (A_p e_vr v_r²)/(2V)
Δπ  = f_os·C_feed·ln(1/(1−Y))/Y        f_os = 78.7 Pa/(mg/L)
P_sys = (ρA_p)/(A_m K_m)(v_f − v_r) + Δπ
```

The `ln(1/(1−Y))/Y` log-mean osmotic factor is the dominant nonlinearity. **Valve resistance is not linear in stem position** — UCLA fit `e_vr = α ln(O_p) + β` piecewise over five position bands and call capturing this "extremely crucial" for transferring simulated controllers to hardware. Other control-oriented model families: **NARMAX/grey-box** three-equation discrete models re-estimated per cycle by least squares (median-filtered at W = 21, 1 s sampling) for CCRO; **LSTM** sequence models mapping `[x(k); u(k..k+T−1)] → x(k+1..k+T)`; **Koopman** lifted-linear models; and **subspace identification (N4SID/MOESP)** — block-Hankel matrices, oblique projection `O_i = Y_f /_{U_f} W_p`, SVD truncation to order n, then `(A,B,C,D)` by least squares — the pragmatic route to a MIMO linear model from step/PRBS tests, though **no membrane-specific N4SID result exists in the literature**.

### 5.3 MPC and economic MPC — the fully specified cases

**Field-validated supervisory SEC optimization** (Gao, Jarma, Christofides & Cohen, *Water* 17:2363, 2025): two-stage brackish plant (14× Toray TM710D + 7× TM810V, ~98 m³/day at 75 % recovery, agricultural drainage at 11,000–19,000 mg/L). The supervisory layer estimates permeabilities online then SQP-minimizes `SEC(Y, Y₁)` subject to pressure/flux/crossflow/recovery bounds; three PI loops execute; supervisory updates every ~300 s. The analytic optimum is

```
Y₁,opt = 1 − √( R₁·η₂ / (R_T·η₁·(1−Y)) )
```

— **the optimal recovery split is set by relative pump efficiencies, not membrane properties.** Field results: **4.2 % SEC reduction** at fixed 74 % recovery (Y₁ 52 → 60 %), **7.1 %** with Y and Y₁ optimized jointly (Y 74 → 58 %), **~10 %** vs flux-equality operation across a 24,190 → 17,833 mg/L salinity transition. Loop convergence 150/280/430 s; pump-efficiency maps fitted as 2-D Gaussians (R² = 0.98).

**Real-time SEC minimization on hardware** (Bartman et al., *J. Process Control* 2010):

```
min_{v_f, e_vr}  SEC = ρ e_vr (v_f − v_p)² v_f / (2 v_p)
s.t. v_p = v_p^set ;  v_f, e_vr > 0 ;  P_sys ≥ π₀/(1−Y)
     0 = P_sys/ρ − ½ e_vr (v_f − v_p)²
```

solved by SQP in MATLAB, exchanging data with the plant HMI over UDP every ~10 s (1–5 s per solve), 19-point moving average on sensors. Experiments at 1600/1850/3500 ppm landed on the theoretical SEC-vs-recovery curve. **Two caveats the authors report**: the optimum sat where hardware limits blocked higher recovery, and salt rejection is *not* constant — permeate TDS exceeded the 500 ppm drinking-water limit at the highest recovery on 3500 ppm feed. **Add a rejection constraint for any potable application.**

**CCRO MPC, fully specified** (Chowdhury et al., IWA *Water Supply* 25(4):727–748, 2025):

```
min_{f_F(1..M), f_R(1..M)}  iSEC = Σ(P_F + P_R) / Σ f_F
s.t.  grey-box model, recalibrated each cycle
      44 ≤ f_R ≤ 55 L/min      (recirc pump safety)
      1  ≤ f_F ≤ 3  L/min      (feed pump / membrane safety)
      c_R(k) ≤ 25 mS/cm
      setpoints change every 120 samples (2 min);  M = 90 moves over 2.5 h
```

Solved with IPOPT (cyipopt), LabVIEW running the 1 s PI/VFD layer. Per-cycle recalibration kept iSEC forecasts **within 1 %** of measured, versus a static model biased **1.5–3.5 % low** after an unmeasured salinity change that it never recovered from; realized filtration length stayed within **12 min of the 180 min target**. The optimal policy is structurally simple and interpretable: **recirculation at its lower bound throughout, feed flow at its upper bound early and lower bound late** — because pump power rises with concentrate conductivity, so make water while the loop is still dilute.

**The identifiability trap — the most transferable practical lesson in this literature.** When the CCRO optimizer converged onto flat, near-constant setpoints, the next cycle's parameter estimates **diverged within two cycles** and forecasts became badly wrong. The fix was deliberate dither: `u_perturbed = u* + a·w`, `w ~ N(0,1)`, plus randomizing the first 2 minutes of every filtration phase. **Any adaptive MPC on a process that never reaches steady state must budget for persistent excitation explicitly.**

**LSTM-MPC successor** (Chowdhury et al., *ChERD* 2025): 190 pilot cycles (151 ESC + 39 MPC), resampled to 1 s, 8:1:1 split **by cycle**, MinMax to [−1,1] with the scaler fit on train+val only; **one hidden layer, 128 units**, PyTorch, custom loss = MSE over the three states + MSE of the numerically differentiated `ċ_R` + a reconstruction term integrating the predicted gradient back. Test MSE 0.111 mS/cm, MAE 0.732 mS/cm. Projected **iSEC 9.01 vs 9.58 kWh/m³ (17 mS/cm) and 9.24 vs 9.88 (25 mS/cm)** against NARMAX-MPC (~6 % better), with no per-cycle re-identification and therefore no dither. **Caveat the authors state: these are offline simulations — the pilot was no longer operating — and the LSTM will not extrapolate outside its training feedwater distribution.**

**Koopman EMPC — the computational argument.** On BSM1, a deep input–output Koopman model (lift `z = ψ_θ(y)` with a (128,128) ELU MLP to 60 observables, `z⁺ = Az + Bu`, economic stage cost linear in z, so EMPC is a **QP**), 1e5 samples / 400 epochs, horizon 30: **stage cost 1.295e7 vs 1.582e7 (nonlinear EMPC) vs 1.789e7 (tracking MPC)**, at **0.0339 s vs 334.5 s online solve time (~9,900×)**; SAC reached a worse 1.345e7 needing 1e6 samples. That is the strongest quantitative case for Koopman methods in water treatment. For EMPC stability with a non-tracking stage cost, add a Lyapunov constraint (LEMPC), a terminal region + cost, or **average constraints** over a window — the last maps naturally onto water-supply obligations (Ellis, Durand & Christofides, *J. Process Control* 24:1156, 2014).

### 5.4 Reinforcement learning: entirely simulation-only for RO

The reference RO formulation is a **cascade** (Golabi et al., *Applied Intelligence* 54:6333, 2024): a lower-level **DDPG** (state = integrated error, tracking error, permeate flow; action = HP pump feed pressure; reward = +10 if |e| < 0.2 m³/h else −1; 15,000 episodes × 25 steps, γ = 1.0, lr 1e−3, 4 s sampling) under an upper-level **DQN** (state = tank level, demand flow, permeate flow, Δdemand, Δflow; action = permeate setpoint ∈ [12,30] m³/h; reward = quality-dependent revenue − energy cost − overflow/underflow penalty; 1,000 episodes × 1,440 steps at 15 min, γ = 0.9, lr 1e−4, $0.08/kWh). DDPG beats PID above ~65 m³/h, the nonlinear regime. **Simulation only.** Likewise: DDPG on TMP at 99 % rejection (Bonny 2022); **CNN-enhanced SAC** for PV-RO as a POMDP, beating DDPG/PPO/TD3 and vanilla SAC (Soleimanzade 2022); **multi-agent VDN/QMIX** on two-stage RO controlling feed flow, HP pressure and interstage booster pressure, 50,000 episodes in a Julia simulator with PyTorch + PettingZoo, more robust than single-agent.

**The best RL numbers in water are on the wastewater side**: TD3 cut BSM1 aeration + pumping energy **14.3 %** (Croll et al., *ES&T* 2023); DQN cut modelled full-scale MBR aeration energy **34 %** (Nam et al., *WST* 81:1578, 2020) — on a calibrated plant model, not in closed loop. For UF the practical pattern is **LSTM-as-environment**: an LSTM surrogate serves as the RL environment while the agent controls operating pressure, cleaning time and cleaning concentration — **SEC −20.9 %, mean flux 39.5 → 43.7 LMH, operating pressure 0.617 → 0.540 bar** (Park, Shim, Yoon, Lee, Kwak, Lee, Kim, Son & Cho, *Chemosphere* 308:136364, 2022, DOI 10.1016/j.chemosphere.2022.136364) — the correct peer-reviewed anchor for a UF cleaning/pressure business case, and simulation-based like everything else here. The two-stage RO MARL work is now fully identified as Yun, Shim, Moon, Lee, Jeong & Cho, *Desalination* 609:118870 (2025, DOI 10.1016/j.desal.2025.118870): VDN and QMIX versus single-agent DRQN over 50,000 episodes, controlling feed flow, HP pump pressure and interstage booster pressure — **cite it for architecture, not for savings; the abstract reports no % energy figure.** It is the only viable route — you cannot train on a real plant, and no first-principles UF fouling simulator is accurate enough over long horizons.

**Barriers**: a 2025 systematic review screened 678 papers, retained 40, found DQN then PPO dominant, simulator-based training the norm everywhere except hydropower, and **real-world deployment minimal** — the named barriers being the reality gap, explainability, hyperparameter non-standardization, constraint handling and reward design (Kåge et al., *Frontiers in Water*). **Mitigations that exist**: learned simulators with prediction feedback and shape/dynamics loss terms (up to 98 % DTW improvement, arXiv:2403.15091); **offline RL** from historian data with transition filtering, prioritized approximation loss and a VAE bounding distribution shift (BCQ/CQL/AWAC family). **Safe RL for water treatment is thin — no paper applies formal shielding, control barrier functions or constrained MDPs to RO/UF.** The workable safety architecture is synthesized engineering practice, not a cited result: keep RL at L2 as a setpoint selector inside hard L1/L0 interlocks, clip actions to the MPC's constraint box, and fall back to the incumbent PI/DMC controller on any residual or constraint alarm.

### 5.5 Fault detection, diagnosis and fault-tolerant control

**Model-based FDI with reconfiguration** (McFall et al. 2008): one observer per actuator, decoupled using measured states — `dṽ_b/dt = (A_p/ρV)(P̃₁ − ½ṽ_b²e_v1)` with residual `r_b = |v_b − ṽ_b|`, likewise `r_r` for the retentate valve — and a supervisor that switches to a spare on threshold crossing (`k = 2` if `r_r > δ_rr`, `k = 3` if `r_b > δ_rb`). Two hard constraints: **FTC requires physically installed redundant actuators**, and **actuator faults propagate in ~1 s versus hours for feed disturbances, so FDI must sample fast even when the economic layer runs every 5 minutes.**

**Multivariate SPC** — `X = TPᵀ + E`, retain `a` components, monitor `T² = xᵀPΛ_a⁻¹Pᵀx` and `SPE = ‖(I − PPᵀ)x‖²`, with **kernel-density** limits rather than F/χ² on water data and contribution plots for diagnosis. Two extensions matter — **DPCA** (lag augmentation at highest PACF) and **adaptive PCA** (rolling refit) — together AD-PCA (§3.5). Defaults from the full-scale MBR study: **90 % cumulative variance, 6–7 day windows, α = 0.10**, state stratification by covariance analysis rather than arbitrary operating tags. Slow multivariate TMP drift is the hardest case. **Autoencoders** extend SPE to nonlinear manifolds (alarm when `‖x − x̂‖² > τ`), benchmarked on BSM2 for the five canonical sensor faults — **drift, bias, precision degradation, spike, stuck** — with convolutional AEs best; a stacked denoising AE reached **74–98 % detection** while reconstructing the faulty signal so control keeps running. **RO-specific AE fault detection with quantitative F1/false-alarm numbers was not located in this corpus.** The RO-specific sensor-drift answer remains normalization: *normalized* variables into PCA/AE monitors remove most of the nuisance nonstationarity that otherwise forces aggressive retraining.

### 5.6 Real vs simulated — the honest ledger

| Deployed / field-validated | Simulation-only (as of mid-2026) |
|---|---|
| Multi-loop PI + DMC/CMPC on RO trains (1989–2001) | All RL for RO: cascade DDPG/DQN, MARL two-stage, PV-RO SAC, DDPG on TMP |
| Supervisory SEC optimization, 4.2–10 %, two-stage BWRO (Gao 2025) | RL for aeration at 14.3 % (TD3/BSM1) and 34 % (DQN/MBR model) |
| Nonlinear model-based control + SQP energy optimization, UCLA rig (Bartman 2009/2010) | Koopman EMPC (BSM1) |
| MPC and ESC closed-loop on a CCRO **pilot** (Chowdhury 2024/2025) | LSTM-MPC for CCRO (offline replay of pilot data) |
| Commercial ML advisory layers on operating plants (Synauta, Gradiant, Veolia, IDE) | Most autoencoder FDD (BSM2) |
| AD-PCA monitoring on SB-MBR and UF trains over 1–2 years of real SCADA | — |
| Supervisory ML + optimization for pump scheduling in live distribution (EMAGIN HARVI) | — |

**Expected returns for a business case**, consolidated: SEC reduction from supervisory optimization on real plants clusters at **4–10 %**; chemical/CIP savings around **10–15 %** (CIP 12 → 9/yr); pump scheduling in *distribution* is larger at **11–22 %** with 2–7 month paybacks. Anything above 20 % SEC on a modern ERD-equipped SWRO train is extrapolation, not evidence.

---

## 6. Commercial landscape

Vendor-by-vendor detail, sourcing and skeptic's notes: [`research/06_commercial_landscape.md`](research/06_commercial_landscape.md).

Every product in this space wraps the same three layers: (1) physics normalization (SD + ASTM D4516 TCF/NDP), (2) SEC accounting with ERD, (3) a statistical/ML layer. Differentiation is in data engineering, deployment model and trust, not in mathematics.

### 6.1 Vendor table

| Vendor / product | Technique disclosed | Deployment | Quantified savings | Evidence class |
|---|---|---|---|---|
| **Synauta** (Calgary) | ML forecast of feed T/salinity → 3 daily setpoints (HP pump flow, PX booster flow, PX valve-to-drain); normalized to 25 °C/32,000 ppm | Advisory by **email**; 4×1,000 m³/d Osmoflo SWRO, WA | **18 % instantaneous, 9.7 % 6-month average energy, ≈$65k/yr**; extrapolated >$3M/yr at 300,000 m³/d, ~$15M/yr across Australia's Big 6 | **Vendor-run but properly controlled** (normalized, 6 months) |
| **Synauta** (CIP product) | ML-recommended flush/clean intervals | 2-month **A/B with a parallel control train**, 2,700 m³/d brackish, 3 trains, 60 vessels × 4 elements | **+6.2 % permeate, 4 fewer cleans, 8.7 % EDTA savings**, projected ~2× membrane life; F&B deployment projected 10–15 % chemical | **Best controlled trial in the sector** |
| **Gradiant SmartOps** | ML load allocation across trains with differing efficiencies (convex allocation over per-train SEC curves) | ENGIE Middle East SWRO, >200,000 m³/d, 25+1 trains, Pelton ERD | **Up to 5 % energy**, 48 % max recovery, 99.95 % uptime, Δp rise held <5 %; >10 % at an Australian project | **ISO-IPMVP verified — the most defensible large-plant number found** |
| **Gradiant × PUB Singapore** | SmartOps + ceramic pretreatment + ultra-permeable SWRO; €5.4M NRF/PUB grant, D-IVP Ulu Pandan | Pilot train | Target **<2 kWh/m³** vs 3.5 baseline | **Process target**, not an AI result |
| **Veolia Hubgrade Performance** (ex-AQUAVISTA, 2007) | Online digital twin writing optimized setpoints **directly to PLC (closed loop)** | >100 WWTPs | Named sites (traced via Water Projects Online, which reproduces Veolia's case-study content): **Nosedo/Milan, 1,250,000 PE — €630,000/yr, energy intensity 0.431 → 0.323 kWh/kg (−25 %), +20–30 % wet-weather hydraulic capacity**; BlueKolding/Agtrup −25 % effluent TN, −45 % precipitant; Sewerflex +80 % storm hydraulic capacity, −83 % overflows, −23 % energy, €2 M cumulative. Fleet: "up to 30 % aeration energy", "100 % of chemicals", "+40 % biological capacity" | **PARTIALLY VERIFIED — and wrong process class for this report.** Vendor-authored, no independent audit, no stated baseline normalization. **Every verified Hubgrade number is activated-sludge aeration, sewer hydraulics or chemical precipitation, not membranes**; fleet figures are explicitly "up to" single-site maxima. **Do not use to populate a UF/RO band.** The widely-circulated "€1.5 M annual savings / +20 % hydraulic capacity" claim is **DEMOTED and removed**: it traces only to councilofinnovation.com, which names no plant, cites no source, self-assigns "Evidence Score 5/10", and conflicts with the €630 k traceable to Nosedo |
| **Veolia Smart Membranes** | **GAM** normalization of Δp/conductivity/specific flux + **DeepAR on AWS SageMaker** for probabilistic multi-horizon forecasts; 3 yr of Sur (Oman) SWRO historian data; live since Sept 2020 | Inside Hubgrade | **None published** — only qualitative "proactive maintenance / stock management" | Most architecturally transparent; zero numbers |
| **Pani Energy** | Pani Zed (monitoring/anomaly) + Pani Genius (hybrid digital twin: ML + first-principles); advisory only, existing sensors | OCWD GWRS 100 MGD pilot (May 2022, results never published); Aquatech LoWatt partnership | All quantified claims live in **one vendor PDF** (*Pani Zed Case Studies – Desalination*, fetched from their HubSpot CDN; the website carries none). Four cases, 6 MLD to 150+ MLD: FDD on anomalous RO-train feed ORP → **$850k**, issue found in 30 days; predictive servicing 10–30 days ahead → **4.2 % energy = $700k**, **$260k** net annual OPEX, **20 %** membrane-life extension; 6 MLD SWRO predictive time-to-clean → **6 % energy, +12 % recovery, $160k over 2 yr, 16 % membrane life**; UF-RO fouling detected 6 months earlier → $160k, 38 inefficiencies, +30 % successful cleanings | **PARTIALLY VERIFIED, contested — three internal inconsistencies.** (i) Pani's own LinkedIn headline for case 2 says **2.2 %** where the PDF says **4.2 %**. (ii) The arithmetic does not close: **$700k energy + "$440k spent wisely" on chemicals vs $260k stated total annual OPEX savings** — so $700k cannot be quoted as a net saving. (iii) Membrane life drifts 16 % (PDF) vs 20 % (LinkedIn) for the same case. OCWD GWRS results promised mid-2023 remain **unreported as of Aug 2026**; the Aquatech "2.7 kWh/m³" is an aspirational target, not a result. **Defensible residue: 4–6 % energy on SWRO, 16–20 % membrane life, up to 12 % recovery at one 6 MLD site — all vendor self-reported, none audited, no disclosed baseline normalization** |
| **IDE Technologies** | Biofouling/membrane-degradation digital twin from **5 years of Carlsbad data**; Rockwell PlantPAx + Emulate3D; "autopilot" executes production/recovery targets | Carlsbad, 54 MGD | **$1.5M projected over 5 yr** (~0.4–0.5 ¢/m³) — usefully modest and believable; Hadera claims 75 % membrane-lifespan increase | Vendor case study; the small number is its credibility |
| **Ecolab / Nalco 3D TRASAR for Membranes** | Fluorescent-tagged chemistry + online fluorometry + real-time ASTM normalization + ECOLAB3D cloud (Azure) | >50,000 industrial water systems fleet-wide | Fertilizer plant recovery 74→76 %: $14.1k water + $3.2k chemical + $9.8k (CIP 5→3/yr) = **$27.1k/yr**; RO Optimizer PRO 60→73 %: **>$40k** | Small, concrete, plant-named; digital increment not separable from chemistry+service |
| **Kurita** (S.sensing, Fracta, Fracta Leap, Avista) | S.sensing online dosing control; Fracta GBM over **>1,000 variables** for pipe failure; Avista **AdvisorCi** deterministic dosing/scale projection + cleaner selection, NormRO normalization | Broad industrial | >30 % manual-testing time reduction (S.sensing); no membrane % savings | AdvisorCi makes **no ML claims** — it is deterministic chemistry projection |
| **SUEZ AQUADVANCED / InSight** | Real-time multi-source data platform | >1,500 networks and plants | Up to 30 % energy, 15 % NRW, 33 Mm³ losses avoided in 2024 | **Network-level aggregates, not membrane plants**; portfolio muddied post-2022 merger |
| **Xylem Vue / Treatment System Optimization** (+ GoAigua/Idrica) | ML C/N/P models + whole-plant twin driving aeration and dosing | Cuxhaven WWTP | **30 % aeration energy = 1.1 GWh/yr**; Monterrey network 17 % water savings | Wastewater/network, not membranes |
| **EMAGIN HARVI** (→ Innovyze → Autodesk) | Deep learning + (vendor-labelled) RL: demand forecasting + least-cost pump-schedule trajectory optimization | United Utilities Oldham DMZ, 55 MLD, 19 DMAs | **22 % average cost saving (17–45 % range), £50,219/yr, 2.8 £/ML, 5-month payback** after a 12-week programme; network-wide rollout 2019 | Third-party case study; "RL in production" is a vendor/press label, not peer-reviewed |
| **Membrane OEM design tools** (DuPont WAVE/WAVE PRO, Hydranautics IMSDesign-Cloud, Toray DS2/TORAYWISE, LG Q+) | Free physics projection; TORAYWISE adds automatic normalization + trouble-cause analysis + MBR sludge image analysis | Universal | **No published savings for any monitoring product** | Treat as **validation oracles**, not pipeline components |
| **Transcend Design Generator** | Generative design: decision-tree expert rules + 365-day biokinetic simulation → full preliminary package | Design-time | **~90 % of preliminary design automated, <24 h per variant** | Value metric is engineering-hours, not $ savings |
| **ACCIONA** | **Maestro** AI platform (Umm Al Houl SWRO, Qatar); **ACRRO** (simulation optimization) + **Insight** (real-time ML) dual-model | Operating plants | ~12,000 t CO₂/yr at Umm Al Houl; "measurable improvements" in SEC unquantified | Press-release sourced |
| **Gradiant CFRO** (MLD/ZLD hardware, SmartOps as an optional layer) | Counterflow RO placing a controlled brine on the permeate side to suppress effective Δπ — the LSRRO/OARO trick in counterflow; concentrates to **up to 250,000 mg/L TDS** on commercially available membranes below 69 bar | European semiconductor fab; U.S. mining resource-recovery site (capacities undisclosed); USBR pilot | Secondary-source claim of **~half the energy of MVC**; the only audited digital number remains SmartOps' **≤5 % energy** (ENGIE, ISO-IPMVP) | Academic root is split-feed counterflow RO (Bouma & Lienhard, *Desalination* 445:280, 2018). **"Free Flow" branding could not be verified anywhere — treat as unconfirmed.** Audit any "half of MVC" claim: it still means 10–15 kWh/m³ at high concentration factors |
| **Saltworks** (UHP-RO MLD) | **XtremeRO** spiral-wound UHP-RO at **1,800 psi (120 bar)** to 130,000 mg/L; **BrineRefine** chemical softening driven by a **real-time calcium sensor** | Pilots; industrial MLD | Volume-reduction ladder 5×/10×/20×/40×/70× = 80/90/95/97.5/99 % recovery; pilot at **99 % recovery on 1,800 mg/L cooling-tower blowdown, concentrated to 130 g/L**; "membrane systems typically cost 5–10× less than thermal evaporators" | Most concrete numbers published in the MLD space. **The closed-loop Ca-analyzer → softening-dose loop is the practical ML/control entry point in MLD pretreatment** |
| **Aquatech** | **HERO™** high-pH RO (silica-scaling suppression after hardness/CO₂ removal), evaporation/crystallization, "Water Island" ZLD; **DesalPro™ AI-Powered Desalination Optimization** as the digital layer | 2,000+ installations; Thacker Pass lithium | ZLD recovering **99 % of plant wastewater**; **quantified AI results: none published** | Full thermal+membrane ZLD house; the AI layer is unevidenced |

**Notable absences verified**: DuPont "OSMO"/"memEXPERT" digital services have **no public web footprint** — could not confirm they ship. Veolia's "BOB" membrane tool has no surviving documentation (Smart Membranes is the successor). Pani's OCWD results, promised mid-2023, were never published.

### 6.2 Calibration band and how to read vendor claims

The defensible band from controlled/verified results: **5–10 % energy** (large well-run plants at the low end, small plants with loose recovery control at the high end), **10–25 % cleaning chemicals**, **~6 % production uplift** from CIP timing, **22 % pumping energy** in distribution-side scheduling, and **20–100 % membrane-life extension claims that are almost never verified**. Any "up to 30–40 %" traces to a bad baseline, a whole-process redesign, or marketing.

**The band has been re-cut after primary-source verification** ([`research/09_gap_2.md`](research/09_gap_2.md)). Three changes: **Veolia's Hubgrade figures are removed from it entirely** — they are aeration, sewer hydraulics and precipitation, a different physics and a different savings mechanism from membrane fouling management; **Pani's contribution is narrowed to 4–6 % energy and 16–20 % membrane life and explicitly labelled *vendor self-reported*** given the 2.2/4.2 % contradiction and the $700k/$260k arithmetic; and the band is now **triangulated against peer-reviewed anchors on the same problem class rather than resting on vendor numbers** — Park et al. 2022 (UF DRL, **SEC −20.9 %**), Shim et al. 2025 (RO CIP threshold, **−16.1 % opex, simulated**), Jeong et al. 2021 (*Desalination* 518:115289; a full-dimension pressure-vessel model validated on **3,875 h across 27 operational scenarios**, establishing the **high dependence of SEC on cleaning frequency within the feed-temperature range** — the mechanistic justification for the whole CIP-optimization thesis), and the Ecolab CIP patent as the incumbent heuristic to beat. Two rules that fall out of the exercise and should govern how you report your own results: **never quote a gross saving without the offsetting cost increase**, and **if a number has two decimal places it came from a simulation — round it before it enters a business case.**

**Flagship plants' "AI" is mostly modern DCS plus design-time digital twins.** Al Khobar 1 (210,000 m³/d) was commissioned **remotely from Madrid in 2020** via a Siemens SIMIT hydraulic twin. Taweelah (2.81 kWh/m³) and Jubail 3A (<2.80) got there through **ERDs and solar hybridization, not ML**. Keppel Marina East runs ABB Ability DCS, and its "up to 40 %" figure is a process-optimization envelope, not a measured AI result. PUB's Changi twin (Jacobs) is a process twin; Tuas (Bentley iTwin) is an asset/BIM twin — most utility "digital twin programs" start with the latter.

**Market size** diverges by definition: AI-in-water-management $1.48B (2025) → $6.22B (2033) at 19.3 % CAGR; digital water $7–9B → $16–22B (2032–35); smart water management $23.7B → $43.7B (2030). The membrane-plant AI-optimization slice is order **$100Ms**. Benchmark exit: Autodesk's **$1B** acquisition of Innovyze (2021); cautionary tale: FATHOM's 2019 shutdown despite strong technology.

---

## 7. Data infrastructure and deployment reality

Sensor economics, stack detail, twin architectures and regulatory constraints: [`research/07_data_and_digital_twins.md`](research/07_data_and_digital_twins.md).

### 7.1 The sensor layer and what it costs you

| Measurement | Tech | Installed cost (order of magnitude) | Character |
|---|---|---|---|
| Conductivity (feed, permeate, per stage, product) | toroidal/contacting | $1–3k/point | **Most critical instrument**; cell fouling and temperature-compensation errors; frequent calibration |
| Pressure (feed, interstage, concentrate, permeate, cartridge Δp) | piezoresistive | $0.5–2k/point | Stable (±0.1 % span); **stage Δp is the fouling KPI, so transmitter pairing/zeroing errors propagate straight into cleaning decisions** |
| Flow (feed, permeate, concentrate, CIP) | magnetic; ultrasonic on headers | $2–8k/point | Very stable; errors from straight-run and entrained air |
| Temperature | RTD | $0.3–1k | Stable — but **1 °C error biases normalized flow ~3 %** |
| pH | glass electrode | $1–3k + consumable | **Fastest-drifting class**; replacement every 6–18 months |
| ORP / free chlorine | electrode / amperometric / DPD | ORP $1–3k; analyzer $4–10k + reagents | A missed dechlorination event destroys polyamide membranes, so these loops are **hard-interlocked, never ML-mediated** |
| Turbidity | nephelometric | $3–6k/point | Bubble/fouling artifacts; regulatory-grade units need primary-standard verification |
| SDI | manual ASTM D4189 rig / automated | <$2k manual; $15–30k automated | Manual 1–3×/day — sparse, discrete, operator-dependent |
| TOC | UV-persulfate / combustion+NDIR | $6–35k+; **consumables $1.5–5k/yr** | Reagent-dependent, drifts between standardizations |

Sensors split into a **trustworthy backbone** (pressure, mag flow, temperature, conductivity) and **drift-prone chemistry** (pH, ORP, chlorine, turbidity, TOC); a common pattern is to reconstruct chemistry from the backbone via mass balance and flag divergence. SDI and lab data arrive at 10³–10⁵× lower frequency than SCADA tags, requiring asynchronous feature stores with **explicit staleness features**.

**Instrumentation upgrades ranked by value per dollar** (UF): (1) online **UV254** — NOM, not turbidity, drives irreversible fouling; (2) **streaming current monitor** for closed-loop coagulation feedback; (3) online **fluorescence/EEM** — unlocks the Hermia+SVM hybrid; (4) for bloom-exposed SWRO, TEP (particulate and colloidal separately), chlorophyll-a, optionally a hyperspectral feed camera; (5) a **planar camera on a sacrificial canary module** for CNN biofilm classification.

**Instrumentation upgrades ranked by value per dollar (RO chemical side)**: (1) an **external scale-guard element** fed with last-stage concentrate so it scales *first* — this is what lets you run a descending antiscalant dose search without ever risking the production train, and it is the cheapest way to convert §2.10's kinetics from theory into fitted `k_s`, `k_a`, `k_d` for your water; (2) a **Membrane Fouling Simulator** on the RO feed logging Δp continuously, which is the only practical biofouling early-warning instrument given that the meaningful AOC threshold (~1 µg/L) is below routine assay capability; (3) **per-stage or last-element permeate flow** — the whole-stage average dilutes the scaling signal roughly 3×; (4) **inline fluorometry** on feed and concentrate if you use a tagged antiscalant, which buys delivered-dose verification plus an independent recovery estimate; (5) quarterly **ATP/AOC** on the feed and a **full ionic panel including SiO₂ and orthophosphate** — the two ions that silently cap recovery. Note the resolution requirement: the dose search needs **≥5-minute** per-stage pressures, flows, conductivities and temperature, because the NDP-slope test must produce a clean derivative inside a 12–24 h dwell. Hourly data cannot run it.

Counterpoint on budget: the published UF prognostics system ran on **four hydraulic sensors**, and the AD-PCA monitor on **14 tags at 15-minute averages** — you do not need a large instrument budget to start.

### 7.2 The stack, and the silent data killer

Purdue/ISA-95: L0 instruments (4–20 mA/HART, Modbus/Profibus/EtherNet-IP) → L1 PLCs (Rockwell, Siemens S7, Schneider) running interlocks, CIP sequencing and UF backwash state machines → L2 SCADA/HMI (AVEVA System Platform, iFIX, Ignition) → L3 historian → L3.5 DMZ → L4 cloud analytics. The dominant historian is the **AVEVA PI System** (ex-OSIsoft); Ignition is common at smaller municipals. **OPC-UA (IEC 62541)** is the de facto northbound protocol — how a Python service subscribes to tags without touching the control network. Sampling spans 4–5 decades: 100 ms–1 s control loops, 1–60 s historian storage, 2–15 min analyzer cycles, 1–3×/day manual SDI, daily–weekly lab.

**Historian compression is a silent ML killer.** PI-style exception reporting plus swinging-door compression stores only points deviating beyond a band from a linear reconstruction. Thornhill, Choudhury & Shah (*J. Process Control* 14:389, 2004, DOI 10.1016/j.jprocont.2003.06.003) showed data-driven analyses — minimum-variance benchmarks, spectral features, oscillation detection — degrade above **compression factor ≈3**, with nonlinearity measures disturbed lower still. The membrane symptom is staircase-interpolated conductivity that fakes flatlines and destroys derivative features, i.e. **fouling-rate estimates**. **Archive the ~30 tags feeding your twin uncompressed** — a one-line config change that removes a whole class of silent bias.

Three more pathologies to handle explicitly: **calibration steps and drift** (keep the calibration-event log as a first-class dataset; segment training windows at calibrations or add "time since calibration" as a feature); **quality flags** (value + validity + timestamp; bad-quality flags, comms dropouts and manual lab entries coexist); and **operating-mode pollution** (CIP, integrity tests, standby and train swaps must be labelled or your "fouling model" learns the CIP schedule — and UF direct integrity tests run **daily by regulation**, putting structured excursions in every pressure tag).

### 7.3 Digital twin architectures — four families

1. **Mechanistic online twins** (gPROMS-based SWRO), run online for real-time optimal setpoints or offline for scenario exploration, soft sensing and operator training. The argument for them, from Sichel/Siemens: mechanistic twins "optimize to the highest possible level of performance" whereas pure ML "optimizes to the best *experienced* level" — **data-driven models cannot exceed the historical operating envelope.**
2. **The replicable open-source blueprint** — the **Santa Barbara (Charles E. Meyer) SWRO twin**, LBNL + NETL 2021 (DOI 10.2172/1831427), on ProteusLib/**WaterTAP**: **(a) data reconciliation**, `min Σ_i ((x̂_i − x_i^meas)/σ_i)²` subject to material/energy balances; then **(b) windowed parameter estimation** refining `A`, `B`, fouling factors and pump efficiencies. Entire toolchain open source. **This is the pattern to copy.**
3. **Data-driven surrogate twins.** Daaboub et al. 2024 trained 11 algorithms on **18,816 scenarios generated by a solution-diffusion model**; **XGBoost, CatBoost and ANN best**, SHAP confirming sensible drivers. Physics generates the corpus, GBTs serve as the fast online twin.
4. **Asset-degradation twins** — per-element wear states for swap/replacement policy (van Rooij, Scarf & Do 2021).

**Utility programs**: PUB Changi (Jacobs) fuses SCADA-historian data with Replica and Sumo simulators, with automated validation and — the key design feature — **ML that continuously adjusts calibrations *within defined ranges*** without staff intervention; PUB Tuas (Bentley iTwin) is an asset/BIM twin. ACCIONA runs Maestro (Umm Al Houl, ~12,000 t CO₂/yr) plus the ACRRO + Insight pair — **mechanistic + ML in tandem is the emerging commercial pattern: physics for global optimality, ML for real-time tracking.**

### 7.4 Model–plant mismatch and bounded recalibration

Mismatch is structural — feedwater fluctuates, membranes age monotonically, elements get swapped, and fouling develops in ways simulators do not capture — so **a twin calibrated at commissioning diverges within weeks.** The published recipe: (1) **normalize first**, since mismatch in normalized space isolates membrane-state change from operating-condition change; (2) **data reconciliation** before every calibration cycle to detect and correct biased sensors; (3) **windowed parameter estimation** of a small identifiable set — `A(t)`, `B(t)`, per-stage fouling resistance, pump efficiency — by weighted least squares, **freezing everything else**; (4) **bounded auto-recalibration** within defined ranges (the Changi design), so a failing sensor cannot drag the model into nonsense and out-of-bound corrections raise an engineering review; (5) **drift-vs-degradation disambiguation** — a fouling event moves `A` down and stage Δp up **coherently**, whereas conductivity-probe drift moves apparent `B` with **no hydraulic signature**, with a CUSUM on reconciliation residuals `S_t = max(0, S_{t−1} + (r_t − k))` as the practical discriminator; (6) **element-level state tracking** where maintenance optimization is the goal.

### 7.5 MLOps, OT security and operator trust

**Topology.** Inference at L3/DMZ, read-only from the historian, outbound-only; cloud for training, fleet benchmarking and non-latency-critical optimization. The minimum-viable topology **skips OT integration entirely**: Synauta required no new hardware, ran off historian exports, and delivered three setpoints by daily email.

**IEC 62443** shapes everything. Structure: 1-x concepts; 2-x program requirements (**2-4 covers service-provider capabilities — directly applicable to ML vendors**); 3-3 system requirements and four security levels (SL1 casual → SL4 state-level); 4-1/4-2 secure development and components. Seven foundational requirements, including restricted data flow. The operative concept is **zones and conduits**, with three consequences: the model may **read** from the historian in the DMZ but must never open inbound connections into the control zone; **closed-loop writes require certifying the ML host into the control zone at that zone's SL** — precisely why virtually all deployments stay advisory; and vendor remote access falls under 62443-2-4.

**Retraining cadence.** Monitor per-tag input drift (PSI/KS against the training window), prediction-vs-normalized-actual residuals, and constraint-violation counts. **Trigger retraining on membrane-replacement events and seasonal feed transitions, not a fixed calendar.**

**Operator trust.** All commercial desalination twins run advisory, "recommending actions rather than taking them," with a projected **3–5 years to supportive deployments and 5–10 to autonomy**. What worked in the field: three emailed setpoints entered "in a matter of seconds," full manual override retained, no new hardware — eventually reaching "operators depending on the machine learning with only minor validation." **Low-dimensional, physically meaningful recommendations with visible normalization logic are what operators accept.** The negative baseline is **alarm fatigue** (ISA-18.2/IEC 62682, EEMUA 191: ~1 alarm per 10 min steady-state per operator, >10 in 10 min is a flood): **any ML anomaly detector routed into the alarm system must obey the plant's alarm philosophy or operators will suppress it within weeks.** Twins double as operator-training simulators — the trust-building on-ramp.

**Regulated drinking water: keep ML out of the compliance path.** Under EPA's Membrane Filtration Guidance Manual framework, UF log-removal credit rests on **daily direct integrity testing plus continuous filtrate turbidity**; ML may supplement but never replace these, and chlorine/ORP protection stays hard-interlocked. The **EU AI Act classifies treatment-process AI as high-risk, compliance deadline December 2027**, with no RL/ML-control-specific guidance yet published — expect conformity assessment, logging, human-oversight and robustness obligations.

**Acceptance pattern**: a **2–6 month A/B trial against a parallel control train** with pre-registered metrics (Δ normalized SEC, Δ cleans/quarter, Δ chemical spend, Δ normalized permeate flow); absent a control train, **IPMVP Option D calibrated-simulation baselining**. And note where the effort goes: Veolia spent the first phase of the Sur project purely cleaning three years of historian data; Synauta starts every engagement with a historical data audit. **Budget half the project for tag mapping, drift reconciliation and normalization before any ML.**

---

## 8. From-scratch implementation playbook

Tooling detail, repo links, dataset access and the synthetic-simulator recipe: [`research/08_implementation_resources.md`](research/08_implementation_resources.md). Build-order advice from every other file is reconciled here.

The staged plan below is designed so that **every stage produces a testable artifact against known ground truth**, and so that the first shippable artifact requires no actuator authority and no labels.

### Stage 0 — Environment, data inventory and the decision that shapes everything

```bash
conda create -n water python=3.11 && conda activate water
pip install watertap                 # pulls idaes-pse + pyomo
idaes get-extensions                 # IPOPT and friends
pip install gekko do-mpc casadi cyipopt \
            pyEQL phreeqpython rosspy \
            scikit-learn xgboost lightgbm catboost shap optuna \
            torch pytorch-lightning darts pysindy deepxde \
            statsmodels PyWavelets filterpy pymoo \
            mlflow streamlit plotly polars pyarrow duckdb
```

**Minimum viable data (per RO train), reconciled across files 01/02/04/05/07:** at ≥1-minute (accept 5–15 min) historised resolution — feed/permeate/concentrate **flow**; feed, interstage, concentrate, permeate **pressure**; feed and permeate **conductivity**; feed **temperature**; **pH**, ORP; per-stage Δp; and **pump power on every pump** (you cannot optimize SEC from a plant-level kWh meter). **Event logs are mandatory, not optional**: every CIP/CEB/backwash/integrity test with chemistry, dose and duration, membrane install/replacement dates by vessel position, and calibration events per analyzer — without cleaning-response labels there is no cleaning model. Add feedwater chemistry panels at whatever cadence exists, the tariff schedule, hourly renewable generation (PVGIS/NSRDB) if relevant, and costs ($/kWh, element cost ~$500–800 BWRO / ~$600–1,000 SWRO, CIP chemical cost per event, replacement rate 10–20 %/yr). Budget **≥12 months** to capture a seasonal swing and ≥2 CIP cycles; published anchors are 14,542 hourly rows (H2Oaks), 3 years (Veolia Sur), 5 years (IDE Carlsbad), 4 years (UF–RO seawater), 422 days / 12,528 cycles (UF prognostics), 13 months at 15 min (AD-PCA), and 58 months / 2.56 M 1-minute records subsampled to 30 min (Gaublomme/FARYS).

**Three non-tag datasets that are just as load-bearing, and are usually missing.** (1) A **full ionic feed analysis** — Na, K, Ca, Mg, Ba, Sr, Cl, SO₄, HCO₃, F, NO₃, **SiO₂, orthophosphate**, Fe/Mn, plus pH, T, TDS, DOC — because the recovery ceiling is a speciation calculation, not an energy one, and orthophosphate and silica are the two ions that silently cap it. (2) A **firm site disposal-cost function, not a literature range**: the sewer surcharge schedule or POTW contract, DWI quotes with permitting timeline, land price plus net pan evaporation (NOAA/NWS atlas, pan × ~0.7) for ponds, trucking $/m³·km. The published ranges span 5× and the optimum is highly sensitive to which point you sit on. (3) **Chemical prices, dosing-pump calibration curves and the antiscalant certificate of analysis** (active %, phosphorus content) — you cannot bound the overdose side without concentrate Ca²⁺ and antiscalant residual.

**Extraction**: PI Web API / AF SDK, PI Integrator, Ignition SQL, or OPC-UA (`open62541`, `python-opcua`). Land raw tags **with quality flags** into Parquet/TimescaleDB, keep **three layers side by side — raw → reconciled → normalized**, and set CompDev→0 on the ~30 twin tags.

**If you have no plant data** — the common case, since essentially every published dataset in this field is private — the synthetic simulator (Stage 1) is on the critical path. Free real-world sanity checks:

| Dataset | Contents | Use |
|---|---|---|
| **SWaT** (iTrust/SUTD, https://www.sutd.edu.sg/itrust/itrust-labs/datasets/) | 6-stage testbed **including UF (P3) and RO (P5)**; 51 sensors/actuators at **1 Hz, 11 days (~946,700 rows), 36 labelled attacks** | Best open multivariate UF+RO series; practise soft sensors, drift detection, anomaly detection. Free on request (~3 working days) |
| **WADI / BATADAL** | Distribution network (123 tags, 16 days); attack-detection benchmark | Adjacent anomaly-detection practice |
| **UCI Water Treatment Plant** | 527 daily records × 38 features | Pipeline smoke tests only |
| **USBR DWPR + RISE** (https://www.usbr.gov/research/dwpr/, https://data.usbr.gov/) | Pilot desal technical reports (PDF tables); API-accessible water-quality time series | Realistic operating envelopes; expect camelot/tabula extraction |

### Stage 1 — The simulator (weeks 1–3)

Build it **twice** and make the two agree to <1 %: (a) a NumPy/SciPy standalone for speed (thousands of runs/min for ML data generation), and (b) the same steady-state physics as a **WaterTAP/Pyomo flowsheet** (fork `RO_with_energy_recovery`) for the optimizer. This dual build is what makes every later stage verifiable.

**1.1 Deterministic RO core.** Per axial segment (100–300 per vessel):

```python
# per segment, marching along the leaf
pi_b   = osmotic(c_b, T)                       # van 't Hoff / ASTM / pyEQL-Pitzer
k      = Sh(Re, Sc) * D / d_h                  # Schock&Miquel, Koutsou, WaterTAP 0.46(ReSc)^0.36,
                                               # or the CFD M_CP correlation if spacer geometry known
c_m    = c_b * exp(Jw / k)                     # film theory
Jw     = A(T) * (dP - (pi_m - pi_p))           # solution-diffusion
Js     = B(T) * (c_m - c_p)                    # or SF-AA: P*(sqrt(C^2+c_m^2)-sqrt(C^2+c_p^2))
c_p    = Js / Jw
dPf_dx = -f * rho * u_c**2 / (2 * d_h)         # f = 6.23 Re^-0.3 (spiral wound)
```

Solve each segment with `scipy.optimize.brentq` on the flux–CP fixed point, or integrate the whole vessel with `solve_ivp(..., method="Radau")`. Energy: `SEC = (P_f Q_f − η_ERD P_c Q_c)/(η_pump Q_p)`.

**1.2 Chemistry.** `pyEQL` (LGPL) gives Pitzer-based osmotic pressure, activity, density and conductivity from a `Solution` object, decaying gracefully to simpler models when parameters are missing; `phreeqpython` wraps USGS PHREEQC for speciation and saturation indices; `ROSSpy` does 1D reactive-transport RO scaling on the Pitzer database. WaterTAP ships an **OLI Cloud API client** if you hold credentials. Expect ~9 % osmotic-pressure error if you skip activities on SWRO.

**1.3 Fouling and degradation (the slow states).**

```
RO permeability:  A(t) = A_inf + (A_0 - A_inf)·exp(-t/tau_f)      tau_f ~ weeks
cake resistance:  dR_c/dt = k_c·J_w·c_foulant - k_r·R_c           -> J_w = dP_net/[mu (R_m + R_c)]
salt passage:     B(t) = B_0(1 + beta·t)                          beta ~ 5-15 %/yr
UF cycles:        Hermia constant-flux duals; cake p/p0 = 1 + K_c J_0 V
backwash:         R_f -> (1 - eta_bw)·R_f,  eta_bw in [0.8, 0.98]
CEB/CIP:          near-full reset with a small permanent residual (the ratchet)
scaling:          accelerate decline when PHREEQC/pyEQL SI of CaCO3/CaSO4 at the CP-corrected
                  wall concentration exceeds 0
```

Calibrate the drift magnitudes against the Gran Canaria plant: **A −30 %, B +70 % over 4 years / ~27,000 h**, recovery 46 → 38 %.

**1.4 Exogenous drivers and the sensor layer.** Feed temperature = seasonal sinusoid + AR(1) weather noise; feed TDS/turbidity = AR(1) with storm spikes; operator-like setpoint steps. Sensor model: multiplicative Gaussian noise 0.5–2 % per tag, **slow drift with random recalibration steps**, stuck-at and dropout faults at realistic rates, 1-min sampling, plus **quality flags**. Exciting feed concentration with Gaussian noise is exactly what the LSTM-NMPC work used to robustify its model.

**1.5 Validation gates before you proceed.** Cross-check ~10 steady-state cases against **WAVE / IMSDesign-Cloud / Toray DS2 / LG Q+ projections** — note that **none of the four exposes an API or CLI**, so this is manual, and they should be treated as validation oracles, not pipeline components. Then: NumPy twin vs WaterTAP flowsheet agree <1 %; SEC lands in **2–4 kWh/m³** for SWRO; thermodynamic floor respected (≥1.06 kWh/m³); normalized permeate flow **flat across a diurnal temperature cycle**; lead-element flux 2–3× tail flux. Generate **1–3 synthetic plant-years per scenario**, matching the ~2-year scale of the real published datasets.

### Stage 2 — Normalization and the monitoring layer (weeks 3–5): ship this first

This is the highest-ROI artifact in the whole plan: it needs **no labels, no actuator authority, and no ML**, and by itself it reproduces roughly 70 % of the value of commercial monitoring products (3D TRASAR-for-RO, TORAYWISE class).

**2.1 Implement normalization as a pure, unit-tested function** `normalize(df, ref_conditions) -> df_norm`:

```
TCF   = exp[K(1/298 − 1/(273+T))]           K = 2640 (T≥25 °C) / 3020 (T<25 °C) FilmTec;
                                            2500–3000 generic; ASTM fallback 1.03^(T−25)
NDP   = P_f − ΔP_fc/2 − P_p − π̄_fc + π_p
Q_ps  = Q_pa · (NDP_s/NDP_a) · (TCF_s/TCF_a)
C_fb  = C_f·ln[1/(1−Y)]/Y                   ← log-mean, NOT arithmetic
SP_s  = SP_a · (EPF_a/EPF_s)(CF_s/CF_a)(STCF_a/STCF_s)
UF:   L_p = J/TMP · μ(T)/μ(20)              (≈ 1.025^(20−T) to 1.03^(20−T))
```

Unit-test against the worked examples in the DuPont normalization manual (Form 45-D01616). **Validate by confirming normalized permeate flow is flat across a diurnal temperature cycle** — if it is not, your TCF or your temperature sensor is wrong.

**2.2 UF cycle segmentation and per-cycle features.** Split filtration / backwash / CEB / CIP / idle by valve state or a flow threshold (a published system used 15 gpm on backwash flow), then extract per cycle: `R_start`, `R_end`, `R_PB`, `ΔR_irr`, `η_BW`, duration, permeate volume, mean flux, fitted Hermia `n` and `k`. **This step alone usually reveals fouling-rate variability nobody at the plant had quantified.**

**2.3 Fouling-rate estimation.** Robust slopes (Theil–Sen) of normalized indicators between CIPs; resistance-in-series decomposition; the Lakner probabilistic linear baseline with parameter σ's as your model-to-beat.

**2.4 Ship AD-PCA monitoring.** Copy the published configuration verbatim as a starting point: lag-augment each variable with its highest-PACF lag; detrend monitored variables (temperature-corrected permeability, filtrate turbidity, filtrate ammonia) on explanatory variables with **adaptive lasso**; rolling window; **12-day window, α = 0.005, 5 consecutive exceedances**; retrain every 96 in-control observations. Use KDE control limits and contribution plots for diagnosis. Expect **~75 % fault-period detection at ~26 % in-control exceedance** — route it to an operator-review queue, **never into the alarm system**.

**2.5 Diagnostic rule engine.** Encode the four normalized-KPI patterns from §2.6 (flow down → fouling; salt passage up → oxidation/leak; both → tail scaling; Δp up → spacer biofouling) plus the CUSUM drift-vs-degradation discriminator from §7.4.

### Stage 3 — Soft sensors (weeks 5–7)

**Targets** (things the plant does not measure directly): permeate TDS from conductivity, normalized permeability, net driving pressure, CP modulus, membrane resistance, boron permeability coefficient, MFI-UF/SDI from spectral inputs.

**Features**: the backbone tags plus **physics features you compute** — π from van 't Hoff/Pitzer, Re, Sc, Sh, temperature-corrected flux, log-mean C_fb, time-since-CIP, membrane age, and staleness indicators for asynchronous lab values.

**Model ladder**: Ridge → **XGBoost/LightGBM/CatBoost** → small MLP → GPR where calibrated uncertainty is needed. Tree hyperparameters: 300–1000 trees, depth 4–8, lr 0.01–0.1, early stopping on a **chronological** validation block; Optuna for tuning with 5-fold **blocked** CV. SHAP for attribution and physics sanity-checking (temperature ↑ → flux ↑; Δp mostly flow-driven).

**Online parameter tracking** is the physics-side complement: an **EKF/UKF** with state `[R_m or A, B, friction coefficient]` and measurements `[permeate conductivity, permeate flow, reject pressure]` (`filterpy`, or a hand-written UKF — the state is 3–5 dimensional). Reported behaviour: good noise rejection and peak detection, with estimation error growing monotonically as measurement noise rises from 10 % to 50 %. **Critical identification caveat**: fit `A`, `B`, `k` **simultaneously** by non-linear least squares (`scipy.optimize.least_squares`, `trf`, bounded) on clean-membrane windows and report the parameter covariance — `B` and `k` are strongly correlated when only `c_p` is observed, so fitting `B` with `k` fixed from a literature Sherwood correlation **biases `B` high**. Prefer SF-AA `(A, P, C)` if you have multi-salinity data.

**Success bar**: ρ ≥ 0.96, normalized RMSE ≤ 0.02–0.023 (Karimanzira 2021); GPR/ensemble R² 0.98–0.99 on UF flow and resistance.

### Stage 4 — The fouling forecaster (weeks 7–12)

Three parallel tasks, in order of business value:

**Task A — short-horizon trajectory (the core product).** Forecast normalized permeability / TMP / Δp 1–14 days ahead **with planned flux and the CIP schedule as future covariates** — this is what makes the forecast counterfactual and therefore actionable (the MBR-Net design). `darts` (https://github.com/unit8co/darts) gives one API over TFT, TiDE, TCN, N-BEATS/N-HiTS, DLinear, and wrapped XGBoost/LightGBM/CatBoost, **with past/future covariate support, probabilistic outputs, rolling-origin backtesting and SHAP** — the covariate machinery maps exactly onto "forecast TMP given planned flux and CIP schedule."

Architecture selection by regime: **<10⁴ effective samples** → XGBoost on lagged + per-cycle features (do not skip this); **10⁴–10⁵, single train** → GRU/LSTM on **differenced** per-cycle series (ADF first; realistic benchmark **GRU R² = 0.890**), or a TCN with kernel 3, dilations 1/2/4/8, 64–128 channels, dropout 0.1–0.2, Adam 1e−3, input window 1–7 days; **multiple trains with static metadata and multi-horizon quantiles** → **TFT**, whose static-covariate encoder is worth 8 pp of R² (0.981 vs 0.898); **horizons beyond a few days** → Informer-family long-sequence models (R² 0.82 vs 0.65 for CNN-LSTM); **N parallel racks sharing a feed** → graph attention, starting from **https://github.com/cbhua/coagulant-forecast**, the only official open-source codebase in this domain (pretrained checkpoints, YAML configs, W&B, and MLR/LSTM/GRU/CNN-LSTM/LSTM-Attention baselines) — swap the coagulant target for TMP or ΔR_irr.

**Target engineering matters more than architecture**: model **ΔR_irr** and **η_BW** per cycle, or specific flux, not raw TMP across the sawtooth.

**Task B — RUL / cycles-to-threshold.** Implement the Health-Index + fuzzy-similarity baseline first (§3.5). **Beat MAE ≈ 4.1–4.5 cycles before reaching for deep sequence models**, and note its 80 % intervals achieved only 68.6 % empirical coverage — report coverage, not just nominal.

**Task C — structure discovery and inverse problems.** Run **PySINDy** on the simulator's fouling states to confirm you can recover the generating ODE (`dR_f/dt = k₁J² − k₂R_f`-type laws) from noisy data — a clean test of whether your real data is informative enough. Then **DeepXDE** or plain PyTorch autograd for PINN inversion of `A(t)`, `B(t)`:

```
L = L_data + λ₁‖J_w − A(T)(ΔP − Δπ)‖² + λ₂‖J_s − B(T)Δc‖² + λ₃ L_IC/BC + λ₄ L_monotonicity
A(T) = A_ref·exp[−E_a/R (1/T − 1/T_ref)]     learned jointly
```

**Be honest about what is unknown here**: no RO/UF PINN paper in this corpus disclosed layer counts, activations, collocation-point counts, loss weights λ or optimizer schedules. The loss above is a generic construction, not a verbatim published architecture — you will tune λ from scratch, and the *Water Research* 2026 PINN review catalogues the failure modes (loss balancing, stiff PDEs, sparse boundary data). For UF, the two hybrids with the best small-sample evidence are **Hermia-PINN with adaptive sigmoid stage weighting** and **ML-predicts-Hermia-parameters** (SVM on initial flux + organic load + 3 EEM band combinations, R² 0.87–0.99) if you can install a fluorescence probe.

**Validation discipline (non-negotiable)**: chronological blocked splits; **leave-one-CIP-cycle-out** for fouling models; leave-one-membrane/plant-out for materials models; **at least one fully held-out independent run or parallel train** (MBR-Net used two independent test sets). Report horizon-wise RMSE **in engineering units** (kPa, LMH·bar⁻¹, L/min) plus MAE/MAPE and — following the better UF papers — **NSE, KGE and the Willmott index**, which expose bias and variance errors R² hides. Compare against three baselines: persistence, the linear normalized-drift model with CIs, and XGBoost. Provide intervals (bootstrap ensembles, quantile regression, conformal) and **report empirical coverage**.

### Stage 5 — The optimizer (weeks 12–18)

**5.1 First, reproduce the SEC–recovery curve for your plant** from the closed form and plot the current operating point on it. **The gap is your RTO prize — typically 5–15 %.** If the gap is small, the honest answer is that setpoint RTO is not your project; go to cleaning optimization instead.

**5.2 Steady-state economic optimization** on the WaterTAP flowsheet — because a calibrated WaterTAP flowsheet **is already a Pyomo NLP**, this is just: unfix decision variables, add an objective, solve.

```
decision vars: feed pressure, overall recovery Y, stage recovery split Y1, (staged) flux split,
               crossflow velocity u, acid dose / pH, antiscalant dose C_a
objective:     SEC  or  LCOW = (f_crf·C_cap + C_op)/(f_util·Q)  +  c_dis·(1−Y)/Y  +  c_f/Y
                                                          ← price the brine (§4.8); at inland plants
                                                            this term, not SEC, sets the optimum
constraints:   permeate TDS ≤ spec ;  boron ≤ 0.5–1 mg/L (if potable SWRO)
               ΔP ≥ π0/(1−Y)                              ← thermodynamic restriction
               J_w ≤ fouling-safe ceiling                 ← from Stage 4, embedded via OMLT
               SI_s at the TAIL-ELEMENT WALL ≤ S_s^max    ← Reaktoro-PSE / PHREEQC / RBF surrogate (§2.10)
               t_A(SI_wall, C_a) ≥ λ·τ_res(Y,u)           ← the kinetic constraint that PERMITS S^max > 1
               C_a ≤ C_a^overdose(Ca²⁺_conc)              ← the U-shape; calcium-phosphonate bound
               T_run ≤ 1/BFI                              ← biofouling-limited run length (§2.11)
               min brine flow per vessel ;  Δp per stage ≤ 4 bar ;  P ≤ 83 bar
               surrogate input box constraints            ← anti-extrapolation guard
```

Score any scaling-tendency surrogate by **classification accuracy at ST = 1**, not R² — the optimizer only needs the feasible/infeasible boundary (the FOCAPD RBFs hit >99.2 %). Watch for **Regime 2 behaviour**: if the optimizer responds to a tightening scaling constraint by lowering flux and raising crossflow rather than adding chemical, that is correct, and it is telling you concentration polarization is your cheapest scaling lever.

WaterTAP's **default economics give you the $ arithmetic for free**: membranes **$30/m² standard / $75/m² high-pressure**, replacement factor **0.2/yr**, electricity **$0.07/kWh**, WACC **9.30734 %**, 30-yr life → **CRF ≈ 0.0993**, utilization 90 %, TIC 2.0 / TPEC 4.121212. Solve with IPOPT; **scale variables** (pressures in bar, flows in m³/h) or IPOPT will stall; use **multistart (10–50 random initializations)** against nonconvexity.

**5.3 Embed the learned constraint** with **OMLT**, translating your trained Keras/ONNX fouling model or GBT into a Pyomo block. **Tighten big-M by per-neuron interval arithmetic** or MILP solve times explode. The H2Oaks precedent shows a **3-neuron ReLU layer at R² = 0.895 sufficed** — set the accuracy budget by the optimum's sensitivity, not by prediction benchmarks.

**5.4 Cleaning/backwash scheduling** — the higher-value optimizer for most plants:

```
CIP (renewal-reward):
  min_θ  [C_CIP + ∫₀^{T(θ)} c_e·SEC(t)·Q_p(t)dt + C_repl·1(irreversible)] / ∫₀^{T(θ)} Q_p(t)dt

UF cycle (cost per m³ of NET product, not TMP):
  min_{t_f, t_b, τ_CEB, C_dose}  (E_pump·c_e + m_chem·c_chem + amortized membrane) / V_net
  s.t. ΔP_TM ≤ ΔP_max ;  recovery ≥ R_min ;  N_CEB ≥ N_min   ← the anti-reward-hack constraint
```

Initialize/bound with the engineering-scale empirical optima: **TMP trigger ≈103 kPa, recovery ≈92 %**, backwash interval 55–65 min seasonal, and treat backwash *duration* as a weak lever. Solve by enumeration over scenarios first (forecast-then-optimize), then **stochastic dynamic programming** on the learned transition model (the Georgia Tech pattern), then — only if you want the analytic route — **Pontryagin singular control** on the cake-deposition model with per-cycle re-identification (4–9 % MF / 28–31 % UF energy).

**5.5 Tariff/renewable MILP** — only if flexibility exists (storage, parallel pumps, turndown); HiGHS/Gurobi/CPLEX. Remember that for renewable-colocated plants the optimal dispatch often **collapses to an offline-computable threshold policy**, far easier to deploy than an online MILP.

**5.6 Model-free fallback.** If you cannot maintain a model — small plants, CCRO — run **extremum-seeking control** on one variable (recovery or the conductivity trigger) with a small sinusoidal dither: PLC-implementable, needs only flow/pressure/conductivity/power, and delivered **6.5–6.8 %** in **35–85 h** in the published pilot. Its convergence time is also its limitation.

**5.7 Dynamic control, if the process warrants it.** Cyclic or strongly constrained processes (CCRO, batch RO, UF backwash sequencing) justify NMPC. **GEKKO** is the fastest path to a prototype (one `IMODE` switch covers steady-state, RTO, MHE and NMPC, with a `brain` module for an NN internal model); **do-mpc** gives rigorous **robust multi-stage MPC branching over parametric uncertainty** — a natural fit for a drifting `A(t)`; **CasADi + IPOPT** for custom transcription or maximum speed; OSQP/qpOASES for linear/Koopman models at millisecond solves. Replicate Bartman et al. (2010) SQP SEC minimization and the §5.3 CCRO MPC on your simulator; note LSTM-NMPC ran at validation MAE 0.0039–0.0355, tracking index 98.7 %, ~0.02 s inference on 1,871 points — **NMPC is computationally trivial at RO timescales**.

**Do not start with RL.** If you eventually do: an L2 setpoint selector over the existing PI layer; SAC/TD3 for continuous actions, DQN/PPO (or **DRQN**, the safer single-agent choice under partial observability) for discrete scheduling; budget ~50,000 episodes; train against a **calibrated simulator** *and* validate offline on historian data (BCQ/CQL/AWAC); clip actions to the MPC's constraint box; encode the minimum-CEB-count constraint; keep a bumpless fallback to the incumbent controller. `Stable-Baselines3`/RLlib, `pymarl2`/`epymarl` or `PettingZoo` for MARL. **Always evaluate the learned policy against both the threshold-sweep baseline of §4.4 and the Ecolab-style polynomial-trend-plus-safety-margin heuristic.**

**5.8 The chemical-dosing loop, which runs on hardware rather than models.** Independent of the NLP above, and cheaper to deploy than any of it:

1. Install the **external scale-guard** on last-stage concentrate and the **MFS** on the feed. Everything below runs on those two devices, so no experiment risks the production train.
2. Reproduce your plant's **SI-versus-recovery curve at the tail-element wall** for calcite, gypsum, barite, celestite and silica. Locate the knee and compare it to the published pattern (flat, then steep at 64–66 % brackish / 74 % seawater).
3. Run the **step-down dose search** on the scale-guard at production recovery: 12–24 h dwells, ~10 % steps, ratchet-guard and CUSUM disturbance gate as in §4.7. Expect the vendor dose to be 3–10× the optimum. **Stop-loss: abort and restore dose at >5 % normalized permeability loss** (the published evidence says 27 % was still arrestable, so 5 % is deliberately conservative).
4. Fit **`k_s`** from the no-antiscalant scale-guard run and **`k_a, k_d`** from two doses. You can now *predict* the dose required for a new recovery target instead of re-searching for it.
5. Only then relax `ŜT ≤ 1` to `ŜT ≤ S^max` in the WaterTAP model and re-solve for recovery.
6. Only after that, touch biocide: establish the MFS baseline **BFI**, trial DBNPA shock at vendor concentration and frequency, measure ΔBFI, and keep a hard ledger of cumulative oxidant **ppm·h** against the ~1000 ppm·h element-life budget.

### Stage 6 — Advisory delivery, then (maybe) closed loop (weeks 18–24+)

**6.1 The advisory product.** A read-only dashboard (Streamlit or Plotly Dash): current normalized KPIs; the TMP/permeability forecast as a **fan chart**; days-to-CIP with an interval; **a small number of named setpoint recommendations with predicted ΔSEC, Δ$ and payback arithmetic** from WaterTAP costing; drift/anomaly flags. APScheduler for the batch loop, SQLite/Parquet as the local store, **MLflow** as the registry. Design rules from what operators actually accepted: **three setpoints, not thirty**; physically meaningful variables; visible normalization logic; full manual override; and **log every accept/reject as labelled feedback** — your adherence metric and your next training signal.

**6.2 Acceptance trial.** Pre-register metrics and run **2–6 months against a parallel control train**: Δ normalized SEC, Δ cleans/quarter, Δ chemical spend, Δ normalized permeate flow, Δ production, all normalized to standard conditions (25 °C, 32,000 ppm for SWRO). No control train → IPMVP Option D. **Expect and report 5–10 % energy and 10–25 % chemical savings — treat anything larger as a red flag in your own results too.**

**6.3 Closed loop, if at all**, requires write-back through a certified conduit (ML host at the control zone's SL), **hard safety envelopes enforced below the optimizer in the PLC** (min/max pressure, recovery, permeate conductivity, flux), rate limits, watchdogs, bumpless fallback, full audit logging, and EU-AI-Act conformity documentation in the EU. **Never touch compliance instrumentation** — integrity tests, chlorine/ORP interlocks and turbidity reporting stay out of the ML path entirely.

### 8.7 Sequencing, effort and where the time actually goes

| Weeks | Deliverable | Gate |
|---|---|---|
| 0–1 | Data audit, tag map, event-log reconstruction, compression settings fixed | Every CIP/CEB event timestamped and typed |
| 1–3 | Dual simulator (NumPy + WaterTAP) | <1 % agreement; SEC in 2–4 kWh/m³; matches vendor projections on 10 cases |
| 3–5 | Normalization layer + per-cycle features + **AD-PCA monitoring shipped** | Normalized flow flat across a diurnal temperature cycle |
| 5–7 | Soft sensors + EKF/UKF parameter tracking | ρ ≥ 0.96, nRMSE ≤ 0.02; A/B/k fitted jointly with reported covariance |
| 7–12 | Fouling forecaster (XGBoost → GRU/TCN → TFT) + RUL baseline | Beats persistence, linear-drift and XGBoost baselines on leave-one-CIP-out |
| 5–12 (parallel, hardware track) | **Scale-guard element on last-stage concentrate + MFS on the feed**; antiscalant step-down dose search; `k_s`/`k_a`/`k_d` fitted; baseline `BFI` | `NDP_T` flat at the reduced dose for ≥4 weeks; dose bounded above by the concentrate-Ca overdose limit; oxidant ppm·h ledger open |
| 12–18 | Setpoint optimizer (WaterTAP NLP + OMLT, **with wall-referenced scaling constraints and, inland, the disposal term**) and/or cleaning scheduler (SDP) in **shadow mode** | Shadow recommendations logged against operator decisions for ≥1 month |
| 18–24 | Advisory dashboard + A/B trial | Pre-registered metrics, parallel control train |

**Effort estimate from the corpus**: normalization + baseline ≈ 1 week; tree + sequence models with proper backtesting 2–4 weeks; PINN/hybrid with learned `A(t), B(t)` 4–8 weeks including physics unit tests. **The binding constraint is almost always data hygiene — sensor drift, CIP logs, conductivity-probe fouling — not model capacity.** Budget 50 %+ of the project for tag mapping, drift reconciliation and normalization.

**Order the value capture by lever, not by technical interest.** For a UF plant, the highest-value/lowest-risk first lever is **CEB scheduling**, where the Henriksdal trials show 25–75 % of chemical spend is genuinely addressable; for an RO plant it is **CIP timing** (~6 % production uplift, 10–25 % chemicals) ahead of energy RTO (4–10 %), unless your SEC–recovery gap analysis says otherwise.

**Two additions to that ordering from the gap-filling pass.** For any RO plant, the **antiscalant step-down search** now sits *ahead of both* — it is model-free, field-proven at 26–90 % dose reduction, needs a scale-guard element rather than a data-science project, and it also unlocks recovery headroom by converting a hard thermodynamic constraint into a kinetic one. And for any **inland** plant, run the disposal-price arithmetic of §4.8 *before* choosing a lever at all: if brine costs >$1/m³, a single correct recovery point is worth more than the energy RTO, the CIP scheduler and the forecaster combined, and the project you should be running is a scaling/chemistry project wearing an optimization hat. The build order there is: price every legally available disposal route (if surface or sewer discharge is open and uncapped, stop — no MLD economics exist); compute the scaling-limited maximum recovery and compare it to `Y* = 1 − √(c_e π₀/(c_dis + c_f))` to learn which constraint binds; if brine still costs >$1/m³, run the WaterTAP LSRRO/OARO map on your feed and extend recovery while marginal concentration cost stays below `c_dis + p_w`; size the residual pond/crystallizer last, when its cost is linear in a small volume.

### 8.8 Traps that will cost you weeks

**Physics**: fitting `B` as a constant across salinities; applying one TCF to both water and salt flux; arithmetic instead of log-mean feed-brine concentration; computing LSI on the feed rather than the concentrate; ignoring the mass-transfer correlation's leverage (up to 1.6 kWh/m³ and 83 % Δp); treating SDI as a model input without temperature/pressure correction (prefer MFI/UMFI); assuming ideality on SWRO (~9 % osmotic error, scaling onset misplaced by 1 m).

**Chemistry and scaling**: computing SI on the bulk concentrate instead of the **tail-element wall** (understates the driving force by β ≈ 1.1–1.4, locally 2–3×); **treating antiscalant as a saturation credit** — it changes kinetics only, and the projection program's display is a convention, not physics; assuming dose–benefit is monotone (5.0 mg/L was worse than 0.2 mg/L at 765 mg/L concentrate Ca²⁺); running a dose search on a feed with orthophosphate or high silica, where phosphonates do not inhibit the precipitating phase and the search never converges; choosing acid on unit price alone (H₂SO₄'s sulfate load forced 2–41 % more calcium removal and made HCl cheaper over a 10-point recovery band); letting the dose-search ratchet ride after a transient; **diagnosing biofouling from salt passage** (rejection held at 99.72–99.76 % while feed pressure rose 27 % — use feed-channel Δp); placing the SMBS injection point too far forward, which manufactures AOC; and cross-comparing MFS results normalized on average channel velocity rather than spacer-cell perimeter velocity.

**Economics**: using literature $/m³ disposal ranges in the objective when a site quote is obtainable — they span 5× and the optimum is sensitive to the choice; modelling deep-well injection as a $/m³ price rather than binary well-count × step-fixed capital, which lets the optimizer fractionally build wells; optimizing recovery without concentrate-side SI constraints (no published LSRRO/OARO optimization includes scaling, so interstage softening costs must be added by hand); and taking vendor MLD claims at face value without auditing the energy — "half of MVC" is still 10–15 kWh/m³ at high concentration factors.

**ML**: random splits on autocorrelated series; no temperature normalization; raw TMP across the sawtooth; MSE losses that erase fibre breaks and bloom onsets (use wavelet inputs and separate anomaly detectors); quoting simulated or lab R² as a plant expectation; point predictions on asymmetric-cost decisions; expecting MBR feature importances to transfer to pressurized UF.

**Optimization/control**: omitting the thermodynamic restriction (the optimizer will exploit infeasible low-pressure corners); loose big-M in ReLU embeddings; surrogate extrapolation outside the training hull; unscaled NLP variables stalling IPOPT; overestimating batch/CCRO savings by ignoring mixing entropy; building a tariff MILP for a plant with no turndown; adaptive MPC without persistent excitation (parameters diverge within two cycles); optimizers that reward-hack by skipping CEBs; and forgetting that FTC needs physically installed redundant actuators and ~1 s FDI sampling even when the economic layer runs at 5 minutes.

---

## 9. Key references and resources

Deduplicated across the eight research files. Where a paper appears in several files, the fullest citation is given.

### 9.1 Physics, transport and normalization

- Wijmans & Baker, solution-diffusion, *J. Membr. Sci.* 107:1–21, 1995.
- Wang, Elimelech et al., salinity dependence of `B`, *ES&T* 55, 2021 — https://pubs.acs.org/doi/10.1021/acs.est.1c05649 (open copy https://edepot.wur.nl/560875).
- Solution-friction analytical approximation (`A, P, C` intrinsic parameters, validated to 3.64 M NaCl) — https://pmc.ncbi.nlm.nih.gov/articles/PMC12895524/
- Tong et al., pore-flow vs diffusion, *Science Advances* 9, 2023 — https://www.science.org/doi/10.1126/sciadv.adf8488
- Ahmad et al., Spiegler–Kedem for NF, *Membranes* 8(3):78, 2018 — https://pmc.ncbi.nlm.nih.gov/articles/PMC6160980/
- **Mass-transfer/CP correlations and their economic leverage; 228-case CFD `M_CP` and friction fits** — *Membranes* 11(5):338, 2021 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8147287/
- Lin et al., full-size spiral-wound CFD (spacer effect on wall concentration), *Membranes* 11(5):353, 2021 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8150347/
- Ruiz-García et al., Pitzer activities across a 300-segment vessel, *Membranes*, 2021 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8154145/
- Touati et al., van 't Hoff vs OLI divergence, *Membranes*, 2021 — https://pmc.ncbi.nlm.nih.gov/articles/PMC7918311/
- **ASTM D4516** (RO data normalization) — https://www.astm.org/Standards/D4516.htm ; -00 revision text https://pdfcoffee.com/astm-d4516-00-d4516tynq3040-pdf-free.html ; **ASTM D4189** (SDI); **ASTM D3739** (LSI); **ASTM D3923-23 / D6908-06** (integrity testing).
- DuPont FilmTec Technical Manual 45-D01504-en — https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/RO-NF-FilmTec-Manual-45-D01504-en.pdf ; Normalization manual Form 45-D01616.
- Zhao & Taylor, assessment of ASTM D4516, *Desalination*, 2005 — https://www.sciencedirect.com/science/article/abs/pii/S0011916405003504
- Gran Canaria 4-year SWRO degradation dataset (A −30 %, B +70 %) — https://pmc.ncbi.nlm.nih.gov/articles/PMC8540465/
- Iritani & Katagiri, blocking-filtration review, *KONA* 33, 2016 — https://www.jstage.jst.go.jp/article/kona/33/0/33_2016024/_html/-char/en
- **Extended Hermia Model** (continuous P = 2 − n) — https://pmc.ncbi.nlm.nih.gov/articles/PMC10056723
- Field & Pearce, critical/threshold flux, 2011; boundary-flux synthesis, *Membranes* 4(1), 2014 — https://pmc.ncbi.nlm.nih.gov/articles/PMC3925542/
- Huang, Young & Jacangelo, UMFI, *ES&T* 42, 2008 — https://pubs.acs.org/doi/10.1021/es071043j
- Alhadidi et al., SDI↔MFI under cake filtration, *Desalination* 273, 2011.
- **Sagiv, Semiat & Shemer, closed-form induction time with and without antiscalant** (the dose→time transfer function; γ, k_c, k_s, k_a, k_d parameter tables; 8.0/8.7 % mean error over six datasets), *Applied Sciences* 14:4700, 2024 — https://www.mdpi.com/2076-3417/14/11/4700
- **Tong et al., scalant-specific kinetics — gypsum vs silica vs calcite**, *Front. Environ. Sci. Eng.* 19(1):3, 2025 — https://doi.org/10.1007/s11783-025-1923-9
- **Mangal, antiscalant dose optimization** (PhD thesis, IHE Delft / U. Twente, 2023 — antiscalant does not lower saturation; overdose → calcium phosphonate; arrestability proof) — https://ris.utwente.nl/ws/files/301011511/2023_IHE_THESIS_PHD_MANGAL_i.pdf
- Warsinger et al., salinity cycling resets the induction clock in batch RO, *Water Research*, 2018 — https://doi.org/10.1016/j.watres.2018.01.060
- **Vrouwenvelder et al., biofouling as a feed-spacer / pressure-drop phenomenon**, *Water Research*, 2009 — https://doi.org/10.1016/j.watres.2008.11.019 ; **Huisman, Franco-Clavijo, Vrouwenvelder & Blankert, the BFI index and MFS normalization**, *J. Membr. Sci.* 668:121400, 2023 — https://doi.org/10.1016/j.memsci.2023.121400
- RO biofouling review (SEC +27 % at unchanged rejection; polyphosphonates as biofilm nutrient; surface roughness flux hot-spots), *npj Clean Water*, 2022 — https://www.nature.com/articles/s41545-022-00183-0 ; chlorine damage to polyamide (1000 ppm·h, <0.1 ppm continuous), *npj Clean Water* 3:1, 2019 — https://www.nature.com/articles/s41545-018-0024-8
- Al-Juboori & Yusaf, biofouling-potential proxies (ATP, TDC, AOC, BFR), *Membranes* 2:804, 2012 — https://www.mdpi.com/2077-0375/2/4/804 ; online flow cytometry, *Membranes* 14:185, 2024 — https://www.mdpi.com/2077-0375/14/9/185
- Popov et al., fluorescent-tagged antiscalants (ADMP-F, HEDP-F, PAA-F1; 80–100 % efficacy at 1–3 mg/L), *IJMS* 24:3087, 2023 — https://www.mdpi.com/1422-0067/24/4/3087
- Elimelech & Phillip, *Science* 333:712, 2011 (SEC bounds) — DOI 10.1126/science.1200488 ; energy closed forms, *Membranes* 12(4), 2022 — https://pmc.ncbi.nlm.nih.gov/articles/PMC9030420/
- TEOS-10 seawater thermodynamics — http://www.teos-10.org/

### 9.2 ML for RO and UF

- Libotean, Giralt, Rallo, Cohen et al., ANN/SVR on plant RO with memory windows, *J. Membr. Sci.* 326:408, 2009.
- Delgrange et al., UF TMP ANN, *J. Membr. Sci.*, 1998 (DOI 10.1016/s0376-7388(98)00217-8); Delgrange-Vincent et al., *Desalination* 131:353, 2000.
- **Jeong et al., data-leakage demonstration**, *ES&T* 55(16):11348, 2021 — https://pubs.acs.org/doi/abs/10.1021/acs.est.1c04041
- **Gaublomme, Quaghebeur, Van Droogenbroeck, Vanoppen, De Gusseme, Verliefde, Nopens & Torfs, hybrid SD + RNN-LSTM fouling**, *Desalination* **564:116756**, 2023, DOI 10.1016/j.desal.2023.116756 — https://www.sciencedirect.com/science/article/abs/pii/S0011916423003880 ; **green-OA full text (source of the resolved horizon, f_h/f_B, hyperparameters and CIP encodings)** https://biblio.ugent.be/publication/01H8BH8GMBJQ4W31AWX75490QX
- Park, Shim, Yoon, Lee, Kwak, Lee, Kim, Son & Cho, **DRL on an ultrafiltration system** (LSTM surrogate environment; pressure + cleaning time + cleaning concentration; SEC −20.9 %), *Chemosphere* 308:136364, 2022 — DOI 10.1016/j.chemosphere.2022.136364
- Moon, Jeong, Chae, Shim, Kim, Cho & Park, robust deep learning with missing-input estimation on a 1,000 m³/d high-salinity SWRO plant, *Desalination* 603:118678, 2025 — DOI 10.1016/j.desal.2025.118678
- Jeong, Son, Yoon, Park, Shim, Kim, Lim & Cho, full-dimension pressure-vessel model validated on 3,875 h / 27 scenarios (SEC vs cleaning frequency), *Desalination* 518:115289, 2021
- **Helali, Albalawi & Bel Hadj Ali, PINN for SWRO**, *Water* 17(3):297, 2025 — https://doi.org/10.3390/w17030297
- **MBR-Net**, *ES&T*, 2025 — https://pubs.acs.org/doi/10.1021/acs.est.4c12835
- Hermia-PINN with adaptive mechanism transitions, *Sep. Purif. Technol.*, 2026 — https://www.sciencedirect.com/science/article/pii/S1383586626007781
- Hermia + SVM on EEM fluorescence, *ACS ES&T Water*, 2024 — https://pubs.acs.org/doi/abs/10.1021/acsestwater.4c00473
- Stationarity-aware LSTM/GRU TMP forecasting, *JWPE*, 2025 — https://www.sciencedirect.com/science/article/pii/S2214714425016125
- Pham, Do & Do, TCN on Carlsbad data, PHM Society 2024 — https://doi.org/10.36001/phmconf.2024.v16i1.4144
- Temporal Fusion Transformer for RO Δp, *JWPE*, 2024 — https://www.sciencedirect.com/science/article/abs/pii/S2214714424021470 ; architecture: Lim et al., arXiv:1912.09363
- ConvLSTM on full-scale ZLD RO, *ES&T*, 2025 — https://pubs.acs.org/doi/10.1021/acs.est.5c06257
- Holistic RO framework (NAOMI imputation, XGBoost R² 94.75), *Desalination*, 2023/2024 — https://www.sciencedirect.com/science/article/abs/pii/S0011916423008858
- Lakner & Lakner, probabilistic TMP baseline and cost-optimal cleaning interval, *Membranes*, 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12194824/
- Kovacs et al., per-cycle-phase RF/ANN/LSTM with uncertainty, *J. Membr. Sci.* 660, 2022 — https://www.sciencedirect.com/science/article/abs/pii/S0376738822005622
- Zhang et al., UF membrane design ML (320 records, 21 features), *ES&T*, 2023 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10666290/
- Ensemble BPNN + AEA + Bayesian backwash classifier, 4 years UF–RO, *Desalination*, 2021 — https://www.sciencedirect.com/science/article/abs/pii/S0011916421002009
- UF pretreatment real-time modelling, 426 days, *JWPE*, 2025 — https://www.sciencedirect.com/science/article/pii/S1944398625004023
- Khaled, Genga & Kaymak, explainable similarity-based UF prognostics, arXiv:2602.00659, 2026 — https://arxiv.org/abs/2602.00659
- Karimanzira & Rauschenbach: MTCN performance prediction, DOI 10.4236/gep.2021.97004 ; LSTM-NMPC, DOI 10.4236/jamp.2020.812201
- Wavelet coupling for UF integrity/turbidity spikes, *J. Cleaner Prod.*, 2023 — https://www.sciencedirect.com/science/article/abs/pii/S0959652623033759
- Coagulant dosing: jar-test ANN pair, *DWES* 11:1, 2018 — https://dwes.copernicus.org/articles/11/1/2018/ ; Conv1D+GRU on 5 yr minute data, *Chemosphere*, 2023 ; **GAMTF + code** — https://github.com/cbhua/coagulant-forecast ; cycle-to-cycle resistance-based dosing control, *Desalination*, 2016 — https://www.sciencedirect.com/science/article/abs/pii/S0011916416311870
- Park et al., OCT + DNN fouling growth/flux decline, *J. Membr. Sci.*, 2019 ; planar-camera biofilm CNN, *npj Clean Water*, 2025 — https://www.nature.com/articles/s41545-025-00451-9
- Reviews: "From Black Box to Machine Learning," *Membranes* 11(8):574, 2021 — https://www.mdpi.com/2077-0375/11/8/574 ; ANN fouling review, *Membranes* 13(7):685, 2023 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10383311/ ; PINNs in water systems, *Water Research*, 2026 — https://www.sciencedirect.com/science/article/pii/S0043135426001314

### 9.3 Optimization, control and RL

- **Zhu, Christofides & Cohen**, SEC and the thermodynamic restriction, *I&EC Res.* 48, 2009 — https://pubs.acs.org/doi/10.1021/ie9012826 and http://pdclab.seas.ucla.edu/Publications/AZhu/
- El-Halwagi, RO network superstructure, *AIChE J* 38:1185, 1992; Voros et al. 1996; Lu et al. 2007; Saif, Elkamel & Pritzker, global MINLP, *IECR*, 2008 — https://pubs.acs.org/doi/abs/10.1021/ie071316j
- Comprehensive superstructure MOO with NSGA-II over recovery/cost/SEC/CO₂, *IECR*, 2024 — https://pubs.acs.org/doi/10.1021/acs.iecr.4c03467
- AI + NSGA-II BWRO operating-region redesign, *Water Research*, 2025 — https://www.sciencedirect.com/science/article/abs/pii/S0043135425018378
- H2Oaks MILP-over-ANN RTO, *Membranes*, 2022 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8879670/
- Ghobeity & Mitsos, optimal time-dependent SWRO operation, *Desalination* 263:76, 2010; renewable-colocated dispatch, arXiv 2026 — https://arxiv.org/pdf/2601.02243
- Warsinger, Tow, Nayar, Maswadeh & Lienhard, batch/CCRO energy bounds, *Water Research*, 2016
- Extremum-seeking control on a CCRO pilot, *Water Research X*, 2024 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11648806/
- **Chowdhury et al., CCRO MPC**, IWA *Water Supply* 25(4):727, 2025 — https://iwaponline.com/ws/article/25/4/727/107850/ (OSTI PDF https://www.osti.gov/servlets/purl/3002918); LSTM-MPC successor, *ChERD*, 2025 — https://www.osti.gov/servlets/purl/3002293
- **Gao, Jarma, Christofides & Cohen**, field-validated two-stage SEC optimization, *Water* 17:2363, 2025 — https://doi.org/10.3390/w17162363
- Bartman, Christofides & Cohen, *IECR* 48:6126, 2009; Bartman, Zhu, Christofides & Cohen, *J. Process Control* 20:1261, 2010; McFall et al., *IECR* 47:6698, 2008 — PDFs at http://pdclab.seas.ucla.edu/
- Alatiqi et al., *Desalination* 75:119, 1989; Robertson et al., DMC, *Desalination* 104:59, 1996; Assef et al., CMPC, *J. Process Control* 7:283, 1997; Burden et al., *Desalination* 133:271, 2001; Abbas, *Desalination*, 2006 (DOI 10.1016/j.desal.2005.10.033)
- Ellis, Durand & Christofides, EMPC review, *J. Process Control* 24:1156, 2014
- Han, Yao, Law & Yin, deep input–output Koopman EMPC, arXiv:2405.12478, 2024
- Georgia Tech backwash SDP, *J. Membr. Sci.* 612, 2020 — https://www.sciencedirect.com/science/article/abs/pii/S0376738820310413
- Pontryagin adaptive optimal control of filtration cycles, *Membranes*, 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12195455/
- Engineering-scale backwash settings (TMP trigger 103 kPa; CEB invariance), OSTI/DOE, 2023 — https://www.osti.gov/pages/biblio/2329273
- Henriksdal demand-driven cleaning economics, *Membranes*, 2024 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11205864/
- **Shim, Lee, Park, Moon, Lee & Cho, LSTF + RL CIP scheduling**, *Desalination* **614:119193**, 2025, DOI 10.1016/j.desal.2025.119193 — https://www.sciencedirect.com/science/article/abs/pii/S0011916425006691 (closed access; abstract recovered via https://colab.ws/articles/10.1016%2Fj.desal.2025.119193). Attention backbone: Zhou et al., Informer, AAAI 2021, arXiv:2012.07436
- **Atia, Allen, Young, Knueven & Bartholomew, cost optimization of low-salt-rejection RO**, *Desalination* 551:116407, 2023 — accepted manuscript https://www.osti.gov/pages/servlets/purl/1958140 ; LSRRO origin: Wang, Deshmukh, Du & Elimelech, *Water Research* 170:115317, 2020 — https://doi.org/10.1016/j.watres.2019.115317
- Bartholomew, Mey, Arena, Siefert & Mauter, OARO concept, *Desalination* 421:3, 2017 — https://doi.org/10.1016/j.desal.2017.04.012 ; Bartholomew, Siefert & Mauter, OARO cost optimization, *ES&T* 52:11813, 2018 — https://doi.org/10.1021/acs.est.8b02771
- **Amusat, Dudchenko, Atia & Bartholomew, cost-optimal pH control and mineral-scaling prevention for high-recovery RO**, FOCAPD 2024, DOI 10.69997/sct.143335 — https://netl.doe.gov/projects/files/CostoptimalselectionpHcontrolmineralscalingpreventionhirecoveryreverseosmosisdesalination_071024.pdf
- **Akkor, Amusat, Vecchiarelli, Gounaris, Knueven & Dudchenko, Reaktoro-PSE implicit-function chemistry in Pyomo (the four-regime result)**, *ACS ES&T Engineering*, 2026 — https://www.osti.gov/servlets/purl/3030749
- Bouma & Lienhard, split-feed counterflow RO for brine concentration, *Desalination* 445:280, 2018 — https://doi.org/10.1016/j.desal.2018.07.011
- **Mickley, *Membrane Concentrate Disposal: Practices and Regulation*, 2nd ed., USBR DWPR Report 123, 2006** (disposal-route shares; DWI, pond and thermal-ZLD cost regressions) — https://www.usbr.gov/research/dwpr/reportpdfs/report123.pdf
- Arroyo & Shirazi, *Cost of Desalination in Texas*, TWDB 12-06, 2012 (nine real BWRO plants; the Roscoe/Fort Hancock disposal-route natural experiment) — https://www.twdb.texas.gov/innovativewater/desal/doc/Cost_of_Desalination_in_Texas_rev.pdf
- Panagopoulos, Haralambous & Loizidou, brine disposal methods and per-route unit costs, *Sci. Total Environ.* 693:133545, 2019 — https://doi.org/10.1016/j.scitotenv.2019.07.351 ; Jones, Qadir, van Vliet, Smakhtin & Kang, global brine production, *Sci. Total Environ.* 657:1343, 2019 — https://doi.org/10.1016/j.scitotenv.2018.12.076
- Tong & Elimelech, *The Global Rise of Zero Liquid Discharge*, *ES&T* 50:6846, 2016 — https://doi.org/10.1021/acs.est.6b01000 ; Lugo et al., WaterTAP TEA of brine pretreatment (chemical softening $0.96/m³ at 6.3 kWh/m³), *Water* 17:708, 2025 — https://docs.nlr.gov/docs/fy25osti/93400.pdf
- **Mangal, Yangali-Quintanilla, Salinas-Rodríguez, Dusseldorp, Blankert, Kemperman, Schippers, Kennedy & van der Meer, feedback antiscalant dose-search algorithm** (85–90 % reduction, two groundwater pilots, with Grundfos), *J. Membr. Sci.* 650:120717, 2022 — https://doi.org/10.1016/j.memsci.2022.120717 ; Rahardianto, Gu, Khan & Plumlee, imaging-guided dose step-down (−26 %, 100-MGD reclamation facility), *AWWA Water Sci.* 2:e1196, 2020 — https://doi.org/10.1002/aws2.1196
- Jafari, Vanoppen, van Agtmaal, Cornelissen, Vrouwenvelder, Verliefde, van Loosdrecht & Picioreanu, cost of fouling across seven full-scale installations (~24 % of RO OPEX), *Desalination*, 2021 — https://doi.org/10.1016/j.desal.2020.114865
- Golabi et al., cascade DDPG/DQN for RO, *Applied Intelligence* 54:6333, 2024 — https://link.springer.com/article/10.1007/s10489-024-05452-8
- **Yun, Shim, Moon, Lee, Jeong & Cho**, MARL (VDN/QMIX vs DRQN) two-stage RO, *Desalination* **609:118870**, 2025, DOI 10.1016/j.desal.2025.118870 — code https://github.com/Yumbang/Towards-Autonomous-Operation-of-Two-Stage-Reverse-Osmosis-Water-Treatment-System-with-MARL
- Croll, Ikuma, Ong & Sarkar, RL for aeration (TD3 −14.3 %), *ES&T*, 2023 — https://pubs.acs.org/doi/full/10.1021/acs.est.3c00353 ; Nam et al., DQN MBR aeration −34 %, *WST* 81:1578, 2020
- Kåge et al., systematic RL-in-water review, *Frontiers in Water*, 2025 — https://doi.org/10.3389/frwa.2025.1537868
- **AD-PCA on full-scale UF**, Grimm/Newhart/Hering, *ACS ES&T Eng.* 4:1492, 2024 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11184555/ ; SB-MBR companion — https://pmc.ncbi.nlm.nih.gov/articles/PMC10928711/
- Pascual et al., FDI in spiral-wound RO, *IECR* 53:3257, 2014 — DOI 10.1021/ie403603x
- Ceccon et al., **OMLT**, JMLR 23, 2022 — https://www.jmlr.org/papers/volume23/22-0277/22-0277.pdf

### 9.4 Data, twins and deployment

- **Santa Barbara SWRO digital twin on WaterTAP** (data reconciliation + windowed parameter estimation), Gunter, Amusat, Bartholomew & Drouven, DOE OSTI, 2021 — DOI 10.2172/1831427, https://www.osti.gov/biblio/1831427
- van Rooij, Scarf & Do, per-element wear twin at Carlsbad, *Desalination*, 2021 — DOI 10.1016/j.desal.2021.115214
- Daaboub et al., 18,816-scenario surrogate twin, 2024 — DOI 10.3233/FAIA240403
- Pang et al., XGBoost with 12 h dosing-lag features beating DL, *Water Research*, 2024 — DOI 10.1016/j.watres.2024.122777
- **Thornhill, Choudhury & Shah, historian compression degrades data-driven analysis**, *J. Process Control* 14:389, 2004 — DOI 10.1016/j.jprocont.2003.06.003
- Water-sector digital-twin review (147 studies, 4 on desalination), *Water* 17(20):2957, 2025 — https://www.mdpi.com/2073-4441/17/20/2957
- RL-in-desalination survey and TRL assessment — https://smartwatermagazine.com/news/smart-water-magazine/when-plant-learns-run-itself-reinforcement-learning-agents-desalination
- IEC 62443 overview — https://www.fortinet.com/resources/cyberglossary/iec-62443 ; https://www.rockwellautomation.com/en-us/company/news/blogs/iec-62443-security-guide.html
- AVEVA PI System architecture — https://www.aveva.com/en/products/aveva-pi-system/
- EPA Membrane Filtration Guidance Manual, EPA 815-R-06-009, 2005; ISA-18.2 / IEC 62682 / EEMUA 191 (alarm management)
- Jacobs/PUB Changi twin (bounded ML auto-recalibration) — https://www.jacobs.com/newsroom/press-release/jacobs-creating-first-digital-twin-pubs-changi-water-reclamation-plant
- **Ecolab USA (Dörries, Hicks & Krack), US20250296050A1, "Membrane monitoring and clean-in-place control"**, published 25 Sep 2025 — the deployed CIP-scheduling heuristic any ML policy must beat — https://patents.google.com/patent/US20250296050A1/en ; 3D TRASAR for membranes (tracer chemistry and savings unpublished) — https://www.ecolab.com/nalco-water/offerings/3d-trasar-technology-for-membranes
- Veolia Hubgrade case-study content reproduced by an independent trade publication (Nosedo, BlueKolding, Sewerflex figures) — https://waterprojectsonline.com/innovations/hubgrade-2022/
- Pani *Zed Case Studies – Desalination* (the only document carrying Pani's quantified claims) — https://4386400.fs1.hubspotusercontent-na1.net/hubfs/4386400/2025%20-%20Pani%20Website%20-%20Resources%20Page%20and%20Downloadable%20Files/Pani%20Zed%20Case%20Studies%20-%20Desalination.pdf ; OCWD GWRS pilot announcement, results never published — https://www.pani.global/news/pani-energy-&-orange-county-water-district-begin-pilot-to-optimize-groundwater-replenishment-system
- Gradiant CFRO — https://www.gradiant.com/technologies/counter-flow-reverse-osmosis-cfro/ ; Saltworks MLD/UHP-RO — https://www.saltworkstech.com/articles/minimal-liquid-discharge-with-advanced-reverse-osmosis-paper/ ; Aquatech ZLD/HERO/DesalPro — https://www.aquatech.com/technologies/zero-liquid-discharge/

### 9.5 Software, data and code

| Resource | What it gives you | URL |
|---|---|---|
| **WaterTAP** (NAWI/DOE, IDAES/Pyomo) | RO 0D/1D, OARO, NF-DSPMDE, ED, MD unit models; SD **and** SKK transport; film-theory CP with `Sh = 0.46(ReSc)^0.36`; `f = 6.23Re^−0.3`; LCOW costing with real defaults; `RO_with_energy_recovery`, `seawater_RO_desalination`, `lsrro`, `oaro` flowsheets. **UF exists only as zero-order models** — mechanistic UF fouling is yours to build | https://github.com/watertap-org/watertap · https://watertap.readthedocs.io |
| watertap-reflo | Renewable-driven desalination, flexible-load co-optimization | https://github.com/watertap-org/watertap-reflo |
| IDAES-PSE / Pyomo | Equation-oriented substrate; parameter estimation, optimization under uncertainty, surrogate integration (PySMO/ALAMO/Keras), **model diagnostics for ill-conditioned NLPs**, trust-region-filter | https://idaes-pse.readthedocs.io · https://www.pyomo.org |
| **OMLT** | Embed trained NNs/GBTs into Pyomo as full-space, reduced-space or ReLU-MILP | https://github.com/cog-imperial/OMLT |
| GEKKO | Steady-state, RTO, MHE and NMPC via one `IMODE`; APOPT/IPOPT; small `brain` NN module | https://gekko.readthedocs.io |
| do-mpc | Modular NMPC/MHE, orthogonal collocation, **robust multi-stage MPC over parametric uncertainty** | https://www.do-mpc.com |
| CasADi | AD + IPOPT/BONMIN/SUNDIALS; the substrate under do-mpc | https://web.casadi.org |
| pyEQL / phreeqpython / ROSSpy | Pitzer osmotic pressure, activities, conductivity; PHREEQC speciation and SI; 1D reactive-transport RO scaling | https://github.com/KingsburyLab/pyEQL · https://github.com/freiburgermsu/ROSSpy |
| **Reaktoro-PSE** | Equilibrium chemistry **inside** a Pyomo NLP as an implicit-function/external grey-box model returning exact derivatives — scaling tendencies, softening and acid dosing as constraints without surrogate retraining (the prior NN route needed ~2 M PHREEQC samples). Use `pitzer.dat` for sulfates in high-ionic-strength brine | https://github.com/watertap-org/reaktoro-pse · replication flowsheets https://github.com/watertap-org/reaktoro_enabled_watertap |
| **WaterTAP `lsrro` / `oaro` flowsheets + zero-order `deep_well_injection`** | Cost-optimal high-recovery cascades (per-stage `B_case`, `AB_tradeoff`, NaCl solubility cap, `multi_sweep.py` for the salinity × recovery × stage map) and the disposal term, in one Pyomo model | https://watertap.readthedocs.io/en/latest/technical_reference/flowsheets/lsrro.html · https://watertap.readthedocs.io/en/latest/technical_reference/unit_models/zero_order_unit_models/deep_well_injection_zo.html |
| darts | One API over TFT/TiDE/TCN/N-HiTS/DLinear + wrapped GBMs, **past/future covariates**, probabilistic forecasts, backtesting | https://github.com/unit8co/darts |
| PySINDy / DeepXDE | Sparse identification of the fouling ODE; PINN forward/inverse problems | https://pysindy.readthedocs.io · https://deepxde.readthedocs.io |
| **GAMTF coagulant-forecast** | The only official open-source codebase in this domain: pretrained checkpoints, YAML configs, W&B, MLR/LSTM/GRU/CNN-LSTM/LSTM-Attention baselines | https://github.com/cbhua/coagulant-forecast |
| MARL two-stage RO | PettingZoo + PyTorch VDN/QMIX on a Julia RO simulator | https://github.com/Yumbang/Towards-Autonomous-Operation-of-Two-Stage-Reverse-Osmosis-Water-Treatment-System-with-MARL |
| SWaT / WADI / BATADAL | The only open UF+RO plant-scale time series | https://www.sutd.edu.sg/itrust/itrust-labs/datasets/ |
| Vendor projection tools | DuPont WAVE / WAVE PRO, Hydranautics IMSDesign-Cloud, Toray DS2/UF tools, LG Q+ — free, **no API/CLI on any of them**; validation oracles only | https://www.dupont.com/water/resources/design-software.html · https://membranes.com/solutions/software/ · https://www.water.toray/knowledge/tool/ |

---

## 10. Confidence, and what this synthesis does not know

The eight core source files were compiled under heavy paywall constraints; the same caveats propagate here. The three 09-series gap-fill notes narrow the uncertainty in specific places — [`09_gap_2.md`](research/09_gap_2.md) in particular ran a deliberate verification protocol (Crossref PII→DOI, OpenAlex for authorship/funding, green-OA institutional copies, abstract aggregators for closed-access records, vendor PDFs fetched from CDN origins rather than CAPTCHA-protected marketing pages) and graded each claim **VERIFIED / PARTIALLY VERIFIED / DEMOTE**. The paragraphs below are updated accordingly.

**Weakly sourced by construction.** ScienceDirect, ACS, MDPI, Wiley, IWA and Springer all returned HTTP 403/402 to scripted fetching, so roughly 60 % of the UF/MBR primary sources and a substantial share of the RO ones are characterized from abstracts or secondary reviews. **Exact hyperparameters, layer counts, batch sizes and per-fold results are missing** for several headline studies (the TCN, the TFT, MBR-Net, the Georgia Tech SDP backwash paper, the stationarity-aware GRU, the DRL ultrafiltration paper), and author attribution is incomplete for several UF papers cited by journal/year/URL only.

**Reconstructed rather than verified.** ASTM D4516-19a and D4189-07 are paywalled; the equations here come from the withdrawn D4516-00 revision and vendor sources, so symbol conventions may differ in the current revision. DuPont's design shortcuts (`β = exp(0.7·Y_element)`, `Δp ≈ 0.01q^1.7`) are "widely reproduced" rather than primary-verified. Pitzer parameter tables, TEOS-10 Gibbs coefficients, SDI↔MFI conversion coefficients and the full MFI-UF derivation were not retrievable — use PHREEQC/pyEQL/Reaktoro implementations.

**Numbers that differ between files** (flagged in place above): thermodynamic SEC minimum (1.06 vs 1.07 kWh/m³, vendor floor band 0.8–1.5); UF RUL MAE (4.08 vs 4.50 cycles); Veolia's aeration claim (25 vs 30 %); TCF constant K (2500–3000 vs 2640/3020, with Mangal's monitoring practice using 2700); osmotic shorthand (0.75–0.8 vs 0.7854 vs 0.78 bar per g/L). **Resolved**: the Gaublomme horizon is not a discrepancy — 8 months is the data-driven model's test partition and 2.5 months is the hybrid simulation window, chosen where fouling prediction was good (§3.3). **New internal contradictions, in vendor material rather than ours**: Pani's 2.2 % vs 4.2 % energy saving for the same case, its 16 % vs 20 % membrane-life extension, and its $700k energy saving against a stated $260k net OPEX saving.

**Verified absences — do not assume these exist.** No supervised classifier for UF fouling *type* from routine online SCADA. No labelled corpus of CNNs on membrane-autopsy SEM images. No RO-element-specific RUL model. No peer-reviewed payback periods for ML-on-membrane deployments (only vendor figures: Synauta $65k/yr, EMAGIN 5-month payback, ERD retrofit ~1.3 years). No published RMSE/R² for any commercial digital twin. No sim-to-real methodology for desalination RL. No shielding/CBF/constrained-MDP work on RO/UF. No membrane-specific subspace identification. No closed-loop RL deployment on a real RO train. **No ML controller for antiscalant dose** (targeted OpenAlex searches on `antiscalant AND machine learning` and `scaling index prediction neural network desalination brine` return essentially zero on-topic works). **No published DBNPA shock concentrations, contact times or frequencies** — neither major biofouling review gives them. **No published tracer chemistry or quantified savings for Ecolab 3D TRASAR.** **No LSRRO/OARO cost optimization that includes mineral scaling, and no LSRRO pilot demonstration anywhere.** The Sagiv induction-time model is validated **only on CaSO₄ with two antiscalant chemistries** — `k_a, k_d` for CaCO₃, BaSO₄ and modern polycarboxylates must be measured, not looked up.

**Traceability, after the verification pass.** Now **VERIFIED**: the 16.13 % / 139.53 % RL-CIP figures appear verbatim in the author-written abstract of *Desalination* 614:119193 — but as simulated outputs on an industrial UPW RO train, with the run-time figure being the mechanism rather than the benefit. Now **PARTIALLY VERIFIED and quarantined**: Veolia's Hubgrade numbers (vendor-authored, unaudited, and all of them wastewater aeration/sewer/precipitation rather than membranes) and all Pani figures (vendor-authored, internally inconsistent, no control train). Now **DEMOTED and removed**: the €1.5 M / +20 % hydraulic capacity claim sourced only to councilofinnovation.com. Still untraceable: the Aquatech LoWatt 2.7 kWh/m³ target (an aspiration, not a result), Gradiant's "half the energy of MVC" for CFRO and its unverifiable "Free Flow" branding, and all market-size estimates.

Treat §6's percentages as **upper bounds pending an A/B trial on your own trains**, and §1.1's calibration band — 5–10 % energy, 10–25 % chemicals, ~6 % production uplift — as the planning number. For the chemical and recovery levers added in this revision, the planning numbers are **26–90 % antiscalant dose reduction** (field-measured on pilots, arrestable, but with a U-shaped risk curve that demands an overdose bound) and, at inland plants, **a disposal-cost-aware recovery optimum worth more than the entire energy stack** — both of which need site-specific chemistry and a site-specific disposal price before they mean anything.




