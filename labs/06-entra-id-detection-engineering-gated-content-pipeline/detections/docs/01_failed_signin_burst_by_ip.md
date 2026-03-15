# Failed sign-in burst by IP

## Purpose

Detect repeated failed interactive Entra sign-ins from one source IP across multiple users inside a short time window.

## Telemetry

- Table: `SigninLogs`
- Required fields:
  - `TimeGenerated`
  - `IPAddress`
  - `UserPrincipalName`
  - `ResultType`
  - `ResultDescription`
  - `AppDisplayName`

## Logic

The rule looks back 15 minutes for interactive sign-in failures, groups the results by source IP, and triggers when one IP generated at least five failed sign-ins across at least three distinct users.

## Thresholds

- Minimum failures: 5
- Minimum distinct users: 3
- Lookback: 15 minutes
- Run frequency: 15 minutes

## Entity mapping

- Account:
  - `Name` -> `FirstUserName`
  - `UPNSuffix` -> `FirstUserUPNSuffix`
- IP:
  - `Address` -> `IPAddress`

## False positives

- Shared VPN egress
- Shared NAT
- Bulk testing by administrators
- Password manager retry noise

## Validation

1. Trigger failed sign-ins against three lab users from one IP.
2. Run the hunt query first.
3. Confirm one result row is returned.
4. Create the scheduled analytic.
5. Re-run the sign-in burst.
6. Confirm an incident is created.

## Limitations

This rule depends on `SigninLogs`. If `SigninLogs` is not licensed or not flowing, this rule should not be claimed as implemented.

## Evidence

- [Failed sign-in burst hunt result](../../screenshots/04_failed_signin_burst_hunt.png)
- [Scheduled analytic configuration](../../screenshots/08_rule_failed_signin_burst.png)
- [Incident triggered from the rule](../../screenshots/11_identity_incident_triggered.png)
