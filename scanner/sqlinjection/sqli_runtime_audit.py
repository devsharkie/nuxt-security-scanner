import requests
import time
import sys

# Dajemy Nuxtowi chwilę na pełne uruchomienie się
time.sleep(10)

# Adres URL jest zbudowany z nazwy serwisu `frontend` i portu aplikacji
BASE_URL = "http://frontend:3000/api"
HEADERS = {'Content-Type': 'application/json'}

def run_test(name, url, payload, is_attack_expected_to_succeed):
    """Uruchamia pojedynczy test i sprawdza wynik."""
    print(f"--- 🧪 Test: {name} ---")
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        # Zgłoś błąd, jeśli status HTTP to 4xx lub 5xx
        response.raise_for_status()
        data = response.json()
        print(f"Odpowiedź serwera: {data}")

        users_found = data.get("data")
        test_passed = False

        if is_attack_expected_to_succeed:
            # Atak się udał, jeśli zwrócono WIĘCEJ NIŻ 0 użytkowników
            if users_found and len(users_found) > 0:
                print("REZULTAT: 🚨 PODATNE (zgodnie z oczekiwaniami)")
                test_passed = True
            else:
                print("REZULTAT: ❌ Atak się nie powiódł, choć powinien")
        else:
            # Obrona zadziałała, jeśli zwrócono DOKŁADNIE 0 użytkowników
            if users_found and len(users_found) == 0:
                print("REZULTAT: ✅ BEZPIECZNE (zgodnie z oczekiwaniami)")
                test_passed = True
            else:
                print("REZULTAT: ❌ Endpoint nie zachował się bezpiecznie")
        
        return test_passed

    except requests.exceptions.RequestException as e:
        print(f"Błąd krytyczny testu: {e}")
        return False

# Złośliwy ładunek, który zawsze zwraca prawdę w zapytaniu SQL
sql_injection_payload = {"username": "' OR 1=1 --"}

# Uruchomienie testów
print("--- Rozpoczynanie skanowania podatności SQL Injection ---")

vulnerable_test_result = run_test(
    "Atak na podatny endpoint (notsecure_sqli)",
    f"{BASE_URL}/notsecure_sqli",
    sql_injection_payload,
    is_attack_expected_to_succeed=True
)

secure_test_result = run_test(
    "Atak na bezpieczny endpoint (secure_sqli)",
    f"{BASE_URL}/secure_sqli",
    sql_injection_payload,
    is_attack_expected_to_succeed=False
)

print("\n--- ✅ Podsumowanie testów ---")
if vulnerable_test_result and secure_test_result:
    print("Wszystkie testy zakończone pomyślnie. Luki wykryte, zabezpieczenia działają.")
    sys.exit(0) # Zakończ z kodem sukcesu
else:
    print("Jeden lub więcej testów zakończyło się niepowodzeniem.")
    sys.exit(1) # Zakończ z kodem błędu