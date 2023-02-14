import { createRouter, createWebHashHistory } from 'vue-router'
import AdminIndex from "@/views/admin/AdminIndex.vue";
import HelloWorld from "@/components/HelloWorld.vue";

const routes = [
  {
    path: '/admin',
    component: AdminIndex,
    children: [
      {
        path: 'hello',
        component: HelloWorld,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
