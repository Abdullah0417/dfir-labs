# Detection tuning notes — LAB04

## Detection intent
Detect **PowerShell** executing a script from a user-writable AppData path consistent with low-effort persistence.

This lab’s controlled scenario uses:
- Script path: `%APPDATA%\AdobeUpdate\adobeupdate.ps1`
- Suspicious flags: `-ExecutionPolicy Bypass`, `-WindowStyle Hidden`

## Expected false positives
- Admin/helpdesk scripts legitimately run from user profile directories.
- Software updaters and enterprise login scripts may execute from AppData (less common, but possible).

## Tuning recommendations
1. **Add strict PowerShell image filter** (recommended)
   - Require `Image` ends with `\powershell.exe` (or `pwsh.exe` if applicable).

2. **Add flag-based scoring**
   - Alert only when command line contains one or more:
     - `-ExecutionPolicy Bypass`
     - `-EncodedCommand`
     - `-WindowStyle Hidden`
     - `-NoProfile`

3. **Expand coverage beyond a single script name**
   - Detect `\AppData\Roaming\` + suspicious PowerShell flags + `-File`.

4. **Correlate with Scheduled Task creation (Security 4698)**
   - If Security logs are available, correlate a task creation within ±5 minutes to strengthen persistence confidence.

## Validation
- Confirm this lab’s canary activity triggers an alert and creates an incident.
- Confirm the incident includes Host entity mapping and contains the extracted command line.
