# Plan Działania - Spotify Stats App

## Przegląd projektu

**Cel**: Stworzenie aplikacji webowej do przeglądania statystyk Spotify z własnym systemem śledzenia odtworzeń.

**Timeline**: ~4-6 tygodni (w zależności od tempa pracy)

---

## Faza 1: Fundament (Tydzień 1)

### Sprint 1.1: Inicjalizacja projektu

#### Backend (Python/FastAPI)
- [ ] Utworzenie struktury projektu
- [ ] Konfiguracja virtual environment
- [ ] Instalacja zależności (FastAPI, SQLAlchemy, httpx, python-dotenv)
- [ ] Konfiguracja pytest
- [ ] Utworzenie pliku `.env` z placeholderami

#### Frontend (Next.js)
- [ ] Inicjalizacja projektu Next.js z TypeScript
- [ ] Konfiguracja Tailwind CSS
- [ ] Konfiguracja Jest + React Testing Library
- [ ] Utworzenie podstawowej struktury folderów
- [ ] Utworzenie pliku `.env.local` z placeholderami

#### DevOps
- [ ] Utworzenie `.gitignore`
- [ ] Utworzenie README.md z instrukcjami uruchomienia

### Sprint 1.2: Autentykacja Spotify OAuth

#### Backend
- [ ] Implementacja endpointu `/api/auth/login`
- [ ] Implementacja endpointu `/api/auth/callback`
- [ ] Implementacja endpointu `/api/auth/refresh`
- [ ] Implementacja endpointu `/api/auth/logout`
- [ ] Obsługa tokenów (JWT lub session)
- [ ] **Testy**: test_auth.py (minimum 5 testów)

#### Frontend
- [ ] Strona logowania z przyciskiem "Zaloguj przez Spotify"
- [ ] Obsługa callback i zapisanie sesji
- [ ] Komponent do wyświetlania stanu zalogowania
- [ ] **Testy**: Login.test.tsx

---

## Faza 2: Core Features (Tydzień 2-3)

### Sprint 2.1: Profil i Dashboard

#### Backend
- [ ] Implementacja endpointu `/api/spotify/me`
- [ ] Serwis do komunikacji ze Spotify API
- [ ] **Testy**: test_spotify.py (testy profilu)

#### Frontend
- [ ] Layout dashboardu z nawigacją
- [ ] Komponent profilu użytkownika
- [ ] Obsługa stanów loading/error
- [ ] **Testy**: Dashboard.test.tsx, UserProfile.test.tsx

### Sprint 2.2: Top Artyści

#### Backend
- [ ] Implementacja endpointu `/api/spotify/top/artists`
- [ ] Obsługa parametru `time_range`
- [ ] Cache'owanie odpowiedzi (opcjonalne)
- [ ] **Testy**: test_spotify.py (testy artystów)

#### Frontend
- [ ] Komponent TopArtists
- [ ] Komponent ArtistCard
- [ ] Przełącznik okresów (short/medium/long)
- [ ] **Testy**: TopArtists.test.tsx, ArtistCard.test.tsx

### Sprint 2.3: Top Utwory

#### Backend
- [ ] Implementacja endpointu `/api/spotify/top/tracks`
- [ ] Obsługa parametru `time_range`
- [ ] **Testy**: test_spotify.py (testy utworów)

#### Frontend
- [ ] Komponent TopTracks
- [ ] Komponent TrackCard
- [ ] Formatowanie czasu trwania
- [ ] **Testy**: TopTracks.test.tsx, TrackCard.test.tsx

---

## Faza 3: Rozszerzenia (Tydzień 3-4)

### Sprint 3.1: Top Albumy

#### Backend
- [ ] Implementacja endpointu `/api/spotify/top/albums`
- [ ] Logika wyliczania top albumów z top utworów
- [ ] **Testy**: test_spotify.py (testy albumów)

#### Frontend
- [ ] Komponent TopAlbums
- [ ] Komponent AlbumCard
- [ ] **Testy**: TopAlbums.test.tsx, AlbumCard.test.tsx

### Sprint 3.2: Historia słuchania

