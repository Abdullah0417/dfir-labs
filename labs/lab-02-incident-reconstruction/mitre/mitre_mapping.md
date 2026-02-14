# MITRE ATT&CK Mapping — Lab 02

| Tactic | Technique | Sub-technique | Why it applies | Primary telemetry | Evidence |
|---|---|---|---|---|---|
| Execution | T1059 (Command and Scripting Interpreter) | T1059.001 (PowerShell) | Encoded PowerShell execution using `-EncodedCommand` / `-enc` is a common obfuscation pattern for script-based execution. | Sysmon EID 1 (Process Create) with `CommandLine` and `Image` fields. | Screenshot: `../screenshots/mitre_mapping_t1059_001.png` |

## Detection implemented
- Scheduled analytic rule: `LAB02 - Encoded PowerShell Execution`
- Query frequency: 5m, lookback: 1h
- Entities: Host (Computer), Account (User)
