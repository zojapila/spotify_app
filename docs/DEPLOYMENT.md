# Wdrożenie Spotify Stats na Vercel + ngrok

## Przegląd architektury

```
┌─────────────────────────────────────────────────────────────┐
│                    TWÓJ KOMPUTER                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Backend   │◄───│   ngrok     │◄───│   Internet  │◄────┼────┐
│  │  (FastAPI)  │    │   Tunnel    │    │             │     │    │
│  │  port 8000  │    │             │    │             │     │    │
│  └─────────────┘    └─────────────┘    └─────────────┘     │    │
└─────────────────────────────────────────────────────────────┘    │
                                                                   │
                                                                   │
┌─────────────────────────────────────────────────────────────┐    │
│                     VERCEL                                   │    │
│  ┌─────────────────────────────────────────────────────┐    │    │
│  │                  Frontend (Next.js)                  │────┼────┘
│  │              twoja-apka.vercel.app                   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Krok 1: Instalacja ngrok

1. **Pobierz ngrok**: https://ngrok.com/download
2. **Utwórz konto** (darmowe): https://dashboard.ngrok.com/signup
3. **Skopiuj authtoken** z dashboardu ngrok
4. **Skonfiguruj ngrok**:
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

## Krok 2: Wdrożenie na Vercel

### Opcja A: Przez Vercel CLI

1. **Zainstaluj Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Przejdź do folderu frontend**:
   ```bash
   cd frontend
   ```

3. **Wdróż**:
   ```bash
   vercel
   ```

4. **Postępuj zgodnie z instrukcjami**:
   - Zaloguj się do Vercel
   - Wybierz/utwórz projekt
   - Potwierdź ustawienia

### Opcja B: Przez GitHub

1. **Wypchnij kod na GitHub**
2. **Zaloguj się do Vercel**: https://vercel.com
3. **Kliknij "New Project"**
4. **Importuj repozytorium z GitHub**
5. **Skonfiguruj**:
   - Root Directory: `frontend`
   - Framework: Next.js (automatyczne wykrycie)
6. **Kliknij "Deploy"**

### Konfiguracja zmiennych środowiskowych na Vercel

W ustawieniach projektu na Vercel → Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> **Uwaga**: Ta wartość jest tylko domyślna. Prawdziwy URL API (ngrok) 
> będzie ustawiany przez użytkownika w aplikacji.

## Krok 3: Codzienna konfiguracja

### Na komputerze (jednorazowo przy starcie):

1. **Uruchom backend**:
   ```bash
   start_backend.bat
   ```
   
2. **Uruchom ngrok**:
   ```bash
   start_ngrok.bat
   ```
   
3. **Skopiuj URL ngrok** (np. `https://a1b2c3d4.ngrok.io`)

### Na telefonie/tablecie/innym urządzeniu:

1. **Otwórz aplikację**: `https://twoja-apka.vercel.app`
2. **Kliknij ⚙️ Ustawienia**
3. **Wklej URL ngrok** (np. `https://a1b2c3d4.ngrok.io`)
4. **Kliknij "Testuj połączenie"**
5. **Zaloguj się przez Spotify**

## Ważne uwagi

### URL ngrok się zmienia
- Darmowe konto ngrok = nowy URL przy każdym uruchomieniu
- **Rozwiązanie 1**: Płatny plan ngrok (~$8/mies) = stały subdomain
- **Rozwiązanie 2**: Za każdym razem aktualizuj URL w ustawieniach

### Problemy z logowaniem Spotify
Jeśli logowanie przez Spotify nie działa z ngrok:

1. **Zaktualizuj Redirect URI w Spotify Dashboard**:
   - Idź do: https://developer.spotify.com/dashboard
   - Wybierz aplikację
   - Dodaj redirect URI: `https://TWOJ-NGROK-URL.ngrok.io/api/auth/callback`

2. **Lub użyj ngrok z własną domeną** (płatny plan)

### Bezpieczeństwo
- ngrok URL jest publiczny - każdy z linkiem może się połączyć
- Rozważ włączenie Basic Auth w ngrok:
  ```bash
  ngrok http 8000 --basic-auth="user:haslo"
  ```

### Automatyzacja (opcjonalne)

#### Stały URL z ngrok (płatny plan)
```bash
ngrok http 8000 --subdomain=spotify-stats
```
URL zawsze: `https://spotify-stats.ngrok.io`

#### Skrypt all-in-one
Utwórz `start_all_remote.bat`:
```batch
@echo off
start cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 5
start cmd /k "ngrok http 8000"
```

## Troubleshooting

### "Nie można połączyć z backendem"
- Sprawdź czy backend działa: `http://localhost:8000/docs`
- Sprawdź czy ngrok działa i skopiowałeś poprawny URL
- Upewnij się, że URL w ustawieniach NIE ma `/` na końcu

### "CORS error"
- Backend jest skonfigurowany do akceptowania wszystkich origin
- Jeśli problem: sprawdź `backend/app/main.py` → CORS middleware

### "Token wygasł"
- Zaloguj się ponownie przez Spotify
- Backend automatycznie odświeża tokeny

### ngrok pokazuje "Tunnel not found"
- ngrok został wyłączony lub utracił połączenie
- Uruchom ponownie `start_ngrok.bat`

## Limity darmowego planu ngrok

- 1 aktywny tunel
- ~40 połączeń/minutę
- URL zmienia się przy każdym uruchomieniu
- Brak własnej domeny

Dla codziennego użytku **wystarczy darmowy plan**.
