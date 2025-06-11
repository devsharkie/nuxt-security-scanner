import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';

// db bedzie zapisana w pliku /server/nuxt_security_test.sqlite
const dbFilePath = path.resolve(process.cwd(), 'server', 'nuxt_security_test.sqlite');

let db: Awaited<ReturnType<typeof open>>;

export default async function getDb() {
  if (!db) {
    db = await open({
      filename: dbFilePath,
      driver: sqlite3.Database
    });
  }
  return db;
}