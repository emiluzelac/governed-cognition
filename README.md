# Governed Cognition — Paper Artifact

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18691808.svg)](https://doi.org/10.5281/zenodo.18691808)

Artifact repository for:

> **From Fragile Glue to Governed Cognition: A Controlled Study of Blackboard Kernels for Modular AI Systems**
>
> Emil Uzelac, 2026

## Contents

- `paper/` — LaTeX source and compiled PDF
- `results/results.jsonl` — Raw benchmark data (1,200 episodes)
- `verification/verify_results.py` — Script to verify Table 3

## Verify Results

The verification script reads the raw episode data, computes aggregate metrics per agent, and checks them against the values reported in Table 3 of the paper.

```bash
python verification/verify_results.py
```

Expected output:

```
Agent             N        task_success        unsafe_action    unsupported_belief          traceability  failure_transparency
------------------------------------------------------------------------------------------------------------------
string_glue     300                 0.613                0.387                0.387                 0.100                 0.100
json_glue       300                 0.570                0.430                0.430                 0.300                 0.300
alethic         300                 1.000                0.000                0.000                 1.000                 1.000
llm_bk          300                 0.990                0.000                0.000                 1.000                 1.000

Total episodes: 1200
PASS: All metrics match Table 3 of the paper.
```

## Build Paper

Requires a LaTeX distribution (e.g., TeX Live).

```bash
cd paper
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## License

MIT License. See [LICENSE](LICENSE).
