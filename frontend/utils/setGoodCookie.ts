import { setCookie } from 'h3'

export default defineEventHandler((event) => {
  setCookie(event, 'user-token', 'abc123', {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 3600
  })
})
