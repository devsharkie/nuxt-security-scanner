export default defineEventHandler(async (event) => {
  // @ts-ignore
  const user = event.context.auth; // Access user data from middleware

  if (!user) 
    throw createError({ statusCode: 401, statusMessage: 'Unauthorized' });

  return { message: `Welcome, ${user.username}! You are logged in. Your role is ${user.role}.`, user };
});