# Spotify Stats - Autostart Setup Script
# Run this script as Administrator to add Spotify Stats to Windows startup

$taskName = "SpotifyStatsBackend"
$backendPath = "D:\spotify_app\backend"
$pythonPath = "D:\spotify_app\backend\venv\Scripts\python.exe"

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Please run this script as Administrator!" -ForegroundColor Red
    Write-Host "Right-click on PowerShell and select 'Run as Administrator'"
    pause
    exit
}

Write-Host "======================================" -ForegroundColor Green
Write-Host "  Spotify Stats - Autostart Setup" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Remove existing task if exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the action
$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument "-m uvicorn app.main:app --host 127.0.0.1 --port 8000" `
    -WorkingDirectory $backendPath

# Create the trigger (at logon)
$trigger = New-ScheduledTaskTrigger -AtLogon

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Create the task
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Spotify Stats Backend - Automatic tracking server"

Write-Host ""
Write-Host "Task '$taskName' created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "The backend server will now start automatically when you log in." -ForegroundColor Cyan
Write-Host ""
Write-Host "To disable autostart, run:" -ForegroundColor Yellow
Write-Host "  Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false" -ForegroundColor Gray
Write-Host ""
Write-Host "To start the task manually:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
Write-Host ""

# Ask if user wants to start the task now
$response = Read-Host "Do you want to start the backend now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Start-ScheduledTask -TaskName $taskName
    Write-Host "Backend started!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
pause
