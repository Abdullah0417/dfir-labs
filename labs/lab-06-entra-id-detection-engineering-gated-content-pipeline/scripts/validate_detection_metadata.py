#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Purpose",
    "## Telemetry",
    "## Logic",
    "## Thresholds",
    "## Entity mapping",
    "## False positives",
    "## Validation",
    "## Limitations",
    "## Evidence",
]

ALLOWED_PLACEHOLDERS = {
    "<ROLE_ASSIGNMENT_OPERATION_1>",
    "<ROLE_ASSIGNMENT_OPERATION_2>",
    "<SP_CREDENTIAL_OPERATION_1>",
    "<SP_CREDENTIAL_OPERATION_2>",
}

PLACEHOLDER_RE = re.compile(r"<[A-Z0-9_\\-]+>")

def gh_error(path: str, message: str) -> None:
    print(f"::error file={path}::{message}")

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_detection_metadata.py <lab_dir>", file=sys.stderr)
        return 2

    repo_root = Path.cwd()
    lab_dir = repo_root / sys.argv[1]
    artifacts_dir = lab_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    errors = []

    mapping = {
        "failed_signin_burst_by_ip.kql": "01_failed_signin_burst_by_ip.md",
        "directory_role_assignment_change.kql": "02_directory_role_assignment_change.md",
        "service_principal_credential_addition.kql": "03_service_principal_credential_addition.md",
    }

    for kql_name, doc_name in mapping.items():
        kql_path = lab_dir / "kql/analytics" / kql_name
        doc_path = lab_dir / "detections/docs" / doc_name

        if not kql_path.exists():
            errors.append({"path": str(kql_path.relative_to(repo_root)), "message": "Missing analytics KQL file."})
            continue
        if not doc_path.exists():
            errors.append({"path": str(doc_path.relative_to(repo_root)), "message": "Missing detection documentation file."})
            continue

        kql_text = kql_path.read_text(encoding="utf-8")
        if "TimeGenerated" not in kql_text:
            errors.append({"path": str(kql_path.relative_to(repo_root)), "message": "Scheduled analytic KQL must return TimeGenerated."})

        placeholders = set(PLACEHOLDER_RE.findall(kql_text))
        unexpected = placeholders - ALLOWED_PLACEHOLDERS
        if unexpected:
            errors.append({"path": str(kql_path.relative_to(repo_root)), "message": f"Unexpected placeholders in KQL: {sorted(unexpected)}"})

        doc_text = doc_path.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in doc_text:
                errors.append({"path": str(doc_path.relative_to(repo_root)), "message": f"Missing required heading: {heading}"})

    mitre_path = lab_dir / "mitre/mitre_mapping.md"
    if not mitre_path.exists():
        errors.append({"path": str(mitre_path.relative_to(repo_root)), "message": "MITRE mapping file is missing."})
    else:
        mitre_text = mitre_path.read_text(encoding="utf-8")
        for phrase in [
            "Failed sign-in burst by IP",
            "Directory role assignment change",
            "Service principal credential addition",
        ]:
            if phrase not in mitre_text:
                errors.append({"path": str(mitre_path.relative_to(repo_root)), "message": f"MITRE mapping missing phrase: {phrase}"})

    report_path = artifacts_dir / "validation-detection-metadata.json"
    report_path.write_text(json.dumps({"errors": errors}, indent=2), encoding="utf-8")

    for err in errors:
        gh_error(err["path"], err["message"])

    if errors:
        return 1

    print(f"[OK] Detection metadata validation passed. Report written to {report_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())