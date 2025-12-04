# Copilot Instructions - Spotify Stats App

## Opis projektu
Aplikacja webowa do przeglądania statystyk Spotify użytkownika. Umożliwia wyświetlanie top artystów, utworów, albumów oraz śledzenie historii słuchania w czasie rzeczywistym.

## Stack technologiczny
- **Frontend**: Next.js 14+ (App Router) z TypeScript
- **Backend**: Python 3.11+ (FastAPI)
- **Stylowanie**: Tailwind CSS
- **Baza danych**: SQLite (SQLAlchemy ORM) do lokalnego trackingu
- **Testy Frontend**: Jest + React Testing Library
- **Testy Backend**: pytest + pytest-asyncio
- **API**: Spotify Web API

## Struktura projektu
```
spotify_app/
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   │   ├── dashboard/     # Strona główna dashboardu
│   │   │   ├── login/         # Strona logowania
│   │   │   └── layout.tsx     # Root layout
│   │   ├── components/        # Komponenty React
│   │   │   ├── ui/           # Reużywalne komponenty UI
│   │   │   ├── dashboard/    # Komponenty dashboardu
│   │   │   └── charts/       # Komponenty wykresów
│   │   ├── lib/              # Utilities
│   │   ├── hooks/            # Custom React hooks
│   │   ├── types/            # TypeScript types/interfaces
│   │   └── __tests__/        # Testy frontend
│   ├── public/               # Static assets
│   └── package.json
│
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── config.py         # Konfiguracja i env variables
│   │   ├── routers/          # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py       # Spotify OAuth endpoints
│   │   │   ├── spotify.py    # Spotify data endpoints
│   │   │   └── tracking.py   # Własny tracking endpoint
│   │   ├── services/         # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── spotify_service.py
│   │   │   └── tracking_service.py
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   └── listening_session.py
│   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── spotify.py
│   │   │   └── tracking.py
│   │   └── database.py       # Database connection
│   ├── tests/                # Testy backend
│   │   ├── __init__.py
│   │   ├── conftest.py       # pytest fixtures
│   │   ├── test_auth.py
│   │   ├── test_spotify.py
│   │   └── test_tracking.py
│   ├── requirements.txt
│   └── pytest.ini
│
└── docs/                      # Dokumentacja
    ├── USER_STORIES.md
    ├── PLAN.md
    └── API.md
```

## Konwencje kodowania

### Python (Backend)
- Używaj type hints wszędzie
- Formatowanie: Black + isort
- Linting: ruff
- Async/await dla operacji I/O
- Pydantic do walidacji danych
- Docstrings dla funkcji publicznych

### TypeScript (Frontend)
- Używaj strict mode
- Definiuj interfejsy dla wszystkich obiektów API
- Unikaj `any` - używaj `unknown` jeśli typ nieznany
- Eksportuj typy z dedykowanych plików w `types/`

### React/Next.js
- Używaj Server Components gdzie możliwe
- Client Components oznaczaj `'use client'`
- Używaj `async/await` w Server Components
- Obsługuj stany loading i error

### Nazewnictwo

#### Python:
- Moduły: snake_case (`spotify_service.py`)
- Klasy: PascalCase (`ListeningSession`)
- Funkcje/zmienne: snake_case (`get_top_artists`)
- Stałe: UPPER_SNAKE_CASE (`SPOTIFY_API_URL`)

#### TypeScript:
- Komponenty: PascalCase (`TopArtists.tsx`)
- Hooki: camelCase z prefixem `use` (`useSpotifyData.ts`)
- Utilities: camelCase (`formatDuration.ts`)
- Typy/Interfejsy: PascalCase z prefixem `I` dla interfejsów (`ITrack`, `IArtist`)

### Testy

#### Backend (pytest):
- Pliki testowe: `test_*.py`
- Używaj fixtures w `conftest.py`
- Mockuj zewnętrzne API (responses, unittest.mock)
- Testuj: endpoints, services, edge cases
- Pokrycie kodu: minimum 80%

#### Frontend (Jest):
- Pliki testowe: `*.test.tsx`
- Mockuj API calls
- Testuj: renderowanie, interakcje, stany
- Pokrycie kodu: minimum 80%

## Spotify API

### Endpointy których używamy:
- `GET /me` - profil użytkownika
- `GET /me/top/artists` - top artyści
- `GET /me/top/tracks` - top utwory
- `GET /me/player/recently-played` - ostatnio słuchane
- `GET /me/player/currently-playing` - obecnie grany utwór (do trackingu)

### Time ranges dla top items:
- `short_term` - ostatnie ~4 tygodnie
- `medium_term` - ostatnie ~6 miesięcy
- `long_term` - wszystkie dane

### Rate limiting:
- Spotify ma limity requestów
- Implementuj cache gdzie możliwe (in-memory lub Redis)
- Używaj exponential backoff przy błędach 429

## Baza danych - schemat trackingu (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base

class ListeningSession(Base):
    __tablename__ = "listening_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    track_id = Column(String, nullable=False, index=True)
    track_name = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)
    album_name = Column(String, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    played_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index('idx_user_played', 'user_id', 'played_at'),
    )
```

## Zmienne środowiskowe

### Backend (.env)
```env
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=http://localhost:8000/api/auth/callback
SECRET_KEY=your-secret-key-for-jwt
DATABASE_URL=sqlite:///./spotify_stats.db
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Ważne uwagi

1. **Bezpieczeństwo**: Nigdy nie eksponuj client_secret po stronie klienta
2. **Tokeny**: Access token wygasa po 1h - implementuj refresh token flow
3. **Scopes**: Wymagane scopes: `user-read-private`, `user-read-email`, `user-top-read`, `user-read-recently-played`, `user-read-currently-playing`
4. **CORS**: Skonfiguruj CORS w FastAPI dla frontend URL

## Komendy

### Backend
```bash
# Utworzenie virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Instalacja zależności
pip install -r requirements.txt

# Development
uvicorn app.main:app --reload --port 8000

# Testy
pytest
pytest --cov=app --cov-report=html

# Formatowanie
black app/
isort app/
ruff check app/
```

### Frontend
```bash
# Instalacja zależności
npm install

# Development
npm run dev

# Testy
npm run test
npm run test:watch
npm run test:coverage

# Build
npm run build

# Lint
npm run lint
```

## API Endpoints (Backend)

### Auth
- `GET /api/auth/login` - Redirect do Spotify OAuth
- `GET /api/auth/callback` - Callback z Spotify
- `POST /api/auth/refresh` - Odświeżenie tokenu
- `POST /api/auth/logout` - Wylogowanie

### Spotify Data
- `GET /api/spotify/me` - Profil użytkownika
- `GET /api/spotify/top/artists?time_range=medium_term&limit=20` - Top artyści
- `GET /api/spotify/top/tracks?time_range=medium_term&limit=20` - Top utwory
- `GET /api/spotify/top/albums?time_range=medium_term&limit=20` - Top albumy (wyliczone)
- `GET /api/spotify/recently-played?limit=50` - Ostatnio słuchane

### Tracking
- `GET /api/tracking/stats` - Statystyki użytkownika z własnej bazy
- `GET /api/tracking/history?days=30` - Historia słuchania
- `POST /api/tracking/record` - Zapisz odsłuchanie (wywoływane przez tracker)
