<template>
  <LoginComponent
      :show="show"
      :login-callback="loginCallback"
  />
    <router-view/>
</template>

<script setup>
import LoginComponent from "@/components/common/LoginComponent.vue";
import axios from "axios";
import {ElMessage} from "element-plus";
import 'element-plus/es/components/message/style/css'
import {ref} from "vue";

const loginCallback = () => {
  axios.get('/v1/role').then((res) => {
    const result = res.data
    if (result.code === 0) {
      const role = result.data
      show.value = false
      if (role === '管理员') {
        //router push
        window.location.href = '#/admin/'
      } else if(role === '教师') {
        window.location.href = '#/teacher/'
      } else if(role === '学生') {
        window.location.href = '#/student/'
      }
    }
  }).catch((err) => {
    ElMessage({
      message: err,
      type: 'error',
      showClose: true,
    })
  })
}

const show = ref(true)
if ('token' in localStorage) {
  loginCallback();
}


</script>

<style scoped>
</style>
