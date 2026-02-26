# Redactions — detections (LAB04)

## What was exported
- `detections/LAB04_appdata_powershell_persistence_rule.arm.json` is a publish-safe ARM-style template representing the scheduled analytic rule.

## Redactions
- No subscription IDs, tenant IDs, or workspace **resource IDs** are embedded in the export.
  - Workspace is provided as an input parameter (`workspace`).
- The analytic rule resource name uses a deterministic GUID:
  - `guid(parameters('workspace'), 'LAB04_appdata_powershell_persistence')`

## Verification
- Repo-wide scan performed for:
  - `/subscriptions/` paths
  - GUIDs that look like subscription/tenant/object IDs
  - emails / UPNs
