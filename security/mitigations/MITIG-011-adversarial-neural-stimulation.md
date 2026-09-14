# MITIG-011 — Adversarial Neural Stimulation

**Threat:** ASDR-011 — Adversarial Neural Stimulation

## Steps

1. **Contain** — disarm the closed-loop (no actuator/control command while under
   active stimulation), isolate the affected electrode groups, and stop writing
   those epochs into the identity/coherence memory.
2. **Identify** — which stimulation class hit: impulse burst, patterned drive,
   electrode-group poisoning, white-noise overlay, or amplitude elevation.
   Run the adversarial stress suite against the recorded baseline.
3. **Fix**
   - Re-run `adversarial_stress_test` with the observed signal; require the
     catastrophic/poisoned classes to be flagged before re-arming.
   - Keep a measured idle coherence baseline and compare every epoch to it.
   - Clamp reward memory growth; fail closed whenever coherence/integrity is
     indeterminate.
4. **Validate** — the suite's mean_security_score is >= 0.5 and the specific
   attacking class is detected; a poisoned sensory/motor injection no longer
   changes the decoded command.
5. **Regression** — store the sanitized epoch as an `INC`; update `ASDR-011`
   detection notes with the observed signature.

## Definition update
See the parent project's cognitive-robotics validation (celebrum `neurobot`,
s-ai `src/cognitive/`) for the reference suite to port into CI.