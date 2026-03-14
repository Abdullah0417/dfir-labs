# Lab 06 redaction log

## Purpose

This file records what I reviewed before publishing Lab 06 and what I chose to redact, keep, or leave local.

## Files reviewed

- `detections/exports/analytics/lab06-failed-signin-burst-by-ip.export.json`
- `detections/exports/analytics/lab06-directory-role-assignment-change.export.json`
- `detections/exports/analytics/lab06-service-principal-credential-addition.export.json`
- `automation/exports/lab06-identity-triage-automation.export.json`
- `workbooks/LAB06_identity_dashboard.json`
- supporting markdown notes used to explain the lab

## What I redacted

- personal email addresses and tenant-specific user principal names where they were not required to explain the workflow
- the public source IP used during sign-in testing, because it was incidental lab context rather than a reusable detection artifact
- exact resource identifiers where the full value added no technical value in the public repo
- environment-specific workbook references that were useful for deployment locally but too specific for a recruiter-facing publication

## What I intentionally kept

- rule names and detection descriptions
- `OperationName` values needed to explain detection logic
- MITRE mappings
- rule schedules, thresholds, and entity mappings
- workbook section names and publish-safe query content
- scenario timestamps and sequence details needed to explain how the validation was performed

## Verification notes

- I reviewed the exported analytics and automation content for live secrets, credentials, and user-specific ownership fields.
- I reviewed the workbook export more closely than the other files because ARM-wrapped workbook content can carry workspace-specific references.
- Exact values that mattered only for local deployment were kept in local working files and not relied on for the public write-up.

## Result

The public Lab 06 material keeps the technical story intact without publishing more tenant detail than the repo needs.

