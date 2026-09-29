# Updated manuscript alignment

The alignment target is **Service Certification for Agentic Wireless Networks** in the supplied `SC_for_Agentic_Wireless_Networks_GitHub_checked(1).zip`. The archive SHA-256 is `aab060ab3984a741450902e0e5e8407464718cb36dbb1b8c2efe06915e208c46`. The consistency review dated 29 September 2026 compared this source with repository commit `778be9d179e9b2a6816e8c3696c81468666d16b8`. This document records the source alignment; build instructions and dated validation records are described in [`reproduction.md`](reproduction.md).

The paper title has no subtitle. The companion protocol is presented as **Extended Experiments**, without an author byline, in [`extended_experiments.md`](../extended_experiments.md).

## Source mapping

Paths in the first column are relative to the uploaded manuscript archive, not to this repository. The repository distributes companion material; it does not contain the complete updated `main.tex` and `supplement.tex`.

| Updated manuscript source | Corresponding repository material | Scope |
| --- | --- | --- |
| `main.tex` | [`README.md`](../README.md), [`CITATION.cff`](../CITATION.cff), [`extended_experiments.md`](../extended_experiments.md), and active figure sources | Associated paper title, scientific terminology, and presentation alignment. |
| `main.tex`: five active TikZ imports | [`figures/tikz/`](../figures/tikz/) fragments `goal_evidence_loop`, `joint_exclusion_geometry`, `wireless_confidence_trace`, `certification_costs`, and `execution_stopping_costs` | Updated layouts, annotations, mean-delay terminology, and “Unguarded” maximin qualifiers; numerical data retained. |
| `figures/figure_overview.py` and `figures/plot_figures.py` | The same relative repository paths | Consistent measurement, model-validity, and mean-delay terminology across retained rendering paths. |
| `code/extended_experiments.tex` | [`extended_experiments.md`](../extended_experiments.md) | Experimental populations, comparator definitions, retained outcomes, and limitations; cross-references and missing-source disclosures are preserved in Markdown. |
| `main.tex`: scalar completion theorem; `supplement.tex`: scalar proof and numerical benchmark | [`scripts/scalar_frontier.py`](../scripts/scalar_frontier.py), [`docs/scalar_frontier.md`](scalar_frontier.md), and `figures/tikz/data/frontier_*.csv` | Executable scalar precision maximization, exact completion curves, deadline table, and separately identified endpoint Monte Carlo. |
| `main.tex`: multivariate frontier and Bellman recursion; `supplement.tex`: its proof | The coverage statements in this document and [`implementation.md`](implementation.md) | Theoretical characterization only; no multivariate numerical solver or policy recovery is supplied. |
| `supplement.tex`: adaptive-separation proposition and numerical example | “Numerical Adaptive-Instrument Reference” in [`extended_experiments.md`](../extended_experiments.md) and the paired coarse acquisition convention in [`implementation.md`](implementation.md) | Analytical example with unchanged formulas, resource bounds, and numerical values. |
| `figures/*.json` and `figures/tikz/data/*.csv` | The same relative repository paths | Frozen supplied summaries and exact-reference plotting values; alignment does not modify observations or recompute historical intervals. |

The historical source mapping and original checksums remain in [`provenance.md`](provenance.md) and [`source_manifest.json`](source_manifest.json). The fragments under [`docs/source/`](source/) are historical records and are intentionally unchanged. Differences between those fragments and current active sources do not imply an incomplete synchronization.

[`manuscript_alignment.json`](manuscript_alignment.json) records the source hashes and scope of the manuscript synchronization. The overview retains the updated terminology with small typography adjustments so longer labels fit. Active TikZ drawing fragments match the updated manuscript. The superseded architecture assets, duplicate top-level native PDFs, and duplicate goal/evidence wrapper have been removed; native sources and canonical previews remain under [`figures/tikz/`](../figures/tikz/).

## Numerical implementation coverage

The scalar benchmark maximizes total precision over legal integer acquisition designs and evaluates the exact Gaussian endpoint test. Its dynamic program is not the updated paper's multivariate likelihood-state Bellman recursion.

The multivariate result characterizes a completion frontier using finite witness sets, a continuous likelihood-ratio state, nonnegative risk/cost multipliers, and an infimum over witness sets. The repository has no implementation of the associated numerical integration, state approximation, multiplier optimization, witness refinement, or feasible optimal-policy recovery. Implementing those components would require a separately documented numerical method and accuracy assessment. The theoretical result must not be described as a reproduced multivariate experiment.

The adaptive-separation example is also analytical. A coarse acquisition is a pair of independent scalar stage observations, charged as one bundle with its stated total cost and duration. Thus 224 coarse acquisitions count as 224 bundles; the reported duration 1452 and cost 2680 remain unchanged. This vector-valued acquisition convention does not modify the scalar benchmark.

## Records required for experimental replay

Summary means, figure coordinates, source hashes, and published completion counts cannot recover the missing original observations or execution order. The following material must be restored from the original research records before a full replay can be claimed.

| Study or component | Required original records |
| --- | --- |
| Verifier, controller, and diagnostic generators | Versioned controller and verifier source; wireless/FCFS generators; optimizer and LP-auditor implementations; full configurations, dependencies, seeds, and run commands. |
| Earlier stage/wireless comparisons and the 32-/64-sequence confirmations | Original runners and comparator adapters; complete paired report tapes or exact generators with seed schedules; per-sequence/per-goal outcomes, stopping counts, resource ledgers, and pairing identifiers; bootstrap inputs, resampling settings, and records. Keep each comparison's own population. |
| G-ACOL comparison | Exact upstream and adapted source, including the cited upstream commit and `wireless_validation/vendor/v13/` material; unchanged-code replay runner and adapter settings. |
| 120-trial stopping comparison | All 120 paired attempts, preparation/pilot/completion reports, planned quotas, observed stopping points, certification outcomes, acquisition costs, and durations for every executor. |
| Historical auditing and guarded promises | Complete trial grids and paired tapes; original audit/controller source; mask/checkpoint decisions, promise issuance and reservation ledgers, realized acquisition, and all-attempt outcomes. The 500 selected-promise plotting points alone are insufficient. |
| Practical policy and physical-diagnostic studies | Original policy/FCFS runners, model/prior settings, report streams, paired seed-cluster outcomes at every deadline, and bootstrap records; raw EdgeDroid or localhost latency data, measurement harnesses, splits, and timestamp logs where claimed. |
| Validity study | `methods/validity_study/trial_results.csv` and its producing runner, seeds, and schema. `validity_counts.csv` is a published-count transcription, not a substitute for trial records. |
| Language-model demonstration | Exact model/version and settings, prompts and transcripts, tool and guard harnesses, action/report logs, all attempts, the 16 guard checks, and certificate/resource replay files cited under `research_v41/study/`. |

The cited `research_v*` and `archive_v*` research directories are absent. A restored record set should include a manifest mapping each file to its study, source version, configuration, and checksum. Newly reconstructed implementations or newly generated trials must be identified separately from historical originals; they cannot establish an exact historical replay merely by matching an aggregate value.

## Reader access

The repository is private. Readers need explicit GitHub permission to open its files; a repository URL in the manuscript does not provide that permission. Before describing the companion material as generally available, the owner must provide an accessible archival deposit or authorize a public repository release. This alignment does not change repository visibility.
