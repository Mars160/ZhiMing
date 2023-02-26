<template>
  <el-dialog
      v-model="show"
      :on-close="onClose"
      align-center
      center
      width="400px"
  >
    <el-row :gutter="20">
      <span class="inline-flex w-20 items-center">年级:</span>
      <el-input
          class="w-80"
          v-model="grade"
          placeholder="10代表一(上)、15代表一(下)、20代表二(上)"
      />
    </el-row>
    <el-row :gutter="20" class="mt-10">
      <span class="inline-flex w-20 items-center">练习册名:</span>
      <el-input
          class="w-80"
          v-model="bname"
          placeholder="请输入练习册名"
      />
    </el-row>
    <div class="footer">
      <el-button
          type="danger"
          class="mt-20"
          @click="deleteClicked"
          v-if="type === 'edit'"
      >
        删除
      </el-button>
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
    </div>
  </el-dialog>
</template>

<script setup>
import {defineProps, inject} from 'vue'
import axios from "axios";
import {ElMessage, ElMessageBox} from "element-plus";

const bid = inject("select-bid")
const bname = inject("select-bname")
const grade = inject("select-grade")
const show = inject("showBookUpsertDialog");

const props = defineProps({
  confirmCallback: {
    type: Function,
    default: (bid, bname, grade, type, show) => {
      //const show = inject("showBookUpsertDialog")
      if(type === "add") {
        axios.post('/v1/books', {
          bname: bname,
          grade: grade
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
        axios.put('/v1/books/' + bid, {
          bname: bname,
          grade: grade
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
  type: {
    type: String,
    default: "add"
  },
})

function onClose() {
  grade.value = ''
  bname.value = ""
}

function confirmClicked() {
  props.confirmCallback(bid.value, bname.value, grade.value, props.type, show)
}

function cancelClicked() {
  props.cancelCallback(show)
}

function deleteClicked() {
  ElMessageBox.confirm('此操作将永久删除该练习册, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    axios.delete('/v1/books/' + bid.value).then((res) => {
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
  }).catch(() => {
     console.log("delete canceled")
  })
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