# Advanced Process Control for RO/UF: MPC, Reinforcement Learning, and Fault Detection

Scope: control-oriented modelling and identification for membrane systems; MPC and economic MPC formulations for reverse osmosis (RO); the DMC/PID baselines that actually run in plants; reinforcement learning (RL) applied to desalination, pumping and chemical dosing; and multivariate fault detection and diagnosis (FDD). Written for an engineer intending to implement from scratch. Deployment status (real plant vs simulation-only) is flagged explicitly throughout and summarised in §9.

---

## 1. The control hierarchy that actually exists in an RO/UF plant

Almost every real membrane plant is organised in three layers, and any advanced control you add must slot into one of them:

- **L0 — drive/regulatory layer (milliseconds–seconds).** VFD speed loops on the high-pressure (HP) pump, booster pump and recirculation pump; positioner loops on the concentrate throttling valve; PLC interlocks. Universally PI/PID with sample times 0.1–1 s.
- **L1 — unit regulatory layer (seconds–minutes).** Feed flow, feed pressure, permeate flow, crossflow velocity, recovery. Classically 2–3 SISO PI loops with fixed pairings. Alatiqi, Ghabris and Ebrahim (1989) published the first systematic step-test identification and multi-loop design for RO (*Desalination* 75:119–140, [doi:10.1016/0011-9164(89)85009-x](https://doi.org/10.1016/0011-9164(89)85009-x)); Robertson, Watters, Deshpande, Assef and Alatiqi (1996) then applied **Dynamic Matrix Control (DMC)** to the same class of plant (*Desalination* 104:59–68, [doi:10.1016/0011-9164(96)00026-4](https://doi.org/10.1016/0011-9164(96)00026-4)), and Assef, Watters, Deshpande and Alatiqi (1997) demonstrated **constrained MPC (CMPC)** experimentally on an RO unit (*J. Process Control* 7:283–289, [doi:10.1016/s0959-1524(97)00004-8](https://doi.org/10.1016/s0959-1524(97)00004-8)). Burden, Deshpande and Watters (2001) reported CMPC on a B-9 Permasep permeator pilot, where PI control could not hold product quality when manipulating pH but CMPC kept outputs in spec (*Desalination* 133:271–283, [doi:10.1016/s0011-9164(01)00107-2](https://doi.org/10.1016/s0011-9164(01)00107-2)). These four papers are the DMC/PID baseline the field still measures against.
- **L2 — supervisory / economic layer (minutes–hours).** Recovery split, SEC minimisation, CIP scheduling, cycle sequencing, load shifting. This is where MPC, economic MPC (EMPC), extremum-seeking control (ESC) and RL are actually being deployed, almost always as **set-point generators for the L1 PI loops** rather than as direct actuator controllers. Gao, Jarma, Christofides and Cohen (2025) state this explicitly: "a higher-level (supervisory) control system that guided a lower-level controller for real-time SEC optimization" (*Water* 17:2363, [doi:10.3390/w17162363](https://doi.org/10.3390/w17162363)).

**Manipulated variables (MVs)** in practice: HP pump VFD speed (or feed flow set-point), concentrate throttling valve position, interstage booster pump speed/valve, ERD (PX) booster flow, PX valve-to-drain, recirculation pump speed (CCRO/CCD), three-way valve position (filtration/drain switch), antiscalant and coagulant dose, backwash/CIP timing.
**Controlled variables (CVs):** system pressure, permeate flux, overall recovery `Y`, crossflow/retentate velocity, permeate conductivity/TDS, concentrate conductivity (batch RO), transmembrane pressure (TMP), specific energy consumption (SEC).

---

## 2. Control-oriented models: governing equations

### 2.1 Lumped first-principles RO model (UCLA formulation)

The UCLA Christofides/Cohen line of work uses a kinetic-energy balance around the actuated valve plus a membrane mass balance. For a single-stage plant with retentate valve resistance `e_vr` as MV (Bartman, Zhu, Christofides, Cohen 2010, *J. Process Control* 20:1261–1269, [PDF](http://pdclab.seas.ucla.edu/Publications/ABartman/Bartman2010_JPC.pdf)):

```
0 = (A_p²)/(A_m K_m V) (v_f − v_r) + (A_p/ρV) Δπ − (A_p e_vr v_r²)/(2V)
Δπ = f_os · C_feed · ln(1/(1−Y))/Y ,     f_os = 78.7 Pa/(mg L⁻¹)
Y = Q_p/Q_f = v_p/(v_p+v_r)
P_sys = (ρ A_p)/(A_m K_m) (v_f − v_r) + Δπ
v_p = (A_m K_m)/(ρ A_p) (P_sys − Δπ)
```

with experimentally fitted parameters ρ = 1007 kg/m³, V = 0.6 m³, A_p = 1.27×10⁻⁴ m², A_m = 15.6 m², K_m = 9.7×10⁻⁹ s/m. The `ln(1/(1−Y))/Y` factor is the log-mean osmotic pressure across the module and is the single most important nonlinearity for control.

Valve resistance is *not* linear in stem position; UCLA fit `e_vr = α ln(O_p) + β` piecewise over five valve-position ranges (three in the 2009 paper), e.g. `O_p = −84.428 ln(e_vr) + 459.21` in one band (Bartman, Christofides, Cohen 2009, *Ind. Eng. Chem. Res.* 48:6126–6136, [PDF](http://pdclab.seas.ucla.edu/Publications/ABartman/ABartman_PDChristofides_YCohen_IECR_2009_48_Nonlinear_Model-Based_Control_Experimental_Reverse-Osmosis_Water_Desalination_System.pdf)). Capturing this nonlinearity is described as "extremely crucial" for transferring simulated controllers to hardware.

### 2.2 Spatially distributed high-recovery model

At >85% recovery the well-mixed assumption fails. McFall, Bartman, Christofides and Cohen (2008, *Ind. Eng. Chem. Res.* 47:6698–6710, [PDF](http://pdclab.seas.ucla.edu/Publications/CMcFall/CMcFall_ABartman_PDChristofides_YCohen_IECR_2008_47_Control_Monitoring_High-Recovery_Reverse-Osmosis_Desalination_Process.pdf)) combine two time-domain ODEs with two space-domain ODEs:

```
dv_b/dt = (A_p/ρV)(P − ½ v_b² e_v1)
dv_r/dt = (A_p/ρV)(P − ½ v_r² e_v2)
dC_z/dz = (C_z/v_z) · K_m(P − K_Δπ C_z)/(ρH)
dv_z/dz = − K_m(P − K_Δπ C_z)/(ρH)
BCs: C_z(0)=C_f ,  v_z(0)=α v_mf ,  v_z(L)=α v_r
```

Pressure `P` is an *algebraic* unknown solved at every time step by a shooting method until the outlet velocity BC is satisfied; the resulting `P` is substituted into the time ODEs. Parameters: A_m = 13 m², K_m = 9.218×10⁻⁹ s/m, K_Δπ = 78.7 Pa/(mg/L), H = 1 mm, L = 5 m, C_f = 10,000 mg/L, giving a 91% recovery steady state at P = 8.61 MPa. This is the reference model for high-recovery brackish control studies.

### 2.3 Data-driven control models

- **NARMAX / grey-box discrete models.** For closed-circuit RO (CCRO), Chowdhury et al. (2025, *Water Supply* 25(4):727–748, [OSTI PDF](https://www.osti.gov/servlets/purl/3002918)) use a three-equation grey-box model estimated by least squares on each cycle:
  `c_R(k+1) = (1−θ_c1) c_R(k) + θ_c2 f̄_F(k) + θ_c3 c_R(k) f̄_F(k)`;
  `P_R(k+1) = θ_R1 f̄_R(k) + θ_R2 f̄_R(k)²`;
  `P_F(k+1) = θ_F1 + θ_F2 f̄_F(k) + θ_F3 c(k)`.
  Signals are median-filtered with window W = 21 at 1 s sampling before fitting.
- **LSTM sequence models.** The same group's follow-up (Chowdhury et al. 2025, *Chem. Eng. Res. Des.*, [OSTI PDF](https://www.osti.gov/servlets/purl/3002293)) trains an LSTM that maps `[x(k); u(k..k+T−1)]` to `x(k+1..k+T)` with x = (reject conductivity c_R, feed pump power P_F, recirc pump power P_R) and u = (f_F, f_R, feed conductivity c_F).
- **Koopman lifted linear models.** Han, Yao, Law and Yin (2024, *Control Engineering Practice*; [arXiv:2405.12478](https://arxiv.org/abs/2405.12478)) learn a deep input–output Koopman operator (DIOKO): lift measurements `z = ψ_θ(y)` with a (128,128) ELU MLP into a 60-dimensional observable space where `z⁺ = A z + B u` and the economic stage cost is *linear in z*, which makes the EMPC a QP.
- **Subspace identification (N4SID/MOESP).** Build block-Hankel matrices `U_p, U_f, Y_p, Y_f` from input–output data, compute the oblique projection `O_i = Y_f /_{U_f} W_p`, take its SVD `O_i = UΣVᵀ`, truncate to order n, recover the extended observability matrix `Γ_i = U_1 Σ_1^{1/2}` and then `(A,B,C,D)` by least squares. This is the pragmatic route to an MIMO `x⁺ = Ax + Bu, y = Cx + Du` model for linear MPC of an RO train from step/PRBS tests, and it is what Alatiqi-style step-test identification was doing manually in 1989. Numerically it relies only on QR and SVD, which is why it scales to MIMO where PEM struggles.

### 2.4 The identifiability trap (a real, reproducible failure)

Chowdhury et al. found that when their CCRO MPC converged onto flat, near-constant flow set-points, the next cycle's parameter estimates diverged: "Lack of perturbation leads to dramatic" parameter drift, and the resulting forecasts were badly wrong two cycles later. Their fix was to **inject deliberate dither** into the optimal set-points (`u_perturbed = u* + a·w`, w ~ N(0,1), σ = a_F, a_R) and to randomise the first 2 minutes of each filtration phase. Any adaptive MPC on a membrane system that never reaches steady state must budget for persistent excitation explicitly; this is the single most transferable practical lesson in the CCRO literature.

---

## 3. Regulatory-layer control: what beats PID and by how much

Bartman et al. (2009) ran a controlled experiment on UCLA's WaTeR Center RO rig (feed tank, 2 low-pressure pumps, 2 HP pumps each ~4.3 gpm at 1000 psi, 18 pressure vessels of Filmtec spiral-wound elements, 6 in series used for the tests; sampling 0.1 s; valve full-stroke time ≈45 s; VFD limited to 4.5/10 max):

- Loop I: PI on system pressure via VFD speed, `S_VFD = K_f(P_sys^sp − P_sys) + (K_f/τ_f)∫(P_sys^sp − P_sys)dt`, set-point 150 psi, K_f = 0.01, τ_f = 0.1.
- Loop II: feedback-linearising controller on retentate flow via the valve, requesting first-order closed-loop response `dv_r/dt = (1/γ)(v_r^sp − v_r)` with γ = 0.6, plus integral action.

For a 1.5 → 3 gpm retentate set-point step at 5400 ppm NaCl: the P controller left **~20% steady offset with sustained oscillations** (which propagate into pressure and pump speed and shorten pump life), while the nonlinear model-based controller settled with **~3–4% offset** and only brief overshoot. The mechanism is loop interaction: opening the valve drops pressure, loop I raises feed flow, retentate flow rises again — a P controller that ignores the coupling limit-cycles. This is the cleanest published justification for model-based control at the RO regulatory layer.

McFall et al. (2008) show the complementary result for disturbance rejection: with a 24 h time-varying feed-concentration disturbance and 60 s sampling, two PI loops (P via bypass valve, v_r via retentate valve) "ultimately fail[ed] to keep P and v_r at the desired values", pure Lyapunov-based bounded feedback only marginally damped the oscillation, and only **feed-forward + feedback** (measuring C_f with a feed conductivity meter and re-solving the steady-state model for nominal `e_v1^nom, e_v2^nom` at every sample) rejected it. The bounded control law is

```
u_k = − r(x, u_max) L_g V_L ,
r = [ L_f̂ V_L + √((L_f̂ V_L)² + (u_max |L_g V_L|)⁴) ] / [ |L_g V_L|² (1 + √(1+(u_max|L_g V_L|)²)) ]
```

with `V_L = xᵀ P_L x`, and `f̂(x) = f(x) + w(x)d(t)` folding the measured disturbance into the drift term. Practical note from the same paper: for RO, feedback is not needed for stability (the plant is open-loop stable and fast); it is needed for *performance, constraint keeping and fault tolerance*.

---

## 4. MPC and economic MPC formulations for RO

### 4.1 Generic tracking MPC (the DMC baseline)

DMC uses a step-response model `y(k+j) = Σ_{i=1}^{N} a_i Δu(k+j−i)` and solves the unconstrained least-squares move `Δu = (AᵀΓᵀΓA + λ²I)⁻¹AᵀΓᵀ e`, with `A` the dynamic (step-coefficient) matrix. On RO this is what Robertson (1996) and Assef (1997) implemented; typical CV/MV pairing is permeate flow ← feed pressure/VFD and permeate conductivity ← recovery/pH. It remains the correct baseline: it is trivially retunable from bump tests, requires no state estimator, and is what a plant's DCS vendor can actually support.

### 4.2 Economic MPC: minimising SEC directly

The RO economic objective is specific energy consumption:

```
SEC = ΔP/Y = P_sys Q_f / Q_p ,     SEC_norm = SEC/π_0
```

subject to the **thermodynamic restriction** `P_sys ≥ π_0/(1−Y)` (below this, the exit region of the module produces no permeate). Bartman et al. (2010) implemented, on the UCLA rig, the real-time optimisation

```
min_{v_f, e_vr}  SEC = ρ e_vr (v_f − v_p)² v_f / (2 v_p)
s.t. v_p = v_p^set ;  v_f > 0 ;  e_vr > 0 ;  SEC ≥ 0 ;
     P_sys ≥ π_0/(1−Y) ;  0 = P_sys/ρ − ½ e_vr (v_f − v_p)²
```

solved by SQP in MATLAB, exchanging data with the plant HMI over UDP every ~10 s (1–5 s per solve after the first), with a 19-point moving average on sensor data. Experiments at 1600/1850/3500 ppm NaCl, 110–170 psi, 1 and 1.45 gpm permeate set-points landed on the theoretical SEC-vs-recovery curve, confirming that the energy-optimal operating point is real and reachable. Two honest caveats the paper reports: the optimum sits where hardware limits prevent going to higher recovery, and salt rejection is *not* constant — permeate TDS exceeded the 500 ppm drinking-water limit at the highest recovery on 3500 ppm feed. A rejection constraint must be added for any potable application.

For EMPC theory (stability with a non-tracking stage cost), the reference is Ellis, Durand and Christofides (2014, *J. Process Control* 24:1156–1178, [PDF](http://pdclab.seas.ucla.edu/Publications/MEllis/Ellis20141156.pdf)): Lyapunov-based EMPC (LEMPC) adds the constraint `V̇(x,u) ≤ V̇(x, h(x))` (or region constraint `V(x̃(t)) ≤ ρ_e`) to an economic cost, giving closed-loop boundedness in `Ω_ρ`; alternatives are point-wise terminal constraints `x̃(N) = x_s`, terminal region + terminal cost, and asymptotic/transient **average constraints** (e.g. average recovery or average production over a window), which map naturally onto water-supply obligations.

### 4.3 Two-stage RO supervisory optimisation, validated in the field

Gao, Jarma, Christofides and Cohen (2025, *Water* 17:2363) formulate a dual-level controller for a two-stage brackish plant (Stage 1: 14× Toray TM710D; Stage 2: 7× TM810V; ~98 m³/day at 75% recovery; agricultural drainage feed at 11,000–19,000 mg/L TDS). The supervisory layer estimates membrane permeabilities online from sensors, then SQP-minimises `SEC(Y, Y₁)` over overall recovery `Y` and first-stage recovery `Y₁` subject to pressure, flux, crossflow and recovery bounds; the analytic optimum is

```
Y₁,opt = 1 − √( R₁ η₂ / (R_T η₁ (1−Y)) )
```

i.e. the optimal recovery split depends on relative *pump efficiencies*, not just membrane properties. Three PI loops (feed flow ← VFD1, stage-1 pressure ← VFD2, stage-2 pressure ← valve) execute set-points; supervisory updates every ~300 s. Field results: **SEC reduced 4.2%** at fixed 74% recovery (Y₁ 52% → 60%), **7.1%** when Y and Y₁ were optimised jointly (Y 74% → 58%, feed flow 61.4 → 78.3 L/min), and **~10%** versus flux-equality operation under a feed-salinity transition from 24,190 to 17,833 mg/L. Loop convergence: 150 s (flow), 280 s (stage-1 pressure), 430 s (stage-2 pressure), with 0.11–0.15 MPa overshoot. Pump-efficiency maps were fitted as 2-D Gaussians (R² = 0.98) and concentration polarisation from `Sh = 0.38 Re^0.54 Sc^0.33`.

### 4.4 MPC of a cyclic (closed-circuit) RO process — full formulation

CCRO alternates a **filtration** phase (concentrate recirculated; `f_P = f_F`) and a **drain** phase, switching on concentrate conductivity limits (upper 25 mS/cm, lower 3 mS/cm on the CSM pilot). Because it never reaches steady state, the economic metric must be integrated over the cycle:

```
iSEC = Σ_{k=0}^{N} (P_F(k)+P_R(k)) / Σ_{k=0}^{N} f_F(k)
```

and the MPC (Chowdhury et al. 2025, *Water Supply* 25(4):727–748) is

```
min_{f_F(1..M), f_R(1..M)}  iSEC
s.t.  model Eqs. (grey-box, recalibrated each cycle)
      44 ≤ f_R ≤ 55 L/min      (recirc pump safety)
      1 ≤ f_F ≤ 3 L/min        (feed pump / membrane safety)
      c_R(k) ≤ c_R^UCL (25 mS/cm)
      set-points change every C = 120 samples (2 min)
      [variant II] filtration phase length fixed (e.g. 180 min)
```

M = 90 set-point moves over a 2.5 h horizon; solved with **IPOPT** (cyipopt/Python), with LabVIEW running the 1 s PI/VFD layer and R doing preprocessing/estimation. Results: with a *static* model the iSEC forecast was biased 1.5–3.5% low after an unmeasured feed-salinity change and never recovered; with per-cycle recalibration forecasts stayed **within 1%** of measured iSEC except for the one cycle immediately after the disturbance; realised filtration length stayed **within 12 min of the 180 min target**. The optimal policy is structurally simple and interpretable: recirculation at its *lower* bound (45 L/min) throughout, feed flow at its *upper* bound early and *lower* bound late — because pump power rises with concentrate conductivity, so you should make water while the loop is still dilute.

The LSTM-MPC successor (Chowdhury et al. 2025, *Chem. Eng. Res. Des.*) replaces the grey-box model with an LSTM: 190 cycles of pilot data (151 from ESC experiments, 39 from MPC experiments), resampled to a uniform 1 s grid, 8:1:1 train/val/test split by cycle, MinMax-scaled to [−1,1] with the scaler fit on train+val only, sliding-window sequence augmentation. Architecture: **1 hidden layer, 128 units**, PyTorch, learning rate tuned over [1e−5, 1e−2] (1e−3 reported optimal in text; Table 3 lists 0.01), early stopping on validation loss. Custom loss = MSE over all three states + MSE of the numerically differentiated `ċ_R` + a reconstruction term integrating the predicted gradient back to `c_R`. Test metrics: MSE `c_R` = 0.111 mS/cm, MAE 0.732 mS/cm; MSE `P_F` = 1.68e−4 kW, `P_R` = 1.98e−4 kW. The MPC is a 60-dimensional NLP (30 moves × 2 flows over 1 h) solved with IPOPT. **Projected iSEC: 9.01 vs 9.58 kWh/m³ (c_R^UCL = 17 mS/cm) and 9.24 vs 9.88 kWh/m³ (25 mS/cm) for LSTM-MPC vs NARMAX-MPC** — ~6% better, and the LSTM needs no per-cycle re-identification and therefore no dither. Important caveat stated by the authors: these are **offline simulations**, because the pilot was no longer operating; and the LSTM will not extrapolate to feedwater compositions outside its training distribution.

### 4.5 Model-free alternative: extremum-seeking control

For CCRO, Chowdhury et al. (2024, *Water Research X*, [PMC11648806](https://pmc.ncbi.nlm.nih.gov/articles/PMC11648806/)) optimise `J_i = SEC_i + α·SBV_i` (SBV = specific brine volume) by cycle-indexed ESC: dither `u_k = ū_k + Ã sin(2πk/τ)` on the upper conductivity limit, high-pass filter + demodulate to estimate the gradient `ρ_k`, update `ū_{k+1} = ū_k − γρ_k`. Pilot: DuPont BW30-4040 (7.9 m²), 900–1350 mg/L NaCl, 1 s sampling. It recovered **6.5%** of performance after an economic-parameter change (α: 1 → 10; ~70 cycles ≈ 35 h to converge) and **6.8%** after a +50% feed-salinity step (~150 cycles ≈ 85 h). ESC is attractive when you cannot maintain a model, but its convergence time (tens of hours) makes it unsuitable for fast disturbances.

### 4.6 Koopman EMPC — the computational argument

On BSM1 (five-compartment activated sludge + secondary clarifier, 15 min sampling, 14-day evaluation, three weather files), DIOKO-EMPC was trained on 1e5 samples (8e4 train / 1e4 val / 1e4 test), 400 epochs, batch 128, latent dim 60, prediction horizon 30. Dry-weather results (Han et al. 2024, Table 8): **stage cost 1.295e7 (DIOKO-EMPC) vs 1.582e7 (nonlinear EMPC) vs 1.789e7 (tracking MPC)** — an 18% economic improvement over nonlinear EMPC — with **online solve time 0.0339 s vs 334.5 s** (≈9,900×; the authors quote >5,600× overall). SAC reached 1.345e7 but required 1e6 training samples versus 1e5. That trade-off — convex QP EMPC on a learned lifted-linear model beating both nonlinear EMPC and model-free RL on sample efficiency — is currently the strongest quantitative case for Koopman methods in water treatment.

---

## 5. Reinforcement learning for RO, desalination and water systems

### 5.1 Formulation

MDP `(S, A, P, r, γ)`; the practical pattern in water is a **cascade**: the RL agent chooses set-points, PI loops execute them. Golabi, Erradi, Qiblawey, Tantawy, Bensaid and Shaban (2024, *Applied Intelligence* 54:6333–6353, [doi:10.1007/s10489-024-05452-8](https://link.springer.com/article/10.1007/s10489-024-05452-8)) do exactly this for RO:

- **Lower level (DDPG):** state = (integrated error, tracking error, permeate flow); action = HP pump feed pressure; reward = +10 if |e| < 0.2 m³/h else −1; 15,000 episodes × 25 steps, γ = 1.0, lr 1e−3, 4 s sampling; 3-layer actor and critic.
- **Upper level (DQN):** state = (tank level, demand flow, permeate flow, Δdemand, Δflow); action = permeate flow set-point ∈ [12, 30] m³/h; reward = revenue(quality-dependent price) − energy cost − overflow/underflow penalty; 1,000 episodes × 1,440 steps (24 h at 15 min), γ = 0.9, lr 1e−4.
- Plant model: FilmTec SW30HR-380, `Q_p = A_w A_em T_cp (ΔP − β Δπ)`, `E_c = 0.036 Q_f P_f/ξ_HP − 0.036 Q_b P_b ξ_E`, fouling decay constants, tank `dH_st/dt = (F_p − F_d)/A_st`, 2.5 ≤ H_st ≤ 3.5 m, electricity $0.08/kWh.
- Result: DDPG beats PID for set-points above ~65 m³/h (nonlinear regime); average episode rewards 3454.9 / 3452.62 / 3450.2 across deterministic, randomised-level and stochastic-demand scenarios; underflow appears at demand-perturbation α = 0.08. **Simulation only.**

Other RO-specific studies: Bonny, Kashkash and Ahmed (2022, *Desalination*, [doi:10.1016/j.desal.2021.115443](https://doi.org/10.1016/j.desal.2021.115443)) use DDPG on transmembrane pressure while holding 99% salt rejection. Soleimanzade (2022, University of Alberta thesis, [handle](https://ualberta.scholaris.ca/items/5844238e-c1a8-4098-95d9-addec0b797ac); see also *Applied Energy* 317:119184, 2022) formulates grid-connected PV-RO energy management as a POMDP and adds 1-D CNNs to SAC actor/critic/value nets, beating DDPG, PPO, TD3 and vanilla SAC on solar exploitation. A 2025 *Desalination* paper applies **multi-agent RL** (VDN, QMIX vs a DRQN single-agent baseline) to two-stage RO, controlling feed flow, HP pump pressure and interstage booster pressure to minimise SEC while meeting production, trained 50,000 episodes in a Julia simulator built on Chen et al. (2004) fouling and Jeong et al. (2021) full-scale models, with PyTorch + PettingZoo ([code](https://github.com/Yumbang/Towards-Autonomous-Operation-of-Two-Stage-Reverse-Osmosis-Water-Treatment-System-with-MARL)); the MARL agents were more robust than single-agent RL. All simulation-only.

### 5.2 RL in the wider water sector — the numbers that exist

- **Aeration/activated sludge.** Croll, Ikuma, Ong and Sarkar (2023, *Environ. Sci. Technol.*, [doi:10.1021/acs.est.3c00353](https://pubs.acs.org/doi/full/10.1021/acs.est.3c00353)) benchmarked four algorithms on BSM1; **TD3 cut aeration + pumping energy 14.3%** versus the BSM1 benchmark controller and beat the advanced domain-based strategy. Their 2024 *Water Research* follow-up extends to unified multi-objective control of diverse actions ([doi link](https://www.sciencedirect.com/science/article/abs/pii/S0043135424010789)).
- **MBR.** Nam, Heo, Loy-Benitez, Ifaei and Yoo (2020, *Water Sci. Technol.* 81:1578–1587, [doi:10.2166/wst.2020.053](https://doi.org/10.2166/wst.2020.053)) report a DQN autonomous aeration trajectory reducing **MBR aeration energy 34%** while holding effluent limits — evaluated on a calibrated full-scale plant model, not in closed loop on the plant.
- **Pump scheduling / WDN.** Patel, Zhou, Lamb, Wang and Luo (2023, [arXiv:2310.09412](https://arxiv.org/abs/2310.09412)) trained PPO (RLlib) on a real network (6 pump/valve stations, 6 reservoirs, 18 demand zones, 15-min SCADA 2019–2023, 96-step episodes; state dims 6 → 103 including 96 tariff values). Over 330 test cases: **90% reduction in out-of-bound tank-level area and 93% fewer violations at 1.1% cost penalty** (constraint-focused agent), or **88%/87% with 0.2% cost saving** (dual-objective). Exploration-enhanced PPO on Anytown/D-town reported up to **11.14% energy-cost saving** with 0.42 s online decision time ([Systems 11(2):56](https://www.mdpi.com/2079-8954/11/2/56)).
- **Chemical dosing.** RL-based decision support for coagulant and disinfectant dosing using multi-armed bandits across simulation, a scaled-down replica DWTP and a real DWTP ([Water Supply 24(1):86](https://iwaponline.com/ws/article/24/1/86/99400/Reinforcement-learning-based-DSS-for-coagulant-and)). Compare with the non-RL but *closed-loop and real* UCLA approach: self-adaptive cycle-to-cycle control of in-line coagulant dosing in UF pretreatment (Gao, Gu, Rahardianto, Christofides, Cohen 2017, *Desalination* 401:22–31, [doi:10.1016/j.desal.2016.09.024](https://doi.org/10.1016/j.desal.2016.09.024)).

### 5.3 Sim-to-real, safety, and offline RL

The systematic review by Kåge, Milić, Andersson and Wallén (2025, *Frontiers in Water*, [doi:10.3389/frwa.2025.1537868](https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2025.1537868/full)) screened 678 papers, retained 40 (2013–2024), and found DQN then PPO dominant, simulator-based training the norm in every domain except hydropower, and **real-world deployment minimal**. Named barriers: the reality gap, explainability, hyperparameter non-standardisation, constraint handling and reward design. Croll et al.'s 2023 review (*Crit. Rev. Environ. Sci. Technol.* 53:1775–1794, [doi:10.1080/10643389.2023.2183699](https://doi.org/10.1080/10643389.2023.2183699)) lists five adoption barriers: practical implementation, data management, integration with existing process models, trust in empirical control policies, and operator training.

Concrete mitigations in the literature:
- **Learned simulators.** Mohammadi, Ortiz-Arroyo, Stokholm-Bjerregaard, Hansen and Durdevic (2024, [arXiv:2403.15091](https://arxiv.org/abs/2403.15091)) attack compounding error in LSTM WWTP simulators by feeding model predictions back during training and adding a shape/dynamics term to the loss, improving Dynamic Time Warping by up to 98% over the base model on annual simulation.
- **Offline RL from historian data.** Yang, Wang, Li, Cui and Qiao (2025, *Neurocomputing* 636:129977, [doi:10.1016/j.neucom.2025.129977](https://doi.org/10.1016/j.neucom.2025.129977)) add a transition filter (discard low-performance transitions) and a prioritised approximation loss, with a VAE to bound distribution shift — the right family (BCQ/CQL/AWAC-style) when you have years of SCADA but cannot explore on a live plant.
- **Safety architecture that actually ships.** Keep RL at L2 (set-point selection) inside hard L1/L0 interlocks, clip actions to the same box constraints the MPC uses (`44 ≤ f_R ≤ 55`, `c_R ≤ 25 mS/cm`, `P_sys ≥ π_0/(1−Y)`), and fall back to the incumbent PI/DMC controller on any residual/constraint alarm. This is functionally the shielding approach and requires no new theory.

---

## 6. Fault detection, diagnosis and fault-tolerant control

### 6.1 Model-based FDI + reconfiguration (UCLA)

McFall et al. (2008) build per-actuator observers that decouple the ODEs using measured states:

```
dṽ_b/dt = (A_p/ρV)(P̃₁ − ½ ṽ_b² e_v1),  ṽ_b(0)=v_b(0)
dṽ_r/dt = (A_p/ρV)(P̃₂ − ½ ṽ_r² e_v2),  ṽ_r(0)=v_r(0)
r_b = |v_b − ṽ_b| ,  r_r = |v_r − ṽ_r|
```

where `P̃₁` uses (ṽ_b, v_r) and `P̃₂` uses (v_b, ṽ_r). A residual crossing its threshold `δ_ri` isolates the faulty actuator, and the supervisor switches configuration: `k = 2 if r_r > δ_rr` (spare retentate valve), `k = 3 if r_b > δ_rb` (spare bypass valve). The FTC precondition is redundancy — you must physically install fall-back actuators. Actuator faults propagate in ~1 s whereas feed disturbances act over hours, so FDI sampling must be fast even if the economic layer runs every 5 minutes. Related: Pascual et al. (2014), "Fault Detection and Isolation in Spiral-Wound RO Desalination," *Ind. Eng. Chem. Res.* 53:3257–3271 ([doi:10.1021/ie403603x](https://doi.org/10.1021/ie403603x)) and the companion data-driven plant models (Pascual et al. 2013, *Desalination* 316:154–161, [doi:10.1016/j.desal.2013.02.006](https://doi.org/10.1016/j.desal.2013.02.006)); scale detection by real-time membrane-surface imaging is in Bartman et al. (2011, *Desalination* 273:64–71).

### 6.2 Multivariate SPC: PCA, DPCA, adaptive PCA

Scale X (n×m) to zero mean/unit variance, decompose `X = TPᵀ + E`, retain `a` components, then monitor

```
T² = xᵀ P Λ_a⁻¹ Pᵀ x        (variation inside the model)
SPE (Q) = ‖(I − P Pᵀ) x‖²   (variation outside the model)
```

with control limits from an F/χ² approximation or, better for water data, **kernel density estimation** of the empirical statistic (Silverman bandwidth). Diagnosis uses **contribution plots**: `c_j^SPE = ((I − PPᵀ)x)_j²` per variable, and for T² the per-variable contributions `c_j^{T²} = Σ_i (t_i/λ_i) p_{ij} x_j`.

Two extensions matter for membranes: **dynamic PCA (DPCA)** — augment each observation with lags, `x_aug(k) = [x(k), x(k−1), …, x(k−l)]`, choosing `l` per variable by highest partial autocorrelation — and **adaptive PCA** — refit on a rolling window to track nonstationarity (fouling, temperature, membrane age). Together: **AD-PCA**.

**Full-scale evidence (SB-MBR, Colorado School of Mines):** Newhart/Hering and co-workers monitored 44 SCADA variables at 1-min resolution over Feb 2017–Sep 2018 in three blocks (53,226 / 241,915 / 184,318 observations), comparing single-state (SSAD-PCA) and multistate (MSAD-PCA, 16 SBR states / 44 MBR states) models ([ACS ES&T Water, PMC10928711](https://pmc.ncbi.nlm.nih.gov/articles/PMC10928711/)). A permeate-salinity drift was detected in **109 minutes with no false alarms** (SSAD-PCA, 90% cumulative variance, α = 0.10, 6-day training window). Recommended defaults: **90% cumulative variance, 6–7 day windows, α = 0.10**, state stratification chosen by covariance analysis rather than by arbitrary operating tags. "Configurations of AD-PCA detected every other fault studied in this paper, and none of these were detected by the typical UCL and LCL thresholds" — but slow multivariate TMP drift remained the hardest case.

**Full-scale evidence (UF for potable reuse, Calabasas CA):** Grimm, Branch, Thompson, Salveson, Zhao, Johnson, Hering and Newhart (2024, *ACS ES&T Engineering* 4:1492–1506, [doi:10.1021/acsestengg.4c00042](https://doi.org/10.1021/acsestengg.4c00042)) monitored 9 variables at 15-min sampling for 414 days (Apr 2021–May 2022) on pilot UF at 40 gfd, using ~12-day training sets (848 and 1052 observations) and detrending the monitoring variables (temperature-corrected permeability, filtrate turbidity, filtrate ammonia) on the explanatory variables via **adaptive lasso** (chosen over kNN, random forest and XGBoost by 10-fold CV RMSE). Best long-term configuration (12-day window, α = 0.005, alarm on 5 consecutive exceedances): **75.8% of the known-fault period flagged by T² (7.3% by SPE) at a 25.9% false-alarm rate during the known in-control period**, versus adaptive Shewhart charts that flagged 100% of the in-control period on filtrate ammonia (unusable) and 64% vs 26.8% on filtrate turbidity in the unknown period. The lesson: multivariate SPC on membranes works, but tuning (window length, α, consecutive-exceedance rule, detrending model) dominates performance, and false-alarm rates in the tens of percent are what untuned deployments actually produce.

### 6.3 Autoencoders and sensor validation

Reconstruction-error monitoring generalises SPE to nonlinear manifolds: train an AE on in-control data, alarm when `‖x − x̂‖² > τ`. Convolutional and LSTM autoencoders have been benchmarked on BSM2 for the five canonical sensor faults — **drift, bias, precision degradation, spike, stuck** — across scenarios varying fault order, intensity and duration, with convolutional AEs best on accuracy and detection delay ([Springer, 2023](https://link.springer.com/chapter/10.1007/978-3-031-23618-1_4); open-access thesis version [here](https://repositorio-aberto.up.pt/bitstream/10216/146754/2/597464.pdf)). For sensor *validation and reconciliation* (not just detection), Ba-Alawi, Vilela, Loy-Benitez, Heo and Yoo (2021, *J. Water Process Eng.* 43:102206, [doi:10.1016/j.jwpe.2021.102206](https://doi.org/10.1016/j.jwpe.2021.102206)) report a stacked denoising autoencoder achieving **detection rates of 74–98%** on influent-quality sensors while reconstructing the faulty signal so downstream control keeps running.

Practical sensor-drift handling on RO specifically still rests on **performance normalisation**: ASTM D4516 standardises permeate flow, salt passage and coefficient of performance to reference temperature/pressure/recovery ([ASTM D4516-19a](https://www.astm.org/d4516-19a.html)). Normalised permeate flow and normalised salt passage are the two trends that trigger CIP in nearly every plant; feeding *normalised* rather than raw variables into PCA/AE monitors removes most of the nuisance nonstationarity that otherwise forces aggressive adaptive retraining.

---

## 7. What has actually reached real plants

**Deployed / field-validated:**
- Multi-loop PI + DMC/CMPC on RO trains (Alatiqi 1989; Robertson 1996; Assef 1997; Burden 2001) — the industrial baseline.
- Supervisory SEC optimisation on a two-stage brackish plant with PI execution: 4.2–10% SEC reduction, field-tested (Gao et al. 2025, *Water* 17:2363).
- Nonlinear model-based flow/pressure control and SQP-based energy optimisation on UCLA's experimental RO system (Bartman 2009, 2010).
- MPC and ESC on a pilot CCRO system, closed loop on hardware (Chowdhury et al. 2024, 2025).
- Commercial ML advisory/optimisation layers on operating plants: **Synauta** manipulated HP pump flow, PX booster flow and PX valve-to-drain at an Osmoflo SWRO in Western Australia (4 trains × 1000 m³/day, 14 vessels × 6 elements) for a 6-month trial: **18% instantaneous and 9.7% average energy saving**, CIP frequency 12 → 9/yr (~10–15% less chemical), **$65,000/yr OPEX** at that plant and an extrapolated **>$3M/yr for a 300,000 m³/day plant** at $0.15/kWh and 2.5 kWh/m³ ([Smart Water Magazine](https://smartwatermagazine.com/news/synauta/machine-learning-delivers-energy-savings-desalination)). **Pani Energy** reports 2.2% energy reduction at an SWRO plant and $260,000/yr OPEX savings at a 6 MLD plant, with leadership quoting "5% to 7%" for mega-scale and "20% to 30%" for smaller plants ([Fortune, Jan 2024](https://fortune.com/2024/01/18/ai-make-business-better-water-industry)); Pani's integration with Aquatech LoWatt targets **2.7 kWh/m³** ([Water Online](https://www.wateronline.com/doc/solving-water-scarcity-aquatech-pani-consumption-sea-water-desalination-0001)).
- Supervisory ML + optimisation for pump scheduling in live distribution operations: EMAGIN HARVI at United Utilities' Oldham DMZ (55 MLD, 19 DMAs, 5 of 10 pump stations remotely controlled) — **22% average cost saving (17–45% range), £50,219/yr, 2.8 £/ML normalised, 5-month payback (2–7 months)** after a 12-week programme ([BlueTech case study PDF](https://www.bluetechforum.com/wp-content/uploads/Bluetech_Case-Study_EMAGIN_FINAL.pdf)). Note the vendor describes demand forecasting plus least-cost trajectory optimisation; third-party descriptions of HARVI also label it reinforcement learning, so treat the "RL in production" claim as vendor-level, not peer-reviewed.
- Adaptive-dynamic PCA monitoring on operating SB-MBR and UF trains, evaluated over 1–2 years of real SCADA (Hering/Newhart group).

**Simulation-only (as of mid-2026):** essentially all RL for RO — cascade DDPG/DQN (Golabi 2024), MARL two-stage RO (2025), PV-RO SAC/CNN-SAC (Soleimanzade 2022), DDPG TMP control (Bonny 2022); RL for aeration at the 14.3% (TD3/BSM1) and 34% (DQN/MBR model) figures; Koopman EMPC on BSM1; LSTM-MPC for CCRO (offline replay of pilot data); most autoencoder FDD benchmarked on BSM2.

---

## 8. Implementation notes

**Data you need (minimum viable).**
1. High-rate (1 s) L0/L1 tags: HP pump VFD %, motor power (kW), feed/permeate/concentrate flow, feed and interstage pressure, valve position feedback, feed/permeate/concentrate conductivity, temperature, pH. Power meters on *every* pump — you cannot optimise SEC from a plant-level kWh meter.
2. 1–15 min historised versions of the same tags plus CIP/backwash events, membrane replacement dates, and chemical dosing rates, for ≥12 months. AD-PCA training windows of 2–14 days and 90% cumulative variance are a reasonable starting grid; expect to tune α ∈ {0.005, 0.01, 0.05, 0.10} and a consecutive-exceedance rule.
3. Deliberate excitation campaigns: PRBS or multi-level steps on VFD speed and valve position at several recoveries and feed salinities. Budget dither into normal operation if the controller drives you to constant set-points (§2.4).
4. Normalise RO performance per ASTM D4516 before monitoring or modelling.

**Math and algorithms to implement.**
- Steady-state and dynamic RO model of §2.1–2.2 with the log-mean osmotic term and a piecewise-log valve characteristic; shooting method for the algebraic pressure in the high-recovery case.
- Subspace ID (N4SID) for a linear MIMO model; NARMAX/grey-box for cyclic processes; LSTM only if you have ≥100 cycles/months of varied data and can enforce input-domain guards.
- MPC: build the NLP with CasADi and solve with **IPOPT** (this is exactly the CCRO stack: LabVIEW/PLC at 1 s, Python MPC over the network, R or Python for estimation). For linear/Koopman models use OSQP/qpOASES and you will get millisecond solves.
- EMPC stability: add either a Lyapunov constraint (LEMPC), a terminal region + cost, or an average constraint on production/recovery; see Ellis, Durand and Christofides (2014).
- Parameter re-estimation every cycle or every N minutes by weighted least squares on the last window; monitor RMSR and bias of the forecast and refuse to apply MPC moves when forecast error exceeds a threshold.
- FDI: one observer per actuator with residual thresholds tuned on fault-free data; supervisory switching to redundant actuators; run at the fastest available rate.
- MSPC: PCA with lag augmentation, rolling-window refit, KDE thresholds, contribution plots; detrend monitoring variables on explanatory variables with adaptive lasso before charting.
- RL: implement as a set-point selector over an existing PI layer; use SAC or TD3 for continuous actions, DQN/PPO for discrete scheduling; train against a calibrated simulator *and* validate with offline RL (BCQ/CQL/AWAC-style) on historian data; use conservative action clipping to the MPC's constraint box.

**Software.** Python: CasADi + IPOPT (`cyipopt`), `do-mpc`, `scikit-learn` (PCA/PLS), `pyod`, PyTorch (LSTM/AE/Koopman), Stable-Baselines3 or RLlib, PettingZoo for MARL, `sippy`/`SIPPY` or MATLAB `n4sid` for subspace ID. Interfacing: OPC-UA or Modbus to the PLC, never direct actuator writes from the optimiser — write set-points only, with rate limits, watchdogs and a bumpless fallback to the incumbent PI/DMC controller.

**Expected returns, for a business case.** SEC reductions from supervisory optimisation on real plants cluster at **4–10%** (Gao 2025 field: 4.2/7.1/~10%; Synauta: 9.7% average, 18% peak; Pani: 2.2–7% on large plants). Chemical/CIP savings around **10–15%** (CIP 12 → 9/yr). Pump-scheduling savings in distribution are larger, **11–22%**, with **2–7 month paybacks**. Anything claiming >20% SEC reduction on a modern SWRO train with an ERD should be treated as extrapolation, not evidence.

**Sequencing advice.** Build the monitoring layer (normalisation + AD-PCA + contribution plots) first — it pays for itself, needs no actuator authority, and produces the labelled fault data your controller will later need. Then add supervisory economic optimisation with hard constraints and PI execution (the Gao/Bartman pattern), which is field-proven. Add MPC where the process is cyclic or strongly constrained (CCRO, batch RO, UF backwash scheduling). Treat RL as the last step, trained offline against a validated simulator plus historian data, deployed as a bounded set-point advisor with a supervised fallback.
