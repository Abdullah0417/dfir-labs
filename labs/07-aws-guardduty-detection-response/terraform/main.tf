terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.7"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = var.project_name
      Lab       = "lab-07"
      ManagedBy = "terraform"
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}

locals {
  account_id            = data.aws_caller_identity.current.account_id
  region                = var.aws_region
  partition             = data.aws_partition.current.partition
  bucket_name           = lower("${var.project_name}-${local.account_id}-${local.region}-findings")
  response_lambda_name  = "${var.project_name}-securityhub-response"
  guardduty_product_arn = "arn:${local.partition}:securityhub:${local.region}::product/aws/guardduty"
}

resource "aws_guardduty_detector" "this" {
  enable                       = true
  finding_publishing_frequency = "SIX_HOURS"
}

resource "aws_securityhub_account" "this" {
  enable_default_standards = false
}

resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-guardduty-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

data "aws_iam_policy_document" "sns_topic_policy" {
  statement {
    sid    = "AllowEventBridgePublish"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.alerts.arn]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudwatch_event_rule.guardduty_high.arn]
    }
  }
}

resource "aws_sns_topic_policy" "alerts" {
  arn    = aws_sns_topic.alerts.arn
  policy = data.aws_iam_policy_document.sns_topic_policy.json
}

resource "aws_s3_bucket" "guardduty_findings" {
  bucket        = local.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "guardduty_findings" {
  bucket = aws_s3_bucket.guardduty_findings.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "guardduty_findings" {
  bucket = aws_s3_bucket.guardduty_findings.id

  rule {
    id     = "guardduty-retention"
    status = "Enabled"

    filter {}

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = 90
    }
  }
}

data "aws_iam_policy_document" "kms_key_policy" {
  statement {
    sid    = "AllowRootAccountAdministration"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["arn:${local.partition}:iam::${local.account_id}:root"]
    }

    actions   = ["kms:*"]
    resources = ["*"]
  }

  statement {
    sid    = "AllowGuardDutyKey"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["guardduty.amazonaws.com"]
    }

    actions   = ["kms:GenerateDataKey"]
    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [local.account_id]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [aws_guardduty_detector.this.arn]
    }
  }
}

resource "aws_kms_key" "guardduty_findings" {
  description         = "KMS key for Lab 07 GuardDuty findings export"
  enable_key_rotation = true
  policy              = data.aws_iam_policy_document.kms_key_policy.json
}

resource "aws_kms_alias" "guardduty_findings" {
  name          = "alias/${var.project_name}-guardduty-findings"
  target_key_id = aws_kms_key.guardduty_findings.key_id
}

data "aws_iam_policy_document" "guardduty_bucket_policy" {
  statement {
    sid    = "AllowGetBucketLocation"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["guardduty.amazonaws.com"]
    }

    actions   = ["s3:GetBucketLocation"]
    resources = [aws_s3_bucket.guardduty_findings.arn]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [local.account_id]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [aws_guardduty_detector.this.arn]
    }
  }

  statement {
    sid    = "AllowPutObject"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["guardduty.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.guardduty_findings.arn}/*"]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [local.account_id]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [aws_guardduty_detector.this.arn]
    }
  }

  statement {
    sid    = "DenyUnencryptedObjectUploads"
    effect = "Deny"

    principals {
      type        = "Service"
      identifiers = ["guardduty.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.guardduty_findings.arn}/*"]

    condition {
      test     = "StringNotEquals"
      variable = "s3:x-amz-server-side-encryption"
      values   = ["aws:kms"]
    }
  }

  statement {
    sid    = "DenyIncorrectEncryptionHeader"
    effect = "Deny"

    principals {
      type        = "Service"
      identifiers = ["guardduty.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.guardduty_findings.arn}/*"]

    condition {
      test     = "StringNotEquals"
      variable = "s3:x-amz-server-side-encryption-aws-kms-key-id"
      values   = [aws_kms_key.guardduty_findings.arn]
    }
  }

  statement {
    sid    = "DenyNonHTTPSAccess"
    effect = "Deny"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.guardduty_findings.arn,
      "${aws_s3_bucket.guardduty_findings.arn}/*"
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "guardduty_findings" {
  bucket = aws_s3_bucket.guardduty_findings.id
  policy = data.aws_iam_policy_document.guardduty_bucket_policy.json
}

resource "aws_guardduty_publishing_destination" "this" {
  detector_id     = aws_guardduty_detector.this.id
  destination_arn = aws_s3_bucket.guardduty_findings.arn
  kms_key_arn     = aws_kms_key.guardduty_findings.arn

  depends_on = [
    aws_s3_bucket_policy.guardduty_findings
  ]
}

data "archive_file" "response_zip" {
  type             = "zip"
  source_file      = "${path.module}/../automation/response/lambda_handler.py"
  output_file_mode = "0666"
  output_path      = "${path.module}/lambda_response.zip"
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "${var.project_name}-lambda-exec"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:${local.partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "lambda_securityhub_policy" {
  statement {
    sid       = "AllowBatchUpdateFindings"
    effect    = "Allow"
    actions   = ["securityhub:BatchUpdateFindings"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "lambda_securityhub" {
  name   = "${var.project_name}-lambda-securityhub"
  policy = data.aws_iam_policy_document.lambda_securityhub_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_securityhub" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_securityhub.arn
}

resource "aws_cloudwatch_log_group" "response" {
  name              = "/aws/lambda/${local.response_lambda_name}"
  retention_in_days = 14
}

resource "aws_lambda_function" "response" {
  function_name    = local.response_lambda_name
  role             = aws_iam_role.lambda_exec.arn
  runtime          = "python3.11"
  handler          = "lambda_handler.lambda_handler"
  filename         = data.archive_file.response_zip.output_path
  source_code_hash = data.archive_file.response_zip.output_base64sha256
  timeout          = 30

  depends_on = [
    aws_cloudwatch_log_group.response,
    aws_iam_role_policy_attachment.lambda_logs,
    aws_iam_role_policy_attachment.lambda_securityhub
  ]
}

resource "aws_cloudwatch_event_rule" "guardduty_high" {
  name        = "${var.project_name}-guardduty-high-to-sns"
  description = "Send high-severity GuardDuty findings to SNS email"

  event_pattern = jsonencode({
    source        = ["aws.guardduty"]
    "detail-type" = ["GuardDuty Finding"]
    detail = {
      severity = [
        {
          numeric = [">=", 7]
        }
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "guardduty_to_sns" {
  rule = aws_cloudwatch_event_rule.guardduty_high.name
  arn  = aws_sns_topic.alerts.arn
}

resource "aws_cloudwatch_event_rule" "securityhub_new_high" {
  name        = "${var.project_name}-securityhub-new-high-to-lambda"
  description = "Send new high and critical GuardDuty Security Hub findings to Lambda response"

  event_pattern = jsonencode({
    source        = ["aws.securityhub"]
    "detail-type" = ["Security Hub Findings - Imported"]
    detail = {
      findings = {
        ProductArn = [local.guardduty_product_arn]
        Severity = {
          Label = ["HIGH", "CRITICAL"]
        }
        Workflow = {
          Status = ["NEW"]
        }
        RecordState = ["ACTIVE"]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "securityhub_to_lambda" {
  rule = aws_cloudwatch_event_rule.securityhub_new_high.name
  arn  = aws_lambda_function.response.arn
}

resource "aws_lambda_permission" "allow_eventbridge_to_invoke_response" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.response.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.securityhub_new_high.arn
}
