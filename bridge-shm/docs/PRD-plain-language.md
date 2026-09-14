# Bridge Vibration Monitoring Platform — PRD v0.1, plain-language edition

**What this is:** a companion to PRD v0.1 (`docs/PRD.md`) for readers without a vibration-engineering background. It says the same things in everyday language and explains every technical term in the glossary at the end. Where the two differ, the original PRD is the reference. Placeholders in [brackets] are still to be filled in.

**Status:** Draft · **Date:** 14 Sep 2026 · **Owner:** [ ] · **Stakeholders:** bridge owner, NTU (Mark), [inspection partner]

## The idea in one paragraph
Every bridge vibrates slightly all the time, from traffic, wind and even people walking. The way it vibrates is like a fingerprint. Each bridge has a set of natural "notes" it prefers to vibrate at (its frequencies), a rate at which those vibrations die away (damping), and characteristic patterns of movement (mode shapes). If the structure changes because a bearing seizes, a cable loosens or a crack grows, that fingerprint shifts. This platform listens to the bridge continuously, works out its fingerprint every hour, and tells the owner's engineer when it changes in a way that weather and traffic cannot explain.

## 1. The problem
Sensors are installed on [bridge name]: accelerometers (motion sensors), thermometers, strain and displacement gauges (which measure stretch and movement) and traffic counters, all wired to one recorder that time-stamps everything against the same clock. Nothing has been recorded yet. The owner wants to track the bridge's vibration fingerprint over the years to spot structural change early. The established commercial product, ARTeMIS Modal with its monitoring add-ons, does far more than this bridge needs, at a price to match. We are building a simpler tool that does just this job.

## 2. What version 1 must do
- Work without a specialist. The software finds the fingerprint on its own from ordinary everyday vibration; nobody has to sit at a screen and interpret it.
- Keep a history. For each note of the bridge, a timeline of its frequency, damping and shape, alongside the temperature, traffic and strain at the time, because these change the fingerprint too.
- Raise the alarm only when it means something. Alerts are based on statistics and are switched on only after a "getting to know the bridge" period, called the baseline.
- A simple web page the owner's engineer can read without any vibration training.

**What version 1 will not do:** shaking or hitting the bridge deliberately to test it (EMA, impact testing); tuning a computer model of the bridge to match the measurements (FE model updating); pointing to where damage is (damage localisation); estimating how much load the bridge can carry from strain readings (load rating, planned for version 2); managing several bridges at once; a phone app.

## 3. Who uses it
- **Owner's engineer** (main user): looks at the dashboard about once a week, receives alerts, exports reports.
- **Research partner (NTU):** checks that the methods are sound, tunes the thresholds, works with the raw data.
- **Platform operator (us):** keeps the processing running and manages the settings.

## 4. What the system must do, step by step

**Getting the data in**
- FR1: The recorder produces one file every 30–60 minutes, sampling each sensor 100–200 times per second and stamping the time in UTC (universal time, so there is no time-zone confusion). Files are uploaded automatically on a schedule.
- FR2: Each file is checked on arrival: the right number of channels, the right sampling rate, no missing stretches (gaps), no readings stuck at the sensor's maximum (clipping), no sensors that have gone silent (dead channels). Files that fail are set aside ("quarantined") and flagged. They are never silently used.
- FR3: The original data is stored exactly as recorded and never modified, together with a description of the set-up: where each sensor is, which way it points, how it converts motion to numbers, and how the recorder was configured. That description is version-numbered so we always know which set-up produced which data.

**Working out the fingerprint**
- FR4: Each block of data is cleaned first. Slow drifts are removed (detrend), the sample rate is reduced to what is needed (decimate), frequencies outside the range of interest are filtered out (band-pass), and there is a check for steady vibration from machinery or mains electricity (harmonics) that could be mistaken for the bridge.
- FR5: Two independent methods extract the fingerprint from each block: SSI-cov as the main method and FDD as a cross-check. Both come from the open-source pyOMA2 library. For each note they give a frequency, a damping value, a mode shape and an estimate of how confident to be (uncertainty bounds).
- FR6: SSI-cov produces many candidate answers. The software groups the consistent ones automatically (stabilisation-diagram clustering) and matches each group to an agreed list of the bridge's known notes, the reference set, by checking that the frequency is close enough and the shape is similar enough (MAC score). Anything that does not match is logged rather than discarded.
- FR7: Every block is tagged with the average temperature, a traffic-intensity number and strain statistics for that period.
- FR8: Temperature and traffic shift the fingerprint by themselves: a hot deck is slightly less stiff, and a queue of lorries adds mass. A statistical model learned during the baseline predicts this everyday shift. What is left after removing it (the residual) is what could indicate real change. Both the raw and the corrected values are stored.

