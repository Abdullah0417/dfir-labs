# scenario execution log

This file records the UTC windows used for each scenario, along with the specific validation notes that mattered during hunting and rule testing. It serves as the public source of truth for the hunt windows and screenshot timing.

## Scenario 1 — Failed sign-in burst from one IP across multiple users

- Start UTC: 2026-03-12T20:37:38Z
- End UTC: 2026-03-12T20:39:08Z
- Users: `lab06-user-a@tenant.onmicrosoft.com`, `lab06-user-b@tenant.onmicrosoft.com`, `lab06-user-c@tenant.onmicrosoft.com`
- Expected source IP: redacted in the public repo
- Notes: Two failed attempts were generated per user inside roughly 90 seconds from an incognito browser session. This produced a clean burst pattern for the initial hunt and the scheduled analytic.
- Screenshot: [Failed sign-in burst hunt](../screenshots/04_failed_signin_burst_hunt.png)
- Correlation IDs: not required for the public write-up

## Scenario 2 — Successful sign-in after recent failure burst

- Start UTC: 2026-03-12T20:43:03Z
- End UTC: 2026-03-12T20:54:27Z
- User: `lab06-user-b@tenant.onmicrosoft.com`
- Expected source IP: redacted in the public repo
- Notes: The first successful login triggered a forced password change, but it still provided the post-failure success signal I wanted for hunting context.
- Screenshot: [Successful sign-in after failure burst hunt](../screenshots/05_success_after_failure_burst_hunt.png)
- Correlation IDs: not required for the public write-up

## Scenario 3 — Directory role assignment change

- Start UTC: 2026-03-12T20:55:00Z
- End UTC: 2026-03-12T21:07:19Z
- Actor: redacted external lab admin account
- Target user: `lab06-role-target@tenant.onmicrosoft.com`
- Role: `Security Reader`
- Notes: Initial hunt validation used a wider start time to account for audit log ingestion delay. During rule validation, I intentionally removed and then re-added the Security Reader role assignment so both role membership events would appear in Sentinel. Duplicate rows were observed for the remove action under the same correlation value, which was acceptable for this validation flow.
- Observed `OperationName` values: `Add member to role`, `Remove member from role`
- Screenshots:
  - [Role assignment hunt](../screenshots/06_role_assignment_hunt.png)
  - [Identity incident triggered](../screenshots/11_identity_incident_triggered.png)
- Correlation IDs: recorded locally during validation and omitted from the public repo

## Scenario 4 — Service principal credential addition

- Start UTC: 2026-03-12T20:56:00Z
- End UTC: 2026-03-12T21:07:19Z
- Actor: redacted guest admin account
- App / service principal: `lab06-sp-detection-test`
- Credential display name: `lab06-temp-secret-01`
- Notes: My original manually recorded start time was later than the actual `TimeGenerated` values in Sentinel. I removed the time filter first, confirmed the events by content, and then pushed the hunt start back to `2026-03-12T20:56:00Z` so both audit events were captured cleanly. Two events fired under the same change flow: `Add service principal credentials` was the main detection signal, and `Update service principal` was the companion write event.
- Observed `OperationName` values: `Add service principal credentials`, `Update service principal`
- Screenshot: [Service principal credential addition hunt](../screenshots/07_sp_credential_addition_hunt.png)
- Correlation IDs: recorded locally during validation and omitted from the public repo
