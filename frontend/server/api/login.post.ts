import getDb from '~/server/utils/db'; // Make sure this path is correct
import { readBody, createError } from 'h3';

export default defineEventHandler(async (event) => { 
  const { username, password } = await readBody(event); 

  if (!username || !password) 
    throw createError({ statusCode: 400, statusMessage: 'Missing username or password' });

    const db = await getDb();

    const user = await db.get('SELECT id, username, password, role FROM users WHERE username = ? AND password = ?', username, password);

    if (!user) 
      throw createError({ statusCode: 401, statusMessage: 'Invalid credentials' });

    if (user.role === 'admin') {
      console.warn(`Attempted admin login via public /api/login endpoint for user: ${username}`);
      throw createError({ statusCode: 401, statusMessage: 'Invalid credentials' });
    }

    return { message: 'Login successful', user: { id: user.id, username: user.username, role: user.role } };
});