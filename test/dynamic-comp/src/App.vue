<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <DyComponent />
</template>

<script setup>
import { defineAsyncComponent } from "vue";

const DyComponent = defineAsyncComponent(() => {
  const choice = Math.round(Math.random());
  if (choice === 0)
    return import(
      /* webpackChunkName: "components/hello-world" */
      '@/components/HelloWorld.vue'
    )
  else
    return import(
      /* webpackChunkName: "components/fuck-world" */
      '@/components/FuckWorld.vue'
    )
}
)
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
