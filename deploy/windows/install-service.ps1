# LordCoder Windows service scaffolding
#
# This is intentionally a template for a later packaging phase.
# The current phase validates cross-platform dev installs only.

param(
    [string]$BinaryPath = "C:\Program Files\LordCoder\lordcoder.exe"
)

Write-Host "Planned command:"
Write-Host "sc.exe create LordCoderCore binPath= `"$BinaryPath daemon`" start= auto"
