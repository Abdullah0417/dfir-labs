# Service principal credential addition

## Purpose

Detect the addition of a new password credential to a dedicated service principal.

## Telemetry

- Table: `AuditLogs`
- Required fields:
  - `TimeGenerated`
  - `OperationName`
  - `InitiatedBy`
  - `TargetResources`
  - `ResultType`
  - `CorrelationId`
  - `LoggedByService`

## Logic

The rule looks back one hour for the exact credential-addition operation names observed during discovery. It expands `TargetResources` so the alert includes the target application or service principal.

## Thresholds

- Trigger when query result count is greater than 0
- Lookback: 1 hour
- Run frequency: 1 hour

## Entity mapping

- Account:
  - `Name` -> `ActorName`
  - `UPNSuffix` -> `ActorUPNSuffix`

## Observed operation names used

- `Add service principal credentials`
- `Update service principal`

## False positives

- Legitimate secret rotation
- Planned application maintenance
- Test app bootstrap activity

## Validation

1. Add a password credential to the dedicated scenario service principal by using `az ad sp credential reset --append`.
2. Run the discovery hunt and capture the exact operation names.
3. Create the scheduled analytic.
4. Add a second temporary credential or repeat the event.
5. Confirm an incident is created.

## Limitations

This rule is intentionally focused on a dedicated lab service principal so the detection logic can be validated cleanly without polluting the OIDC deployment identity.

## Evidence

- [Service principal credential-addition hunt result](../../screenshots/07_sp_credential_addition_hunt.png)
- [Scheduled analytic configuration](../../screenshots/10_rule_sp_credential_addition.png)
- [Incident triggered from the rule](../../screenshots/11_identity_incident_triggered.png)
