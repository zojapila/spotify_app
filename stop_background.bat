@echo off
:: Zatrzymaj backend + ngrok działające w tle

echo ========================================
echo    Zatrzymywanie Spotify Stats...
echo ========================================

:: Zabij proces uvicorn/python
echo Zatrzymuję backend...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1

:: Zabij ngrok
echo Zatrzymuję ngrok...
taskkill /F /IM ngrok.exe >nul 2>&1

echo.
echo ========================================
echo    Wszystkie procesy zatrzymane!
echo ========================================
pause
