# AUdyt Kontroli Dostępu
## 📌 Cel
Ten dokument przedstawia szczegółowy raport z audytu bezpieczeństwa przeprowadzonego na aplikacji webowej. Głównym celem było kompleksowe sprawdzenie i weryfikacja poprawności implementacji mechanizmów kontroli dostępu i uwierzytelniania. Audyt miał za zadanie zidentyfikować wszelkie potencjalne luki, które mogłyby pozwolić na nieautoryzowany dostęp lub eskalację uprawnień.

## 🛠️ Przeprowadzone Testy
Skaner bezpieczeństwa wykonał serię rygorystycznych testów w ramach audytu kontroli dostępu (run_access_control_audit), obejmujących następujące scenariusze:

 ### 1. Dostęp Nieautoryzowany (Basic Auth)
 - Scenariusz: Próby dostępu do chronionych zasobów takich jak /api/logged i /api/admin bez podawania jakichkolwiek danych uwierzytelniających (nagłówek Basic Auth).
 - Oczekiwany Wynik: HTTP 401 Unauthorized (Odmowa dostępu).

### 2. Dostęp Użytkowników z Rolą user (Basic Auth)
- Scenariusz: 
  - Próba dostępu do zasobu przeznaczonego dla wszystkich uwierzytelnionych użytkowników (/api/logged).
  - Próba dostępu do zasobu przeznaczonego wyłącznie dla administratorów (/api/admin).
- Oczekiwany Wynik: HTTP 200 OK dla /api/logged (Sukces), HTTP 403 Forbidden dla /api/admin (Odmowa dostępu).

### 3. Dostęp Użytkowników z Rolą user_test (Basic Auth)
- Scenariusz: Powtórzenie testów dla roli user, używając użytkownika user_test, aby potwierdzić spójność polityki dostępu dla wszystkich użytkowników o roli user.
- Oczekiwany Wynik: HTTP 200 OK dla /api/logged (Sukces), HTTP 403 Forbidden dla /api/admin (Odmowa dostępu).

### 4. Dostęp Użytkowników z Rolą admin (Basic Auth)
- Scenariusz:
  - Próba dostępu do zasobu przeznaczonego dla wszystkich uwierzytelnionych użytkowników (/api/logged).
  - Próba dostępu do zasobu przeznaczonego dla administratorów (/api/admin).
- Oczekiwany Wynik: HTTP 200 OK dla obu zasobów (Sukces).

### 5. Logowanie poprzez Publiczny Endpoint /api/login
- Scenariusz
  - Próba zalogowania się jako użytkownik z rolą admin przez publiczny endpoint /api/login (który celowo nie powinien zezwalać na logowanie adminów).
  - Próba zalogowania się jako użytkownik z rolą user, jednocześnie próbując manipulować payloadem żądania, aby zmienić swoją rolę na admin.
  - Próba zalogowania się jako nieistniejący użytkownik.
- Oczekiwany wynik:
  - HTTP 401 Unauthorized dla administratora i nieistniejącego użytkownika.
  - Dla próby manipulacji rolą: HTTP 200 OK, ale post-check potwierdzający, że przypisana rola użytkownika to nadal user, a nie admin.

### 6. Logowanie poprzez Endpoint Administracyjny /api/admin-login
- Scenariusz:
  - Próba udanego logowania jako administrator.
  - Próba zalogowania się jako zwykły użytkownik.
- Oczekiwany Wynik: HTTP 200 OK dla administratora (Sukces), HTTP 403 Forbidden dla zwykłego użytkownika (Odmowa dostępu).


## 🤔 Kluczowe Wyzwania i Rozwiązania
Proces osiągnięcia pełnej zgodności testów wymagał identyfikacji i rozwiązania kilku istotnych problemów:
### Błąd składni SQL w skrypcie inicjalizującym bazę danych (db-initializer.ts)
- Problem: Początkowe niepowodzenia testów logowania i dostępu wynikały z tego, że baza danych była pusta lub niekompletna. Analiza logów wykazała błąd składniowy w instrukcji INSERT INTO (brak przecinka między zestawami wartości). Co więcej, biblioteka SQLite, której używaliśmy, wymagała wykonywania każdej komendy SQL osobno (np. DROP TABLE, CREATE TABLE, INSERT) zamiast jako jednego długiego ciągu, co objawiało się błędem sqlite_error near "(": syntax error.
- Rozwiązanie: Składnię SQL poprawiono, a wykonanie poleceń rozdzielono na osobne wywołania await db.exec() dla każdej instrukcji (DROP, CREATE, INSERT dla każdego użytkownika). Pozwoliło to na prawidłowe przygotowanie danych testowych.

### Problemy z uprawnieniami do plików w środowisku Docker (EACCES: permission denied)
- Problem: Podczas budowania i uruchamiania aplikacji w kontenerach Docker, pojawiały się błędy EACCES: permission denied przy próbie zapisu do katalogu node_modules/.cache. Wynikało to z konfliktu uprawnień między systemem plików hosta a użytkownikiem kontenera. Gdy node_modules było bind-mountowane z hosta (./frontend:/app), pliki tworzone przez npm install (często jako root w kontenerze) miały uprawnienia, które uniemożliwiały późniejszy zapis przez proces Nuxt (np. jako użytkownik node).
- Rozwiązanie: Zastosowano anonimowy wolumin dla node_modules w pliku docker-compose.yml (- /app/node_modules). Dzięki temu katalog node_modules jest zarządzany wewnętrznie przez Docker, z zapewnionymi odpowiednimi uprawnieniami, niezależnie od uprawnień na hoście.

## 🔒 Wnioski
Skuteczne rozwiązanie wszystkich powyższych problemów pozwoliło na kompleksowe i pomyślne przetestowanie mechanizmów kontroli dostępu. Wyniki audytu potwierdzają, że aplikacja posiada solidnie zaimplementowane i działające mechanizmy autoryzacji i uwierzytelniania, spełniające oczekiwane standardy bezpieczeństwa. Ten proces podkreśla kluczowe znaczenie szczegółowej weryfikacji zarówno kodu aplikacji, jak i konfiguracji środowiska uruchomieniowego (zwłaszcza w kontekście Dockera) w kontekście bezpieczeństwa.