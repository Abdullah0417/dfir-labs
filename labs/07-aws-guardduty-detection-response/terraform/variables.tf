variable "aws_region" {
  description = "AWS Region for Lab 07"
  type        = string
}

variable "project_name" {
  description = "Short project name used for resource naming"
  type        = string
}

variable "alert_email" {
  description = "Email address that will receive SNS alerts"
  type        = string
}
