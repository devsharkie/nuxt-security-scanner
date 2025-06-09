# 🔒 SECURITY_PATTERNS.md

## 🔍 Jak działa skaner?

Skaner rekurencyjnie przeszukuje wszystkie pliki `.vue` i `.ts` w katalogu frontendowym (z wyłączeniem folderów takich jak `node_modules`, `.nuxt`, `dist`). Dla każdego pliku sprawdza, czy zawiera zdefiniowane wzorce (`DETECTION_PATTERNS`) w kodzie źródłowym.

Jeśli dany wzorzec zostanie znaleziony, skaner:
- rejestruje incydent w bazie danych (za pomocą funkcji `log_issue`),
- zapisuje poziom zagrożenia (`severity`), opis (`message`) oraz ścieżkę pliku,
- kontynuuje skanowanie wszystkich pozostałych plików (brak wczesnego zakończenia).

---

## 🚨 Wykrywane wzorce i potencjalne zagrożenia

### 1. `v-html`
- **Zagrożenie:** Pozwala na wstrzyknięcie nieufnego HTML do DOM — może prowadzić do **XSS (Cross-Site Scripting)**.
- **Przykład niebezpieczny:**
  ```vue
  <div v-html="userProvidedHtml"></div>
  ```