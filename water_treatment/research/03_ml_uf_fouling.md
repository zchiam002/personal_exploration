# Machine Learning for Ultrafiltration Fouling Prediction and Cleaning Optimization — State of the Art (2021–2026)

Research synthesis, 2026-08-01. Scope: data-driven and hybrid models for low-pressure membrane processes — pressurized/submerged UF and MF for drinking water, water reuse and SWRO pretreatment, plus the much larger MBR fouling literature and what transfers from it. Covers TMP/permeability forecasting, fouling-mode classification, backwash timing and duration optimization, CEB/CIP scheduling, coagulant dose optimization as a fouling-control lever, integrity monitoring/anomaly detection, and image-based fouling characterization.

---

## 1. The physical substrate: what the model is actually predicting

Unlike RO (solution-diffusion), low-pressure membranes are pore-flow devices and the entire fouling problem reduces to a time-varying hydraulic resistance. Darcy's law for the permeate flux $J$ [L·m⁻²·h⁻¹, "LMH"]:

$$J = \frac{\Delta P_{TM}}{\mu(T)\,R_t}, \qquad R_t = R_m + R_c + R_{if} + R_{cp}$$

where $\Delta P_{TM}$ = transmembrane pressure [Pa], $\mu(T)$ = permeate dynamic viscosity, $R_m$ = clean-membrane resistance, $R_c$ = hydraulically reversible cake resistance, $R_{if}$ = irreversible (chemically-removable) resistance, $R_{cp}$ = concentration polarization / gel layer. Permeability (specific flux) is

$$L_p = \frac{J}{\Delta P_{TM}} \quad [\mathrm{LMH\,bar^{-1}}], \qquad L_{p,20} = L_p\cdot\frac{\mu(T)}{\mu(20^\circ\mathrm{C})} \approx L_p\cdot 1.03^{(20-T)}$$

