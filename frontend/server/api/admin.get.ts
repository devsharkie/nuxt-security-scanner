export default defineEventHandler(async (event) => {
  // @ts-ignore
  const user = event.context.auth; // Access user data from middleware

  if (!user || user.role !== 'admin') {
    throw createError({ statusCode: 403, statusMessage: 'Forbidden: Admin access required' });
  }

  return { message: `Welcome, Admin ${user.username}! This is a highly restricted area.`, user };
});