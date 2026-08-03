# When the Market State Contains Your Own Hand: Surge & Surge Radius as Levers

Companion to [00_problem_and_head_selection_framework.md](00_problem_and_head_selection_framework.md).
Produced by a 5-lens analysis (causal inference, RL/world-models, marketplace economics,
spatial dynamics, ML architecture) followed by an adversarial critique pass. Claims below are
the ones that **survived** the critique; corrections the critique forced are marked ⚠.

---

## 1. The problem in one paragraph

Surge and surge radius are not observations of the market — they are **actions** chosen by a
policy π to steer fulfilment and CSAT. Every logged outcome was generated *under* π, and the
embedding is destined to feed the very systems that set those actions. This breaks the doc-00
design in specific, fixable ways — but also in one way that no architecture can fix without an
operational change (see §3).

## 2. The headline failure mode: the sign flip

Surge **causally raises** fulfilment (attracts supply, suppresses demand), but the policy fires
surge precisely where fulfilment was about to crater. So in logged data, high surge *predicts*
low fulfilment. A fulfilment probe trained on the doc-00 heads will load **negatively** on the
surge direction — handing any pricing consumer the exact wrong lever gradient. A consumer that
trusts it would cap or shrink surge, deepening the deficits surge exists to fix. This is the
single most dangerous concrete failure and the reason "just add a fulfilment head" is not safe.

## 3. The identification wall (the part architecture cannot fix)

Under a (near-)deterministic policy a = π(s), logged data has **zero overlap** in (state,
action): for a given state you only ever observe one action. Then E[Y | do(a), s] is not
biased — it is **unidentified**. No encoder, head design, or data volume recovers it.

**Consequence:** modest, guardrailed, *logged* randomization of the levers (surge-step jitter,
radius jitter, driver-incentive randomization) is a **precondition** for any elasticity-shaped
head — an identifiability tax, not an experiment. It cannot be backfilled: data collected
without it is permanently unusable for causal heads.

⚠ Critique correction: jitter identifies **local** derivatives near the current policy, not
global counterfactuals. The system must publish a refusal boundary — which counterfactual
queries it answers (small perturbations, on-support) and which it refuses (surge levels/states
never explored). Regulatory surge caps mean tail states stay unidentified *forever*; say so.

## 4. The state/action contract (core design rule)

This is the main amendment to doc 00's architecture:

- **Past actions a_{<t} are encoder inputs.** They shaped current supply positioning and rider
  expectations; excluding them breaks Markov sufficiency.
- **The concurrent action a_t never enters the embedding z_t.** If it leaks in, counterfactual
  queries become meaningless and the policy sees its own action reflected in its state input.
- **Every policy-influenced outcome head becomes action-conditioned:** y = f(z_t, a_t),
  implemented as a low-rank bilinear probe
  `ŷ = dᵀz + cᵀφ(a) + φ(a)ᵀ W z` with a *fixed hand-specified* action basis φ(a).
  For fixed a the map z→ŷ is affine, so doc 00's linear-probe discipline survives, and
  `∂ŷ/∂a` — the state-dependent elasticity — is available in closed form.

⚠ Critique correction: the bilinear form is the right **interface** but confers **zero
identification**. On the policy manifold a ≈ π(z), the split between the z-term and the
action-term is pure collinearity — the regularizer, not the data, picks the coefficients.
Action coefficients mean something *only where fit on randomized slices*.

- **Leakage is temporal, not just columnar.** "Effective price," conversion, even request
  counts during bucket t already embed a_t (riders saw the surge before converting). Encoder
  inputs must be snapshotted as-of the action-commit timestamp. Enforce with a CI perturbation
  test: flip a_t in raw logs, rebuild features, assert z_t is bit-identical.

## 5. What NOT to do (mistakes the lenses themselves made)

1. **Do not enforce independence between the embedding and the action.** A good Markov state
   *should* predict a state-dependent policy's action — high action-probe accuracy is not
   leakage. Independence penalties force the encoder to delete genuine market state. The sound
   audit: z_t must not predict the **randomized component** of a_t beyond chance (stop-gradient
   diagnostic probe, wired into CI). Measure policy invariance via cross-era transfer; don't
   try to architect it in with adversarial losses (policy versions confound with calendar time).
