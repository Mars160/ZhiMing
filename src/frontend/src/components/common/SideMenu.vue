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
      <el-button
          class = "el-menu-item"
          color="#001529"
        @click="logout"
      >
        <el-icon>
          <i-ep-circle-close/>
        </el-icon>
        <span>登出</span>
      </el-button>
        <el-button
                class = "el-menu-item"
                color="#001529"
                @click="editPwd"
        >
            <el-icon>
                <i-ep-edit/>
            </el-icon>
            <span>修改密码</span>
        </el-button>
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
          size="101%"
          :with-header="false"
          :show-close="false"
      >
        <el-menu
            router
            style="height: 100vh"
            background-color="#001529"
            text-color="hsla(0, 0%, 100%, .65)"
            active-text-color="#fff"
            class="el-menu-drawer"
            :default-active="path"
            @select="close_menu"
        >
          <slot/>
          <el-button
              class = "el-menu-item"
              color="#001529"
              @click="logout"
          >
            <el-icon>
              <i-ep-circle-close/>
            </el-icon>
            <span>登出</span>
          </el-button>
            <el-button
                    class = "el-menu-item"
                    color="#001529"
                    @click="editPwd"
            >
                <el-icon>
                    <i-ep-edit/>
                </el-icon>
                <span>修改密码</span>
            </el-button>
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
import {ElMessageBox} from "element-plus";
import axios from "axios";

const route = useRoute()
const path = route.path

const show_drawer = ref(false)
let show_menu = true

//检测是否移动端
if (window.innerWidth < window.innerHeight) {
  show_menu = false
}

function logout() {
  localStorage.removeItem('token')
  window.location.reload()
}

function close_menu() {
  show_drawer.value = false
}

function editPwd() {
    ElMessageBox.prompt('请输入新的密码', '密码修改', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
    }).then((value) => {
        axios.put('/v1/users/' + localStorage.getItem('uid'), {
            pwd: value.value
        }).then(res => {
            if (res.data.code === 0) {
                ElMessageBox.alert('密码修改成功', '密码修改', {
                    confirmButtonText: '确定',
                }).then(() => {
                    logout()
                })
            } else {
                ElMessageBox.alert('密码修改失败', '密码修改', {
                    confirmButtonText: '确定',
                })
            }
        })
    })
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
  width: 100%;

    margin-left: 0 !important;
}

.el-menu-vertical {
  width: 200px;
  height: 100%;
}

.el-menu-drawer {
  width: 100%;
  height: 100%;
}

ul {
  border-right-width: 0;
}

.fill {
  width: 100%;
  height: 100%;
}

.el-drawer__body {
  padding: 0;
}
</style>