<template>
    <el-dialog
            v-model="show"
            :on-close="onClose"
            align-center
            center
    >
        <el-row :gutter="20">
            <span class="inline-flex w-20 items-center">页码:</span>
            <el-input
                    class="w-80"
                    v-model="qpage"
                    placeholder="输入题目所在页码"
            />
        </el-row>
        <el-row :gutter="20" class="mt-10">
            <span class="inline-flex w-20 items-center">位置:</span>
            <el-input
                    class="w-80"
                    v-model="qplace"
                    placeholder="请输入题目在本页位置（第几题），如2"
            />
        </el-row>
        <el-row :gutter="20" class="mt-10">
            <span class="inline-flex w-20 items-center">题目图片:</span>
            <div class="w-80">
                <el-upload action="#"
                           drag
                           auto-upload
                           :before-upload="beforeImageUpload"
                >
                    <div v-if="new_ocr_task" style="max-height: 60px">
                        <el-image
                            :src="img_base64_url"
                            fit="scale-down"
                            style="height: 100%; width: 100%;"
                        />
                    </div>
                    <div v-else>
                        <el-icon class="el-icon-upload"><i-ep-upload-filled /></el-icon>
                        <div class="el-upload__text">
                            拖图片到此 或者 <em>点我上传</em>
                        </div>
                    </div>

                </el-upload>
            </div>
        </el-row>
        <el-row :gutter="20" class="mt-10">
            <span class="inline-flex w-20 items-center">题目:</span>
            <el-input
                    class="w-80"
                    type="textarea"
                    v-model="qname"
                    placeholder="请输入题干"
                    v-loading="ocring"
                    :autosize="{ minRows: 2, maxRows: 7 }"
            />
        </el-row>
        <el-row class="mt-10">
            <span class="inline-flex w-20 items-center">知识点:</span>
            <el-card style="width: 100%;" class="mt-10">
                <el-tag
                        v-for="tag in qpoints"
                        :key="tag"
                        class="mx-1"
                        closable
                        :disable-transitions="false"
                        @close="handleClose(tag)"
                >
                    {{ tag }}
                </el-tag>
                <el-input
                        v-if="inputVisible"
                        id="InputNewTag"
                        v-model="inputValue"
                        class="ml-1 w-20"
                        size="small"
                        @keyup.enter="handleInputConfirm"
                        @blur="handleInputConfirm"
                />
                <el-button v-else class="button-new-tag ml-1" size="small" @click="showInput">
                    + New Tag
                </el-button>
            </el-card>
        </el-row>
        <div class="footer">
            <el-button
                    type="primary"
                    class="mt-20"
                    @click="confirmClicked"
            >
                确认
            </el-button>
            <el-button
                    type="info"
                    class="mt-20"
                    @click="cancelClicked"
            >
                取消
            </el-button>
        </div>
    </el-dialog>
<!--    <CopperDialog :img="img_base64_url" />-->
</template>

<script setup>
import {defineProps, inject, nextTick, provide, ref} from 'vue'
import axios from "axios";
import {ElMessage} from "element-plus";
// import CopperDialog from "@/components/teacher/CopperDialog.vue";

const show = inject("showQuestionUpsertDialog");
const qid = inject("select-qid");
const qname = inject("select-qname");
const qpoints = inject("select-qpoints");
const qpage = inject("select-qpage");
const qplace = inject("select-qplace");
const bid = inject("select-bid")

const inputVisible = ref(false);
const img_base64_url = ref("");
const inputValue = ref("");
const showCopperDialog = ref(false);
const ocring = ref(false);

const new_ocr_task = ref(false);

provide("question-img-url", img_base64_url)
provide("show-copper-dialog", showCopperDialog)

const props = defineProps({
    type: {
        type: String,
        default: "add"
    }
})

function confirmClicked() {
    if (props.type === "edit") {
        axios.put("/v1/questions/" + qid.value.toString(), {
            qname: qname.value,
            point: qpoints.value,
            page: qpage.value,
            place: qplace.value
        }).then(() => {
            ElMessage.success("修改成功");
            show.value = false;
            window.location.reload();
        }).catch(err => {
            ElMessage.error("修改失败", err);
        })
    } else if (props.type === "add") {
        axios.post("/v1/questions", {
            qname: qname.value,
            point: qpoints.value,
            page: qpage.value,
            place: qplace.value,
            bid: bid.value
        }).then(() => {
            ElMessage.success("修改成功");
            show.value = false;
            window.location.reload();
        }).catch(err => {
            ElMessage.error("修改失败", err);
        })
    }
}

function handleClose(tag) {
    qpoints.value.splice(qpoints.value.indexOf(tag), 1);
}

function handleInputConfirm() {
    if (inputValue.value) {
        qpoints.value.push(inputValue.value);
    }
    inputVisible.value = false;
    inputValue.value = "";
}

function showInput() {
    inputVisible.value = true;
    nextTick(() => {
        document.getElementById("InputNewTag").getElementsByTagName("input")[0].focus();
    });
}

function beforeImageUpload(file) {
    //判断file是否为图片
    const fileType = file.type;
    const validType = ['image/jpeg', 'image/png'];
    if (!validType.includes(fileType)) {
        ElMessage.error('上传图片只能是 JPG,PNG 格式!');
        return false;
    } else {
        //转成base64
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (e) {
            img_base64_url.value = e.target.result;
        }

        ocring.value = true;
        //上传图片到/v1/plugin/ocr，并获取返回的data中的uuid
        const formData = new FormData();
        formData.append("file", file);
        axios.post("/v1/plugin/ocr", formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(res => {
            new_ocr_task.value = true;
            const result = res.data;
            if(result.code === 0){
                //每秒轮询/v1/plugin/ocr/{uuid}，直到返回的data中的data不为空或undefined
                const uuid = result.data;
                const timer = setInterval(() => {
                    axios.get("/v1/plugin/ocr/" + uuid).then(res => {
                        const result = res.data;
                        if(result.code === 0){
                            const data = result.data;
                            if(data !== null){
                                new_ocr_task.value = false;
                                clearInterval(timer);
                                if (data.length === 0) {
                                    ElMessage.error("未识别到文字");
                                    ocring.value = false;
                                    return;
                                }
                                //将返回的data中的data赋值给qname
                                let str = ""
                                for (let i = 0; i < data.length; i++) {
                                    str += data[i];
                                }
                                //去除空格
                                str = str.replace(/\s+/g, "");
                                qname.value = str;
                                ocring.value = false;
                            }
                        } else {
                            if(new_ocr_task.value){
                                ElMessage.error(result.msg);
                            }
                            ocring.value = false;
                        }
                    }).catch(err => {
                        if(new_ocr_task.value){
                            ElMessage.error(err);
                        }
                        ocring.value = false;
                    })
                }, 2000);
            }
        }).catch(err => {
            ElMessage.error("上传图片失败", err);
            ocring.value = false;
        })
        return false;
    }
}

function cancelClicked() {
    show.value = false;
}
</script>

<style scoped>
.inline-flex {
    display: inline-flex;
}

.w-20 {
    width: 20%;
}

.items-center {
    align-items: center;
}

.w-80 {
    width: 80%;
}

.mt-20 {
    margin-top: 20px;
}

.footer {
    text-align: center;
}

.mt-10 {
    margin-top: 10px;
}
.el-icon-upload {
    font-size: 50px;
    color: #99a9bf;

}
</style>