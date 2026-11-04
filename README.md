# Sharp first-order energy correction under an Eulerian tidal bound for finite-wall Alcubierre profiles

[日本語](README.ja.md)

For a fixed finite radial wall in the specified Alcubierre metric, within the class of monotone C² radial profiles smoothly matched to the constant interior and exterior at both boundaries, the paper determines how the least negative Eulerian energy magnitude approaches its harmonic floor as the permitted tidal norm increases. The first correction has the explicit coefficient

\[
\eta\left[J_R^*(\eta)-\frac{R}{R-1}\right]
\longrightarrow \frac{1}{3R(R-1)^3}
\quad\text{uniformly for }R\in[3/2,3].
\]

Read the [nine-page paper](paper.pdf), [LaTeX source](paper.tex), and [precise claims](claims.json). Version **1.2** is a local publication candidate prepared on 27 October 2026. No public release or DOI has been assigned. The proposed repository name is **`alcubierre-tidal-energy-asymptotics`**.

## What is bounded

The inner radius is 1, the outer radius is R, and the wall width stays between 1/2 and 2. Profiles are globally C², monotone, and match the constant interior and exterior exactly. The stationary metric has one shift component and fixed speed v=1/10. The constraint bounds the Euclidean operator norm of **E/v² at every radius and angle**, where E is the electric part of the full Riemann tensor for the Eulerian normal.

The dimensionless index is J=∫₁ᴿ r²f′(r)² dr; the negative Eulerian slice integral equals −J/1200 at the stated speed. The theorem gives nonemptiness for η≥128, an explicit finite lower bound, and uniform estimates with **η₀=128, B₋=5, B₊=61000**. The upper estimate comes from a constructed admissible family; existence of an optimizer is not assumed. These error constants are deliberately loose, and their rates are not claimed optimal.

## Reproduce the finite checks

Use Python 3.11 or newer and Poppler (`pdftotext`, `pdfinfo`). No Python packages or network access are needed for the default checks. Run the same command used by CI and the clean-clone preflight:

```sh
python3 -B check_all.py
```

Success is exit code 0 and `status: PASS`. It checks the distribution manifest, input/export provenance, PDF version and text, claim metadata, and saved citation records. It regenerates **18 exact rational enclosures**, the numerical table, the bibliography, and **15 exact arithmetic checks** of the constant bounds in temporary directories. Negative controls require rejection of a changed table cell, a missing row, a changed rational bound, and optimized Python. The numerical checker compares against regeneration without consulting the file-hash manifest.

[REPRODUCE.md](REPRODUCE.md) separates these executed finite checks from the optional symbolic, 120-digit quadrature, PDF-build, and Lean procedures. [FORMAT.md](FORMAT.md) describes the stored intervals. [MANIFEST.sha256](MANIFEST.sha256) fixes the distribution. Default checks leave tracked files unchanged.

## Assurance and scope

The uniform theorem has an analytic proof. Finite computations corroborate formulas and examples; they do not establish the infinite-parameter theorem. Saved symbolic calculations derive the tidal tensor from Christoffel symbols and compare it with an ADM expression. A separate quadrature implementation checks the 18 mass and energy integrals.

**Lean level L1:** the supplied file defines a weaker consequence of Theorem 1 with existential error constants. It was type-checked previously; it is not a proof, does not contain the explicit constants 5 and 61000, and does not formalize the metric-to-matrix derivation. The unchanged file's prior result is retained, not presented as a new run. The work has received AI review but **no human expert peer review**. [VERIFICATION-RECORD.md](VERIFICATION-RECORD.md) states the checks and their limits.

The result concerns this metric, radial profile class, observer, and electric Riemann norm. It does not establish bounds on other curvature components or other observers' measurements, matter realizability, quantum inequalities, stability, or satisfaction of energy conditions. No exhaustive novelty or priority claim is made.

## Attribution and license

Tatsuhiko Takimoto is responsible for the work. Claude and Codex assisted with mathematical exploration, derivation, computation, literature organization, and drafting; they are tools, not authors.

Alcubierre supplied the metric; Lobo and Visser developed the Eulerian volume-integral viewpoint; Bobrick and Martire studied radial shape variation. Natário's construction and the energy-minimum analysis reported by Bolívar, Vasilev and Abellán provide the divergence-free comparison, while Santiago, Schuster and Visser clarify curvature and observer distinctions. The cited computational and variational work provides further context. I am grateful to these authors for the models and analyses on which this work builds. This does not imply their review or endorsement. Primary references and version-specific access limits are in [SOURCES.md](SOURCES.md) and the paper.

Project-owned code and CI configuration are **Apache-2.0**. The article, original documentation and generated numerical data are **CC BY 4.0**. Third-party libraries and external papers are not bundled. See [LICENSE](LICENSE) and [CITATION.cff](CITATION.cff).
