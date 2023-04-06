<template>
    <el-tabs v-model="activebook" @tab-change="refreshTab">
        <el-tab-pane :label="book.bname" :name="book.bid" v-for="book in books" :key="book.bid" lazy>
            <el-dialog title="选择页码范围" v-model="showdialog" :show-close="false" :close-on-click-modal="false"
                       :close-on-press-escape="false">
                <span>从</span>
                <el-input-number v-model="start" :min="1" :controls="false" :step="1"
                                 style="width: 100px"></el-input-number>
                <span>页到</span>
                <el-input-number v-model="end" :min="1" :controls="false" :step="1"
                                 style="width: 100px"></el-input-number>
                <span>页</span>
                <template #footer>
                    <el-button type="primary" @click="loadQuestion()">确定</el-button>
                </template>
            </el-dialog>
            <el-table
                    style="width: 100%"
                    border
                    height="550"
                    :data="questions"
                    v-if="!showdialog"
                    :default-sort="{prop: 'page', order: 'ascending'}"
                    @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection"/>
                <el-table-column label="题目ID" prop="qid" width="100" sortable v-if="false"/>
                <el-table-column label="题干" prop="qname"/>
                <el-table-column label="页码" prop="page" width="90" default-sort sortable/>
                <el-table-column label="位置" prop="place" width="90" sortable/>
            </el-table>
            <el-button type="primary" @click="submit()">提交</el-button>
        </el-tab-pane>
    </el-tabs>
</template>

<script setup>
import {reactive, ref} from "vue";
import axios from "axios";
import {ElMessage} from "element-plus";

const books = reactive([])
const activebook = ref(0)
const showdialog = ref(true)
const start = ref(1)
const end = ref(1)
const questions = reactive([])
const selected = reactive([])
axios.get("/v1/books").then(res => {
    const data = res.data.data
    for (const book of data) {
        books.push(book)
    }
})

function refreshTab() {
    showdialog.value = true
}

function loadQuestion() {
    showdialog.value = false
    //清空questions
    questions.splice(0, questions.length)
    axios.get("/v1/questions", {
        params: {
            bid: activebook.value,
            pagerange: start.value.toString() + "-" + end.value.toString(),
            limit: 10000
        }
    }).then(res => {
        const data = res.data.data
        for (const question of data) {
            questions.push(question)
        }
    })
}

function submit() {
    const qids = selected.map(question => question.qid)
    console.log(qids)
    axios.post("/v1/homeworks", {
        qids: qids
    }).then((re) => {
        const res = re.data
        if (res.code !== 0)
            ElMessage.error(res.msg)
        else
            ElMessage.success("提交成功")
    })
}

function handleSelectionChange(val) {
    selected.splice(0, selected.length)
    for (const question of val) {
        selected.push(question)
    }
}
</script>

<style scoped>

</style>