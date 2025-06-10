# Skanowanie Nagłówków HTTP

## 📌 Cel
Moduł ten wykonuje skanowanie bezpieczeństwa nagłówków HTTP, aby wykrywać brakujące lub źle skonfigurowane nagłówki związane z bezpieczeństwem w aplikacji. Celem jest poprawa bezpieczeństwa poprzez identyfikację słabych punktów i braków w nagłówkach.

## 🛠️ Jak to działa?

### 1. Logowanie nagłówków
Skaner sprawdza obecność i konfigurację ważnych nagłówków bezpieczeństwa, takich jak Content-Security-Policy, X-Frame-Options oraz Strict-Transport-Security. Loguje wyłącznie te przypadki, gdzie nagłówki są brakujące, niepoprawne lub potencjalnie stanowią ryzyko.

### 2. Zapisywanie wykrytych problemów
Problematyczne nagłówki są zapisywane w bazie danych z informacjami o:
- header_name: nazwa nagłówka
- header_value: wartość nagłówka (jeśli dostępna)
- timestamp: czas wykrycia problemu
- scan_id: powiązanie z konkretnym skanowaniem

### 3. Typy skanowania
- Skanowanie statyczne: analiza plików konfiguracyjnych (np. nuxt.config.js) pod kątem nieprawidłowej konfiguracji nagłówków.
- Skanowanie dynamiczne: (planowane) wykonywanie zapytań HTTP do serwera i analiza nagłówków odpowiedzi pod kątem błędów lub braków.

## 🤔 Dlaczego to ważne?

### ✅ Wykrywanie realnych zagrożeń
Moduł skupia się na logowaniu faktycznych problemów, które mogą narazić aplikację na ataki takie jak clickjacking, XSS czy MITM, co pozwala efektywnie poprawić bezpieczeństwo.

### 🛡️ Poprawa najlepszych praktyk bezpieczeństwa
Daje jasny obraz obecnej konfiguracji nagłówków i wskazuje miejsca wymagające poprawy, co sprzyja stosowaniu rygorystycznych zabezpieczeń.

## ⚙️ Możliwości rozszerzenia
Moduł można rozszerzyć o dodatkowe nagłówki i reguły, aby wykrywać mniej krytyczne, ale nadal wartościowe dla bezpieczeństwa nagłówki, takie jak:
- Referrer-Policy
- Permissions-Policy
- Expect-CT

Dla takich nagłówków można ustawić niższy poziom ważności alertów, aby dostosować skaner do indywidualnych potrzeb.

