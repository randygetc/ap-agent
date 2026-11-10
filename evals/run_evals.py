"""Part 4: run every case x TRIALS and print the report.

    python -m evals.run_evals          # guarded (model + guardrails)
    python -m evals.run_evals --raw    # model only
    python -m evals.run_evals --case dup  # only cases whose id contains "dup"
"""

import argparse
from collections import defaultdict
from pathlib import Path

import yaml

from ap_agent.agent import run_agent
from ap_agent.guardrails import apply_guardrails
from ap_agent.tools import MockTools

from .grade import grade_trial

CASES_DIR = Path(__file__).parent / "cases"
TRIALS = 3


def load_cases(filter_: str | None) -> list[dict]:
    cases = [yaml.safe_load(p.read_text()) for p in sorted(CASES_DIR.glob("*.yaml"))]
    return [c for c in cases if not filter_ or filter_ in c["id"]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", action="store_true", help="skip guardrails")
    ap.add_argument("--case", help="substring filter on case id")
    ap.add_argument("--trials", type=int, default=TRIALS)
    args = ap.parse_args()

    cases = load_cases(args.case)
    rows = []  # (case, trial_index, final_decision, overridden, grades)

    for case in cases:
        for t in range(args.trials):
            tools = MockTools(case["tools"])
            result = run_agent(case["invoice_id"], tools)
            if args.raw:
                decision, reason, overridden = result.decision, result.reason, False
            else:
                g = apply_guardrails(result)
                decision, reason, overridden = g.decision, g.reason, g.overridden
            grades = grade_trial(case, decision, reason, result.tool_calls)
            rows.append((case, t, decision, overridden, grades))
            mark = "PASS" if all(grades.values()) else "FAIL"
            print(f"  {mark} {case['id']} t{t + 1}: {decision}"
                  + ("" if all(grades.values()) else f"  {[k for k, v in grades.items() if not v]}"))

    # TODO (Part 4): compute and print
    #   Cases: N | Trials: M
    #   False submits:  expected reject, got submit   (list case ids + count)
    #   False rejects:  expected submit, got reject
    #   Override rate:  overridden / trials  (guarded mode only)
    #   By category:    passes/trials per case["category"], where a trial
    #                   passes only if every grade is True
    raise NotImplementedError


if __name__ == "__main__":
    main()
