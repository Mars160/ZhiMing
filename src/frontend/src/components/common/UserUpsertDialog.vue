<template>
    <el-dialog
            v-model="show"
            :on-close="onClose"
            align-center
            center
            width="320px"
    >
        <el-row :gutter="20" v-if="type === 'edit'">
            <span class="inline-flex w-20 items-center">用户ID:</span>
            <el-input
                    class="w-80"
                    v-model="uid"
                    placeholder="请输入用户ID"
            />
        </el-row>
        <el-row :gutter="20" class="mt-10">
            <span class="inline-flex w-20 items-center">用户名:</span>
            <el-input
                    class="w-80"
                    v-model="nickname"
                    placeholder="请输入用户名"
            />
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
                    type="danger"
                    class="mt-20"
                    @click="cancelClicked"
            >
                取消
            </el-button>
            <el-button
                    type="success"
                    class="mt-20"
                    @click="resetPwdClicked"
                    v-if="type === 'edit'"
            >
                重置密码
            </el-button>
        </div>
    </el-dialog>
</template>

<script setup>
import {defineProps, inject} from 'vue'
import axios from "axios";
import {ElMessage} from "element-plus";

const uid = inject("select-uid")
const nickname = inject("select-nickname")
const show = inject("showAddUserDialog")

const props = defineProps({
    confirmCallback: {
        type: Function,
        default: (uid, nickname, type, show) => {
            if (type === "add") {
                axios.post('/v1/users', {
                    nickname: nickname
                }).then((res) => {
                    const data = res.data
                    if (data.code === 0) {
                        ElMessage.success(data.msg)
                        //1s后刷新页面
                        setTimeout(() => {
                            window.location.reload()
                        }, 1000)
                    } else {
                        ElMessage.error(data.msg)
                    }
                }).catch((err) => {
                    ElMessage.error(err)
                })
            } else if (type === "edit") {
                axios.put('/v1/users/' + uid, {
                    nickname: nickname
                }).then((res) => {
                    const data = res.data
                    if (data.code === 0) {
                        ElMessage.success(data.msg)
                        setTimeout(() => {
                            window.location.reload()
                        }, 1000)
                    } else {
                        ElMessage.error(data.msg)
                    }
                }).catch((err) => {
                    ElMessage.error(err)
                })
            }
            show.value = false
        }
    },
    cancelCallback: {
        type: Function,
        default: (show) => {
            show.value = false
        }
    },
    resetPwdCallback: {
        type: Function,
        // eslint-disable-next-line no-unused-vars
        default: (uid) => {
            axios.put('/v1/users/' + uid,
                {
                    pwd: null
                }).then((res) => {
                const data = res.data
                if (data.code === 0) {
                    ElMessage.success(data.msg)
                    setTimeout(() => {
                        window.location.reload()
                    }, 1000)
                } else {
                    ElMessage.error(data.msg)
                }
            }).catch((err) => {
                ElMessage.error(err)
            })
        }
    },
    type: {
        type: String,
        default: "add"
    },
})

function onClose() {
    uid.value = ''
    nickname.value = ""
}

function confirmClicked() {
    props.confirmCallback(uid.value, nickname.value, props.type, show)
}

function cancelClicked() {
    props.cancelCallback(show)
}

function resetPwdClicked() {
    props.resetPwdCallback(uid.value, nickname.value, props.type)
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
</style>