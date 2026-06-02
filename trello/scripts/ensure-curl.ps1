<#
.SYNOPSIS
  Ensure an HTTP client is available on Windows for calling the Trello API.

.DESCRIPTION
  trello.ps1 uses Invoke-RestMethod, which is built into PowerShell, so no
  install is normally required. This script verifies that and, if you prefer
  the curl.exe binary (bundled with Windows 10 1803+), checks for it too and
  offers to install it via winget or Chocolatey when missing.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

if (Get-Command Invoke-RestMethod -ErrorAction SilentlyContinue) {
  Write-Host "Invoke-RestMethod is available (built into PowerShell). trello.ps1 is ready to use."
}
else {
  Write-Warning "Invoke-RestMethod not found. Upgrade to PowerShell 5.1+ or PowerShell 7: https://aka.ms/powershell"
}

if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
  Write-Host "curl.exe also available: $((Get-Command curl.exe).Source)"
  exit 0
}

Write-Host "curl.exe not found (optional). Attempting install..."

if (Get-Command winget -ErrorAction SilentlyContinue) {
  winget install --id curl.curl -e --source winget
}
elseif (Get-Command choco -ErrorAction SilentlyContinue) {
  choco install curl -y
}
else {
  Write-Warning "Neither winget nor Chocolatey found. curl.exe is optional; trello.ps1 works without it."
  Write-Warning "To install curl manually: https://curl.se/windows/"
}
