<template>
  <el-container>
    <el-menu
        v-if="show_menu"
        style="height: 100vh"
        router
    >
      <slot/>
    </el-menu>
    <div v-else>
      <el-button
          type="primary"
          circle
          size="large"
          class="affix"
          @click="show_drawer = !show_drawer"
      >
        <el-icon>
          <i-ep-menu v-show="show_drawer === false"/>
          <i-ep-close v-show="show_drawer"/>
        </el-icon>
      </el-button>
      <el-drawer
          v-model="show_drawer"
          direction="ltr"
          size="100%"
          :with-header="false"
          :show-close="false"
      >
        <el-menu
            router
            style="height: 100vh"
        >
          <slot/>
        </el-menu>
      </el-drawer>
    </div>

    <div class="m-15">
      <router-view/>
    </div>
  </el-container>

</template>

<script setup>
import {ref} from "vue";

const show_drawer = ref(false)
let show_menu = true

//检测是否移动端
if (window.innerWidth < window.innerHeight) {
  show_menu = false
}

</script>

<style scoped>
.m-15 {
  margin: 15px;
}

.affix {
  position: fixed;
  bottom: 100px;
  right: 30px;
  z-index: 2023;
}

el-menu {
  border-right: none;
}
</style>