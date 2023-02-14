<template>
  <Login :show="show"></Login>
  <SiderLayout></SiderLayout>
</template>

<script setup>
import Login from "@/components/common/LoginComponent.vue";
import SiderLayout from "@/components/common/SiderLayout.vue";

let show = true
if ('token' in localStorage) {
  show = false
}
</script>

<style scoped>

</style>