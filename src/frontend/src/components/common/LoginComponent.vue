<template>
  <el-dialog
      v-model="show_login_dialog"
      center
      align-center
  >

  </el-dialog>

</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const emits = defineEmits(['show_login_dialog']);
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})
const show_login_dialog = ({
  get: () => props.show,
  set: (value) => emits('update:modelValue', value)
})
</script>

<style scoped>

</style>