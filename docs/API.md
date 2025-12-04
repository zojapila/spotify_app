# API Documentation - Spotify Stats App

## Przegląd

Backend API zbudowane w FastAPI, udostępniające endpointy do:
- Autentykacji przez Spotify OAuth 2.0
- Pobierania danych ze Spotify API
- Własnego systemu trackingu odtworzeń

**Base URL**: `http://localhost:8000`

---

## Autentykacja

### GET /api/auth/login

Inicjuje proces logowania przez Spotify OAuth.

**Odpowiedź**: Redirect do Spotify authorization page

**Przykład**:
```
GET /api/auth/login
→ Redirect to https://accounts.spotify.com/authorize?...
```

---

### GET /api/auth/callback

Endpoint callback dla Spotify OAuth. Spotify przekierowuje tutaj po zalogowaniu.

**Query Parameters**:
| Parametr | Typ | Opis |
|----------|-----|------|
| code | string | Authorization code od Spotify |
| state | string | State parameter dla weryfikacji |
| error | string | (opcjonalne) Błąd autoryzacji |

**Odpowiedź**: Redirect do frontend z tokenem w cookie lub query param

**Przykład**:
```
GET /api/auth/callback?code=AQD...&state=xyz123
→ Redirect to http://localhost:3000/dashboard
```

---

### POST /api/auth/refresh

Odświeża access token używając refresh token.

**Headers**:
```
Authorization: Bearer <refresh_token>
```

