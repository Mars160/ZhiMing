import {createRouter, createWebHashHistory} from 'vue-router'

import {defineAsyncComponent} from "vue";

const AdminLayout = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/admin-layout" */
    "@/views/admin/AdminLayout.vue"
    ))
const CommonIndex = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/common-index" */
    "@/views/common/CommonIndex.vue"
    ))
const NotFound = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/not-found" */
    "@/views/common/NotFound.vue"
    ))
const UserManage = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/user-manage" */
    "@/views/common/UserManage.vue"
    ))
const TeacherLayout = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/teacher-layout" */
    "@/views/teacher/TeacherLayout.vue"
    ))
const BookManage = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/book-manage" */
    "@/views/teacher/BookManage.vue"
    ))
const QuestionManage = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/question-manage" */
    "@/views/teacher/QuestionManage.vue"
    ))
const StudentLayout = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/student-layout" */
    "@/views/student/StudentLayout.vue"
    ))
const HomeworkIndex = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/homework-index" */
    "@/views/student/HomeworkIndex.vue"
    ))
const QuestionUpload = defineAsyncComponent(() => import(
    /* webpackChunkName: "views/question-upload" */
    "@/views/student/QuestionUpload.vue"
    ))




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
