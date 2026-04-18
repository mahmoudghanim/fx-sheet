# FX Sheet Stock Dashboard Launcher
# This script starts the dashboard and opens it in your browser

$host.UI.RawTitle = "FX Sheet Dashboard"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FX Sheet Stock Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Pause
    exit 1
}

Write-Host "Starting dashboard server..." -ForegroundColor Yellow
Write-Host "Dashboard will open automatically in your browser" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start the server
python server.py

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Yellow
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
