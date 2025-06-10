import getDb from '~/server/utils/db';
import type { User } from '~/types/user';

export default defineEventHandler(async (event) => {
    const { username, password } = await readBody(event);
    if (!username || !password) {
        throw createError({ statusCode: 400, statusMessage: 'Missing credentials' });
    }

    const db = await getDb();
    const sql = 'SELECT id, username, role FROM users WHERE username = ? AND password = ?';
    const user: User | undefined = await db.get(sql, [username, password]);

    if (user) {
        // ✅ BLOKADA: Nie pozwól adminowi zalogować się przez publiczny formularz.
        if (user.role === 'admin') {
            console.warn(`SECURITY ALERT: Admin login attempt from public form for user '${username}'`);
            throw createError({ statusCode: 401, statusMessage: 'Invalid credentials' });
        }
        return { user };
    }

    throw createError({ statusCode: 401, statusMessage: 'Invalid credentials' });
});