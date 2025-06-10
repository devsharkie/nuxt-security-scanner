<template>
  <h1>Admin Login</h1>
  <form @submit.prevent="handleLogin">
    <input v-model="username" placeholder="Admin Username" /><br/>
    <input v-model="password" type="password" placeholder="Password" /><br/>
    <button type="submit">Admin Login</button>
    <p v-if="errorMsg" style="color:red;">{{ errorMsg }}</p>
  </form>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { navigateTo } from '#app';

const { adminLogin } = useAuth();
const username = ref('');
const password = ref('');
const errorMsg = ref('');

async function handleLogin() {
    const { error } = await adminLogin({ username: username.value, password: password.value });
    if (error.value) {
        errorMsg.value = error.value.data?.statusMessage || 'An unexpected error occurred.';
    }
    else {
        await navigateTo('/admin');
    }
}
</script>