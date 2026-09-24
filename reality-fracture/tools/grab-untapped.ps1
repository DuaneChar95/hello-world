# Grab Untapped.gg's Reality Fracture Limited pages from your own machine,
# using your installed Chrome or Edge in headless mode. Run in PowerShell:
#
#   Set-ExecutionPolicy -Scope Process Bypass
#   .\grab-untapped.ps1
#
# It writes rendered HTML for each page into .\untapped-out\. Attach those
# files (or zip the folder) in chat and the data will be parsed from them.
#
# If a page needs your Untapped login (premium tables), run it with your
# profile:   .\grab-untapped.ps1 -UseProfile
param([switch]$UseProfile)

$pages = @{
  "tier-list"    = "https://mtga.untapped.gg/limited/draft/reality-fracture/"
  "pick-order"   = "https://mtga.untapped.gg/limited/draft/reality-fracture/pick-order"
  "trophy-decks" = "https://mtga.untapped.gg/limited/draft/reality-fracture/trophy-decks"
  "cards"        = "https://mtga.untapped.gg/limited/draft/reality-fracture/cards"
  "sealed"       = "https://mtga.untapped.gg/limited/sealed/reality-fracture/"
}
$browser = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $browser) { Write-Error "Chrome or Edge not found."; exit 1 }

$out = Join-Path (Get-Location) "untapped-out"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$profileArgs = @()
if ($UseProfile) {
  $ud = if ($browser -like "*chrome*") { "$env:LOCALAPPDATA\Google\Chrome\User Data" } else { "$env:LOCALAPPDATA\Microsoft\Edge\User Data" }
  $profileArgs = @("--user-data-dir=`"$ud`"", "--profile-directory=Default")
  Write-Host "Using your browser profile at $ud (close the browser first)."
}
foreach ($name in $pages.Keys) {
  $file = Join-Path $out "$name.html"
  Write-Host "Fetching $name ..."
  $args = @("--headless=new", "--disable-gpu", "--window-size=1400,4000", "--virtual-time-budget=15000", "--dump-dom") + $profileArgs + @($pages[$name])
  & $browser @args 2>$null | Out-File -Encoding utf8 $file
  $size = (Get-Item $file).Length
  Write-Host "  wrote $file ($size bytes)"
}
Write-Host ""
Write-Host "Done. Attach the files in untapped-out\ (or zip the folder)."
Write-Host "If a file is tiny or shows a login/verification page, open the site normally,"
Write-Host "press F12 -> Network -> filter 'Fetch/XHR', reload, and save the JSON responses"
Write-Host "whose names mention cards, ratings, picks or decks (right-click -> Save as)."
