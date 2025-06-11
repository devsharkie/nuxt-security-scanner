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