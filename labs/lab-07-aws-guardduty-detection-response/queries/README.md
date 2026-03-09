# Athena Query Pack

This folder contains the SQL used to triage GuardDuty findings exported to S3.

- `00_create_guardduty_table.sql` builds the external table over the GuardDuty export prefix.
- `01_severity_by_day.sql` trends findings by date and severity.
- `02_top_finding_types.sql` surfaces the most common finding types.
- `03_affected_resources.sql` pivots to resources and principals.
- `04_findings_by_account.sql` summarizes findings by account.
