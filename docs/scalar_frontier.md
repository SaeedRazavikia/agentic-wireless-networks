# Exact scalar Gaussian completion benchmark

`scripts/scalar_frontier.py` is a **new implementation of the analytical benchmark specified in the supplied manuscript**. It is not the recovered original simulator. It computes exact completion curves and optimal integer report allocations; an optional command samples the endpoint sufficient statistic. It does not reconstruct the unavailable original trial tapes, the 1,966,080-outcome evaluation, sequential stopping, or the practical wireless controllers.

The specification comes from “Completion Frontiers and Practical Curves” in `docs/source/experiments_original.tex` and the exact scalar completion theorem in the paper's supplement. The figure caption identifies the eight supplied frontier CSVs as curves at absolute margin 0.2. Their columns are `deadline,correct`, with 513 deadlines per curve. The original presentation-export provenance remains in `figures/tikz/data/PROVENANCE.json`.

## Model and computation

The centered radio and server means are respectively the scalar margin and its negative. Their costs are 1 and 6; their serialized durations are 1 and 4. Historical precision is zero. The accurate-server catalogue has variances 1 and 1/9; the accurate-radio catalogue reverses these variances. Each report therefore adds precision 1 or 9. The hard acquisition cost and count caps are 512, and modeled deadlines range from 0 through 512.

The script uses integer dynamic programming over exact spent cost and exact elapsed acquisition duration. Every transition adds one legal report. It then maximizes precision over all states within each deadline, choosing lower cost and then lower duration to break precision ties. With these two instruments, cost and duration determine both counts, so merging equal resource states preserves feasibility. The script checks both per-instrument and total count caps; either interpretation is redundant here because each informative report costs at least one unit. Each informative report's duration is no greater than its cost, so deadline 512 already contains every design feasible under the cost cap. Thus an unattainable entry cannot improve with additional acquisition time.

For maximum precision A and nonzero margin m, the exact uniformly safe correct-completion probability is `Phi(abs(m) * sqrt(A) - Phi_inverse(0.95))`. The endpoint test returns the backup above `Phi_inverse(0.95)`, the cheaper service below its negative, and unresolved between the thresholds. The probability curve at zero precision is the randomized frontier 0.05. An operational policy that always abstains has zero correct completion there. Aggregate-only reports have zero loading; the implementation schedules none because they add no precision. It does not invent an aggregate cost or variance.

All analytical commands use Python 3.10 or later and its standard library. Run them from the repository root:

```sh
python scripts/scalar_frontier.py verify
python scripts/scalar_frontier.py table
python scripts/scalar_frontier.py export --output-dir reproduced/scalar-frontier
```

`verify` checks every supplied plot value at margin 0.2 with an absolute tolerance of 1e-12, all 18 reported first-deadline entries, and the reported accurate-server precision ceiling of 767 and completion ceiling of approximately 0.869626 at margin 0.1. It returns a nonzero status for a mismatch and emits a JSON report. `export` creates eight new CSVs and a metadata file in the requested directory; it does not modify the supplied data unless the user explicitly selects that directory. A different valid nonzero margin can be selected with `--margin`.

During repository preparation, the implementation matched all 4,104 supplied curve values with maximum absolute error 3.33e-16 and matched all 18 first-deadline entries. It computed the precise completion ceiling 0.8696255583022073 from 2 radio reports and 85 server reports, costing 512 units and taking 342 duration units. These checks validate the analytical reconstruction against the supplied exports; they do not reproduce the unavailable original trials.

The reported first deadlines for 95% correct completion are:

| Catalogue | Access | Margin 0.1 | Margin 0.2 | Margin 0.4 |
|---|---|---:|---:|---:|
| Accurate server | Radio | Unattainable | 271 | 68 |
| Accurate server | Server | Unattainable | 124 | 32 |
| Accurate server | Both | Unattainable | 121 | 32 |
| Accurate radio | Radio | 121 | 31 | 8 |
| Accurate radio | Server | Unattainable | Unattainable | 272 |
| Accurate radio | Both | 121 | 31 | 8 |

## Optional endpoint Monte Carlo

NumPy is required only for this command. Both the seed and replication count must be supplied explicitly. For example:

```sh
python scripts/scalar_frontier.py monte-carlo --catalogue accurate_server --access both --margin 0.2 --deadline 128 --seed 20260914 --replications 10000
```

This generates independent draws of the Gaussian endpoint sufficient statistic for the selected integer design. It does not generate individual report trajectories or replay the original trials. Both margin signs are supported. The output records the seed, replication count, NumPy version, random-number generator, report counts, acquisition cost and duration, outcome counts, exact expected probabilities, and the sampling standard error for correct completion.

At zero precision, the default policy abstains. Add `--zero-precision randomized` to return each sign with probability 0.05 and abstain otherwise, attaining the theoretical randomized frontier. Monte Carlo frequencies fluctuate around their exact expectations; they are supplementary diagnostics and do not establish the mathematical guarantee. Computation and actuation times are outside this modeled acquisition ledger.
