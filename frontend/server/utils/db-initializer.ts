import getDb from '~/server/utils/db';

export async function initializeAndSeedDb() {
  if (process.env.NODE_ENV === 'production') {
    console.warn("Attempted to seed database in production. Skipping.");
    return; 
  }

  const db = await getDb();

  try {
    await db.exec(`DROP TABLE IF EXISTS users`);

    await db.exec(`
      CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
      )
    `);

    await db.exec(`
      INSERT INTO users (username, password, role)
      VALUES ('admin', 'supersecretpassword', 'admin')
    `);

    await db.exec(`
      INSERT INTO users (username, password, role)
      VALUES ('user', 'password123', 'user')
    `);

    await db.exec(`
      INSERT INTO users (username, password, role)
      VALUES ('user_test', 'testpassword', 'user')
    `);
    console.log('Database seeded successfully!');
  } catch (error: any) {
    console.error('Error seeding database:', error.message);
    throw error; 
  }
}