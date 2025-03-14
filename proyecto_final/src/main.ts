import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'bootstrap-icons/font/bootstrap-icons';
import axios from 'axios';
import { useAuthStore } from './store/auth'

axios.defaults.baseURL='http://127.0.0.1:8000'
const pinia = createPinia()
const app =createApp(App)
app.use(router)
app.use(pinia)
const authStore = useAuthStore()
authStore.setCsrfToken()
app.mount('#app')
