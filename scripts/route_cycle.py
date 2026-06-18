"""
route_cycle.py — Universal PMCR-O Routing Engine (v4.3.0+)
========================================================
Certified logic with Domain Extension Support.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

DEFAULT_MAP = {
    "planner": "Generate Plan",
    "maker": "Execute Action",
    "checker": "Validate Result",
    "reflector": "Reflect on Loop",
    "hil": "Escalate to Human",
    "closed": "Cycle Complete"
}

def route(payload: Dict[str, Any], governor_verdicts: List[str]) -> Dict[str, Any]:
    domain_map = payload.get("domain_map", DEFAULT_MAP)
    
    frame = {
        "cycle_id": payload.get("cycle_id", f"CycleQ-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),
        "loop": int(payload.get("loop", 1)),
        "o_mode": payload.get("o_mode", "DIRECT"),
        "routed_to": None,
        "domain_action": None,
        "reason": None,
        "hil_required": False,
        "trail_written": False,
        "earned_constraints": payload.get("constraints_active", []),
        "notes": [],
        "cycle_id_self": f"CycleQ-ORCHSTR-{uuid.uuid4().hex[:8].upper()}"
    }

    if "BLOCK" in governor_verdicts or "ESCALATE" in governor_verdicts:
        frame.update({"routed_to": "hil", "hil_required": True, "reason": "ORC-010: Governance block."})
    
    elif payload.get("type1_action_requested") and not _valid_hil_token(payload.get("hil_token")):
        frame.update({"routed_to": "hil", "hil_required": True, "reason": "ORC-018: HIL token missing."})
        
    elif frame["loop"] >= payload.get("max_loops", 3) and payload.get("reflector_verdict") == "RETRY":
        frame.update({"routed_to": "hil", "hil_required": True, "reason": "ORC-007: MaxLoops ceiling."})

    elif payload.get("reflector_verdict") == "ACCEPT":
        frame.update({"routed_to": "closed", "reason": "ORC-022: ACCEPT."})
        
    elif payload.get("reflector_verdict") == "RETRY":
        frame["loop"] += 1
        frame["routed_to"] = "planner"
        frame["o_mode"] = payload.get("suggest_o_mode", "ITERATIVE")
        frame["reason"] = f"ORC-022: RETRY Loop {frame['loop']}."
        
    else:
        phase_map = {"init": "planner", "planner": "maker", "maker": "checker", "checker": "reflector"}
        current = payload.get("current_phase", "init")
        frame["routed_to"] = phase_map.get(current, "hil")
        frame["reason"] = f"ORC-004: Progression from {current}."

    dest = frame["routed_to"]
    frame["domain_action"] = domain_map.get(dest, "Unknown Action")

    return frame

def _valid_hil_token(token: Optional[str]) -> bool:
    return token is not None and len(str(token)) > 8