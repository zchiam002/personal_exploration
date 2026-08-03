# Physics Foundations of RO and UF: Mechanistic Models that Anchor Hybrid ML, Digital Twins and Optimization

Scope: the first-principles layer that a hybrid (physics + ML) water-treatment model must contain. Everything below is written so it can be coded directly: governing equations, the exact correlations and their fitted exponents, what is measurable, what must be regressed from plant data, and where ML is grafted on. Units are SI unless a vendor convention is stated.

---

## 1. Modeling hierarchy

Five nested levels, each with its own state vector and its own identifiable parameters:

1. **Membrane point model** — local water and salt flux at a differential membrane area (`A`, `B`, or friction/partition parameters).
2. **Channel model** — hydrodynamics + concentration polarization (CP) in the spacer-filled feed channel (mass transfer coefficient `k`, friction factor `f`).
3. **Element model** — spiral-wound 8" element, 37.2 m² (400 ft²) of active area, integrated along the leaf length.
4. **Pressure-vessel / stage model** — 6–8 elements in series, tapered arrays (e.g. 2:1), interstage boosters.
5. **Plant model** — pretreatment (UF/MF, dosing), high-pressure pumps, energy recovery devices (ERDs), post-treatment, and the economics (SEC, chemical cost, CIP frequency).

A digital twin that only implements level 1 will misestimate stage-2 flux distribution and scaling risk; a twin that implements 1–4 but ignores level 5 cannot optimize energy or chemicals. The full-size spiral-wound CFD study of Lin et al. (Membranes 11(5):353, 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC8150347/) shows why: in a 2.05 m × 0.9 m leaf with a 0.86 mm feed channel, removing the spacer raised wall concentration by **84.67 %** over inlet versus **15.30 %** with the spacer, and the mass transfer coefficient rose from **7.95 × 10⁻⁵ to 1.59 × 10⁻⁴ m/s** — a level-2 effect that entirely changes level-1 driving force.

---

## 2. Membrane transport: solution-diffusion and its successors

### 2.1 Classical solution-diffusion (SD)

$$J_w = A\,\big[(P_f - P_p) - \sigma(\pi_m - \pi_p)\big] \equiv A\,(\Delta P - \Delta\pi)$$
$$J_s = B\,(c_m - c_p)$$

with `A` [L m⁻² h⁻¹ bar⁻¹, or m s⁻¹ Pa⁻¹] the water permeability, `B` [m s⁻¹] the salt permeability, `c_m` the wall concentration, and for high-rejection RO `σ ≈ 1`. Permeate concentration follows from the flux ratio:

$$c_p = \frac{J_s}{J_w} = \frac{B\,c_m}{J_w + B}, \qquad R_{obs} = 1 - \frac{c_p}{c_b}$$

