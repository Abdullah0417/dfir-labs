# AWS Case View — GuardDuty, Security Hub, Athena, and Response State

## Purpose
This document is the AWS-native equivalent of a case-view workbook for Lab 07. It gives a reviewer the shortest path through the evidence.

## Fastest review path
1. Open `../screenshots/06_response_executed.png` to see the final `NOTIFIED` state.
2. Open `../screenshots/05_alert_fired.png` to see the analyst-facing SNS alert.
3. Open `../screenshots/03_athena_query_result.png` to see that the retained findings were queryable.

## Full pivot path
### 1. Start in GuardDuty
Confirm sample findings exist and identify the featured GuardDuty finding.
- Evidence: `../screenshots/01_finding_generated.png`

### 2. Confirm retention
Open the S3 findings bucket and verify GuardDuty objects exist under the export path.
- Evidence: `../screenshots/02_exported_to_s3.png`
- Lifecycle proof: `../screenshots/s3_lifecycle_rule.png`

### 3. Query the retained findings
Use Athena to prove the retained findings are huntable.
- Evidence: `../screenshots/03_athena_query_result.png`
- Query pack: `../queries/`

### 4. Validate the alert path
Review the EventBridge rule monitoring and the SNS email.
- Evidence: `../screenshots/04_eventbridge_rule_matched.png`
- Evidence: `../screenshots/05_alert_fired.png`

### 5. Pivot into Security Hub
Open the Security Hub finding and the JSON/details view to confirm ASFF structure.
- Evidence: `../screenshots/securityhub_asff_finding_json.png`

### 6. Confirm the response state
Review the Security Hub findings table and verify `Workflow status = NOTIFIED`.
- Evidence: `../screenshots/06_response_executed.png`

### 7. Validate the API-side timeline
Use CloudTrail to confirm the `CreateSampleFindings` activity.
- Evidence: `../screenshots/cloudtrail_createSampleFindings.png`

## Important lab note
Security Hub was enabled after the first sample batch. The response workflow was therefore validated against a second batch generated after Security Hub was already importing findings. One finding was manually updated by CLI to make the final `NOTIFIED` console proof easy to read.
