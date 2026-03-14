#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

FORBIDDEN_EXTENSIONS = {
    ".evtx", ".pcap", ".dmp", ".etl", ".pfx", ".pem", ".key", ".p12",
    ".exe", ".dll"
}

REQUIRED_DIRS = [
    "screenshots",
    "kql/validation",
    "kql/hunts",
    "kql/analytics",
    "kql/workbook",
    "detections/docs",
    "detections/exports/analytics",
    "automation/exports",
    "workbooks/exports",
    "notes",
    "mitre",
    "ioc",
    "pipeline/manifests",
    "pipeline/parameters",
    "pipeline/deploy",
    "scripts",
]

REQUIRED_FILES = [
    ".gitignore",
    "notes/lab06-values.env.example",
    "notes/licensing-and-fallback.md",
    "notes/scenario-execution.md",
    "notes/redactions.md",
    "mitre/mitre_mapping.md",
    "ioc/identity_observables.csv",
    "pipeline/manifests/content-manifest.json",
    "pipeline/parameters/test.parameters.json",
    "pipeline/deploy/main.bicep",
    "pipeline/deploy/workbook.serialized.json",
]

ROOT_WORKFLOWS = [
    ".github/workflows/lab06-oidc-smoke-test.yml",
    ".github/workflows/validate-lab06-content.yml",
    ".github/workflows/package-lab06-content.yml",
    ".github/workflows/deploy-lab06-test.yml",
]

def gh_error(path: str, message: str) -> None:
    print(f"::error file={path}::{message}")

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_repo.py <lab_dir>", file=sys.stderr)
        return 2

    repo_root = Path.cwd()
    lab_dir = repo_root / sys.argv[1]
    artifacts_dir = lab_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    errors: list[dict[str, str]] = []

    if not lab_dir.exists():
        errors.append({"path": str(lab_dir), "message": "Lab directory does not exist."})

    for rel in REQUIRED_DIRS:
        path = lab_dir / rel
        if not path.is_dir():
            errors.append({"path": str(path.relative_to(repo_root)), "message": "Required directory is missing."})

    for rel in REQUIRED_FILES:
        path = lab_dir / rel
        if not path.is_file():
            errors.append({"path": str(path.relative_to(repo_root)), "message": "Required file is missing."})

    for rel in ROOT_WORKFLOWS:
        path = repo_root / rel
        if not path.is_file():
            errors.append({"path": rel, "message": "Required workflow file is missing from repo-root .github/workflows."})

    if (lab_dir / ".github" / "workflows").exists():
        errors.append({
            "path": str((lab_dir / ".github" / "workflows").relative_to(repo_root)),
            "message": "Workflow files must not exist inside the lab folder. Use repo-root .github/workflows."
        })

    for path in lab_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            errors.append({
                "path": str(path.relative_to(repo_root)),
                "message": f"Forbidden file extension detected: {path.suffix.lower()}"
            })
        if path.name.endswith(".env") and path.name != "lab06-values.env.example":
            errors.append({
                "path": str(path.relative_to(repo_root)),
                "message": "A live .env file appears tracked. Keep local values untracked."
            })

    screenshots_dir = lab_dir / "screenshots"
    if screenshots_dir.exists():
        for path in screenshots_dir.iterdir():
            if path.is_file() and path.name != path.name.lower():
                errors.append({
                    "path": str(path.relative_to(repo_root)),
                    "message": "Screenshot filenames must be lowercase."
                })

    report = {"errors": errors}
    report_path = artifacts_dir / "validation-repo.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    for err in errors:
        gh_error(err["path"], err["message"])

    if errors:
        print(json.dumps(report, indent=2))
        return 1

    print(f"[OK] Repo validation passed. Report written to {report_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())