<template>
  <el-collapse
    v-model="bookName"
    accordion
  >
    <el-collapse-item
      v-for="book in books"
      :key="book.bid"
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
            <el-button
              type="danger"
              @click="deleteSelectedQuestions"
            >
              删除所选
            </el-button>
          </el-col>
        </el-row>
      </template>
     <el-table
      style="width: 100%"
      height="500"
      border
      :data="fakeQuestions"
     >
       <el-table-column type="selection"/>
      <el-table-column label="题目ID" prop="qid" width="100" sortable/>
      <el-table-column label="题干" prop="qname"/>
       <el-table-column label="知识点">
         <template #default="scope">
            <el-tag
              v-for="point in scope.row.point"
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
       <el-table-column label="编辑" prop="place" width="70">
         <template #default="scope">
           <el-button size="small" type="success" @click="editQuestion(scope.$index, scope.row)">编辑</el-button>
         </template>
       </el-table-column>
     </el-table>
    </el-collapse-item>
  </el-collapse>

  <QuestionUpsertDialog :type="dialogType"/>
</template>

<script setup>
import {ref, provide} from 'vue';
import axios from "axios";
import {ElMessage} from "element-plus";
import QuestionUpsertDialog from "@/components/teacher/QuestionUpsertDialog.vue";

let global_counter = -1

const bookName = ref('');
const books = ref([]);
const fakeQuestions = ref([{
  "qid":1,
  "qname":"小熊九月份每天坚持跑 12 千米，这个月他共跑多少千米？列式正确的是",
  "point":["大数计算", "十以内加减"],
  "rightnum":80,
  "totalnum":100,
  "page":10,
  "place":1
},{
  "qid":2,
  "qname":"小熊九月份每天坚持跑 12 千米，这个月他共跑多少千米？列式正确的是",
  "point":["大数计算", "十以内加减", "P3"],
  "rightnum":80,
  "totalnum":100,
  "page":10,
  "place":1
}
])

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

for(let index =3;index <= 100; index++) {
  fakeQuestions.value.push({
    "qid":index,
    "qname":"小熊九月份每天坚持跑 12 千米，这个月他共跑多少千米？列式正确的是",
    "point":["大数计算", "十以内加减", "P3"],
    "rightnum":80,
    "totalnum":100,
    "page":10,
    "place":1
  })
}

//fakeQuestions End

axios.get('/v1/books',
    {params: {
        page: 1,
        size: 10
      }}
).then((res) => {
  if (res.data.code === 0) {
    books.value = res.data.data
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

</script>

<style scoped>

</style>