**Odpowiedź** (200 OK):
```json
{
  "access_token": "BQD...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Błędy**:
- 401 Unauthorized - Invalid refresh token

---

### POST /api/auth/logout

Wylogowuje użytkownika i unieważnia sesję.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Odpowiedź** (200 OK):
```json
{
  "message": "Successfully logged out"
}
```

---

## Spotify Data

Wszystkie endpointy wymagają nagłówka Authorization:
```
Authorization: Bearer <spotify_access_token>
```

---

### GET /api/spotify/me

Pobiera profil aktualnie zalogowanego użytkownika.

**Odpowiedź** (200 OK):
```json
{
  "id": "user123",
  "display_name": "Jan Kowalski",
  "email": "jan@example.com",
  "images": [
    {
      "url": "https://i.scdn.co/image/...",
      "height": 300,
      "width": 300
    }
  ],
  "product": "premium",
  "followers": {
    "total": 42
  }
}
```

---

### GET /api/spotify/top/artists

Pobiera top artystów użytkownika.

**Query Parameters**:
| Parametr | Typ | Domyślnie | Opis |
|----------|-----|-----------|------|
| time_range | string | medium_term | short_term, medium_term, long_term |
| limit | integer | 20 | 1-50 |
| offset | integer | 0 | Pagination offset |

**Przykład**:
```
GET /api/spotify/top/artists?time_range=short_term&limit=10
```

**Odpowiedź** (200 OK):
```json
{
  "items": [
    {
      "id": "artist123",
      "name": "Arctic Monkeys",
      "genres": ["rock", "indie rock"],
      "popularity": 85,
      "images": [
        {
          "url": "https://i.scdn.co/image/...",
          "height": 640,
          "width": 640
        }
      ],
      "external_urls": {
        "spotify": "https://open.spotify.com/artist/..."
      }
    }
  ],
  "total": 50,
  "limit": 10,
  "offset": 0,
  "time_range": "short_term"
}
```

---

### GET /api/spotify/top/tracks

Pobiera top utwory użytkownika.

**Query Parameters**:
| Parametr | Typ | Domyślnie | Opis |
|----------|-----|-----------|------|
| time_range | string | medium_term | short_term, medium_term, long_term |
| limit | integer | 20 | 1-50 |
| offset | integer | 0 | Pagination offset |

**Przykład**:
```
GET /api/spotify/top/tracks?time_range=long_term&limit=20
```

**Odpowiedź** (200 OK):
```json
{
  "items": [
    {
      "id": "track123",
      "name": "Do I Wanna Know?",
      "duration_ms": 272000,
      "popularity": 88,
      "album": {
        "id": "album123",
        "name": "AM",
        "images": [
          {
            "url": "https://i.scdn.co/image/...",
            "height": 640,
            "width": 640
          }
        ]
      },
      "artists": [
        {
          "id": "artist123",
          "name": "Arctic Monkeys"
        }
      ],
      "external_urls": {
        "spotify": "https://open.spotify.com/track/..."
      }
    }
  ],
  "total": 50,
  "limit": 20,
  "offset": 0,
  "time_range": "long_term"
}
```

---

### GET /api/spotify/top/albums

Pobiera top albumy użytkownika (wyliczone z top utworów).

**Query Parameters**:
| Parametr | Typ | Domyślnie | Opis |
|----------|-----|-----------|------|
| time_range | string | medium_term | short_term, medium_term, long_term |
| limit | integer | 20 | 1-50 |

**Przykład**:
```
GET /api/spotify/top/albums?time_range=medium_term&limit=10
```

**Odpowiedź** (200 OK):
```json
{
  "items": [
    {
      "id": "album123",
      "name": "AM",
      "artists": [
        {
          "id": "artist123",
          "name": "Arctic Monkeys"
        }
      ],
      "images": [
        {
          "url": "https://i.scdn.co/image/...",
          "height": 640,
          "width": 640
        }
      ],
      "release_date": "2013-09-09",
      "total_tracks": 12,
      "track_count_in_top": 5,
      "external_urls": {
        "spotify": "https://open.spotify.com/album/..."
      }
    }
  ],
  "total": 15,
  "limit": 10,
  "time_range": "medium_term"
}
```

---

### GET /api/spotify/recently-played

Pobiera ostatnio słuchane utwory.

**Query Parameters**:
| Parametr | Typ | Domyślnie | Opis |
|----------|-----|-----------|------|
| limit | integer | 20 | 1-50 |

**Przykład**:
```
GET /api/spotify/recently-played?limit=50
```

**Odpowiedź** (200 OK):
```json
{
  "items": [
    {
      "track": {
        "id": "track123",
        "name": "Do I Wanna Know?",
        "duration_ms": 272000,
        "album": {
          "id": "album123",
          "name": "AM",
          "images": [...]
        },
        "artists": [
          {
            "id": "artist123",
            "name": "Arctic Monkeys"
          }
        ]
      },
      "played_at": "2024-01-15T14:30:00Z"
    }
  ],
  "total": 50
}
```

---

## Tracking (Własne statystyki)

### POST /api/tracking/record

Zapisuje odsłuchanie utworu do własnej bazy danych.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Body**:
```json
{
  "track_id": "track123",
  "track_name": "Do I Wanna Know?",
  "artist_name": "Arctic Monkeys",
  "album_name": "AM",
  "duration_ms": 272000
}
```

**Odpowiedź** (201 Created):
```json
{
  "id": 1,
  "message": "Listening session recorded"
}
```

**Odpowiedź** (200 OK - duplikat):
```json
{
  "message": "Duplicate play detected, skipped"
}
```

---

### GET /api/tracking/stats

Pobiera statystyki użytkownika z własnej bazy.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Query Parameters**:
| Parametr | Typ | Domyślnie | Opis |
|----------|-----|-----------|------|
| days | integer | 30 | Okres w dniach (0 = wszystko) |

**Przykład**:
```
GET /api/tracking/stats?days=7
```

**Odpowiedź** (200 OK):
```json
{
  "period_days": 7,
  "total_plays": 156,
  "total_time_ms": 28800000,
  "total_time_formatted": "8h 0m",
  "unique_tracks": 45,
  "unique_artists": 23,
  "unique_albums": 30,
  "average_daily_time_ms": 4114285,
  "average_daily_time_formatted": "1h 8m",
  "top_tracks": [
    {
      "track_id": "track123",
      "track_name": "Do I Wanna Know?",
      "artist_name": "Arctic Monkeys",
      "play_count": 12
    }
  ],
  "top_artists": [
    {
      "artist_name": "Arctic Monkeys",
      "play_count": 45
    }
  ]
}
```

---

### GET /api/tracking/history

Pobiera historię słuchania z własnej bazy.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Query Parameters**:
| Parametr | Typ | Domyślnie | Opis |
|----------|-----|-----------|------|
| days | integer | 30 | Okres w dniach |
| limit | integer | 100 | Maksymalna liczba rekordów |
| offset | integer | 0 | Pagination offset |

**Przykład**:
```
GET /api/tracking/history?days=7&limit=50
```

**Odpowiedź** (200 OK):
```json
{
  "items": [
    {
      "id": 1,
      "track_id": "track123",
      "track_name": "Do I Wanna Know?",
      "artist_name": "Arctic Monkeys",
      "album_name": "AM",
      "duration_ms": 272000,
      "played_at": "2024-01-15T14:30:00Z"
    }
  ],
  "total": 156,
  "limit": 50,
  "offset": 0
}
```

---

## Kody błędów

| Kod | Opis |
|-----|------|
| 200 | OK - Sukces |
| 201 | Created - Zasób utworzony |
| 400 | Bad Request - Nieprawidłowe parametry |
| 401 | Unauthorized - Brak lub nieprawidłowy token |
| 403 | Forbidden - Brak uprawnień |
| 404 | Not Found - Zasób nie znaleziony |
| 429 | Too Many Requests - Rate limit |
| 500 | Internal Server Error - Błąd serwera |

**Format błędu**:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting

- Spotify API ma własne limity (zazwyczaj 100+ req/min)
- Nasz backend implementuje cache dla często używanych endpointów
- Przy błędzie 429 od Spotify, czekaj czas z nagłówka `Retry-After`

---

## Przykłady użycia (cURL)

### Logowanie
```bash
# Otwórz w przeglądarce:
curl -X GET "http://localhost:8000/api/auth/login"
```

### Pobranie profilu
```bash
curl -X GET "http://localhost:8000/api/spotify/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Pobranie top artystów
```bash
curl -X GET "http://localhost:8000/api/spotify/top/artists?time_range=short_term&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Zapisanie odsłuchania
```bash
curl -X POST "http://localhost:8000/api/tracking/record" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "track_id": "track123",
    "track_name": "Do I Wanna Know?",
    "artist_name": "Arctic Monkeys",
    "album_name": "AM",
    "duration_ms": 272000
  }'
```
