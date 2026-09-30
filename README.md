# Service Certification for Agentic Wireless Networks

Companion code, experimental protocols, and figure data for **Service Certification for Agentic Wireless Networks**.

This repository collects the simulation-related material supplied with the manuscript. The full experimental protocol, numerical comparisons, additional plots, and implementation notes are separated from the theoretical supplement so that the supplement can focus on its proofs.

The active documentation is aligned with the current 13-page main paper and 7-page theoretical supplement as of 30 September 2026. The companion protocol is [`extended_experiments.md`](extended_experiments.md). Earlier manuscript sources remain identified as historical records in [`docs/manuscript_alignment.md`](docs/manuscript_alignment.md), together with the source mapping, implementation coverage, and records required for full experimental replay.

## Contents

| Path | Contents |
| --- | --- |
| [`extended_experiments.md`](extended_experiments.md) | Full experimental protocol, comparisons, supporting figures and tables, and continuation-selector guarantee in Markdown. |
| [`docs/implementation.md`](docs/implementation.md) | Verifier, resource ledger, acquisition, and guarded-promise specifications. |
| [`docs/manuscript_alignment.md`](docs/manuscript_alignment.md) | Updated-manuscript mapping, scalar and multivariate implementation scope, and missing-record inventory. |
| [`docs/reproduction.md`](docs/reproduction.md) | Commands, dependencies, validation results, and the boundary of reproducibility. |
| [`docs/provenance.md`](docs/provenance.md) | File mapping and interpretation of the supplied data. |
| [`figures/`](figures/) | Active plotting scripts, frozen JSON summaries, and figure assets. |
| [`figures/tikz/`](figures/tikz/) | Native editable figures and CSV plotting data. |
| [`scripts/reproduce.py`](scripts/reproduce.py) | Portable entry point that regenerates available figures in a separate build directory. |
| [`scripts/scalar_frontier.py`](scripts/scalar_frontier.py) | New exact scalar Gaussian benchmark implementation, with an optional endpoint Monte Carlo experiment. |
| [`docs/source/`](docs/source/) | Unmodified experimental and acquisition source fragments retained for traceability. |

## Reproduce the available figures

Use Python 3.10 or later and install the dependencies:

```bash
python -m pip install -r requirements.txt
python scripts/reproduce.py --python
```

The default Python task reproduces the overview with Matplotlib. With a working TeX distribution and Poppler, reproduce the four legacy PGF plots, every native TikZ figure, and the PNG illustrations used in Extended Experiments:

```bash
python scripts/reproduce.py --pgf --tikz --previews
```

Outputs and logs are written under `build/`; supplied inputs are preserved. See [`docs/reproduction.md`](docs/reproduction.md) for TeX dependencies and individual commands.

## Exact scalar benchmark

A new implementation of the specified exact scalar Gaussian benchmark reproduces all eight supplied frontier curves and the reported deadline table. This does not recover the missing original simulator or trial tapes. See [`docs/scalar_frontier.md`](docs/scalar_frontier.md).

The updated paper also gives a multivariate finite-witness frontier through a joint likelihood-state Bellman recursion. That result is theoretical coverage: this repository supplies no multivariate Bellman solver or numerical policy-recovery implementation. The scalar dynamic program maximizes precision over integer acquisition designs and does not implement that recursion.

```bash
python scripts/scalar_frontier.py verify
python scripts/scalar_frontier.py table
python scripts/scalar_frontier.py monte-carlo --seed 20260914 --replications 10000
```

## Evidence scope

The supplied manuscript archive contains plotting code, summary data, native figure sources, and experimental descriptions. It does **not** contain the original simulation/controller drivers, complete paired trial records, random report tapes, LLM transcripts, or the `research_v*` and `archive_v*` directories cited in the protocol. Regenerating a plot reproduces its presentation from supplied data; it does not rerun the underlying experiment. The original `plot_validity_study.py` requires the absent `methods/validity_study/trial_results.csv`; the supplied TikZ plot instead uses the documented transcription in `validity_counts.csv`.

The supplied historical numerical results are preserved. The new scalar benchmark independently reconstructs the declared exact reference; its optional Monte Carlo command generates a separately identified experiment. Historical adverse outcomes and reproduction limitations are retained in the extended protocol.

Original controllers, report tapes, paired outcomes, and LLM execution records cannot be recovered from summary figures. The [restoration inventory](docs/manuscript_alignment.md#records-required-for-experimental-replay) identifies the material needed to rerun each affected study. No missing records or experimental results have been synthesized.

## Citation

[`CITATION.cff`](CITATION.cff) contains author/title metadata, and [`docs/repository_citation.bib`](docs/repository_citation.bib) provides the BibTeX entry for this [GitHub repository](https://github.com/SaeedRazavikia/agentic-wireless-networks). Development instructions are in [`docs/development.md`](docs/development.md).

No license has been added; reuse permissions have not been specified in this package.
