# User Stories - Spotify Stats App

## Epik 1: Autentykacja i Autoryzacja

### US-001: Logowanie przez Spotify
**Jako** użytkownik  
**Chcę** zalogować się za pomocą mojego konta Spotify  
**Aby** aplikacja mogła uzyskać dostęp do moich danych słuchania

**Kryteria akceptacji:**
- [ ] Na stronie głównej jest przycisk "Zaloguj przez Spotify"
- [ ] Kliknięcie przekierowuje do strony autoryzacji Spotify
- [ ] Po zalogowaniu użytkownik jest przekierowany do dashboardu
- [ ] Token dostępu jest bezpiecznie przechowywany
- [ ] Wyświetlany jest komunikat o błędzie gdy logowanie się nie powiedzie

**Testy:**
- Test przekierowania do Spotify OAuth
- Test obsługi callback z tokenem
- Test obsługi błędów autoryzacji

---

### US-002: Wylogowanie
**Jako** zalogowany użytkownik  
**Chcę** móc się wylogować z aplikacji  
**Aby** zabezpieczyć swoje dane

**Kryteria akceptacji:**
- [ ] Widoczny przycisk "Wyloguj" w nawigacji
- [ ] Po wylogowaniu tokeny są usuwane
- [ ] Użytkownik jest przekierowany na stronę logowania

**Testy:**
- Test usunięcia sesji po wylogowaniu
- Test przekierowania po wylogowaniu

---

### US-003: Automatyczne odświeżanie tokenu
**Jako** zalogowany użytkownik  
**Chcę** żeby aplikacja automatycznie odświeżała mój token dostępu  
**Aby** nie musieć się ponownie logować co godzinę

**Kryteria akceptacji:**
- [ ] Token jest odświeżany przed wygaśnięciem
- [ ] Użytkownik nie jest przerywany podczas korzystania z aplikacji
- [ ] Jeśli odświeżenie się nie powiedzie, użytkownik jest przekierowany do logowania

**Testy:**
- Test odświeżania tokenu przed wygaśnięciem
- Test obsługi błędu odświeżania

---

## Epik 2: Dashboard i Profil

### US-004: Wyświetlanie profilu użytkownika
**Jako** zalogowany użytkownik  
**Chcę** widzieć swój profil Spotify  
**Aby** potwierdzić że jestem zalogowany na właściwe konto

**Kryteria akceptacji:**
- [ ] Wyświetlane jest zdjęcie profilowe
- [ ] Wyświetlana jest nazwa użytkownika
- [ ] Wyświetlany jest typ konta (premium/free)

**Testy:**
- Test renderowania komponentu profilu
- Test wyświetlania danych użytkownika

---

### US-005: Nawigacja dashboardu
**Jako** zalogowany użytkownik  
**Chcę** mieć łatwy dostęp do wszystkich sekcji statystyk  
**Aby** szybko przełączać się między widokami

**Kryteria akceptacji:**
- [ ] Menu nawigacyjne z sekcjami: Top Artyści, Top Utwory, Top Albumy, Historia
- [ ] Aktywna sekcja jest wyróżniona wizualnie
- [ ] Nawigacja działa na urządzeniach mobilnych

**Testy:**
- Test nawigacji między sekcjami
- Test responsywności menu

---

## Epik 3: Top Artyści

### US-006: Wyświetlanie top artystów
**Jako** zalogowany użytkownik  
**Chcę** widzieć listę moich najczęściej słuchanych artystów  
**Aby** poznać swoje preferencje muzyczne

**Kryteria akceptacji:**
- [ ] Lista top 20 artystów z pozycją rankingową
- [ ] Dla każdego artysty: zdjęcie, nazwa, gatunki
- [ ] Możliwość kliknięcia w artystę (przekierowanie do Spotify)

**Testy:**
- Test renderowania listy artystów
- Test wyświetlania danych artysty
- Test obsługi pustej listy

---

