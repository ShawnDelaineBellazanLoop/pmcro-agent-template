"""
route_cycle.py — Universal PMCR-O Routing Engine (v4.4.2)
========================================================
Certified logic with Domain Extension Support.
Compliant with EC-SYS-001 (Atomic File Output).

o_mode    — cognitive technique (OUTPUT/OPTIMIZE/ORCHESTRATE/COT/TOT/GOT/REACT/THOUGHTLOCK)
cycle_policy — loop execution behavior (DIRECT/ITERATIVE/REFLECTIVE/ESCALATION/AUDIT)
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

# Default mapping used if no domain_map is provided in the payload
DEFAULT_MAP = {
    "planner": "Phase: Plan",
    "maker": "Phase: Make",
    "checker": "Phase: Check",
    "reflector": "Phase: Reflect",
    "hil": "Phase: HIL Escalation",
    "closed": "Phase: Cycle Close"
}

def route(payload: Dict[str, Any], governor_verdicts: List[str]) -> Dict[str, Any]:
    """
    Determines the next phase of the PMCR-O loop and projects it
    into the specialized domain vocabulary.
    """
    # 1. Identify Domain Context — "or" catches explicit None values
    domain_map = payload.get("domain_map") or DEFAULT_MAP

    # Initialize the Universal Frame
    frame = {
        "cycle_id": payload.get("cycle_id", f"CycleQ-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),
        "loop": int(payload.get("loop", 1)),
        "o_mode": payload.get("o_mode", "OUTPUT"),
        "cycle_policy": payload.get("cycle_policy", "ITERATIVE"),
        "routed_to": None,
        "domain_action": None,
        "reason": None,
        "hil_required": False,
        "trail_written": False,
        "earned_constraints": payload.get("constraints_active", []),
        "notes": [],
        "cycle_id_self": f"CycleQ-AGENT-{uuid.uuid4().hex[:8].upper()}"
    }

    # 2. Sequential Governance Logic

    # ORC-010: Governance BLOCK/ESCALATE
    if "BLOCK" in governor_verdicts or "ESCALATE" in governor_verdicts:
        frame.update({
            "routed_to": "hil",
            "hil_required": True,
            "reason": "ORC-010: Governance pre-check failure (BLOCK/ESCALATE)."
        })

    # ORC-018: TYPE 1 Authorization
    elif payload.get("type1_action_requested") and not _valid_hil_token(payload.get("hil_token")):
        frame.update({
            "routed_to": "hil",
            "hil_required": True,
            "reason": "ORC-018: TYPE 1 action requested without valid HIL token."
        })

    # ORC-007: MaxLoops Guardrail (EC-009)
    elif frame["loop"] >= payload.get("max_loops", 3) and payload.get("reflector_verdict") == "RETRY":
        frame.update({
            "routed_to": "hil",
            "hil_required": True,
            "reason": "ORC-007: MaxLoops ceiling reached; escalating to HIL."
        })

    # ORC-022: Reflector Verdicts
    elif payload.get("reflector_verdict") == "ACCEPT":
        frame.update({
            "routed_to": "closed",
            "reason": "ORC-022: Reflector issued ACCEPT verdict."
        })

    elif payload.get("reflector_verdict") == "RETRY":
        frame["loop"] += 1
        frame["routed_to"] = "planner"
        # suggest_o_mode governs loop behavior → applied to cycle_policy
        # Field name preserved for backwards compatibility
        frame["cycle_policy"] = payload.get("suggest_o_mode", payload.get("suggest_cycle_policy", "ITERATIVE"))
        frame["reason"] = f"ORC-022: Reflector issued RETRY; entering loop {frame['loop']}."

    else:
        # ORC-004: Standard Phase Sequencing
        phase_map = {
            "init":    "planner",
            "planner": "maker",
            "maker":   "checker",
            "checker": "reflector"
        }
        current = payload.get("current_phase", "init")
        frame["routed_to"] = phase_map.get(current, "hil")
        frame["reason"] = f"ORC-004: Standard progression from {current}."

    # 3. Domain Projection
    dest = frame["routed_to"]
    frame["domain_action"] = domain_map.get(dest, "Unknown Action")

    return frame

def _valid_hil_token(token: Optional[str]) -> bool:
    """Stub for HIL token verification (MAAI-001). Replace with real verifier in production."""
    return token is not None and len(str(token)) > 8
