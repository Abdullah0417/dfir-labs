# Cost Estimate — Lab 07

## Region
- `us-east-1`

## Services enabled
- GuardDuty
- Security Hub
- EventBridge
- SNS
- Lambda
- S3
- Athena
- KMS

## Why each service was in scope
- **GuardDuty:** generated the findings used to drive the lab
- **Security Hub:** centralized GuardDuty findings in ASFF and emitted finding events for the response workflow
- **EventBridge:** routed alert and response events
- **SNS:** delivered the analyst-facing alert email
- **Lambda:** executed the automated first-response update
- **S3:** retained GuardDuty findings beyond the console view
- **Athena:** queried the retained findings for triage
- **KMS:** encrypted the GuardDuty findings export

## Cost guardrails used
- Single AWS account
- Single Region
- No long-running EC2 workload required for the core lab
- Findings bucket lifecycle rule: transition to Standard-IA after 30 days, expire after 90 days
- Athena used only for a small exported findings dataset
- Services were torn down promptly after proof capture

## Start and stop record
- GuardDuty enabled: March 08, 2026, 01:43 (UTC-05:00)
- Security Hub enabled: March 08, 2026, 02:02 (UTC-05:00)
- Athena used: March 08, 2026, 02:00 (UTC-05:00)
- Terraform destroy started: March 09, 2026, 03:35 (UTC-05:00)
- Terraform destroy completed: March 09, 2026, 03:36 (UTC-05:00)
- GuardDuty disabled / detector removed: March 09, 2026, 03:36 (UTC-05:00)
- Security Hub disabled: March 09, 2026, 03:36 (UTC-05:00)

## Destroy result
`Apply complete! Resources: 0 added, 0 changed, 23 destroyed.`

## Notes
- Terraform showed a deprecated attribute warning during destroy tied to `data.aws_region.current.name` in the original code path.
- That warning did not block teardown.
- The SNS subscription endpoint was intentionally omitted from the public package.
