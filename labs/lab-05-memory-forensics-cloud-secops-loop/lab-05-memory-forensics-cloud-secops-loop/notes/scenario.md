# Scenario

A Sentinel hunt surfaced repeated **PowerShell `-EncodedCommand` executions** on `win-ws1` with outbound HTTP activity in the same window.

The lab’s intent was to validate this activity two ways:
- **Memory-backed proof** (volatile evidence that won’t reliably exist on disk)
- **Cloud SecOps loop** (turn the investigation into a repeatable Sentinel detection + response workflow)

Because full-RAM Volatility triage was blocked in the Azure guest environment, the memory component pivots to **process-memory evidence** (PowerShell canary dump + strings proof). See `notes/pivot-constraints-and-decision.md`.
