# 🐳 NUXT IMMUNE SYSTEM

## STRUKTURA PROJEKTU I CELE
Projekt na obecnym etapie jest narzędziem do lokalnej analizy bezpieczeństwa aplikacji opartych o Nuxt. Jego głównymi komponentami są:
  - scanner/ - skaner bezpieczeństwa napisany w Pythonie uruchamiany jako kontener Docker
  - frontend/ - frontend w Nuxt3 (uruchamiany osobno jako kontener)
  - baza danych - logi skanowania zapisywane w PostgreSQL

Projekt skupia się nie tylko na detekcji, ale także na edukacji i automatyzacji bezpiecznego tworzenia kodu. Częścią jego tworzenia jest od razu zapisywanie przykładów kodu nie tylko niebezpiecznych, ale również tych spełniających normy bezpieczeństwa, które następnie mogą być reużywalne w innych repozytoriach, przykładowo: logowanie, zarządzanie cookies lub Access Control dla panelu admina.

## WYKRYWANE TYPY ZAGROŻEŃ
- Brak odpowiednich nagłówków bezpieczeństwa (np. Content-Security-Policy)
- Nieprawidłowa konfiguracja cookies (np. brak Secure, HttpOnly, expiration date)
- Podatności typu SQL injection
- XSS - potencjalne miejsca wstrzyknięć skryptów
- Błędy kontroli dostępu

DISCLAIMER: Obecna wersja to etap testowy uruchamiany lokalnie. Stąd uproszczenia takie jak:
- hardkodowane dane logowania
- brak hashowania haseł
- uproszczone reguły skanowanie, stworzone pod konkretne przypadki

# 🧬 Metafora układu odpornościowego
## 1️⃣ Odpowiedź nieswoista — statyczna analiza

## 2️⃣ Odpowiedź swoista — dynamiczna analiza

## Pamięć immunologiczna - baza danych

# 🛡️ Obrona bierna i czynna

# 🚀 Możliwości rozbudowy