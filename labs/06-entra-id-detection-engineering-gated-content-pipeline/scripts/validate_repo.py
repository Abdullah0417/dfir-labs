#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_repo.py <lab06_dir>", file=sys.stderr)
        return 2

    lab_dir = Path(sys.argv[1]).resolve()
    repo_root = Path.cwd().resolve()

    errors: list[dict[str, str]] = []

    if not lab_dir.exists():
        print(json.dumps({"errors": [{"path": str(lab_dir), "message": "Lab directory does not exist."}]}, indent=2))
        return 1

    # Phase 8 required files only
    required_lab_files = [
        "README.md",
        "executive-summary.md",
        "notes/oidc-setup.md",
        "pipeline/manifests/content-manifest.json",
        "pipeline/deploy/workbook.serialized.json",
        "pipeline/deploy/main.bicep",
        "scripts/validate_repo.py",
        "scripts/validate_deployable_json.py",
        "scripts/validate_detection_metadata.py",
        "scripts/validate_workflow_guardrails.py",
        "scripts/validate_readme_evidence.py",
        "scripts/build_package.py",
        "scripts/evaluate_whatif.py",
    ]

    for rel in required_lab_files:
        p = lab_dir / rel
        if not p.exists():
            errors.append({"path": str(p.relative_to(repo_root)), "message": "Required file is missing."})

    required_workflows = [
        ".github/workflows/lab06-oidc-smoke-test.yml",
        ".github/workflows/validate-lab06-content.yml",
        ".github/workflows/package-lab06-content.yml",
    ]

    for rel in required_workflows:
        p = repo_root / rel
        if not p.exists():
            errors.append({"path": rel, "message": "Required workflow file is missing from repo-root .github/workflows."})

    # Ignore rule can exist in root .gitignore OR lab-local .gitignore
    ignore_target = "notes/lab06-values.env"
    root_gitignore = repo_root / ".gitignore"
    lab_gitignore = lab_dir / ".gitignore"

    root_text = load_text(root_gitignore)
    lab_text = load_text(lab_gitignore)

    root_ok = "labs/06-entra-id-detection-engineering-gated-content-pipeline/notes/lab06-values.env" in root_text
    lab_ok = ignore_target in lab_text or "/notes/lab06-values.env" in lab_text

    if not (root_ok or lab_ok):
        errors.append({
            "path": str((lab_dir / ".gitignore").relative_to(repo_root)),
            "message": "Missing ignore rule for notes/lab06-values.env in root .gitignore or lab-local .gitignore."
        })

    # Enforce lowercase screenshot filenames
    screenshots_dir = lab_dir / "screenshots"
    if screenshots_dir.exists():
        for item in screenshots_dir.iterdir():
            if item.is_file():
                if item.name != item.name.lower():
                    errors.append({
                        "path": str(item.relative_to(repo_root)),
                        "message": "Screenshot filenames must be lowercase."
                    })
    else:
        errors.append({"path": str(screenshots_dir.relative_to(repo_root)), "message": "Screenshots directory is missing."})

    if errors:
        print("Error: Repo validation failed.")
        print(json.dumps({"errors": errors}, indent=2))
        return 1

    print("Repo structure and hygiene validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
