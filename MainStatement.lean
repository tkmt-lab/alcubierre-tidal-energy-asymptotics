import Mathlib

/-!
# L1 statement only: finite-wall Eulerian tidal asymptotic

This file defines propositions, not proofs. No theorem below is asserted.
The metric-to-matrix calculation is the analytic calculation in Section 3
of paper.tex; it is not formalized here. The reduced symmetric 2x2 block
has one additional zero eigenvalue in three dimensions. Its Euclidean
operator-norm constraint is written as a quadratic-form bound for all
real x,z. Thus no default matrix norm from a library is being substituted.

Profiles on [0,infinity) are extended constantly by 1 to negative radii.
This is equivalent for the stated class, since they are constant up to 1.
The ordinary interval integral and real infimum use mathlib definitions.
Existence and boundedness belong to the stated claims, not assumptions
or axioms introduced to force the asymptotic conclusion.
-/

noncomputable section
open Set MeasureTheory
open scoped Interval

namespace FiniteWallTidal

def h (f : ℝ → ℝ) (r : ℝ) : ℝ := 1 - f r
def p (f : ℝ → ℝ) (r : ℝ) : ℝ := -deriv f r
def dp (f : ℝ → ℝ) (r : ℝ) : ℝ := -deriv (deriv f) r

def electricA (f : ℝ → ℝ) (r u : ℝ) : ℝ :=
  -(3 / 4 : ℝ) * p f r ^ 2 * (1 - u ^ 2)

def electricB (f : ℝ → ℝ) (r u : ℝ) : ℝ :=
  -(h f r / 2) * (dp f r - p f r / r) * Real.sqrt (1 - u ^ 2) * u
    - p f r ^ 2 * Real.sqrt (1 - u ^ 2) * u

def electricD (f : ℝ → ℝ) (r u : ℝ) : ℝ :=
  -h f r * dp f r * u ^ 2
    - h f r * p f r / r * (1 - u ^ 2)
    + (1 - 5 * u ^ 2) / 4 * p f r ^ 2

/-- E/v^2 in the rotated radial plane, with v fixed at 1/10 in the paper. -/
def TidalBound (f : ℝ → ℝ) (r u η : ℝ) : Prop :=
  ∀ x z : ℝ,
    |electricA f r u * x ^ 2 + 2 * electricB f r u * x * z
      + electricD f r u * z ^ 2| ≤ η * (x ^ 2 + z ^ 2)

def Admissible (R η : ℝ) (f : ℝ → ℝ) : Prop :=
  ContDiff ℝ 2 f ∧
  (∀ r : ℝ, r ≤ 1 → f r = 1) ∧
  (∀ r : ℝ, R ≤ r → f r = 0) ∧
  (∀ r : ℝ, deriv f r ≤ 0) ∧
  deriv f 1 = 0 ∧ deriv (deriv f) 1 = 0 ∧
  deriv f R = 0 ∧ deriv (deriv f) R = 0 ∧
  (∀ r ∈ Icc (1 : ℝ) R, ∀ u ∈ Icc (-1 : ℝ) 1, TidalBound f r u η)

def J (R : ℝ) (f : ℝ → ℝ) : ℝ :=
  ∫ r in (1 : ℝ)..R, r ^ 2 * (deriv f r) ^ 2

def EnergySet (R η : ℝ) : Set ℝ :=
  {value | ∃ f : ℝ → ℝ, Admissible R η f ∧ value = J R f}

def Jstar (R η : ℝ) : ℝ := sInf (EnergySet R η)
def C (R : ℝ) : ℝ := R / (R - 1)
def a (R : ℝ) : ℝ := 1 / (R * (R - 1))
def K (R : ℝ) : ℝ := 1 / (3 * R * (R - 1) ^ 3)
def L (R η : ℝ) : ℝ :=
  (R - a R / η) ^ 2 * a R ^ 3 / 3 * (1 - 2 * Real.sqrt (a R / η))

def FeasibilityClaim : Prop :=
  ∀ R ∈ Icc (3 / 2 : ℝ) 3, ∀ η : ℝ, 128 ≤ η →
    (EnergySet R η).Nonempty ∧ BddBelow (EnergySet R η)

def FiniteLowerClaim : Prop :=
  ∀ R ∈ Icc (3 / 2 : ℝ) 3, ∀ η : ℝ, 128 ≤ η →
    L R η ≤ η * (Jstar R η - C R)

def UniformErrorBoundsClaim : Prop :=
  ∃ Bminus Bplus η₀ : ℝ, 0 < Bminus ∧ 0 < Bplus ∧ 128 ≤ η₀ ∧
    ∀ η : ℝ, η₀ ≤ η → ∀ R ∈ Icc (3 / 2 : ℝ) 3,
      K R - Bminus / Real.sqrt η ≤ η * (Jstar R η - C R) ∧
      η * (Jstar R η - C R) ≤ K R + Bplus / η

/-- Epsilon form of the uniform sup limit in Theorem 1, Equation (2.7).
The equation number is descriptive; the formula, not numbering, is the contract. -/
def UniformLimitClaim : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ η₀ : ℝ, 128 ≤ η₀ ∧
    ∀ η : ℝ, η₀ ≤ η → ∀ R ∈ Icc (3 / 2 : ℝ) 3,
      |η * (Jstar R η - C R) - K R| < ε

/-- The proposition to be formalized in future work; no proof is supplied. -/
def MainClaim : Prop :=
  FeasibilityClaim ∧ FiniteLowerClaim ∧ UniformErrorBoundsClaim ∧ UniformLimitClaim

#check MainClaim
#check UniformLimitClaim

end FiniteWallTidal
