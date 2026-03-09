# Timeline (UTC)

| Time (UTC) | Host | Artifact | What happened | Evidence |
|---|---|---|---|---|
| 2026-02-24T22:45:46Z | win-ws1 | MFT | `adobeupdate.ps1` created in `%APPDATA%\AdobeUpdate` | MFTECmd row + [screenshots/07_mft_suspicious_file_row.png](../screenshots/07_mft_suspicious_file_row.png) |
| 2026-02-24T22:46:10Z | win-ws1 | EVTX (Sysmon) | `powershell.exe` executed the script with bypass-style flags | EvtxECmd row + [screenshots/09_evtx_powershell_exec_sysmon.png](../screenshots/09_evtx_powershell_exec_sysmon.png) |
| 2026-02-24T22:47:14Z | win-ws1 | EVTX (Security 4698) | Scheduled task `AdobeUpdateSvc` created for logon persistence | EvtxECmd row + [screenshots/08_evtx_task_create_4698.png](../screenshots/08_evtx_task_create_4698.png) |
