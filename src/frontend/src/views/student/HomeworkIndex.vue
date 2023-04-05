<template>
    <el-card class="middle-parent">
        <canvas id="homework-canvas" :width="WIDTH" :height="HEIGHT">如果您看到这条消息，说明您的浏览器并不支持canvas绘图，请在其他设备上打开本网站。</canvas>
        <img class="canvas-img" />
        <div style="padding: 14px; text-align: center">
            <p>{{ text }}</p>
            <el-row class="middle-row">
                <el-button type="primary" @click="drawPrevQuestions()" :disabled="pageIndex <= 1">上一页</el-button>
                <el-button type="primary" @click="drawNextQuestions()" :disabled="pageIndex >= totalPage">下一页</el-button>
            </el-row>
        </div>
    </el-card>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axios  from "axios";
import {ElMessage} from "element-plus";
const WIDTH = 2480
const HEIGHT = 3508
const EACH_PAGE = 5
const MARGIN = 170
const FONT_SIZE = 25
const FONT = FONT_SIZE.toString() + 'px serif'
const EACH_HEIGHT = Math.ceil((HEIGHT - MARGIN * 2) / EACH_PAGE)
const BACKGROUND_COLOR = 'rgb(255, 255, 255)'

const questions = []
const pageIndex = ref(0)
const totalPage = ref(0)
let text = '右键保存图片到设备'
let img = null
let ctx = null

if(innerHeight > innerWidth) {
    text = '长按保存图片到设备'
}

onMounted(() => {
    img = document.getElementById('homework-canvas')
    ctx = img.getContext('2d')
    ctx.fillStyle = BACKGROUND_COLOR
    ctx.fillRect(0, 0, img.width, img.height)

    axios.get('/v1/homeworks').then((res) => {
        const data = res.data
        if (data.code !== 0) {
            ElMessage.error(data.msg)
            return
        }
        questions.push(...data.data)
        totalPage.value = Math.ceil(questions.length / EACH_PAGE)

        drawNextQuestions()

    }).catch((err) => {
        ElMessage.error(err)
    })
})

function drawNextQuestions() {
    ctx.fillStyle = BACKGROUND_COLOR
    ctx.fillRect(0, 0, img.width, img.height)
    ctx.fillStyle = 'rgb(0, 0, 0)'
    ctx.font = FONT
    for(let num = pageIndex.value * EACH_PAGE + 1; num <= (pageIndex.value + 1) * EACH_PAGE; num++) {
        const qname = questions[num - 1]
        if (qname === undefined) {
            break
        }
        const y = (num - pageIndex.value * EACH_PAGE - 1) * EACH_HEIGHT + FONT_SIZE + MARGIN
        ctx.fillText(`${num}. ${qname}`, MARGIN, y)
    }
    pageIndex.value++
    canvasToImg()
}

function drawPrevQuestions() {
    if (pageIndex.value <= 1) {
        return
    }
    const prevPage = pageIndex.value - 2
    ctx.fillStyle = BACKGROUND_COLOR
    ctx.fillRect(0, 0, img.width, img.height)
    ctx.fillStyle = 'rgb(0, 0, 0)'
    ctx.font = FONT
    for(let num = prevPage * EACH_PAGE + 1; num <= (prevPage + 1) * EACH_PAGE; num++) {
        const qname = questions[num - 1]
        if (qname === undefined) {
            break
        }
        const y = (num - prevPage * EACH_PAGE - 1) * EACH_HEIGHT + FONT_SIZE + MARGIN
        ctx.fillText(`${num}. ${qname}`, MARGIN, y)
    }
    pageIndex.value--
    canvasToImg()
}

function canvasToImg() {
    let actualLeft = img.offsetLeft
    let actualTop = img.offsetTop
    let current = img.offsetParent
    while (current !== null) {
        actualLeft += current.offsetLeft
        actualTop += current.offsetTop
        current = current.offsetParent
    }
    const image = new Image()
    const imageWidth = img.scrollWidth + 'px'
    const imageHeight = img.scrollHeight + 'px'
    image.src = img.toDataURL('image/png')
    image.style.width = imageWidth
    image.style.height = imageHeight
    image.style.position = 'absolute'
    image.style.left = actualLeft + 'px'
    image.style.top = actualTop + 'px'
    image.style.opacity = '0'
    document.body.appendChild(image)
    return image
}
</script>

<style scoped>
#homework-canvas {
    border: 1px solid #000000;
    max-height: 100%;
    max-width: 100%;
}

.middle-parent {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
}

.middle-row {
    display: flex;
    justify-content: center;
    align-items: center;
}

.canvas-img {
    opacity: 0;
}
</style>