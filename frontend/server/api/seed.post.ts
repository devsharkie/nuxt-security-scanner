//hardcoding databse only for test purposes
//very very bad practice in real projects

import getDb from '~/server/utils/db';

export default defineEventHandler(async () => {
    if (process.env.NODE_ENV === 'production') {
        throw createError({ statusCode: 403, statusMessage: 'Forbidden' });
    }

    console.log("--- Inicjalizacja bazy danych (SQLite) ---");

    const db = await getDb();

    const sqlSetup = `
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        );
        INSERT INTO users (username, password, role) VALUES
        ('admin', 'supersecretpassword', 'admin'),
        ('user', 'password123', 'user');
    `;

    try {
        await db.exec(sqlSetup);
        return { status: 'success', message: 'Database seeded successfully!' };
    } catch (error: any) {
        throw createError({ statusCode: 500, statusMessage: error.message });
    }
});