@echo off
:: Spotify Stats Backend - Uruchom w tle (ukryte okno)
:: Uruchamia backend + ngrok jako procesy w tle

echo ========================================
echo    Spotify Stats - Background Service
echo ========================================

:: Ścieżka do projektu (zmień jeśli potrzeba)
set PROJECT_DIR=%~dp0

:: Sprawdź czy venv istnieje
if not exist "%PROJECT_DIR%backend\venv\Scripts\python.exe" (
    echo [ERROR] Brak virtual environment!
    echo Uruchom najpierw: setup_backend.bat
    pause
    exit /b 1
)

:: Uruchom backend w tle (ukryte okno)
echo Uruchamiam backend w tle...
start /B /MIN "" "%PROJECT_DIR%backend\venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir "%PROJECT_DIR%backend"

:: Poczekaj aż backend wstanie
timeout /t 3 /nobreak >nul

:: Sprawdź czy ngrok jest zainstalowany
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] ngrok nie jest zainstalowany!
    echo Backend dziala na http://localhost:8000
    echo Zainstaluj ngrok aby uzyskac dostep zdalny.
    goto :end
)

:: Uruchom ngrok w tle
echo Uruchamiam ngrok w tle...
start /B /MIN "" ngrok http 8000 --log=stdout > "%PROJECT_DIR%ngrok.log" 2>&1

:: Poczekaj na ngrok
timeout /t 3 /nobreak >nul

:: Pobierz URL ngrok z API
echo.
echo Pobieram URL ngrok...
for /f "tokens=*" %%i in ('powershell -Command "(Invoke-WebRequest -Uri 'http://localhost:4040/api/tunnels' -UseBasicParsing | ConvertFrom-Json).tunnels[0].public_url"') do set NGROK_URL=%%i

if defined NGROK_URL (
    echo ========================================
    echo    BACKEND DZIALA W TLE!
    echo ========================================
    echo.
    echo URL ngrok: %NGROK_URL%
    echo.
    echo Wklej ten URL w ustawieniach aplikacji.
    echo.
    echo Aby zatrzymac: stop_background.bat
    echo ========================================
) else (
    echo [WARNING] Nie udalo sie pobrac URL ngrok
    echo Sprawdz ngrok.log lub http://localhost:4040
)

:end
echo.
echo Procesy dzialaja w tle. Mozesz zamknac to okno.
pause
