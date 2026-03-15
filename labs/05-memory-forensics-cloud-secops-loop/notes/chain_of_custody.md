# Chain of custody

## Case
- **Case ID:** 2026-02-26_Lab05_WinWS1_MemoryTriage
- **Primary host:** `win-ws1` (acquisition + canary)
- **Analysis host:** `win-ws2` (strings triage + Sentinel authoring)
- **Evidence root (LOCAL ONLY):** `C:\Evidence\Cases\<CaseID>\...`
- **Repo root (SAFE TO COMMIT):** `labs/lab-05-memory-forensics-cloud-secops-loop/`

## Evidence items (hashes only)
See `notes/evidence_manifest.csv` for SHA256.

## Custody events (high-level)
1. **Collection (win-ws1):**
   - Full-memory acquisitions attempted (FTK / WinPmem variants). Images retained under the evidence root.
   - Process-memory dump collected for the canary PowerShell process using `comsvcs.dll MiniDump`.
2. **Transfer (win-ws1 → win-ws2):**
   - Process dump copied to `\\win-ws2\EvXfer\` over SMB.
   - SHA256 computed on both hosts to confirm integrity.
3. **Analysis (win-ws2):**
   - Strings extracted from the dump to a **LOCAL ONLY** output file (`ps_canary_strings.txt`).
   - Only screenshots + hashes + derived IOCs were retained for the repo.

## Evidence discipline (publish-safe)
- **Never committed:** `.dmp`, `.raw`, `.mem`, or `ps_canary_strings.txt`.
- **Committed:** screenshots proving steps + hashes, KQL, exports (rules/workbook), and the SHA256 manifest.
