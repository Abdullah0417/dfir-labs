# Alert Workflow — GuardDuty to EventBridge to SNS

## Purpose
This workflow turns a GuardDuty finding into an analyst-visible signal.

## Trigger
- GuardDuty native EventBridge finding event
- Severity threshold: high and above

## Event pattern artifact
- `eventbridge_guardduty_high_severity_to_sns.json`

## Target
- SNS topic with email subscription

## What the workflow proves
The alert path proves the finding left the AWS backend services and reached a human-readable destination.

## Validation evidence
- `../../screenshots/04_eventbridge_rule_matched.png`
- `../../screenshots/05_alert_fired.png`

## Why this matters
A finding that never leaves a console view is weak operationally. This workflow proves the lab can move from detection to analyst notification.
