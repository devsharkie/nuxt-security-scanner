import { setCookie } from 'h3'

export default defineEventHandler((event) => {
  setCookie(event, 'debug-mode', 'true', {
    httpOnly: false,
    maxAge: 86400
  })
})
