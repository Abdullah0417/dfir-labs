output "aws_account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  value = var.aws_region
}

output "guardduty_detector_id" {
  value = aws_guardduty_detector.this.id
}

output "guardduty_detector_arn" {
  value = aws_guardduty_detector.this.arn
}

output "findings_bucket_name" {
  value = aws_s3_bucket.guardduty_findings.bucket
}

output "findings_bucket_arn" {
  value = aws_s3_bucket.guardduty_findings.arn
}

output "kms_key_arn" {
  value = aws_kms_key.guardduty_findings.arn
}

output "sns_topic_arn" {
  value = aws_sns_topic.alerts.arn
}

output "alert_rule_name" {
  value = aws_cloudwatch_event_rule.guardduty_high.name
}

output "response_rule_name" {
  value = aws_cloudwatch_event_rule.securityhub_new_high.name
}

output "response_lambda_name" {
  value = aws_lambda_function.response.function_name
}
