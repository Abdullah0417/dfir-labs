# Redactions (publish-safe exports)

Goal: keep exports recruiter-usable while avoiding cloud identifiers that shouldn't be published.

## What was redacted
- **Azure subscription GUIDs** were replaced with placeholders in:
  - `workbooks/LAB05_case_view_workbook.json`
  - `automation/LAB05_automation_tag_escalate.json`

## What was *not* redacted (intentionally)
- Hostnames (`win-ws1`, `win-ws2`) and lab resource names (`law-dfir`, `rg-dfir-lab-scus`) were kept because they are generic lab identifiers and help the story stay readable.
- Rule/workbook GUIDs inside templates were kept; they are not privileged secrets on their own.

## How to re-use the artifacts
- Replace `<SUBSCRIPTION_ID>` placeholders with your own subscription ID before importing the workbook template.
