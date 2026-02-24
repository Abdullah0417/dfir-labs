Hands-on DFIR labs focused on enterprise telemetry, hunting, and incident reconstruction in Azure.

**This proves:** I can set up an end-to-end logging pipeline (Sysmon + Security → AMA/DCR → Log Analytics/Sentinel) and use it to validate telemetry coverage, hunt, and reconstruct incidents.

## Skills demonstrated
- Microsoft Sentinel (Log Analytics) investigation workflow
- Azure Monitor Agent (AMA) + Data Collection Rules (DCR) telemetry onboarding
- Windows telemetry: Sysmon + Security Event Logs (auth + admin activity)
- KQL authoring + validation queries (tables + charts)
- DFIR discipline: evidence kept local; repo contains reproducible queries + proof screenshots + notes

## Labs
| Lab | Focus | Outputs |
|---|---|---|
| [Lab 01 — Telemetry + SIEM Validation (Sentinel)](labs/lab-01-telemetry-siem-validation/) | Confirm ingestion + baseline telemetry | KQL queries + screenshots + config proof |
| [Lab 02 — Incident Reconstruction (Sentinel)](labs/lab-02-incident-reconstruction/README.md) | Multi-host timeline + detection + automation | KQL + incident proof + analytic rule + automation rule + workbook |
| [Lab 03 — Controls-to-Telemetry Audit (Sentinel)](labs/lab-03-controls-to-telemetry-audit/) | Prove what security controls are observable (and where blind spots exist) | Validation KQL pack + coverage matrix + analytic rule + automation rule + workbook |

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
