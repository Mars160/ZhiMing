<template>
  <div class="parent-div">
    <el-table
        :data="teacherData"
        size="large"
        fit
        width="100%"
        table-layout="auto"
        @selection-change="updateSelectionTeacher"
    >
      <el-table-column type="selection" />
      <el-table-column prop="tid" label="工号" />
      <el-table-column prop="tname" label="教师姓名" />
    </el-table>
    <el-row style="margin-top: 15px">
      <el-button type="success" size="medium">添加新教师</el-button>
      <el-button type="danger" size="medium">删除所选教师</el-button>
    </el-row>

    <AddUserDialog
      :show="showAddUserDialog"
      :confirm-callback="confirmAddUser"
      :cancel-callback="cancelAddUser"
    />
  </div>
</template>

<script setup>
import {ref} from "vue";
import AddUserDialog from "@/components/common/AddUserDialog.vue";

const teacherData = ref([
  {
    "tid": 1,
    "tname": "张三"
  }
])

//TODO Here
const showAddUserDialog = ref(false)
const confirmAddUser = () => {
  showAddUserDialog.value = false
}
const cancelAddUser = () => {
  showAddUserDialog.value = false
}
//END OF TODO

const updateSelectionTeacher = (selection) => {
  sessionStorage.setItem("selectedTeacher", JSON.stringify(selection))
}
</script>

<style scoped>
.parent-div {
  width: 100%;
}
</style>