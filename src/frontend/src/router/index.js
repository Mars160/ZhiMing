import { createRouter, createWebHashHistory } from 'vue-router'
import AdminLayout from "@/views/AdminLayout.vue";
import AdminTeacherIndex from "@/components/common/AdminTeacherIndex.vue";
import NotFound from "@/components/common/NotFound.vue";
import TeacherManagement from "@/views/admin/TeacherManagement.vue";

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
        path: 'teacher-management',
        component: TeacherManagement,
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
