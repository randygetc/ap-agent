"""Part 3: deterministic checks. The code owns the decision; the model owns the explanation."""

from dataclasses import dataclass

from .agent import AgentResult
from .prompt import READ_TOOLS

REQUIRED_INVOICE_FIELDS = {"vendor_id", "number", "amount", "department"}  # adjust to match your README rules
FORBIDDEN_PHRASES = ["approved", "payment released", "has been paid", "submitted for payment"]


@dataclass
class GuardedResult:
    decision: str
    reason: str
    model_decision: str
    overridden: bool
    failed_checks: list[str]


def check_vendor(vendor: dict) -> str | None:
    """Return a failure message, or None if the vendor passes."""
    # TODO: implement your "Vendor passes when" rule from the README.
    raise NotImplementedError


def check_duplicate(invoice: dict, matches: list[dict]) -> str | None:
    # TODO: implement your "Duplicate means" rule. Remember to exclude the
    # invoice itself if search_invoices returns it.
    raise NotImplementedError


def check_budget(invoice: dict, budget: dict) -> str | None:
    # TODO: implement your budget rule (strict < vs <=, include pending?).
    raise NotImplementedError


def apply_guardrails(result: AgentResult) -> GuardedResult:
    failed: list[str] = []

    # TODO (Part 3):
    # 1. Missing required tools: READ_TOOLS - {c.name for c in result.tool_calls}
    #    -> add "missing: <tool>" for each.
    # 2. Any call with c.error -> add "tool error: <name>: <error>".
    # 3. If result.hit_cap -> add "turn cap reached".
    # 4. If no structural failures, pull the LAST successful result for each tool
    #    from result.tool_calls and run:
    #      - REQUIRED_INVOICE_FIELDS present on the invoice
    #      - check_vendor, check_duplicate, check_budget
    # 5. Forbidden phrases in result.reason -> add "forbidden claim in reason".
    # 6. Decision: "reject" if failed else result.decision.
    #    (Note: if failed is empty but the model said reject, keep reject.
    #     That's a false reject you'll see in the evals, not something to override.)
    # 7. overridden = (result.decision == "submit" and decision == "reject")
    # 8. Reason: if overridden, use "; ".join(failed); otherwise result.reason.
    raise NotImplementedError
