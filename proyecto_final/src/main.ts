import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "bootstrap-icons/font/bootstrap-icons";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

authStore.token = localStorage.getItem("token");
authStore.user = JSON.parse(localStorage.getItem("user") || "null");

app.mount("#app");
