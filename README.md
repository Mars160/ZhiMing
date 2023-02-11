# 知明

> 君子博学而日参省乎己，则知明而行无过矣。   

知明——面向学生的轻量级作业管理系统

----

## 逻辑设计

该系统分为教师端和家长端

### 家长端

上传教师批改后的作业正误情况

根据学生做题情况生成新的题目，家长下载题目的PNG

### 教师端

教师上传题目到题库，用于给学生出题

教师创建班级，并给学生分配账号

教师在后台查看每题正确率

教师在后台查看学生易错点

### 管理员

增删教师账号

## 其他

[API设计](./doc/API.md)

[开发情况](./doc/TODO.md)

[Demo](https://zhiming.somewang.top/)（尚未发布）

Vue + Flask
