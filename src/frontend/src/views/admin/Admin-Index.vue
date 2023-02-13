<template>
  <Login :show="show"></Login>
</template>

<script setup>
import Login from "@/components/common/LoginComponent.vue";

let show = true
if ('token' in localStorage) {
  show = false
}
</script>

<style scoped>

</style>