<template>
    <el-dialog v-model="show" title="请选择作业来源" align-center>
        <el-radio-group v-model="source" class="mt-10">
            <el-radio label="teacher">来自老师布置</el-radio>
            <el-radio label="zhiming">来自本系统</el-radio>
        </el-radio-group>
        <template #footer>
            <el-button type="primary" class="mt-10" @click="show = false">确定</el-button>
        </template>
    </el-dialog>

    <HomeworkByTeacher v-if="source === 'teacher' && show === false"/>
    <HomeworkByZhiming v-if="source === 'zhiming' && show === false"/>
</template>

<script setup>
import HomeworkByTeacher from "@/components/student/HomeworkByTeacher.vue";
import HomeworkByZhiming from "@/components/student/HomeworkByZhiming.vue";
import {ref} from "vue";

const show = ref(true)
const source = ref("none")
</script>

<style scoped>

</style>