// frontend/server/plugins/db-setup.ts
import { initializeAndSeedDb } from '~/server/utils/db-initializer'; // Adjust path if needed

export default defineNitroPlugin(async (nitroApp) => {
  console.log('Running database initialization on server startup...');
  try {
    await initializeAndSeedDb();
    console.log('Database initialization and seeding completed.');
  } catch (e) {
    console.error('Failed to initialize database on startup. Application may not function correctly.', e);
    // In a critical application, you might want to process.exit(1) here
    // to prevent the server from starting with a broken database.
    // For development/testing, just logging the error might be sufficient.
  }
});