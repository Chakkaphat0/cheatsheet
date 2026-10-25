param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Path,
    [string]$OutDir = ""
)

$ErrorActionPreference = "Stop"
$resolved = (Resolve-Path -LiteralPath $Path).Path

if (-not $OutDir) {
    $safeName = [IO.Path]::GetFileName($resolved) -replace '[^A-Za-z0-9._-]', '_'
    $OutDir = Join-Path (Get-Location) ("triage_" + $safeName)
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$report = Join-Path $OutDir "report.txt"

function Add-Section([string]$Title, [scriptblock]$Action) {
    "`n=== $Title ===" | Tee-Object -FilePath $report -Append
    try {
        (& $Action 2>&1 | Out-String).TrimEnd() | Tee-Object -FilePath $report -Append
    }
    catch {
        ("[!] " + $_.Exception.Message) | Tee-Object -FilePath $report -Append
    }
}

"Target: $resolved" | Set-Content -LiteralPath $report
"UTC: $([DateTime]::UtcNow.ToString('u'))" | Add-Content -LiteralPath $report

Add-Section "Basic" {
    Get-Item -LiteralPath $resolved | Select-Object FullName, Length, CreationTimeUtc, LastWriteTimeUtc
    Get-FileHash -LiteralPath $resolved -Algorithm SHA256
}

Add-Section "First 128 bytes" {
    Format-Hex -LiteralPath $resolved -Count 128
}

foreach ($tool in @("file", "exiftool", "strings", "binwalk", "pngcheck", "7z")) {
    $cmd = Get-Command $tool -ErrorAction SilentlyContinue
    if (-not $cmd) {
        "`n=== $tool ===`n[skip] not found in PATH" | Add-Content -LiteralPath $report
        continue
    }

    switch ($tool) {
        "strings"  { Add-Section "strings"  { & $cmd.Source -n 5 -- $resolved } }
        "binwalk"  { Add-Section "binwalk"  { & $cmd.Source $resolved } }
        "pngcheck" { Add-Section "pngcheck" { & $cmd.Source -vt $resolved } }
        "7z"       { Add-Section "7z list"  { & $cmd.Source l -- $resolved } }
        default    { Add-Section $tool       { & $cmd.Source $resolved } }
    }
}

Write-Host "Triage report: $report"

