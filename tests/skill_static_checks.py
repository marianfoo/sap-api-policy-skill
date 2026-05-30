#!/usr/bin/env python3
"""Static checks for the SAP API Policy evidence skill.

These checks catch contract drift that the first benchmark exposed:
- confidence must be one of high/medium/low, not a range
- evals must exercise the FAQ edge cases and fixed output labels
- Architecture Center AI Golden Path URLs must use the live public path
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "sap-api-policy-evidence"
REFS = SKILL / "references"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise AssertionError(message)


def assert_file(path: Path) -> None:
    if not path.exists():
        fail(f"Missing required file: {path.relative_to(ROOT)}")


def check_skill_structure() -> None:
    assert_file(SKILL / "SKILL.md")
    for name in [
        "policy-baseline.md",
        "evidence-model.md",
        "tool-playbooks.md",
        "report-template.md",
        "inventory-scan-mode.md",
    ]:
        assert_file(REFS / name)
    assert_file(SKILL / "agents" / "openai.yaml")

    skill_text = read(SKILL / "SKILL.md")
    if "name: sap-api-policy-evidence" not in skill_text:
        fail("SKILL.md frontmatter must name sap-api-policy-evidence")
    for ref in [
        "references/policy-baseline.md",
        "references/evidence-model.md",
        "references/tool-playbooks.md",
        "references/report-template.md",
        "references/inventory-scan-mode.md",
    ]:
        if ref not in skill_text:
            fail(f"SKILL.md must link {ref}")


def check_confidence_contract() -> None:
    source_paths = [
        SKILL / "SKILL.md",
        REFS / "evidence-model.md",
        REFS / "report-template.md",
        REFS / "tool-playbooks.md",
        REFS / "policy-baseline.md",
    ]
    banned = re.compile(r"\b(?:medium-to-high|high-to-medium|medium/high|high/medium)\b", re.I)
    for path in source_paths:
        text = read(path)
        match = banned.search(text)
        if match:
            fail(f"Hybrid confidence label found in {path.relative_to(ROOT)}: {match.group(0)}")

    evidence_model = read(REFS / "evidence-model.md")
    if "Use exactly one confidence label: `high`, `medium`, or `low`" not in evidence_model:
        fail("evidence-model.md must explicitly forbid hybrid confidence labels")

    report_template = read(REFS / "report-template.md")
    if "**Confidence:** <high | medium | low>" not in report_template:
        fail("report-template.md must specify fixed confidence labels")

    skill_md = read(SKILL / "SKILL.md")
    if "no\n  trailing words, parentheticals, or qualifiers" not in skill_md and "no trailing words, parentheticals, or qualifiers" not in skill_md:
        fail("SKILL.md must require the Assessment value to be a clean fixed label (no qualifiers)")


def check_policy_url_contract() -> None:
    tool_text = read(REFS / "tool-playbooks.md")
    baseline_text = read(REFS / "policy-baseline.md")
    if "https://architecture.learning.sap.com/docs/ai-golden-path" not in tool_text:
        fail("tool-playbooks.md must prefer the live AI Golden Path URL")
    if "`/docs/aigp` may appear as an alias" not in tool_text:
        fail("tool-playbooks.md must treat /docs/aigp as an alias requiring live verification")
    if "https://architecture.learning.sap.com/docs/ai-golden-path" not in baseline_text:
        fail("policy-baseline.md must mention the current AI Golden Path URL")


def check_eval_contract() -> None:
    data = json.loads(read(ROOT / "evals" / "evals.json"))
    evals = data.get("evals", [])
    names = {item["name"] for item in evals}
    required = {
        "published-api-ipaas-order-sync",
        "odp-rfc-bulk-extraction",
        "agentic-mcp-direct-s4hana",
        "outbound-event-callback",
        "rise-remediation-responsibility",
        "partner-certification-not-enough",
        "binary-answer-refusal",
    }
    missing = required - names
    if missing:
        fail(f"Missing eval scenarios: {sorted(missing)}")

    for item in evals:
        expectations = "\n".join(item.get("expectations", []))
        if "single labeled `Assessment:`" not in expectations:
            fail(f"Eval {item['name']} must require a fixed Assessment label")
        if "single labeled `Confidence:`" not in expectations and item["name"] != "binary-answer-refusal":
            fail(f"Eval {item['name']} must require a fixed Confidence label")
        if item["name"] == "binary-answer-refusal" and "unconditional yes/no" not in expectations:
            fail("binary-answer-refusal must assert refusal of unconditional yes/no")


def main() -> None:
    check_skill_structure()
    check_confidence_contract()
    check_policy_url_contract()
    check_eval_contract()
    print("skill-static-checks-ok")


if __name__ == "__main__":
    main()
