# Redactions (publish-safe)

These artifacts were sanitized before publishing to avoid leaking identifiers.

## What was redacted
- **Automation rule export**: removed the *Assign owner* action because it contained a real user objectId + email.
- **Workbook template**: removed `fallbackResourceIds` because it contained the subscription ID.
- **Incident export CSV**: replaced real email addresses with `redacted@example.com`.

## How to restore owner assignment (optional)
If you want the automation rule to assign an incident owner in your own workspace, add a third action of type **ModifyProperties** with an `owner` object containing your user fields (objectId/email).

Keep the publish version sanitized.
