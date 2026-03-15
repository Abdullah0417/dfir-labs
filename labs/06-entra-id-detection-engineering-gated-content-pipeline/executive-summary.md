# Executive Summary

This lab shows practical Microsoft Sentinel detection engineering built around Microsoft Entra ID telemetry. The point was not to make a vague platform claim. The point was to show a clean workflow: validate the data, build the hunts, promote the strongest logic into scheduled analytics, add minimal triage context, and keep the resulting content reviewable and safe to publish.

I built three identity-focused detections in Sentinel. The first looks for a failed sign-in burst from one IP across multiple users. The second tracks directory role assignment changes. The third watches for service principal credential additions. I also added a small identity workbook so the results are easier to review and a lightweight automation rule so the lab shows a basic investigation and response flow instead of stopping at query output.

I also proved the gated path around the content. The repo includes the exported detection content, the deploy wrapper, and the proof chain for GitHub OIDC, validation checks, packaging, ARM `what-if`, approval, and controlled deployment into a separate test workspace. That claim stays narrow on purpose: this is a portfolio-scale gated content pipeline, not a finished enterprise release program.

From a technical review perspective, this lab shows that I can validate Entra telemetry before I write detections, use KQL against real identity activity instead of canned sample data, turn hunt logic into scheduled analytics with usable mappings and incident creation, and document the deployment path without overstating what was built.

