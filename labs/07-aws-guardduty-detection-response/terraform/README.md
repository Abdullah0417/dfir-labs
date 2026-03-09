# Terraform — Lab 07 AWS GuardDuty Detection + Response

## What Terraform deploys
Terraform handles the AWS infrastructure baseline for the lab:
- GuardDuty detector
- Security Hub enablement
- S3 findings bucket
- S3 lifecycle rule
- KMS key and alias for GuardDuty export
- GuardDuty publishing destination
- SNS topic and email subscription
- EventBridge alert rule and target
- EventBridge response rule and target
- Lambda response function
- IAM role and policy attachments for Lambda execution

## What stayed manual
These steps stayed manual on purpose:
- generating GuardDuty sample findings
- confirming the SNS subscription
- reviewing Security Hub and GuardDuty console views
- running Athena queries
- capturing screenshots
- documenting the timing constraint and the manual CLI proof step

## Included files
- `main.tf`
- `variables.tf`
- `outputs.tf`
- `terraform.tfvars.example`

## Variables
- `aws_region`
- `project_name`
- `alert_email`

## Example tfvars
Create a local-only `terraform.tfvars` file from `terraform.tfvars.example` and keep the real file out of Git.

## Typical run sequence
```powershell
terraform init
terraform fmt
terraform validate
terraform plan -out lab07.tfplan
terraform apply lab07.tfplan
terraform output
```

## Destroy sequence
```powershell
terraform plan -destroy -out lab07-destroy.tfplan
terraform apply lab07-destroy.tfplan
```

## Publish-safe handling
Do not commit any of the following if they are generated locally:
- `terraform.tfvars`
- `*.tfstate*`
- `*.tfplan`
- `filters.json`
- `update.json`
- `lambda_response.zip`
