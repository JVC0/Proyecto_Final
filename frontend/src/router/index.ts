import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import ProductPage from "@/views/ProductPage.vue";
import LoginPage from "@/views/LoginPage.vue";
import RegisterPage from "@/views/RegisterPage.vue";
import CartPage from "@/views/CartPage.vue";
const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "",
        component: ProductPage,
    },
    {
        path: "/Login",
        name: "LoginPage",
        component: LoginPage,
    },
    {
        path: "/Register",
        name: "RegisterPage",
        component: RegisterPage,
    },
    {
        path: "/Cart",
        name: "CartPage",
        component: CartPage,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
