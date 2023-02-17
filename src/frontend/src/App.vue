<template>
  <LoginComponent
      :login-callback="loginCallback"
  />
    <router-view/>
</template>

<script setup>
import LoginComponent from "@/components/common/LoginComponent.vue";
import axios from "axios";
import {ElMessage} from "element-plus";
import 'element-plus/es/components/message/style/css'
import {provide, ref} from "vue";

const show = ref(true)
provide("show-login", show)

const loginCallback = () => {
  axios.get('/v1/role').then((res) => {
    const result = res.data
    if (result.code === 0) {
      const role = result.data

      if (role === '管理员') {
        //router push
        //如果当前url含有admin，不跳转
        if(window.location.href.includes('admin')) return
        window.location.href = '#/admin/'
      } else if(role === '教师') {
        if (window.location.href.includes('teacher')) return
        window.location.href = '#/teacher/'
      } else if(role === '学生') {
        if (window.location.href.includes('student')) return
        window.location.href = '#/student/'
      }
    }
  }).catch((err) => {
    ElMessage({
      message: err,
      type: 'error',
      showClose: true,
    })
    localStorage.removeItem('token')
    //2s后刷新
    setTimeout(() => {
      window.location.reload()
    }, 2000)
  })
}

if ('token' in localStorage) {
  show.value = false
  loginCallback();
} else {
  show.value = true
}


</script>

<style scoped>
</style>
