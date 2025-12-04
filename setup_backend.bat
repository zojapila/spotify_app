@echo off
:: Pierwsza instalacja backendu na nowym komputerze

echo ========================================
echo    Spotify Stats - Setup Backend
echo ========================================
echo.

set PROJECT_DIR=%~dp0

:: Sprawdź Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python nie jest zainstalowany!
    echo Pobierz z: https://www.python.org/downloads/
    pause
    exit /b 1
)

cd "%PROJECT_DIR%backend"

:: Utwórz venv jeśli nie istnieje
if not exist "venv" (
    echo Tworzę virtual environment...
    python -m venv venv
)

:: Aktywuj i zainstaluj zależności
echo Instaluję zależności...
call venv\Scripts\activate.bat
pip install -r requirements.txt

:: Sprawdź .env
if not exist ".env" (
    echo.
    echo [UWAGA] Brak pliku .env!
    echo Tworzę szablon...
    (
        echo # Spotify API Credentials
        echo SPOTIFY_CLIENT_ID=539e52fb1f92436d9d662f5292efb451
        echo SPOTIFY_CLIENT_SECRET=78032785af4b40a590afee9cda10a563
        echo SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/api/auth/callback
        echo.
        echo # App Settings
        echo SECRET_KEY=your-super-secret-key-change-this-in-production-1234567890
        echo DATABASE_URL=sqlite+aiosqlite:///./spotify_stats.db
        echo.
        echo # Frontend URL ^(Vercel^)
        echo FRONTEND_URL=https://twoja-apka.vercel.app
    ) > .env
    echo.
    echo Plik .env utworzony!
    echo EDYTUJ backend\.env i ustaw FRONTEND_URL na URL Twojej apki Vercel.
)

echo.
echo ========================================
echo    Setup zakończony!
echo ========================================
echo.
echo Następne kroki:
echo 1. Edytuj backend\.env (ustaw FRONTEND_URL)
echo 2. Zainstaluj ngrok: https://ngrok.com/download
echo 3. Skonfiguruj ngrok: ngrok config add-authtoken TWOJ_TOKEN
echo 4. Uruchom: start_background.bat
echo.
pause
