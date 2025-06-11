import getDb from '~/server/utils/db';
import { getCredentialsFromHeaders } from '~/server/utils/auth';
import { H3Event } from 'h3';

const AUTH_ROUTES = [
  { path: '/api/logged', roles: ['user', 'admin'] },
  { path: '/api/admin', roles: ['admin'] }
];

export default defineEventHandler(async (event: H3Event) => {
  const path = event.node.req.url;

  if (path === '/api/login' || path === '/api/admin-login' || path === '/api/health') {
    return;
  }

  const requiredAuth = AUTH_ROUTES.find(route => path?.startsWith(route.path));

  if (requiredAuth) {
    const credentials = getCredentialsFromHeaders(event);

    if (!credentials || !credentials.username || !credentials.password) {
      console.warn(`Access Denied: Missing Basic Auth credentials for ${path}`);
      throw createError({ statusCode: 401, statusMessage: 'Unauthorized: No credentials provided' });
    }

    const db = await getDb();
    const authenticatedUser = await db.get(
      'SELECT id, username, role FROM users WHERE username = ? AND password = ?',
      credentials.username,
      credentials.password
    );

    if (!authenticatedUser) {
      console.warn(`Access Denied: Invalid Basic Auth credentials for ${path}`);
      throw createError({ statusCode: 401, statusMessage: 'Unauthorized: Invalid credentials' });
    }

    // @ts-ignore
    event.context.auth = authenticatedUser;

    if (requiredAuth.roles.length > 0 && !requiredAuth.roles.includes(authenticatedUser.role)) {
      console.warn(`Access Denied: User '${authenticatedUser.username}' (role: ${authenticatedUser.role}) attempted to access ${path}`);
      throw createError({ statusCode: 403, statusMessage: 'Forbidden: Insufficient permissions' });
      }
    }
});