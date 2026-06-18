# PMCR-O Cognitive Terminology
**Version:** 1.0.0

This document defines the fractal structure of the PMCR-O cognitive process. Every agent must adhere to these definitions in their TrailFrames.

---

## 1. The Intent (The Seed)
The **Intent** is the high-level goal provided by a human or a parent agent (e.g., "Commit the auth module"). It is the reason the loop exists.

## 2. The Cycle (The Session)
A **Cycle** is a single unique instance of working on an Intent. 
- **Cycle ID:** A unique string (e.g., `CycleQ-12345`) that persists until the Intent is satisfied or abandoned.
- **Scope:** A Cycle spans from the moment an agent is first triggered until the final `closed` phase.

## 3. The Loop (The Iteration)
A **Loop** is a single "pass" through the cognitive phases within a Cycle.
- **Direct Mode:** Most Cycles have only **Loop 1**.
- **Retry Mode:** If the Reflector issues a `RETRY` verdict, the agent enters **Loop 2**. 
- **Limit:** Governed by `max_loops` (Default: 3).
- **Difference:** A Cycle is the *container*; a Loop is the *attempt*.

## 4. The Phase (The Step)
A **Phase** is a discrete cognitive state within a Loop.
1. **Planner:** Decomposing the intent.
2. **Maker:** Executing the action.
3. **Checker:** Verifying the outcome.
4. **Reflector:** Assessing performance.
5. **Orchestrate:** Transitioning to the next state.

## 5. The Frame (The Record)
A **Frame** is the data structure produced by a Phase. 
- **TrailFrame:** The final JSON object (e.g., `1.json`) that aggregates all Phase results for a specific Loop.
- **Self-Frame:** The internal log created by `orchestrate.py` when an agent "thinks" about its own routing.