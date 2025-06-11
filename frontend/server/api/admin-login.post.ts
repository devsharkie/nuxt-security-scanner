// w prawdziwym życiu dla takiego osobnego endpointa można dodać dodatkowe mechanizmy
// np. whitelisting ip, rygorystyczne limity prób logowania
import getDb from '~/server/utils/db';

export default defineEventHandler(async (event) => {
  const { username, password } = await readBody(event);

  if (!username || !password) 
    throw createError({ statusCode: 400, statusMessage: 'Missing username or password' });
    
  const db = await getDb();

  const user = await db.get('SELECT id, username, password, role FROM users WHERE username = ? AND password = ?', username, password);

  if (!user) 
    throw createError({ statusCode: 401, statusMessage: 'Invalid credentials' });
    
  if (user.role !== 'admin') {
    console.warn(`Non-admin user '${username}' attempted to log in via /api/admin-login.`);
    throw createError({ statusCode: 403, statusMessage: 'Forbidden: Admin access required' });
  }

  return { message: `Admin login successful. Welcome, ${user.username}!`, user: { id: user.id, username: user.username, role: user.role } };
});