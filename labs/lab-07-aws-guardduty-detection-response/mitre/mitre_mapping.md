# MITRE Mapping — Lab 07

## Featured finding
- **Title:** `[SAMPLE] The EC2 instance i-99999999 is communicating with a Tor entry node.`
- **GuardDuty finding type:** `UnauthorizedAccess:EC2/TorClient`
- **Why this finding anchors the lab:** it appears cleanly across the GuardDuty view, the SNS alert email, the Security Hub ASFF view, and the final response-state proof.

## MITRE ATT&CK mapping
- **Technique:** `T1090.003 – Multi-hop Proxy`

## Why this mapping fits
This sample finding represents outbound communication that GuardDuty associates with Tor infrastructure. Tor is a layered relay network used to obscure origin and destination. That behavior aligns best with **T1090.003 – Multi-hop Proxy**.

In this lab, the point is not to claim that Tor traffic automatically proves compromise. The point is to show that the security workflow can detect, surface, retain, triage, alert on, and respond to proxy-anonymization behavior that would deserve analyst review in a real environment.

## Why broader claims were not made
The uploaded proof does not show successful intrusion, persistence, credential theft, data exfiltration, or impact. It supports a narrow mapping to proxy-based traffic obfuscation and nothing more.

## Supporting artifacts
- `../screenshots/01_finding_generated.png`
- `../screenshots/05_alert_fired.png`
- `../screenshots/securityhub_asff_finding_json.png`
- `../screenshots/06_response_executed.png`
