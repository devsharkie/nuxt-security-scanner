# 🐳 NUXT IMMUNE SYSTEM

## STRUKTURA PROJEKTU I CELE
Projekt na obecnym etapie jest narzędziem do lokalnej analizy bezpieczeństwa aplikacji opartych o Nuxt. Jego głównymi komponentami są:
  - scanner/ - skaner bezpieczeństwa napisany w Pythonie uruchamiany jako kontener Docker, stanowi układ odpornościowy projektu
  - frontend/ - frontend w Nuxt3 (uruchamiany osobno jako kontener), to nasz "organizm" do skanowania
  - baza danych - logi skanowania zapisywane w PostgreSQL, tworzą pamięć immunologiczną systemu

Projekt skupia się nie tylko na detekcji, ale także na edukacji i automatyzacji bezpiecznego tworzenia kodu. Częścią jego tworzenia jest od razu zapisywanie przykładów kodu nie tylko niebezpiecznych, ale również tych spełniających normy bezpieczeństwa, które następnie mogą być reużywalne w innych repozytoriach, przykładowo: logowanie, zarządzanie cookies lub Access Control dla panelu admina.

## WYKRYWANE TYPY ZAGROŻEŃ
- Nieprawidłowa konfiguracja cookies (np. brak Secure, HttpOnly, expiration date)
- Podatności typu SQL injection
- XSS - potencjalne miejsca wstrzyknięć skryptów
- Błędy kontroli dostępu

DISCLAIMER: Obecna wersja to etap testowy uruchamiany lokalnie. Stąd uproszczenia takie jak:
- hardkodowane dane logowania
- brak hashowania haseł
- uproszczone reguły skanowanie, stworzone pod konkretne przypadki

# 🧬 Metafora układu odpornościowego
Prezentacja będzie skupiona na teorii i powiązaniu rozwiązań technicznych z fizjologią układu odpornościowego. Odpowie na pytania: Jak systemy bezpieczeństwa naśladują biologiczną obronę organizmu? Jakie podstawowe zagadnienia obejmuje ta metafora?
## 1️⃣ Odpowiedź nieswoista — statyczna analiza
Odpowiedź nieswoista to pierwsza linia obrony organizmu, działająca szybko i ogólnie. W naszym systemie odpowiada jej statyczna analiza kodu (SAST).
- Działanie: Skaner przegląda kod źródłowy aplikacji (np. pliki Vue/TypeScript) bez jego uruchamiania. To jak monitorowanie skóry czy błon śluzowych pod kątem zagrożeń, zanim dostaną się do wnętrza.
- Przykłady: Wykrywanie niepoprawnych konfiguracji ciasteczek, potencjalnych miejsc XSS
## 2️⃣ Odpowiedź swoista — dynamiczna analiza
Gdy zagrożenie przeniknie przez pierwszą linię obrony, wkracza odpowiedź swoista, która jest bardziej precyzyjna i celowana. W naszym projekcie odpowiada jej dynamiczna analiza bezpieczeństwa aplikacji (DAST).
- Działanie: Skaner interaguje z uruchomioną aplikacją, wysyłając specjalnie spreparowane żądania i analizując odpowiedzi. To jak wyspecjalizowane komórki odpornościowe atakujące konkretne patogeny, które już znalazły się w krwiobiegu.
- Przykłady: Testowanie podatności na SQL Injection poprzez wstrzykiwanie złośliwych zapytań, czy audyt kontroli dostępu poprzez próby logowania i dostępu do chronionych zasobów z różnymi uprawnieniami.
## 3️⃣ Pamięć immunologiczna - baza danych
Układ odpornościowy zapamiętuje spotkane patogeny, aby w przyszłości reagować szybciej i skuteczniej. W naszym systemie za "pamięć immunologiczną" odpowiada baza danych PostgreSQL.
- Działanie: Wszystkie wyniki skanowania, wykryte luki oraz statusy testów są trwale zapisywane w bazie danych. Pozwala to na śledzenie postępów, analizę trendów i naukę na podstawie wcześniejszych skanów.
- Korzyści: Budowanie historii bezpieczeństwa aplikacji, przy rozbudowie, bardziej szczegółowych logach - możliwość tworzenia inteligentniejszego, „uczącego się” systemu obronnego np. dzięki ML.
# 🛡️ Obrona bierna i czynna
- Obrona czynna to świadome, proaktywne działania mające na celu zapobieganie i testowanie odporności. Odpowiadają jej „szczepionki” – czyli regularne, kontrolowane testowanie aplikacji za pomocą naszego skanera. Wykonujemy „atak” (np. próbę SQL Injection) w kontrolowanym środowisku, aby „nauczyć” nasz system, jak reagować i czy jest odporny na znane zagrożenia.
- Obrona bierna to mechanizmy, które są zawsze obecne i wbudowane w kod oraz środowisko, działając prewencyjnie. Przykłady to użycie funkcji sanitacji danych wejściowych, stosowanie bezpiecznych nagłówków HTTP (np. Content-Security-Policy), czy domyślne stosowanie parametrów bezpieczeństwa dla ciasteczek. To jak naturalne bariery ochronne organizmu, które minimalizują ryzyko infekcji. "Surowica" w tym kontekście to natychmiastowe dostarczenie gotowego rozwiązania (np. specyficznego skryptu blokującego, konkretnej reguły WAF, szybkiej edycji kodu) na problem, który już wystąpił. Taka interwencja niekoniecznie musi być trwale logowana w "pamięci immunologicznej" (bazie danych) jako wykryta luka, jeśli jej celem jest błyskawiczne zażegnanie incydentu.
# 🚀 Możliwości rozbudowy
Projekt „Nuxt Immune System” jest elastyczny i ma ogromny potencjał rozbudowy:
- Integracja z CI/CD: Możliwość włączenia skanera do potoków Continuous Integration/Continuous Delivery. Pozwoli to na automatyczne, okresowe skanowanie aplikacji lub wykonywanie skanów po każdym commicie, zapewniając ciągłą weryfikację bezpieczeństwa i wychwytywanie problemów na wczesnym etapie cyklu rozwojowego.
- Rozszerzenie zakresu skanowania: Dodawanie nowych typów wykrywanych zagrożeń i rozwijanie algorytmów detekcji.
- Rozbudowa pamięci immunologicznej: Implementacja zaawansowanych raportów, dashboardów oraz mechanizmów predykcyjnych opartych o zgromadzone dane.
- Udoskonalenie „szczepionek”: Tworzenie bardziej złożonych i realistycznych scenariuszy ataków w dynamicznej analizie.