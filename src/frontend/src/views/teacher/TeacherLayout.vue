<template>
  <SideMenu>
    <el-menu-item index="/teacher/user-manage">
      <el-icon>
        <i-ep-user/>
      </el-icon>
      <span>学生管理</span>
    </el-menu-item>
    <el-menu-item index="/teacher/book-manage">
      <el-icon>
        <i-ep-user/>
      </el-icon>
      <span>练习册管理</span>
    </el-menu-item>
    <el-menu-item index="/teacher/question-manage">
      <el-icon>
        <i-ep-QuestionFilled />
      </el-icon>
      <span>题目管理</span>
    </el-menu-item>
  </SideMenu>
</template>

<script setup>
import SideMenu from "@/components/common/SideMenu.vue";
</script>

<style scoped>

</style>