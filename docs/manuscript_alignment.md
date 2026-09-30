# Updated manuscript alignment

The current alignment target is **Service Certification for Agentic Wireless Networks**, comprising a 13-page main paper and a 7-page theoretical supplement as of 30 September 2026. Active documentation uses the current supplement's adaptive-example parameters and acquisition caps. The paper links directly to this repository, and its supplement identifies the root-level [`extended_experiments.md`](../extended_experiments.md) as the companion protocol. Build instructions and dated validation records are described in [`reproduction.md`](reproduction.md).

The earlier alignment dated 29 September 2026 used `SC_for_Agentic_Wireless_Networks_GitHub_checked(1).zip`, with SHA-256 `aab060ab3984a741450902e0e5e8407464718cb36dbb1b8c2efe06915e208c46`, and compared it with repository commit `778be9d179e9b2a6816e8c3696c81468666d16b8`. That archive and the preserved fragments under `docs/source/` document earlier source versions; they are not the current paper and supplement.

## Source mapping

The first column identifies paper sources and the historical protocol source. These source paths are not repository entry points. The repository distributes companion material; it does not contain the complete current `main.tex` and `supplement.tex`.

| Paper or historical source | Corresponding repository material | Scope |
| --- | --- | --- |
| `main.tex` | [`README.md`](../README.md), [`CITATION.cff`](../CITATION.cff), [`extended_experiments.md`](../extended_experiments.md), and active figure sources | Associated paper title, scientific terminology, and presentation alignment. |
| `main.tex`: five active TikZ imports | [`figures/tikz/`](../figures/tikz/) fragments `goal_evidence_loop`, `joint_exclusion_geometry`, `wireless_confidence_trace`, `certification_costs`, and `execution_stopping_costs` | Updated layouts, annotations, mean-delay terminology, and “Unguarded” maximin qualifiers; numerical data retained. |
| `figures/figure_overview.py` and `figures/plot_figures.py` | The same relative repository paths | Consistent measurement, model-validity, and mean-delay terminology across retained rendering paths. |
| Historical `code/extended_experiments.tex` | [`extended_experiments.md`](../extended_experiments.md) | Experimental populations, comparator definitions, retained outcomes, and limitations; cross-references and missing-source disclosures are preserved in Markdown. The current supplement points directly to this Markdown file. |
| `main.tex`: scalar completion theorem; `supplement.tex`: scalar proof and numerical benchmark | [`scripts/scalar_frontier.py`](../scripts/scalar_frontier.py), [`docs/scalar_frontier.md`](scalar_frontier.md), and `figures/tikz/data/frontier_*.csv` | Executable scalar precision maximization, exact completion curves, deadline table, and separately identified endpoint Monte Carlo. |
| `main.tex`: multivariate frontier and Bellman recursion; `supplement.tex`: its proof | The coverage statements in this document and [`implementation.md`](implementation.md) | Theoretical characterization only; no multivariate numerical solver or policy recovery is supplied. |
| `supplement.tex`: adaptive-separation proposition and numerical example | “Numerical Adaptive-Instrument Reference” in [`extended_experiments.md`](../extended_experiments.md) and the paired coarse acquisition convention in [`implementation.md`](implementation.md) | Current parameters and acquisition caps; analytical duration 1452 and acquisition cost 2680. |
| `figures/*.json` and `figures/tikz/data/*.csv` | The same relative repository paths | Frozen supplied summaries and exact-reference plotting values; alignment does not modify observations or recompute historical intervals. |

The historical source mapping and original checksums remain in [`provenance.md`](provenance.md) and [`source_manifest.json`](source_manifest.json). The fragments under [`docs/source/`](source/) are historical records and are intentionally unchanged. Differences between those fragments and current active sources do not imply an incomplete synchronization.

[`manuscript_alignment.json`](manuscript_alignment.json) records the source hashes and scope of the manuscript synchronization. The overview retains the updated terminology with small typography adjustments so longer labels fit. Active TikZ drawings follow the current manuscript, with presentation clarifications including explicit “Unguarded” labels for the maximin comparators. The Python overview and plots also clarify labels; numerical data are unchanged. The superseded architecture assets, duplicate top-level native PDFs, and duplicate goal/evidence wrapper have been removed; native sources and canonical previews remain under [`figures/tikz/`](../figures/tikz/).

## Numerical implementation coverage

The scalar benchmark maximizes total precision over legal integer acquisition designs and evaluates the exact Gaussian endpoint test. Its dynamic program is not the updated paper's multivariate likelihood-state Bellman recursion.

The multivariate result characterizes a completion frontier using finite witness sets, a continuous likelihood-ratio state, nonnegative risk/cost multipliers, and an infimum over witness sets. The repository has no implementation of the associated numerical integration, state approximation, multiplier optimization, witness refinement, or feasible optimal-policy recovery. Implementing those components would require a separately documented numerical method and accuracy assessment. The theoretical result must not be described as a reproduced multivariate experiment.

The adaptive-separation example is also analytical. It uses no historical reports, `(d_min, d_max, D, D_max) = (0.1, 0.2, 1, 1)`, and coarse/fine caps `(224, 307, 307)`, matching the current supplement. A coarse acquisition is a pair of independent scalar stage observations, charged as one bundle with its stated total cost and duration. Thus 224 coarse acquisitions count as 224 bundles; with 307 selected-stage fine reports, the duration is 1452 and the acquisition cost is 2680. This vector-valued acquisition convention does not modify the scalar benchmark.

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

The companion files are maintained in the [GitHub repository](https://github.com/SaeedRazavikia/agentic-wireless-networks), whose visibility and access permissions are managed by the owner.
