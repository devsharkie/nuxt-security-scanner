// frontend/server/api/health.ts
export default defineEventHandler(() => {
  return { status: 'ok', timestamp: new Date().toISOString(), service: 'frontend' };
});