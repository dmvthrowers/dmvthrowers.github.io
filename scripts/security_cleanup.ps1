param(
  [switch]$RunHistoryPurge,
  [string]$Branch = "main",
  [string]$Remote = "origin"
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Split-Path -Parent $PSScriptRoot)

Write-Host "== DMV Throwers security cleanup ==" -ForegroundColor Cyan

# Ensure sensitive paths stay ignored.
$gitignorePath = Join-Path $PWD ".gitignore"
$gitignore = Get-Content -Path $gitignorePath -Raw
if ($gitignore -notmatch "(?m)^dmvthrowers\.club-ssl-bundle/$") {
  Add-Content -Path $gitignorePath -Value "dmvthrowers.club-ssl-bundle/"
  Write-Host "Added dmvthrowers.club-ssl-bundle/ to .gitignore"
}
if ($gitignore -notmatch "(?m)^\.vs/$") {
  Add-Content -Path $gitignorePath -Value ".vs/"
  Write-Host "Added .vs/ to .gitignore"
}

# Remove tracked sensitive or unnecessary files from index.
$pathsToUntrack = @(
  "dmvthrowers.club-ssl-bundle",
  ".vs",
  ".github/workflows/fortify.yml",
  ".github/workflows/python-publish.yml",
  ".github/workflows/python-package-conda.yml",
  ".github/workflows/jscrambler-code-integrity.yml",
  ".github/workflows/powershell.yml",
  ".github/workflows/jekyll-docker.yml"
)

foreach ($p in $pathsToUntrack) {
  git rm -r --cached --ignore-unmatch -- $p | Out-Null
}

# Try to remove local copies too; if locked, leave and continue.
foreach ($p in @("dmvthrowers.club-ssl-bundle", ".github/workflows/fortify.yml", ".github/workflows/python-publish.yml", ".github/workflows/python-package-conda.yml", ".github/workflows/jscrambler-code-integrity.yml", ".github/workflows/powershell.yml", ".github/workflows/jekyll-docker.yml")) {
  try {
    if (Test-Path $p) {
      Remove-Item -Path $p -Recurse -Force
      Write-Host "Removed local path: $p"
    }
  } catch {
    Write-Warning "Could not remove local path (likely lock/OneDrive): $p"
  }
}

Write-Host "\nStaged changes:" -ForegroundColor Yellow
git status --short

Write-Host "\nIMPORTANT: Revoke and reissue TLS cert now. The old private key was exposed." -ForegroundColor Red

if (-not $RunHistoryPurge) {
  Write-Host "\nHistory purge not run. To run it, execute:" -ForegroundColor Yellow
  Write-Host "  .\\scripts\\security_cleanup.ps1 -RunHistoryPurge"
  exit 0
}

# Purge sensitive directory from full git history.
$filterRepo = Get-Command git-filter-repo -ErrorAction SilentlyContinue
if (-not $filterRepo) {
  throw "git-filter-repo is required. Install it first: pip install git-filter-repo"
}

Write-Host "\nRunning git-filter-repo..." -ForegroundColor Yellow
git filter-repo --path dmvthrowers.club-ssl-bundle/ --invert-paths --force

Write-Host "\nForce-pushing rewritten history..." -ForegroundColor Yellow
git push $Remote $Branch --force

Write-Host "\nDone. Notify collaborators to re-clone or hard reset." -ForegroundColor Green
