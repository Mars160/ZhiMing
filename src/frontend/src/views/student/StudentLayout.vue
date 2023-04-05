<template>
  <SideMenu>
      <el-menu-item index="/student/questions-download">
          <el-icon>
              <i-ep-edit-pen />
          </el-icon>
          <span>下载新题</span>
      </el-menu-item>
    <el-menu-item index="/student/questions-upload">
      <el-icon>
        <i-ep-finished />
      </el-icon>
      <span>上传错题</span>
    </el-menu-item>
  </SideMenu>
</template>

<script setup>
import SideMenu from "@/components/common/SideMenu.vue";
</script>

<style scoped>

</style>