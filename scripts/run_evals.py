"""
run_evals.py — Orchestrator Evaluation Suite Runner
==================================================
Validates the routing engine against canonical test cases.
"""

import json
import sys
from pathlib import Path

# Setup paths
_HERE = Path(__file__).parent.resolve()
_ROOT = _HERE.parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import route_cycle

def run_suite():
    eval_file = _ROOT / "evals" / "eval_cases.json"
    if not eval_file.exists():
        print(f"Error: Could not find {eval_file}")
        return

    with open(eval_file, 'r') as f:
        suite = json.load(f)

    print(f"--- PMCR-O Eval Suite: {suite['skill']} v{suite['version_tested']} ---")
    
    passed_count = 0
    total_count = len(suite['cases'])

    for case in suite['cases']:
        case_id = case['id']
        desc = case['description']
        payload = case['input']['payload']
        verdicts = case['input']['governor_verdicts']
        expected = case['expected']

        # Execute routing
        result = route_cycle.route(payload, verdicts)

        # Validate against expectations
        mismatches = []
        for key, expected_val in expected.items():
            actual_val = result.get(key)
            if actual_val != expected_val:
                mismatches.append(f"{key}: expected {expected_val}, got {actual_val}")

        if not mismatches:
            print(f"[PASS] {case_id}: {desc}")
            passed_count += 1
        else:
            print(f"[FAIL] {case_id}: {desc}")
            for m in mismatches:
                print(f"       -> {m}")

    print(f"\n--- Result: {passed_count}/{total_count} Passed ---")
    if passed_count == total_count:
        print("STATUS: ORCHESTRATOR CERTIFIED ✅")
    else:
        print("STATUS: FAILURES DETECTED ❌")

if __name__ == "__main__":
    run_suite()