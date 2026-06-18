"""
run_evals.py — Engine Certification Runner (v4.4.1)
==================================================
Validates the universal routing engine against canonical test cases.
Compliant with EC-SYS-001 (Atomic File Output).
"""

import json
import sys
from pathlib import Path

# Setup absolute path resolution for imports
_HERE = Path(__file__).parent.resolve()
_ROOT = _HERE.parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import route_cycle

def run_suite():
    """
    Executes all test cases in evals/eval_cases.json and reports results.
    """
    eval_file = _ROOT / "evals" / "eval_cases.json"
    if not eval_file.exists():
        print(f"Error: Certification file not found at {eval_file}")
        return

    with open(eval_file, 'r', encoding='utf-8') as f:
        suite = json.load(f)

    print(f"--- PMCR-O Certification Suite: {suite['skill']} v{suite['version_tested']} ---")
    
    passed_count = 0
    cases = suite.get('cases', [])
    total_count = len(cases)

    for case in cases:
        case_id = case['id']
        desc = case['description']
        payload = case['input']['payload']
        verdicts = case['input'].get('governor_verdicts', [])
        expected = case['expected']

        # Execute routing via the universal engine
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
        print("STATUS: CORE LOGIC CERTIFIED ✅")
        sys.exit(0)
    else:
        print("STATUS: CERTIFICATION FAILED ❌")
        sys.exit(1)

if __name__ == "__main__":
    run_suite()