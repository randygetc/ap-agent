"""Part 1: MockTools serves case data and logs every call."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    name: str
    args: dict
    result: Any

    @property
    def error(self) -> str | None:
        if isinstance(self.result, dict):
            return self.result.get("error")
        return None


@dataclass
class MockTools:
    """Built from the `tools:` section of a case file.

    Case shape (see evals/cases/happy-01.yaml):
      get_invoice:     {<invoice_id>: {...}}   or {error: "..."}
      get_vendor:      {<vendor_id>: {...}}    or {error: "..."}
      search_invoices: {result: [...]}         or {error: "..."}
      get_budget:      {<department>: {...}}   or {error: "..."}
    """

    data: dict
    calls: list[ToolCall] = field(default_factory=list)

    def call(self, name: str, args: dict) -> Any:
        # TODO (Part 1):
        # 1. If self.data[name] has an "error" key, return {"error": <that message>}.
        # 2. Otherwise look up the record:
        #      get_invoice     -> by args["invoice_id"]
        #      get_vendor      -> by args["vendor_id"]
        #      get_budget      -> by args["department"]
        #      search_invoices -> the "result" list (ignore args; it's a mock)
        # 3. Unknown ID -> {"error": f"{name}: not found: <id>"}  (NOT None or {})
        # 4. Unknown tool name -> {"error": f"unknown tool: {name}"}
        # 5. Append ToolCall(name, args, result) to self.calls before returning.
        raise NotImplementedError
