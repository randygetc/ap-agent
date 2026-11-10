# AP Invoice Agent + Eval Harness

An accounts-payable agent that investigates an invoice with read-only tools and
recommends `submit` or `reject`, plus a deterministic guardrail layer and an
eval harness that measures it.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
export AP_MODEL=claude-sonnet-5-5   # optional override
```

## Layout

```
ap_agent/
  prompt.py       # system prompt + tool schemas (done)
  tools.py        # MockTools: serves case data, logs calls      <- Part 1
  agent.py        # manual tool-use loop                         <- Part 2
  guardrails.py   # deterministic checks + override              <- Part 3
evals/
  cases/*.yaml    # one scenario per file                        <- Part 4
  grade.py        # graders                                      <- Part 4
  run_evals.py    # runs cases x trials, prints report           <- Part 4
```

## Parts

1. **tools.py** — Implement `MockTools.call()`. Return case data, return
   `{"error": ...}` for configured failures AND for unknown IDs. Log every call.
2. **agent.py** — Implement `run_agent()`. Loop: send messages, execute
   `tool_use` blocks against MockTools, append `tool_result` blocks, repeat.
   Stop when the model calls `record_recommendation`. Cap at `MAX_TURNS`
   (hitting the cap = reject).
3. **guardrails.py** — Implement `apply_guardrails()`. Reject on missing
   required tools or any tool error; compute vendor/duplicate/budget checks in
   code; override a model `submit` when a check fails; record `overridden`.
4. **evals** — Write 10 cases (one per category), implement graders, run each
   case 3 times, print the report.

Work in that order. Run `python -m evals.run_evals --raw` and without `--raw`
to compare model-only vs guarded results.

## Rules to decide before writing cases

Write your answers here; the graders and guardrails must agree with them.

- Vendor passes when: ...
- Duplicate means: ...
- Budget passes when (strict `<` or `<=`, pending commitments?): ...
- Missing invoice fields that force reject: ...

## Definition of done

```
Cases: 10 | Trials: 30
False submits:  0
False rejects:  ...
Override rate:  ...
By category:    ...
```
