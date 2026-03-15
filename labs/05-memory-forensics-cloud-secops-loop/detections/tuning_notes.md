# Detection tuning notes

Rule: **LAB05 - Encoded PowerShell (decoded payload present)** (`detections/LAB05_encoded_powershell_decoded_rule.json`)

## What it detects
- Sysmon **EID 1** ProcessCreate where `RenderedDescription` contains `-EncodedCommand`
- Extracts the base64 blob and decodes it (UTF-16LE), then projects the decoded content

## Tuning ideas (if you deploy this outside a lab)
- **Reduce noise:**
  - Add allowlists for known automation frameworks that legitimately use `-EncodedCommand`.
  - Require additional suspicious context (e.g., `ExecutionPolicy Bypass`, unusual parent process, unusual user).
- **Focus on high-value payloads:**
  - Trigger only if the decoded payload contains high-signal keywords (e.g., `IEX`, `Invoke-WebRequest`, `FromBase64String`, `DownloadString`).
- **Entity mapping:**
  - Map Host from `Computer` (already done).
  - Optionally parse and map Account from `RenderedDescription` if needed.
- **Suppression:**
  - If an admin task repeatedly fires, use suppression windows rather than disabling the rule.
