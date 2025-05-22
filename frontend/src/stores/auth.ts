import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/utils/api";
import { useRouter } from "vue-router";
import { useMessageStore } from '@/stores/message';
interface User {
    id: number;
    username: string;
    email: string;
}

const getCsrfToken = (): string | null => {
    const cookieValue = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return cookieValue || null;
};

export const useAuthStore = defineStore("auth", () => {
    const token = ref<string | null>(localStorage.getItem("token") || null);
    const user = ref<User | null>(
        JSON.parse(localStorage.getItem("user") || "null")
    );
    const router = useRouter();
    const isAuthenticated = computed(() => !!token.value);

    const makeAuthenticatedRequest = async (url: string, data: any) => {
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            throw new Error("CSRF token not found.");
        }

        const response = await api.post(url, data, {
            headers: {
                "X-CSRFToken": csrfToken,
            },
        });
        return response;
    };



    const login = async (username: string, password: string) => {
        const messageStore = useMessageStore();

        try {
            const response = await makeAuthenticatedRequest("/api/auth/login/", {
                username,
                password
            });
            if (response.status === 200) {
                token.value = response.data.token;
                user.value = response.data.user;
                localStorage.setItem("token", token.value || "");
                localStorage.setItem("user", JSON.stringify(user.value));

                if (response.data.message) {
                    messageStore.setMessage(response.data.message);
                }
                router.push("/");
                return;
            }
        } catch (error: any) {
            if (error.response?.data?.message) {
                messageStore.setMessage(error.response.data.message, true);
            } else {
                messageStore.setMessage("Login failed. Please try again.", true);
            }
        }
    };

    const register = async (
        email: string,
        username: string,
        password: string
    ) => {
        try {
            const response = await makeAuthenticatedRequest(
                "/api/auth/register/",
                {
                    email,
                    username,
                    password,
                }
            );
            if (response.data.message) {
                router.push("/login");
            }
        } catch (error) {
            console.error("Registration failed", error);
            throw error;
        }
    };

    const logout = () => {
        token.value = null;
        user.value = null;
        localStorage.removeItem("token");
        localStorage.removeItem("user");
    };

    return { token, user, isAuthenticated, login, register, logout };
});
