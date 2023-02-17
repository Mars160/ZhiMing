<template>
  <div class="parent-div">
    <el-table
        :data="userdata"
        size="large"
        fit
        width="100%"
        table-layout="auto"
        v-infinite-scroll="loadMoreUser"
        :v-infinite-scroll-disabled="loadDisable"
        @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" />
      <el-table-column prop="uid" label="学/工号" />
      <el-table-column prop="uname" label="用户姓名" />
      <el-table-column prop="role" label="用户身份" />
    </el-table>
    <el-row style="margin-top: 15px">
      <el-button type="primary" @click="editClicked">修改所选用户</el-button>
      <el-button type="success" @click="addClicked">添加新用户</el-button>
      <el-button type="danger" @click="deleteClicked">删除所选用户</el-button>
    </el-row>

    <UserUpsertDialog
      :type="dialogType"
    />
  </div>
</template>

<script setup>
import {provide, ref} from "vue";
import UserUpsertDialog from "@/components/common/UserUpsertDialog.vue";
import axios from "axios";
import {ElMessage} from "element-plus";

const LIMIT = 10;
let PAGE = 1;
const loadDisable = ref(false)

const userdata = ref([])
const dialogType = ref("add")
const selectedUser = ref([])

const uid = ref('')
const uname = ref('')

provide("select-uid", uid)
provide("select-uname", uname)

function loadMoreUser() {
  axios.get('/v1/users', {
    params: {
      page: PAGE,
      limit: LIMIT
    }
  }).then((res) => {
    //合并res.data.data到userdata.value, 并去除uid重复的
    const uidSet = new Set()
    userdata.value.forEach((user) => {
      uidSet.add(user.uid)
    })
    const result = res.data.data
    result.forEach((user) => {
      if (!uidSet.has(user.uid)) {
        userdata.value.push(user)
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

function editClicked() {
  //获取选中的第一个用户
  const userrow = selectedUser.value[0]
  if (userrow === undefined) {
    ElMessage.error("请先选择一个用户")
    return
  }
  uid.value = userrow.uid
  uname.value = userrow.uname

  console.log(userrow.uid);

  showAddUserDialog.value = true
  dialogType.value = "edit"
}

function addClicked() {
  showAddUserDialog.value = true
  dialogType.value = "add"
  uid.value = ''
  uname.value = ''
  console.log(showAddUserDialog);
}

function deleteClicked() {
  ElMessage.error("暂未实现")
  //TODO Here
}

function handleSelectionChange(val) {
  selectedUser.value = val
}

const showAddUserDialog = ref(false)
provide("showAddUserDialog", showAddUserDialog)
</script>

<style scoped>
.parent-div {
  width: 100%;
}
</style>