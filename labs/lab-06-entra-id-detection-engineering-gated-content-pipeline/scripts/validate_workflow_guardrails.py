#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

def gh_error(path: str, message: str) -> None:
    print(f"::error file={path}::{message}")

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_workflow_guardrails.py <lab_dir>", file=sys.stderr)
        return 2

    repo_root = Path.cwd()
    lab_dir = repo_root / sys.argv[1]
    artifacts_dir = lab_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    errors = []

    workflow_paths = {
        "smoke": repo_root / ".github/workflows/lab06-oidc-smoke-test.yml",
        "validate": repo_root / ".github/workflows/validate-lab06-content.yml",
        "package": repo_root / ".github/workflows/package-lab06-content.yml",
        "deploy": repo_root / ".github/workflows/deploy-lab06-test.yml",
    }

    loaded = {}
    for name, path in workflow_paths.items():
        if not path.exists():
            errors.append({"path": str(path.relative_to(repo_root)), "message": "Workflow file missing."})
            continue
        loaded[name] = yaml.safe_load(path.read_text(encoding="utf-8"))
        raw_text = path.read_text(encoding="utf-8")
        if "AZURE_CLIENT_SECRET" in raw_text:
            errors.append({"path": str(path.relative_to(repo_root)), "message": "Workflow must not use AZURE_CLIENT_SECRET."})

    smoke = loaded.get("smoke")
    deploy = loaded.get("deploy")
    validate = loaded.get("validate")
    package = loaded.get("package")

    if smoke:
        perms = smoke.get("permissions", {})
        if perms.get("id-token") != "write":
            errors.append({"path": ".github/workflows/lab06-oidc-smoke-test.yml", "message": "Smoke-test workflow must request id-token: write."})
        if smoke.get("jobs", {}).get("smoke-test", {}).get("environment") != "sentinel-test":
            errors.append({"path": ".github/workflows/lab06-oidc-smoke-test.yml", "message": "Smoke-test workflow must use environment sentinel-test."})

    if deploy:
        perms = deploy.get("permissions", {})
        if perms.get("id-token") != "write":
            errors.append({"path": ".github/workflows/deploy-lab06-test.yml", "message": "Deploy workflow must request id-token: write."})
        if deploy.get("jobs", {}).get("deploy", {}).get("environment") != "sentinel-test":
            errors.append({"path": ".github/workflows/deploy-lab06-test.yml", "message": "Deploy workflow must use environment sentinel-test."})
        raw = (repo_root / ".github/workflows/deploy-lab06-test.yml").read_text(encoding="utf-8")
        for required_snippet in [
            "azure/login@v2",
            "az deployment group what-if",
            "az deployment group create",
            "actions/upload-artifact@v4",
        ]:
            if required_snippet not in raw:
                errors.append({"path": ".github/workflows/deploy-lab06-test.yml", "message": f"Deploy workflow missing required step text: {required_snippet}"})

    if validate:
        raw = (repo_root / ".github/workflows/validate-lab06-content.yml").read_text(encoding="utf-8")
        for required_snippet in [
            "validate_repo.py",
            "validate_deployable_json.py",
            "validate_detection_metadata.py",
            "validate_workflow_guardrails.py",
            "validate_readme_evidence.py",
        ]:
            if required_snippet not in raw:
                errors.append({"path": ".github/workflows/validate-lab06-content.yml", "message": f"Validation workflow missing required validator: {required_snippet}"})

    if package:
        raw = (repo_root / ".github/workflows/package-lab06-content.yml").read_text(encoding="utf-8")
        if "build_package.py" not in raw:
            errors.append({"path": ".github/workflows/package-lab06-content.yml", "message": "Package workflow must run build_package.py."})

    report_path = artifacts_dir / "validation-workflow-guardrails.json"
    report_path.write_text(json.dumps({"errors": errors}, indent=2), encoding="utf-8")

    for err in errors:
        gh_error(err["path"], err["message"])

    if errors:
        return 1

    print(f"[OK] Workflow guardrail validation passed. Report written to {report_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())