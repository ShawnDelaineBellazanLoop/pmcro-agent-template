"""
orchestrate.py — Universal Invocation Entry Point (v4.4.0)
=========================================================
Wires route_cycle.py + run_cycle.py. 
Automatically loads domain identity from root domain_config.json.
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
    governor_verdicts = governor_verdicts or []

    # NEW: Self-Awareness Logic
    # Load local domain config if domain_map is missing from payload
    if "domain_map" not in payload:
        config_path = _HERE.parent / "domain_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    payload["domain_map"] = config.get("domain_map")
            except Exception as e:
                print(f"Warning: Failed to load domain_config.json: {e}")

    # 1. Execute pure routing
    decision_frame = route_cycle.route(payload, governor_verdicts)

    # 2. Log Self-Frame (Orchestrator's internal cycle)
    cycle = run_cycle.PMCROCycle(
        skill_name="orchestrator-agent",
        intent=payload.get("intent", "Routing Dispatch"),
        cycle_id=decision_frame["cycle_id_self"],
        loop=1,
        trails_root=trails_root
    )

    cycle.orchestrate_open(
        o_mode="DIRECT", 
        governance_pre_checks=["ORC-010", "ORC-018", "ORC-007"]
    )

    cycle.plan(steps=[
        "Load local domain identity (v4.4.0)",
        "Apply C-suite governance pre-checks (ORC-010)",
        "Validate HIL token for TYPE 1 actions (ORC-018)",
        "Verify MaxLoops guardrails (ORC-007)",
        "Project decision into domain vocabulary"
    ])

    cycle.make(
        action=f"route(payload) -> {decision_frame['routed_to']}",
        result=decision_frame["domain_action"]
    )

    valid_destinations = ["planner", "maker", "checker", "reflector", "hil", "closed"]
    passed = decision_frame["routed_to"] in valid_destinations
    cycle.check(
        passed=passed,
        issues=[] if passed else [f"Invalid destination: {decision_frame['routed_to']}"]
    )

    cycle.reflect(
        training_example={"input": payload, "output": decision_frame},
        loop_verdict="ACCEPT"
    )

    cycle.orchestrate_close(
        summary=f"Routed to {decision_frame['routed_to']} ({decision_frame['domain_action']})"
    )

    cycle.write()
    decision_frame["trail_written"] = True
    
    return decision_frame

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/orchestrate.py <payload.json>")
        sys.exit(1)
    
    payload_path = Path(sys.argv[1])
    with open(payload_path, 'r') as f:
        data = json.load(f)
    
    result = orchestrate(data)
    print(json.dumps(result, indent=2))