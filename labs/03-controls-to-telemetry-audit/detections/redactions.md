# Redactions

This file documents what was removed or replaced from exported Sentinel artifacts before committing to GitHub.

## Lab 03 — Analytic Rule Export (Rules-as-Code)

**Artifact**
- `detections/LAB03_audit_log_tampering_rule.arm.json`

**Source**
- Exported from Microsoft Sentinel → Analytics → (selected rule) → Export / Export to ARM template.

**Redactions performed**
- Replaced the exported analytic rule GUID in the ARM resource path with the placeholder GUID:
  - `/alertRules/<GUID>` → `/alertRules/00000000-0000-0000-0000-000000000000`
- Same replacement applied in both ARM fields:
  - `resources[].id`
  - `resources[].name`

**Items reviewed (none found in this export)**
- `subscriptions/<id>`
- `resourceGroups/<name>`
- `tenantId` / `objectId` / `principalId`
- `userPrincipalName` / emails

**Notes**
- Query content, scheduling, MITRE mappings, and custom details were left unchanged.
