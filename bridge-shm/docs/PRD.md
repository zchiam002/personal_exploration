# Bridge Vibration Monitoring Platform — PRD v0.1

**Status:** Draft · **Date:** 14 Sep 2026 · **Owner:** [ ] · **Stakeholders:** bridge owner, NTU (Mark), [inspection partner]

## 1. Problem
The bridge owner needs to track modal frequencies, damping ratios and mode shapes of [bridge name] over time to detect structural change. The market incumbent (ARTeMIS Modal + SHM modules) exceeds the owner's needs and budget. A wired, common-clock DAQ with acceleration, temperature, strain/displacement and traffic channels is installed; no data has been recorded yet.

## 2. Goals (v1)
- Fully automated OMA on continuous ambient-vibration data, no analyst in the loop
- Modal-parameter history per mode, with environmental context
- Alerting on statistically significant change, enabled only after a baseline period
- Simple web dashboard the owner's engineer can read without OMA training

**Non-goals (v1):** EMA / impact testing, FE model updating, damage localisation, strain-based load rating (v2), multi-bridge fleet management, mobile app.

## 3. Users
- **Owner's engineer** (primary): checks dashboard weekly, receives alerts, exports reports
- **Research partner** (NTU): validates algorithms, tunes thresholds, accesses raw data
- **Platform operator** (us): monitors pipeline health, manages configs

## 4. Functional requirements
**Ingestion**
- FR1: Accept fixed-length raw files (30–60 min, 100–200 Hz, UTC timestamps) via scheduled auto-upload
- FR2: Validate on arrival: channel count, sample rate, gaps, clipping, dead channels; quarantine and flag failures
- FR3: Store raw data unmodified with a versioned metadata schema (sensor coordinates, orientations, sensitivities, DAQ config)

**Processing**
- FR4: Pre-process per window: detrend, decimate, band-pass, harmonic check
- FR5: Identify modes per window with SSI-cov (primary) and FDD (cross-check) via pyOMA2; output frequency, damping, mode shape and uncertainty bounds
- FR6: Automated stabilisation-diagram clustering; track modes against a signed-off reference set by frequency tolerance and MAC threshold; log unmatched modes
- FR7: Tag every window with mean temperature, traffic index and strain statistics
- FR8: Normalisation model (regression or PCA) trained on the baseline; store residuals alongside raw parameters

**Presentation**
- FR9: Dashboard: per-mode history (raw and normalised), MAC vs reference, environmental overlays, data-quality status, pipeline health
- FR10: Alerting: control charts on normalised residuals, configurable thresholds, alert log with acknowledgement; disabled until baseline sign-off
- FR11: Maintenance/event log linked to the timeline
- FR12: Monthly report export (PDF + CSV)

## 5. Non-functional requirements
- Results within 1 h of file arrival
- Raw data retained ≥ [5] years; processed history indefinitely
- Every result reproducible: algorithm version and config stored per window; full re-run supported
- Pipeline outage or missing file alerts the operator within 2 h
- Owner data access-controlled; hosting decision open (on-prem vs cloud)

## 6. Data specification
- Acceleration: [n] channels, 100–200 Hz, anti-alias filter on, raw units with sensitivities in metadata
- Temperature / strain / traffic: native rates, same clock, aligned to OMA windows
- File format: [TBD — one shake-down file to decide]

## 7. Phases
| Phase | Scope | Exit criterion |
|---|---|---|
| 0 (wk 1–2) | Recording protocol, shake-down record, sensor placement validated against hand calc / FE | First 3+ modes identified consistently across channels |
| 1 (wk 3–8) | Batch pipeline + descriptive dashboard | 90% of windows yield reference modes automatically |
| 2 (after ~3 months data) | Normalisation + alerting | Baseline signed off; false-alarm rate < [1]/month |
| 3 (v2) | Strain/traffic indicators, influence lines | — |

## 8. Success metrics
- Identification rate of reference modes per window
- Frequency coefficient of variation after normalisation (target < 1%)
- False alarms per month; mean time-to-result; pipeline uptime

## 9. Risks and open questions
- Sensor on a node line → mode invisible (mitigate in Phase 0)
- Sensor noise floor at < 1 Hz may hide the fundamental
- Baseline shorter than the full environmental range → unreliable alerts; agree on baseline length with owner up front
- pyOMA2 licence terms for commercial use — confirm
- Reference-mode definition: who signs off, and when
- Data ownership and hosting
- Does an FE model of the bridge exist?
