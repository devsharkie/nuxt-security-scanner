<!-- <template>
  <h1>Dashboard</h1>
  <p v-if="user">Welcome, {{ user.username }}!</p>
  <button @click="handleLogout">Logout</button>
</template>
<script setup lang="ts">
import { navigateTo } from '#app';
import { definePageMeta } from '#imports';
import { useAuth } from '~/composables/useAuth';

definePageMeta({ middleware: 'auth' }); // Używa globalnego middleware
const { user, logout } = useAuth();
async function handleLogout() {
  await logout();
  await navigateTo('/login');
}
</script> -->