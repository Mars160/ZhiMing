<template>
  <el-container>
    <el-menu
        v-if="show_menu"
        style="height: 100vh;width:200px;"
        router
        background-color="#001529"
        text-color="hsla(0, 0%, 100%, .65)"
        active-text-color="#fff"
        class = "el-menu-vertical"
        :default-active="path"
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
            background-color="#001529"
            text-color="hsla(0, 0%, 100%, .65)"
            active-text-color="#fff"
        >
          <slot/>
        </el-menu>
      </el-drawer>
    </div>

    <div class="m-15 fill">
      <router-view/>
    </div>
  </el-container>

</template>

<script setup>
import {ref} from "vue";
import {useRoute} from "vue-router";

const route = useRoute()
const path = route.path

const show_drawer = ref(false)
let show_menu = true

//检测是否移动端
if (window.innerWidth < window.innerHeight) {
  show_menu = false
}

</script>

<style>
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

.el-menu-item.is-active {
  background-color: #1890ff !important;
}

.el-menu-item{
  justify-content: center;
}

.el-menu-vertical {
  width: 200px;
  height: 100%;
}

ul {
  border-right-width: 0;
}

.fill {
  width: 100%;
  height: 100%;
}
</style>