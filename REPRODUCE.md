# Reproduction and checking

## Default offline command

Requirements: Python 3.11 or newer; Poppler with `pdftotext` and `pdfinfo`.
No pip packages, solver, network, symbolic engine or Lean runtime are needed.
From this repository root:

```sh
python3 -B check_all.py
```

This is the command in `.github/workflows/verify.yml` and the local clean-clone
preflight. It runs distribution checks, regenerates exact results, exercises
negative controls, then checks the distribution again. Exit code 0 and
`status: PASS` mean those checks passed. Optimized Python (`-O`) is refused
because the numerical scripts also use assertions. Temporary files live in
ignored `.check-tmp/` subdirectories and are cleaned up after each check;
tracked files are unchanged. The checks themselves run offline.

The default command recomputes the 18 finite rational enclosures, outward
rounded table and finite-example document, 15 rational constant-envelope
checks, and bibliography. `verify.py` compares supplied data to regenerated
results without using the distribution manifest. Negative controls change a
numerical table cell, remove a table row, and corrupt a rational upper bound;
each must be rejected. A separate control confirms optimized Python is refused.

The workflow provisions Python and Poppler on its runner before the offline
checks. Its actions are pinned to the same commits as the reference publication
workflow, it uses read-only repository permissions, no secrets, one-thread
environment settings and a ten-minute job timeout. A locally passing preflight
does not imply that a remote GitHub Actions run has occurred.

## Regenerate tracked numerical and bibliography outputs

These commands deliberately overwrite the corresponding tracked generated
files; preserve any edits first.

```sh
python3 -B reproduce.py
python3 -B constant_check.py
python3 -B build_references.py
```

The scripts use only the standard library. The exact rational JSON and TeX
numerical rows are unchanged from v1.1. The finite-example prose was adjusted
to describe the construction without referring to the internal review phase.

## Optional symbolic and quadrature corroboration

Use the pinned packages in `requirements-optional.txt` in an environment you
manage. They are not installed or invoked by the default command or CI.
SymPy 1.14.0 and mpmath 1.3.0 were used for the saved results.

```sh
python3 -B symbolic_check.py
python3 -B quadrature_crosscheck.py
```

These commands overwrite their result JSON files. The symbolic script derives
Christoffel and Riemann tensors directly from the metric and compares the
contractions with ADM formulas. It checks the radial and axial matrices,
Eulerian geodesic acceleration, cancellation of nonzero speed in E/v², the
energy angular integral, and kernel moments. The quadrature script integrates
the unsmoothed pieces with 120-digit arithmetic and checks inclusion in the
exact intervals. It is a separate calculation, not a formal proof.

## PDF source build

The included PDF was built with Tectonic 0.17.0 and an already populated
TeX/font cache. To use the same cached dependencies:

```sh
mkdir -p build
tectonic --only-cached --keep-logs --outdir build paper.tex
```

The output is `build/paper.pdf`; the supplied PDF remains unchanged. A new
machine must obtain the required Tectonic bundle files before using
`--only-cached`. PDF bytes may differ because of creation metadata, even when
extracted text and rendered content agree. The default offline checks inspect
the supplied PDF and its manifest; they do not recompile TeX.

## Lean statement

`MainStatement.lean` is the unchanged L1 statement file. It defines a weaker
consequence of Theorem 1 with existential error constants, not its literal
transcription with B₋=5 and B₊=61000. The historical record in `lean-check.json`
checks this file's SHA-256 and reports successful type-checking with Lean
4.35.0 and matching mathlib. No proof of the propositions is supplied.

For an optional type-check, copy the file into an existing mathlib v4.35.0
project using Lean 4.35.0 and run there:

```sh
lake env lean -j1 MainStatement.lean
```

No Lean installation, dependency fetch, or new type-check is performed by the
default command. The finite checks, statement type-check and analytic theorem
have different assurance levels; none should be reported as the others.
