# Executive Summary — Lab 07 AWS GuardDuty Detection + Response

## Objective
Build and validate an AWS-native detection and response workflow that starts with GuardDuty, preserves findings to S3, supports Athena triage, alerts an analyst through SNS, and performs an automated first-response action through Security Hub, EventBridge, and Lambda.

## What was built
The lab deployed a GuardDuty and Security Hub baseline in `us-east-1` with Terraform. The deployed services included GuardDuty, Security Hub, EventBridge, SNS, Lambda, S3, KMS, and Athena support.

Two workflows were implemented on purpose:
- **Alert path:** GuardDuty to EventBridge to SNS email
- **Response path:** Security Hub imported findings to EventBridge to Lambda to `BatchUpdateFindings`

## What was validated
The uploaded evidence proves the full loop from detection to response:
- GuardDuty sample findings were generated.
- Findings were exported to S3 under the expected GuardDuty path.
- Athena queried the retained findings successfully.
- EventBridge matched GuardDuty events and invoked the SNS target.
- An analyst-facing alert email was received.
- Security Hub findings reached `NOTIFIED` after the Lambda response executed.

## Constraint and handling decision
Security Hub was enabled after the first sample-finding batch. That meant the response workflow could not honestly claim that it processed the first batch through Security Hub.

The lab handled that constraint directly:
- a second sample batch was generated after Security Hub was enabled,
- Lambda execution was verified in CloudWatch logs for that second batch,
- and one finding was manually updated by CLI so the final `NOTIFIED` state was easy to show in the Security Hub console.

That decision keeps the write-up accurate while still proving the response path.

## Operational value
This package shows more than service familiarity. It shows a complete cloud SecOps motion:
- detection from a managed AWS security service,
- normalized case handling through ASFF in Security Hub,
- durable retention for later hunting,
- analyst notification,
- and a small but real automated response action.

## Best evidence to open first
1. `screenshots/06_response_executed.png`
2. `screenshots/05_alert_fired.png`
3. `screenshots/03_athena_query_result.png`

## Recommended next step
The highest-value improvement is to harden the response Lambda with retry and backoff so the workflow remains reliable when GuardDuty generates many findings at once.
