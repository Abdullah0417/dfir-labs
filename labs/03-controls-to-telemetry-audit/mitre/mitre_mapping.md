# MITRE Mapping (Lab 03)

## Detections shipped
### LAB03 - Audit/Log Tampering (4719/1102)
- T1562.002 — Impair Defenses: Disable Windows Event Logging
  - Rationale: audit policy changes (event 4719) can indicate attempts to reduce/disable logging.
- T1070.001 — Indicator Removal: Clear Windows Event Logs
  - Rationale: clearing Security log (event 1102) is a direct anti-forensics behavior.

Evidence:
- Analytic rule mapping screenshot: screenshots/10_analytic_rule_mitre_mapping.png
- Tampering events visible in workbook tile: screenshots/16_workbook_overview_exec.png, 16_workbook_overview.png