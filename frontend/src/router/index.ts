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
import AddGroup from "@/views/AddGroup.vue"
import EditProfile from "@/views/EditProfile.vue";
import RecipeList from "@/views/RecipeList.vue";
import RecipeDetail from "@/views/RecipeDetail.vue";
import AddRecipe from "@/views/AddRecipe.vue"
const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "ProductPage",
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
        path: "/Profile/:username/edit",
        name: "EditProfilePage",
        component: EditProfile,
    },
    {
        path: "/Profile/:username/groups/",
        name: "GroupPage",
        component: GroupPage,
    },
    {
        path: "/Profile/:username/groups/:id",
        name: "GroupDetail",
        component: GroupDetail,
    },
    {
        path: "/Cart/payment",
        name: "PaymentPage",
        component: PaymentPage,
    },
    {
        path: "/Profile/:username/groups/add",
        name: "AddGroup",
        component: AddGroup,
    },
    {
        path: "/Recipes/",
        name: "RecipeList",
        component: RecipeList,
    },
    {
        path: "/Recipes/:id",
        name: "RecipeDetail",
        component: RecipeDetail,
    },
    {
        path: "/Recipes/add",
        name: "AddRecipe",
        component: AddRecipe,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
