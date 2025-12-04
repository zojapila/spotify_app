@echo off
title Spotify Stats
echo ========================================
echo    Spotify Stats App
echo ========================================
echo.
echo Starting servers...
echo.

:: Start backend in background
start "Spotify Stats Backend" cmd /k "cd /d D:\spotify_app\backend && venv\Scripts\activate && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

:: Wait a bit for backend to start
timeout /t 3 /nobreak > nul

:: Start frontend in background
start "Spotify Stats Frontend" cmd /k "cd /d D:\spotify_app\frontend && npm run dev"

echo.
echo ========================================
echo Servers starting...
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:3000
echo API Docs: http://127.0.0.1:8000/docs
echo ========================================
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak > nul

:: Open browser
start http://127.0.0.1:3000

echo.
echo Press any key to close this window (servers will keep running)
pause > nul
