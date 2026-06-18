# PMCR-O Agent Template (v4.4.1)

> The universal cognitive container for specialized PMCR-O agents.

This repository serves as the **Mother Template** for the entire agent ecosystem. It provides the certified routing engine, self-framing infrastructure, and domain projection logic required to build specialized, autonomous agents.

---

## ⚖️ Mandatory System Laws

Every agent spawned from this template must strictly enforce these constraints:

1.  **EC-SYS-001 (Atomic File Protocol):** Agents must always provide the **entire file** content when creating or modifying files. Snippets, partial updates, and "..." markers are strictly prohibited to ensure structural integrity.
2.  **EC-SYS-002 (Minimalist Planning):** The internal Planner phase must produce only the **bare minimum** actionable steps needed for the current loop. Avoid speculative over-planning.

---

## 🛠️ Spawning Protocol (How to Create an Agent)

1.  **Create Repository:** Click the **"Use this template"** button on GitHub.
2.  **Name the Instance:** Name your new repo based on its role (e.g., `jira-agent`, `aws-agent`).
3.  **Localize Identity:**
    -   **`domain_config.json`**: Update the `domain` name and the `domain_map` vocabulary to match the new specialized role.
    -   **`SKILL.md`**: Update the metadata and descriptions to define the agent's specific authorities.
4.  **Certify Engine:** Run the evaluation suite to ensure the inheritance is intact:
    ```powershell
    python scripts/run_evals.py
    ```

---

## 📦 Core Architecture

-   **Routing Engine:** `scripts/route_cycle.py` (Certified Universal Engine v4.3.0+).
-   **Self-Framing:** `scripts/orchestrate.py` + `scripts/run_cycle.py` (Logs internal reasoning to `.pmcro/trails/`).
-   **Projection Logic:** Automatically maps generic P-M-C-R-O phases to specialized domain actions defined in `domain_config.json`.
-   **Validation Suite:** `evals/eval_cases.json` containing 7 canonical governance test cases.

---

## 📜 Domain Parity Mapping

| Phase | Generic | Example (Git-Agent) |
| :--- | :--- | :--- |
| **P** | Planner | `git stage` |
| **M** | Maker | `git commit` |
| **C** | Checker | `git diff/test` |
| **R** | Reflector | `git log review` |
| **O** | Orchestrate | `dispatch` |

**Framework Version:** PMCR-O v1.5.0  
**Logic Version:** v4.4.1 (Atomic & Minimalist)