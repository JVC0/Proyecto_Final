import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import ProductPage from '@/views/ProductPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'ProductPage',
    component: ProductPage
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
