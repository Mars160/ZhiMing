<template>
  <ul
      v-infinite-scroll="loadMoreBook"
      :infinite-scroll-disabled="loadDisable"
  >
    <li
        v-for="book in books"
        :key="book.bid"
        @click="editBook(book.bid, book.bname, book.grade)"
    >
      <el-card>
        <span class="book-info">{{ book.bname }}</span>
        <span class="book-info">{{ book.gradeStr }}</span>
      </el-card>
    </li>
    <li>
      <el-card>
        <el-button type="primary" @click="addClicked" circle size="large">
          <el-icon>
            <i-ep-plus/>
          </el-icon>
        </el-button>
      </el-card>
    </li>
  </ul>

  <BookUpsertDialog
      :type="dialogType"
  />
</template>

<script setup>
import {provide, ref} from "vue";
import axios from "axios";
import {ElMessage} from "element-plus";
import BookUpsertDialog from "@/components/teacher/BookUpsertDialog.vue";

const books = ref([])
const LIMIT = 10
let PAGE = 1

const dialogType = ref("add")

const showBookUpsertDialog = ref(false)
const bid = ref('')
const bname = ref('')
const grade = ref('')
provide("showBookUpsertDialog", showBookUpsertDialog)
provide("select-bid", bid)
provide("select-bname", bname)
provide("select-grade", grade)

const loadDisable = ref(false)
const number2Str = ['一', '二', '三', '四', '五', '六']

function loadMoreBook() {
  axios.get('/v1/books', {
    params: {
      page: PAGE,
      limit: LIMIT
    }
  }).then((res) => {
    const bidSet = new Set()
    books.value.forEach((book) => {
      bidSet.add(book.bid)
    })
    const result = res.data.data
    result.forEach((book) => {
      if (!bidSet.has(book.uid)) {
        book.gradeStr = number2Str[parseInt(book.grade / 10)] + '年级'
        //十位 1: 一年级, 2: 二年级, 3: 三年级, 4: 四年级, 5: 五年级, 6: 六年级 个位 0: 上册, 5: 下册
        switch (book.grade % 10) {
          case 0:
            book.gradeStr += '上册'
            break
          case 5:
            book.gradeStr += '下册'
            break
        }
        books.value.push(book)
      }
    })
    if (result.length !== 0) {
      PAGE = PAGE + 1
    } else {
      loadDisable.value = true
    }
  }).catch((err) => {
    ElMessage.error(err)
  })
}

function addClicked() {
  dialogType.value = "add"
  showBookUpsertDialog.value = true
}

function editBook(bid1, bname1, grade1) {
  dialogType.value = "edit"
  showBookUpsertDialog.value = true
  bid.value = bid1
  bname.value = bname1
  grade.value = grade1
}
</script>

<style scoped>
.el-card {
  height: 297px;
  width: 210px;
  text-align: center;
  justify-content: center;
  align-items: center;
  display: flex;

  cursor: pointer;
}

.el-card:hover {
  background-color: #f5f5f5;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  display: inline-block;
  margin: 10px;
}

.book-info {
  display: block;
  height: 20px;
  margin-top: 10px;
}
</style>