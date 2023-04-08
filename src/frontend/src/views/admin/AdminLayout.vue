<template>
    <SideMenu>
        <el-menu-item index="/admin/user-manage">
            <el-icon>
                <i-ep-user/>
            </el-icon>
            <span>教师管理</span>
        </el-menu-item>
    </SideMenu>
</template>

<script setup>
import {defineAsyncComponent} from "vue";

const SideMenu = defineAsyncComponent(() => import(
    /* webpackChunkName: "components/side-menu" */
    '@/components/common/SideMenu.vue'
    ))
</script>

<style scoped>

</style>