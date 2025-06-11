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

### Dostęp Użytkowników z Rolą user_test (Basic Auth)





## Kluczowe Wyzwania i Rozwiązania
Proces osiągnięcia pełnej zgodności testów wymagał identyfikacji i rozwiązania kilku istotnych problemów:
