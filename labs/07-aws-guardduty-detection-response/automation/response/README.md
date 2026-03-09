# Response Workflow — Security Hub to EventBridge to Lambda

## Purpose
This workflow performs an automated first-response action on GuardDuty findings after they are normalized in Security Hub.

## Trigger
- Security Hub imported findings event
- Product: GuardDuty
- Workflow status: `NEW`
- Record state: `ACTIVE`
- Severity: `HIGH` or `CRITICAL`

## Event pattern artifact
- `eventbridge_securityhub_guardduty_new_high_to_lambda.json`

## Target
- Lambda function

## Lambda action
The Lambda function calls `BatchUpdateFindings` to:
- set `Workflow.Status` to `NOTIFIED`
- add a note that records the automated response

Code artifact:
- `lambda_handler.py`

## Constraint, decision, and evidence
Security Hub was enabled after the first sample-finding batch. Because of that timing, the response workflow was validated against a second batch generated after Security Hub was already importing findings.

One finding was also updated manually by CLI so the final `NOTIFIED` state was easy to show in the Security Hub console. That manual step was used for proof presentation, not as a substitute for the Lambda workflow.

## Validation evidence
- `../../screenshots/06_response_executed.png`
- Lambda CloudWatch logs showing successful `workflow_status = NOTIFIED`

## Why `NOTIFIED` was the right response here
These are GuardDuty sample findings, not a real compromised workload. Updating the finding workflow and adding an automation note is an honest first-response action. It proves orchestration without pretending a sample finding justified host containment.

## Operational note
The original logs showed at least one `TooManyRequestsException` from the Security Hub API during burst processing. The successful updates still prove the workflow worked, but retry and backoff should be added before using this pattern in a busier environment.
