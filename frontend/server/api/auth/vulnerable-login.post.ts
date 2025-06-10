import getDb from '~/server/utils/db';
import type { User } from '~/types/user';

export default defineEventHandler(async (event) => {
    const { username, password } = await readBody(event);
    
    // 🚨 PODATNOŚĆ: Bezpośrednie wklejenie danych do zapytania!
    const sql = `SELECT id, username, role FROM users WHERE username = '${username}' AND password = '${password}'`;
    console.log(`Executing vulnerable query: ${sql}`);
    
    try {
        const db = await getDb();
        const user: User | undefined = await db.get(sql);
        if (user) {
            return { message: 'Logged in!', user: user };
        }
        return { message: 'Invalid credentials' };
    } catch (error: any) {
        return { message: 'SQL Error', error: error.message };
    }
});