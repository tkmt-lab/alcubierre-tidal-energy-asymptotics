# Verification record — v1.2

This supplement separates the analytic argument, computational corroboration,
AI review, statement type-checking, and distribution preparation.

## Mathematical result

Theorem 1 concerns the specified stationary one-component Alcubierre metric
at v=1/10, globally C² monotone radial profiles with exact matching at 1 and
R∈[3/2,3], the Eulerian normal, and the all-angle Euclidean operator norm of
the electric part of the full Riemann tensor divided by v². It gives
feasibility for η≥128, the explicit finite lower bound, and the uniform
coefficient 1/[3R(R−1)³], with error constants 5 and 61000.

The proof combines a universal lower bound from the axial necessary
condition with an all-angle sufficient estimate for an explicitly smoothed
and normalized family. Neither angular sampling nor an assumed optimizer
replaces those analytic arguments. The four remainder sources, including
the shifted ramp, are explicitly bounded. The large upper constant is a
convenient valid bound rather than an estimate fitted to finite observations.

## Derivation and review history

The initial drafting reconciled two supplied analytic derivations, one of
which was produced before access to the other proof. They use the same fixed
claim; this is a proof-access distinction, not human peer review or independent
physical-model selection. A supplied AI review raised eight minor issues.
Version 1.1 resolved those issues and a second supplied AI review accepted
that revision, leaving two nonblocking wording points. No new reviewer or
agent was invoked to prepare v1.2.

Version 1.2 makes the convolution implication explicit: a positive derivative
requires the convolution window to meet the increasing interval, hence the
stated upper bound on r. It also states directly that the Lean file is a
weaker consequence with existential error constants. These are exposition
changes; mathematical formulas and exact interval data are unchanged.

## Executed calculations and default checks

The supplied symbolic record was produced with SymPy 1.14.0. Christoffel and
Riemann tensors are evaluated from the metric and compared with an ADM
expression. Einstein and Hamiltonian contractions agree. Radial and axial
matrices, zero Eulerian acceleration, nonzero-v scaling, the energy angular
integral and compact-kernel moments are checked.

The supplied mpmath 1.3.0 record uses 120 decimal digits and a separate
piecewise quadrature implementation. All 18 unsmoothed mass and energy values
lie in the exact rational enclosures. These are separate implementations
executed by the authoring agent, not a new agent's independent review.

The default portable command newly regenerates the exact fractions, table,
finite-example document, constant arithmetic and bibliography. It checks 15
rational inequalities after the analytic envelope reduction. Negative
controls require rejection of changed numerical cells, missing rows and a
changed rational endpoint independently of the hash manifest. These tests
check finite reproducibility, not the infinite-parameter theorem. The saved
symbolic and quadrature results are not silently presented as freshly run by
the default command. Optional rerun commands are in REPRODUCE.md.

## Lean correspondence and limits

MainStatement.lean is unchanged from the previously successful Lean 4.35.0
and matching mathlib check. Its SHA-256 is
`706875e54c20ef6e90ea62934c09ff5993d48c09b10f05ed6c5e60a3f43e29ae`.
The exported historical result removes only the machine-local runtime path
and adds an explicit status/strength description. No fresh type-check is
claimed for v1.2. The file contains propositions with no proof terms, no
axioms asserting their truth, and no sorry.

| Paper content | Lean representation |
|---|---|
| Global profile and endpoint conditions | Admissible |
| Radial electric matrix and Euclidean norm | electricA/B/D and TidalBound quadratic form |
| Energy and its infimum | J, EnergySet, Jstar |
| Feasibility and finite lower bound | FeasibilityClaim, FiniteLowerClaim |
| Uniform error estimates | UniformErrorBoundsClaim with existential constants; weaker than the explicit choices in Theorem 1 |
| Uniform limit | UniformLimitClaim in epsilon form |

The metric-to-matrix bridge is analytic and symbolic, not formalized in Lean.
Type-checking a proposition does not prove it. There has been no human expert
peer review and no full formal proof.

## Sources and distribution

SOURCES.md records the limited primary-source checks, version-qualified
locators, 15 matching bibliographic records, and the separate volume/article
metadata checks. The package contains original code/text/generated data and
bibliographic records, not external papers or runtime libraries.

The local publication candidate uses a cached Tectonic build. Every final
PDF page is rendered and visually inspected before handoff. Distribution
integrity, PDF text, finite reproduction and negative controls are checked
in a clean local Git clone with the same default command as CI. Remote CI
execution, publication, external repository creation, release and DOI
assignment remain separate operations and are not claimed here.

The claims do not extend to other curvature components, other observers,
matter realizability, quantum inequalities, stability, energy-condition
satisfaction, finite-η optimizer existence, optimal error rates, or exhaustive
novelty. Attribution to cited authors does not imply their endorsement.
