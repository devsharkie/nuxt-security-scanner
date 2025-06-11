// UWAGA: W PRAWDZIWEJ APLIKACJI HASEŁ NIE WOLNO PRZECHOWYWAĆ ANI PORÓWNYWAĆ W POSTACI PLAIN TEXT!
// UPROSZCZENIE DO CELOW TESTOWYCH
import { H3Event } from 'h3'; // Ensure H3Event is imported

export function getCredentialsFromHeaders(event: H3Event): { username?: string, password?: string } | null {
  const authHeader = event.node.req.headers['authorization'];

  if (authHeader && authHeader.startsWith('Basic ')) {
    try {
      const credentials = Buffer.from(authHeader.substring(6), 'base64').toString('utf8');
      const [username, password] = credentials.split(':');
      if (username && password) 
          return { username, password };
    } catch (error) {
      console.error("Error decoding Basic Auth header:", error);
      return null;
    }
  }
  return null;
}
