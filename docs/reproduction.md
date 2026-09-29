# Reproduction guide

## What can be rerun

The supplied Python code regenerates the architecture, overview, four legacy summary plots, and—if its absent trial input is recovered—the historical validity plot. Native TikZ sources independently regenerate ten editable figures from supplied CSV values and drawing instructions. The additional exact scalar benchmark is documented in [`scalar_frontier.md`](scalar_frontier.md); it is a new implementation of the declared reference, not a recovered controller simulator.

The full historical simulation studies cannot be rerun from this package because their original drivers and trial records were not supplied. [`provenance.md`](provenance.md) identifies the missing material.

## Dependencies

- Python 3.10 or later, NumPy, Matplotlib, Pillow, and pypdf. Install `requirements.txt` in your chosen environment. Pillow and pypdf validate generated outputs.
- A TeX distribution providing `pdflatex`, TikZ/PGFPlots 1.18, `standalone`, `newtxmath`, `fontenc`, Times (`ptm`), `amsmath`, `amssymb`, `amsthm`, `booktabs`, `geometry`, `flafter`, and `hyperref`; the protocol uses Times, Courier, and Helvetica text fonts.
- Poppler's `pdftoppm` for the PNG previews produced by the legacy PGF plotting script.

Validation used Python 3.12.14, NumPy 2.3.5, Matplotlib 3.10.8, and pdfTeX from TeX Live 2023/Debian. TeX setup is platform-specific; the companion source does not depend on this session's private runtime paths.

## Portable build entry point

Run these commands from the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/reproduce.py --python
python scripts/reproduce.py --pgf --tikz --protocol
```

With no flags, `reproduce.py` performs the two Matplotlib-only tasks. You may combine flags. `--output PATH` selects a distinct output directory; by default all generated files and logs are under `build/reproduction/`. The helper copies supplied assets into that directory before execution, preserving the packaged figures. It replaces the historical hard-coded `/usr/bin/pdftoppm` path only in its temporary copy of `plot_figures.py`, using the executable found on `PATH`.

| Task | Generated files |
| --- | --- |
| `--python` | `figures/agent_architecture.pdf`, `.png`; `figures/joint_service_overview.pdf`, `.png`. |
| `--pgf` | PDF and PNG versions of `joint_exclusion_geometry`, `wireless_confidence_trace`, `certification_costs`, and `execution_stopping_costs`. |
| `--tikz` | One PDF beside each of the ten copied standalone `.tex` wrappers. |
| `--protocol` | `extended_experiments.pdf`; two LaTeX passes resolve its references. |

`build_results.json` records each task's exit code, log, output-validation results, and combined success. Before each task, the helper removes only that task's expected PDF/PNG products, including copied previews or outputs from a previous run. It preserves LaTeX auxiliary files between the sequential protocol passes. A zero process exit is insufficient: every expected PDF must have a complete header/trailer, parse strictly, and contain readable page streams; every PNG must have a complete final chunk, pass its integrity check, and decode successfully. Missing or invalid products make the overall command fail. No task imputes observations or executes the blocked validity script.

Run the focused build-validation regression tests with:

```bash
python -m unittest discover -s tests -v
```

To compile the extended protocol without the helper:

```bash
pdflatex -interaction=nonstopmode -halt-on-error extended_experiments.tex
pdflatex -interaction=nonstopmode -halt-on-error extended_experiments.tex
```

## Supplied validity script

`figures/plot_validity_study.py` is retained unchanged. It expects `methods/validity_study/trial_results.csv`, with method, budget, immediate/issued/correct/unresolved/wrong fields, and checks 720 trials per budget for the audited-sufficient method. That file was not supplied. The script's `FileNotFoundError` was verified; do not create synthetic replacement rows or infer trial histories from totals.

The native `validity_completion_outcomes.tikz` figure instead renders the supplied `validity_counts.csv`. Its provenance explicitly identifies the values as a published-count transcription.

## Original validation record

Validation was performed on 14 September 2026:

| Check | Result |
| --- | --- |
| Original `agent_architecture.py` and `figure_overview.py` | Both passed in an isolated copy. |
| Original `plot_figures.py` | Passed after the documented build-copy adaptation of the Poppler path; regenerated all four PDF/PNG pairs. |
| Original `plot_validity_study.py` | Confirmed blocked by its absent `trial_results.csv`; source retained unchanged. |
| Ten native TikZ wrappers | All compiled successfully. |
| Extended protocol | 11 pages; compiled in two passes, visually inspected, and checked for unresolved references and overfull boxes. |
| Original exported CSV provenance | All 16 SHA-256 checksums matched. |
| New scalar reference | All 4104 supplied curve values and all 18 first-deadline entries matched; maximum absolute curve error was 3.33e-16. |

These are presentation/build checks and analytical benchmark checks. They do not recover the missing original controller trials.

## Manuscript synchronization validation, 29 September 2026

The active figure sources and associated paper title were synchronized with the updated manuscript identified in [manuscript_alignment.md](manuscript_alignment.md). The frozen numerical data and original fragments under `docs/source/` remain unchanged. The earlier `validation.json` is retained as a historical record; fresh results are in [validation_2026-09-29.json](validation_2026-09-29.json).

| Check | Current result |
| --- | --- |
| Build-validation regression tests | All 9 tests pass, including missing, stale, truncated, and unreadable outputs despite zero producer exit status. |
| `reproduce.py --python` | Both tasks pass; both PDFs and both PNGs validate and were visually inspected. |
| `reproduce.py --pgf --tikz --protocol` | All 13 tasks pass; four legacy PDF/PNG pairs, all ten native TikZ figures, and both protocol passes validate. |
| Extended protocol | 11 pages; no undefined references/citations, duplicate labels, or overfull boxes; all pages visually inspected. |
| Figure layout | Updated long Python labels fit their boxes; active native drawings and legacy alternatives were visually inspected. The standalone system-model drawing retains only minor font-size substitutions of at most 0.5 pt. |
| Scalar reference | All 4,104 curve values and all 18 deadline entries match; maximum absolute error 3.33e-16. |
| Frozen data | All 16 exported CSV provenance checks pass; numerical JSON/CSV data and archived source fragments are unchanged. |
| Separate uploaded manuscript | Read-only compilation succeeds: 13-page main and 8-page supplement, with no unresolved references/citations, missing characters, font warnings, or overfull boxes. These manuscript files are not distributed by this companion repository. |
| Compatibility figure entry point | `figures/goal_evidence_loop.tex` compiles and inputs the current canonical drawing. |

The complete build used genuine TeX Live packages and fonts, including IEEEtran, newtx, and its kastrup/binhex dependency. No replacement class or substitute font was used. Python-library versions and per-task output validation are recorded in the current JSON record.

[generated_assets.json](generated_assets.json) maps all refreshed previews to their generating task and SHA-256 checksum. Native previews are in `figures/tikz/rendered/`; the top-level `goal_evidence_loop`, `v37_*`, `v42_*`, `v44_*`, and `validity_completion_outcomes` PDFs are copies of their native counterparts. The legacy filename `figures/joint_geometry.pdf` is an alias of the native `joint_exclusion_geometry` PDF. Other top-level figures are generated by the Python/PGF scripts. The architecture PNG is now included alongside its PDF.

An earlier review observed a transient truncated overview PDF after a zero process exit. The current runner detects this class of failure and also prevents a valid preview copied from the repository from masking a producer that writes nothing. The successful builds above validate the files produced during each task, not only its exit status.
