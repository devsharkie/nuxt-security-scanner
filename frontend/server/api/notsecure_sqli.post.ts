import getDb from '~/server/utils/db';

export default defineEventHandler(async (event) => {
  const { username } = await readBody(event);

  if (!username) {
    throw createError({ statusCode: 400, message: 'Missing username' });
  }

  const db = await getDb();

  // 🚨 PODATNOŚĆ: Zmienna `username` jest wstawiana bezpośrednio do zapytania.
  // Atakujący może zamknąć cudzysłów i dodać własny kod SQL.
  const query = `SELECT id, username, role FROM users WHERE username = '${username}'`;

  try {
    // Używamy `db.all()` do wykonania zapytania SELECT w bibliotece `sqlite`
    const users = await db.all(query);
    console.log(`Executing vulnerable query: ${query}`);
    return { data: users, query }; // Zwracamy też zapytanie dla celów demonstracyjnych
  } catch (error: any) {
    return { error: error.message, query };
  }
});