# MITRE ATT&CK Mapping — Lab 04

## T1059.001 — PowerShell (Execution)
- **Why it applies:** PowerShell executed a script from a user profile path with bypass-style flags.
- **Evidence:** Sysmon Event ID 1 process creation showing `powershell.exe ... -ExecutionPolicy Bypass ... -File ...\AdobeUpdate\adobeupdate.ps1`.
  - Proof: [screenshots/09_evtx_powershell_exec_sysmon.png](../screenshots/09_evtx_powershell_exec_sysmon.png)

## T1053.005 — Scheduled Task (Persistence)
- **Why it applies:** A scheduled task was created to execute the PowerShell script at logon.
- **Evidence:** Security Event ID 4698 showing task `AdobeUpdateSvc` with task action/arguments referencing the script path.
  - Proof: [screenshots/08_evtx_task_create_4698.png](../screenshots/08_evtx_task_create_4698.png)
