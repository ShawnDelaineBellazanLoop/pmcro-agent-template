# orchestrator-agent

> PMCR-O v1.5.0 · Loop Controller & O-Mode Governor · v4.2.0

The Orchestrator-Agent is the sole routing authority for the PMCR-O cognitive loop.
It does not plan, execute, validate, or reflect — it **routes**, and it governs the
shape of the loop itself.

---

## Repo Structure

```
orchestrator-agent/
├── SKILL.md                          ← Skill spec (Claude skill loader entry point)
├── README.md                         ← This file
├── scripts/
│   ├── orchestrate.py                ← Invocation entry point (runtime / Claude tool calls)
│   ├── route_cycle.py                ← Pure routing engine (deterministic, no side effects)
│   └── run_cycle.py                  ← PMCR-O cycle frame builder & trail writer
├── references/
│   └── orchestrator-design.md        ← Full design spec: O-Mode, HIL, TrailFrame, MaxLoops
├── assets/
│   ├── request_template.json         ← Input payload schema + example
│   └── orchestrator_frame_template.json  ← Output frame schema + example
├── evals/
│   └── eval_cases.json               ← Test cases for all routing paths
└── .pmcro/
    └── trails/                       ← Runtime TrailFrame output directory (gitignored)
```

---

## Quick Start

```python
from scripts.orchestrate import orchestrate

frame = orchestrate(
    payload={
        "intent": "Refactor authentication module",
        "cycle_id": "CycleQ-20240118-001",
        "loop": 1,
        "max_loops": 3,
        "current_phase": "init",
        "reflector_verdict": None,
        "type1_action_requested": False,
        "hil_token": None,
        "constraints_active": [],
        "context": {}
    },
    governor_verdicts=[]
)

print(frame["routed_to"])   # → "planner"
print(frame["o_mode"])      # → "ITERATIVE"
```

---

## O-Mode Reference

| O-Mode | Use case |
|---|---|
| `DIRECT` | Simple single-pass, no retry |
| `ITERATIVE` | Standard loop, up to max_loops |
| `REFLECTIVE` | Complex tasks, EarnedConstraint generation |
| `ESCALATION` | Risk/safety block, HIL required |
| `ORCHESTRATE` | Meta — spawns sub-cycles |
| `AUDIT` | Read-only validation, no mutations |

---

## Key Governance Rules

- **ORC-001** — Planner First: all new intents route to Planner
- **ORC-007** — MaxLoops (EC-009): loop ≥ max_loops + RETRY → HIL
- **ORC-010** — Governance pre-check before every dispatch
- **ORC-014** — TrailFrame written for every routing decision
- **ORC-018** — TYPE 1 actions require valid HIL token (MAAI-001)
- **ORC-022** — O-Mode may adapt between iterations

---

## Domain Universality

PMCR-O is declarative and template-driven. This orchestrator pattern applies
verbatim to any domain — git commits, Jira tickets, Terraform plans, CI/CD pipelines,
database migrations — by substituting domain vocabulary while keeping the loop
topology, frame schema, and routing rules constant.

See `references/orchestrator-design.md` for the full design rationale.