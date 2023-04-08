import {createRouter, createWebHashHistory} from 'vue-router'
import AdminLayout from "@/views/admin/AdminLayout.vue";
import CommonIndex from "@/views/common/CommonIndex.vue";
import NotFound from "@/views/common/NotFound.vue";
import UserManage from "@/views/common/UserManage.vue";
import TeacherLayout from "@/views/teacher/TeacherLayout.vue";
import BookManage from "@/views/teacher/BookManage.vue";
import QuestionManage from "@/views/teacher/QuestionManage.vue";
import StudentLayout from "@/views/student/StudentLayout.vue";
import HomeworkIndex from "@/views/student/HomeworkIndex.vue";
import QuestionUpload from "@/views/student/QuestionUpload.vue";

const routes = [
    {
        path: '/admin',
        component: AdminLayout,
        children: [
            {
                path: 'index',
                component: CommonIndex,
                alias: ['']
            },
            {
                path: 'user-manage',
                component: UserManage,
            }
        ],
    },
    {
        path: '/teacher',
        component: TeacherLayout,
        children: [
            {
                path: 'index',
                component: CommonIndex,
                alias: ['']
            },
            {
                path: 'user-manage',
                component: UserManage,
            },
            {
                path: 'book-manage',
                component: BookManage,
            },
            {
                path: 'question-manage',
                component: QuestionManage,
            }
        ],
    },
    {
        path: '/student',
        component: StudentLayout,
        children: [
            {
                path: 'index',
                component: CommonIndex,
                alias: ['']
            },
            {
                path: 'questions-download',
                component: HomeworkIndex,
            },
            {
                path: 'questions-upload',
                component: QuestionUpload,
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