#### Backend
- [ ] Implementacja endpointu `/api/spotify/recently-played`
- [ ] **Testy**: test_spotify.py (testy historii)

#### Frontend
- [ ] Komponent RecentlyPlayed
- [ ] Formatowanie dat
- [ ] **Testy**: RecentlyPlayed.test.tsx

---

## Faza 4: Własny Tracking (Tydzień 4-5)

### Sprint 4.1: Baza danych i modele

#### Backend
- [ ] Konfiguracja SQLite + SQLAlchemy
- [ ] Model ListeningSession
- [ ] Migracje bazy danych
- [ ] **Testy**: test_models.py

### Sprint 4.2: Tracking Service

#### Backend
- [ ] Implementacja endpointu `/api/tracking/record`
- [ ] Implementacja endpointu `/api/tracking/stats`
- [ ] Implementacja endpointu `/api/tracking/history`
- [ ] Logika wykrywania duplikatów
- [ ] **Testy**: test_tracking.py (minimum 5 testów)

### Sprint 4.3: Frontend Tracking

#### Frontend
- [ ] Hook useTracker do automatycznego śledzenia
- [ ] Komponent StatsOverview (liczba odtworzeń, łączny czas)
- [ ] Komponent TrackingHistory
- [ ] **Testy**: useTracker.test.ts, StatsOverview.test.tsx

---

## Faza 5: Polish (Tydzień 5-6)

### Sprint 5.1: UI/UX

- [ ] Responsywny design (mobile-first)
- [ ] Skeleton loading states
- [ ] Animacje i transitions
- [ ] Tryb ciemny/jasny
- [ ] **Testy**: Testy responsywności

### Sprint 5.2: Finalizacja

- [ ] Code review i refactoring
- [ ] Uzupełnienie dokumentacji
- [ ] Testy end-to-end (opcjonalne)
- [ ] Przegląd pokrycia testami (cel: 80%)
- [ ] README z instrukcją uruchomienia

---

## Definicja ukończenia (Definition of Done)

Każda funkcjonalność jest ukończona gdy:

1. ✅ Kod jest napisany zgodnie z konwencjami
2. ✅ Są napisane testy jednostkowe (min. pokrycie 80%)
3. ✅ Testy przechodzą
4. ✅ Kod jest sformatowany (Black/Prettier)
5. ✅ Brak błędów lintingu
6. ✅ Dokumentacja jest aktualna

---

## Techniczne wymagania

### Backend (Python)
```
fastapi>=0.104.0
uvicorn>=0.24.0
sqlalchemy>=2.0.0
httpx>=0.25.0
python-dotenv>=1.0.0
python-jose[cryptography]>=3.3.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
black>=23.0.0
isort>=5.12.0
ruff>=0.1.0
```

### Frontend (Next.js)
```
next: 14+
react: 18+
typescript: 5+
tailwindcss: 3+
jest: 29+
@testing-library/react: 14+
@testing-library/jest-dom: 6+
```

---

## Ryzyka i mitigacje

| Ryzyko | Prawdopodobieństwo | Wpływ | Mitigacja |
|--------|-------------------|-------|-----------|
| Rate limiting Spotify API | Średnie | Wysoki | Implementacja cache |
| Token expiration issues | Średnie | Wysoki | Automatyczny refresh token |
| Brak danych dla nowego użytkownika | Niskie | Niski | Obsługa pustych stanów |
| Problemy z CORS | Średnie | Średni | Prawidłowa konfiguracja FastAPI |

---

## Kamienie milowe

1. **M1**: Backend + Frontend działa, użytkownik może się zalogować ✨
2. **M2**: Dashboard z top artystami i utworami 🎵
3. **M3**: Top albumy i historia słuchania 📊
4. **M4**: Własny tracking działa i zbiera dane 📈
5. **M5**: Aplikacja jest dopracowana i przetestowana 🚀

---

## Następne kroki

1. Utworzenie konta deweloperskiego na [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Utworzenie aplikacji i pobranie Client ID/Secret
3. Skonfigurowanie Redirect URI
4. Rozpoczęcie implementacji zgodnie z planem
