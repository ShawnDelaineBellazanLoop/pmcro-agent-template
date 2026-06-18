"""
run_cycle.py — PMCR-O Lifecycle Utility
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

class PMCROCycle:
    def __init__(
        self, 
        skill_name: str, 
        intent: str, 
        cycle_id: Optional[str] = None, 
        loop: int = 1,
        trails_root: Optional[Path] = None
    ):
        self.skill_name = skill_name
        self.intent = intent
        self.cycle_id = cycle_id or f"CycleQ-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.loop = loop
        
        if trails_root:
            self.base_path = Path(trails_root) / self.cycle_id
        else:
            self.base_path = Path(".pmcro/trails") / self.cycle_id
            
        self.frame: Dict[str, Any] = {
            "skill": self.skill_name,
            "cycle_id": self.cycle_id,
            "loop": self.loop,
            "intent": self.intent,
            "phases": {}
        }

    def orchestrate_open(self, o_mode: str, governance_pre_checks: List[str]):
        self.frame["o_mode"] = o_mode
        self.frame["phases"]["orchestrate_open"] = {
            "status": "SUCCESS",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "governance_applied": governance_pre_checks
        }

    def plan(self, steps: List[str]):
        self.frame["phases"]["planner"] = { "status": "SUCCESS", "steps": steps }

    def make(self, action: str, result: Any):
        self.frame["phases"]["maker"] = { "status": "SUCCESS", "action": action, "result": result }

    def check(self, passed: bool, issues: List[str]):
        self.frame["phases"]["checker"] = { "status": "SUCCESS" if passed else "FAILED", "passed": passed, "issues": issues }

    def reflect(self, training_example: Dict[str, Any], loop_verdict: str, earned_constraints: List[str] = None):
        self.frame["phases"]["reflector"] = {
            "status": "SUCCESS",
            "verdict": loop_verdict,
            "training_data": training_example,
            "earned_constraints": earned_constraints or []
        }

    def orchestrate_close(self, summary: str):
        self.frame["phases"]["orchestrate_close"] = {
            "status": "SUCCESS",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": summary
        }

    def write(self) -> Path:
        os.makedirs(self.base_path, exist_ok=True)
        file_path = self.base_path / f"{self.loop}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.frame, f, indent=2)
        return file_path