#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

PLACEHOLDER_RE = re.compile(r"<[A-Z0-9_\\-]+>")

def gh_error(path: str, message: str) -> None:
    print(f"::error file={path}::{message}")

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def collect_json_files(base: Path) -> list[Path]:
    return sorted([p for p in base.rglob("*.json") if p.is_file()])

def resource_types_from_template(obj: Any) -> list[str]:
    types: list[str] = []
    if isinstance(obj, dict):
        if "type" in obj and isinstance(obj["type"], str):
            types.append(obj["type"])
        for key in ("resources",):
            if key in obj and isinstance(obj[key], list):
                for item in obj[key]:
                    types.extend(resource_types_from_template(item))
    elif isinstance(obj, list):
        for item in obj:
            types.extend(resource_types_from_template(item))
    return types

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_deployable_json.py <lab_dir>", file=sys.stderr)
        return 2

    repo_root = Path.cwd()
    lab_dir = repo_root / sys.argv[1]
    artifacts_dir = lab_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    manifest_path = lab_dir / "pipeline/manifests/content-manifest.json"
    params_path = lab_dir / "pipeline/parameters/test.parameters.json"
    workbook_serialized_path = lab_dir / "pipeline/deploy/workbook.serialized.json"

    manifest = load_json(manifest_path)
    for key in ["lab", "package_prefix", "allowed_resource_types", "deployable_files", "proof_files", "proof_directories"]:
        if key not in manifest:
            errors.append({"path": str(manifest_path.relative_to(repo_root)), "message": f"Manifest missing key: {key}"})

    for rel in manifest.get("deployable_files", []):
        if not (lab_dir / rel).exists():
            errors.append({"path": str((lab_dir / rel).relative_to(repo_root)), "message": "Manifest references a missing deployable file."})

    for rel in manifest.get("proof_files", []):
        if not (lab_dir / rel).exists():
            errors.append({"path": str((lab_dir / rel).relative_to(repo_root)), "message": "Manifest references a missing proof file."})

    for rel in manifest.get("proof_directories", []):
        if not (lab_dir / rel).is_dir():
            errors.append({"path": str((lab_dir / rel).relative_to(repo_root)), "message": "Manifest references a missing proof directory."})

    params = load_json(params_path)
    values = params.get("parameters", {})
    for key in [
        "roleAssignmentOperation1",
        "roleAssignmentOperation2",
        "servicePrincipalCredentialOperation1",
        "servicePrincipalCredentialOperation2",
    ]:
        value = values.get(key, {}).get("value", "")
        if not value or PLACEHOLDER_RE.search(value):
            errors.append({"path": str(params_path.relative_to(repo_root)), "message": f"Parameter {key} still contains a placeholder or empty value."})

    workbook_serialized = load_json(workbook_serialized_path)
    if workbook_serialized.get("version") != "Notebook/1.0":
        errors.append({"path": str(workbook_serialized_path.relative_to(repo_root)), "message": "Workbook serializedData version must be Notebook/1.0."})
    if not isinstance(workbook_serialized.get("items"), list) or not workbook_serialized["items"]:
        errors.append({"path": str(workbook_serialized_path.relative_to(repo_root)), "message": "Workbook serializedData must contain at least one item."})

    allowed_types = set(manifest.get("allowed_resource_types", []))

    export_dirs = [
        lab_dir / "detections/exports/analytics",
        lab_dir / "automation/exports",
        lab_dir / "workbooks/exports",
    ]

    for export_dir in export_dirs:
        for json_file in collect_json_files(export_dir):
            raw_text = json_file.read_text(encoding="utf-8")
            if PLACEHOLDER_RE.search(raw_text):
                errors.append({"path": str(json_file.relative_to(repo_root)), "message": "Exported JSON still contains unresolved placeholders."})
                continue
            try:
                obj = json.loads(raw_text)
            except json.JSONDecodeError as exc:
                errors.append({"path": str(json_file.relative_to(repo_root)), "message": f"Invalid JSON: {exc}"})
                continue

            types = resource_types_from_template(obj)
            for rtype in types:
                if rtype not in allowed_types and not rtype.startswith("Microsoft.Resources/"):
                    warnings.append({"path": str(json_file.relative_to(repo_root)), "message": f"Unexpected resource type in export: {rtype}"})

    report = {"errors": errors, "warnings": warnings}
    report_path = artifacts_dir / "validation-json.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    for err in errors:
        gh_error(err["path"], err["message"])

    for warn in warnings:
        print(f"::warning file={warn['path']}::{warn['message']}")

    if errors:
        print(json.dumps(report, indent=2))
        return 1

    print(f"[OK] JSON validation passed. Report written to {report_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())