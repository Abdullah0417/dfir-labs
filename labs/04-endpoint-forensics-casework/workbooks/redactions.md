## Workbook export redactions

- Exported workbook as ARM template to: `workbooks/LAB04_workbook_template.json`
- Redacted all Azure resource identifiers from the template:
  - Subscription ID, resource group, workspace name/resource ID
  - Any `/subscriptions/...` paths
- Replaced sensitive values with placeholders (`<SUBSCRIPTION_ID>`, `<RESOURCE_GROUP>`, `<WORKSPACE_NAME>`)

## Verification performed

- Searched the repo for common Azure identifiers and paths:
  - `subscription`, `tenant`, `workspace`, `resourceGroups`, `/subscriptions/`
- Confirmed no raw evidence or parsed outputs are committed:
  - No EVTX, `$MFT`, KAPE output, MFTECmd/EvtxECmd CSVs, or suspicious file samples