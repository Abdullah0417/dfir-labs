# Pivot decision: full-RAM Volatility blocked in Azure → process-memory dump (Azure-only)

## Goal (original plan)
Triage a full-RAM memory image from `win-ws1` with Volatility 3 (target milestone: `windows.info` works → pslist/pstree/cmdline/netscan).

## Constraint (what blocked the plan)
In this Azure guest environment, multiple full-memory acquisition methods produced images that **Volatility could not build a Windows kernel layer from**.

Observed failures (repeatable):
- `No suitable kernels found during pdbscan`
- Unsatisfied requirements: `kernel.layer_name`, `kernel.symbol_table_name`

Additional acquisition proof (pre-fix FTK image):
- The FTK `memdump.mem` reads as **all 0x00 above the 4GB boundary** at offsets:
  - `0x100000000`, `0x140000000`, `0x180000000`, `0x200000000`

## Attempts (kept intentionally brief)
Azure-only retries were performed to remove “operator error” as a variable:
- VM resized (4GB → 2GB)
- FTK `.mem` + WinPmem `.raw` variants
- Volatility symbols validated and placed under `symbols\windows\*.json.xz`

Result: full-RAM kernel discovery remained blocked.

## Decision (what we did instead)
To stay **Azure-only** and still produce memory-backed evidence, we pivoted to **process-memory forensics**:
1. Launch a benign `powershell.exe -EncodedCommand` canary on `win-ws1`.
2. Capture **only that process’s memory** using `comsvcs.dll MiniDump`.
3. Transfer the dump to `win-ws2`.
4. Extract strings and prove the canary markers + encoded command line exist in memory.
5. Operationalize the same signal in Sentinel: hunts → analytic rule → automation → workbook.

## What this preserves (why this still “counts” as memory forensics)
- We did not lose the volatile-memory objective.
- We narrowed scope from “full system RAM” to “memory of the suspicious process”, which is a defensible approach when full-RAM acquisition is unreliable.

## Proof artifacts (publish-safe)
- Full-RAM blocker proof:
  - `screenshots/02_volatility_failure_pdbscan_no_kernels.png`
  - `screenshots/03_memdump_zero_above_4gb.png`
- Process-memory proof:
  - `screenshots/05_process_dump_created_winws1.png`
  - `screenshots/07_strings_extraction_command.png`
  - `screenshots/08_strings_hits_canary_markers.png`
  - `screenshots/09_strings_hits_encoded_commandline.png`
- Sentinel loop proof:
  - `screenshots/01_incident_tagged_high_lab05.png`
  - `screenshots/00_workbook_case_view.png`
