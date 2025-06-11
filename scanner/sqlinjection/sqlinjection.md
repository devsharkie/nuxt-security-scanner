# SQL INJECTION AUDIT

## 📌 Cel
Ten moduł implementuje audyt w celu wykrycia luk typu SQL Injection w aplikacjI nUXT. Działając w oparciu o testy z użyciem złośliwych ładunków, skaner weryfikuje, czy endpointy aplikacji są podatne na wstrzyknięcia SQL. Jego celem jest identyfikacja słabo zabezpieczonych interakcji z bazą danych, które mogłyby pozwolić atakującemu na manipulowanie zapytaniami SQL.

## 🤔 Czym jest SQL Injection?
SQL Injection (SQLI) to rodzaj ataku polegającego na wstrzyknięciu złośliwego kodu SQL do zapytania wykonywanego przez aplikację do bazy danych. Dzieje się to, gdy aplikacja dynamicznie konstruuje zapytania SQL, łącząc dane dostarczone przez użytkownika bezpośrednio z kodem zapytania, bez odpowiedniego czyszczenia lub parametryzacji.

### Atakujący może w ten sposób:
- Odczytywać, modyfikować lub usuwać dane z bazy danych.
- Obchodzić mechanizmy uwierzytelniania (np. logować się jako administrator bez hasła).
- Wykonywać operacje administracyjne na bazie danych.

### Typowe Payloads (Ładunki Ataku)
Atakujący często używają specjalnie spreparowanych ciągów znaków, które "łamują" oryginalne zapytanie SQL i wstrzykują własną logikę. Przykłady:
- Logowanie jako dowolny użytkownik: username: ' OR 1=1 --
  - Oryginalne zapytanie: SELECT * FROM users WHERE username = 'admin' AND password = 'password'
  - Z ładunkiem: SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = 'password'
  - 1=1 zawsze jest prawdziwe, a -- komentuje resztę zapytania, co skutecznie omija weryfikację hasła.
- Pobieranie wszystkich rekordów: id: 1 OR 1=1
  - Oryginalne zapytanie: SELECT * FROM products WHERE id = 1
  - Z ładunkiem: SELECT * FROM products WHERE id = 1 OR 1=1
  - Zwraca wszystkie produkty, niezależnie od ID.

W pokazanym w kodzie przykładzie używany jest ładunek {"username": "' OR 1=1 --"} do testowania podatności

## 🛡️ Jak unikać SQL Injection w Nuxt.js
Kluczem do unikania SQL Injection jest nigdy nie konkatenować danych użytkownika bezpośrednio do zapytań SQL. Zamiast tego, należy używać zapytań parametryzowanych (prepared statements).

### Bezpieczny przykład:
```
import getDb from '~/server/utils/db';

export default defineEventHandler(async (event) => {
  const { username } = await readBody(event);
  
  if (!username) 
    throw createError({ statusCode: 400, message: 'Missing username' });

  const db = await getDb();

  //PARAMETRYZOWANE ZAPYTANIE Z PLACEHOLDEREM
  const query = 'SELECT id, username, role FROM users WHERE username = ?';
  const params = [username];

  try {
    const users = await db.all(query, params);
    console.log(`Executing secure query with params: ${params}`);
    return { data: users };
  } catch (error: any) {
    throw createError({ statusCode: 500, message: error.message });
  }
});
```
### Podatny przykład:
```
import getDb from '~/server/utils/db';

export default defineEventHandler(async (event) => {
  const { username } = await readBody(event);

  if (!username) 
    throw createError({ statusCode: 400, message: 'Missing username' });

  const db = await getDb();

  //ZMIENNA WSTAWIONA BEZPOSREDNIO DO ZAPYTANIA
  const query = `SELECT id, username, role FROM users WHERE username = '${username}'`;

  try {
    const users = await db.all(query);
    console.log(`Executing vulnerable query: ${query}`);
    return { data: users, query }; 
  } catch (error: any) {
    return { error: error.message, query };
  }
});
```

## 🛠️ Jak działa ten skaner?
Ten skaner koncentruje się na audycie środowiskowym (runtime audit). Oznacza to, że faktycznie wysyła zapytania do uruchomionej aplikacji, aby sprawdzić, jak reaguje na złośliwe ładunki.

### 1. Endpointy do testowania
Skaner przyjmuje listę endpointów API (np. ["notsecure_sqli", "secure_sqli"]), które mają zostać poddane testom.

### 2. Wykonanie testu (test_sqli)
Dla każdego endpointu, funkcja test_sqli:
- Konstruuje pełny URL do endpointu.
- Wysyła żądanie POST z predefiniowanym ładunkiem SQL Injection ({"username": "' OR 1=1 --"}).
- Czeka na odpowiedź serwera i zwraca pole data z tej odpowiedzi (które powinno zawierać listę znalezionych użytkowników).

### 3. Interpretacja wyników (sqli_results)
Funkcja sqli_results analizuje odpowiedzi z test_sqli i loguje potencjalne podatności:
- Wykryto podatność: Jeśli odpowiedź serwera zawiera niepustą listę użytkowników (np. zwróciło wszystkich użytkowników z bazy), oznacza to, że wstrzyknięcie SQL się powiodło. Skaner loguje to jako "HIGH" severity do bazy danych.
- Endpoint bezpieczny: Jeśli odpowiedź serwera zawiera pustą listę użytkowników, oznacza to, że endpoint poprawnie zignorował złośliwy ładunek i jest bezpieczny. Skaner loguje to jako INFO.

### 4. Mechanizm whitelistingu
Skaner integruje się z modułem whitelist.manager. Jeśli wykryta podatność (identyfikowana przez unikalny vuln_id) znajduje się na białej liście, zostanie ona zignorowana i nie będzie logowana jako problem. To pozwala na eliminację false positives dla świadomie zaakceptowanych przypadków.

## 📈 Rozszerzalność
Obecnie skaner używa jednego, konkretnego ładunku SQL Injection (' OR 1=1 --). Przykłady rzoszerzeń:
- Pętla po ładunkach: Zamiast jednego SQL_INJECTION_PAYLOAD, stworzenie listy różnych ładunków (np. dla błędów, opartych na czasie, na danych, UNION attacks). Następnie, w funkcji test_sqli iteracja po tej liście, wykonując test dla każdego ładunku.
- Różne typy zapośredniczenia: Obecnie testowane tylko pola JSON. Można dodać obsługę danych formularzy (application/x-www-form-urlencoded), parametrów URL (GET), czy nagłówków
- Analiza typu błędu: Niektóre SQL Injection objawiają się specyficznymi błędami bazy danych. Skaner mógłby analizować komunikaty błędów w odpowiedzi serwera.

