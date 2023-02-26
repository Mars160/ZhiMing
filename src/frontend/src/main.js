import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios";
import locale from 'element-plus/lib/locale/lang/zh-cn'
import 'element-plus/theme-chalk/el-message-box.css'
import 'element-plus/theme-chalk/el-message.css'

axios.interceptors.request.use(
    config => {
        const token = localStorage.getItem("token");
        if (token !== undefined && token !== null) {
            config.headers.Authorization = "Bearer " + localStorage.getItem("token");
        }
        return config;
    }
)

const app = createApp(App)
app.use(router).mount('#app')
//设置默认语言
app.config.globalProperties.$ELEMENT = { locale }
