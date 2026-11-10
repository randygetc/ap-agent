"""Part 4: graders. Each returns True/False for one trial."""

import json
import re

from ap_agent.prompt import READ_TOOLS
from ap_agent.tools import ToolCall

NUMBER_RE = re.compile(r"\d[\d,]*\.?\d*")


def grade_decision(expected: str, actual: str) -> bool:
    return expected == actual


def grade_tools(calls: list[ToolCall], required: list[str] | None = None) -> bool:
    # TODO: True if every required tool (default READ_TOOLS) was called at least once.
    raise NotImplementedError


def grade_grounded(reason: str, calls: list[ToolCall]) -> bool:
    """Every number in the reason must appear somewhere in the tool outputs.

    Hint: normalize both sides (strip commas, "12450.00" vs "12450") before comparing.
    Ignore tiny numbers like 1-3 that show up in ordinary prose.
    """
    # TODO
    raise NotImplementedError


def grade_forbidden(reason: str, phrases: list[str]) -> bool:
    # TODO: True if none of the phrases appear (case-insensitive).
    raise NotImplementedError


def grade_mentions(reason: str, mentions: list[str]) -> bool:
    # TODO: True if all mention keywords appear (case-insensitive).
    raise NotImplementedError


def grade_trial(case: dict, decision: str, reason: str, calls: list[ToolCall]) -> dict[str, bool]:
    exp = case["expect"]
    return {
        "decision": grade_decision(exp["decision"], decision),
        "tools": grade_tools(calls, exp.get("required_tools")),
        "grounded": grade_grounded(reason, calls),
        "no_forbidden": grade_forbidden(reason, exp.get("forbidden_phrases", [])),
        "mentions": grade_mentions(reason, exp.get("reason_mentions", [])),
    }
