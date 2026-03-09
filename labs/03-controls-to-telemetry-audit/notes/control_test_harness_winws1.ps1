# Lab 03 — benign control test harness
# Creates known events so Sentinel KQL can validate coverage.

$User = "lab03_user"
$Pass = "P@ssw0rd-ForLab03!"   # lab-only; do not reuse anywhere
$TaskPath = "\Lab03\"
$TaskName = "CanaryTask"
$FullTask = $TaskPath + $TaskName

Write-Host "== A) Generate a failed logon (4625) =="
cmd /c "net use \\localhost\ipc$ /user:$User WrongPassword123" | Out-Null

Write-Host "== B) Create local user (4720) =="
cmd /c "net user $User $Pass /add" | Out-Null

Write-Host "== C) Add user to local Administrators (4732) =="
cmd /c "net localgroup Administrators $User /add" | Out-Null

Write-Host "== D) Create scheduled task (4698) =="
cmd /c "schtasks /Create /TN `"$FullTask`" /SC ONCE /ST 23:59 /TR `"cmd.exe /c whoami > C:\Windows\Temp\lab03_canary.txt`" /RU SYSTEM /F" | Out-Null

Write-Host "== E) Change audit policy (4719) =="
cmd /c "auditpol /set /subcategory:`"Security Group Management`" /success:enable /failure:enable" | Out-Null

Write-Host "Done. Next: run Sentinel validation KQL pack."