2. **Remove policy-forecast heads from the shared substrate.** Doc 00's "price signal ×
   {level, trend} × {+15m, +1h}" cells forecast *the company's own future actions* — training
   them distills π into the embedding, invalidated by construction at every retune. If driver
   UX needs surge forecasts, ship a separate, explicitly policy-versioned model.
3. **Don't apply the corr>0.9 pruning rule across causal classes.** Levels and derivatives
   correlate under a stationary policy and decouple exactly when the policy changes — which is
   when the embedding is needed. Doc 00's framework gains a **fourth axis**:
   {quantities} × {moments} × {horizons} × **{causal status: observational level | structural
   derivative}**. Prune within a causal class, never across.
4. **Never publish fulfilment as a ratio head.** Numerator and denominator are both endogenous
   to the lever — a policy can hit fill-rate targets by suppressing demand, and the embedding
   would certify a demand-destroyed market as healthy. Publish components (pre-exposure demand
   proxy, realized requests, supply, matches); derive rates downstream.
5. **Don't trust "raw counts are policy-invariant."** ⚠ Logged requests are suppressed by
   displayed prices; idle-driver counts are reshaped by surge-driven repositioning. Only
   pre-exposure funnel signals (app opens before any quote) are approximately policy-invariant.
6. **Elasticities are not "Lucas-stable deep parameters."** ⚠ They drift with UX changes,
   habituation, competitor behavior, and boundary-gaming. Treat them as slowly-varying,
   versioned quantities with a permanent re-estimation pipeline; drop the word "invariant."

## 6. Spatial structure: radius makes the action a field

- Surge over a radius **reallocates conserved short-run supply**: it pulls drivers from ring-1/2
  neighbors (supply cannibalization, ~5–15 min timescale) and displaces price-sensitive riders
  across the boundary. Own-elasticity of fulfilment is positive; cross-elasticity w.r.t.
  neighbor surge is strongly negative. Per-hex-independent embeddings encode these spillovers
  as mysterious local volatility — policy artifacts masquerading as market structure.
- **Design rule: heads receive actions; encoders receive states.** Action-conditioned heads get
  the ring-aggregated neighbor action field; the encoder gets neighbor *states* via 2–3-hop
  graph attention with **travel-time edges, not geodesic adjacency** (rivers and highways break
  H3 adjacency). Hierarchical city+hex latent with a city-level conservation head (total idle
  driver-hours + allocation shares) distinguishes "surge grew the pie" from "surge moved it."
- **Per-hex A/B tests of lever policies are structurally invalid** (treated hexes cannibalize
  control-hex supply → inflated or sign-flipped lift). Use city/region switchbacks (blocks ≥ 2h,
  burn-in, autocorrelation-robust analysis) plus cluster randomization with clusters cut from
  the historical driver-flow graph and donut estimation at boundaries.
- This **resolves doc 00's open spatial question**: neighbor-aware encoding is mandatory, not
  optional — the radius lever makes cross-zone flux part of the state.

## 7. The feedback loop (embedding → policy → data → embedding)

Once the embedding feeds the pricing policy, future training data is generated by that policy:
never-surged zones produce no counterevidence, blind spots self-confirm, and each retraining
generation narrows the action distribution further (recommender-style echo, arriving over
quarters). Governance that survives scrutiny:

- Never retrain the encoder purely on data generated by a policy consuming that encoder — always
  mix exploration and holdout data.
- Record the (encoder version, policy version) pair on every training row; co-version them.
- Monitor predicted-vs-realized outcomes **specifically on explored (off-policy) actions** —
  the early-warning channel for performative self-confirmation.

## 8. Log now, model later (highest-confidence, lowest-regret action)

Everything causal downstream depends on telemetry that is cheap today and unrecoverable
retroactively:

1. Policy version **and config hash of parameters actually in force** per hex-hour (release
   tags mislabel regimes).
2. The policy's running variables (imbalance index, thresholds) and the realized action field
   (multiplier, radius/surface) with **commit timestamps**.
