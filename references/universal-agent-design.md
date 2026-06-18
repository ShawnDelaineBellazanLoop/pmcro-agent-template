# Universal Agent Design Notes
**Version:** 4.4.1

This document outlines the architectural principles for all specialized agents 
spawned from the `pmcro-agent-template`. Every agent inherited from this 
blueprint is a self-orchestrating cognitive entity.

---

## Core System Laws

All agents must strictly adhere to the following constraints to maintain 
ecosystem integrity:

1.  **EC-SYS-001 (Atomic File Protocol):** 
    Output must never contain partial code snippets or "diffs" for file 
    modifications. The agent must output the **entire file** content to 
    prevent structural corruption and ensure the state is always valid.
2.  **EC-SYS-002 (Minimalist Planning):** 
    The internal Planner phase must only decompose an intent into the 
    **bare minimum** steps required for the immediate loop. Speculative 
    planning for future cycles is prohibited to prevent logic bloat.

---

## Routing Precedence Order

The internal engine (`route_cycle.py`) evaluates conditions in a fixed sequence:

1.  **Governance Pre-check:** Any BLOCK or ESCALATE verdict wins immediately.
2.  **TYPE 1 Authorization:** State mutations require a valid HIL token.
3.  **MaxLoops Guardrail:** Prevents infinite looping (EC-009).
4.  **Reflector Verdict:** Processes ACCEPT, RETRY, or ESCALATE.
5.  **Sequential Phase Routing:** Standard fallback (P -> M -> C -> R -> O).

---

## Domain Projection

Each specialized agent provides a `domain_config.json`. The universal engine 
takes the generic phase (e.g., `maker`) and projects it into a domain-specific 
`domain_action` (e.g., `git commit` or `AWS Provisioning`). 

This allows the **Code** to remain identical across the fleet while the 
**Identity** remains unique and data-driven.

---

## Self-Framing (Internal Audit)

Every time an agent is invoked to make a routing decision, it performs a 
"Self-Frame." This is a recursive PMCR-O loop where the agent acts as its 
own orchestrator, logging its internal reasoning to `.pmcro/trails/`. This 
ensures the "Short-Term Memory" of the agent's thought process is preserved.