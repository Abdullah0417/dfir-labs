# Timeline (UTC)

> This is a concise timeline suitable for a recruiter-facing repo. Detailed console logs remain LOCAL ONLY.

- **2026-03-01 23:52Z** — Full-memory image captured and hashed (FTK) from `win-ws1` (Volatility later fails kernel discovery). (See `notes/evidence_manifest.csv`)
- **2026-03-04 04:17Z** — Sysmon EID 1 shows `powershell.exe` launched with `-EncodedCommand` on `win-ws1`. (See `screenshots/10_sentinel_sysmon_eid1_encodedcommand.png`)
- **2026-03-04 04:51Z** — Process-memory dump of the canary PowerShell process collected and hashed. (See `notes/evidence_manifest.csv`)
- **2026-03-04 05:00Z** — Strings extracted from the dump; markers and encoded command line validated. (See `screenshots/08_strings_hits_canary_markers.png`, `screenshots/09_strings_hits_encoded_commandline.png`)
- **2026-03-04 12:02Z** — Sentinel incident created from scheduled analytics rule; automation tags `lab05` and escalates severity to High. (See `screenshots/01_incident_tagged_high_lab05.png`)
- **2026-03-05 22:49Z** — Workbook “case view” confirms latest canary execution + decoded payload + correlated egress. (See `screenshots/00_workbook_case_view.png`)
