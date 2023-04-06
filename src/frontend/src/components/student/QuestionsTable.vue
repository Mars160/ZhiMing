<template>
    <p>{{ props }}}</p>
</template>

<script setup>
import {defineProps} from "vue";
const props = defineProps({
    source: {
        type: String,
    },
    bid: {
        type: Number,
        default: undefined,
    }
})
</script>

<style scoped>

</style>