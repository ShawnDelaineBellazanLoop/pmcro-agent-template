# Universal Agent Design Notes
**Version:** 4.4.2

## Architectural Philosophy
Every agent spawned from this template is an autonomous "Cognitive Unit." It does not just run scripts; it manages its own state through the P-M-C-R-O loop.

---

## Core System Laws

1.  **EC-SYS-001 (Atomic File Protocol):** Output the **entire file** for any modification. Partial updates are forbidden.
2.  **EC-SYS-002 (Minimalist Planning):** The Planner phase must produce only the **bare minimum** actionable steps for the current loop.
3.  **EC-SYS-003 (Log Before Act):** No state-mutating write occurs until the `open` phase of the cycle is recorded in `.pmcro/trails/`.

---

## Data-Driven Persistence (TrailFrames)

The agent's memory is stored in `.pmcro/trails/`. This is organized hierarchically to reflect the relationship between Cycles and Loops:

`/.pmcro/trails/<cycle_id>/<loop_number>.json`

### The Schema of Thought
Each Loop file (e.g., `1.json`) must contain:
- `skill`: The identity of the agent.
- `intent`: The goal being pursued.
- `cycle_id`: The session identifier.
- `loop`: The current attempt number.
- `phases`: A dictionary recording the `status`, `timestamp`, and `data` for every phase (open, plan, make, check, reflect, close).

## Orchestration vs. Execution
- **`orchestrate.py`**: Acts as the "Inner Voice" that moves the agent between phases.
- **`route_cycle.py`**: Acts as the "Pre-frontal Cortex" making the logical decision on where to go next.
- **`domain_config.json`**: Acts as the "Persona," projecting generic phases into domain actions (e.g., `maker` -> `git commit`).