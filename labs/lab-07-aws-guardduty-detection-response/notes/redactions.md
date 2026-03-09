# Redactions and Publish-Safe Handling — Lab 07

## Redactions applied in the recruiter package
- AWS console top-right identity banner was masked where it exposed the operator name.
- The CloudTrail proof screenshot was masked where it exposed the AWS access key value.
- Personal email destination details were kept out of the package.

## What stayed visible on purpose
- Service names
- Finding titles and severities
- Region
- Workflow state `NOTIFIED`
- S3 export path structure
- Athena query text and result set
- EventBridge rule names and monitoring state
- GuardDuty, Security Hub, and ASFF context needed to understand the workflow

## Files explicitly excluded from the final package
- `terraform/terraform.tfvars`
- `terraform/terraform.tfstate`
- `terraform/terraform.tfstate.backup`
- `terraform/lab07.tfplan`
- `terraform/lab07-destroy.tfplan`
- `terraform/filters.json`
- `terraform/update.json`
- generated Lambda zip artifacts if created locally
- raw finding JSON files outside the screenshots

## Rule followed
Raw evidence remains local only. The recruiter-facing package contains sanitized screenshots, Markdown write-ups, SQL, JSON workflow patterns, Terraform source, and a sanitized IOC pack.
