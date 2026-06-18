# PMCR-O Agent Template (v4.4.0)

> Canonical Blueprint for specialized cognitive agents.

## How to use this Template
1. Click **"Use this template"** on GitHub.
2. Name your new repository (e.g., `jira-agent`, `maker-agent`).
3. **Localize Identity:**
   - Edit `domain_config.json`: Set the `domain` name and the `domain_map` vocabulary.
   - Edit `SKILL.md`: Replace `{{AGENT_NAME}}` and placeholders with your agent's specifics.
4. **Initialize:** Run `python scripts/orchestrate.py assets/request_template.json` to verify the new identity.

## Included Core
- **Universal Engine:** `scripts/route_cycle.py` (Certified v4.4.0).
- **Self-Framing:** `scripts/orchestrate.py` + `scripts/run_cycle.py`.
- **Validation:** `evals/eval_cases.json` for engine certification.