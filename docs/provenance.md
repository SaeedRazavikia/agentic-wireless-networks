# Source mapping and provenance

The supplied source was `Agentic_Wireless_Networks__JSAC_ (1).zip`. This package reorganizes those manuscript assets and supplies documentation/build utilities. The original simulation research directories were absent from the attachment.

## File mapping

| Original path | Repository path | Treatment |
| --- | --- | --- |
| `compact/experiments.tex` | `docs/source/experiments_original.tex` | Preserved byte for byte before manuscript edits. |
| `compact/experiments.tex` | `docs/experimental_protocol.tex` | Full experimental content retained; unavailable record references are clarified, the acquisition cross-reference names the theoretical supplement, and long inline lists are reformatted for standalone readability. |
| `compact/acquisition.tex` | `docs/source/acquisition_original.tex` | Original derivation retained for implementation traceability; the paper's theoretical supplement remains the authoritative proof context. |
| `compact/adaptive.tex` | `docs/source/adaptive_original.tex` | Complete original adaptive-selection source retained; its simulation-based continuation theorem and proof are included in the extended protocol. |
| `v37_results_section.tex` | `docs/source/v37_results_section.tex` | Unmodified older results fragment; not substituted for the current protocol. |
| `v41_results_section.tex` | `docs/source/v41_results_section.tex` | Unmodified older results fragment; not substituted for the current protocol. |
| `v42_results_section.tex` | `docs/source/v42_results_section.tex` | Unmodified older results fragment; not substituted for the current protocol. |
| `figures/` | `figures/` | All supplied scripts, data, images, PDFs, native TikZ, and wrappers retained. |
| `figures/tikz/README.md` | `docs/source/editable_figures_original_README.md` | Original README preserved; the active figure README now points to the supplied portable build helper. |

The standalone protocol adds the wireless-instance definitions and scalar reference from the supplied paper/supplement so its numerical descriptions do not depend on unresolved cross-references. It does not add experimental observations. The original LaTeX fragments in `docs/source/` still contain their historical external references and are provenance records, not standalone documents.

[`source_manifest.json`](source_manifest.json) records source/package paths and SHA-256 checksums for 82 supplied assets, including the preserved source fragments. The one intentional change to an existing asset is the active TikZ README. New documentation, helpers, and the independently reconstructed scalar benchmark are identified by their own documentation.

## Figure data

| Dataset | Content and interpretation |
| --- | --- |
| `figures/figure_data.json` | Frozen comparison means, execution summaries, and a recorded wireless confidence trace; includes upstream hashes and notes. |
| `figures/overview_data.json` | Wireless trace used by the overview script. |
| `figures/v37_figure_data.json` | Separate comparison summaries and the 500 selected-promise plotting points. |
| `figures/tikz/data/certification_costs.csv` | Legacy comparison plotting summaries. |
| `figures/tikz/data/execution_costs.csv` | Fixed-reserve stopping summaries. |
| `figures/tikz/data/wireless_trace.csv` | Exported confidence-trace values. |
| `figures/tikz/data/v37_cost_comparisons.csv` | Frozen comparison means and intervals; retain each row's own population. |
| `figures/tikz/data/v37_promise_points*.csv` | Selected issued-promise reservations and realized costs, including budget-specific subsets. |
| `figures/tikz/data/frontier_*.csv` | Eight exact-reference curves with 513 deadline points each: 4104 points in total. |
| `figures/tikz/data/validity_counts.csv` | Exact published-count transcription for the validity-outcome plot, not reconstructed trial-level records. |

The original [`figures/tikz/data/PROVENANCE.json`](../figures/tikz/data/PROVENANCE.json) labels its data exports as presentation-only. All 16 listed exported SHA-256 checksums were verified against the supplied CSV files. Hashes naming unavailable upstream files identify a source dependency; they do not establish that those files are included or independently replayed here.

## Missing upstream material

The attachment contains no `research_v*`, `archive_v*`, `methods/validity_study`, or `wireless_validation/vendor/v13` directory. In particular, it omits:

- Original wireless/FCFS diagnostic generators, controller and verifier implementations, optimization/audit runners, and complete paired random-report tapes.
- Trial-level execution records and bootstrap resamples underlying the historical summaries.
- `methods/validity_study/trial_results.csv`, required by `plot_validity_study.py`.
- Original G-ACOL adapter/vendor source and the unchanged-code replay runner.
- Agent transcripts, exact model version, and tool/guard-replay harnesses.
- Raw EdgeDroid or localhost latency data, measurement harnesses, split definitions, and timestamp logs.

The extended protocol retains adverse results, differing denominators, prior-sensitivity corrections, and limits of physical interpretation. Selected-promise points and aggregate completion counts must not be treated as full trial logs or used to invent missing confidence intervals.
