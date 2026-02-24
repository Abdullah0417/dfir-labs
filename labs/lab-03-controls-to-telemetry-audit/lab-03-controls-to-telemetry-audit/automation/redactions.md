## Lab 03 — Automation rule export redactions

Artifact:
- `automation/LAB03_soar_lite_automation_rule.arm.json`

Redactions performed:
- Replaced automation rule GUID in `resources[].id` and `resources[].name` with `00000000-0000-0000-0000-000000000000`
- Replaced referenced analytic rule GUID in `IncidentRelatedAnalyticRuleIds` with `00000000-0000-0000-0000-000000000000`

Notes:
- This export intentionally does **not** assign an owner to avoid leaking user identifiers.
