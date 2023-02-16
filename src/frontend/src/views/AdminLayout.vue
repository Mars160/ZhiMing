<template>
  <SideMenu>
    <el-menu-item index="teacher-management">
      <el-icon>
        <i-ep-user/>
      </el-icon>
      <span>教师管理</span>
    </el-menu-item>
  </SideMenu>
</template>

<script setup>
import SideMenu from "@/components/common/SideMenu.vue";
</script>

<style scoped>
.el-menu-item{
  justify-content: center;
}
</style>