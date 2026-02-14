Hands-on DFIR labs focused on enterprise telemetry, hunting, and incident reconstruction in Azure.

**This proves:** I can set up end-to-end logging pipeline (Sysmon + Security → AMA/DCR → Log Analytics/Sentinel) and use it to validate telemetry, hunt, and reconstruct incidents.

## Labs
| Lab | Focus | Outputs |
|---|---|---|
| [Lab 01 — Telemetry + SIEM Validation (Sentinel)](labs/lab-01-telemetry-siem-validation/) | Confirm ingestion + baseline telemetry | KQL queries + screenshots + config proof |
| [Lab 02 — Incident Reconstruction (Sentinel)](labs/lab-02-incident-reconstruction/README.md) | Multi-host timeline + detection + automation | KQL + incident proof + analytic rule + automation rule + workbook |

## Tooling / Stack
- Microsoft Sentinel + Log Analytics Workspace
- Azure Monitor Agent (AMA) + Data Collection Rules (DCR)
- Sysmon + Windows Security Event Logs

## How to use this repo
- Open a lab folder and follow its `README.md`.
- Run KQL in each lab’s `/kql` folder.
- Compare results to `/screenshots`.

## Notes / Safety
- Costs: shut down VMs when idle; avoid open inbound rules.
- Access: prefer Bastion; avoid public Internet RDP.
- Evidence: local casework paths are documented, but raw evidence is not published.
