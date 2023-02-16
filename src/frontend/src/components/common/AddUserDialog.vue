<template>
 <el-dialog
     :v-model="props.show"
 >
   <el-row :gutter="20">
     <span class="inline-flex w-20 items-center">用户ID:</span>
     <el-input
         class="w-80"
         v-model="id"
         placeholder="请输入用户ID"
     />
   </el-row>
   <el-row :gutter="20" class="mt-10">
     <span class="inline-flex w-20 items-center">用户名:</span>
     <el-input
         class="w-80"
         v-model="username"
         placeholder="请输入用户名"
     />
   </el-row>
   <div class="footer">
     <el-button
         type="primary"
         class="mt-20 w-80"
         @click="props.confirmCallback"
     >
       确认
     </el-button>
     <el-button
         type="danger"
         class="mt-20 w-80"
         @click="props.cancelCallback"
      >
       取消
      </el-button>
     </div>
 </el-dialog>
</template>

<script setup>
import {defineProps} from 'vue'

const props = defineProps({
 show: {
   type: Boolean,
   default: true
 },
  confirmCallback: {
    type: Function,
    default: () => {
      this.show = false
      console.log("confirm")
    }
  },
  cancelCallback: {
    type: Function,
    default: () => {
      this.show = false
      console.log("cancel")

    }
  }
})
</script>

<style scoped>

</style>