**Showing the results**
- FR9: Dashboard. A timeline for each note, raw and corrected; how well today's shape still matches the reference (MAC); temperature and traffic overlays; data-quality status; and whether the processing is running.
- FR10: Alerting. A control chart (a running chart with statistical limits) on the corrected values. Thresholds are adjustable, alerts are logged and must be acknowledged, and the whole thing stays off until the baseline is signed off.
- FR11: A diary of maintenance and events, linked to the timeline, so that a jump in the data can be matched to "resurfacing, lane 2".
- FR12: A monthly report as PDF and CSV.

## 5. How well it must work
- Results within one hour of a file arriving.
- Raw data kept for at least [5] years; the processed history kept indefinitely.
- Every result can be reproduced: the software version and settings used are stored with each block, and everything can be re-run from scratch.
- If the processing stops or a file goes missing, the operator is told within two hours.
- Only the owner's people can see the owner's data. Whether to host on the owner's premises or in the cloud is still open.

## 6. What the data looks like
- Motion: [n] accelerometers sampled 100–200 times per second, with a filter that stops fast vibrations from masquerading as slow ones (anti-alias filter). Values are stored as the raw sensor output, and the conversion factors (sensitivities) live in the set-up description.
- Temperature, strain, traffic: recorded at their own natural rates, on the same clock, lined up with the vibration blocks.
- File format: [TBD — one shake-down file to decide]. We will decide after seeing the first real recording.

## 7. Plan
| Phase | What happens | Done when |
|---|---|---|
| 0 (weeks 1–2) | Agree how to record; make a first trial recording (the shake-down); check that the sensors are in sensible places against a hand calculation or a computer model of the bridge | The first three or more notes of the bridge show up clearly and consistently on every sensor |
| 1 (weeks 3–8) | Build the automatic processing chain and a dashboard that shows the history | Nine blocks in ten yield the reference notes with no human help |
| 2 (after about 3 months of data) | Add the weather-and-traffic correction and switch on alerting | Baseline signed off; fewer than [1] false alarm per month |
| 3 (version 2) | Use strain and traffic data for load-related indicators and influence lines | — |

## 8. How we will know it works
- How often each reference note is found per block of data.
- How much the corrected frequencies still wander (aim: a spread of less than 1%).
- False alarms per month; how long results take; how often the processing is up.

## 9. Risks and open questions
- A sensor placed at a point that does not move for a given note will never see that note (a "node"). Phase 0 checks for this.
- The sensors may be too noisy below 1 Hz to see the bridge's slowest and most important note.
- If the baseline is shorter than a full cycle of weather, alerts will be unreliable. Agree the baseline length with the owner up front.
- pyOMA2's licence must be checked for commercial use.
- Who signs off the reference set of notes, and when.
- Who owns the data, and where it is stored.
- Does a computer (finite-element) model of the bridge already exist?

## Glossary
Alphabetical, in plain terms.

