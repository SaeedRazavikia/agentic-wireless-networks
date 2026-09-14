#!/usr/bin/env python3
"""New implementation of the paper's specified exact scalar Gaussian benchmark.

This is not the recovered original simulator. Analytical curves use only the
Python standard library. Optional endpoint Monte Carlo requires NumPy and an
explicit seed and replication count. See docs/scalar_frontier.md.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
from statistics import NormalDist


ROOT = Path(__file__).resolve().parents[1]
NORMAL = NormalDist()
BUDGET = COUNT_CAP = MAX_DEADLINE = 512
RISK = 0.05
CATALOGUES = ("accurate_server", "accurate_radio")
ACCESS = ("aggregate", "radio", "server", "both")
MARGINS = (0.1, 0.2, 0.4)
EXPECTED_DEADLINES = {
    ("accurate_server", "radio"): (None, 271, 68),
    ("accurate_server", "server"): (None, 124, 32),
    ("accurate_server", "both"): (None, 121, 32),
    ("accurate_radio", "radio"): (121, 31, 8),
    ("accurate_radio", "server"): (None, None, 272),
    ("accurate_radio", "both"): (121, 31, 8),
}


@dataclass(frozen=True)
class Plan:
    precision: int = 0
    radio: int = 0
    server: int = 0
    cost: int = 0
    duration: int = 0


def plan_key(plan: Plan) -> tuple[int, int, int, int, int]:
    """Maximize precision, then prefer lower cost, time, and counter counts."""
    return (plan.precision, -plan.cost, -plan.duration, -plan.server, -plan.radio)


def frontier(catalogue: str, access: str) -> list[Plan]:
    """Integer DP over exact spent cost and serialized acquisition duration.

    Each transition adds one report. Positive costs give an acyclic DP. We
    enforce the 512-report cap explicitly; it is also implied by the 512-unit
    cost cap because every informative report costs at least one unit. With
    these two instruments, exact cost and duration determine both counts, so
    merging states cannot hide different remaining count allowances.
    """
    if catalogue not in CATALOGUES or access not in ACCESS:
        raise ValueError("unknown catalogue or instrument access")
    precision = (1, 9) if catalogue == "accurate_server" else (9, 1)
    probes = []
    if access in ("radio", "both"):
        probes.append((1, 1, precision[0], 1, 0))
    if access in ("server", "both"):
        probes.append((6, 4, precision[1], 0, 1))
    # Zero-loading aggregate reports cannot increase precision. No aggregate
    # price or variance is invented: an optimum can omit those reports.
    states: list[dict[int, Plan]] = [{} for _ in range(BUDGET + 1)]
    states[0][0] = Plan()
    at_time = [Plan() for _ in range(MAX_DEADLINE + 1)]
    for spent, time_states in enumerate(states):
        for duration, plan in time_states.items():
            if plan_key(plan) > plan_key(at_time[duration]):
                at_time[duration] = plan
            for cost, time, information, radio, server in probes:
                next_cost, next_time = spent + cost, duration + time
                if next_cost > BUDGET or next_time > MAX_DEADLINE:
                    continue
                nr, ns = plan.radio + radio, plan.server + server
                if nr > COUNT_CAP or ns > COUNT_CAP or nr + ns > COUNT_CAP:
                    continue
                candidate = Plan(plan.precision + information, nr, ns,
                                 next_cost, next_time)
                previous = states[next_cost].get(next_time)
                if previous is None or plan_key(candidate) > plan_key(previous):
                    states[next_cost][next_time] = candidate
    for deadline in range(1, MAX_DEADLINE + 1):
        if plan_key(at_time[deadline - 1]) > plan_key(at_time[deadline]):
            at_time[deadline] = at_time[deadline - 1]
    return at_time


def correct_probability(precision: int, margin: float) -> float:
    """Exact safe completion frontier, including randomized value delta at A=0."""
    return NORMAL.cdf(abs(margin) * math.sqrt(precision) - NORMAL.inv_cdf(1 - RISK))


def first_deadline(plans: list[Plan], margin: float) -> int | None:
    required = ((NORMAL.inv_cdf(1 - RISK) + NORMAL.inv_cdf(0.95)) / abs(margin)) ** 2
    return next((h for h, p in enumerate(plans) if p.precision >= required), None)


def all_frontiers() -> dict[tuple[str, str], list[Plan]]:
    return {(catalogue, access): frontier(catalogue, access)
            for catalogue in CATALOGUES for access in ACCESS}


def verify(data_dir: Path, tolerance: float) -> dict:
    curves = all_frontiers()
    comparisons, errors, points = [], [], 0
    for (catalogue, access), plans in curves.items():
        path = data_dir / f"frontier_{catalogue}_{access}.csv"
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != ["deadline", "correct"]:
                raise ValueError(f"unexpected columns in {path}")
            rows = list(reader)
        deadlines = [int(row["deadline"]) for row in rows]
        if deadlines != list(range(MAX_DEADLINE + 1)):
            raise ValueError(f"expected each integer deadline 0..512 once in {path}")
        deviations = [abs(float(row["correct"]) - correct_probability(plans[h].precision, 0.2))
                      for h, row in enumerate(rows)]
        if not all(math.isfinite(value) for value in deviations):
            raise ValueError(f"nonfinite probability in {path}")
        maximum = max(deviations)
        comparisons.append({"file": path.name, "points": len(rows),
                            "max_absolute_error": maximum})
        points += len(rows)
        if maximum > tolerance:
            errors.append(f"curve mismatch: {path.name}")
    table = []
    for key, expected in EXPECTED_DEADLINES.items():
        actual = tuple(first_deadline(curves[key], margin) for margin in MARGINS)
        table.append({"catalogue": key[0], "access": key[1],
                      "margins": MARGINS, "expected": expected, "computed": actual})
        if actual != expected:
            errors.append(f"first-deadline mismatch: {key}")
    capped = curves[("accurate_server", "both")][-1]
    cap_probability = correct_probability(capped.precision, 0.1)
    if capped.precision != 767 or abs(cap_probability - 0.869626) > 0.0000005:
        errors.append("accurate-server precision/completion cap mismatch")
    return {"implementation": "new analytical reconstruction; original simulator not recovered",
            "passed": not errors, "curve_points_checked": points,
            "reference_margin": 0.2, "absolute_tolerance": tolerance,
            "curves": comparisons, "first_deadlines": table,
            "accurate_server_cap": {**asdict(capped), "margin": 0.1,
                                    "correct_probability": cap_probability},
            "errors": errors}


def export(output: Path, margin: float) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for (catalogue, access), plans in all_frontiers().items():
        with (output / f"frontier_{catalogue}_{access}.csv").open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(("deadline", "correct"))
            writer.writerows((h, correct_probability(p.precision, margin))
                             for h, p in enumerate(plans))
    metadata = {"implementation": "new analytical reconstruction; original simulator not recovered",
                "margin": margin, "wrong_return_risk": RISK, "cost_cap": BUDGET,
                "count_cap": COUNT_CAP, "maximum_deadline": MAX_DEADLINE,
                "history": "empty", "zero_precision_curve": "randomized frontier 0.05"}
    (output / "scalar_frontier_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


def monte_carlo(args: argparse.Namespace) -> dict:
    try:
        import numpy as np
    except ImportError as exc:
        raise ValueError("Monte Carlo requires NumPy; analytical commands use the standard library") from exc
    plan = frontier(args.catalogue, args.access)[args.deadline]
    rng = np.random.default_rng(args.seed)
    correct = wrong = unresolved = 0
    threshold = NORMAL.inv_cdf(1 - RISK)
    # Chunking bounds memory; the supplied seed and replication count are recorded.
    remaining = args.replications
    while remaining:
        size = min(remaining, 100_000)
        if plan.precision:
            z = rng.normal(args.margin * math.sqrt(plan.precision), 1, size=size)
            positive, negative = z > threshold, z < -threshold
        elif args.zero_precision == "randomized":
            u = rng.random(size)
            positive, negative = u < RISK, (u >= RISK) & (u < 2 * RISK)
        else:
            unresolved += size
            remaining -= size
            continue
        correct += int(np.count_nonzero(positive if args.margin > 0 else negative))
        wrong += int(np.count_nonzero(negative if args.margin > 0 else positive))
        unresolved += size - int(np.count_nonzero(positive)) - int(np.count_nonzero(negative))
        remaining -= size
    if plan.precision:
        expected_correct = correct_probability(plan.precision, args.margin)
        expected_wrong = NORMAL.cdf(-abs(args.margin) * math.sqrt(plan.precision) - threshold)
    else:
        expected_correct = expected_wrong = RISK if args.zero_precision == "randomized" else 0.0
    return {"implementation": "new endpoint sufficient-statistic simulation; not original trial replay",
            "catalogue": args.catalogue, "access": args.access, "margin": args.margin,
            "deadline": args.deadline, "seed": args.seed, "replications": args.replications,
            "numpy_version": np.__version__, "bit_generator": type(rng.bit_generator).__name__,
            "zero_precision_policy": args.zero_precision, "plan": asdict(plan),
            "correct": correct, "wrong": wrong, "unresolved": unresolved,
            "empirical_correct_probability": correct / args.replications,
            "expected_correct_probability": expected_correct,
            "expected_wrong_probability": expected_wrong,
            "expected_unresolved_probability": 1 - expected_correct - expected_wrong,
            "correct_sampling_standard_error": math.sqrt(expected_correct * (1 - expected_correct) / args.replications)}


def margin_value(value: str) -> float:
    margin = float(value)
    if not math.isfinite(margin) or not 0 < abs(margin) < 0.8:
        raise argparse.ArgumentTypeError("the specified benchmark requires 0 < |margin| < 0.8")
    return margin


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("verify", help="compare 4104 original plot values and the 18 deadline entries")
    check.add_argument("--data-dir", type=Path, default=ROOT / "figures/tikz/data")
    check.add_argument("--tolerance", type=float, default=1e-12)
    write = commands.add_parser("export", help="write eight newly computed CSV curves and provenance metadata")
    write.add_argument("--output-dir", type=Path, required=True)
    write.add_argument("--margin", type=margin_value, default=0.2)
    commands.add_parser("table", help="print first deadlines for margins 0.1, 0.2, and 0.4")
    simulation = commands.add_parser("monte-carlo", help="sample the endpoint statistic with an explicit fixed seed")
    simulation.add_argument("--catalogue", choices=CATALOGUES, default="accurate_server")
    simulation.add_argument("--access", choices=ACCESS, default="both")
    simulation.add_argument("--margin", type=margin_value, default=0.2)
    simulation.add_argument("--deadline", type=int, default=128)
    simulation.add_argument("--seed", type=int, required=True)
    simulation.add_argument("--replications", type=int, required=True)
    simulation.add_argument("--zero-precision", choices=("abstain", "randomized"), default="abstain")
    args = parser.parse_args()
    try:
        if args.command == "verify":
            if not math.isfinite(args.tolerance) or args.tolerance < 0:
                parser.error("tolerance must be finite and nonnegative")
            result = verify(args.data_dir, args.tolerance)
            print(json.dumps(result, indent=2))
            return 0 if result["passed"] else 1
        if args.command == "export":
            export(args.output_dir, args.margin)
            print(f"Wrote eight new analytical curves to {args.output_dir}")
        elif args.command == "table":
            print("catalogue,access,margin_0.1,margin_0.2,margin_0.4")
            for key, plans in all_frontiers().items():
                values = [first_deadline(plans, margin) for margin in MARGINS]
                print(",".join((*key, *("unattainable" if v is None else str(v) for v in values))))
        else:
            if not 0 <= args.deadline <= MAX_DEADLINE or args.replications <= 0 or args.seed < 0:
                parser.error("deadline must be in 0..512, replications positive, and seed nonnegative")
            print(json.dumps(monte_carlo(args), indent=2))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
