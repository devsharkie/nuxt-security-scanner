# 📘 Secure Cookies – Skanowanie i Problemy
## 🔍 Etap 1: Statyczne skanowanie ciasteczek
W projekcie został zaimplementowany statyczny skaner bezpieczeństwa, który analizuje kod źródłowy aplikacji frontendowej (.vue, .ts) w celu wykrycia potencjalnych nieprawidłowości przy ustawianiu ciasteczek.

### Obsługiwane metody ustawiania ciasteczek:
- useCookie(...) – typowe dla Nuxt
- setCookie(...) – serwerowe API Nuxt
- document.cookie = ... – klient

## 📋 Co jest sprawdzane?
Każdy przypadek ustawienia ciasteczka analizowany jest pod kątem:

| Wymóg                         | Poziom błędu | Opis                                                                 |
|-------------------------------|--------------|----------------------------------------------------------------------|
| `httpOnly: true`              | LOW/HIGH     | Wymagane w cookie serwerowym. Niedostępne w `document.cookie`.      |
| `secure: true`                | MEDIUM       | Wymagane dla bezpiecznej transmisji przez HTTPS.                    |
| `sameSite: strict` lub `lax` | LOW          | Ogranicza wysyłanie ciasteczek cross-site.                          |
| `maxAge` ≤ 90 dni             | MEDIUM       | Zabezpieczenie przed nadmierną trwałością ciasteczek.               |
| Przypisania dynamiczne (`+`) | HIGH         | Możliwe manipulacje przez użytkownika lub XSS.                      |

### ✅ Przykład poprawnego użycia (Nuxt 3, server-side)

```
setCookie(event, 'secureCookie', 'value', {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 60 * 60 * 24 * 7 // 7 dni
})
```
### ⚠️ Przykład błędnego użycia:
```
useCookie("badCookie").value = "bad"
// Brakuje httpOnly, secure, sameSite
```

## 🔧 Etap 2: Dynamiczne skanowanie ciasteczek
Dynamiczny skan miał za zadanie uruchomić instancję przeglądarki (np. przez selenium + chromedriver), otworzyć stronę aplikacji i odczytać ciasteczka ustawione przez serwer.

### ❌ Problemy:
- Brak komunikacji z serwerem przez host.docker.internal:
Rozwiązanie: użycie nazwy kontenera (np. frontend:3000).
- Brak ciasteczek w odpowiedzi HTTP:
- Problemy z konfiguracją chromedriver: niepoprawna konfiguracja w kontenerze/ Brak zależności systemowych (np. chromium, fonts, libnss)/ Potrzebna poprawna baza obrazu (np. selenium/standalone-chrome) lub ręczna instalacja chromium w Dockerfile.

## 💡 Wnioski i rekomendacje
✅ Co działa:
Pełny statyczny skan kodu frontendowego, który wykrywa:
- Zbyt długie maxAge
- Brak secure, httpOnly, sameSite

🚧 Co wymaga poprawy:
- Dynamiczne testy, możliwe alternatywy:
  - Test po stronie Nuxt (setCookie, sprawdzanie przez event.headers.cookie)
  - Wysyłanie danych do bazy z poziomu Nuxt/TypeScript?