"""
log_frame.py — Universal PMCR-O Trail Logger
============================================
CLI utility to record phase transitions into the .pmcro/trails/ memory.
Compliant with EC-SYS-001 (Atomic File Output).
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Log a PMCR-O loop to the trail.")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--intent", required=True)
    parser.add_argument("--cycle_id", required=True)
    parser.add_argument("--loop", type=int, default=1)
    parser.add_argument("--phase", required=True, choices=["open", "plan", "make", "check", "reflect", "close"])
    parser.add_argument("--data", required=True, help="Description of the phase outcome")
    parser.add_argument("--status", default="SUCCESS")

    args = parser.parse_args()

    # Define path: .pmcro/trails/<cycle_id>/<loop>.json
    base_path = Path(".pmcro/trails") / args.cycle_id
    os.makedirs(base_path, exist_ok=True)
    file_path = base_path / f"{args.loop}.json"

    # Initialize or Load Frame
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            frame = json.load(f)
    else:
        frame = {
            "skill": args.skill,
            "cycle_id": args.cycle_id,
            "loop": args.loop,
            "intent": args.intent,
            "timestamp_start": datetime.utcnow().isoformat() + "Z",
            "phases": {}
        }

    # Atomic Phase Update
    frame["phases"][args.phase] = {
        "status": args.status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": args.data
    }

    # Persistence
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(frame, f, indent=2)

    print(f"SEALED: {args.phase} phase recorded in {file_path}")

if __name__ == "__main__":
    main()