# Controller implementation specification

This guide collects implementation details stated in the supplied manuscript and supplementary acquisition source. It specifies the reported controller interfaces and safeguards. The original controller implementations are not present; the four supplied Python programs draw figures. The complete original acquisition derivation is preserved in [`source/acquisition_original.tex`](source/acquisition_original.tex), while the paper and theoretical supplement retain the proof prerequisites.

The executable analytical benchmark is [`scripts/scalar_frontier.py`](../scripts/scalar_frontier.py). It implements integer precision maximization and the scalar Gaussian endpoint test. The updated manuscript's multivariate finite-witness frontier, likelihood-state Bellman recursion, multiplier optimization, and feasible-policy recovery are not implemented. Controller specifications below describe the supplied studies; they do not imply that their original implementations are available. See [`manuscript_alignment.md`](manuscript_alignment.md) for the manuscript mapping and the missing-record inventory.

## Paired coarse acquisition convention

The adaptive-separation example extends the scalar-report notation by acquiring two independent scalar observations as one coarse bundle. A coarse acquisition returns one observation of each stage, with independent Gaussian coordinate errors of variance `sigma_D²`. It consumes one coarse count and the declared total bundle price `c_D` and duration `ell_D`. A fine acquisition returns one scalar observation of its selected stage. All fresh errors are independent across acquisitions and coordinates.

The coarse count therefore measures pairs, not individual coordinates. The bundle supplies information about both stages while its cost and duration are charged once. In the numerical example, 224 coarse acquisitions and 307 selected-stage fine reports retain duration `224 + 4 × 307 = 1452` and cost `224 + 8 × 307 = 2680`, with coarse/fine caps `(300, 400, 400)`. This convention clarifies accounting without changing the example's formulas, bounds, or numerical values.

## Verification and acquisition loop

The reported execution order is:

1. Read the current goal, valid model restrictions, retained evidence, and absolute resource ledger.
2. Intersect each affine-response confidence interval with earlier intervals and valid physical bounds. Treat constants as exact and unestimable directions as having infinite radius. An empty intersection indicates model conflict.
3. Verify the proposed configuration's own feasibility and exclude every feasible rival that could improve the objective by more than the goal tolerance. A rival can be excluded jointly without identifying a particular violated stage. Eliminate a candidate on objective grounds only when it is certainly more than the tolerance worse than a certainly feasible candidate.
4. If verification succeeds, authorize the corresponding answer. If a conflict is detected, report it. Otherwise choose a legal acquisition batch using the declared rule.
5. Charge the acquired reports, update counts and sums, and invoke the complete verifier again. Return unresolved when no admissible continuation or certificate is obtained.

Allocation affects which evidence is acquired; it never replaces observed-data verification. Ridge regularization may guide a center or an allocation objective but does not authorize a certificate.

## Absolute resource ledger

Retain the original historical counts, fresh counts, report prices, report durations, and total count limits. Discarding historical evidence does not erase reports already consumed under a total cap. Every fresh pilot, audit, discovery, and completion report counts toward both cost and acquisition duration. The modeled duration excludes computation; controller times are reported separately.

For the two-instrument guarded study, aggregate and server counts are `n_A` and `n_S`; costs and durations are:

$$C(n)=n_A+8n_S,\qquad T(n)=n_A+4n_S.$$

There are 512 historical reports per instrument, an absolute cap of 4000 per instrument, and therefore at most 3488 fresh reports per instrument. The budget pairs are `(5000, 4000)` and `(14000, 9000)`. A proposed plan must pass the original cost, duration, and count checks after integer rounding. Clipping an over-budget plan can destroy its advertised completion property.

A changed service request can reuse evidence within a valid coefficient epoch. It does not reset physical quotas or previously spent statistical risk. A changed physical regime requires reassessing evidence validity; the agent-loop study quarantines earlier evidence after an announced change.

## Residual and comparator allocations

At a fixed empirical center, the residual rule solves the declared alternative-distance allocation problem, regards an infeasible design as having infinite cost, and selects the cheapest attained proposal. The separate resource-aware comparator maximizes the minimum alternative distance under remaining time and count constraints. It minimizes cost if it attains a target of `1.10 beta²`; otherwise it executes the best attained maximin design. Projection cuts and dual witnesses bound numerical optimization gaps. Neither this empirical-center search nor quota rounding establishes future completion or integer optimality.

The frozen nine-pair studies use distinct comparators:

| Comparison | Declared rule and execution details |
| --- | --- |
| 64 paired sequences, seeds 57000000–57000063 | Goals `24 → 12.6 → 9.5 → 24` ms; batch size at most 8; residual replans within 512 reports with inflation 1.1; all methods retain original caps and a common v10 `JointVerifier`. |
| Authors-code G-ACOL adaptation | Select the most uncertain remaining target, then choose the report giving its largest one-report variance reduction. Allocation uses `(M + 0.1 I)^(-1)` and does not divide the score by price. The source identifies upstream commit `33fc4d2`; its code was not supplied. |
| Printed maximum-variance adaptation | Measure the most uncertain remaining configuration. Do not transfer the published method's guarantees to these noise/history/batching/verifier adaptations. |
| Separate 32-sequence custom maximin confirmation | Use an added-cost planning allowance of current-goal expenditure plus the sum of report prices, 64 iterations, and tolerance 0.005. This planning allowance is not the physical budget. |

