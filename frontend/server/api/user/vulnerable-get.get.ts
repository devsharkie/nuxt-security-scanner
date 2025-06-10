import getDb from '~/server/utils/db';
import type { User } from '~/types/user';

export default defineEventHandler(async (event) => {
    const query = getQuery(event);
    const userId = query.id;

    // 🚨 PODATNOŚĆ: Bezpośrednie wklejenie ID z URL!
    const sql = `SELECT id, username FROM users WHERE id = ${userId}`;
    console.log(`Executing vulnerable query: ${sql}`);

    try {
        const db = await getDb();
        const data: User[] = await db.all(sql);
        return { data: data };
    } catch(error: any) {
        return { message: 'SQL Error', error: error.message };
    }
});