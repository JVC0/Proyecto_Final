import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/utils/api";
import { useRouter } from "vue-router";
interface User {
    id: number;
    username: string;
    email: string;
}

export const useAuthStore = defineStore("auth", () => {
    const token = ref<string | null>(localStorage.getItem("token") || null);
    const user = ref<User | null>(
        JSON.parse(localStorage.getItem("user") || "null")
    );
    const router = useRouter();
    const isAuthenticated = computed(() => !!token.value);

    const login = async (email: string, password: string) => {
        try {
            const response = await api.post("/api/auth/login/", {
                email,
                password,
            });
            token.value = response.data.token;
            user.value = response.data.user;
            localStorage.setItem("token", token.value || "");
            localStorage.setItem("user", JSON.stringify(user.value));
            router.push("/");
        } catch (error) {
            console.error("Login failed", error);
            throw error;
        }
    };

    const logout = () => {
        token.value = null;
        user.value = null;
        localStorage.removeItem("token");
        localStorage.removeItem("user");
    };

    return { token, user, isAuthenticated, login, logout };
});
