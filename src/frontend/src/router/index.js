import { createRouter, createWebHashHistory } from 'vue-router'
import AdminLayout from "@/views/admin/AdminLayout.vue";
import AdminTeacherIndex from "@/components/common/AdminTeacherIndex.vue";
import NotFound from "@/components/common/NotFound.vue";
import UserManage from "@/views/common/UserManage.vue";

const routes = [
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: 'index',
        component: AdminTeacherIndex,
        alias: ['']
      },
      {
        path: 'user-manage',
        component: UserManage,
      }
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    component: NotFound,
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
