# Redactions — Lab 04

## Evidence boundary
- Raw evidence and parsed outputs are stored **locally only** under:
  - `C:\Evidence\Cases\2026-02-24_Lab04_WinWS1_EndpointForensics\`
- The GitHub repo contains only publish-safe artifacts:
  - documentation, KQL, templates/exports, screenshots, hashes/manifests

## Items explicitly NOT committed
- Raw EVTX files (Security/System/Application/Sysmon)
- `$MFT` and any KAPE raw output directories
- MFTECmd and EvtxECmd parsed CSV outputs
- Any copied suspicious file samples (only metadata/hashes are published)

## Template hygiene (rules-as-code)
- Analytic rule export/template (sanitized):
  - `detections/LAB04_appdata_powershell_persistence_rule.arm.json`
- Automation rule export/template (sanitized):
  - `automation/LAB04_soar_lite_automation_rule.arm.json`
  - **Owner assignment was removed** from the publishable export to avoid exposing user identifiers.
- Workbook export/template (sanitized):
  - `workbooks/LAB04_workbook_template.json`

## Screenshot hygiene
- Screenshots were reviewed to ensure they do not expose:
  - subscription IDs, tenant IDs, workspace resource IDs
  - user emails / UPNs
  - secrets or tokens
- `screenshots/14_automation_rule.png` was **redacted** to remove a visible owner name/email and the automation rule GUID.
