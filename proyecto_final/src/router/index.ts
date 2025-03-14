import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import ProductPage from '@/views/ProductPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import SignupPage from '@/views/SignupPage.vue'
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: '',
    component: ProductPage
  },
  {
    path: '/Login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/Signup',
    name: 'SignupPage',
    component: SignupPage
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
