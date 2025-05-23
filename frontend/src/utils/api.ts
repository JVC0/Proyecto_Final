import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: true,
});

api.interceptors.request.use((config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
        config.headers.Authorization = `Token ${authStore.token}`;
    }
    return config;
});

export default api;