This is the model embedded in essentially every commercial projection tool (WAVE/ROSA, IMSDesign, Winflows) and in the mechanistic half of published hybrid models (Gaublomme et al., *Desalination* 2023, https://www.sciencedirect.com/science/article/abs/pii/S0011916423003880).

### 2.2 Why `B` is not a constant — and what to do about it

`B` treated as a membrane constant is the single largest structural error in RO models. Wang, Elimelech and co-workers (ES&T 55, 2021, https://pubs.acs.org/doi/10.1021/acs.est.1c05649; open copy https://edepot.wur.nl/560875) showed that measured rejection varies strongly with feed salinity, so `B` fitted at one salinity does not transfer. Tong et al. (*Science Advances* 9, 2023, https://www.science.org/doi/10.1126/sciadv.adf8488) argue water transport is pore-flow rather than diffusive; Wijmans-style SD derivations are challenged in *Desalination* 2024 ("The solution-diffusion model for water transport in reverse osmosis: what went wrong?", https://www.sciencedirect.com/science/article/abs/pii/S0011916424002868).

The practical replacement is the **solution-friction analytical approximation (SF-AA)** (2025/2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC12895524/), which replaces `B` with two salinity-invariant parameters:

$$J_s = P\Big(\sqrt{C^2 + c_m^2} - \sqrt{C^2 + c_p^2}\Big), \qquad B_{obs} = \frac{P\big(\sqrt{C^2+c_m^2}-\sqrt{C^2+c_p^2}\big)}{c_m - c_p}$$

with `P` the transport factor [L m⁻² h⁻¹ bar⁻¹] and `C` the charge factor [M]. Validated on NaCl to **3.64 M**; for NF90 `C ≈ 0`, `P ≈ 3`; a chlorinated NF90 gave `P ≈ 99 L m⁻² h⁻¹ bar⁻¹`. Data from different salinities collapse onto one master curve of `B_obs` vs interfacial concentration — meaning three intrinsic parameters (`A`, `P`, `C`) replace a salinity-indexed lookup of `B`.

### 2.3 Irreversible-thermodynamics form (Spiegler–Kedem / Kedem–Katchalsky)

For NF and loose RO, use the two-parameter SK form (Ahmad et al., Membranes 8(3):78, 2018, https://pmc.ncbi.nlm.nih.gov/articles/PMC6160980/):

$$J_v = L_p(\Delta P - \sigma\Delta\pi),\quad J_s = P_s\Delta c_s + (1-\sigma)J_v c_m$$
$$R_{obs} = \frac{\sigma(1-F)}{1-\sigma F},\qquad F = \exp\!\left[-\frac{(1-\sigma)J_v}{P_s}\right]$$

Fitting `(σ, P_s)` per ion by Levenberg–Marquardt on an `R` vs `J_v` sweep is the standard characterization experiment. Reported values for NF270 on seawater: Cl⁻ σ = 0.18, `P_s` = 2.1 × 10⁻⁵ m/s; SO₄²⁻ σ = 0.97, `P_s` = 5.3 × 10⁻⁷ m/s; Mg²⁺ σ = 0.45, `P_s` = 6.2 × 10⁻⁶ m/s. Steric-hindrance-pore closure: `σ = 1 − S_F[1 + (16/9)q²]`, `S_D = (1−q)²`, `S_F = 2(1−q)² − (1−q)⁴`, `q = r_s/r_p`.

### 2.4 Temperature dependence

Both `A` and `B` are Arrhenius-activated. Vendor practice (DuPont FilmTec Technical Manual 45-D01504-en, https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/RO-NF-FilmTec-Manual-45-D01504-en.pdf) uses

$$\mathrm{TCF} = \exp\!\left[2640\left(\frac{1}{298} - \frac{1}{T}\right)\right] \ (T \ge 298\,\mathrm{K}),\qquad \mathrm{TCF} = \exp\!\left[3020\left(\frac{1}{298} - \frac{1}{T}\right)\right]\ (T \le 298\,\mathrm{K})$$

i.e. `A(T) = A(25 °C)·TCF`. The activation energies implied are 21.9 and 25.1 kJ/mol; an independent Arrhenius fit gives `E_a ≈ 25 kJ/mol` for transmembrane water transport (Desalination & Water Treatment 192, 2020, https://www.deswater.com/DWT_articles/vol_192_papers/192_2020_431.pdf). ASTM D4516's default when vendor data are unavailable is the simpler `TCF = 1.03^(T−25)` with T in °C (https://www.astm.org/Standards/D4516.htm), which corresponds to the field rule of thumb of **2.5–3.0 % permeate flow change per °C**. Salt permeability has a *higher* activation energy than water permeability, which is why rejection degrades with warm feed — a hybrid model that applies one TCF to both flows will systematically mispredict summer permeate TDS.

---

## 3. Osmotic pressure: van 't Hoff vs Pitzer/OLI

**van 't Hoff:** `π = i·C·R·T` (`i` = 1.9 for NaCl, `C` in mol/L, π in bar with R = 0.083145 L bar mol⁻¹ K⁻¹). Simple, differentiable, adequate to ~0.6 M.

**ASTM D4516 engineering form** (mg/L, kPa):
$$\pi_{fb} = \frac{0.2654\,C_{fb}\,(T + 273.15)}{1000 - C_{fb}/1000}$$
with permeate osmotic pressure approximated `π_p = 0.05 π_fb` (brackish) or `0.01 π_fb` (seawater).

**FilmTec form** (psi): `π = 1.12 (273 + T) Σ m_j`, summing molal concentrations of all species.

**Non-ideal:** OLI Stream Analyzer regression for NaCl, `π = 5.94028 C² + 37.4521 C` (bar, C in mol/L), valid above 0.6 M. Touati et al. (Membranes, 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC7918311/) quantify the error: van 't Hoff and OLI cross near 1.9 M, deviate <5 % over 1.0–2.4 M, and diverge by up to **30 % in π and >50 % in derived power density above 2.4 M**. At seawater strength the practical numbers are ~27 bar for 35,000 mg/L; Pitzer gives 381 psi vs a 366–382 psi measured band at 35,630 ppm TDS.

**Pitzer inside the element model:** Ruiz-García et al. (Membranes, 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC8154145/) discretized a 6 m pressure vessel into **300 axial elements** and solved Pitzer activity/osmotic coefficients locally. Assuming ideality **overestimated osmotic pressure by ~9 %**, sulfate activity coefficients fell up to **65 %** from inlet to outlet at high recovery while the osmotic coefficient rose 3 %, and — critically for scaling control — activity-based calculation predicted fouling onset **1 m earlier** along the vessel than concentration-based calculation.

Engineering guidance: use van 't Hoff (or the ASTM form) for BWRO up to ~10 g/L; use Pitzer/OLI for SWRO brine, ZLD, and any scaling-index computation. TEOS-10 (http://www.teos-10.org/) provides a thermodynamically consistent Gibbs function for seawater properties (density, viscosity, activity) and is the right source for `ρ(T,S)`, `μ(T,S)`, `D(T,S)` inputs to the Sherwood correlations.

---

## 4. Concentration polarization and mass transfer in spiral-wound channels

### 4.1 Film theory

Steady 1-D solute balance in the boundary layer gives the CP modulus:

$$\frac{c_m - c_p}{c_b - c_p} = \exp\!\left(\frac{J_w}{k}\right), \qquad \beta \equiv \frac{c_m}{c_b} \ \text{(for high rejection)} \approx \exp(J_w/k)$$

`k` [m/s] is the mass transfer coefficient, obtained from `Sh = k d_h / D`.

### 4.2 Correlations

- **Schock & Miquel (1987)**, the industry default for spacer-filled channels: `Sh = 0.065 Re^0.875 Sc^0.25`, with pressure drop `dp/dx = f ρ u_c²/(2 d_h)`, `f = 6.23 Re^(−0.3)`.
- **Koutsou et al.**: `Sh = 0.2 Re^0.57 Sc^0.40`.
- **Generic literature fit**: `Sh ∝ Re^0.68 Sc^0.20`.
- **CFD-derived direct CP correlation** (Membranes 11(5):338, 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC8147287/) bypasses film theory entirely:

$$M_{CP} - 1 = C\,Re_c^{\alpha}\,(m\,Re_t)^{\beta}\,Sc^{\gamma}\,GR^{\delta},\qquad m = 10^4,\ GR = L_f/D_f$$

with `Re_c = ρ u_c D_f/μ` (crossflow) and `Re_t = ρ u_t D_f/μ` (transmembrane, i.e. built from the permeate velocity). Fitted over **228 CFD cases** (76 per spacer configuration), `Re_c` 1.12–274, `Sc` 111–4475, channel height 0.2–1.4 mm, `L_f/D_f` 2–6:

| Spacer | C | α | β | γ | δ | MAPE |
|---|---|---|---|---|---|---|
| Cavity | 2.55e-4 | −0.350 | 1.11 | 0.611 | 5.40e-4 | 0.375 % |
| Submerged | 5.55e-3 | −0.422 | 1.09 | 0.672 | 0.536 | 0.516 % |
| Zigzag | 3.24e-4 | −0.394 | 1.12 | 0.597 | 2.18e-4 | 0.516 % |

Friction factor: `f = C' Re_c^{α'} GR^{δ'} + ζ`; cavity: C' = 14.8, α' = −0.910, δ' = −0.525, ζ = 0.0256 (MAPE 1.15 %); submerged: 63.3, −0.994, −0.810, 0.0868 (1.48 %); zigzag: 14.0, −0.898, −0.510, 0.0200 (0.974 %).

**Why this matters economically:** propagating the different correlations through a process model changed predicted recovery by **−4.7 to +1.9 %**, pressure drop by **−53 to +83 %**, and specific energy by **−0.81 to +1.6 kWh/m³**. Mass-transfer correlation choice is therefore not a second-order detail — it is comparable in magnitude to the entire energy-optimization opportunity.

### 4.3 Vendor element-scale shortcut

Design software collapses level 2 into the element recovery. DuPont's FilmTec design equations use the widely reproduced empirical CP factor `β = exp(0.7 Y_i)` (with `Y_i` the *element* recovery) and cap `β ≤ 1.2`, plus an element pressure-drop power law of the form `Δp ≈ 0.01 q_avg^{1.7}` (bar, m³/h) — convenient, but calibrated to specific spacers, and the correct move in a twin is to replace both with the CFD-fitted forms above once spacer geometry is known.

---

## 5. Element, vessel and stage models

Integrate along the leaf coordinate `x ∈ [0, L]` (or discretize into N segments; 100–300 segments per vessel is typical and matches the Pitzer study's 300):

$$\frac{dQ_f}{dx} = -J_w(x)\,w,\qquad \frac{d(Q_f c_f)}{dx} = -J_s(x)\,w,\qquad \frac{dP_f}{dx} = -\frac{f\rho u_c^2}{2 d_h}$$

Closures per segment: `π` from §3, `c_m = c_b exp(J_w/k)` from §4, `J_w, J_s` from §2, `k` and `f` from the Sherwood/friction correlations, `A, B` scaled by TCF and a fouling factor.

Vessel-level aggregate quantities:
- Recovery `Y = Q_p/Q_f`; concentration factor `CF = 1/(1−Y)` for perfect rejection, `CF = (1 − Y(1−R))/(1−Y)` in general.
- Log-mean feed-brine concentration (ASTM D4516): `C_fb = C_f ln[1/(1−Y)] / Y`; arithmetic alternative `C_fb = (C_f + C_b)/2`. The log-mean is the correct average for exponential concentration build-up and is what should feed the osmotic pressure term.
- Bulk `β` limit and minimum concentrate flow per element (typically ≥ 3.6 m³/h for 8" SWRO elements) are the hard constraints that any optimizer must carry.

Element-by-element models validated against ROSA agree to ~95 % (see the survey in *Water Practice & Technology* 19(7), 2024, https://iwaponline.com/wpt/article/19/7/2681/102654/Mathematical-modeling-of-reverse-osmosis-system). The flux distribution matters: lead elements can run 2–3× the tail flux, which is why fouling concentrates in stage 1 and scaling in the tail.

---

## 6. Data normalization: making plant data model-comparable

Raw SCADA trends are useless for fouling detection because pressure, temperature, recovery and feed TDS all drift. **ASTM D4516** (https://www.astm.org/Standards/D4516.htm; text of the -00 revision at https://pdfcoffee.com/astm-d4516-00-d4516tynq3040-pdf-free.html) defines the standard transformation:

$$Q_{ps} = Q_{pa}\cdot\frac{(P_{fs} - \Delta P_{fbs}/2 - P_{ps} - \pi_{fbs} + \pi_{ps})}{(P_{fa} - \Delta P_{fba}/2 - P_{pa} - \pi_{fba} + \pi_{pa})}\cdot\frac{\mathrm{TCF}_s}{\mathrm{TCF}_a}$$

i.e. normalized permeate flow = actual flow × (standard NDP / actual NDP) × TCF ratio. Salt passage normalizes analogously against the standard element permeate flow and the feed-brine concentration ratio. Brine concentration `C_b = C_f/(1−Y)`.

Interpretation rules that a diagnostic layer should encode:
- Normalized permeate flow ↓ >10–15 % → fouling/compaction → CIP trigger.
- Normalized salt passage ↑ >10 % with flow steady → membrane damage/oxidation or o-ring leak.
- Both moving together → scaling in the tail.
- Δp across a stage ↑ >15 % → colloidal/biofouling in the feed spacer.

Real degradation rates for calibration: a 5,000 m³/d SWRO plant in Gran Canaria (56 vessels × 7 elements, ~27,000 operating hours over 4 years, https://pmc.ncbi.nlm.nih.gov/articles/PMC8540465/) saw **A fall ~30 %** and **B rise ~70 %**, recovery drift from 46 % → 38 %, feed pressure 6.1–6.8 MPa, salt rejection 99.75 %, permeate 200–800 µS/cm, and SEC 3.75–4.25 kWh/m³ (HPP alone ~3.04 kWh/m³). Three candidate A(t) decay models fitted with standard deviations 0.0011–0.0015.

---

## 7. Feedwater fouling and scaling indices

**SDI (ASTM D4189)**: 0.45 µm, 47 mm membrane, dead-end at 207 kPa (30 psi), time to collect 500 mL initially (`t_i`) and after T = 15 min (`t_f`):

$$\mathrm{SDI}_{15} = \frac{100\,(1 - t_i/t_f)}{T}$$

Plugging factor `%P30 = 100(1 − t_i/t_f)` must be ≤ 75 %, else use SDI₅. Design limits: SDI₁₅ < 4 for RO feed; <1 ≈ years between cleanings, 3–5 ≈ frequent cleaning, >5 unacceptable (Hydranautics procedure, https://membranes.com/wp-content/uploads/pdf/tsb/RO/Procedure%20for%20Measuring%20Silt%20Density%20Index%20(SDI).pdf). SDI is *not* model-based, is not temperature-corrected, and is non-linear in colloid concentration.

**MFI** replaces it with cake-filtration theory: plotting `t/V` vs `V` gives a linear region whose slope is MFI,

$$\frac{t}{V} = \frac{\mu R_m}{\Delta P\,A} + \frac{\mu\, I}{2\,\Delta P\, A^2}\,V \equiv a + \mathrm{MFI}\cdot V$$

so MFI ∝ `μ I /(2 ΔP A²)` with `I` the cake fouling index. MFI is pressure- and temperature-correctable; the SDI↔MFI mapping under a cake-filtration assumption is derived by Alhadidi et al. (*Desalination* 273, 2011, https://www.sciencedirect.com/science/article/abs/pii/S0011916410008593), which also shows SDI's dependence on pressure, temperature and membrane resistance. See also the fouling-index treatment in Iritani & Katagiri's blocking-filtration review (KONA 33, 2016, https://www.jstage.jst.go.jp/article/kona/33/0/33_2016024/_html/-char/en).

**UMFI** (Huang, Young & Jacangelo, ES&T 42, 2008, https://pubs.acs.org/doi/10.1021/es071043j) generalizes to low-pressure membranes: normalized specific flux `J'_s = J_s/J_s,0` against unit permeate volume `V_s` [L/m²],

$$\frac{1}{J'_s} = 1 + \mathrm{UMFI}\cdot V_s$$

so UMFI is a slope with units m²/L, valid in both constant-pressure and constant-flux modes and comparable across scales.

**Scaling indices.** LSI = pH − pHs, with the ASTM D3739 / Langelier decomposition `pHs = (9.3 + A + B) − (C + D)`, `A = (log₁₀ TDS − 1)/10`, `B = −13.12 log₁₀(T_K) + 34.55`, `C = log₁₀[Ca²⁺ as CaCO₃] − 0.4`, `D = log₁₀[alkalinity as CaCO₃]` (https://www.astm.org/Standards/D3739.htm). Compute it **on the concentrate**, not the feed. Above ~10,000 mg/L TDS switch to Stiff & Davis (S&DSI), which carries an ionic-strength term. Modern phosphonate/polymer antiscalants allow stable operation at LSI +1.8 to +2.5 in the concentrate (American Water Chemicals, https://www.membranechemicals.com/water-treatment/langelier-saturation-index-lsi/). For sulfates (CaSO₄, BaSO₄, SrSO₄) and silica, use saturation ratios from Pitzer/OLI speciation rather than an index. LSI is a thermodynamic tendency, not a rate — kinetics (induction time, residence time in the tail element) must be modeled separately or learned.

---

## 8. Ultrafiltration: resistance, blocking laws, critical flux

### 8.1 Darcy + resistance-in-series

$$J = \frac{\Delta P_{TM}}{\mu\,(R_m + R_{cp} + R_{ad} + R_{pp} + R_c + R_{irr})}$$

Cake resistance from cake-filtration theory: `R_c = α_c · m_c/A` with the specific cake resistance from Carman–Kozeny,

$$\alpha_c = \frac{180(1-\varepsilon)}{\rho_p d_p^2 \varepsilon^3}, \qquad J = \frac{\varepsilon^3}{k_0 S^2 (1-\varepsilon)^2}\cdot\frac{\Delta P}{\mu L}$$

For compressible cakes `α_c = α_0 ΔP^n` with n ∈ [0.3, 1.0] fitted from stepped-pressure tests. Reviews: Membranes 9(2), 2019 (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6409801/) and the UF flux-prediction review, Membranes 11(5), 2021 (https://pmc.ncbi.nlm.nih.gov/articles/PMC8158366/).

### 8.2 Hermia blocking laws

Unified constant-pressure law: `d²t/dV² = k (dt/dV)^n`, equivalently `dJ/dt = −K J^{3−n}`. Integrated forms (Iritani & Katagiri, KONA 33, 2016, https://www.jstage.jst.go.jp/article/kona/33/0/33_2016024/_html/-char/en):

| Mechanism | n | J(t) form | Linearized |
|---|---|---|---|
| Complete blocking | 2 | `J = J₀ exp(−K_b t)` | `ln J` vs `t` |
| Standard blocking | 1.5 | `J = J₀(1 − K_s² V)²` | `J^{-1/2}` vs `t` |
| Intermediate blocking | 1 | `J = J₀ exp(−K_i V)` | `J^{-1}` vs `t` |
| Cake filtration | 0 | `J = J₀/√(1 + 2K_c J₀² t)` | `J^{-2}` vs `t` |

Constant-flux (the operating mode of every municipal UF plant) duals, in terms of TMP `p`: complete `p₀/p = 1 − K_br J₀ V`; standard `(p₀/p)^0.5 = 1 − K_s² V`; intermediate `ln(p/p₀) = K_i V`; cake `p/p₀ = 1 + K_c J₀ V`. The cake form — TMP linear in cumulative specific volume — is the workhorse for UF cycle models.

**Extended Hermia model (EHM)** (Membranes, 2023, https://pmc.ncbi.nlm.nih.gov/articles/PMC10056723) lets `n` be continuous via `P = 2 − n`: `(J/J₀)^P ≈ 1/(1 + k t)` for P ≠ 0 and `J/J₀ ≈ exp(−k t)` for P = 0, with half-life `t½ = (0.5^P − 1)/k`. Across six datasets (UF pretreatment, ceramic MF of corn syrup, crossflow UF of oily effluent, ASP-flooding wastewater, BSA, nanoparticle CMP wastewater) EHM RMSE was 0.0101–0.0682 versus 0.0287–0.1108 for the best classical mechanism; fitted P ranged 1.25–9.67, with P > 2 indicating mechanisms outside Hermia's four. **This is the cleanest place to insert a learned parameter into a UF twin: keep the functional form, let ML predict `k` and `P` from feedwater state.**

Field et al. (1995) extended the laws to crossflow by subtracting a removal term, `−dJ/dt = k (J − J*) J^{2−n}`, where `J*` is the critical/limiting flux.

### 8.3 Critical, threshold and boundary flux

Definitions matter because plant setpoints are chosen against them (Field & Pearce 2011, https://www.sciencedirect.com/science/article/abs/pii/S0001868611000078; boundary-flux synthesis, Membranes 4(1), 2014, https://pmc.ncbi.nlm.nih.gov/articles/PMC3925542/):

- **Critical flux**: `dm/dt = 0` for `J ≤ J_c`; `dm/dt = B(J − J_c)` above.
- **Threshold flux**: `dm/dt = a` (constant, non-zero) below `J_th`; `a + b(J − J_th)` above.
- **Boundary flux** (unifying): `dm/dt = −α` for `J ≤ J_b`; `−α + β(J − J_b)` above, with α [L h⁻² m⁻² bar⁻¹] the sub-boundary fouling rate and β [h⁻¹ m⁻² bar⁻¹] the super-boundary index.

Measured by flux- or pressure-stepping (e.g. ΔP = 1 bar steps with reproducibility checks). A useful parametric closure is `J_b(KP, t) = m₀P_b − α t P_b − [m₀p₁ − α p₁ t + m₁P_b]KP + m₁p₁KP²` where `KP` is a pollutant-concentration key parameter — again a natural target for a learned mapping from raw-water quality.

### 8.4 UF plant cycle model

State: TMP under constant flux. Cycle: filtration (20–60 min) → backwash (30–60 s) → periodic CEB → CIP. Net water production per cycle:

$$\mathrm{NWP} = \frac{J\,t_f - J_{bw}\,t_{bw} - V_{CEB}/A}{t_f + t_{bw} + t_{idle}}$$

Backwash effectiveness is the key learned quantity: reported specific flux recovery of **55 % after flow-direction reversal vs 53 % for chemically assisted backwash + reversal** at low chemical dose. Optimal-control formulations for backwash switching maximize NWP over a horizon (OSTI, https://www.osti.gov/pages/biblio/2329273). Energy: dead-end UF at 0.4 bar with 15-min backwash interval and 30 s backwash duration gave the highest net flux (**27 LMH**) and lowest SEC (**146 Wh/m³**) (*J. Membrane Sci.* 2011, https://www.sciencedirect.com/science/article/abs/pii/S0376738811005011).

---

## 9. Energy: SEC, thermodynamic minimum, ERDs

Thermodynamic minimum work of separation at recovery `Y`:

$$W_{min} = \frac{RT}{V_w}\int_0^{Y}\ln\!\frac{a_w^{feed}(y)}{a_w^{perm}}\,dy \quad\Rightarrow\quad \mathrm{SEC}_{min} \approx 1.07\ \mathrm{kWh/m^3}\ \text{at }35{,}000\ \mathrm{ppm},\ Y=50\%$$

(Lin & Elimelech 2015; see also *J. Chem. Educ.* 98, 2021, https://pubs.acs.org/doi/10.1021/acs.jchemed.0c01194.) At the thermodynamic-restriction limit (feed pressure exactly equal to brine osmotic pressure) the classical closed forms are (Membranes 12(4), 2022, https://pmc.ncbi.nlm.nih.gov/articles/PMC9030420/):

$$\mathrm{SEC}_{RO} = \frac{\pi_{sw}R_t}{\eta_p\,Y(1-Y)},\qquad \mathrm{SEC}_{RO\text{-}ERD} = \frac{\pi_{sw}R_t\big[1-\eta_{PX}(1-Y)\big]}{\eta_p\,Y(1-Y)}$$

Numerical results at 50 % recovery: RO 2.28 kWh/m³; RO+PRO 1.47; RO+MD 1.75; RO-MD-PRO 0.67. RO-ERD minimizes at **1.97 kWh/m³ at Y = 30 %**. Zhu, Christofides & Cohen (I&EC Res. 48, 2009; https://pubs.acs.org/doi/10.1021/ie9012826) formalized SEC minimization as a constrained NLP in dimensionless variables for single-stage, two-stage and ERD configurations, showing the interior optimum in `Y` created by the thermodynamic restriction.

Reality check numbers:
- Practical SWRO: **2.5–4.0 kWh/m³** for the RO block; **3.5–4.5 kWh/m³** plant-wide with pre/post-treatment (*Desalination* 459, 2019, https://www.sciencedirect.com/science/article/abs/pii/S030626191931339X). HPP efficiency 88.5–90 % at 100,000 m³/d scale.
- BWRO: **0.36–1.51 kWh/m³**; ~0.5 kWh/m³ at 2 g/L, 28 °C; **16 % SEC reduction** achievable by operating-point optimization at constant permeate rate (*Energy* 2024, https://www.sciencedirect.com/science/article/pii/S004896972402919X).
- Isobaric ERDs: PX pressure exchangers up to **98–99 % peak efficiency**, up to 83 bar (Energy Recovery Inc., https://energyrecovery.com/px-technology/); >35,000 units installed, ~36 Mm³/d, ~$6 bn/yr energy cost avoided.
- Record: DESALRO 2.0 in the Canary Islands achieved **1.861 kWh/m³** in May 2024 with positive-displacement pumps (>90 % efficiency) plus isobaric ERD, on trains of 5,000–10,000 m³/d; Danfoss estimates retrofitting all plants above 2.0 kWh/m³ would save 247 TWh and €34.5 bn (https://www.danfoss.com/en/about-danfoss/articles/hpp/a-new-world-record-in-swro-energy-efficiency-underscores-the-enormous-potential-of-updating-existing-desalination-plants-with-best-in-class-technology/). Retrofit is "practically always" economic above 2.5–3 kWh/m³.
- ERD retrofit payback ≈ **1.3 years** in a reported case; optimized operating schedules have delivered **11.7 % energy gain / ~$126,000 per year** and 15 % energy + 12 % CO₂ reductions in control-optimization case studies.

---

## 10. Which parameters are fitted from plant data

| Parameter | Physical? | How obtained | Drift |
|---|---|---|---|
| `A` (water permeability) | intrinsic | NLS on normalized flux vs NDP; or online estimation | −30 % over 4 yr |
| `B` (salt permeability) | not truly intrinsic | NLS on permeate TDS; better: `P`, `C` of SF-AA | +70 % over 4 yr |
| `k` (mass transfer) | correlation | fitted jointly with A,B, or from Sh correlation | changes with spacer fouling |
| `f`, `d_h` | geometry | Δp data per stage | Δp rises with biofouling |
| `R_f` fouling resistance | lumped | inverted from normalized flux | the ML target |
| `α_c`, `n` (cake) | UF | stepped-pressure tests | feed-dependent |
| `J_b`, `α`, `β` | UF | flux/pressure stepping | feed-dependent |
| `η_pump`, `η_ERD` | equipment | pump curves + energy meters | slow |

The canonical identification experiment (Journal of Membrane Science, 2023, https://www.sciencedirect.com/science/article/abs/pii/S0376738823003423) fits `A`, `B`, `k` **simultaneously** by non-linear regression of measured stage water and salt fluxes onto the transport equations — important because `B` and `k` are strongly correlated when only `c_p` is observed; fitting `B` with `k` fixed from a literature Sherwood correlation biases `B` high. A data-driven variant of the same task is given in *J. Water Process Eng.* 2024 (https://www.sciencedirect.com/science/article/pii/S2214714424008663).

For **online** tracking, extended and unscented Kalman filters are the standard soft-sensor: state = `[R_m, B, friction coefficient]`, measurement = permeate conductivity, permeate flow, reject pressure. Reported behaviour: good noise rejection and peak detection, with estimation error growing monotonically as measurement noise goes from 10 % to 50 % (https://www.sciencedirect.com/science/article/pii/S1944398624169949). A patented plant-side version periodically re-estimates membrane transport parameters by minimizing the error between measured and predicted permeate conductivity, flow and reject pressure.

---

## 11. Embedding physics in ML: the actual architectures

**Taxonomy** (von Stosch et al., *Comput. Chem. Eng.* 60, 2014, https://www.sciencedirect.com/science/article/abs/pii/S0098135413002639):

- **Serial**: ML predicts an unknown *parameter* of the mechanistic model, which then produces the output. `NN: (features) → R_f(t)` → SD model → `J_w, c_p`. Best interpretability; accuracy capped by the white-box model's fidelity.
- **Parallel / residual**: mechanistic model predicts, ML learns the residual. `ŷ = f_phys(x; θ) + g_ML(x)`. Robust when the physics is structurally right but biased.
- **Physics-constrained loss (PINN)**: `L = L_data + λ_1 L_PDE + λ_2 L_BC + λ_3 L_monotonicity`, enforcing e.g. `J_w = A(T)(ΔP − Δπ)` and `∂(rejection)/∂T < 0` as soft constraints.

**Reference implementations with numbers:**

- **Serial hybrid, full-scale RO** — Gaublomme et al., *Desalination* 2023 (https://www.sciencedirect.com/science/article/abs/pii/S0011916423003880): mechanistic SD model (CP, osmotic pressure, solute transport) + **RNN-LSTM** predicting membrane resistance as a fouling proxy; inputs = feed properties, recovery setpoint, CIP events; `A`, `B` and feed-spacer channel height made functions of the learned fouling state. Outperformed the pure SD model over a **2.5-month prediction horizon** on the full-scale Farys/Tereos Aalst installation.
- **PINN for SWRO monitoring** — *Water* 17(3):297, 2025 (https://doi.org/10.3390/w17030297): PINN estimating permeate TDS and pressure drop from operating conditions with temperature-dependent permeability and progressive fouling embedded; validated on months of full-scale SWRO data with **R² = 0.96 (permeate TDS)** and **R² = 0.97 (transmembrane Δp)**; retained physical plausibility during feedwater excursions and post-CIP recovery where conventional ML produced non-physical predictions.
- **Ensemble ML on normalized features** — holistic RO framework, *Desalination* 2024 (https://www.sciencedirect.com/science/article/abs/pii/S0011916423008858): **XGBoost R² = 94.75, RMSE = 0.181**, with recursive feature elimination + SHAP identifying membrane age, feed temperature, feed pressure, feed flow and chloride as the five dominant predictors — i.e. the model rediscovers the normalization variables of ASTM D4516, a good sanity check that the physics features are the right features.
- **Spatio-temporal deep learning, full-scale ZLD** — ES&T 2025 (https://pubs.acs.org/doi/10.1021/acs.est.5c06257): **ConvLSTM R² = 0.960 (1-day) and 0.942 (7-day)** RO performance forecasts.
- **Dynamic CFD-based fouling twin** — Membranes 11(5):349, 2021 (https://pmc.ncbi.nlm.nih.gov/articles/PMC8151604/): coupled Navier–Stokes + advection–diffusion + surface adsorption `∂C_s/∂t = K₁(C_s,max − C_s)C_b − K₂C_s`, with two flux-reduction closures. Effective-pressure-drop closure beat resistance-in-series: **4.51 % vs 10.78 % flux error** (Δp error ~12 % for both), calibrating only one parameter (`A_p` = 3600 or `A_k` = 0.067) on one geometry and validating on four others. Implemented in OpenFOAM ("SUMs" solver), ≥15 cells across the narrowest throat.
- **Control** — ML-MPC on closed-circuit RO projected **~6 % integrated SEC reduction** (https://www.sciencedirect.com/science/article/abs/pii/S0263876225004435); MPC for CCRO with 3-hour filtration-phase forecasts and online recalibration (IWA *Water Supply* 25(4), 2025, https://iwaponline.com/ws/article/25/4/727/107850/Closing-the-loop-model-predictive-control-for-a). RL for CIP scheduling (Shim et al. 2025, https://www.sciencedirect.com/science/article/abs/pii/S0011916425006691) achieved **16.13 % operating-cost reduction and 139.53 % more RO operating time**; multi-agent QMIX/VDN beat single-agent baselines on two-stage RO SEC (https://doi.org/10.1016/j.desal.2025.118870); CNN-SAC beat DDPG/PPO/TD3 on renewable-powered RO (https://doi.org/10.1016/j.apenergy.2022.119184). No RL agent yet runs autonomously in a production desalination plant — all results are digital-twin simulations (https://smartwatermagazine.com/news/smart-water-magazine/when-plant-learns-run-itself-reinforcement-learning-agents-desalination).
- **Field status** — a 2025 review of **147 water-sector digital-twin studies (2015–May 2025)** found publications growing from 1 (2015) to 41 (2024), **58/147 (40 %) using ML**, but only **4 studies on desalination** (https://www.mdpi.com/2073-4441/17/20/2957; OSTI copy https://www.osti.gov/servlets/purl/3001751). AI-driven MPC inside DT platforms has reported **18–25 % energy savings** at pilot facilities in the US, Netherlands and Singapore. A membrane-specific critical review of hybrid models, digital twins and digital shadows is at https://www.sciencedirect.com/science/article/pii/S2772823426000096.

---

## Implementation notes

**Data you need (minimum viable twin).** Per stage, at ≥5-minute resolution: feed/permeate/concentrate flow, feed and interstage pressure, permeate pressure, feed and permeate conductivity (and ideally full ion panel monthly), temperature, pH, ORP, dosing rates (antiscalant, acid, SBS), CIP/CEB event log with chemistry and duration, membrane install dates. For UF: TMP, flux, backwash/CEB timestamps and volumes, feed turbidity/UVA254/TOC, SDI or MFI when available. Twelve months minimum to capture seasonal temperature swings; the published hybrid models trained on multi-month to multi-year records (2.5-month horizons; 27,000 h datasets).

**Build order.**
1. Implement the normalization layer first (ASTM D4516 + TCF). Nothing downstream is trustworthy until normalized flow and normalized salt passage are stable on clean-membrane periods. Validate by confirming that normalized permeate flow is flat across a diurnal temperature cycle.
2. Implement osmotic pressure: van 't Hoff/ASTM for BWRO, a Pitzer routine (PHREEQC with the Pitzer database, `pyEQL`, or Reaktoro) for SWRO/ZLD and for all saturation indices. Expect ~9 % osmotic-pressure error if you skip activities.
3. Implement the element ODEs with 100–300 axial segments per vessel, closed with the CFD-fitted `M_CP` and `f` correlations (§4.2) if spacer geometry is known, else Schock & Miquel. Integrate with `scipy.integrate.solve_ivp` (stiff-capable, e.g. `Radau`) or hand-rolled marching with pressure-flow iteration per segment.
4. Fit `A`, `B`, `k` jointly by non-linear least squares (`scipy.optimize.least_squares`, `trf` with bounds) on clean-membrane windows; report parameter covariance and check the `B`–`k` correlation. Prefer SF-AA `(A, P, C)` if you have multi-salinity data.
5. Add the fouling state: `A(t) = A₀·φ(t)`, `B(t) = B₀·ψ(t)`, `d_h(t)` shrinking with cake growth. Estimate `φ, ψ` online with an EKF/UKF (`filterpy`, or a hand-written UKF — the state is 3–5 dimensional).
6. Only then train ML: serial hybrid (NN → fouling state → physics) or residual. Use XGBoost/LightGBM for tabular baselines, LSTM/ConvLSTM or a temporal fusion transformer for sequences, and SHAP for feature attribution. Expect R² 0.93–0.97 on TDS/Δp targets as the state of the art; anything above that on a naive split is leakage — split by time, never randomly, and hold out at least one CIP cycle.
7. Close the loop with optimization: NLP for steady-state setpoints (`CasADi` + IPOPT), MPC for dynamic operation, or RL only if you already have a validated twin. Realistic prizes: 6 % iSEC via ML-MPC, 16 % SEC via BWRO operating-point tuning, 16 % opex via RL-scheduled CIP.

**Math/software stack.** Python: NumPy/SciPy, CasADi (algorithmic differentiation + IPOPT), PHREEQC/`phreeqpython` or Reaktoro (Pitzer speciation, LSI/S&DSI, saturation ratios), `filterpy` (EKF/UKF), PyTorch (PINN with autograd-based residual terms), scikit-learn/XGBoost, `pySINDy` if you want to discover the fouling ODE. For CFD closure generation: OpenFOAM (the SUMs approach) or COMSOL, meshing ≥15 cells across the spacer throat; a 228-case DOE is enough to fit a `M_CP`/`f` surrogate to <1 % MAPE.

**Traps.**
- Fitting `B` as a constant across salinities — use SF-AA or refit per salinity band.
- Applying one TCF to both water and salt flux.
- Using arithmetic instead of log-mean feed-brine concentration at high recovery.
- Computing LSI on the feed rather than the concentrate.
- Ignoring the mass-transfer correlation's leverage: correlation choice alone moves SEC predictions by up to 1.6 kWh/m³ and Δp by 83 %.
- Random train/test splits on time-series plant data.
- Treating SDI as a model input without temperature/pressure correction — prefer MFI or UMFI.

**Validation targets to hold yourself to.** Normalized permeate flow reproduced within ±3 % over a clean cycle; permeate TDS R² ≥ 0.95 on a held-out month; stage Δp within ±10 %; SEC within ±0.1 kWh/m³ of metered; fouling-onset location predicted within ~1 m of the observed autopsy evidence along the vessel.
