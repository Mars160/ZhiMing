<template>
    <el-table
            style="width: 100%"
            border
            height="550"
            :data="questions"
            :default-sort="{prop: 'page', order: 'ascending'}"
            @selection-change="handleSelectionChange"
    >
        <el-table-column type="selection"/>
        <el-table-column label="序号" prop="index" width="100" sortable v-if="false"/>
        <el-table-column label="题干" prop="qname"/>
    </el-table>
    <el-button type="primary" @click="submit()">提交</el-button>
</template>

<script setup>
import axios from "axios";
import {reactive} from "vue";
import {ElMessage} from "element-plus";

const questions = reactive([])
const selected = reactive([])

axios.get('/v1/homeworks').then((res) => {
    const data = res.data
    if (data.code !== 0) {
        ElMessage.error(data.msg)
        return
    }
    //转data列表为字典
    for (let i = 0; i < data.data.length; i++) {
        questions.push({
            qid: data.qids[i],
            qname: data.data[i]
        })
    }
}).catch((err) => {
    ElMessage.error(err)
})

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