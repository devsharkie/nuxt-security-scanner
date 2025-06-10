import { navigateTo, defineNuxtRouteMiddleware, abortNavigation } from '#app';
import { useAuth } from '~/composables/useAuth';

export default defineNuxtRouteMiddleware((to) => {
    const { isLoggedIn, isAdmin } = useAuth();

    // Dostęp do /admin wymaga roli admina
    if (to.path.startsWith('/admin')) {
        if (!isLoggedIn.value) return navigateTo('/login?redirect=' + to.path);
        if (!isAdmin.value) return abortNavigation({ statusCode: 403, statusMessage: 'Forbidden' });
    }

    // Dostęp do /dashboard wymaga bycia zalogowanym
    if (to.path === '/dashboard') {
        if (!isLoggedIn.value) return navigateTo('/login?redirect=' + to.path);
    }
    
    // Zalogowany użytkownik nie powinien widzieć stron logowania
    const loginPages = ['/login', '/management-login'];
    if (loginPages.includes(to.path) && isLoggedIn.value) {
        return navigateTo('/dashboard');
    }
});