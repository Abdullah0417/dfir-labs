# Cleanup Log — Lab 07

## Terraform destroy
- Destroy plan created successfully: `lab07-destroy.tfplan`
- Destroy started: March 09, 2026, 03:35 (UTC-05:00)
- Destroy completed: March 09, 2026, 03:36 (UTC-05:00)
- Result: `Apply complete! Resources: 0 added, 0 changed, 23 destroyed.`

## Resources removed
- GuardDuty detector and publishing destination
- Security Hub account enablement
- EventBridge alert and response rules plus targets
- SNS topic, topic policy, and subscription
- Lambda function, permission, and CloudWatch log group
- IAM role, policy, and attachments
- S3 bucket, lifecycle configuration, policy, and public access block
- KMS key and alias

## Manual follow-up
- No manual bucket purge was required because the bucket used `force_destroy = true`.
- No second destroy run was needed.
- Raw console and terminal output that contained the SNS endpoint was left out of the public package.

## Verification
- Final verification performed: March 09, 2026, 03:40 (UTC-05:00)
- Region checked after teardown: `us-east-1`
- Expected outcome confirmed: no Lab 07 resources left running in scope
