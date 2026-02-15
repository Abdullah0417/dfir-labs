# LAB 02 — Multi-host Incident Reconstruction (Microsoft Sentinel + Sysmon)

## What this proves

- Multi-host endpoint telemetry ingestion into Sentinel (`win-ws1`, `win-ws2`) validated via `Heartbeat` and Windows Event Logs.
- Cross-host reconstruction using a single **timeline query** that correlates Sysmon + Security events.
- Hunt → **Scheduled analytic rule** shipped: `LAB02 - Encoded PowerShell Execution` (MITRE `T1059.001`).
- **SOAR-lite automation** shipped: tag + severity escalation on incident creation.
- **Workbook dashboard** shipped for “client-ready” investigation views.

## Topology (lab)

- `win-ws1` — Windows endpoint
- `win-ws2` — Windows endpoint
- `ub-attacker` — Ubuntu attacker VM (optional; internal only, not onboarded to Sentinel for this lab)
- Log Analytics workspace: `law-dfir`
- Resource group: `rg-dfir-lab-scus`

## Data sources / tables used

- `Heartbeat` — agent health
- `Event` — Windows Event Logs via AMA + DCR
- Sysmon: `Microsoft-Windows-Sysmon/Operational` (EIDs: `1`, `3`)
- Security: `Security` (EIDs: `4624`, `4625`)

**Implementation detail:** in this workspace, `Event.EventData` is XML (string).  
Queries parse it using `parse_xml()` and build a bag to extract fields like `Image`, `CommandLine`, and account names.

---

## Artifacts (this repo)

- KQL queries: `kql/`
- Analytic rule export (ARM): `detections/LAB02_encoded_powershell_rule.arm.json`
- Automation rule export (ARM): `automation/AB02_soar_lite_automation_rule.arm.json`
- Workbook template: `workbooks/LAB02_timeline_dashboard.galleryTemplate.json`
- IOC list (lab-scoped): `ioc/ioc_list.csv`
- MITRE mapping: `mitre/mitre_mapping.md`
- Redactions note: `notes/redactions.md`

---

## Evidence (screenshots)

- Workbook dashboard: [`screenshots/workbook_timeline_dashboard.png`](screenshots/workbook_timeline_dashboard.png)
- Timeline results: [`screenshots/lab02_timeline_results.png`](screenshots/lab02_timeline_results.png)
- Events-by-host chart: [`screenshots/events_by_host_timechart.png`](screenshots/events_by_host_timechart.png)
- MITRE mapping view: [`screenshots/mitre_mapping_t1059_001.png`](screenshots/mitre_mapping_t1059_001.png)
- Incident automation: [`screenshots/incident_automation_applied.png`](screenshots/incident_automation_applied.png)
- Ub-attacker overview: [`screenshots/ub-attackers(ubuntu)_vm_overview.png`](screenshots/ub-attackers(ubuntu)_vm_overview.png)

---

## KQL queries (saved under kql/)

Ingestion validation:

- [`kql/01_heartbeat_agent_health.kql`](kql/01_heartbeat_agent_health.kql)
- [`kql/02_sysmon_event_counts_1h.kql`](kql/02_sysmon_event_counts_1h.kql)
- [`kql/03_security_logon_4624_4625_counts_1h.kql`](kql/03_security_logon_4624_4625_counts_1h.kql)

Investigation / reconstruction:

- [`kql/lab02_timeline.kql`](kql/lab02_timeline.kql)
- [`kql/04_events_by_host_5m_24h.kql`](kql/04_events_by_host_5m_24h.kql)

---

## Detection + automation shipped

### Scheduled analytic rule

- Export: [`detections/LAB02_encoded_powershell_rule.arm.json`](detections/LAB02_encoded_powershell_rule.arm.json)
- Tuning notes: [`detections/tuning_notes.md`](detections/tuning_notes.md)

Behavior:

- Detects Sysmon EID 1 where PowerShell runs with `-EncodedCommand` / `-enc`.
- Frequency: every 5 minutes
- Lookback: 1 hour
- Event grouping: alert per result

### Automation rule (SOAR-lite)

- Export: [`automation/AB02_soar_lite_automation_rule.arm.json`](automation/AB02_soar_lite_automation_rule.arm.json)
- Notes: [`automation/README.md`](automation/README.md)

Behavior:

- Trigger: incident created from the LAB02 analytic rule
- Actions: tag `lab02`, set severity `High`

> Publish-safe note: owner assignment was removed to avoid leaking user identifiers. See `notes/redactions.md`.

---

## Workbook shipped

- Template: [`workbooks/LAB02_timeline_dashboard.galleryTemplate.json`](workbooks/LAB02_timeline_dashboard.galleryTemplate.json)

Contents:

- Scenario text block
- Timeline grid (Sysmon + Security merged)
- Time chart (events-by-host, 5m bins)

---

## Repro steps (lab-safe)

### 1) Validate ingestion

Run the 3 ingestion KQL queries (`kql/01_*` → `kql/03_*`).

### 2) Generate a known-good signal (Encoded PowerShell)

Run on **either** `win-ws1` or `win-ws2`:

```powershell
$cmd = '"LAB02 encoded test $(Get-Date -Format o)" | Out-File C:\ProgramData\lab02_encoded_test.txt -Append'
$b64 = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd))
powershell.exe -NoProfile -EncodedCommand $b64
