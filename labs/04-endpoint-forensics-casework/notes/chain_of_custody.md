# Chain of Custody — Lab 04

- Case ID: 2026-02-24_Lab04_WinWS1_EndpointForensics
- Evidence host: win-ws1
- Collector: labadmin
- Collection method: Live triage (KAPE + wevtutil exports)
- Storage (local only): C:\Evidence\Cases\2026-02-24_Lab04_WinWS1_EndpointForensics\

## Evidence items (local only)
1) $MFT  
   - Source: C:\  
   - Stored at: raw\triage\kape\C\

2) Windows Event Logs (EVTX exports)  
   - raw\triage\evtx\Security.evtx  
   - raw\triage\evtx\System.evtx  
   - raw\triage\evtx\Application.evtx  
   - raw\triage\evtx\Sysmon.evtx

3) Command transcripts  
   - notes\command_log.txt  
   - notes\command_log_part2.txt

## Integrity
- SHA256 evidence manifest (local): C:\Evidence\Cases\2026-02-24_Lab04_WinWS1_EndpointForensics\notes\evidence_manifest.csv
- SHA256 evidence manifest (repo-safe copy): notes/evidence_manifest.csv

## Transfers
- None (lab environment, single handler)

## Notes
- Raw evidence and parsed outputs remain local and are not committed to GitHub.
