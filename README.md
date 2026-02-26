Hands-on DFIR labs focused on enterprise telemetry, hunting, incident reconstruction, and endpoint casework in Azure (Microsoft Sentinel).

## This proves
- I can build an end-to-end Windows telemetry pipeline (Sysmon + Security → AMA/DCR → Log Analytics/Sentinel).
- I can move from findings → hunts → scheduled analytic rules → automation → workbooks (rules-as-code where possible).
- I can perform endpoint forensics casework (MFT/EVTX triage, hashing, chain-of-custody) without publishing raw evidence.

## Skills demonstrated
- Microsoft Sentinel (Log Analytics) investigation workflow: incidents, entities, timelines
- Azure Monitor Agent (AMA) + Data Collection Rules (DCR) telemetry onboarding
- Windows telemetry: Sysmon + Security Event Logs (auth + admin + persistence signals)
- KQL authoring + validation (tables, joins, charts)
- Detection engineering: scheduled analytic rules + tuning notes + MITRE mapping
- SOAR-lite automation rules (tagging, severity, triage actions)
- Endpoint forensics: EVTX export, MFT parsing, artifact correlation, publish-safe IOC packaging (hashes/paths only)
- DFIR discipline: evidence kept local; repo contains reproducible queries + proof screenshots + templates + hash manifests

## Labs
| Lab | Focus | Outputs | Status |
|---|---|---|---|
| [Lab 01 — Telemetry + SIEM Validation (Sentinel)](labs/lab-01-telemetry-siem-validation/) | Confirm ingestion + baseline telemetry | KQL queries + screenshots + config proof | ✅ Done |
| [Lab 02 — Incident Reconstruction (Sentinel)](labs/lab-02-incident-reconstruction/) | Multi-host timeline + detection + automation | KQL + incident proof + analytic rule + automation rule + workbook | ✅ Done |
| [Lab 03 — Controls-to-Telemetry Audit (Sentinel)](labs/lab-03-controls-to-telemetry-audit/) | Prove what security controls are observable (and where blind spots exist) | Validation KQL pack + coverage matrix + analytic rule + automation rule + workbook | ✅ Done |
| [Lab 04 — Endpoint Forensics Casework (MFT/EVTX)](labs/lab-04-endpoint-forensics-casework/) | Disk + log artifact triage and correlation, then uplift into detection | Evidence manifest (SHA256) + chain-of-custody + timeline + IOC pack + hunts + analytic rule + automation rule + workbook | ✅ Done |
| Lab 05 — Memory Forensics + Cloud SecOps | Volatility 3 triage + bridge findings into Sentinel | Volatility output + hunts + analytic rule + workbook + automation | 🔄 In Progress |
| Lab 06 — Capstone Report | Tie Labs 02/04/05 into one consulting-grade deliverable | Final report + exec summary + technical appendix + NIST CSF mapping | 📋 Planned |
| Lab 07 — AWS GuardDuty Detection + Response | AWS-native detection, centralized findings, automated response | GuardDuty + Security Hub + EventBridge + CloudTrail + Terraform IaC | 📋 Planned |
| Lab 08 — AWS IAM + S3 Misconfiguration | Posture detection + remediation + compliance validation | Access Analyzer + Config rules + Security Hub + Terraform IaC | 📋 Planned |

_Last updated: 2026-02-26_

## Tooling / Stack
- Microsoft Sentinel + Log Analytics Workspace
- Azure Monitor Agent (AMA) + Data Collection Rules (DCR)
- Sysmon + Windows Security Event Logs
- Endpoint triage tooling (inside lab VMs): KAPE, Zimmerman's MFTECmd/EvtxECmd, Timeline Explorer
- Volatility 3 (Lab 05)
- Planned (Labs 07–08): AWS CLI, Terraform, Amazon GuardDuty, AWS Security Hub, Amazon EventBridge, AWS CloudTrail, IAM Access Analyzer, AWS Config

## How to use this repo
- Open a lab folder and follow its `README.md`.
- Run KQL in each lab’s `/kql` folder.
- Compare results to `/screenshots`.
- Review `/detections`, `/automation`, and `/workbooks` for deployable artifacts (templates/exports).

## Notes / Safety
- Costs: shut down VMs when idle; avoid open inbound management ports.
- Access: prefer Bastion; avoid public Internet RDP.
- Evidence: raw artifacts (EVTX/MFT/dumps/binaries) are never published—only reproducible queries, exports/templates, proof screenshots, and hash manifests.
