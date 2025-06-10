<script setup lang="ts">
const token = useCookie('auth-token', {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 3600
})
const badtoken = useCookie('session-id', {
  maxAge: 7200
})
</script>
