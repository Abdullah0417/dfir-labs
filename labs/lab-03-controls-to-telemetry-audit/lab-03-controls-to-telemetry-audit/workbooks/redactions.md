# Redactions — Workbook Export JSON

## What was redacted
Workbook exports can include Azure environment identifiers. The following were replaced with placeholders:

- **Subscription ID**  
  `.../subscriptions/<GUID>/...` → `.../subscriptions/<SUBSCRIPTION_ID>/...`

- **Resource group name**  
  `.../resourcegroups/<name>/...` → `.../resourcegroups/<RESOURCE_GROUP>/...`

- **Workspace name / resource ID**  
  `.../workspaces/<name>` → `.../workspaces/<WORKSPACE_NAME>`

**Common fields containing these values:**
- `crossComponentResources[]`
- `fallbackResourceIds[]`
- `context.ownerId`

## What was not redacted
- KQL logic, table names, event IDs
- Lab hostnames (`win-ws1`, `win-ws2`) — lab-only identifiers

## Quick pre-commit check
Search the JSON for any real IDs before pushing:
- `subscriptions/`
- `resourcegroups/`
- `tenant`
- `objectId`
- `userPrincipalName`
- `token` / `secret`