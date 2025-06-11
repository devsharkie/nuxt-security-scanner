// frontend/server/utils/db-initializer.ts
import getDb from '~/server/utils/db';

export async function initializeAndSeedDb() {
    if (process.env.NODE_ENV === 'production') {
        console.warn("Attempted to seed database in production. Skipping.");
        return; // Or throw an error if this behavior is not desired
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
        console.log('Database seeded successfully!');
    } catch (error: any) {
        console.error('Error seeding database:', error.message);
        throw error; // Re-throw to indicate a critical startup failure
    }
}