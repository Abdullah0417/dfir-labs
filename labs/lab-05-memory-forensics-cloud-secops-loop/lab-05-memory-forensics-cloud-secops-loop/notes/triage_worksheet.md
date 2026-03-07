# Triage worksheet (what I checked and what it proved)

## Objective
Validate suspicious `-EncodedCommand` PowerShell activity with **memory-backed evidence**, then turn it into a **repeatable Sentinel loop**.

## Full-RAM triage status
- **Result:** Blocked in Azure guest environment.
- **Evidence:** Volatility fails kernel discovery (`pdbscan`), and the FTK image reads as zero above 4GB boundary. (See `screenshots/02_volatility_failure_pdbscan_no_kernels.png`, `screenshots/03_memdump_zero_above_4gb.png`)

## Pivoted memory evidence (process-memory)
- **Acquisition:** `comsvcs.dll MiniDump` of the running canary PowerShell process on `win-ws1`.
- **Integrity:** SHA256 recorded in `notes/evidence_manifest.csv` (hash-only) and verified on transfer.
- **Content validation (strings):**
  - Marker proof: `LAB05_CANARY_START`, `Invoke-WebRequest`, `example.com`, `Start-Sleep`.
  - Command-line proof: `powershell.exe ... -EncodedCommand <base64>`.
  - See `screenshots/08_strings_hits_canary_markers.png` and `screenshots/09_strings_hits_encoded_commandline.png`.

## Sentinel investigation (hunts)
- Decoded EncodedCommand from Sysmon EID 1 RenderedDescription. (See `kql/02_decode_encodedcommand_from_rendereddescription.kql`)
- Correlated Sysmon EID 1 ↔ EID 3 using ProcessGuid. (See `kql/03_correlate_eid1_eid3_by_processguid.kql`)

## Operationalized response
- **Detection:** Scheduled analytic rule (exported). (See `detections/LAB05_encoded_powershell_decoded_rule.json`)
- **Automation:** On incident creation, tag `lab05` + set severity `High` (exported). (See `automation/LAB05_automation_tag_escalate.json`)
- **Workbook:** “Case view” dashboard with Host + Marker parameters (exported). (See `workbooks/LAB05_case_view_workbook.json`)
