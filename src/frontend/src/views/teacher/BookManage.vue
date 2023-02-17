<template>
  <ul
    v-infinite-scroll="loadMoreBook"
    :infinite-scroll-disabled="loadDisable"
  >
    <li v-for="book in books" :key="book.bid">
      <el-card>
        <span>{{book.bname}}</span>
      </el-card>
    </li>
  </ul>
  <el-card>
    <span>一课一练数学三年级（下）</span>
  </el-card>
</template>

<script setup>
import {ref} from "vue";
import axios from "axios";
import {ElMessage} from "element-plus";

const books = ref([])
const LIMIT = 10
let PAGE = 1

const loadDisable = ref(false)

function loadMoreBook() {
  axios.get('/v1/books', {
    params: {
      page: PAGE,
      limit: LIMIT
    }
  }).then((res) => {
    const result = res.data.data
    if (result.length !== 0) {
      PAGE = PAGE + 1
    } else {
      loadDisable.value = true
    }
  }).catch((err) => {
    ElMessage.error(err)
  })
}
</script>

<style scoped>
.el-card {
  height: 297px;
  width: 210px;
  line-height: 257px;
  text-align: center;
}
</style>