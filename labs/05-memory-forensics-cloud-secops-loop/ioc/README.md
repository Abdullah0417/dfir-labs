# IOC pack (publish-safe)

This IOC pack is intentionally **keyword + domain** focused (no hashes of malware binaries) because the memory evidence is:
- A **PowerShell canary process-memory dump** (LOCAL ONLY)
- A **strings output file** derived from that dump (LOCAL ONLY)

Repo-safe artifacts include:
- This IOC CSV (`memory_triage_iocs.csv`)
- Screenshots proving each IOC appears in memory and/or telemetry

Derivation method (high level):
1. Extract strings from the process dump (`strings64.exe -u`).
2. Search for deterministic markers and the encoded command line.
3. Cross-check the same EncodedCommand signal in Sysmon EID 1 in Sentinel.

Evidence references are in the `evidence_ref` column.
