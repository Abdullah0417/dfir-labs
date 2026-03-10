Hands-on DFIR and cloud SecOps labs covering telemetry validation, threat hunting, incident reconstruction, endpoint casework, memory triage, and AWS detection/response.

## What this proves
- I can build and validate telemetry pipelines across Windows, Azure, and AWS.
- I can turn findings into usable security content: hunts, scheduled analytics, automation, workbooks, and exported artifacts.
- I can do publish-safe forensic work without dumping raw evidence into GitHub.
- I can correlate endpoint, log, and cloud evidence into clear timelines, detections, and response actions.

## Skills demonstrated
- Microsoft Sentinel investigation workflow: incidents, entities, timelines, workbooks, and rule tuning
- Azure Monitor Agent (AMA) + Data Collection Rules (DCR) onboarding and telemetry validation
- Windows telemetry: Sysmon + Security Event Logs for authentication, admin, persistence, and process activity
- KQL authoring, validation, joins, decoding, triage queries, and detection logic
- Detection engineering: scheduled analytics, MITRE mapping, tuning notes, and rules-as-code exports
- SOAR-lite automation: tagging, severity updates, triage actions, and exported workflow artifacts
- Endpoint forensics: KAPE, MFTECmd, EvtxECmd, Timeline Explorer, chain of custody, and evidence manifests
- Memory triage under cloud constraints, including process-memory proof and documented investigative pivots
- AWS detection and response with GuardDuty, Security Hub, EventBridge, SNS, Lambda, Athena, S3, and Terraform
- Publish-safe repo discipline: screenshots, queries, templates, notes, manifests, and sanitized IOC packs only

## Labs
| Lab | Focus | Status |
|---|---|---|
| [01 — Telemetry + SIEM Validation](labs/01-telemetry-siem-validation/) | Validate AMA/DCR onboarding and prove Heartbeat, Sysmon, and Security event ingestion in Sentinel | ✅ Done |
| [02 — Multi-Host Incident Reconstruction](labs/02-incident-reconstruction/) | Correlate cross-host activity into a timeline and operationalize the result as detection, automation, and workbook content | ✅ Done |
| [03 — Controls-to-Telemetry Audit](labs/03-controls-to-telemetry-audit/) | Test which security controls are actually observable and document gaps with validation queries and a coverage matrix | ✅ Done |
| [04 — Endpoint Forensics Casework](labs/04-endpoint-forensics-casework/) | Triage MFT and EVTX artifacts, build a timeline, package IOCs, and uplift findings into Sentinel content | ✅ Done |
| [05 — Windows Memory Forensics + Cloud SecOps Loop](labs/05-memory-forensics-cloud-secops-loop/) | Document Azure memory-acquisition constraints, pivot cleanly to process-memory proof, and complete the Sentinel hunt-to-response loop | ✅ Done |
| 06 — Entra ID Detection Engineering + Content Validation Pipeline | Planned identity-focused Sentinel lab centered on Entra ID telemetry, detection content, and a gated validation/deployment workflow | 📋 Planned |
| [07 — AWS GuardDuty Detection + Response](labs/07-aws-guardduty-detection-response/) | Build AWS-native alerting, finding retention, Athena triage, and Security Hub-driven response workflow | ✅ Done |
| 08 — AWS IAM + S3 Misconfiguration Response | Planned posture and remediation lab focused on unintended access, attribution, and control validation | 📋 Planned |

Each completed lab includes a `README.md`, proof screenshots, and the artifacts that matter for that case: KQL, detection exports, automation exports, workbook content, IOC packs, Terraform, Athena SQL, Lambda code, notes, or manifests where applicable.

_Last updated: 2026-03-10_

## Tooling / Stack
- Microsoft Sentinel + Log Analytics Workspace
- Azure Monitor Agent (AMA) + Data Collection Rules (DCR)
- Sysmon + Windows Security Event Logs
- KAPE, MFTECmd, EvtxECmd, Timeline Explorer
- Volatility 3 and process-memory triage workflow
- ARM/JSON exports for Sentinel rules, automation, and workbook artifacts
- AWS CLI, Terraform, Amazon GuardDuty, AWS Security Hub, Amazon EventBridge, Amazon SNS, AWS Lambda, Amazon Athena, Amazon S3, AWS CloudTrail, IAM Access Analyzer, AWS Config

## How to use this repo
- Start in a lab folder and read its `README.md` first.
- Use the screenshots to verify the expected results and analyst-facing outputs.
- Open the artifact folders for the reusable pieces: queries, detections, automation, workbook content, Terraform, SQL, notes, and IOC packs.
- Treat each lab as a scoped case study with its own evidence trail, validation logic, and documentation.

## Notes / Safety
- Raw evidence is never published. No EVTX, MFT, memory images, binaries, secrets, or local case data are committed.
- The repo contains reproducible queries, exports, templates, screenshots, notes, and hash-based manifests only.
- Cloud cost discipline matters. Labs that create billable services include teardown and cleanup notes.
- Access is kept narrow where possible. Avoid exposing management services directly to the public internet.
