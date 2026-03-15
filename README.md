# DFIR / Detection Engineering Portfolio

Hands-on DFIR, detection engineering, and cloud SecOps labs covering telemetry validation, threat hunting, incident reconstruction, endpoint casework, memory triage, identity detections, gated content deployment, and AWS detection/response.

## Portfolio snapshot
- 8 labs total
- 7 labs defined
- 6 completed
- Primary focus: DFIR, detection engineering, Microsoft Sentinel, Microsoft Entra ID, and AWS detection/response
- Deliverables include KQL, detection exports, automation, workbooks, timelines, IOC packs, Terraform, Athena SQL, notes, and manifests

## What this proves
- I can build and validate telemetry pipelines across Windows, Microsoft Entra ID, Azure, and AWS.
- I can turn findings into usable security content: hunts, scheduled analytics, automation, workbooks, exported artifacts, and gated deployment workflows.
- I can do publish-safe forensic work without dumping raw evidence into GitHub.
- I can correlate endpoint, identity, log, and cloud evidence into clear timelines, detections, and response actions.

## Skills demonstrated
- Microsoft Sentinel investigation workflow: incidents, entities, timelines, workbooks, and rule tuning
- Azure Monitor Agent (AMA) + Data Collection Rules (DCR) onboarding and telemetry validation
- Microsoft Entra ID telemetry validation and identity-focused detection engineering in Sentinel
- Windows telemetry: Sysmon + Security Event Logs for authentication, admin, persistence, and process activity
- KQL authoring, validation, joins, decoding, triage queries, and detection logic
- Detection engineering: scheduled analytics, MITRE mapping, tuning notes, and rules-as-code exports
- SOAR-lite automation: tagging, severity updates, triage actions, and exported workflow artifacts
- GitHub Actions validation, packaging, GitHub OIDC trust into Azure, ARM `what-if`, approval gates, and controlled test deployment
- Endpoint forensics: KAPE, MFTECmd, EvtxECmd, Timeline Explorer, chain of custody, and evidence manifests
- Memory triage under cloud constraints, including process-memory proof and documented investigative pivots
- AWS detection and response with GuardDuty, Security Hub, EventBridge, SNS, Lambda, Athena, S3, and Terraform
- Publish-safe repo discipline: screenshots, queries, templates, notes, manifests, and sanitized IOC packs only

## Start here
- [Lab 06 — Entra ID Detection Engineering + Gated Content Pipeline](labs/06-entra-id-detection-engineering-gated-content-pipeline/)  
  Identity-focused detection engineering in Sentinel with GitHub OIDC, validation, packaging, approval gates, and controlled test deployment.
- [Lab 04 — Endpoint Forensics Casework](labs/04-endpoint-forensics-casework/)  
  Endpoint artifact triage, timeline building, IOC packaging, and Sentinel uplift.
- [Lab 05 — Windows Memory Forensics + Cloud SecOps Loop](labs/05-memory-forensics-cloud-secops-loop/)  
  Memory triage under cloud constraints, documented pivots, and hunt-to-response completion in Sentinel.
- [Lab 07 — AWS GuardDuty Detection + Response](labs/07-aws-guardduty-detection-response/)  
  AWS-native alerting, finding retention, Athena triage, and Security Hub-driven response workflow.

## Labs
| Lab | Focus | Status |
|---|---|---|
| [01 — Telemetry + SIEM Validation](labs/01-telemetry-siem-validation/) | Validate AMA/DCR onboarding and prove Heartbeat, Sysmon, and Security event ingestion in Sentinel | ✅ Done |
| [02 — Multi-Host Incident Reconstruction](labs/02-incident-reconstruction/) | Correlate cross-host activity into a timeline and operationalize the result as detection, automation, and workbook content | ✅ Done |
| [03 — Controls-to-Telemetry Audit](labs/03-controls-to-telemetry-audit/) | Test which security controls are actually observable and document gaps with validation queries and a coverage matrix | ✅ Done |
| [04 — Endpoint Forensics Casework](labs/04-endpoint-forensics-casework/) | Triage MFT and EVTX artifacts, build a timeline, package IOCs, and uplift findings into Sentinel content | ✅ Done |
| [05 — Windows Memory Forensics + Cloud SecOps Loop](labs/05-memory-forensics-cloud-secops-loop/) | Document Azure memory-acquisition constraints, pivot cleanly to process-memory proof, and complete the Sentinel hunt-to-response loop | ✅ Done |
| [06 — Entra ID Detection Engineering + Gated Content Pipeline](labs/06-entra-id-detection-engineering-gated-content-pipeline/) | Validate Entra telemetry, build identity detections and triage content, and prove a gated GitHub OIDC validation/package/test-deploy path into a separate Sentinel workspace | ✅ Done |
| [07 — AWS GuardDuty Detection + Response](labs/07-aws-guardduty-detection-response/) | Build AWS-native alerting, finding retention, Athena triage, and Security Hub-driven response workflow | ✅ Done |
| 08 — AWS IAM + S3 Misconfiguration Response | Planned posture and remediation lab focused on unintended access, attribution, and control validation | 📋 Planned |

Each completed lab includes a `README.md`, proof screenshots, and the artifacts that matter for that case: KQL, detection exports, automation exports, workbook content, IOC packs, Terraform, Athena SQL, Lambda code, notes, or manifests where applicable.

_Last updated: 2026-03-14_

## Tooling / Stack
- Microsoft Sentinel + Log Analytics Workspace
- Microsoft Entra ID
- Azure Monitor Agent (AMA) + Data Collection Rules (DCR)
- Sysmon + Windows Security Event Logs
- KAPE, MFTECmd, EvtxECmd, Timeline Explorer
- Volatility 3 and process-memory triage workflow
- ARM/JSON exports for Sentinel rules, automation, and workbook artifacts
- GitHub Actions, GitHub OIDC, and Azure Bicep for validation/package/deploy workflow stages
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
