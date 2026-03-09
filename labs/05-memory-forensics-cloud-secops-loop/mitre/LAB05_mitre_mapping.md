# MITRE ATT&CK mapping (Lab 05)

This lab intentionally keeps mapping **tight**: only techniques directly supported by evidence artifacts are claimed.

| Technique | Why it applies | Evidence |
|---|---|---|
| **T1059.001 — PowerShell** | Sysmon EID 1 shows `powershell.exe` launched with `-EncodedCommand`; the payload is decoded in Sentinel and also recovered from process memory strings. | `screenshots/10_sentinel_sysmon_eid1_encodedcommand.png` (EID1), `screenshots/11_kql_decode_encodedcommand.png` (decoded payload), `screenshots/09_strings_hits_encoded_commandline.png` (process-memory command line) |

Notes:
- Sysmon EID 3 network connections are used as **supporting context** (correlation via ProcessGuid) but are not claimed as a separate ATT&CK technique in this repo.
