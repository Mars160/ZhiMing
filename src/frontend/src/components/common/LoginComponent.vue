<template>
  <el-dialog
      v-model="show"
      center
      align-center
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
      title="登录"
      width="320px"
  >
    <el-row :gutter="20">
      <span class="inline-flex w-20 items-center">用户ID:</span>
      <el-input
          class="w-80"
          v-model="user"
          placeholder="请输入用户ID"
      />
    </el-row>
    <el-row :gutter="20" class="mt-10">
      <span class="inline-flex w-20 items-center">密码:</span>
      <el-input
          class="w-80"
          v-model="pwd"
          placeholder="请输入密码"
          show-password
      />
    </el-row>
    <div class="footer">
      <el-button
        type="primary"
        class="mt-20 w-80"
        @click="login"
      >
        登录
      </el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import {defineProps, inject, ref} from 'vue'
import axios from "axios";
import {ElMessage} from "element-plus";

const show = inject('show-login')

const props = defineProps({
  loginCallback: {
    type: Function,
    default: (res_obj) => {
      ElMessage({
        message: res_obj.msg,
        type: 'success'
      })
      setTimeout(() => {
        window.location.reload()
      }, 1000)
    }
  },
  failCallback: {
    type: Function,
    default: (err_str) => {
      ElMessage({
        message: err_str,
        type: 'error',
        showClose: true,
      })
    }
  }
})

// const show_login_dialog = ref(props.show)

const user = ref('')
const pwd = ref('')

function login() {
  const data = {
    user: user.value,
    pwd: pwd.value
  }
  axios.post('/v1/token',
    data
  ).then((res) => {
    const result = res.data
    if (result.code === 0){
      localStorage.setItem('token', result.data)
      window.location.reload()
    } else {
      props.failCallback(result.msg)
    }
  }).catch((err) => {
    props.failCallback(err)
  })
}
</script>

<style scoped>
.inline-flex {
  display: inline-flex;
}

.items-center {
  align-items: center;
}

.w-20 {
  width: 20%;
}

.w-80 {
  width: 80%;
}

.mt-10 {
  margin-top: 10px;
}

.mt-20 {
  margin-top: 20px;
}

.footer {
  text-align: center;
}
</style>