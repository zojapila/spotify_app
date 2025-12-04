@echo off
echo ========================================
echo    Spotify Stats - ngrok Tunnel
echo ========================================
echo.

REM Sprawdz czy ngrok jest zainstalowany
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] ngrok nie jest zainstalowany!
    echo.
    echo Instalacja:
    echo 1. Pobierz ngrok: https://ngrok.com/download
    echo 2. Rozpakuj i dodaj do PATH
    echo 3. Zaloguj sie: ngrok config add-authtoken YOUR_TOKEN
    echo.
    pause
    exit /b 1
)

echo Uruchamiam tunel ngrok na porcie 8000...
echo.
echo Po uruchomieniu skopiuj URL (np. https://xxxxx.ngrok.io)
echo i wklej go w ustawieniach aplikacji (ikona ⚙️)
echo.
echo ========================================

ngrok http 8000
