# Redactions — automation (LAB04)

## What was exported
- `automation/LAB04_soar_lite_automation_rule.arm.json` is a publish-safe ARM-style export representing the automation rule.

## Hygiene / redactions
- **Owner assignment removed** (public-safe). The automation rule only:
  - adds a `lab04` tag
  - sets incident severity to `High`
- No subscription IDs / tenant IDs / user emails are embedded.
- The automation rule resource name uses a deterministic GUID:
  - `guid(parameters('workspace'), 'LAB04_soar_lite_automation_rule')`
