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
      <span class="inline-flex w-20 items-center">题目:</span>
      <el-input
          class="w-80"
          v-model="qname"
          placeholder="请输入题干"
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
</template>

<script setup>
import {defineProps, inject, ref, nextTick} from 'vue'
import axios from "axios";
import {ElMessage} from "element-plus";

const show = inject("showQuestionUpsertDialog");
const qid = inject("select-qid");
const qname = inject("select-qname");
const qpoints = inject("select-qpoints");
const qpage = inject("select-qpage");
const qplace = inject("select-qplace");
const bid = inject("select-bid")

const inputVisible = ref(false);
const inputValue = ref("");

const props = defineProps({
  type: {
    type: String,
    default: "add"
  }
})

function confirmClicked() {
  if(props.type === "edit") {
    axios.put("/v1/questions/" + qid.value.toString(), {
      qname: qname.value,
      point: qpoints.value,
      page: qpage.value,
      place: qplace.value
    }).then(() => {
      ElMessage.success("修改成功");
      show.value = false;
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