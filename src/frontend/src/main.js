import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios";

axios.interceptors.request.use(
    config => {
        const token = localStorage.getItem("token");
        if (token !== undefined && token !== null) {
            config.headers.Authorization = "Bearer " + localStorage.getItem("token");
        }
        return config;
    }
)

createApp(App).use(router).mount('#app')