3. Exploration flags and propensities for any stochastic component.
4. Full pre-exposure funnel: app opens, quote impressions, price/ETA shown, accept/abandon.
5. Shadow-policy actions (what the default policy would have done) and candidate-action score
   tables where available.
6. Spatial decomposition events: idle-trajectory hex crossings without dispatch (repositioned
   inflow), session-start hexes (new-online), cross-hex session drift (displaced demand).

## 9. Evaluation extensions (beyond doc 00 §6)

- **Cross-policy-era transfer (the practical Lucas test):** fit probes on data under policy vN,
  test under vN+1. Run it on *existing historical logs today* to measure how big the problem
  actually is before funding mitigations. Becomes a release gate for embedding versions.
- **Randomized-slice interventional calibration:** on jittered traffic, compare head(z, a)
  against realized outcomes across action deltas; report elasticity *sign agreement* first.
- **Support/overlap monitor as a product surface:** publish action-density per z-neighborhood
  next to the embedding so consumers know where counterfactual queries are estimates vs.
  extrapolations; refuse to certify off-support regions.
- **Per-head contract labels:** every head/probe ships tagged "approximately policy-invariant"
  or "policy-conditional, valid under policy vX" — retunes trigger targeted invalidation
  instead of silent rot.
- ⚠ Do **not** make zone-time CATE-prediction probes release-blocking: switchbacks power
  aggregate effects, not zone-time effects; probing against noise produces arbitrary blocks.

## 10. Statistical and institutional reality checks (from the critique)

- **Power budget before head design:** the fulfilment effect of a 0.1 surge tick on one
  hex-hour is far below outcome noise. With 1–5% jittered traffic, elasticity labels are
  estimable only pooled to ~city × regime level. Design heads at the granularity the power
  analysis supports, not the granularity the vision wants.
- **Verify the real action interface first.** Many production systems use per-hex surge
  surfaces (no explicit "radius" knob) and upfront pricing (no rider-visible multiplier) —
  several proposed heads (multiplier-bucket abandonment, boundary pin-dropping) assume
  mechanisms that may not exist here. Derive φ(a) from the actual pricing-system schema.
- **Rider-facing price randomization is legally fraught** (price discrimination/gouging
  exposure); driver-side incentive randomization is the realistic workhorse instrument.
- **Food delivery is missing from the analysis so far.** Dual-mode drivers mean ride surge
  cannibalizes food-delivery supply — a first-order cross-vertical spillover that bears
  directly on doc 00's one-encoder-vs-two question. Needs its own session.
- **Surge is not the only lever.** Dispatch policy, batching, courier incentives, and ETA
  display have identical endogeneity; conditioning on surge alone leaves residual policy
  confounding.

## 11. Recommended sequencing (buy the causal program incrementally)

1. **Now (no model changes):** logging (§8) + modest exploration + run the cross-era severity
   measurement on historical logs to size the Lucas problem.
2. **In parallel:** ship embedding v1 to **passive consumers only** (ETA, forecasting,
   monitoring) under an explicit "policy-conditional — not valid for counterfactuals" contract.
   Pricing stays on purpose-built causal models.
3. **Only after randomized data accumulates:** bilinear action-conditioned heads trained on
   identified slices; quote-level conversion head (quasi-experimental demand-curve data that
   partially de-confounds even earlier).
4. **Only after a measured case exists:** the full causal-embedding apparatus (policy-context
   block, cross-policy release gates, elasticity products). No lever-setting consumer touches
   the embedding until its action-conditioned heads validate on randomized data.

## Open questions carried forward

- [ ] What is the actual action schema of our pricing system (surface vs. multiplier+radius, upfront vs. visible multiplier)? Blocks φ(a) design.
- [ ] How severe is cross-era probe degradation on our historical logs? (Sizes the whole program.)
- [ ] Cross-vertical spillover: shared encoder with vertical-specific blocks, or two encoders? (Food delivery session needed.)
- [ ] Who owns the permanent exploration budget and its revenue/CSAT cost — and who arbitrates when a causal eval gate blocks a pricing launch?