- **Accelerometer:** a sensor that measures how quickly motion changes. The basic vibration sensor.
- **Ambient vibration:** the small, ever-present vibration from traffic, wind and ground motion, with no deliberate shaking. Free, continuous, and enough for OMA.
- **Anti-alias filter:** if you sample too slowly, fast vibrations can masquerade as slow ones, like wagon wheels appearing to spin backwards on film. The anti-alias filter removes the fast content before sampling so this cannot happen.
- **Band-pass:** keep only the frequencies between two limits and discard the rest.
- **Baseline:** the initial period, about three months here, in which the system learns what "normal" looks like across the range of weather and traffic. No alerts are raised during it.
- **Channel:** one sensor's stream of numbers.
- **Clipping:** a signal so large that the sensor or recorder hits its maximum and flattens the peak. The recording is then unreliable.
- **Coefficient of variation (CoV):** spread divided by average, as a percentage. "Frequency CoV under 1%" means the corrected frequency wanders by less than 1% of its value.
- **Control chart:** a timeline with a centre line and upper and lower limits derived from the baseline scatter. Points outside the limits trigger an alert.
- **DAQ (data acquisition system):** the recorder that turns sensor signals into numbers and time-stamps them.
- **Damage localisation:** working out where on the structure the damage is. Not in version 1.
- **Damping ratio:** how quickly a vibration dies away once started, as a percentage. Bridges typically sit around 0.5–2%. It can change with damage but is also naturally noisy.
- **Dead channel:** a sensor that has stopped responding and shows a flat line.
- **Decimate:** reduce the sample rate by keeping every n-th sample after filtering, to speed up processing.
- **Detrend:** remove a slow drift or offset from a signal before analysis.
- **Displacement:** movement of a point on the structure, in millimetres.
- **EMA (experimental modal analysis):** finding the fingerprint by shaking or hitting the structure with a known force. Not in version 1. OMA uses ambient vibration instead.
- **FDD (frequency domain decomposition):** a quick OMA method that looks at where the vibration energy peaks across frequency. Used here as a cross-check.
- **FE model (finite-element model):** a computer model of the structure built from many small pieces. It can predict the fingerprint. "Updating" it means tuning it to match measurements.
- **Frequency (natural or modal frequency):** the number of times per second the bridge naturally vibrates in a particular pattern, like the note a guitar string plays. For most bridges the important ones lie between about 0.5 and 10 Hz.
- **Harmonic:** vibration at one fixed frequency and its multiples, produced by rotating machinery or mains electricity (50 Hz), not by the bridge. It must be recognised so that it is not mistaken for a bridge note.
- **Hz (hertz):** cycles per second.
- **Influence line:** how a response at one point, say strain at mid-span, changes as a load moves across the bridge. Version 2.
- **Load rating:** estimating how much load a bridge can safely carry. Version 2.
- **MAC (modal assurance criterion):** a similarity score between two mode shapes, from 0 (unrelated) to 1 (identical). Above roughly 0.8–0.9 they are treated as the same note.
- **Mode, mode shape:** one natural pattern of vibration, for example the whole deck bowing up and down, or twisting, and the picture of that pattern along the bridge.
- **Node (of a mode):** a point that does not move in a particular mode. A sensor placed there is blind to that mode.
- **Normalisation:** removing the predictable effect of temperature and traffic from the measured values, so that what remains reflects the structure.
- **OMA (operational modal analysis):** finding the fingerprint from ambient vibration alone, with no controlled shaking. This is what the platform does.
- **PCA (principal component analysis):** a statistical way of separating the main patterns of variation in data. One candidate for the normalisation model.
- **PSD (power spectral density):** a chart of how much vibration energy there is at each frequency. The bridge's notes show as peaks.
- **pyOMA2:** an open-source Python library that implements OMA methods, including SSI-cov and FDD.
- **Quarantine:** set a file aside and flag it because it failed a check, without deleting it.
- **Reference set:** the agreed list of the bridge's notes (frequency and shape) that every new block is matched against. It needs a formal sign-off.
- **Regression:** fitting a formula, for example frequency against temperature, to data so that the predictable part can be removed.
- **Residual:** what is left after the predictable part is removed. This is the quantity watched for change.
- **Sample rate:** how many readings per second are recorded, here 100–200.
- **Sensitivity:** the conversion factor from a sensor's electrical output to physical units.
- **Shake-down:** a first trial run to find problems in the recording set-up before routine operation.
- **SSI-cov (covariance-driven stochastic subspace identification):** the main OMA method. It fits a mathematical model of the vibrating structure directly to the recorded data and gives accurate frequencies, damping values and shapes.
- **Stabilisation diagram:** SSI produces candidate notes for a range of model sizes. Plotted together, real notes line up as stable columns while spurious ones scatter. Clustering picks out the stable columns automatically.
- **Strain:** how much a piece of material stretches or compresses, in parts per million. Measured by strain gauges.
- **Traffic index:** a single number summarising how much traffic crossed the bridge during a block.
- **Uncertainty bounds:** the range within which the true value probably lies, reported alongside each result.
- **UTC:** Coordinated Universal Time, the common global time reference. It avoids time-zone and daylight-saving confusion.
- **Window (block):** one stretch of data, 30–60 minutes long, processed as a unit.