Paired bootstrap intervals for the 64-sequence study resample complete sequences 10,000 times using seed 57009999. Preserve comparator-specific populations and tapes; do not merge these comparisons into a single sample.

## Auditing historical reports

The earlier paid-audit study acquires 128 fresh reports of each instrument before admitting historical evidence. For 512 historical reports and 128 audit reports, the declared upper bound is

$$U_e=|\overline Y_{e,h}-\overline Y_{e,128}|+
\sqrt{2(1/512+1/128)\log(4/0.005)}.$$

History is admitted when this value is at most 0.9. The audit costs 1152 and lasts 640 modeled units. This particular paid-audit study is distinct from the later guarded controller's checkpoint audit below.

The guarded controller uses deterministic legal checkpoints: `(16,16)`, then legal ray points `(ceil(sqrt(8) s_k), s_k)` for `s_k = 16 · 2^k`, followed by a legal dominating endpoint. The terminal endpoints stated in the source are `(1304,462)` for the smaller budget and `(3488,1314)` for the larger budget. They minimize the declared reciprocal-count criterion, with cost/duration/count ties. Causal batches verify after acquisition and eventually reach the next checkpoint if unresolved and legal progress remains.

At checkpoint `k`, define the historical/fresh discrepancy, standard error, and upper bound as

$$D_{e,k}=\overline H_e-\overline Y_{e,n_e^{(k)}},\quad
 a_{e,k}=\sqrt{1/h_e+1/n_e^{(k)}},\quad
 U_{e,k}=|D_{e,k}|+q_{e,k}a_{e,k}.$$

Cache the minimum of these bounds over checkpoints. The source uses `q = Phi^(-1)(1 − alpha/(4L))`, with `alpha = 0.005` and `L` deterministic checkpoints. A historical mask is eligible only if every retained instrument's cached bound is at most 0.9. The fresh mask always remains available. The simultaneous audit and all-mask/all-prefix confidence events each spend risk 0.005; the reported verifier constant is `beta = 7.886153024504561`.

Auditing statistical shifts does not establish the separate physical residual envelope. A fresh-only mask does not erase risk from earlier historical returns.

## Fixed-action historical extension

The primary guarded confirmation uses the same acquisition action rule as the fresh controller. That rule depends only on fresh counts and sums. The extension additionally checks historical masks and audits already charged prefixes. Consequently, coupled actions agree up to stopping; extending the verifier can stop a fixed-goal trajectory earlier without adding physical acquisition. This statement excludes computation and does not establish sequence-wide dominance after stopping states diverge.

The source reports a small mean fixed-goal saving of 0.138%, below its declared 2% target. History-guided acquisition and different audit schedules define different comparisons and cannot isolate this verifier extension.

## Sufficient reserves and observable promises

A sufficient reserve freezes the goal, proposal, history mask, risk allowances, and nonnegative exclusion witnesses at its checkpoint. Integer quotas must satisfy the original remaining resource constraints and the declared conservative margin test. If the test passes, freeze the quotas; stop early only after the complete observed-data verifier certifies the same proposal. The proof controls the joint event of issuance and failure; it does not guarantee that a reserve will be issued.

The later observable-promise rule enumerates deterministic future checkpoints, eligible masks, and complete certificates. It chooses minimum total cost with fixed duration/mask/certificate ties and strict inward numerical buffers. Future variance differs from full-estimator variance because historical sums and already acquired fresh sums are conditioned upon. Zero future variance is deterministic. The source's planning set spends risk 0.01 and the future allowance is 0.03 for one goal.

Record a promise's absolute endpoint and subtract acquisition already spent to obtain the remaining reservation. Record a missed first promise even if later acquisition succeeds within the overall budget. Empirical success of selected promises and 512 successful planning futures do not establish uniform conditional success. For multiple predictable goals, use one shared ledger and allocate the future allowance across goals; randomly restarting relative checkpoints requires new calibration.

## Practical four-configuration policies

The practical six-mean model uses aggregates and optional radio counters, with zero lower bounds explicitly retained for the reported practical curves. Coverage selects the smallest absolute count using a seeded random tie order. Goal-directed acquisition targets the cheapest unexcluded configuration and maximizes reduction of unresolved directional uncertainty per duration. Both truncate before unaffordable batches.

The declared grid crosses two row orientations, radio limits 3.8/3.1 ms, history 0/256 per aggregate, and all probes versus aggregates plus fixed counter 5. Caps, risk, and batch size are 4096, 0.05, and 4. Deadlines are `0, 16, 32, 64, 128, 256, 512`; there are 16 paired seeds. Bootstrap resampling must preserve seed clusters, orientations, and deadlines. The corrected prior replay is a distinct comparison: adding the generator's valid radio minima removes the original one-counter advantage.

The source contains no complete implementation of the diagnostic FCFS generator, controller optimizer, LP auditor, or language-model tool harness. Exact source recovery is required before claiming a replay of those studies.
