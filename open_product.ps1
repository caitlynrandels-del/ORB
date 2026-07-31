$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\Scripts\python.exe"
$apiScript = Join-Path $root "api_server.py"
$webRoot = Join-Path $root "ORB"
$appUrl = "http://localhost:8000/App.html"

function Test-ListeningPort {
    param([int]$Port)
    return $null -ne (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue)
}

if (-not (Test-Path $python)) {
    Write-Host "Python runtime not found at $python"
    exit 1
}

if (-not (Test-ListeningPort -Port 8010)) {
    Start-Process -FilePath $python -ArgumentList "`"$apiScript`"" -WindowStyle Hidden | Out-Null
}

if (-not (Test-ListeningPort -Port 8000)) {
    Start-Process -FilePath $python -ArgumentList "-m", "http.server", "8000", "--directory", "`"$webRoot`"" -WindowStyle Hidden | Out-Null
}

$apiReady = $false
$webReady = $false
for ($i = 0; $i -lt 40; $i++) {
    if (-not $apiReady) {
        try {
            $resp = Invoke-RestMethod -Uri "http://127.0.0.1:8010/api/health" -Method Get -TimeoutSec 2
            if ($resp.ok -eq $true) { $apiReady = $true }
        } catch {}
    }
    if (-not $webReady) {
        $webReady = Test-ListeningPort -Port 8000
    }
    if ($apiReady -and $webReady) { break }
    Start-Sleep -Milliseconds 250
}

$edge = Get-Command "msedge" -ErrorAction SilentlyContinue
if ($edge) {
    Start-Process -FilePath $edge.Source -ArgumentList "--app=$appUrl", "--new-window" | Out-Null
} else {
    Start-Process $appUrl | Out-Null
}
