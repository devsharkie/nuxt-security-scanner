# 🔒 SECURITY_PATTERNS

## Źródło
Wzorce wykrywania oparte są na [oficjalnych wytycznych bezpieczeństwa Vue](https://vuejs.org/guide/best-practices/security.html). Celem jest identyfikacja potencjalnie niebezpiecznych praktyk, które mogą prowadzić do luk takich jak XSS, clickjacking lub zdalne wykonanie kodu (RCE).

## 🔍 Jak działa skaner?
Skaner rekurencyjnie przeszukuje wszystkie pliki `.vue` i `.ts` w katalogu frontendowym (z wyłączeniem folderów takich jak `node_modules`, `.nuxt`, `dist`). Dla każdego pliku sprawdza, czy zawiera zdefiniowane wzorce (`DETECTION_PATTERNS`) w kodzie źródłowym.

Jeśli dany wzorzec zostanie znaleziony, skaner:
- rejestruje incydent w bazie danych (za pomocą funkcji `log_issue`),
- zapisuje poziom zagrożenia (`severity`), opis (`message`) oraz ścieżkę pliku,
- kontynuuje skanowanie wszystkich pozostałych plików (brak wczesnego zakończenia).

---

## 🚨 Wykrywane wzorce i potencjalne zagrożenia

### 1. `r'v-html\s*=\s*"[^"]*"'`
- **Zagrożenie:** Pozwala na wstrzyknięcie nieufnego HTML do DOM — może prowadzić do **XSS (Cross-Site Scripting)**.
- **Przykład niebezpieczny:**
  ```vue
  <div v-html="userProvidedHtml"></div>
  ```
  - **Dlaczego to niebezpieczne:** Vue nie filtruje zawartości w v-html, więc użytkownik może wstrzyknąć złośliwy kod HTML/JS.
  - **Zalecenia:**
    - Nie używaj 'v-html' z treściami pochodzącymi od użytkownika
    - Jeśli musisz, upewnij się, że dane są sanityzowane lub renderowane w sandbox iframe

### 2. `r'eval\s*\('`
- **Zagrożenie:** Funkcja eval() wykonuje dowolny kod JS przekazany jako tekst. Może prowadzić do pełnego przejęcia aplikacji.
- **Przykład niebezpieczny:**
  ```js
  eval(userInput)
  ```
  - **Dlaczego to niebezpieczne:** Pozwala wykonać dowolny kod, np. przesłać tokeny dostępu lub manipulować DOM.
  - **Zalecenia:**
    - Nigdy nie używaj eval() w aplikacjach webowych.
    - Dla JSON: użyj JSON.parse.
    - Dla dynamicznych funkcji użyj bezpiecznych wzorców, np. funkcji mapujących

### 3. `r':href\s*=\s*"[^"]*"'`
- **Zagrożenie:** Pozwala użytkownikowi określić adres URL — może prowadzić do phishingu lub javascript: injection.
- **Przykład niebezpieczny:**
  ```vue
  <a :href="userProvidedUrl">Click me</a>
  ```
  - **Dlaczego to niebezpieczne:** Użytkownik może podać javascript:alert(1) lub link prowadzący do strony phishingowej.
  - **Zalecenia:**
    - Zawsze sanityzuj URL po stronie backendu przed zapisaniem.
    - Można opcjonalnie użyć biblioteki sanitize-url, ale frontend nie wystarcza.
    - Jeśli :href jest przekazywany jako prop — rozważ dodanie lokalnej whitelisty, aby zignorować zatwierdzone przypadki.

### 4. `r':style\s*=\s*"[^"]*"'`
- **Zagrożenie:** Umożliwia użytkownikowi kontrolowanie stylów CSS, co może prowadzić do clickjackingu.
- **Przykład niebezpieczny:**
  ```vue
  <a :style="userProvidedStyles">Click me</a>
  ```
  - **Dlaczego to niebezpieczne:** Możliwe ukrycie istotnych elementów strony, np. nadpisanie przycisku logowania przez link phishingowy.
  - **Zalecenia:**
    - Używaj jawnego przypisywania tylko do dozwolonych właściwości:
    ```vue
  <a
  :style="{
    color: userColor,
    background: userBackground
  }"
>
  Click me
</a>
  ```
    - Jeśli :style pochodzi z propów (np. props.style) — można stosować whitelisty lub walidację typu.