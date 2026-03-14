#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

def gh_error(path: str, message: str) -> None:
    print(f"::error file={path}::{message}")

def infer_type(change: dict) -> str:
    after = change.get("after") or {}
    before = change.get("before") or {}
    for candidate in (
        after.get("type"),
        after.get("resourceType"),
        before.get("type"),
        before.get("resourceType"),
    ):
        if isinstance(candidate, str) and candidate:
            return candidate

    resource_id = change.get("resourceId", "")
    if "/providers/Microsoft.SecurityInsights/alertRules/" in resource_id:
        return "Microsoft.SecurityInsights/alertRules"
    if "/providers/Microsoft.SecurityInsights/automationRules/" in resource_id:
        return "Microsoft.SecurityInsights/automationRules"
    if "/providers/Microsoft.Insights/workbooks/" in resource_id:
        return "Microsoft.Insights/workbooks"
    return "UNKNOWN"

def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: evaluate_whatif.py <lab_dir> <whatif_json> <expected_rg_name>", file=sys.stderr)
        return 2

    repo_root = Path.cwd()
    lab_dir = repo_root / sys.argv[1]
    whatif_path = repo_root / sys.argv[2]
    expected_rg = sys.argv[3]

    manifest = json.loads((lab_dir / "pipeline/manifests/content-manifest.json").read_text(encoding="utf-8"))
    allowed_types = set(manifest["allowed_resource_types"])

    data = json.loads(whatif_path.read_text(encoding="utf-8"))
    changes = data.get("changes", [])

    errors = []
    summary = []

    for change in changes:
        change_type = change.get("changeType", "UNKNOWN")
        resource_id = change.get("resourceId", "")
        rtype = infer_type(change)
        summary.append({
            "changeType": change_type,
            "resourceId": resource_id,
            "resourceType": rtype
        })

        if change_type == "Delete":
            errors.append({"path": str(whatif_path.relative_to(repo_root)), "message": f"Delete detected in what-if for {resource_id}"})

        if rtype not in allowed_types:
            errors.append({"path": str(whatif_path.relative_to(repo_root)), "message": f"Unexpected resource type in what-if: {rtype} ({resource_id})"})

        if expected_rg not in resource_id:
            errors.append({"path": str(whatif_path.relative_to(repo_root)), "message": f"Resource outside expected resource group scope: {resource_id}"})

    report_path = lab_dir / "artifacts/whatif-evaluation.json"
    report_path.write_text(json.dumps({"summary": summary, "errors": errors}, indent=2), encoding="utf-8")

    for err in errors:
        gh_error(err["path"], err["message"])

    if errors:
        return 1

    print(f"[OK] What-if evaluation passed. Report written to {report_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())