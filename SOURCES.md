# Sources, attribution and access

The paper's 12 works are listed in `references.json`, which generates both
`bibliography.tex` and `REFERENCES.md`. The latter has 15 title/author/year
claims because three works include both a DOI and a versioned arXiv record.
`cite-check.json` is the saved metadata check performed on 26 October 2026
UTC (27 October JST): all 15 matched. The arXiv years in that checker input
are first-submission years, separately from journal years and version dates.
This version retains the same bibliography and check input hash. Metadata
agreement does not establish a scientific claim or novelty.

## Inspected primary passages

- [Bobrick and Martire, arXiv:2102.06824v2](https://arxiv.org/html/2102.06824v2), Appendix A.3, equations (28)–(29) and their harmonic solution: the radial energy variation used for context in the Introduction.
- [Santiago, Schuster and Visser, arXiv:2105.03079v2](https://arxiv.org/html/2105.03079v2), §3.1, equations (3.5)–(3.10): flat-slice electric Riemann identities and the extrinsic-curvature Lie derivative. The present specialization is also derived directly from the metric.

These locators were checked in the stated arXiv versions. Publisher full text
was not available through the reading route used, so published-version
numbering is not represented as verified. The paper explicitly says “arXiv
v2” in both citations and also provides the published DOI. The two 2026
preprints are attributed as reported results, not as results independently
reproved by this work. The literature positioning is limited to the cited
comparison and is not an exhaustive novelty search.

## Publication metadata

`publication-metadata.json` records five publisher-deposited Crossref records,
including URLs, dates, volume, issue, page/article identifiers and response
hashes. It confirms Bobrick–Martire 38/105009 (2021), Fell–Heisenberg
38/155020 (2021), Warp Factory 41/095009 (2024), Lentz 38/075015 (2021), and
Lobo–Visser 21/5871–5892 (2004), including the quotation marks in the latter
title. The Lentz arXiv record was first submitted in 2020. Santiago et al.
was first submitted in 2021, with v2 dated 25 February 2022. Volume and
article numbers were checked separately; the title/author/year checker does
not test them.

Only bibliographic metadata and links are included; external paper text is
not redistributed. The paper and README give the scientific attributions.
The distribution layout and CI conventions follow an existing laboratory
publication packet; the present checkers are adapted to this analytic result
and its exact finite examples.
