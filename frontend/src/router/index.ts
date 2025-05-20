import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import ProductPage from "@/views/ProductPage.vue";
import LoginPage from "@/views/LoginPage.vue";
import RegisterPage from "@/views/RegisterPage.vue";
import CartPage from "@/views/CartPage.vue";
import ProductDetail from "@/views/ProductDetail.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import GroupPage from "@/views/GroupPage.vue"
import GroupDetail from "@/views/GroupDetail.vue";
import PaymentPage from "@/views/PaymentPage.vue";
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
    {
        path: "/Product/:slug",
        name: "ProductDetail",
        component: ProductDetail,
    },
    {
        path: "/Profile/:username",
        name: "ProfilePage",
        component: ProfilePage,
    },
    {
        path: "/Profile/:username/groups/",
        name: "GroupPage",
        component: GroupPage,
    },
    {
    path: "/Cart/payment",
        name: "PaymentPage",
        component: PaymentPage,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
