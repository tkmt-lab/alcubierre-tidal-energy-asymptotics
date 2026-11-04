# Numerical and verification formats

`rational-intervals.json` has a `method` string and 18 `rows`, ordered by
R=3/2,2,3 and η=128,512,2048,8192,32768,131072. Every row value is a string
representing an integer or exact fraction `numerator/denominator`.

| Fields | Meaning |
|---|---|
| R, eta, C, a, K | Parameters and constants in Theorem 1 |
| alpha_lo, alpha_hi | Rational enclosure of the inner ramp/harmonic junction α |
| beta_lo, beta_hi | Rational enclosure of the outer junction called ζ in the paper; these names do not denote the lower-bound parameter β |
| I_lo, I_hi | Bounds on the unsmoothed profile mass I |
| Jq_lo, Jq_hi | Bounds on its unsmoothed weighted energy Jq |
| smoothing_error | Explicit energy-error allowance Dη before normalization |
| family_J_lo, family_J_hi | Enclosure of the smoothed, normalized admissible family's J |
| scaled_family_lo, scaled_family_hi | The corresponding η(J−C) enclosure |
| scaled_infimum_lo, scaled_infimum_hi | Lower theorem bound and upper admissible-family bound for η(J*−C) |

Junctions use 256 rational bisection steps on the monotone brackets proved
in the paper. The square-root upper bound uses integer square root and a
power-of-two denominator. Decimal table endpoints are rounded outward to
nine places; the longer finite-example table uses twelve places. Fractions
are the authoritative endpoints. The upper endpoint is not an optimizer.

`constant-check.json` records 15 rational arithmetic checks for the analytic
parameter envelopes. The reduction to those envelopes remains part of the
paper's proof. `symbolic-result.json` contains the saved SymPy tensor and
contraction results. `quadrature-result.json` records a separate 120-digit
integration for all 18 mass/energy pairs. These stored records do not by
themselves constitute a new run, formal proof or human review.

`verify.py` regenerates the finite artifacts in isolation, compares them
byte-for-byte, and separately checks the coefficient identity, parameter
coverage, ordering, and the explicit lower/upper error constants using
fractions. `negative_controls.py` invokes this checker on altered copies,
without relying on distribution hashes. This tests that finite data changes
are detected; it does not provide a second proof of the uniform theorem.

`MANIFEST.sha256` is the distribution inventory; `provenance.json` relates
copied inputs to the exported files. The manifest excludes itself, Git
metadata and explicitly ignored build/check caches. Changing a generated
file requires a justified update and regenerated manifest, not weakening
the checker to accept altered evidence.
