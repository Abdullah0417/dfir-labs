#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## What this lab proves",
    "## Telemetry validation",
    "## Scenarios executed",
    "## Detections shipped",
    "## OIDC and gated deployment",
    "## Evidence",
]

REQUIRED_SCREENSHOTS = [
    "01_entra_connector_enabled.png",
    "02_auditlogs_validation.png",
    "04_failed_signin_burst_hunt.png",
    "05_role_assignment_hunt.png",
    "06_sp_credential_addition_hunt.png",
    "07_rule_failed_signin_burst.png",
    "08_rule_role_assignment_change.png",
    "09_rule_sp_credential_addition.png",
    "10_identity_incident_triggered.png",
    "11_automation_rule_identity_triage.png",
    "12_workbook_identity_dashboard.png",
    "13_pr_validation_checks.png",
    "14_environment_approval_gate.png",
    "15_arm_whatif_output.png",
    "16_test_workspace_deploy_success.png",
    "17_test_workspace_content_inventory.png",
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)")

def gh_error(path: str, message: str) -> None:
    print(f"::error file={path}::{message}")

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_readme_evidence.py <lab_dir>", file=sys.stderr)
        return 2

    repo_root = Path.cwd()
    lab_dir = repo_root / sys.argv[1]
    artifacts_dir = lab_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    errors = []

    readme_path = lab_dir / "README.md"
    exec_summary_path = lab_dir / "executive-summary.md"

    if not readme_path.exists():
        errors.append({"path": str(readme_path.relative_to(repo_root)), "message": "README.md is missing."})
    else:
        readme_text = readme_path.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in readme_text:
                errors.append({"path": str(readme_path.relative_to(repo_root)), "message": f"README is missing heading: {heading}"})

        for match in LINK_RE.finditer(readme_text):
            rel = match.group(1) or match.group(2)
            if rel.startswith("http"):
                continue
            target = (lab_dir / rel).resolve()
            if not target.exists():
                errors.append({"path": str(readme_path.relative_to(repo_root)), "message": f"Broken README link: {rel}"})

    if not exec_summary_path.exists():
        errors.append({"path": str(exec_summary_path.relative_to(repo_root)), "message": "executive-summary.md is missing."})

    screenshots_dir = lab_dir / "screenshots"
    for shot in REQUIRED_SCREENSHOTS:
        if not (screenshots_dir / shot).exists():
            errors.append({"path": str((screenshots_dir / shot).relative_to(repo_root)), "message": "Required screenshot is missing."})

    report_path = artifacts_dir / "validation-readme-evidence.json"
    report_path.write_text(json.dumps({"errors": errors}, indent=2), encoding="utf-8")

    for err in errors:
        gh_error(err["path"], err["message"])

    if errors:
        return 1

    print(f"[OK] README evidence validation passed. Report written to {report_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())