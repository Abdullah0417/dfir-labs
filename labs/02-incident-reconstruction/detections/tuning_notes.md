# Detection tuning notes — LAB02 - Encoded PowerShell Execution

## Current logic
- Data source: `Event` table, Sysmon Operational, EID 1
- Filters:
  - `Image` ends with `\powershell.exe` or `\pwsh.exe`
  - `CommandLine` contains `-EncodedCommand` or `-enc`

## Expected false positives
- Administrative scripts that legitimately use encoded commands
- Some endpoint management tools that invoke PowerShell with encoded payloads

## Low-effort tuning ideas
- Add allowlists for known parent processes (e.g., SCCM/Intune agents) **in your environment**
- Require an additional suspicious signal (e.g., unusual parent, network connection shortly after)
- During lab runs, require a lab marker string written by the test command (e.g., `lab02_encoded_test.txt`)
