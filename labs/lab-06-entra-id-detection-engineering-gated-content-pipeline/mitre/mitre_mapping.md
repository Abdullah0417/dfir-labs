# MITRE ATT&CK mapping

I kept the ATT&CK coverage tight and only mapped what the lab actually demonstrated.

| Rule / Hunt | ATT&CK tactic | ATT&CK technique | Why it maps |
|---|---|---|---|
| Failed sign-in burst by IP | Credential Access | T1110 | Repeated failed authentication attempts across multiple users fit brute-force or password-spraying behavior. |
| Directory role assignment change | Persistence, Privilege Escalation | T1098 | Changing role membership alters privileges in the cloud control plane. |
| Service principal credential addition | Persistence | T1098.001 | Adding a new credential creates an additional cloud credential that can be used later. |
| Hunt - Success after recent failure burst | Credential Access | T1110 | Correlating a burst of failures with a later success from the same source adds useful credential abuse context. |

## Notes

- I did not force broader ATT&CK coverage just to make the table look bigger.
- The role assignment and service principal detections are both identity-control-plane signals, but they map to different pieces of the same account manipulation theme.
