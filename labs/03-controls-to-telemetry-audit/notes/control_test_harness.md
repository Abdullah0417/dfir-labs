# Lab 03 Control Test Harness (benign)

Purpose: Generate known audit events so Sentinel validation queries can PASS/FAIL deterministically.

Run these on win-ws1 (and optionally repeat on win-ws2).

## Canary identifiers (safe to publish)
- Local test user: lab03_user
- Scheduled task name: \Lab03\CanaryTask

## Actions
A) Failed logon (4625)
B) Create local user (4720)
C) Add user to local Administrators (4732)
D) Create scheduled task (4698)
E) Modify audit policy (4719)

Optional (use with caution):
F) Clear Security log (1102) — destructive locally; do not do this outside a disposable lab
