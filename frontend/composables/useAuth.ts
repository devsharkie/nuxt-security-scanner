import { computed, ref } from 'vue';
import type { User } from '../types/user';

export const useAuth = () => {
    const user = useState<User | null>('user', () => null);

    const login = async (credentials: { username: string, password: string }) => {
        const { data, error } = await useFetch<{ user: User }>('/api/auth/login', {
            method: 'POST',
            body: credentials,
        });
        if (data.value) user.value = data.value.user;
        return { data, error };
    };
    
    const adminLogin = async (credentials: { username: string, password: string }) => {
        const { data, error } = await useFetch<{ user: User }>('/api/auth/admin-login', {
            method: 'POST',
            body: credentials,
        });
        if (data.value) user.value = data.value.user;
        return { data, error };
    };

    const logout = () => {
        user.value = null;
    };

    return {
        user,
        login,
        adminLogin,
        logout,
        isLoggedIn: computed(() => !!user.value),
        isAdmin: computed(() => user.value?.role === 'admin')
    };
};