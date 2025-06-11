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