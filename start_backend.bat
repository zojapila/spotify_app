@echo off
title Spotify Stats - Backend Server
cd /d "D:\spotify_app\backend"
call venv\Scripts\activate
echo Starting Spotify Stats Backend...
echo.
echo Backend: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
