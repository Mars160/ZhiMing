<template>
    <el-dialog title="图片剪裁" v-model="show" class="crop-dialog" append-to-body>
        <div class="cropper-content">
            <div class="cropper" style="text-align:center">
                <vue-cropper
                        ref="cropper"
                        :img="props.img"

                />
            </div>
        </div>
        <div class="action-box">
            <el-button type="primary" plain @click="clearImgHandle">清除图片</el-button>
            <el-button type="primary" plain @click="rotateLeftHandle">左旋转</el-button>
            <el-button type="primary" plain @click="rotateRightHandle">右旋转</el-button>
            <el-button type="primary" plain @click="changeScaleHandle(1)">放大</el-button>
            <el-button type="primary" plain @click="changeScaleHandle(-1)">缩小</el-button>
            <el-button type="primary" plain @click="downloadHandle('blob')">下载</el-button>
        </div>
        <template #footer>
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="finish" :loading="loading">确认</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import {ref, reactive, inject, defineProps} from 'vue'
import VueCropper from 'vue-cropper'
import 'vue-cropper/dist/index.css'

const show = inject('show-copper-dialog')
const props = defineProps({
    img: {
        type: String,
        required: true
    }
})

// eslint-disable-next-line no-unused-vars
const option = reactive({
    img: inject('question-img-url'),
    size: 1,
    outputType: 'jpg',
    full: false,
    canMove: true,
    canMoveBox: true,
    original: false,
    autoCrop: true,
    fixed: false,
    fixedNumber: [16, 9],
    centerBox: true,
    infoTrue: true,
    fixedBox: false,
    autoCropWidth: 100,
    autoCropHeight: 100,
})
const loading = ref(false)
</script>

<style scoped>

</style>