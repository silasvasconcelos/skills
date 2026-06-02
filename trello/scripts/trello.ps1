<#
.SYNOPSIS
  Minimal Trello REST API client for Windows (PowerShell 5.1+ / PowerShell 7+).

.DESCRIPTION
  Wraps Invoke-RestMethod (no external dependency) to call the Trello REST API.
  Auth is read from environment variables:
    TRELLO_API_KEY    (required)
    TRELLO_API_TOKEN  (required; TRELLO_TOKEN accepted as fallback)
  Base URL override: TRELLO_API_BASE (default https://api.trello.com/1).

.PARAMETER Method
  HTTP method: GET, POST, PUT, DELETE.

.PARAMETER Path
  API path with optional query string, e.g. "/members/me/boards?fields=name,url".
  Do NOT include key/token; they are appended automatically.

.PARAMETER Data
  Optional JSON string sent as the request body (Content-Type: application/json).

.EXAMPLE
  ./trello.ps1 GET "/members/me/boards?fields=name,url"

.EXAMPLE
  ./trello.ps1 POST "/cards?idList=<listId>&name=Hello"

.EXAMPLE
  ./trello.ps1 PUT "/cards/<id>" -Data '{"name":"Renamed"}'
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$Method,

  [Parameter(Mandatory = $true, Position = 1)]
  [string]$Path,

  [Parameter(Position = 2)]
  [string]$Data
)

$ErrorActionPreference = 'Stop'

$baseUrl = if ($env:TRELLO_API_BASE) { $env:TRELLO_API_BASE } else { 'https://api.trello.com/1' }
$key     = $env:TRELLO_API_KEY
$token   = if ($env:TRELLO_API_TOKEN) { $env:TRELLO_API_TOKEN } else { $env:TRELLO_TOKEN }

if ([string]::IsNullOrWhiteSpace($key) -or [string]::IsNullOrWhiteSpace($token)) {
  Write-Error "Missing credentials. Set TRELLO_API_KEY and TRELLO_API_TOKEN. See references/authentication.md."
  exit 3
}

# Split path and query so we can append auth params safely.
$pathPart  = $Path
$queryPart = ''
if ($Path.Contains('?')) {
  $idx       = $Path.IndexOf('?')
  $pathPart  = $Path.Substring(0, $idx)
  $queryPart = $Path.Substring($idx + 1)
}
if (-not $pathPart.StartsWith('/')) { $pathPart = '/' + $pathPart }

$auth  = "key=$key&token=$token"
$query = if ($queryPart) { "$queryPart&$auth" } else { $auth }
$url   = "$baseUrl$pathPart`?$query"

$params = @{
  Method = $Method.ToUpper()
  Uri    = $url
}
if ($PSBoundParameters.ContainsKey('Data') -and $Data) {
  $params['Body']        = $Data
  $params['ContentType'] = 'application/json'
}

try {
  $response = Invoke-RestMethod @params
  if ($null -ne $response) {
    $response | ConvertTo-Json -Depth 100
  }
}
catch {
  Write-Error $_.Exception.Message
  if ($_.ErrorDetails -and $_.ErrorDetails.Message) {
    Write-Error $_.ErrorDetails.Message
  }
  exit 1
}