### US-007: Filtrowanie top artystów po okresie
**Jako** zalogowany użytkownik  
**Chcę** filtrować top artystów po okresie czasu  
**Aby** zobaczyć jak zmieniają się moje preferencje

**Kryteria akceptacji:**
- [ ] Przyciski/dropdown: "Ostatni miesiąc", "Ostatnie 6 miesięcy", "Wszystkie czasy"
- [ ] Lista aktualizuje się po zmianie filtru
- [ ] Pokazywany jest loader podczas ładowania

**Testy:**
- Test zmiany okresu
- Test wyświetlania loadera
- Test cache'owania danych

---

## Epik 4: Top Utwory

### US-008: Wyświetlanie top utworów
**Jako** zalogowany użytkownik  
**Chcę** widzieć listę moich najczęściej słuchanych utworów  
**Aby** zobaczyć jakie piosenki lubię najbardziej

**Kryteria akceptacji:**
- [ ] Lista top 20 utworów z pozycją rankingową
- [ ] Dla każdego utworu: okładka albumu, tytuł, artysta, album
- [ ] Możliwość kliknięcia w utwór (przekierowanie do Spotify)
- [ ] Wyświetlany czas trwania utworu

**Testy:**
- Test renderowania listy utworów
- Test wyświetlania szczegółów utworu
- Test formatowania czasu trwania

---

### US-009: Filtrowanie top utworów po okresie
**Jako** zalogowany użytkownik  
**Chcę** filtrować top utwory po okresie czasu  
**Aby** zobaczyć jak zmieniają się moje ulubione piosenki

**Kryteria akceptacji:**
- [ ] Przyciski/dropdown: "Ostatni miesiąc", "Ostatnie 6 miesięcy", "Wszystkie czasy"
- [ ] Lista aktualizuje się po zmianie filtru
- [ ] Pokazywany jest loader podczas ładowania

**Testy:**
- Test zmiany okresu
- Test wyświetlania loadera

---

## Epik 5: Top Albumy

### US-010: Wyświetlanie top albumów
**Jako** zalogowany użytkownik  
**Chcę** widzieć listę moich najczęściej słuchanych albumów  
**Aby** zobaczyć które albumy lubię najbardziej

**Kryteria akceptacji:**
- [ ] Lista top 20 albumów (wyliczona z top utworów)
- [ ] Dla każdego albumu: okładka, tytuł, artysta
- [ ] Wyświetlana liczba utworów z danego albumu w top
- [ ] Możliwość kliknięcia w album (przekierowanie do Spotify)

**Testy:**
- Test wyliczania top albumów z utworów
- Test renderowania listy albumów
- Test sortowania albumów

---

### US-011: Filtrowanie top albumów po okresie
**Jako** zalogowany użytkownik  
**Chcę** filtrować top albumy po okresie czasu  
**Aby** zobaczyć jak zmieniają się moje ulubione albumy

**Kryteria akceptacji:**
- [ ] Przyciski/dropdown analogiczne do artystów i utworów
- [ ] Spójna nawigacja między sekcjami

**Testy:**
- Test zmiany okresu dla albumów

---

## Epik 6: Historia słuchania

### US-012: Wyświetlanie ostatnio słuchanych utworów
**Jako** zalogowany użytkownik  
**Chcę** widzieć historię ostatnio słuchanych utworów  
**Aby** przypomnieć sobie co ostatnio słuchałem

**Kryteria akceptacji:**
- [ ] Lista ostatnich 50 utworów (limit Spotify API)
- [ ] Dla każdego utworu: okładka, tytuł, artysta, czas odsłuchania
- [ ] Utwory posortowane chronologicznie (najnowsze na górze)

**Testy:**
- Test renderowania historii
- Test formatowania daty/czasu
- Test sortowania

---

## Epik 7: Własne statystyki (Tracking)

### US-013: Śledzenie obecnie granego utworu
**Jako** zalogowany użytkownik  
**Chcę** żeby aplikacja automatycznie śledziła co słucham  
**Aby** budować szczegółowe statystyki odtworzeń

