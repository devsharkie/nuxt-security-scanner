import { initializeAndSeedDb } from '~/server/utils/db-initializer'; 

export default defineNitroPlugin(async (nitroApp) => {
  try {
    await initializeAndSeedDb();
    console.log('Database initialization and seeding completed.');
  } catch (e) {
    console.error('Failed to initialize database on startup. Application may not function correctly.', e);
  }
});