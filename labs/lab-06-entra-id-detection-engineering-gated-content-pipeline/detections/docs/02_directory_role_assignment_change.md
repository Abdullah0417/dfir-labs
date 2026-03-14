# LAB06 - Directory role assignment change

## Purpose

Detect Entra directory role assignment or role membership changes that increase cloud privileges.

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

The rule looks back one hour for the exact role-assignment operation names observed during the discovery phase. It expands `TargetResources` so the alert captures the actor and the affected target object.

## Thresholds

- Trigger when query result count is greater than 0
- Lookback: 1 hour
- Run frequency: 1 hour

## Entity mapping

- Account:
  - `Name` -> `ActorName`
  - `UPNSuffix` -> `ActorUPNSuffix`

## Observed operation names used

- `Add member to role`
- `Remove member from role`

## False positives

- Legitimate role administration
- PIM role changes
- Planned administrative maintenance

## Validation

1. Assign `Security Reader` to `lab06-role-target`.

2. Run the discovery query and copy the exact `OperationName` values.

   <a href="./05_role_assignment_hunt.png">
     <img src="./05_role_assignment_hunt.png" alt="Role assignment hunt query results" width="900">
   </a>

3. Create the scheduled analytic with those values.

   <a href="./08_rule_role_assignment_change.png">
     <img src="./08_rule_role_assignment_change.png" alt="Scheduled analytic for directory role assignment change" width="900">
   </a>

4. Remove and re-add the role assignment if needed.

5. Confirm the rule creates an incident.

   <a href="./10_identity_incident_triggered.png">
     <img src="./10_identity_incident_triggered.png" alt="Identity incident triggered from directory role assignment change" width="900">
   </a>

## Limitations

`OperationName` values can differ by portal flow, API path, and tenant behavior. The exact strings in this document must match what was observed in Phase 3.

## Evidence

- <a href="./05_role_assignment_hunt.png">05_role_assignment_hunt.png</a>
- <a href="./08_rule_role_assignment_change.png">08_rule_role_assignment_change.png</a>
- <a href="./10_identity_incident_triggered.png">10_identity_incident_triggered.png</a>