**Kryteria akceptacji:**
- [ ] Aplikacja sprawdza obecnie grany utwór co 30 sekund
- [ ] Każde odsłuchanie jest zapisywane do bazy danych
- [ ] Unikamy duplikatów (ten sam utwór w ciągu 3 minut)

**Testy:**
- Test zapisywania odsłuchania
- Test wykrywania duplikatów
- Test obsługi gdy nic nie jest grane

---

### US-014: Wyświetlanie własnych statystyk odtworzeń
**Jako** zalogowany użytkownik  
**Chcę** widzieć dokładną liczbę odtworzeń każdego utworu  
**Aby** mieć szczegółowe statystyki których Spotify nie udostępnia

**Kryteria akceptacji:**
- [ ] Lista utworów z liczbą odtworzeń
- [ ] Sortowanie po liczbie odtworzeń
- [ ] Filtrowanie po okresie (ostatni tydzień, miesiąc, rok, wszystko)

**Testy:**
- Test zliczania odtworzeń
- Test sortowania
- Test filtrowania po dacie

---

### US-015: Wyświetlanie łącznego czasu słuchania
**Jako** zalogowany użytkownik  
**Chcę** widzieć łączny czas słuchania muzyki  
**Aby** wiedzieć ile czasu spędzam na słuchaniu

**Kryteria akceptacji:**
- [ ] Łączny czas słuchania w godzinach/minutach
- [ ] Podział na okresy: dziś, ten tydzień, ten miesiąc, wszystko
- [ ] Średni dzienny czas słuchania

**Testy:**
- Test sumowania czasu
- Test formatowania czasu (godziny/minuty)
- Test obliczania średniej

---

## Epik 8: UI/UX

### US-016: Responsywny design
**Jako** użytkownik  
**Chcę** korzystać z aplikacji na różnych urządzeniach  
**Aby** mieć dostęp do statystyk z telefonu i komputera

**Kryteria akceptacji:**
- [ ] Aplikacja działa poprawnie na mobile (320px+)
- [ ] Aplikacja działa poprawnie na tablet (768px+)
- [ ] Aplikacja działa poprawnie na desktop (1024px+)

**Testy:**
- Testy responsywności komponentów

---

### US-017: Obsługa stanów ładowania i błędów
**Jako** użytkownik  
**Chcę** widzieć informacje o stanie ładowania i błędach  
**Aby** wiedzieć co się dzieje z aplikacją

**Kryteria akceptacji:**
- [ ] Skeleton loading podczas ładowania danych
- [ ] Czytelne komunikaty o błędach
- [ ] Możliwość ponowienia żądania po błędzie

**Testy:**
- Test wyświetlania skeleton loading
- Test wyświetlania komunikatów o błędach
- Test przycisku retry

---

### US-018: Tryb ciemny/jasny
**Jako** użytkownik  
**Chcę** móc przełączać między trybem ciemnym a jasnym  
**Aby** dostosować wygląd do swoich preferencji

**Kryteria akceptacji:**
- [ ] Przełącznik trybu w nawigacji
- [ ] Domyślnie zgodny z ustawieniami systemowymi
- [ ] Zapamiętywanie preferencji użytkownika

**Testy:**
- Test przełączania trybu
- Test persystencji preferencji

---

## Podsumowanie priorytetów

| Priorytet | User Story | Opis |
|-----------|------------|------|
| 🔴 Krytyczne | US-001, US-002, US-003 | Autentykacja |
| 🔴 Krytyczne | US-004, US-005 | Dashboard podstawy |
| 🟠 Wysokie | US-006, US-007 | Top artyści |
| 🟠 Wysokie | US-008, US-009 | Top utwory |
| 🟡 Średnie | US-010, US-011 | Top albumy |
| 🟡 Średnie | US-012 | Historia |
| 🟢 Rozszerzone | US-013, US-014, US-015 | Własny tracking |
| 🔵 Nice-to-have | US-016, US-017, US-018 | UI/UX |
