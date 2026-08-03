# Machine Learning for RO Performance Modeling, Prediction, and Soft Sensing — State of the Art (2021–2026)

Research synthesis, 2026-08-01. Scope: data-driven and hybrid models of reverse osmosis (RO) plant performance — permeate flux, salt passage/rejection, permeate TDS/conductivity, differential pressure (DP), specific energy consumption (SEC) — plus fouling-trajectory forecasting, uncertainty quantification, membrane-materials ML, and remaining-useful-life (RUL)/replacement scheduling.

---

## 1. Physical baseline every ML model is built against

All credible RO ML work is anchored to the solution-diffusion (SD) model. Water and salt fluxes through the membrane:

$$J_w = A\,(\Delta P - \Delta\pi), \qquad J_s = B\,(c_m - c_p)$$

where $A$ [L·m⁻²·h⁻¹·bar⁻¹] is the water permeability coefficient, $B$ [L·m⁻²·h⁻¹] the salt permeability, $\Delta P$ the transmembrane pressure, $\Delta\pi$ the osmotic pressure difference (van 't Hoff: $\pi = i c R T$; rule of thumb ≈ 0.7–0.8 bar per 1000 mg/L TDS), and $c_m$ the membrane-wall concentration. Concentration polarization couples the two fluxes:

$$\frac{c_m - c_p}{c_b - c_p} = \exp\!\left(\frac{J_w}{k}\right)$$

with $k$ the mass-transfer coefficient in the feed channel. Fouling manifests as declining $A$, rising $B$ (degradation/oxidation), and rising feed-concentrate channel DP (spacer plugging). These parameters are exactly what grey-box and physics-informed models make time-varying (see §6).

**Normalization (ASTM D4516).** Raw plant data confound fouling with operating-condition changes (temperature, pressure, recovery, feed TDS). ASTM D4516-19a ("Standard Practice for Standardizing Reverse Osmosis Performance Data", ASTM, 2019, https://store.astm.org/d4516-19a.html) and the DuPont FilmTec normalization manual (DuPont, Form 45-D01616, https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/RO-NF-FilmTec-Plant-Performance-Norm-Manual-Exc-45-D01616-en.pdf) define the standard transform. Normalized permeate flow references actual flow to a standard condition "s" via the net driving pressure (NDP) and a temperature correction factor (TCF):

$$Q_{p,s} = Q_{p,a}\cdot\frac{\mathrm{NDP}_s}{\mathrm{NDP}_a}\cdot\frac{\mathrm{TCF}_s}{\mathrm{TCF}_a},\qquad \mathrm{NDP} = P_f - \frac{\Delta P_{fc}}{2} - P_p - \bar{\pi}_{fc} + \pi_p$$

$$\mathrm{TCF} = \exp\!\left[K\left(\frac{1}{298} - \frac{1}{273+T}\right)\right],\; K \approx 2640\text{–}3020 \text{ (membrane-specific)}$$

Normalized salt passage corrects observed passage for flux, concentration factor and temperature: $SP_s = SP_a \cdot \frac{\mathrm{EPF}_a}{\mathrm{EPF}_s}\cdot\frac{\mathrm{CF}_s}{\mathrm{CF}_a}\cdot\frac{\mathrm{STCF}_a}{\mathrm{STCF}_s}$ (EPF = effective pressure×flow term; CF from recovery $Y$: $\mathrm{CF} = \frac{1}{Y}\ln\frac{1}{1-Y}$ for plug flow). ASTM D4516 applies temperature correction only to water production, not salt passage — a known limitation discussed in Zhao & Taylor's assessment (Desalination, 2005, https://www.sciencedirect.com/science/article/abs/pii/S0011916405003504). Practical guidance: normalize first, then model; trigger cleaning on 10–15 % normalized flow decline or 15–25 % normalized DP rise (DuPont 15 %, Toray up to 50 % per Lakner & Lakner, Membranes, 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12194824/). Wiley's *Reverse Osmosis* (3rd ed.) ch. 12 covers data collection/normalization workflow (Kucera, 2023, https://onlinelibrary.wiley.com/doi/10.1002/9781119725183.ch12).

Most academic papers instead use z-score or min-max scaling on raw SCADA tags; the best plant-facing work does ASTM normalization *first* and then models the normalized KPIs, so the ML target is the fouling signal itself rather than the confounded raw measurement.

---

## 2. ANN / MLP static regression — the canonical baseline

**Seminal work.** Early proposals for ANNs in desalination date to Desalination 1993 (https://www.sciencedirect.com/science/article/abs/pii/0011916493800782). The canonical plant-scale study is **Libotean, Giralt, Rallo, Cohen et al. (2009)**, "Neural network approach for modeling the performance of reverse osmosis membrane desalting," *J. Membrane Science* 326(2):408–419 (https://www.researchgate.net/publication/233529231_Neural_Network_Approach_for_Modeling_the_Performance_of_Reverse_Osmosis_Membrane_Desalting): back-propagation ANN and support-vector regression on plant data, introducing a "short-term memory" time-window because pure state-of-plant models and standard time-series analysis gave unrealistically short predictive horizons for permeate flux and salt passage. This memory-window idea (lagged inputs over a sliding interval) remains the standard feature-engineering trick for static models applied to drifting plants.

**Representative MLP studies and their specifics:**

- **Khayet, Cojocaru & Essalhi (2011)**, "ANN modeling and response surface methodology of desalination by reverse osmosis," *J. Membrane Science* (https://www.sciencedirect.com/science/article/abs/pii/S0376738810008975): inputs NaCl concentration, feed temperature, feed flow rate, operating hydrostatic pressure; response = performance index (salt rejection × permeate flux). Template for the RSM+ANN pairing that dominates lab-scale work.
- **Gaza Strip brackish-water plants (2015)**, *Desalination* (https://www.sciencedirect.com/science/article/abs/pii/S0011916415002532): MLP and RBF networks; permeate flow predicted from feed pressure, pH, conductivity; permeate TDS predicted from temperature, pH, conductivity, pressure. Demonstrated soft-sensing of product quality from cheap feed-side instrumentation.
- **Brooke, Fan, Khayet & Wang (2022)**, *Heliyon* 8(9):e10692 (https://pmc.ncbi.nlm.nih.gov/articles/PMC9519509/): single hidden layer, **3-10-1** topology, tansig/purelin activations, Bayesian-regularization training; 16 central-composite-design runs (12 train / 2 val / 2 test); inputs feed TDS 1000–4000 mg/L, temperature 20–37.5 °C, pressure 95–145 psi. RSM R² = 0.9999 (RMSE 2.41×10⁻⁵), ANN R² = 0.999 (RMSE 5.85×10⁻⁵) on the performance index. Note the tiny dataset — typical of lab-scale RSM/ANN papers; these near-unity R² values reflect smooth designed experiments, not plant reality.
- **Mahadeva et al. (2024)**, "Improvised grey wolf optimizer assisted ANN (IGWO-ANN)," *Heliyon* (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11277383/): MLP **4-9-1** (4 inputs: feed flow 400–600 L/h, salt concentration 35–140 g/L, evaporator/condenser inlet temperatures), output permeate flux 0.118–2.656 L/m²·h; 88 experimental sets, 75/20/5 split, MATLAB 2022a. Test R² = 99.3 %, MSE = 0.004, beating plain ANN (R² 98.8 %) and RSM (98.5 %). Metaheuristic-tuned ANNs (GWO, PSO, GA) are a large sub-literature; gains over well-regularized vanilla MLPs are real but modest (~0.5–1 pt R²).
- **Cabrera et al. (2017–2018)**, *Desalination* (https://www.sciencedirect.com/science/article/abs/pii/S0011916416315120): ANNs managing variable operation of a wind-driven SWRO prototype in Gran Canaria — networks output feed-flow and pressure setpoints given available electrical power, feedwater temperature and conductivity; follow-up compared ANN, SVM and random forest for predicting pressure, feed flow, permeate flow and permeate conductivity under fluctuating power. Canonical for renewable-driven variable-load RO.
- **Boron soft sensor**: ANN ensemble estimating the boron (boric acid) permeability coefficient in SWRO plants, *Desalination* (2023, https://www.sciencedirect.com/science/article/pii/S0011916423008123) — an example of ML replacing a hard-to-measure transport parameter.

**Typical recipe** distilled from this literature: 1 hidden layer with 5–15 neurons for <10³ samples; tanh/sigmoid hidden activations; Levenberg-Marquardt or Bayesian-regularization training in MATLAB, or Adam in Keras/PyTorch; min-max scaling to [-1,1]; 70/15/15 split. Inputs almost always drawn from: feed conductivity/TDS, feed temperature, feed pressure, feed flow, pH, recovery, and (for time-aware variants) lagged values of the target.

---

## 3. Tree ensembles: RF, XGBoost, LightGBM/CatBoost

Gradient-boosted trees are now the default strong baseline for tabular RO data and frequently beat ANNs:

- **Small-scale SWRO design/performance (2025)**, *Desalination* (https://www.sciencedirect.com/science/article/abs/pii/S0011916425011634): real seawater from Korea's east/west/south coasts; XGBoost vs RF vs RNN for salt rejection and energy consumption; **XGBoost best, R² > 0.98** with a minimal feature set.
- **SEC of SWRO plants (2025)**, *Desalination* (https://www.sciencedirect.com/science/article/abs/pii/S0011916425001298): mechanistic SEC model benchmarked against CatBoost and XGBoost; tree models beat neural networks; SHAP used to verify the models recover known mechanism (recovery, flux, feed salinity dominate SEC).
- **Osmotically assisted RO, explainable ML comparison (2024)**, *Desalination* (https://www.sciencedirect.com/science/article/pii/S0011916424003588): comparative RF/XGBoost/ANN study with SHAP feature attribution.
- **Feed-water parameter analysis** (Elsevier book chapter, https://www.sciencedirect.com/science/chapter/bookseries/abs/pii/B9780323885065500383): RF, XGBoost, ANN and MLR compared for predicting the three ASTM-normalized KPIs — salt passage, permeate flow, differential pressure — selecting per-target best models by test RMSE.
- **Micropollutant rejection — the data-leakage cautionary tale**: Jeong et al. (2021), "Predicting Micropollutant Removal by RO and NF Membranes: Is Machine Learning Viable?", *Environ. Sci. Technol.* 55(16):11348–11359 (https://pubs.acs.org/doi/abs/10.1021/acs.est.1c04041). XGBoost on literature-compiled rejection data; showed that random-split CV with near-duplicate experiments produces **falsely high accuracy**; SHAP (cooperative-game attribution) used to test whether the model learned real separation mechanisms. Any RO ML evaluation must split by membrane/plant/time-block, not by row. A companion RF study for organic-compound rejection is Jeong et al./ASCE *J. Environ. Eng.* 146(11) (2020, https://ascelibrary.org/doi/abs/10.1061/(ASCE)EE.1943-7870.0001806).

Typical tree-model hyperparameters in these papers: 100–1000 trees, depth 4–8, learning rate 0.01–0.1, early stopping on a chronological validation block; SHAP for interpretation is near-universal post-2022.

---

## 4. Recurrent architectures and temporal convolution for fouling trajectories

This is where the field moved 2021–2026: treating DP, normalized permeate flow and salt passage as multivariate time series and forecasting them for predictive maintenance.

- **Holistic framework, Desalination (2023)** (https://www.sciencedirect.com/science/article/abs/pii/S0011916423008858): high-salinity SWRO plant data; missing SCADA data filled with the **NAOMI** (non-autoregressive multiresolution imputation) technique; five deep models compared for transmembrane pressure, energy consumption and permeate flow, with inputs flow, temperature, conductivity, pressure, ORP, pH, energy. **LSTM best for TMP and energy consumption**; imputation improved every model's accuracy — a rare paper that treats data quality as a first-class problem.
- **LSTM vs ARIMAX inside a hybrid model — Gaublomme et al. (2023)**, "A hybrid modelling approach for reverse osmosis processes including fouling," *Desalination* (https://www.sciencedirect.com/science/article/abs/pii/S0011916423003880; preprint https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4340730): mechanistic SD model plus data-driven fouling dynamics, where fouling-sensitive parameters (water permeability $A$, feed-spacer channel height, solute permeability $B$) are made functions of membrane resistance and forecast with ARIMAX or RNN-LSTM. **RNN-LSTM clearly outperformed ARIMAX over an 8-month test period.**
- **Temporal Convolutional Network — Pham, Do & Do (2024)**, PHM Society Annual Conference, Vol. 16 (https://doi.org/10.36001/phmconf.2024.v16i1.4144; also https://hal.science/hal-04818480v1): 1-D dilated-convolution TCN forecasting pressures at both ends of the RO vessel (hence DP) using **Carlsbad Desalination Plant (California) data**; TCN gave the smallest test error against LSTM, GRU, and CNN-LSTM baselines. TCNs are attractive here: parallelizable, stable gradients, long effective receptive field via dilations.
- **Fouling-time statistics as the target** — Lakner & Lakner (2025), *Membranes* (https://pmc.ncbi.nlm.nih.gov/articles/PMC12194824/): not ML but the essential statistical baseline. Brackish RO unit (700 L/h), ~4500 measurements over 75 days at 30-min intervals reduced to **104 independent samples** after outlier and independence filtering (consecutive points discarded if ΔTMP ≤ 0.01 bar) and Arrhenius temperature-compensation to 20 °C. Linear TMP growth $TMP(t)=TMP_0+at$ fit: $a = 0.020 \pm 0.002$ bar/day, $TMP_0 = 10.5 \pm 0.265$ bar; expected fouling time to a 25 % TMP rise = **130 ± 15 days (95 % CI 100–160)**; cost-optimal cleaning at 103–117 days depending on the fouling-cost ratio. Any LSTM/TCN forecaster should beat this linear-probabilistic baseline to justify itself.
- **Water-reuse RO fouling**: integrated adsorption + data-driven models, *Desalination* (2024, https://www.sciencedirect.com/science/article/abs/pii/S001191642400064X); MLR/ANN/SVR comparison at the Boujdour SWRO plant, *Eng* 7(3):106 (MDPI, 2026, https://www.mdpi.com/2673-4117/7/3/106): 195 daily measurements, five inputs (temperature, turbidity, pH, conductivity, feed flow), SMOGN augmentation to ~2000 training samples, evaluation on 39 held-out real observations, GridSearchCV tuning — **SVR best average accuracy** for TMP. Illustrates the small-data regime most municipal plants are actually in.

---

## 5. Transformers for RO process time series

- **Temporal Fusion Transformer for DP prediction (2024)**, *J. Water Process Engineering* (https://www.sciencedirect.com/science/article/abs/pii/S2214714424021470): industrial RO process; TFT's variable-selection networks and static-covariate encoders let it mix static descriptors (membrane/train identity) with dynamic SCADA series. **R² = 0.9813 with the static encoder vs 0.8980 without it; LSTM baseline R² ≈ 0.9364.** Attention weights give interpretable indications of which lags/features drive DP. Architecture reference: Lim et al., "Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting," arXiv:1912.09363 (2019/2021, https://arxiv.org/abs/1912.09363) — gated residual networks + LSTM encoder + multi-head attention, quantile-loss output for prediction intervals.
- **Long-sequence forecasting for CIP optimization (2025)**, *Desalination* (https://www.sciencedirect.com/science/article/abs/pii/S0011916425006691): industrial RO for ultrapure water; attention-based long-sequence forecasters (Informer-family) beat CNN+LSTM for multi-week DP trajectories; forecasts feed a clean-in-place (CIP) scenario optimizer; combined with reinforcement-learning cleaning policies, reported **~16.1 % operating-cost reduction and ~140 % increase in RO operating time between cleanings** by choosing higher DP thresholds that account for cleaning-agent and membrane-replacement costs (see also multi-agent RL for a two-stage RO system, *Desalination* 2025, https://www.sciencedirect.com/science/article/abs/pii/S0011916425003455, and DRL control of RO, *Desalination* 2021, https://www.sciencedirect.com/science/article/abs/pii/S0011916421005142).

Practical judgment from the literature: transformers win when (a) sequences are long (thousands of steps), (b) static metadata must be fused, and (c) multi-horizon quantile forecasts are needed; for single-train, short-history plants, GRU/LSTM or even XGBoost with lag features remain competitive and far cheaper to train.

---

## 6. Physics-informed neural networks and grey-box hybrids

**Taxonomy.** Serial (data-driven submodel estimates parameters/inputs for a mechanistic model) vs parallel (data-driven model corrects the mechanistic model's residual) — standard hybrid-modeling classification used across the membrane literature (see the review "From Black Box to Machine Learning: A Journey through Membrane Process Modelling," *Membranes* 11(8):574, 2021, https://www.mdpi.com/2077-0375/11/8/574; grey-box training methods: Comput. Chem. Eng., 2000, https://www.sciencedirect.com/science/article/abs/pii/S0098135499801380).

- **Helali, Albalawi & Bel Hadj Ali (2025)**, "Harnessing Physics-Informed Neural Networks for Performance Monitoring in SWRO Desalination," *Water* 17(3):297 (https://doi.org/10.3390/w17030297): PINN embedding the SD equations (coupled water flux and salt rejection) in the loss; trained on several months of full-scale SWRO operating data; simultaneously learns physically meaningful membrane parameters ($A$, $B$ with Arrhenius temperature dependence) while flagging outliers. **R² = 0.96 for permeate TDS, R² = 0.97 for transmembrane pressure drop**, with better extrapolation beyond training conditions than pure regressors — the key PINN selling point for seasonal plants.
- **PINN for membrane degradation diagnosis (2025)**, *Desalination and Water Treatment* (https://www.sciencedirect.com/science/article/pii/S1944398625005077): mass/momentum transport equations in the loss; positions PINNs as early-warning mechanisms for real-time degradation monitoring.
- **Closed-circuit RO with pretraining + transfer learning (2024)**, *Desalination* (https://www.sciencedirect.com/science/article/abs/pii/S0011916424002686): CCRO is cyclic/multi-mode (closed-circuit mode + flushing mode); two tailored PINNs approximate each mode's latent solution; time-adaptive domain decomposition partitions the sequence; coarse-model pretraining then transfer learning cut **training time from 18 h to 8 h (>50 %)** with accuracy comparable to numerical solvers.
- **Spacer-filled channel CFD surrogate**: PINN with embedded transfer learning solving 3-D flow + mass transfer in SWRO feed channels, *Sep. Purif. Technol.* (2025, https://www.sciencedirect.com/science/article/abs/pii/S1383586625006094); interpretable fouling PINN with adaptive transitions between fouling mechanisms (cake filtration ↔ pore blocking), *Sep. Purif. Technol.* (2026, https://www.sciencedirect.com/science/article/pii/S1383586626007781).
- **Critical review**: "Physics-informed neural networks in water and wastewater systems," *Water Research* (2026, https://www.sciencedirect.com/science/article/pii/S0043135426001314) — catalogs failure modes (loss balancing, stiff PDEs, sparse boundary data) and argues PINNs pay off mainly where sensors are sparse relative to physics.
- **Hybrid grey-box exemplar**: Gaublomme et al. (2023) above (§4) — mechanistic SD core + LSTM-forecast fouling parameters; also hybrid models reducing prediction error ~74 % vs baseline and enabling tighter chemical dosing control, per the desalination digital-twin/RL survey in Smart Water Magazine (2025, https://smartwatermagazine.com/news/smart-water-magazine/when-plant-learns-run-itself-reinforcement-learning-agents-desalination).

PINN loss template for RO (as used in the SWRO PINN papers):

$$\mathcal{L} = \underbrace{\frac{1}{N}\sum \|y_{pred}-y_{meas}\|^2}_{\text{data}} + \lambda_1 \underbrace{\| J_w - A(T)(\Delta P - \Delta\pi)\|^2}_{\text{water flux residual}} + \lambda_2 \underbrace{\| J_s - B(T)\,\Delta c\|^2}_{\text{salt flux residual}} + \lambda_3\,\mathcal{L}_{IC/BC}$$

with $A(T)=A_{ref}\exp[-E_a/R\,(1/T-1/T_{ref})]$ learned jointly.

---

## 7. Gaussian processes and uncertainty quantification

- **Membrane fouling prediction + uncertainty, WWTP case study**, *J. Membrane Science* (2022, https://www.sciencedirect.com/science/article/abs/pii/S0376738822005622): ML fouling prediction with explicit uncertainty analysis at a full-scale wastewater plant — the reference for honest error bars in membrane ML.
- **UF pretreatment of SWRO, real-time soft sensing (2025)**, *J. Water Process Engineering* (https://www.sciencedirect.com/science/article/pii/S1944398625004023): GPR vs tree regression vs ensembles vs NNs for flow rate and membrane resistance; GPR R² = 0.99/0.98; best ensemble R² = 0.99 with RMSE 3.08 L/min.
- **Wave-powered SWRO (2025)**, *Water* 17:2896 (https://doi.org/10.3390/w17192896): Matérn-5/2 GPR for salt-rejection prediction reporting train/test R² = 1.0000 — treat as an overfitting red flag on small smooth datasets rather than a method endorsement.
- **Hybrid physics-ML forward-osmosis flux with complete UQ (2025)**, arXiv:2512.10457 (https://arxiv.org/pdf/2512.10457): GPR on the residual of a physical flux model; propagates aleatoric sensor error and combines with GPR's epistemic variance — the cleanest published template for "physics mean function + GP residual + full predictive distribution," directly transferable to RO flux.

GP math for implementers: $f \sim \mathcal{GP}(m(x), k(x,x'))$ with Matérn-5/2 kernel; predictive variance $\sigma^2(x_*) = k_{**} - k_*^T(K+\sigma_n^2 I)^{-1}k_*$; O(N³) limits exact GPs to ~10⁴ points — use inducing-point (SVGP) approximations for SCADA-scale data. Alternatives seen in the literature: MC-dropout and deep ensembles on LSTMs, and TFT's native quantile loss ($\sum_q \max(q\,e, (q-1)e)$) for interval forecasts.

---

## 8. Membrane property and materials-discovery ML (brief)

- **TFC polyamide RO dataset**: fragment-based ML for inverse design of thin-film composite membranes, *J. Membrane Science* (2025, https://www.sciencedirect.com/science/article/abs/pii/S0376738825010324): **867 water-permeance and 2059 salt-rejection data points from 396 unique TFC membranes across 150 publications**; XGBoost + SHAP links monomer fragments (from interfacial polymerization chemistry) to permeance/rejection; used for inverse design of new monomer combinations.
- **Inverse design at scale**: ML-aided inverse design and discovery of novel polymeric membrane materials, *Environ. Sci. Technol.* (2024, https://pubs.acs.org/doi/10.1021/acs.est.4c08298; open version https://pmc.ncbi.nlm.nih.gov/articles/PMC11755723/): features from membrane chemistry, structure, modification (PEG, zwitterions, GO, polydopamine coatings) on >1000 RO membranes.
- **Permeability–selectivity trade-off**: ML screening predicted gas permeability/selectivity for 3219 polymer candidates and identified ~500 exceeding the Robeson upper bound (phys.org summary of the Georgia Tech work, 2022, https://phys.org/news/2022-07-machine-polymer-membranes.html) — the methodological blueprint (fingerprint polymers → GP/NN property model → screen virtual library) now being replicated for water/salt selectivity.
- Reviews: "Machine Learning in Membrane Design: From Property Prediction to AI-Guided Optimization" (2024, https://pubmed.ncbi.nlm.nih.gov/38436240/); RO synthesis-feature ML, *Materials* 18:840 (2025, https://doi.org/10.3390/ma18040840); ML-driven membrane design across scales, *Environ. Sci.: Water Res. Technol.* 11:2080 (2025, https://pubs.rsc.org/ew/article-abstract/11/9/2080/892390).

---

## 9. RUL, replacement scheduling, fault prediction

- **MBR membrane replacement timing**: predictive-maintenance system using AI-based functional profile monitoring at a full-scale MBR plant, *J. Membrane Science* (2022, https://www.sciencedirect.com/science/article/abs/pii/S0376738822001466); membrane-lifetime predictive modeling for full-scale MBRs, *Water Research* (2025, https://www.sciencedirect.com/science/article/abs/pii/S0043135425015799). Directly transferable framing for RO element replacement (target: years-scale $A$/$B$ drift after each CIP "reset").
- **Explainable UF prognostics**: similarity-based (fuzzy-similarity) RUL estimation for ultrafiltration membranes, arXiv:2602.00659 (2026, https://arxiv.org/abs/2602.00659) — explicitly motivated by operator distrust of opaque ML and by cleaning-induced resets and temperature effects that break naive degradation models.
- **Probabilistic replacement window**: Lakner & Lakner (2025) (§4) gives the closed-form cost-optimal maintenance interval $C_{year}/C_0 = \frac{365}{t_{main}}\left(1+\Phi(t_{main})(C_{foul}/C_0-1)\right)$ — a template for converting any fouling forecast + uncertainty into a replacement/cleaning schedule.
- **Auxiliary-equipment faults**: ML-based early fault prediction for high-pressure pumps in an RO plant (Morocco case study), 2026 (https://www.sciencedirect.com/science/article/pii/S2949821X26002024); early-warning ML on RO sensor data for power failure, fouling/scaling and wash scheduling (Agh et al., 2018, https://www.researchgate.net/publication/327736664).

Published RO-element-specific RUL (as opposed to fouling/cleaning forecasting) remains thin — the MBR and UF literature is where the methods are; mapping them onto ASTM-normalized RO KPIs is an open, publishable gap.

---

## 10. Deployed economics — what ML actually saves

- **Synauta × Osmoflo trial (Western Australia)**, Smart Water Magazine (2019–2020, https://smartwatermagazine.com/news/synauta/machine-learning-delivers-energy-savings-desalination): 4 × 1000 m³/day SWRO trains; ML optimized three setpoints (HP pump flow, PX booster flow, PX drain valve), emailed to operators daily. **Up to 18 % instantaneous and 9.7 % average energy savings over a 6-month trial; CIP frequency cut from 12 to 9 per year (10–15 % chemical savings); ≈ $65,000/yr OPEX savings on the 4000 m³/day plant; extrapolated $3M+/yr for a 300,000 m³/day plant at 10 % energy saving.**
- **Design-space optimization**: supercomputing + ML optimal design of high-permeability SWRO systems (2023, https://pubmed.ncbi.nlm.nih.gov/36774298/): simulated SEC reduction of **27.5 % to 1.66 kWh/m³** (12.2 % from high-permeability membranes, 14.5 % from two-stage design).
- **CIP/RL economics**: ~16 % operating-cost reduction from smarter cleaning thresholds (§5); digital-twin case studies (ACCIONA/Sichel, Smart Water Magazine, https://smartwatermagazine.com/blogs/dr-cosima-sichel/optimizing-plant-performance-a-case-digital-twins-desalination) report real-time energy/chemical minimization; SWRO digital twin + ML efficiency study, IOS Press (2024, https://ebooks.iospress.nl/volumearticle/69380).
- Payback: vendors quote months-scale payback for software-only optimization (no capex beyond integration) — the Synauta figures imply <1 yr on the trial plant; peer-reviewed payback numbers are scarce.

---

## 11. Cross-cutting: inputs, data volumes, preprocessing, metrics

**Canonical input feature set** (union across §§2–5): feed conductivity/TDS, feed temperature, feed pressure, feed flow, permeate flow, permeate conductivity, concentrate/reject pressure and flow, recovery, pH, ORP, turbidity/SDI, DP per stage, pump power/energy, time-since-last-CIP, membrane age; for time-series models, 6–48 lagged steps of each. Reviews: AI methods for RO membrane processes, *Water Conservation Science and Engineering* (2023, https://link.springer.com/article/10.1007/s41101-023-00227-7); ML in membrane-based desalination, *Desalination* (2025, https://www.sciencedirect.com/science/article/abs/pii/S001191642500517X); fouling control and modeling review, *Comput. Chem. Eng.* (2022, https://www.sciencedirect.com/science/article/abs/pii/S0098135422001351); data-driven identification of industrial RO, *Comput. Chem. Eng.* (2022, https://www.sciencedirect.com/science/article/abs/pii/S0098135422001235).

**Data volumes seen in practice**: 16–88 points (lab RSM/ANN); 100–200 daily records (small municipal, Boujdour); 10³–10⁴ (pilot campaigns, Lakner's 4500 raw → 104 independent); 10⁵–10⁶ (SCADA at minutes-scale over months — Carlsbad TCN, holistic-framework SWRO, PINN SWRO). Rule of thumb from the corpus: deep sequence models only start beating trees/GPs above ~10⁴ effective samples spanning at least one full seasonal cycle and ≥2 CIP cycles.

**Preprocessing pipeline** (composite of best practice): (1) hard sensor-range and rate-of-change filters; (2) steady-state detection or independence filtering; (3) ASTM D4516 / FilmTec normalization to reference conditions; (4) imputation (NAOMI for multiresolution gaps); (5) z-score scaling fit on the training block only; (6) chronological (blocked) train/val/test splits, never random shuffles (Jeong 2021 leakage result); (7) optional augmentation (SMOGN) only in small-data regimes and only on training folds.

**Metrics**: R², RMSE, MAE, MAPE on test blocks; for forecasters add horizon-wise RMSE and quantile coverage (P10/P90). Headline numbers to benchmark against: XGBoost R² > 0.98 (salt rejection/energy, tabular); TFT R² 0.981 vs LSTM 0.936 (DP, sequence); PINN R² 0.96/0.97 (TDS/ΔP, hybrid); GPR R² 0.98–0.99 (UF soft sensors).

---

## Implementation notes

What a practitioner needs to replicate this from scratch:

**Data.** Minimum viable: 6–12 months of SCADA at 1–15 min resolution covering ≥1 seasonal temperature cycle and ≥2 CIP events, with tags: feed/permeate/concentrate pressures and flows, feed & permeate conductivity, feed temperature, pH, (ideally ORP, turbidity, pump kW, CIP log with dates/chemistry). ~20 tags × 1-min × 1 yr ≈ 10⁷ rows — trivially handled in Parquet/pandas or DuckDB. If no plant data: generate synthetic training data from DuPont WAVE or a coded SD model with injected fouling drift and sensor noise (the CCRO-PINN and design-optimization papers do exactly this), then transfer-learn on real data.

**Math you must implement first (before any ML):**
1. SD model: $J_w = A(\Delta P - \Delta\pi)$, $J_s = B\Delta c$, van 't Hoff osmotic pressure, CP correction $\exp(J_w/k)$.
2. ASTM D4516/FilmTec normalization: TCF, NDP, normalized permeate flow and salt passage, concentration factor $\frac{1}{Y}\ln\frac{1}{1-Y}$. Encode as a pure function `normalize(df, ref_conditions) -> df_norm`; unit-test against the worked examples in the DuPont manual (Form 45-D01616).
3. A linear/probabilistic fouling baseline (Lakner-style TMP regression with parameter σ's) — this is your model-to-beat and your sanity check.

**Tools.** Python: pandas/polars, scikit-learn (MLR, RF, GPR with Matérn kernels), xgboost/lightgbm/catboost, PyTorch (LSTM/GRU/TCN; `pytorch-forecasting` for TFT with quantile loss), gpytorch (SVGP for >10⁴ points), shap for attribution, optuna for tuning. PINNs: plain PyTorch with autograd residuals (DeepXDE optional). MATLAB + Neural Net Toolbox only if reproducing the older ANN papers exactly.

**Modeling ladder (in order, stop when accuracy suffices):**
1. Normalize per ASTM → monitor KPIs → linear drift model with confidence intervals (cleaning/replacement scheduling per §9's cost formula).
2. XGBoost on tabular features + lags (memory window à la Libotean 2009) for next-day KPI prediction; SHAP to sanity-check physics (temperature ↑ → flux ↑, DP mostly flow-driven).
3. GRU/LSTM or TCN (kernel 3, dilations 1/2/4/8, 64–128 channels, dropout 0.1–0.2, Adam 1e-3, early stopping) for 1–4-week DP/flux trajectories; input window 1–7 days.
4. TFT if you have multiple trains/static metadata and need interpretable multi-horizon quantiles.
5. Hybrid/PINN: SD mean model with time-varying $A(t), B(t)$ (Arrhenius in T) estimated by the network; physics residuals in the loss with tuned λ's — expect the biggest gains in extrapolation (season, setpoint changes), per Helali 2025.
6. GP (or GP-on-physics-residual per arXiv:2512.10457) wherever a decision needs calibrated uncertainty — CIP triggers, replacement windows.

**Validation discipline.** Chronological blocked splits; leave-one-CIP-cycle-out for fouling models; leave-one-membrane/plant-out for materials/rejection models; report horizon-wise RMSE + interval coverage; always compare against (a) persistence, (b) the linear normalized-drift baseline, (c) XGBoost. Distrust any published R² > 0.99 on <100 samples.

**Effort estimate.** Normalization + baseline: ~1 week. Tree + sequence models with proper backtesting: 2–4 weeks. PINN/hybrid with learned $A(t),B(t)$: 4–8 weeks including physics unit tests. The binding constraint is almost always data hygiene (sensor drift, CIP logs, conductivity-probe fouling), not model capacity.
