# Universal Agent Design Notes
**Version:** 4.4.2

This document outlines the architectural principles for all specialized agents
spawned from the `pmcro-agent-template`. Every agent inherited from this
blueprint is a self-orchestrating cognitive entity.

---

## Core System Laws

All agents must strictly adhere to the following constraints to maintain
ecosystem integrity:

1. **EC-SYS-001 (Atomic File Protocol):**
   Output must never contain partial code snippets or "diffs" for file
   modifications. The agent must output the **entire file** content to
   prevent structural corruption and ensure the state is always valid.

2. **EC-SYS-002 (Minimalist Planning):**
   The internal Planner phase must only decompose an intent into the
   **bare minimum** steps required for the immediate loop. Speculative
   planning for future cycles is prohibited to prevent logic bloat.

3. **EC-SYS-003 (Log Before Act):**
   No state-mutating write occurs until the `open` phase of the cycle
   is recorded in `.pmcro/trails/`. Unlogged writes are integrity violations.

---

## Routing Precedence Order

The internal engine (`route_cycle.py`) evaluates conditions in a fixed sequence:

1. **Governance Pre-check:** Any BLOCK or ESCALATE verdict wins immediately.
2. **TYPE 1 Authorization:** State mutations require a valid HIL token.
3. **MaxLoops Guardrail:** Prevents infinite looping (EC-009).
4. **Reflector Verdict:** Processes ACCEPT, RETRY, or ESCALATE.
5. **Sequential Phase Routing:** Standard fallback (P -> M -> C -> R -> O).

---

## Data-Driven Persistence (TrailFrames)

The agent's memory is stored in `.pmcro/trails/`. This is organized
hierarchically to reflect the relationship between Cycles and Loops:

`.pmcro/trails/<cycle_id>/<loop_number>.json`

### The Schema of Thought
Each loop file (e.g., `1.json`) must contain:
- `skill`: The identity of the agent.
- `intent`: The goal being pursued.
- `cycle_id`: The session identifier.
- `loop`: The current attempt number.
- `phases`: A dictionary recording the `status`, `timestamp`, and `data`
  for every phase (open, plan, make, check, reflect, close).

---

## Domain Projection

Each specialized agent provides a `domain_config.json`. The universal engine
takes the generic phase (e.g., `maker`) and projects it into a domain-specific
`domain_action` (e.g., `git commit` or `AWS Provisioning`).

This allows the **Code** to remain identical across the fleet while the
**Identity** remains unique and data-driven.

---

## Orchestration vs. Execution

- **`orchestrate.py`**: Acts as the "Inner Voice" that moves the agent between phases.
- **`route_cycle.py`**: Acts as the "Prefrontal Cortex" making the logical decision on where to go next.
- **`run_cycle.py`**: The lifecycle utility that builds and writes TrailFrames to disk.
- **`log_frame.py`**: CLI shim for manually recording individual phase transitions during development.
- **`domain_config.json`**: Acts as the "Persona," projecting generic phases into domain actions.

---

## Self-Framing (Internal Audit)

Every time an agent is invoked to make a routing decision, it performs a
"Self-Frame." This is a recursive PMCR-O loop where the agent acts as its
own orchestrator, logging its internal reasoning to `.pmcro/trails/`. This
ensures the "Short-Term Memory" of the agent's thought process is preserved.

The canonical self-frame sequence:
```python
cycle.orchestrate_open(o_mode="DIRECT", governance_pre_checks=[...])
cycle.plan(steps=[...])
cycle.make(action="route(payload)", result=decision_frame["domain_action"])
cycle.check(passed=True, issues=[])
cycle.reflect(training_example={...}, loop_verdict="ACCEPT")
cycle.orchestrate_close(summary="Routed to ...")
cycle.write()
```

---

## Spawning a New Agent

1. Create a repo from the `pmcro-agent-template` (GitHub "Use this template").
2. Update `domain_config.json` with the new `domain` and `domain_map` vocabulary.
3. Update `SKILL.md` frontmatter: replace `{{AGENT_NAME}}`, `{{DOMAIN_DESCRIPTION}}`, `{{AGENT_DOMAIN}}`.
4. Run `python scripts/run_evals.py` to certify the inherited routing engine.
5. Run the Genesis Cycle: `python scripts/orchestrate.py assets/request_template.json`.
