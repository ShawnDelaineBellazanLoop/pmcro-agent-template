"""
orchestrate.py — Universal Invocation Entry Point (v4.4.1)
=========================================================
Wires route_cycle.py + run_cycle.py. 
Automatically loads domain identity from root domain_config.json.
Compliant with EC-SYS-001 (Atomic File Output).
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Force absolute path resolution for imports
_HERE = Path(__file__).parent.resolve()
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import route_cycle
import run_cycle

def orchestrate(
    payload: Dict[str, Any], 
    governor_verdicts: Optional[List[str]] = None,
    trails_root: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Coordinates a single routing decision, projects it into the 
    domain, and logs the internal cognitive process.
    """
    governor_verdicts = governor_verdicts or []

    # 1. Self-Awareness: Load local domain identity
    if "domain_map" not in payload or payload["domain_map"] is None:
        config_path = _HERE.parent / "domain_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    payload["domain_map"] = config.get("domain_map")
            except Exception as e:
                print(f"Warning: Failed to load domain_config.json: {e}")

    # 2. Execute the Routing Engine
    decision_frame = route_cycle.route(payload, governor_verdicts)

    # 3. Log Self-Frame (The Agent's internal P-M-C-R-O cycle)
    # This records the 'thought process' behind the routing decision.
    cycle = run_cycle.PMCROCycle(
        skill_name="universal-pmcro-agent",
        intent=payload.get("intent", "Routing Dispatch"),
        cycle_id=decision_frame["cycle_id_self"],
        loop=1,
        trails_root=trails_root
    )

    # Internal Loop Phase: OPEN
    cycle.orchestrate_open(
        o_mode="DIRECT", 
        governance_pre_checks=["ORC-010", "ORC-018", "ORC-007"]
    )

    # Internal Loop Phase: PLAN (Minimalist per EC-SYS-002)
    cycle.plan(steps=[
        "Identify local domain context (v4.4.1)",
        "Apply sequential governance logic",
        "Project generic phase to domain action"
    ])

    # Internal Loop Phase: MAKE
    cycle.make(
        action=f"route(payload) -> {decision_frame['routed_to']}",
        result=decision_frame["domain_action"]
    )

    # Internal Loop Phase: CHECK (Structural Integrity per EC-SYS-001)
    valid_destinations = ["planner", "maker", "checker", "reflector", "hil", "closed"]
    passed = decision_frame["routed_to"] in valid_destinations
    cycle.check(
        passed=passed,
        issues=[] if passed else [f"Invalid destination: {decision_frame['routed_to']}"]
    )

    # Internal Loop Phase: REFLECT
    cycle.reflect(
        training_example={"input": payload, "output": decision_frame},
        loop_verdict="ACCEPT"
    )

    # Internal Loop Phase: CLOSE
    cycle.orchestrate_close(
        summary=f"Routed to {decision_frame['routed_to']} ({decision_frame['domain_action']})"
    )

    # Persist the self-trail to .pmcro/trails/
    cycle.write()
    decision_frame["trail_written"] = True
    
    return decision_frame

if __name__ == "__main__":
    # Basic CLI interface for manual routing tests
    if len(sys.argv) < 2:
        print("Usage: python scripts/orchestrate.py <payload.json>")
        sys.exit(1)
    
    payload_path = Path(sys.argv[1])
    if not payload_path.exists():
        print(f"Error: File {payload_path} not found.")
        sys.exit(1)

    with open(payload_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = orchestrate(data)
    print(json.dumps(result, indent=2))