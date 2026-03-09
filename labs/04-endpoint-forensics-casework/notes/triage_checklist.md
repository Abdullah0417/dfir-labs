# Triage Checklist — Lab 04 (Endpoint Forensics Casework)

## Scope and goals
- Host: win-ws1
- Goal: Validate a controlled persistence pattern using disk + logs, then convert findings into Sentinel detection content.
- Evidence boundary: raw evidence stays local under `C:\Evidence\Cases\...` (no raw evidence in repo).

## Pre-flight
- [ ] Start PowerShell transcript to `C:\Evidence\Cases\<case>\notes\command_log.txt`
- [ ] Create case folder structure under `C:\Evidence\Cases\<case>\...`
- [ ] Create repo lab folder structure under `labs/lab-04-endpoint-forensics-casework\...`
- [ ] Record system context (host, user, date/time, tool paths)

## Controlled artifact generation (benign)
- [ ] Create directory `%APPDATA%\AdobeUpdate`
- [ ] Create script `%APPDATA%\AdobeUpdate\adobeupdate.ps1`
- [ ] Execute script once using PowerShell with bypass-style flags
- [ ] Create scheduled task `AdobeUpdateSvc` to execute script at logon
- [ ] Verify task configuration with `schtasks /Query /TN AdobeUpdateSvc /V /FO LIST`

## Evidence collection (local only)
### Disk artifact
- [ ] Collect `$MFT` using KAPE to `raw\triage\kape\C\$MFT`
- [ ] Preserve KAPE copy logs (`*_CopyLog.csv`, `*_ConsoleLog.txt`)

### Event logs
- [ ] Export EVTX using `wevtutil epl`:
  - [ ] `Security.evtx`
  - [ ] `System.evtx`
  - [ ] `Application.evtx`
  - [ ] `Sysmon.evtx` (if present)

## Integrity and handling
- [ ] Generate SHA256 evidence manifest for:
  - [ ] `$MFT`
  - [ ] EVTX exports
  - [ ] `command_log.txt`
  - [ ] `command_log_part2.txt` (if used)
- [ ] Update chain-of-custody with evidence list + storage location
- [ ] Confirm no evidence moved into repo

## Parsing (local only)
- [ ] Parse `$MFT` with MFTECmd to `work\parsed\mft\MFTECmd_C_<ts>.csv`
- [ ] Parse EVTX directory with EvtxECmd to `work\parsed\evtx\EvtxECmd_Exported_<ts>.csv`
- [ ] Verify outputs exist and are non-trivial in size

## Correlation and findings
- [ ] Identify file creation record for `...\AdobeUpdate\adobeupdate.ps1` in MFTECmd output
- [ ] Identify PowerShell process execution in Sysmon (Event ID 1) referencing the script path
- [ ] Identify scheduled task creation in Security (Event ID 4698) for `AdobeUpdateSvc`
- [ ] Build UTC timeline in `notes/timeline.md` with evidence references

## Publish-safe outputs
- [ ] IOC pack created in `ioc/malware_triage_iocs.csv`:
  - [ ] Script SHA256
  - [ ] Script file path
  - [ ] Scheduled task name
  - [ ] PowerShell command line pattern
- [ ] Sentinel content created:
  - [ ] KQL hunts saved under `kql/`
  - [ ] Analytic rule configured and enabled
  - [ ] Incident proof captured
  - [ ] Automation rule created and validated
  - [ ] Workbook created and exported as redacted ARM template

## Redactions and repo safety checks (before push)
- [ ] Confirm repo contains no raw evidence:
  - [ ] No `.evtx`
  - [ ] No `$MFT`
  - [ ] No KAPE target directories or raw outputs
  - [ ] No MFTECmd/EvtxECmd parsed CSVs
- [ ] Review exported JSON/templates for identifiers:
  - [ ] Subscription/workspace/tenant IDs removed or replaced with placeholders
- [ ] Review screenshots for secrets/identifiers (tokens, subscription IDs, workspace IDs)

## Wrap-up
- [ ] Stop transcript (or confirm transcript not running)
- [ ] Hash any additional transcript parts and update manifest
- [ ] Git status clean except for publish-safe lab folder changes
- [ ] Commit + push only `labs/lab-04-endpoint-forensics-casework/`