"""Part 2: manual tool-use loop."""

import json
import os
from dataclasses import dataclass

import anthropic

from .prompt import FINAL_TOOL, SYSTEM_PROMPT, TOOLS
from .tools import MockTools, ToolCall

MODEL = os.environ.get("AP_MODEL", "claude-sonnet-5-5")
MAX_TURNS = 10


@dataclass
class AgentResult:
    decision: str            # "submit" | "reject"
    reason: str
    tool_calls: list[ToolCall]
    turns: int
    hit_cap: bool = False


def run_agent(invoice_id: str, tools: MockTools, client: anthropic.Anthropic | None = None) -> AgentResult:
    client = client or anthropic.Anthropic()
    messages = [{
        "role": "user",
        "content": f"Investigate invoice {invoice_id} and record your recommendation.",
    }]

    for turn in range(1, MAX_TURNS + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        # TODO (Part 2):
        # 1. Append the assistant turn: {"role": "assistant", "content": response.content}
        # 2. For each block where block.type == "tool_use":
        #      - If block.name == FINAL_TOOL: return AgentResult(
        #            decision=block.input["decision"], reason=block.input["reason"],
        #            tool_calls=tools.calls, turns=turn)
        #      - Else: result = tools.call(block.name, block.input) and build
        #            {"type": "tool_result", "tool_use_id": block.id,
        #             "content": json.dumps(result),
        #             "is_error": "error" in result if isinstance(result, dict) else False}
        # 3. If there were tool_use blocks, append one user message whose content
        #    is the list of tool_result blocks, then continue the loop.
        # 4. If stop_reason is "end_turn" with no tool_use (model answered in text
        #    instead of calling record_recommendation), append a user message
        #    reminding it to call record_recommendation, and continue.
        raise NotImplementedError

    return AgentResult(
        decision="reject",
        reason=f"Agent did not finish within {MAX_TURNS} turns.",
        tool_calls=tools.calls,
        turns=MAX_TURNS,
        hit_cap=True,
    )
