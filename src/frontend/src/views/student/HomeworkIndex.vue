<template>
    <el-card class="middle-parent">
        <canvas id="homework-canvas" :width="WIDTH" :height="HEIGHT" style="height: 80vh">如果您看到这条消息，说明您的浏览器并不支持canvas绘图</canvas>
        <div style="padding: 14px; text-align: center">
            <span>{{ text }}</span>
        </div>
    </el-card>
</template>

<script setup>
import {onMounted} from "vue";
const WIDTH = 595
const HEIGHT = 842
let text = ''

if(innerHeight > innerWidth) {
    text = '长按保存图片到设备'
} else {
    text = '右键保存图片到设备'
}

onMounted(() => {
    const img = document.getElementById('homework-canvas')
    const ctx = img.getContext('2d')
    ctx.fillStyle = 'rgb(0, 255, 255)'
    ctx.fillRect(0, 0, img.width, img.height)
})

//判断浏览器是更宽还是更高


</script>

<style scoped>
#homework-canvas {
    border: 1px solid #000000;
}

.middle-parent {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>