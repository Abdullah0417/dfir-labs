# Investigation Timeline — Lab 07

## Sequence
1. **GuardDuty baseline deployed and active**
   - Detector, S3 export, KMS, EventBridge rules, SNS, Lambda, and Security Hub baseline were created with Terraform.

2. **First GuardDuty sample batch generated**
   - GuardDuty findings appeared in the GuardDuty console.
   - Proof: `../screenshots/01_finding_generated.png`

3. **Security Hub timing issue identified**
   - Security Hub was enabled after the first sample batch.
   - That meant the response workflow could not honestly rely on the first batch for Security Hub imported-finding automation.

4. **Second sample batch generated after Security Hub enablement**
   - This batch was used to validate the EventBridge to Lambda response path.

5. **Retention path confirmed**
   - GuardDuty findings were exported to S3 under the GuardDuty prefix.
   - Proof: `../screenshots/02_exported_to_s3.png`
   - Lifecycle proof: `../screenshots/s3_lifecycle_rule.png`

6. **Athena triage completed**
   - The exported dataset was queried successfully.
   - Proof: `../screenshots/03_athena_query_result.png`

7. **Alert path validated**
   - EventBridge matched GuardDuty events and SNS delivered an analyst-facing email.
   - Proof: `../screenshots/04_eventbridge_rule_matched.png`
   - Proof: `../screenshots/05_alert_fired.png`

8. **Response path validated**
   - Lambda updated Security Hub findings to `NOTIFIED`.
   - CloudWatch logs proved successful execution.
   - One finding was also updated manually by CLI so the final `NOTIFIED` state was easy to show in the Security Hub console.
   - Proof: `../screenshots/06_response_executed.png`

9. **Investigation pivots documented**
   - CloudTrail proved the `CreateSampleFindings` API activity.
   - Security Hub JSON view showed the ASFF representation used for response and triage.
   - Proof: `../screenshots/cloudtrail_createSampleFindings.png`
   - Proof: `../screenshots/securityhub_asff_finding_json.png`
