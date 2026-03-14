# Lab 06 licensing and fallback notes

## Purpose

This note captures whether the authoring workspace had the log sources needed for the planned Entra ID detection content and what the fallback would have been if key data was missing.

## Decision log

- `AuditLogs` available: **Yes**
- `SigninLogs` available: **Yes**
- `AADServicePrincipalSignInLogs` available: **Pending during early validation** and expected to populate after service principal authentication activity

## Outcome

A fallback path was not needed. The required `AuditLogs` and `SigninLogs` data was confirmed in the authoring workspace, so the lab stayed on the intended build path.

## Notes

- Validation date: `2026-03-12`
- Workspace used for validation: `law-dfir-lab06-authoring`
- Supporting screenshots:
  - [AuditLogs validation](../screenshots/02_auditlogs_validation.png)
  - [SigninLogs validation](../screenshots/03_signinlogs_validation.png)
