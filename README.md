# 🎵 Spotify Stats App

Aplikacja webowa do przeglądania statystyk Spotify - top artyści, utwory, albumy oraz śledzenie historii słuchania.

## 📋 Wymagania

- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **Konto Spotify** z aplikacją w [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## 🚀 Szybki start

### 1. Konfiguracja Spotify Developer

1. Wejdź na [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Utwórz nową aplikację
3. Dodaj Redirect URI: `http://localhost:8000/api/auth/callback`
4. Skopiuj **Client ID** i **Client Secret**

### 2. Backend (Python/FastAPI)

```powershell
# Przejdź do folderu backend
cd backend

# Utwórz virtual environment
python -m venv venv

# Aktywuj virtual environment
.\venv\Scripts\activate

# Zainstaluj zależności
pip install -r requirements.txt

# Skonfiguruj .env (już utworzony, sprawdź dane)
# Upewnij się, że SPOTIFY_CLIENT_ID i SPOTIFY_CLIENT_SECRET są poprawne

# Uruchom serwer
uvicorn app.main:app --reload --port 8000
```

Backend będzie dostępny pod: http://localhost:8000
Dokumentacja API: http://localhost:8000/docs

### 3. Frontend (Next.js)

```powershell
# W nowym terminalu, przejdź do folderu frontend
cd frontend

# Zainstaluj zależności
npm install

# Uruchom serwer deweloperski
npm run dev
```

Frontend będzie dostępny pod: http://localhost:3000

### 4. Używanie aplikacji

1. Otwórz http://localhost:3000
2. Kliknij "Zaloguj przez Spotify"
3. Zaloguj się na swoje konto Spotify
4. Przeglądaj swoje statystyki! 🎉

## 📁 Struktura projektu

```
spotify_app/
├── backend/                # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py        # Entry point
│   │   ├── config.py      # Konfiguracja
│   │   ├── database.py    # SQLAlchemy setup
│   │   ├── routers/       # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── models/        # SQLAlchemy models
│   │   └── schemas/       # Pydantic schemas
│   ├── tests/             # Testy pytest
│   └── requirements.txt
│
├── frontend/              # Next.js Frontend
│   ├── src/
│   │   ├── app/          # Next.js App Router
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities
│   │   └── types/        # TypeScript types
│   └── package.json
│
└── docs/                  # Dokumentacja
    ├── USER_STORIES.md
    ├── PLAN.md
    └── API.md
```

## 🧪 Testy

### Backend
```powershell
cd backend
.\venv\Scripts\activate
pytest
pytest --cov=app --cov-report=html  # z coverage
```

### Frontend
```powershell
cd frontend
npm run test
npm run test:coverage  # z coverage
```

## 📊 Funkcjonalności

- ✅ Logowanie przez Spotify OAuth 2.0
- ✅ Wyświetlanie profilu użytkownika
- ✅ Top 20 artystów (ostatni miesiąc / 6 miesięcy / wszystkie czasy)
- ✅ Top 20 utworów (różne okresy)
- ✅ Top 20 albumów (wyliczone z utworów)
- ✅ Ostatnio słuchane utwory
- 🚧 Własny tracking odtworzeń (w przygotowaniu)
- 🚧 Statystyki łącznego czasu słuchania (w przygotowaniu)

## 🔧 Zmienne środowiskowe

### Backend (.env)
```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/api/auth/callback
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite+aiosqlite:///./spotify_stats.db
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 Licencja

MIT
