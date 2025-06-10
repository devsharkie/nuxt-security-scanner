import getDb from '~/server/utils/db';
import type { User } from '~/types/user';

export default defineEventHandler(async (event) => {
    const { username, password } = await readBody(event);
    
    const db = await getDb();
    // Szukaj tylko użytkownika, który jest adminem.
    const sql = 'SELECT id, username, role FROM users WHERE username = ? AND password = ? AND role = \'admin\'';
    const user: User | undefined = await db.get(sql, [username, password]);

    if (user) {
        return { user };
    }
    
    throw createError({ statusCode: 401, statusMessage: 'Invalid admin credentials' });
});