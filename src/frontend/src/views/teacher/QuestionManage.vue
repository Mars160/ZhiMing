<template>
    <el-collapse
            v-model="bookName"
            accordion
            @change="getQuestions"
    >
        <el-collapse-item
                v-for="book in books"
                :key="book.bid"
                :name="book.bid"
        >
            <template #title>
                <el-row style="width: 100%">
                    <el-col :span="6">
                        <span>{{ book.bname + ' ' + gradeInt2Str(book.grade) }}</span>
                    </el-col>
                    <el-col :span="18" style="text-align: right; padding-right: 30px">
                        <el-button
                                type="primary"
                                @click="addNewQuestion(book.bid)"
                        >
                            添加题目
                        </el-button>
                    </el-col>
                </el-row>
            </template>
            <el-table
                    style="width: 100%"
                    border
                    height="500"
                    :data="questions[book.bid]"
            >
                <el-table-column type="selection"/>
                <el-table-column label="题目ID" prop="qid" width="100" sortable v-if="false"/>
                <el-table-column label="题干" prop="qname"/>
                <el-table-column label="知识点">
                    <template #default="scope">
                        <el-tag
                                v-for="point in scope.row.points"
                                :key="point"
                                :closable="false"
                                :disable-transitions="false"
                                style="margin-left: 5px"
                                :type="randomTagColor()"
                        >
                            {{ point }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="页码" prop="page" width="90" default-sort sortable/>
                <el-table-column label="位置" prop="place" width="90" sortable/>
                <el-table-column label="编辑" prop="place" width="150">
                    <template #default="scope">
                        <el-button size="small" type="success" @click="editQuestion(scope.row)">编辑</el-button>
                        <el-button size="small" type="danger" @click="deleteQuestion(scope.row.qid)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-collapse-item>
    </el-collapse>

    <QuestionUpsertDialog :type="dialogType"/>
</template>

<script setup>
import {provide, reactive, ref} from 'vue';
import axios from "axios";
import {ElMessage} from "element-plus";
import QuestionUpsertDialog from "@/components/teacher/QuestionUpsertDialog.vue";

sessionStorage.setItem('question_manage_last_bid', -1)

let global_counter = -1
const LIMIT = 1000

const pages = {};
const questions = reactive({});
const bookName = ref('');
const books = ref([]);
const loadDisable = reactive({});

const select_qid = ref('')
const select_qname = ref('')
const select_qpoints = ref([])
const select_qpage = ref('')
const select_qplace = ref('')
const select_bid = ref('')
const showDialog = ref(false)

const dialogType = ref('add')

provide('select-qid', select_qid)
provide('select-qname', select_qname)
provide('select-qpoints', select_qpoints)
provide('select-qpage', select_qpage)
provide('select-qplace', select_qplace)
provide('select-bid', select_bid)
provide('showQuestionUpsertDialog', showDialog)

function editQuestion(question) {
    select_qid.value = question.qid
    select_qname.value = question.qname
    select_qpoints.value = question.points
    select_qpage.value = question.page
    select_qplace.value = question.place
    select_bid.value = question.bid
    dialogType.value = 'edit'
    showDialog.value = true
}

axios.get('/v1/books',
    {
        params: {
            page: 1,
            size: 10
        }
    }
).then((res) => {
    if (res.data.code === 0) {
        books.value = res.data.data
        for (const book of books.value) {
            pages[book.bid] = 1
            questions[book.bid] = ref([])
            loadDisable[book.bid] = true
        }
    } else {
        ElMessage({
            message: res.data.msg,
            type: 'error',
            showClose: true,
        })
    }
})

function gradeInt2Str(gradeInt) {
    const ten = Math.floor(gradeInt / 10)
    const one = gradeInt % 10
    let str = ''
    switch (ten) {
        case 1:
            str = '一'
            break
        case 2:
            str = '二'
            break
        case 3:
            str = '三'
            break
        case 4:
            str = '四'
            break
        case 5:
            str = '五'
            break
        case 6:
            str = '六'
            break
    }
    return str + '年级' + (one === 5 ? ' 上册' : ' 下册')
}

function randomTagColor() {
    const colors = ['', 'success', 'warning', 'danger']
    global_counter += 1
    if (global_counter === colors.length) {
        global_counter = 0
    }
    return colors[global_counter]
}

function addNewQuestion(bid) {
    select_bid.value = bid
    dialogType.value = 'add'
    showDialog.value = true
}

function getQuestions(bid) {
    let page = pages[bid]
    const last_bid = sessionStorage.getItem('question_manage_last_bid')
    if (bid === '' || page === -1) {
        loadDisable[last_bid] = true
        return
    } else if (bid !== bookName.value) {
        loadDisable[last_bid] = true
        loadDisable[bid] = false
    }
    sessionStorage.setItem('question_manage_last_bid', bid)
    axios.get('/v1/questions', {
        params: {
            page: page,
            limit: LIMIT,
            bid: bid,
        }
    }).then(res => {
        const ques = res.data.data
        questions[bid] = questions[bid].concat(ques)
        pages[bid] += 1
        if (ques.length < LIMIT) {
            pages[bid] = -1
        }
    }).catch(err => {
        ElMessage({
            message: err,
            type: 'error',
            showClose: true,
        })
    })
}

function deleteQuestion(qid) {
    axios.delete('/v1/questions/' + qid).then(res => {
        if (res.data.code === 0) {
            ElMessage({
                message: '删除成功',
                type: 'success',
                showClose: true,
            })
            for (const book of books.value) {
                questions[book.bid] = questions[book.bid].filter(q => q.qid !== qid)
            }
        } else {
            ElMessage({
                message: res.data.msg,
                type: 'error',
                showClose: true,
            })
        }
    }).catch(err => {
        ElMessage({
            message: err,
            type: 'error',
            showClose: true,
        })
    })
}
</script>

<style scoped>

</style>