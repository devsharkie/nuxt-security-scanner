# 🐳 NUXT IMMUNE SYSTEM

## PROJECT STRUCTURE & GOALS
At its current stage, the project is a tool for local security analysis of applications built with Nuxt. Its main components are:
- scanner/ – a security scanner written in Python, run as a Docker container, representing the immune system of the project
- frontend/ – a Nuxt3 frontend (run separately in a container), which acts as the "organism" to be scanned
- Database – scanning logs are stored in PostgreSQL, forming the immune memory of the system

The project focuses not only on detection, but also on education and automation in secure code development. As part of its creation, it includes examples of both insecure and secure code that meet safety standards and can be reused in other repositories—for example: login mechanisms, cookie management, or access control for admin panels.

## DETECTED THREAT TYPES
- Incorrect cookie configurations (e.g., missing Secure, HttpOnly, expiration date)
- SQL Injection vulnerabilities
- XSS – potential script injection points
- Access control issues
DISCLAIMER: The current version is a local testing stage. Hence, there are simplifications such as:
Hardcoded login credentials
No password hashing
Simplified scanning rules tailored to specific cases

## Immune System Metaphor
The presentation focuses on theory and the correlation between technical solutions and the physiology of the immune system. It aims to answer:
How do security systems mimic the body's biological defenses? What key concepts does this metaphor cover?
## 1️⃣ Innate Response — Static Analysis
The innate immune response is the body’s first line of defense, acting quickly and broadly. In our system, this corresponds to Static Application Security Testing (SAST).
- How it works: The scanner inspects the application’s source code (e.g., Vue/TypeScript files) without executing it. It’s like monitoring the skin or mucous membranes for threats before they penetrate the body.
- Examples: Detecting incorrect cookie settings, Identifying potential XSS vectors
## 2️⃣ Adaptive Response — Dynamic Analysis
When a threat passes the first line of defense, the adaptive immune response engages—more precise and targeted. In our project, this is Dynamic Application Security Testing (DAST).
- How it works: The scanner interacts with the running application, sending specially crafted requests and analyzing the responses. This mirrors specialized immune cells targeting specific pathogens already in the bloodstream.
- Examples: Testing for SQL injection by injecting malicious queries, Auditing access control by attempting logins and accessing protected resources with varying permissions
## 3️⃣ Immune Memory — The Database
The immune system remembers previously encountered pathogens to react faster and more effectively in the future. In our system, PostgreSQL acts as the immune memory.
- How it works: All scanning results, detected vulnerabilities, and test statuses are permanently logged in the database. This allows for progress tracking, trend analysis, and learning from previous scans.
- Benefits: Building a security history for the application, With further expansion and more detailed logs, the potential to create a smarter, learning defense system (e.g., via machine learning)
# 🛡️ Passive and Active Defense
- Active defense involves deliberate, proactive actions to test and improve resistance. These are like vaccinations—regular, controlled application tests using our scanner. We perform a “controlled attack” (e.g., an SQL injection attempt) in a safe environment to “teach” the system how to respond and determine its resistance to known threats.
- Passive defense includes mechanisms built into the code and environment that always work preventively. Examples include input sanitization, secure HTTP headers (e.g., Content-Security-Policy), or default security parameters for cookies. These are like the body’s natural protective barriers that minimize infection risk. "Serum" in this context means delivering an immediate fix (e.g., a specific blocking script, WAF rule, or quick code patch) for an issue that has already occurred. Such interventions might not be permanently logged in the "immune memory" (the database) if their goal is instant incident resolution.
# 🚀 Expansion Potential
The “Nuxt Immune System” project is flexible and has great potential for future growth:
- CI/CD integration: Ability to integrate the scanner into Continuous Integration/Continuous Delivery pipelines. This would allow automated, periodic scanning or triggering scans on each commit, ensuring continuous security verification and early detection.
- Extended scan coverage: Adding new types of threats and enhancing detection algorithms.
- Enhanced immune memory: Implementing advanced reports, dashboards, and predictive mechanisms based on collected data.
- Improved "vaccines": Creating more complex and realistic attack scenarios for dynamic analysis.

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
