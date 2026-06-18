# Orchestrator Design Notes
**Version:** 4.1.0

Extended guidance for `orchestrator-agent` beyond the SKILL.md quick
reference. Covers the O-Mode system spec, the HIL authorization protocol,
the TrailFrame schema, and MaxLoops policy. Full specs for OMode and Trail
systems live in `.pmcro/docs/OMODE_SYSTEM_SPEC.md` and
`.pmcro/docs/TRAIL_SYSTEM_SPEC.md` — this file is the orchestrator-specific
operational view of those specs, not a duplicate of them.

---

## Routing Precedence Order

`route_cycle.py` checks conditions in a fixed order, and that order is load
-bearing — each check can only run if every earlier one passed:

```
1. Governance pre-check (ORC-010)        — any BLOCK/ESCALATE wins immediately
2. TYPE 1 authorization (ORC-018)         — missing/invalid token wins next
3. MaxLoops guardrail (ORC-007)            — loop ceiling beats a fresh RETRY
4. Reflector verdict (ACCEPT/ESCALATE/RETRY)
5. Sequential phase routing (ORC-001/004) — fallback for in-progress cycles
```

The reasoning for this order: governance and authorization are
preconditions for the cycle continuing to exist at all, so they have to be
checked before anything about *where* to route. MaxLoops is checked before
the Reflector's own RETRY request because a Reflector that says "RETRY" on
loop 3 of 3 doesn't get to override the ceiling it doesn't know about —
the Orchestrator, not the Reflector, owns enforcement of EC-009.

---

## O-Mode System Spec (Operational View)

The full mode definitions are in `pmcro-framework/SKILL.md`'s O-Mode
Registry. Operationally, `route_cycle.py` only actively *selects* a mode in
two situations:

- **Cycle open** (`current_phase == "init"`): defaults to `DIRECT` unless
  the payload already specifies one (e.g. the caller pre-classified the
  intent as complex and set `o_mode: "REFLECTIVE"` before the first route
  call).
- **RETRY routing** (ORC-022): if the Reflector attached a
  `suggest_o_mode`, that value is honored verbatim for the next iteration;
  otherwise the Orchestrator defaults retries to `ITERATIVE`.

All other transitions (`maker → checker`, `checker → reflector`) inherit
whatever `o_mode` was already active for the cycle — the Orchestrator
doesn't re-decide mode at every phase boundary, only at cycle open and at
RETRY.

**Worked example** (self-referential): the cycle that built this very file
opened with `o_mode: DIRECT` because the intent — "write
orchestrator-design.md" — was a single bounded write with no expected
retry. Had the Checker found the file missing required sections and the
Reflector issued RETRY with `suggest_o_mode: REFLECTIVE`, the next loop
would have run in REFLECTIVE mode specifically so the re-planning step
could reason more carefully about what was missing, rather than blindly
re-attempting the same write.

---

## HIL Authorization Protocol (ORC-018)

`route_cycle.py`'s `_valid_hil_token()` is a **structural stub**, not the
real MAAI-001 check. The real protocol — implemented by whatever issues
tokens, not by this routing script — requires all five of:

1. Token present (non-null)
2. Token's `cycle_id` matches the current cycle
3. Token's hash matches the exact `approved_tool` + parameters
4. Token not expired (5-minute window, MAAI-003)
5. Valid HMAC-SHA256 signature

This script only checks presence and a loose string match, because full
cryptographic verification depends on a token-issuing service this
repository doesn't yet implement. Anyone wiring `route_cycle.py` into a
real execution path **must** replace `_valid_hil_token()` with a call to
the actual token verifier before TYPE 1 dispatch is permitted in
production — the stub exists only so eval cases can exercise the routing
logic without a live token service.

---

## TrailFrame Writing Discipline

Per EC-002 and EC-010, the Orchestrator is the *only* writer of
TrailFrames, and it writes them *before* routing to the next phase, not
after. `route_cycle.py` itself does not call `trail.append` — it's a pure
decision function. The live Orchestrator process is expected to:

```
decision = route(payload, governor_verdicts)
trail.append(build_trailframe_from(decision))   # EC-010: seal before routing
dispatch_to(decision["routed_to"])
```

Keeping `route_cycle.py` side-effect-free (no trail writes, no TYPE 1
dispatch) means it can be unit-tested and eval-cased without touching
`.pmcro/trails/` at all — see `evals/eval_cases.json`.

---

## MaxLoops Policy (ORC-007 / EC-009)

`max_loops` defaults to 3 and the framework hard-caps it at 10
(`pmcro-framework/references/colony-laws.md`, EC-009). `route_cycle.py`
checks `loop >= max_loops` rather than `loop > max_loops` — meaning the
Nth loop (where N == max_loops) is the last one allowed to attempt a RETRY
response from the Reflector; if the Reflector still says RETRY on that
exact loop, the Orchestrator escalates instead of allowing a loop+1 that
would exceed the budget.

---

## Eval Case Design Notes

See `evals/eval_cases.json`. Cases route framework-internal intents
(version bumps, skill builds) through every branch of the precedence order
above, rather than routing a downstream domain task.
