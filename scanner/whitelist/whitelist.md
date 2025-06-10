# Whitelist Mechanizm dla Skanera Bezpieczeństwa

## 📌 Cel
Ten moduł implementuje prosty mechanizm whitelistingu (białej listy) dla systemu skanowania luk bezpieczeństwa, głównie w kontekście statycznej analizy kodu (SAST). Głównym celem jest ograniczenie fałszywych pozytywów — przypadków, w których skaner wykrywa potencjalną lukę, która w rzeczywistości została świadomie i bezpiecznie zaimplementowana.

## 🛠️ Jak to działa?

### 1. Plik whitelist.json
Plik konfiguracyjny whitelist.json zawiera listę identyfikatorów luk (vuln_id), które mają zostać zignorowane przez system skanowania: 
```
{
  "ignored_ids": [
    "api_key_exposure::/config.js::line:42",
    "cookie_insecure::/auth.vue::missing secure flag"
  ]
}
```
Każdy wpis identyfikuje konkretną lokalizację i typ potencjalnej luki, którą celowo pomijamy.

### 2. Generowanie vuln_id
Identyfikator luki(vuln_id) jest generowany na podstawie ścieżki do pliku i typu wykrytej podatności 
```
generate_vuln_id("/config.js", "API_KEY_EXPOSURE")
# => "config.js::api_key_exposure"
```

### 3. Sprawdzanie czy luka jest whitelist
Funkcja sprawdza, czy dany vuln_id znajduje się na wcześniej załadowanej liście ignorowanych identyfikatorów. Jeśli tak, skaner nie zgłasza tej luki, ani jej nie loguje w bazie danych.
```
is_whitelisted(vuln_id)
```

## 🤔 Po co to wszystko?

### ✅ Redukcja fałszywych pozytywów
Statyczna analiza kodu nie jest doskonała. Detekcja luk opiera się często na sztywnych regułach i wyrażeniach regularnych, które mogą nie uwzględniać kontekstu lub nietypowych, ale bezpiecznych przypadków użycia. Przykład: 
- Jeśli klucz API występuje w pliku, ale został on załadowany dynamicznie w bezpieczny sposób (np. przez dotenv), skaner może błędnie zgłosić lukę.

### 🛡️ Świadome wyjątki
Mechanizm whitelistingu pozwala zespołowi deweloperskiemu świadomie zaakceptować pewne wyjątki, utrzymując kod bez zmian i bez fałszywego alarmu w systemie.

### 🔒 Brak logowania
Ignorowane wpisy nie są logowane do bazy danych, co zapobiega "zanieczyszczeniu" statystyk lub dashboardów skanera informacjami, które nie wymagają działania.