**Temperature normalization is non-negotiable and is the single most common failure in published UF ML work.** Water viscosity changes ~2–3 %/°C; a model trained on raw TMP in a plant with 5–25 °C seasonal swing will spend most of its capacity learning the viscosity curve rather than fouling. The KAUST/ACS ES&T Engineering monitoring study explicitly uses *temperature-corrected permeability* as its monitored variable rather than raw TMP (Wolfand et al., ACS ES&T Engineering 4(6):1492, 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11184555/), and the arXiv prognostics work derives membrane resistance "from TMP and flux via Darcy's law with temperature correction" before building any health index (Explainable Similarity-Based Prognostics for UF Membranes, 2026, https://arxiv.org/html/2602.00659).

**Reversible/irreversible decomposition.** Because UF runs in cycles (filter → backwash → filter), each cycle yields a *free* labelled decomposition without any extra instrumentation:

$$R_{rev}^{(k)} = R_{end}^{(k)} - R_{PB}^{(k)}, \qquad \Delta R_{irr}^{(k)} = R_{PB}^{(k)} - R_{PB}^{(k-1)}$$

where $R_{PB}$ is post-backwash resistance. The cycle-to-cycle increment $\Delta R_{irr}$ is the correct ML target for anything to do with chemical cleaning; $R_{rev}$ within a cycle is the target for backwash optimization. Backwash efficiency $\eta_{BW} = (R_{end}-R_{PB})/(R_{end}-R_m)$ is the natural classification/regression label. "Impaired performance caused by reversible fouling can be recovered through hydraulic backwashing; irreversible fouling induced by foulants bonded to the membrane surface and trapped in pores can be eliminated only by chemical cleaning" — the standard operational definition (per the ES&T UF-materials ML study, Zhang et al., 2023, https://pmc.ncbi.nlm.nih.gov/articles/PMC10666290/).

**Hermia blocking laws** remain the mechanistic backbone for constant-pressure dead-end filtration:

$$\frac{d^2 t}{dV^2} = k\left(\frac{dt}{dV}\right)^{n}$$

with $n=2$ complete pore blocking, $n=1.5$ standard blocking (pore constriction), $n=1$ intermediate blocking, $n=0$ cake filtration. The known weakness: "the main drawback of the Hermia model is that it does not consider the possibility that these mechanisms occur simultaneously in the same process" (Generalization and Expansion of the Hermia Model, Membranes/PMC, 2023, https://pmc.ncbi.nlm.nih.gov/articles/PMC10056723/). This is precisely the gap that physics-informed ML now fills (§4.3). A fractional-calculus alternative that identifies the mechanism in one step without stage-splitting was published in Scientific Reports (2025, https://www.nature.com/articles/s41598-025-33755-4).

**Fouling potential indices.** MFI-UF (modified fouling index, UF version) and SDI are the standard feedwater-side fouling-potential measurements and are the usual ML *targets* when the goal is a soft sensor for feed quality rather than a TMP forecast. Algal organic matter (AOM) shows the highest MFI-UF among organic matter classes, and transparent exopolymer particles (TEP) — sticky acid-polysaccharide gels produced during blooms — are the dominant contributor (see §9).

---

## 2. TMP and permeability forecasting

### 2.1 Seminal ANN work (the field's anchor)

The field starts with **Delgrange et al. (1998)**, "Neural networks for prediction of ultrafiltration transmembrane pressure — application to drinking water production," *J. Membrane Science* (https://www.sciencedirect.com/science/article/abs/pii/S0376738898002178), followed by **Delgrange-Vincent et al. (2000)**, "Neural networks for long term prediction of fouling and backwash efficiency in ultrafiltration for drinking water production," *Desalination* 131(1–3):353–362, and "Neural networks: a tool to improve UF plant productivity," *Desalination* (2002, https://www.sciencedirect.com/science/article/abs/pii/S0011916402004162). Delgrange applied a recurrent network to the time evolution of TMP on a UF drinking-water pilot; three network structures were tested and the architecture chosen by minimizing the train–test gap. Inputs: feed temperature, feed turbidity, permeate flow rate, and — the key insight still worth copying — **feed resistance before backwashing**, which enabled the model to predict resistance in organic-containing water "even without providing information about the nature of the organic matter" (as summarized in the ANN fouling review, Membranes 13(7):685, 2023, https://pmc.ncbi.nlm.nih.gov/articles/PMC10383311/). Feeding the previous cycle's end-of-filtration resistance as a state variable is the cheapest way to give a static regressor memory.

### 2.2 Tabular ensembles — the strong default

Random forests and gradient boosting dominate current tabular UF/MBR work and routinely beat MLPs:

- **Kovacs et al. (2022)**, "Membrane fouling prediction and uncertainty analysis using machine learning: a wastewater treatment plant case study," *J. Membrane Science* 660 (https://www.sciencedirect.com/science/article/abs/pii/S0376738822005622). RF, ANN and LSTM predict TMP at **various stages of the MBR production cycle** (i.e., separate models per cycle phase — filtration, relaxation, backpulse — rather than one model for the whole sawtooth, which is the correct decomposition). Model uncertainty quantified over hyperparameter tuning and variance of extreme predictions. **RF best on accuracy** across all cycle stages.
- **Textile-wastewater MBR (KAUST, *J. Water Process Eng.*, 2025)**, https://www.sciencedirect.com/science/article/pii/S1944398625002541: Lasso, SVM and RF on synthetic textile wastewater with critical sludge parameters as features. **RF: R² = 0.95 (train) / 0.86 (test), RMSE = 1.75 kPa / 3.3 kPa.** The train–test gap here is honest and typical.
- **AnMBR fouling factor identification (*J. Membrane Science*, 2023)**, https://www.sciencedirect.com/science/article/abs/pii/S0376738823007329: ANN optimal topology **14-9-6-1**; RF hyperparameters **n_trees = 1200, n_features = 14**. SHAP + permutation importance ranked **SMPp/SMPc (0.281) > EPSp/EPSc (0.110) > organic loading rate (0.106)**. **RF R² = 0.906, MSE = 0.061; ANN R² = 0.800, MSE = 0.118.** This is the cleanest published evidence that the *ratio* of protein to carbohydrate in soluble microbial products / EPS is the dominant biological fouling driver — a feature you can only get from lab assays, which is the practical catch.
- **Full-scale MBR with AI-driven feature engineering + XAI (*Processes* 13(8):2352, 2025)**, https://www.mdpi.com/2227-9717/13/8/2352: food-processing wastewater MBR; target refined to **specific flux (flux/TMP)** rather than raw TMP — a genuinely important modelling choice. **CatBoost best, R² = 0.8374**; SHAP identified **F/M ratio and MLSS** as most influential.
- **Domestic-wastewater MBR (Nguyen et al., *Water Environment Research*, 2025)**, https://onlinelibrary.wiley.com/doi/10.1002/wer.70205: linear regression, SVR and decision-tree regression on water-quality descriptors; **decision tree R² = 0.99**. Treat that number with suspicion — a single unpruned tree hitting 0.99 on autocorrelated time-series data is the classic signature of a random row-wise split leaking near-duplicate adjacent timesteps into the test set (§11).

### 2.3 Sequence models: LSTM/GRU and the stationarity problem

TMP in a cycling UF plant is a sawtooth on a rising trend — strongly non-stationary with a deterministic periodic component. Naively fitting an LSTM to raw TMP mostly learns the sawtooth.

**AI-driven multivariate TMP forecasting, stationarity-aware (*J. Water Process Eng.*, 2025)**, https://www.sciencedirect.com/science/article/pii/S2214714425016125: the framework pairs autoregressive LSTM and GRU with explicit **Augmented Dickey–Fuller stationarity diagnostics and first-order differencing**, reporting that differencing "improves model stability and reduces autocorrelation in raw data," and enables **long-horizon TMP prediction from short-sequence operational inputs**, validated on independent plant data with variable fouling and operating conditions. Final **GRU predictor R² = 0.890**. This is the single most directly transferable recipe for a pressurized UF plant: difference the series, model $\Delta$TMP, integrate back for the forecast.

**Multicycle forecasting.** "Forecasting multicycle hollow fiber ultrafiltration fouling using time series analysis" (2023, https://www.researchgate.net/publication/376122556_Forecasting_multicycle_hollow_fiber_ultrafiltration_fouling_using_time_series_analysis) frames the problem at the correct granularity — per-cycle summary statistics (end-of-cycle TMP, post-backwash TMP, cycle-average flux) as the time series, rather than raw 1-Hz signals. This collapses the sawtooth and typically reduces the sequence length by 2–3 orders of magnitude.

**Soft sensors for permeability (MBR lineage).** The MBR literature developed a deep line of recurrent/fuzzy soft sensors, summarized in "Recent Advances in the Prediction of Fouling in Membrane Bioreactors" (Membranes/PMC, 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC8225185/):
- **Elman recurrent network** on a pilot MBR: inputs TMP, dTMP/dt, backwash TMP, filtration/backwash cycle lengths, SRT, TSS, temperature, aerobic-zone oxygen decay rate. Over TMP rising 0→40 kPa, **average deviation 2.7 %**.
- **GA-RBF (Tang et al., 2016)**: PCA reduction identified MLSS, operating pressure and temperature as key factors; GA-optimized RBF beat plain RBF on convergence speed and accuracy.
- **Recurrent RBF soft sensor (Han et al., 2017)**: PLS variable screening; fast gradient descent on centre $c(t)$, width $\sigma(t)$, output weight $w(t)$, feedback weight $u(t)$: $c(t+1)=c(t)-\eta_1\phi_c(t)w(t)e(t)$, $\sigma(t+1)=\sigma(t)-\eta_2\phi_\sigma(t)w(t)e(t)$.
- **Multi-step fuzzy NN with improved Levenberg–Marquardt (Han et al., 2019)**: a time-difference update $Z(t+1)=Z(t)+\alpha(G(t)-Z(t))$ suppresses error accumulation in iterated multi-step forecasts — the standard remedy for recursive-forecast drift.
- **ANFIS vs ANN on osmotic MBR (Hosseinzadeh et al., 2020)**: inputs MLSS, EC, DO. **ANFIS R² = 0.9755 (TFC) / 0.9861 (CTA), RMSE 0.2527 / 0.1230; ANN R² = 0.9404 / 0.9817, RMSE 0.4049 / 0.1449.**
- **Tent-SSA-BP (Wang et al., *Membranes*, 2022)**, https://pmc.ncbi.nlm.nih.gov/articles/PMC9318055/: tent chaotic map initialization + Sparrow Search Algorithm optimizing a **6-12-1** BP network. Inputs after PCA: TSS, MLSS, total resistance, TMP, SRT, water-production pressure. **592 samples (500 train / 92 test)**, PVDF hollow-fibre MF. Reported **97.4 % accuracy vs 48.52 % for plain BP**; MAPE 0.0009, RMSE 0.0226, MAE 0.0226; robustness 91–94 % accuracy at 4–12 dB SNR. Note the data come from a spreadsheet simulation model, not a plant — metaheuristic-tuned BP results on simulated data should not be taken as plant-achievable.

### 2.4 Attention, graph and long-sequence models

- **DMGTNet (*J. Membrane Science*, 2025)**, https://www.sciencedirect.com/science/article/abs/pii/S0376738825009615: graph-temporal coupling for fouling prediction in **dual-membrane** wastewater systems; a graph attention mechanism "adaptively identifies key sensors and their spatial dependencies." The right architecture when you have $N$ parallel membrane racks/trains sharing a common feed — the graph encodes rack-to-rack coupling that per-rack models miss.
- **Long-sequence time-series forecasting (LSTF) for RO CIP scheduling (*Desalination*, 2025)**, https://www.sciencedirect.com/science/article/abs/pii/S0011916425006691: an **attention-based (Informer-family) forecaster reached R² = 0.82 vs R² = 0.65 for a 1D-CNN+LSTM hybrid** on the same industrial RO data — a rare clean head-to-head showing attention's advantage specifically at long horizons. Directly transferable to UF CEB/CIP horizon forecasting.
- Transformer penetration into water treatment remains thin: "the application of transformer-based models to water treatment plants remains limited compared with other industrial domains" (dual-level feature attention transformer for chemical dosing, *J. Cleaner Production*, 2026, https://www.sciencedirect.com/science/article/abs/pii/S0959652626008115).

### 2.5 Full-scale deployed forecasters

**MBR-Net (Environ. Sci. Technol., 2025)**, https://pubs.acs.org/doi/10.1021/acs.est.4c12835 (PubMed 40043194) is the reference implementation for a plant-facing fouling forecaster. Built from full-scale WWTP data with bespoke denoising and training strategies, it predicts **one-day-ahead change in irreversible fouling** under different desired fluxes, cleaning conditions and feedwater conditions, with **MAPE < 6.45 %, MAE < 3.71 LMH·bar⁻¹, R² > 0.87 on two independent test sets**. Three design choices worth stealing: (i) target = *irreversible* fouling rate, not TMP; (ii) cleaning conditions and desired flux are model *inputs*, making it counterfactual/actionable rather than merely predictive; (iii) explicit denoising stage ahead of training, acknowledging that plant sensor data is noisy enough to dominate the fouling signal.

---

## 3. Fouling classification and diagnosis

### 3.1 Reversible vs irreversible

The most operationally useful classification is binary on backwash efficacy. **"Modeling UF fouling and backwash in seawater RO feedwater treatment using neural networks with evolutionary algorithm and Bayesian binary classification," *Desalination* (2021)**, https://www.sciencedirect.com/science/article/abs/pii/S0011916421002009, is the key paper: an **ensemble back-propagation NN optimized by an adaptive evolutionary algorithm (AEA)** models UF resistance progression **during both filtration and backwash**, trained on **4 years of operation of an integrated UF–RO seawater plant**, with a **Bayesian binary classifier** deciding backwash success/failure. Modelling the backwash leg explicitly — not just the filtration leg — is what makes the model usable for scheduling.

"High recovery from backwash cycles indicates effective hydraulic cleaning, while diminishing recovery over successive cycles signals transition from reversible to irreversible fouling" — the standard label-generation rule.

### 3.2 Fouling-type attribution (organic / bio / colloidal / scaling)

There is **no published supervised classifier that labels UF fouling by chemical type from routine online data alone**; this is a genuine gap. What exists is attribution via feature importance on models whose inputs include type-diagnostic measurements:
- SHAP on AnMBR data ranks SMPp/SMPc and EPSp/EPSc top (biofouling/organic signature) — *J. Membr. Sci.* 2023, above.
- SHAP on full-scale MBR ranks F/M ratio and MLSS (biological/cake signature) — *Processes* 2025, above.
- Classical diagnostics remain the ground truth: SDI and turbidity for colloidal potential; declining salt rejection alongside flux for bio/organic; lead-element localization for bio/colloidal vs tail-element for scaling.

The practical construction is therefore a **weak-label pipeline**: derive labels from physics (Hermia exponent $n$ fitted per cycle, $\eta_{BW}$, response to acid CEB vs caustic/hypochlorite CEB) and train a classifier on online features to reproduce them. Response to CEB chemistry is itself a near-perfect label generator — permeability recovery after citric/oxalic acid implicates inorganic/metal-oxide fouling; recovery after NaOCl implicates organic/biofouling.

### 3.3 Mechanism identification via physics-informed ML

**A physics-informed neural network for interpretable membrane-fouling prediction with adaptive transitions between fouling mechanisms (*Separation and Purification Technology*, 2026)**, https://www.sciencedirect.com/science/article/pii/S1383586626007781, embeds all four Hermia mechanisms in one physically constrained model. Mechanics: **adaptive sigmoid weighting functions** give smooth continuous transitions between filtration stages; a **probabilistic loss balancing data fidelity, physical constraints and initial conditions through adaptive weights**; the model **estimates stage transition times and quantifies mechanism weights**, so the relative contribution of each mechanism is learned rather than prescribed. Trained on multiple flux-decline datasets across operating conditions and foulant types, it beat purely data-driven models and was notably more robust **under data-scarce conditions**, with learned mechanism coefficients varying systematically with operating conditions. This is the current best answer to "which mechanism is running right now," and the data-scarcity robustness is the practical selling point for a single plant with limited history.

A complementary **mechanism-informed** (not physics-constrained) approach: **"Flux decline prediction in dead-end ultrafiltration combining fluorescence spectroscopy and mechanism-informed machine learning," *ACS ES&T Water* (2024)**, https://pubs.acs.org/doi/abs/10.1021/acsestwater.4c00473 (preprint: https://chemrxiv.org/engage/chemrxiv/article-details/66d5998acec5d6c142dfd5f0). A semi-empirical Hermia model is *empowered* by an SVM whose inputs are **initial flux, organic load, and three pre-selected combinations of excitation–emission fluorescence (EEM) spectra**. Validation on new experiments: **R² = 0.87–0.99, average 0.95.** The architecture — ML predicts the *parameters* of a mechanistic model rather than the output directly — is the most sample-efficient hybrid available and should be the default when you have <10⁴ samples. Online EEM/fluorescence probes are commercially available, so the feature set is deployable.

---

## 4. Backwash timing and duration optimization

### 4.1 The optimization problem

Net water production per membrane area over a cycle of filtration time $t_f$ and backwash time $t_b$:

$$V_{net}(t_f,t_b) = \frac{\int_0^{t_f} J(t)\,dt - J_{bw} t_b}{t_f + t_b}$$

with $J(t)$ declining per the fouling law. Backwash too often and you waste permeate and pumping energy; too rarely and $R_{irr}$ ratchets up, forcing CEB/CIP. The decision variables are backwash **interval** (or TMP trigger), **duration**, **flux**, and CEB **frequency**.

### 4.2 Stochastic dynamic programming on a learned model

**Zhang, Kotsalis, Khan, Xiong, Igou, Lan & Chen (Georgia Tech, *J. Membrane Science* 612, 2020)**, "Backwash sequence optimization of a pilot-scale ultrafiltration membrane system using data-driven modeling for parameter forecasting," https://www.sciencedirect.com/science/article/abs/pii/S0376738820310413. Pilot UF treating **spent filter backwash water** at a water treatment plant. ML (linear regression vs ANN vs random forest, compared head-to-head) learns the mapping from environmental variables and dynamic parameters to (a) **foulant removal efficiency of the backwash** and (b) **foulant accumulation rate**. That learned model becomes the transition function for **stochastic dynamic programming** over backwash timing. Result: the optimized schedule achieved **more efficient operation at lower cost and with lower membrane resistance than the experimental fixed-interval sequence**. The authors note the method "has great potential to intelligently schedule backwash timing on large scale ultrafiltration applications to improve energy consumption and lengthen membrane life." This is the canonical learn-a-model-then-optimize architecture for UF backwash and the one to replicate first.

### 4.3 Optimal control (Pontryagin) with online parameter identification

**"Evaluation of the Genericity of an Adaptive Optimal Control Approach to Optimize Membrane Filtration Systems" (Membranes/PMC, 2025)**, https://pmc.ncbi.nlm.nih.gov/articles/PMC12195455/ — the strongest quantitative energy result in the literature. Cake-deposition fouling model: attachment during filtration $\dot m = \delta Q_{out}(C_{Xi}X_i + C_{Si}S_i)$, exponential detachment during backwash/relaxation. Objective: minimize permeate-pump energy per m³ produced. **Pontryagin's Maximum Principle** yields a singular control giving an **optimal fouling mass $\bar m$** and the corresponding filtration/backwash duration ratio; the algorithm recomputes it after every cycle from real-time parameter identification (closed-loop adaptive). Validated experimentally on two systems:
- **Hollow-fibre microfiltration: 4–9 % energy saving** vs conventional fixed-cycle operation.
- **Flat-sheet ultrafiltration: 28–31 % energy reduction** (larger because relaxation carries a lower energy penalty than backwashing).
- Overall **7–30 % energy consumption reduction**, extended membrane lifespan via delayed chemical cleaning, robust to MLSS and EPS input disturbances.

Related earlier work: "Optimal control of physical backwash strategy — towards the enhancement of membrane filtration process performance," *J. Membrane Science* (2018), https://www.sciencedirect.com/science/article/abs/pii/S0376738817319166; and "Advanced process control for ultrafiltration membrane water treatment system," *J. Cleaner Production* (2018), https://www.sciencedirect.com/science/article/abs/pii/S0959652618300830.

### 4.4 Empirical response-surface optimization at engineering scale

**"Analysis of backwash settings to maximize net water production in an engineering-scale ultrafiltration system for water reuse" (OSTI/DOE, 2023)**, https://www.osti.gov/pages/biblio/2329273. Engineering-scale UF on reclaimed wastewater. **TMP trigger varied 62–145 kPa; optimum 103 kPa giving maximum net water production of 63 m³/day at ~92 % recovery.** Backwash durations of **45, 65 and 85 s performed essentially identically** (~63 m³/day, ~91 % recovery) — a strong, actionable negative result: duration is a weak lever, trigger threshold is the strong one. CEB frequency reduced from 1 per 3 physical backwashes to 1/6 and 1/12 **decreased recovery**, and "the total number of CEBs remained approximately constant regardless of their frequency" — i.e., you cannot cheat CEB demand by stretching the schedule; the membrane simply demands them sooner. Any RL agent that discovers "skip CEBs" as a reward hack is exploiting a model that lacks this constraint.

A complementary response-surface study on seawater UF spanning **backwash interval 30–90 min, backwash flow rate 10–34 L·min⁻¹, backwash duration 15–45 s** likewise concluded "fouling is mainly controlled by backwash interval" (*Membrane Science and Research*, https://www.msrjournal.com/article_27309.html).

### 4.5 Deep reinforcement learning

**"Deep reinforcement learning in an ultrafiltration system: optimizing operating pressure and chemical cleaning conditions," *Chemosphere* (2022)**, https://www.sciencedirect.com/science/article/abs/pii/S0045653522028570. An **LSTM surrogate of the UF system serves as the RL environment**; the agent controls **three actions — operating pressure, cleaning time, and cleaning concentration** — driving the system toward higher water productivity and operating efficiency by varying pressure and cleaning conditions over time. This LSTM-as-environment pattern is the only practical way to do RL here: you cannot train on a real plant, and no calibrated first-principles simulator of UF fouling exists that is accurate enough over long horizons. Related: multi-agent RL for autonomous two-stage RO (*Desalination*, 2025, https://www.sciencedirect.com/science/article/abs/pii/S0011916425003455).

---

## 5. CEB and CIP scheduling

### 5.1 Forecast-then-optimize for cleaning scenarios

**Optimizing membrane cleaning strategy of industrial RO using long-sequence time-series forecasting (*Desalination*, 2025)**, https://www.sciencedirect.com/science/article/abs/pii/S0011916425006691. LSTF models forecast the pressure trajectory far enough ahead to evaluate CIP scenarios; the optimizer searches over the number of CIPs and the pressure threshold at which each is triggered. Result: **performing CIP twice at the highest pressure threshold studied decreased RO operating cost by 16.13 % while increasing operating time by 139.53 %** relative to the incumbent strategy. Attention model R² = 0.82 vs 0.65 for CNN-LSTM. The methodology maps one-for-one onto UF: forecast normalized permeability, enumerate {CEB interval, CEB chemistry, CIP threshold} scenarios, cost them out, pick the minimum.

### 5.2 What is actually on the table: the chemical-savings ceiling

**"Chemical-Saving Potential for Membrane Bioreactor (MBR) Processes Based on Long-Term Pilot Trials" (*Membranes*/PMC, 2024)**, https://pmc.ncbi.nlm.nih.gov/articles/PMC11205864/ — the best quantified target for any cleaning-optimization project. Pilot supporting the Henriksdal WWTP (Stockholm, 1.6 M p.e.).

*Baseline design protocol:* maintenance cleaning (MC) by CEB **twice weekly with NaOCl and once weekly with citric acid**; recovery cleaning (RC) twice per year with each chemical. Backpulse flux held constant at **20 LMH for MC and 34 LMH for RC**. Permeability floor 200 LMH·bar⁻¹; operating flux 18–30 LMH.

*Doses:* NaOCl **200 mg/L (MC) / 1100 mg/L (RC)**; citric acid **2000 / 2200 mg/L**; oxalic acid **1300 / 1500 mg/L**.

*Results:*
| Mode | MC chemical | RC | Total saving |
|---|---|---|---|
| Optimized design | −20 % | 1 RC/yr instead of 2 (−50 %) | ~25–30 % |
| **Demand-driven** | oxalic 32 %, citric 48 %, NaOCl 24 % of design consumption | — | **up to 75 %** |

Membranes ran **92 days with no NaOCl maintenance cleaning**, permeability drifting to 121–394 LMH·bar⁻¹ across tanks before recovery cleaning restored function; demand-driven mode maintained similar average permeability to the design protocol despite the 75 % chemical cut.

*Economics for full-scale Henriksdal:* design (citric + NaOCl) **14.02 M SEK/yr**; optimized design **10.08 M SEK/yr (−28 %)**; demand-driven with oxalic **3.48 M SEK/yr (−75 %)** — roughly **10.5 M SEK/yr saved**. Environmental: **−95 % global warming potential (750 t CO₂eq/yr), −82 % abiotic depletion, −93 % eutrophication, −87 % photochemical ozone creation**. Reduced cleaning intervals also cut membrane downtime, raising capacity and recovery.

The headline for an ML business case: **demand-driven (condition-based) cleaning is worth ~70–75 % of chemical spend versus a fixed calendar schedule.** ML's job is to supply the "demand" signal reliably enough that operators will trust skipping a scheduled clean.

### 5.3 CEB chemistry selection

NaClO was identified as the best-performing reagent for alleviating hydraulically irreversible fouling among NaClO, NaCl, NaOH, sodium citrate and combinations in surface-water CEB work ("Membrane Fouling Alleviation by Chemically Enhanced Backwashing in Treating Algae-Containing Surface Water: From Bench-Scale to Full-Scale Application," *Engineering*, 2021, https://www.sciencedirect.com/science/article/pii/S2095809921001624). Ozone-CEB for ceramic membranes in cyanobacteria-laden water: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7558929/. For seawater UF, CEB-only (no continuous coagulant) has been demonstrated as a complete fouling-control strategy (UBC thesis, https://open.library.ubc.ca/collections/24/items/1.0362864). A model that recommends *which* CEB chemistry, not just when, needs the acid-vs-oxidant response labels described in §3.2.

---

## 6. Coagulant dose optimization in pretreatment

Coagulation is the highest-leverage UF fouling control knob and the area with the most credible published savings.

### 6.1 Jar-test replacement with ANNs

**Optimum coagulant forecasting by modelling jar test experiments using ANNs (*Drinking Water Engineering and Science* 11:1, 2018)**, https://dwes.copernicus.org/articles/11/1/2018/ — open access, fully specified, and the right template for a small plant. Two MLPs, MATLAB NN toolbox:
- **Model 1 (forward)**: inputs turbidity, alkalinity, temperature, pH, coagulant dose → outputs treated turbidity, temperature, alkalinity, pH. **1 hidden layer, 15 neurons.**
- **Model 2 (inverse)**: inputs raw-water quality + *desired* treated-water characteristics → output optimal coagulant dose. **1 hidden layer, 16 neurons.**

**112 data points over 2 years**, 80/10/10 split, z-score normalization. Results: alkalinity R² = 0.94 (MSE 26.31 mg/L), pH R² = 0.85 (0.01 units), turbidity error 0.011 NTU, temperature 0.67 °C; residual aluminium R² = 0.93 (0.37 mg/L). The **forward-model-plus-inverse-model pairing** is the correct structure — it lets you set a target and solve for dose, rather than just imitating operator behaviour. A virtual jar test returns a dose in **under a minute versus ~30 minutes** for the lab test.

Other dose models: hybrid ELM optimized by Bat algorithm (*Environ. Sci. Pollut. Res.*, 2023, https://link.springer.com/article/10.1007/s11356-023-27224-6); ML comparison in *Environ. Dev. Sustain.* (2022, https://link.springer.com/article/10.1007/s10668-022-02835-0); polynomial regression with Lasso regularization (*Processes* 13:3829, 2025, https://doi.org/10.3390/pr13123829); similarity-score-based piecewise ML (*J. Environ. Eng.* 151(6), 2025, https://ascelibrary.org/doi/abs/10.1061/JOEEDU.EEENG-7969).

### 6.2 Large-scale deep learning with reported cash savings

**"Optimizing coagulant dosage using deep learning models with large-scale data," *Chemosphere* (2023)**, https://www.sciencedirect.com/science/article/abs/pii/S0045653523032599. **Conv1D + GRU hybrid** trained on **minute-by-minute monitoring data over five years** — described as the first drinking-water process model built on a continuous minute-resolution five-year dataset. The model predicts coagulant dose and sedimentation-basin turbidity, is validated against a physicochemical model, then used to optimize dose two ways: (i) hold sedimentation turbidity below the 1.0 NTU guideline, (ii) analyse turbidity response to 5–20 % dose reductions. Reported outcome: **~22 % coagulant dosage reduction, ≈21 million KRW/year**. A follow-up targets extreme events specifically (https://www.researchgate.net/publication/383635783_Deep_learning-based_coagulant_dosage_prediction_for_extreme_events_leveraging_large-scale_data).

**GAMTF — graph attention multivariate time-series forecasting (*Water Research*, 2023)**, https://www.sciencedirect.com/science/article/abs/pii/S0043135423001008, **with official open-source code at https://github.com/cbhua/coagulant-forecast**. Simultaneously predicts coagulant dose and settled-water turbidity by modelling "hidden interrelationships between features and the past states." Data: **2011–2021**, minute-resolution PPM and TOC series. **GAMTF: R² = 0.94, RMSE = 3.55, versus baselines (MLR, LSTM, GRU, CNN-LSTM, LSTM-Attention) at R² 0.63–0.89, RMSE 4.80–38.98.** Built on PyTorch + PyTorch Lightning with YAML hyperparameter configs and W&B logging; pretrained checkpoints included. **This is the single best starting codebase in the whole domain** — clone it first.

**Ensemble-learning framework (*Journal of Environmental Management*, Oct 2025)**, https://www.sciencedirect.com/science/article/pii/S001393512502482X (PubMed 41161365). Tree ensembles for coagulant dosing: **RF-ExtraTrees best — RMSE 0.515, MAE 0.329, NSE 0.9850, Willmott index 0.996, KGE 0.969, R² 0.985**; plain RF RMSE 0.807, MAE 0.586, NSE 0.963, R² 0.963. Reporting NSE/KGE/WI alongside R² is good practice worth copying — KGE in particular exposes variance and bias errors that R² hides.

### 6.3 Closed-loop coagulant control tied to UF resistance

**"Self-adaptive cycle-to-cycle control of in-line coagulant dosing in ultrafiltration for pre-treatment of reverse osmosis feed water," *Desalination* (2016/2017)**, https://www.sciencedirect.com/science/article/abs/pii/S0011916416311870 (see also AIChE 2016 paper 454b, https://proceedings.aiche.org/conferences/aiche-annual-meeting/2016/proceeding/paper/454b-optimization-uf-backwash-real-time-control-coagulant-dosing). Implemented on a **pilot UF–RO seawater plant**. The controller tracks UF resistance during **both filtration and backwash** and adjusts in-line coagulant dose to minimize the incremental cycle-to-cycle **post-backwash resistance** change; real-time tracking of resistance metrics and of $\partial(\Delta R_{PB})/\partial(\text{dose})$ lets it quantify irreversible fouling progression and backwash effectiveness simultaneously. Field result: **coagulant dose reduced by up to ~29 %** relative to operation without real-time optimization, while maintaining robust UF operation through both mild and severe feedwater degradation. It also established the mechanism that any ML dose model must respect: **increased coagulant dose promotes faster cake formation but improves backwash efficiency** — dose trades reversible fouling rate against irreversible fouling accumulation, so the objective is not "minimize fouling rate."

Non-ML but essential context on the optimum: a pilot study found an optimized **PACl dose of 0.5 mg/L produced 65 % less irreversible UF fouling than 6 mg/L** — i.e., the fouling-optimal dose can be an order of magnitude below the turbidity-optimal dose. Operating-cost analysis of in-line coagulation/UF for irreversible fouling control: *Water* 10(8):1076 (2018), https://www.mdpi.com/2073-4441/10/8/1076. Earlier control-system work: "Development of a control system for in-line coagulation in an ultrafiltration process," *J. Membrane Science* (2007), https://www.sciencedirect.com/science/article/abs/pii/S0376738807003766.

### 6.4 Streaming current and UV254 as ML features

Streaming current detectors/monitors (SCD/SCM) give continuous **feedback** on charge neutralization; UV254 gives **feedforward** information on incoming NOM (Real Tech, https://realtechwater.com/blog-post/coagulation-optimization-using-streaming-current-detectors-and-uv254-analyzers/; Pi StreamerSense, https://www.processinstruments.net/products/streaming-current-monitor/). Combining computer coagulation models with an SCD for chemical feed control predates ML (PubMed 23787322, https://pubmed.ncbi.nlm.nih.gov/23787322/). The modern pattern — ML on real-time sensor data predicting **clarified-water turbidity 15 minutes ahead** with MLP vs LSTM vs GRU compared — makes SCD reading, UV254, raw turbidity, pH, temperature and dose the standard feature vector. For UF fouling specifically, add **UV254 and TOC removal across the clarifier** as engineered features: NOM breakthrough, not turbidity breakthrough, drives irreversible UF fouling.

### 6.5 Reinforcement learning for dosing

A reinforcement-learning decision-support system for coagulant *and* disinfectant dosage selection at DWTPs was published in *Water Supply* 24(1):86 (2024), https://iwaponline.com/ws/article/24/1/86/99400/Reinforcement-learning-based-DSS-for-coagulant-and. Explainable integrated time-series deep learning for dose regulation: *Process Safety and Environmental Protection* (2025), https://www.sciencedirect.com/science/article/abs/pii/S0957582025008808.

---

## 7. Integrity monitoring and anomaly detection

### 7.1 Multivariate statistical process control — the deployable baseline

**Wolfand et al., "Long-Term Statistical Process Monitoring of an Ultrafiltration Water Treatment Process," *ACS ES&T Engineering* 4(6):1492 (2024)**, https://pmc.ncbi.nlm.nih.gov/articles/PMC11184555/ — the most implementation-ready paper in this section, and unusual in evaluating over >1 year rather than a short case study.

*System:* Pure Water Demonstration Facility, Calabasas CA; three independent UF modules, dead-end, ~40 gfd, 95 % target recovery, indirect potable reuse after tertiary treatment.

*Method:* **AD-PCA** (adaptive-dynamic PCA). Dynamic = augment the matrix with, for each variable, **the lag with the highest partial autocorrelation** in the training period (doubles the columns). Adaptive = rolling window. **Adaptive lasso** chosen for detrending over kNN, random forest and XGBoost because it is "computationally fast, interpretable, and simple" and avoided the overfitting seen with forest methods.

*Variables (14 total):* monitored — filtrate turbidity, filtrate ammonia, temperature-corrected permeability; explanatory/detrending — feed turbidity, temperature, filtrate pH, ORP, total chlorine, conductivity, TOC, backwash flow, flux.

*Sampling/data:* **15-minute averages**, 2 April 2021 – 25 May 2022 (~13 months). Training windows of 848 and 1052 observations. **Model retrained after every 96 in-control observations (24 h).**

*Tuning (the three parameters that matter):* rejection threshold α ∈ {0.005, 0.05}; rolling window ∈ {2 d, 12 d}; consecutive exceedances required ∈ {1, 5}. **Optimum: 12-day window, α = 0.005, 5 consecutive exceedances.**

*Performance:* T² exceedance rate **25.9 % during known in-control periods vs 75.8 % during known fault periods** (SPE: 1.4 % vs 7.3 %). Beat adaptive univariate Shewhart charts, which mis-flagged in-control ammonia periods. Conclusion: "multivariate monitoring produces substantial benefits in long-term testing compared to industry standards of simpler, univariate monitoring or **daily pressure decay tests**," and detects faults substantially faster. Tuning is process-specific but "only needs to be done once, prior to initial usage."

The honest reading of 25.9 % false-exceedance is that MSPC alone is not a silent alarm system — it is a prioritization signal for operator review.

### 7.2 Detecting membrane damage from permeate quality

**"Deep learning with data preprocessing methods for water quality prediction in ultrafiltration," *J. Cleaner Production* (2023)**, https://www.sciencedirect.com/science/article/abs/pii/S0959652623033759. One month of data from a UF train in a real SWRO plant. Conventional CNN and LSTM **failed to predict sudden turbidity spikes caused by UF membrane damage (R² < 0.2351)**; the fix was **coupling wavelet-decomposed signals with raw data** as model input. This is the key negative result for integrity monitoring: fibre breakage is a rare, high-frequency, non-stationary event and standard sequence models trained on MSE will smooth it away. Wavelet decomposition (or any multiresolution basis) surfaces the transient. Spectral approaches to breakage detection have been reported at **96.8–97.4 % accuracy** (per the AI/ML fouling review, Al-Kathiri & Rao, *J. Environ. Earth Sci.*, 2025, https://journals.bilpubgroup.com/index.php/jees/article/view/8630).

Conventional integrity context: pressure/vacuum decay tests per **ASTM D3923-23 and D6908-06**; a single broken fibre (1 % breakage in a pilot module) was detectable by UV254 spectroscopy, plate counting and qPCR alongside pressure decay, and magnetic-susceptibility permeate monitoring detected it instantaneously at feed concentrations as low as 1.2 ppm (hollow-fibre NF integrity evaluation, PMC, 2023, https://pmc.ncbi.nlm.nih.gov/articles/PMC10714397/).

### 7.3 Remaining useful life with interpretable prognostics

**"Predictive Maintenance for Ultrafiltration Membranes Using Explainable Similarity-Based Prognostics" (arXiv, 2026)**, https://arxiv.org/html/2602.00659 — notable for using only four sensors and producing operator-readable rules.

*Data:* **Port Hueneme, California SWRO pretreatment facility; 422 days; 12,528 operational cycles across 373 independent runs**; 80/20 split (9833 cycles/298 runs train; 2668/75 test); 24 process variables available.

*Features:* TMP, flux $J$, membrane resistance $R_m$ (Darcy + temperature correction), recovery $Re$ = max−min TMP within a cycle. Composite health index:
$$HI = 0.30(1-R_m^*) + 0.25(1-TMP^*) + 0.30\,J^* + 0.15\,Rec^*$$
with $^*$ = per-run min-max normalization; HI ∈ [0 failed, 1 healthy].

*Pipeline:* backwash-cycle detection by a **15 gpm threshold on backwash flow**; run segmentation on HI jumps >0.5 or 24-hour gaps; **20-cycle sliding window**; three Gaussian membership functions (Low/Medium/High) per feature with centres HI ∈ {0.0, 0.5, 1.0} and dHI ∈ {−1, 0, 1}, giving a **120-dim fuzzy signature** (20 cycles × 2 features × 3 MFs). Retrieval by fuzzy Jaccard index $S(\tilde A,\tilde B)=\sum\min(\mu_a,\mu_b)/(\sum\max(\mu_a,\mu_b)+\epsilon)$; **top-k = 10** neighbours treated as zero-order TSK rules; $\widehat{RUL} = \sum S_i r_i / \sum S_i$.

*Results:* **MAE 4.08 cycles, RMSE 6.28 cycles**; 80 % prediction-interval coverage 68.6 %. By horizon: 0–5 cycles MAE 6.11; **6–15 cycles MAE 3.67 (best)**; 30+ cycles MAE 9.28. Mean cycle 121 s, so MAE ≈ 8.2 minutes; usable warning 20–30 cycles (~40–60 min) ahead, max horizon 93 cycles (~3.1 h). Deployable with **four hydraulic sensors only**.

Every prediction traces to specific historical cases with similarity weights and emits IF-THEN rules ("IF HI is Very High AND dHI is Medium THEN RUL = 11 cycles") — the explainability property that gets an operator to act.

---

## 8. MBR fouling ML and what transfers to pressurized UF

The MBR literature is 5–10× larger than the pressurized-UF literature (publication growth ~22.7 %/yr since 2010 per the Membranes/PMC review, 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC8225185/). Reviews: *Journal of Environmental Management* (2025, https://www.sciencedirect.com/science/article/abs/pii/S0301479725009545); XAI and digital-twin applications in wastewater MBRs (*Membranes* 16(5):181, 2026, https://doi.org/10.3390/membranes16050181); Bagheri et al. critical review of AI/ML for advanced fouling control (*Chem. Eng. Res. Des.*, 2019, https://www.sciencedirect.com/science/article/abs/pii/S0957582018310863).

**What transfers cleanly:**
1. **Target engineering** — specific flux / normalized permeability instead of raw TMP; per-cycle-phase models; irreversible-fouling increment as the cleaning target. (Kovacs 2022; *Processes* 2025; MBR-Net 2025.)
2. **Sequence architectures and their pathologies** — sawtooth non-stationarity, recursive-forecast drift and the TD correction, the differencing recipe.
3. **XAI workflow** — SHAP on tree ensembles to convert a predictor into an actionable lever list, now near-universal.
4. **Uncertainty quantification** over hyperparameters and extreme predictions (Kovacs 2022).
5. **Cleaning-economics framing** and demand-driven cleaning (Henriksdal, §5.2).
6. **Resistance decomposition as a diagnostic control matrix.** "Development of a dual-metric operational decision-support model for full-scale submerged MBRs," *Water Research* (2026), https://www.sciencedirect.com/science/article/pii/S004313542600117X: a year of full-scale data; integrates a **hydrodynamic index $H$** with **back-pulsing resistance $R_{BP}$ and cake resistance $R_{cake}$**; identifies two thresholds — $H_{Target}$ (sustainable capacity / onset of accelerated fouling) and $H_{Lim}$ (absolute operational limit) — and two fouling pathways (A: $R_{BP}$-initiated cyclical degradation; B: $R_{cake}$-dominant). Produces a **9-state control matrix** collapsed to a practical action matrix. Explicitly framed as "physics-informed, data-driven methodology expected to bridge the gap between field operations and future machine-learning-based control policies." This resistance-component state machine is directly portable to pressurized UF, where $R_{BP}$ ↔ backwash-recoverable and $R_{cake}$ ↔ within-cycle cake.

**What does not transfer:**
- **Biological features** (MLSS, F/M, SRT, SMP, EPS, DO, sludge viscosity) — the strongest MBR predictors by SHAP — have **no analogue in pressurized UF on surface water or seawater**. A UF model's feature space is instead feed turbidity, UV254/TOC/DOC, temperature, algal indicators, coagulant dose, and hydraulic history. Do not expect MBR feature-importance rankings to hold.
- **Air scour** is the dominant MBR fouling-control and energy lever (membrane aeration is **35–50 % of MBR operating cost**); pressurized UF has no equivalent. Air-scour control based on permeability evolution achieved **14 % average and 22 % maximum reduction in membrane aeration energy (0.025 and 0.04 kWh/m³)** at full scale (*Water Research*, 2015, https://www.sciencedirect.com/science/article/abs/pii/S0043135415002237); fuzzy-logic dual-phase control of air scour and permeate flow suggested up to 50 % air-scour reduction in simulation, moderated on empirical validation (*J. Water Process Eng.*, 2024, https://www.sciencedirect.com/science/article/abs/pii/S2214714424012248). Useful as an analogue for backwash-intensity optimization, not as a transferable model.
- **Flux ranges and timescales** differ by ~3×; MBR fouling episodes evolve over days–weeks, pressurized UF cycles over 20–60 minutes. Sequence lengths, sampling rates and forecast horizons must be re-chosen.

---

## 9. Seawater RO pretreatment UF: algal blooms and TEP

**Operational modelling.** Two studies define the state of the art:
- **Ensemble BPNN + AEA with Bayesian binary classification (*Desalination*, 2021)**, https://www.sciencedirect.com/science/article/abs/pii/S0011916421002009: **4 years** of integrated UF–RO seawater operation; models UF resistance during filtration *and* backwash plus backwash efficiency; good accuracy on time-series data displaying "temporal variability of UF performance in response to varying UF feedwater quality."
- **Real-time monitoring and predictive modelling of UF pretreatment (*J. Water Process Eng.*, 2025)**, https://www.sciencedirect.com/science/article/pii/S1944398625004023: **426 days** of operational data; **Tree Regression, Ensemble Learning, Neural Networks and Gaussian Process Regression** trained to predict **UF flow rate and membrane resistance in real time**. **ENS best: R² = 0.99, RMSE = 3.08 L/min**; TR R² = 0.99, RMSE = 3.27 L/min. That both tree methods beat NN and GPR on ~14 months of plant data is the expected result for tabular hydraulics.

**TEP and algal blooms — the physics the model must see.** During blooms, algae produce TEP, sticky acid-polysaccharide gels that are the primary irreversible-fouling agent for UF and the primary biofouling precursor for downstream RO. Key findings: colloidal TEP (c-TEP) is more abundant than particulate TEP (p-TEP) in both fresh and seawater, with higher concentrations in seawater and strong spring seasonality; **MF/UF with in-line coagulation removes only 70–75 % of TEP**, and the residual — mostly c-TEP — passes to the RO and drives organic/biological fouling; a positive relationship exists between feedwater TEP and RO biofouling rate (Villacorte et al. and colleagues; see "The fate of TEP in seawater UF-RO system: a pilot plant study in Zeeland, The Netherlands," https://www.academia.edu/22252258/, "Characterisation of transparent exopolymer particles (TEP) produced during algal bloom: a membrane treatment perspective," https://www.academia.edu/22252184/, and AMTA, "Irreversible Fouling of Ultrafiltration Membranes Caused by TEP in Seawater UF-RO Treatment," https://amtaorg.com/digital-library/irreversible-fouling-of-ultrafiltration-membranes-caused-by-transparent-exoplymer-particles-tep-in-seawater-uf-ro-treatment/). AOM has the highest MFI-UF among organic-matter classes; ceramic-UF comparison of algal, bacterial and humic organics in SWRO pretreatment: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9965402/.

**Consequence for feature design:** turbidity is nearly useless as a bloom-fouling predictor. The informative features are **chlorophyll-a, TEP (particulate + colloidal), AOM/biopolymer fraction by LC-OCD, UV254/SUVA, algal cell counts, SDI and MFI-UF**. Most of these are offline, which is exactly the gap that spectral soft sensors fill.

**Spectral soft sensors for bloom fouling potential.** "Advancing harmful algal bloom detection with hyperspectral imaging: correlation of algal organic matter and fouling indices based on deep learning" (*Desalination*, 2024), https://www.sciencedirect.com/science/article/abs/pii/S0011916424012165: hyperspectral imaging plus **CNN and random forest** to predict fouling indicators, with fouling-related AOM data comprising **SDI, MFI, TOC, TEP and algae density**; band-importance extraction identified **~600 nm as critical for chlorophyll content**; explicitly evaluated for real-time monitoring at SWRO plants during HAB events. Extended to **UAV-based hyperspectral mapping** of fouling-related water-quality indicators for SWRO during HABs (*Water Research*, 2026, https://www.sciencedirect.com/science/article/abs/pii/S0043135426007414). Broader algal-bloom ML: high-frequency in-situ data (*Toxins* 18(5):203, 2026, https://doi.org/10.3390/toxins18050203); *Water Quality Research Journal* 57(4):304 (2022), https://iwaponline.com/wqrj/article/57/4/304/91529/; review in *Critical Reviews in Environmental Science and Technology* (2023), https://www.tandfonline.com/doi/full/10.1080/10643389.2023.2285691.

Field fouling indicators for UF-as-pretreatment operational strategies: *Desalination* (2018), https://www.sciencedirect.com/science/article/abs/pii/S0011916417320301.

---

## 10. Image-based fouling characterization

**In-situ OCT + deep learning (the strongest results in the field).** Park et al., "Deep neural networks for modeling fouling growth and flux decline during NF/RO membrane filtration," *J. Membrane Science* (2019), https://www.sciencedirect.com/science/article/abs/pii/S0376738819301814: **13,708 high-resolution OCT fouling-layer images**; DNN+CNN inputs = initial fouling thickness, membrane type, time, initial permeate flux; the model reproduces 2D/3D organic-fouling growth images and predicts **fouling growth R² = 0.99, RMSE = 2.82 µm; flux decline R² = 0.99, RMSE = 0.30 LMH** (as tabulated in the ANN fouling review, *Membranes* 13(7):685, 2023, https://pmc.ncbi.nlm.nih.gov/articles/PMC10383311/). Shim et al. paired an **LSTM-RNN** with OCT thickness (inputs: operation time, pressure, initial permeate flux, DOC, OCT fouling-layer thickness): **flux R² = 0.9982, layer thickness R² = 0.9987**. Real-time FO fouling monitoring with a deep learning model: *Chemosphere* (2021), https://www.sciencedirect.com/science/article/abs/pii/S0045653521005166. Quantitative OCT characterization of MF fouling with optimized image analysis: *Membranes* 16(2):50 (2026), https://pmc.ncbi.nlm.nih.gov/articles/PMC12943706/. Foundational OCT method papers: *Environ. Sci. Technol.* (2015, https://pubs.acs.org/doi/10.1021/es503326y; 2016 3D method, https://pubs.acs.org/doi/10.1021/acs.est.6b00418).

**Planar camera images → biofilm thickness (cheapest useful imaging).** "Precise biofilm thickness prediction in SWRO desalination from planar camera images by DNN models," *npj Clean Water* (2025), https://www.nature.com/articles/s41545-025-00451-9: CNN models compute cross-sectional biofilm thickness from membrane-surface images; **CNN-Class predicted fouling classification at 90 % accuracy; CNN-Reg predicted average biofilm thickness with mean difference ±24 %.** Because it needs only a planar camera rather than an OCT head, this is the realistic route to instrumenting a membrane-fouling simulator or a sacrificial canary module on a plant.

**Membrane autopsy / SEM.** Despite frequent claims, there is **no substantial published corpus of CNNs trained on UF membrane-autopsy SEM images for foulant classification** — a real gap. The adjacent evidence is that patch-based CNNs on FIB-SEM micrographs successfully detect multiple microstructural features (PMC, 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12780081/) and that CNNs super-resolve SEM images from low-resolution acquisitions, reducing charging and beam damage — so the technique is ready; the labelled dataset is what is missing. RO membrane autopsy plus ANN for inorganic-fouling prediction: *Eng* 6(5):98 (2025), https://doi.org/10.3390/eng6050098.

**Membrane materials / structure ML (adjacent but useful for feature intuition).** Zhang et al., "Understanding and Designing a High-Performance Ultrafiltration Membrane Using Machine Learning," *Environ. Sci. Technol.* (2023), https://pmc.ncbi.nlm.nih.gov/articles/PMC10666290/: **XGBoost and CatBoost on 320 literature records** of flat-sheet polymeric UF membranes made by NIPS; **21 features** (11 fabrication — polymer content/type as molecular fingerprints, pore-maker content and MW, additive loading and type, solvent, coagulant; 6 operational — TMP, contaminant MW and concentration, foulant concentration; 4 membrane properties — mean pore radius, porosity, contact angle, roughness). Bayesian hyperparameter optimization with 5-fold CV. **Test R²: water permeability 0.83 (RMSE 68.24), removal 0.84 (6.60), flux decline ratio 0.78 (9.50), flux recovery ratio 0.62 (7.89), reversible fouling ratio 0.73 (10.33)**; predicted membrane properties: pore radius R² 0.87, contact angle 0.76, porosity 0.66. SHAP: additive wt % most significant (>1.0 wt % optimal), polymer wt % positive over 10–16 wt % and negative above 16 wt %.

**Protein fouling in MF/UF.** "Predictive modeling and insight into protein fouling in microfiltration and ultrafiltration through one-dimensional convolutional models," *Separation and Purification Technology* (2024/2025), https://www.sciencedirect.com/science/article/abs/pii/S1383586624019762: a **1D-CNN (ODCNN) with a staged training scheme that separates numerical and categorical feature fields**; **SMOTE plus Gaussian noise** verified as necessary for data expansion. **Flux R² = 0.833, protein rejection R² = 0.723.** See also *Ind. Eng. Chem. Res.* 62 (2023) on single-protein fouling ML, https://pubs.acs.org/doi/abs/10.1021/acs.iecr.3c00275, and Bayesian optimization for UF protein-purification process design, https://www.sciencedirect.com/science/article/abs/pii/S1383586625007191.

---

## 11. Commercial deployments and reported economics

- **Veolia Water Technologies — Hubgrade Performance Plant (formerly AQUAVISTA Plant)**, an online digital twin first installed 2007 at Agtrup WWTP, now on 100+ installations: reported performance gains up to **30 % of aeration energy, 100 % of chemicals, 40 % of biological treatment capacity, 100 % of hydraulic capacity** (https://www.veoliawatertechnologies.com/en/hubgrade-digital-solutions; whitepaper https://www.veoliawatertechnologies.com/sites/g/files/dvc2471/files/document/2024/08/WP%20All%20HUBGRADE%20Performance%20Plant%20White%20Paper%20EN.pdf). Nosedo WWTP (Milan): real-time optimization delivering **≈ EUR 400,000/yr operating-cost savings, 40–60 % reduction in precipitation chemicals (ferric chloride), 65–90 t/yr sludge reduction** (https://smartwatermagazine.com/news/veolia/aquavista-plant-digital-plant-solution-launched-veolia). Veolia's **Smart Membranes** is a cloud tool combining membrane process expertise and AI to evaluate membrane clogging status in real time for predictive maintenance.
- **Pani Energy** — digital twin + analytics on existing plant sensors, covering filtration, chemical dosing and maintenance programs, including forecasting optimal membrane cleaning timing so facilities "don't replace membranes too early or too late" (https://www.pani.global/desalination-use-case). Industry-typical claim range for AI in water treatment: **5–20 % off chemical, energy or membrane-replacement costs on the addressed processes** (https://aguato.com/resources/ai-water-treatment-applications). Treat vendor figures as upper bounds pending independent verification.

Cross-referencing the peer-reviewed numbers gives a defensible expectation band for a UF-focused project: **chemical (CEB/CIP) 25–75 %** (Henriksdal), **coagulant 20–30 %** (Chemosphere 2023; Desalination 2016), **backwash/permeate-pump energy 4–31 %** (Membranes 2025), **membrane-cleaning-driven operating cost ~16 % with >2× run-length extension** (Desalination 2025 RO CIP).

---

## 12. Failure modes to design against

1. **Row-wise random train/test splits on autocorrelated time series.** This is the single largest source of inflated published R² in this field. The RO literature has the canonical demonstration: random-split CV with near-duplicate experiments produces "falsely high accuracy" (Jeong et al., *Environ. Sci. Technol.* 55(16):11348, 2021, https://pubs.acs.org/doi/abs/10.1021/acs.est.1c04041). **Split by time block, by cycle, by run, or by train/rack — never by row.** A decision tree reporting R² = 0.99 on plant TMP is a leakage alarm, not a result.
2. **Not normalizing for temperature and flux before modelling.** The model learns viscosity and setpoint changes instead of fouling.
3. **Modelling raw TMP across the sawtooth.** Split by cycle phase (Kovacs 2022) or aggregate to per-cycle statistics.
4. **Ignoring rare events.** MSE-trained sequence models smooth away fibre breaks and bloom onsets (R² < 0.2351 in the *J. Cleaner Prod.* 2023 UF study). Use wavelet/multiresolution inputs, quantile or asymmetric losses, and separate anomaly detectors.
5. **Optimizers that hack the cleaning constraint.** The engineering-scale result that total CEB count is roughly invariant to scheduled frequency (OSTI 2023) must be encoded as a constraint or the agent will "save" chemicals that the membrane then demands anyway.
6. **Assuming the fouling-minimal coagulant dose is the turbidity-minimal dose.** It is not; it can be >10× lower.
7. **Lab-scale/simulated R² as a plant expectation.** Tent-SSA-BP's 97.4 % came from a spreadsheet simulation; MBR-Net's MAPE < 6.45 % came from a full-scale plant. Only the latter is a planning number.
8. **Point predictions with no uncertainty.** Cleaning decisions are asymmetric-cost; propagate uncertainty (Kovacs 2022) or use conformal/quantile intervals. Note even the well-built prognostics model achieved only 68.6 % empirical coverage on nominal 80 % intervals.

---

## Implementation notes

**Minimum viable data.** Ten tags at ≤1-minute resolution, historized for ≥6 months (12+ preferred to cover seasonality): feed pressure, permeate pressure (→ TMP), permeate flow (→ flux), backwash flow, feed temperature, feed turbidity, permeate turbidity, feed UV254 or TOC, coagulant dose, valve/mode state. Add pH and conductivity if available. Note that the published RUL system ran on **four hydraulic sensors** (TMP, flux, backwash flow, temperature) and the ACS ES&T Eng monitoring system on **14 tags at 15-minute averages** — you do not need a large instrument budget. Event logs for every backwash, CEB, CIP and integrity test, with chemistry and dose, are mandatory; without them there is no cleaning-response label. Reference dataset scales: 422 days / 12,528 cycles (arXiv 2026), 426 days (JWPE 2025), 4 years (Desalination 2021), 13 months at 15-min (ACS 2024), 5 and 10 years at 1-min for coagulation (Chemosphere 2023; Water Research 2023).

**Preprocessing pipeline (in order).** (1) Mode segmentation — split the stream into filtration / backwash / CEB / CIP / idle using valve states or a flow threshold (the arXiv work used 15 gpm on backwash flow). (2) Per-cycle feature extraction — $R_{start}$, $R_{end}$, $R_{PB}$, $\eta_{BW}$, cycle duration, permeate volume, mean flux, fitted Hermia $n$ and $k$. (3) Temperature-correct to 20 °C via $\mu(T)/\mu(20)$. (4) Detrend with adaptive lasso against explanatory tags if doing MSPC. (5) Stationarity check with ADF and first-difference if needed (JWPE 2025). (6) Chronological split — the last 20 % by time as the test set, plus a held-out independent run/train for true generalization.

**Model ladder, in build order.**
1. *Baseline:* per-cycle random forest / XGBoost predicting $\Delta R_{irr}^{(k+1)}$ and $\eta_{BW}^{(k+1)}$ from the last $m$ cycles of engineered features. 300–1000 trees, depth 4–8, lr 0.01–0.1, early stopping on a chronological validation block. Expect R² 0.8–0.95 on real plant data. SHAP for the lever list.
2. *Sequence:* GRU or LSTM on differenced per-cycle series for multi-day permeability horizons (JWPE 2025 recipe; GRU R² 0.890 as the realistic benchmark). Add attention only if you need horizons beyond a few days — the RO LSTF result (R² 0.82 attention vs 0.65 CNN-LSTM) is where attention pays.
3. *Hybrid:* Hermia-PINN with adaptive sigmoid stage weighting (SepPurTech 2026) when data are scarce, or ML-predicts-mechanistic-parameters (Hermia + SVM on fluorescence, ACS ES&T Water 2024, R² 0.87–0.99) when you have EEM/fluorescence.
4. *Optimization:* build the learned transition model first, then run **stochastic dynamic programming** over backwash timing (Georgia Tech, JMS 2020). For the analytic route, implement Pontryagin singular control on a cake-deposition model with per-cycle parameter re-identification (Membranes 2025; 4–9 % MF, 28–31 % UF energy). Reserve DRL for last and always train it against an LSTM surrogate environment (Chemosphere 2022), with hard constraints on minimum CEB frequency and maximum TMP.

**Objective function.** Optimize cost per m³ of net product, not TMP:
$$\min_{t_f,t_b,\,\tau_{CEB},\,C_{dose}} \; \frac{E_{pump} c_e + m_{chem} c_{chem} + \text{amortized membrane}}{V_{net}} \quad \text{s.t. } \Delta P_{TM}\le \Delta P_{max},\; \text{recovery}\ge R_{min},\; N_{CEB}\ge N_{min}$$
Recovery ~92 % and TMP trigger ~103 kPa are the empirical optima reported at engineering scale (OSTI 2023) and make good initialization/sanity bounds.

**Tools.** Python: scikit-learn, XGBoost/LightGBM/CatBoost, PyTorch + PyTorch Lightning, `shap`, `statsmodels` (ADF, PACF for DPCA lag selection), `PyWavelets` (rare-event features), `optuna` or `scikit-optimize` (Bayesian HPO with 5-fold CV, as in the ES&T UF-materials study), `mlflow`/W&B for tracking. For SDP/optimal control: `scipy.optimize`, `cvxpy`, or `gekko`/`CasADi` for the Pontryagin route; `Stable-Baselines3` for DRL. **Start from the GAMTF repository** (https://github.com/cbhua/coagulant-forecast) — it is the only official open-source codebase in this domain with pretrained checkpoints, YAML configs and multivariate water-treatment baselines (MLR/LSTM/GRU/CNN-LSTM/LSTM-Attention) already implemented; swap the coagulant target for TMP or $\Delta R_{irr}$. Much of the older literature is MATLAB (NN Toolbox, Levenberg–Marquardt, Bayesian regularization); reimplement rather than port.

**Validation protocol.** Chronological split plus at least one fully held-out independent operating period or parallel train (MBR-Net used **two independent test sets**). Report R², RMSE **in engineering units** (kPa, LMH·bar⁻¹, L/min), MAE and MAPE; add NSE/KGE/Willmott index (Journal of Environmental Management 2025) to expose bias and variance errors. Provide intervals — bootstrap ensembles, quantile regression or conformal prediction — and report empirical coverage, not just nominal.

**Instrumentation upgrades ranked by value per dollar.** (1) Online UV254 — the single best fouling-relevant addition for surface-water/seawater UF, since NOM not turbidity drives irreversible fouling. (2) Streaming current monitor for closed-loop coagulation feedback (UV254 gives the feedforward). (3) Online fluorescence/EEM — unlocks the Hermia+SVM hybrid at R² 0.87–0.99. (4) For SWRO with bloom exposure: TEP assay (particulate and colloidal separately), chlorophyll-a, and — if budget allows — a hyperspectral or multispectral feed camera to soft-sense SDI/MFI/TEP (Desalination 2024). (5) A planar camera on a sacrificial canary module gets you CNN-based biofilm classification at 90 % accuracy and thickness to ±24 % (npj Clean Water 2025) at a fraction of OCT cost.

**Sequencing the project.** Weeks 1–4: historian extraction, cycle segmentation, temperature normalization, per-cycle feature table — this alone usually reveals fouling-rate variability nobody had quantified. Weeks 5–8: RF/XGBoost baseline on $\Delta R_{irr}$ and $\eta_{BW}$ + SHAP; ship AD-PCA monitoring (12-day window, α = 0.005, 5 consecutive exceedances) as the first production artifact since it needs no labels. Weeks 9–16: GRU permeability forecaster on differenced per-cycle series; validate on a held-out season. Weeks 17–24: SDP or Pontryagin backwash scheduler in shadow mode against operator decisions; only then close the loop, starting with the highest-value, lowest-risk lever — CEB scheduling, where the Henriksdal trials show 25–75 % of chemical spend is genuinely addressable.
