# Market-State Embeddings for Ride-Hailing / Food Delivery

**Goal (company's framing):** eliminate feature engineering by encoding all raw data into a single
embedding that represents the market state at time *t* — demand, supply, weather, everything.

**Working hypothesis (ours):** a plain encoder–decoder will not produce a usable latent space.
The latent space must be *organized* via auxiliary heads, and since we cannot train against every
conceivable head, we need a principled way to choose a small set of **representative heads**.

---

## 1. Why a pure autoencoder is not enough

A reconstruction objective preserves information in proportion to its contribution to
reconstruction loss, **not** in proportion to its downstream decision value:

- High-variance, low-value signal (GPS jitter, per-request noise) eats latent capacity.
- Low-variance, high-value signal (surge onset, supply cliff at shift change) can be discarded
  almost for free in reconstruction terms.
- Even when information *is* preserved, it may be buried non-linearly, so downstream consumers
  (often linear layers or small MLPs on top of the embedding) can't reach it. "Information present"
  ≠ "information accessible."

So the intuition is right: the latent space needs external pressure to sort itself out.
Auxiliary heads are that pressure.

## 2. The finance analogy, mapped properly

The finance heads (vol, Sharpe, 20d SMA) are not arbitrary — they follow a hidden pattern:
**{level, trend, second moment, risk-adjusted ratio} of the core quantity (returns/price)**.
That pattern transfers. The marketplace analogue of "price/returns" is not one series but a
small set of core quantities:

| Finance concept        | Marketplace analogue                                            |
|------------------------|-----------------------------------------------------------------|
| Price / returns        | Surge multiplier, effective price, earnings-per-hour            |
| Volatility             | Demand/supply arrival-rate variance over trailing windows       |
| SMA / momentum         | Demand trend vs. baseline (e.g., 15-min rate vs. 4-week median) |
| Bid-ask spread / depth | **Marketplace liquidity**: open requests vs. idle supply, time-to-match, fill rate |
| Sharpe ratio           | Utilization efficiency: earnings or completed trips per unit of idle time |
| Term structure         | Multi-horizon demand/supply forecast curve (15m / 1h / 4h / 1d) |
| Regime (bull/bear)     | Regime class: rush hour, weather shock, event spike, holiday, normal |

The key insight: finance converged on those statistics because they are approximately
**sufficient statistics for the decisions traders make**. We should derive our heads the same
way — from the decision family, not from the data.

## 3. Selection principle for representative heads

> A head is representative if many downstream decisions are (approximately) functions of it.

Concretely, take the cross product of three small sets:

**Core quantities** (the marketplace's "state variables"):
1. Demand rate λ_d (requests / orders)
2. Supply rate λ_s (idle drivers / couriers, inflow/outflow)
3. Matching friction (time-to-match, pickup ETA, fill rate)
4. Price signal (surge, delivery fee, incentives in effect)
5. Unit economics (earnings/hour, cost per fulfilled order)

**Statistical moments** (the finance pattern):
- Level (current value)
- Trend (short-window derivative vs. seasonal baseline)
- Volatility (trailing variance)
- Tails (upper/lower quantiles — extremes drive surge and SLA breaches)

**Horizons**:
- Nowcast, +15 min, +1 h, +4 h (different decisions live at different timescales:
  dispatch is minutes, repositioning is tens of minutes, incentives are hours)

5 quantities × 4 moments × ~3 horizons ≈ 60 scalar targets — large but tractable, and *chosen
once, centrally*, rather than re-derived per downstream model. Prune by:

- **Decision coverage:** every major downstream system (pricing, dispatch, ETA, repositioning,
  incentives, forecasting) must have ≥2 heads it directly depends on.
- **Diversity:** drop heads whose targets correlate > ~0.9 with an already-selected head —
  redundant heads add gradient conflict without adding information pressure.

## 4. Make the heads *linear* — this is the enforcement mechanism

If auxiliary heads are deep MLPs, the encoder can bury information non-linearly and still
satisfy the head — defeating the purpose. Constrain heads to be **linear (or 1 hidden layer at
most)** probes on the embedding. This forces the encoder to lay information out in a linearly
accessible geometry, which is exactly what "the latent space sorted out properly" means
operationally. Cheap heads also make it feasible to run many of them.

## 5. Heads are not the only tool — combine objectives

| Objective | What it buys |
|---|---|
| Auxiliary heads (above) | Decision-relevant info is present *and accessible* |
| Masked / future prediction in **latent space** (JEPA-style, not pixel-level reconstruction) | Temporal structure without wasting capacity on noise |
| Contrastive (same zone adjacent time = positive; different regime = negative) | Regime separation, smooth temporal trajectories |
| Variance/covariance regularization (VICReg-style) | Prevents dimensional collapse when heads dominate |
| **Factorized latent**: dedicate embedding sub-blocks to demand / supply / exogenous / economics, attach heads per block | Interpretability, debuggability, partial reuse |

Exogenous data (weather, events) should be **inputs**, not prediction targets — we don't need
the embedding to forecast rain, we need it to encode rain's *effect* on the market. That effect
is captured automatically if the future-demand/supply heads are conditioned on the embedding.

## 6. Evaluation: the real test of "no more feature engineering"

The heads we train on are, by construction, well-represented. The claim we actually need to
validate is generalization to tasks we did *not* train on:

1. **Held-out linear probe suite** — a battery of downstream targets *excluded* from training
   heads (e.g., cancellation rate, courier churn signal, batch-ability of orders). Embedding
   must beat (or match) the hand-engineered feature baseline under an identical linear probe.
2. **Production swap test** — take one real model (ETA is a good first candidate), replace its
   feature vector with the embedding, demand metric parity in offline replay before any A/B.
3. **Regime stress slices** — evaluate probes specifically on rare regimes (storms, concerts,
   New Year's Eve). Averages hide exactly the failures that matter here.

## 7. Honest caveats

- **Feature engineering doesn't disappear — it moves up a level.** Choosing heads, inputs, and
  granularity *is* feature engineering, done once and centrally. That's still a major win
  (consistency, reuse, single pipeline) but the pitch "zero feature engineering" oversells it.
- **Granularity:** "market state" is really per (geo hex × time bucket × vertical), probably
  hierarchical (city-level + hex-level embeddings). Needs its own design doc.
- **Non-stationarity & versioning:** markets drift; the encoder gets retrained; the latent
  space rotates; every downstream consumer breaks. Need embedding version compatibility
  (distillation / alignment loss between versions). This is the biggest *operational* risk.
- **Leakage:** future-horizon heads must respect information availability at time *t* —
  easy to get wrong with late-arriving data (completed-trip records, weather backfill).

## Open questions for next session

- [ ] Which downstream systems commit to being the first embedding consumers? (Determines head pruning.)
- [ ] Spatial structure: per-hex embeddings with neighbor-prediction heads, or city-level with hex queries?
- [ ] One encoder for both ride-hailing and food delivery, or two encoders with a shared trunk?
- [ ] Embedding dimension budget and the update cadence (streaming vs. batch refresh)?
