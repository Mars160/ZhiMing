# 知明数据库设计

所有字段默认非空

---

## 实体数据库

### User

| 字段    | 类型      | 含义     | 备注        |
| ----- | ------- | ------ | --------- |
| uid   | varchar | 用户角色id | 主键，自增     |
| uname | varchar | 用户名    |           |
| role  | enum    | 用户角色   | 管理员、教师、学生 |
| pwd   | varchar | 加密后的密码 |           |

### Book

| 字段    | 类型      | 含义    | 备注    |
| ----- | ------- | ----- | ----- |
| bid   | varchar | 练习册id | 主键、自增 |
| bname | varchar | 练习册名  | 不重复   |
| grade | integer | 适用年级  |       |

### Question

| 字段    | 类型      | 含义     | 备注     |
| ----- | ------- | ------ | ------ |
| qid   | varchar | 题目id   | 主键、自增  |
| qname | varchar | 题干     | 不重复    |
| level | integer | 当前题目等级 | （可能会加） |

### Class

| 字段    | 类型      | 含义   | 备注    |
| ----- | ------- | ---- | ----- |
| cid   | varchar | 班级id | 主键、自增 |
| cname | varchar | 班级名  | 不重复   |
| grade | integer | 班级年级 |       |

### Point

| 字段    | 类型      | 含义    | 备注    |
| ----- | ------- | ----- | ----- |
| pid   | varchar | 知识点id | 主键、自增 |
| pname | varchar | 知识点名  | 不重复   |

---

## 实体关系数据库

### RUC

**R**elationship between **U**sers and **C**lasses

用于记录用户属于哪个班级，学生同时只能属于一个班级，而教师可以属于多个班级

| 字段   | 类型      | 含义              | 备注    |
| ---- | ------- | --------------- | ----- |
| ucid | varchar | user和class关系的id | 主键、自增 |
| uid  | varchar | 用户id            |       |
| cid  | varchar | 班级id            |       |

### RQB

**R**elationship between **Q**usetion and **B**ook

用于记录题目属于哪本练习册，每个题目只能属于一个练习册

| 字段    | 类型      | 含义        | 备注     |
| ----- | ------- | --------- | ------ |
| bqid  | varchar | 关系记录的id   | 主键、自增  |
| qid   | varchar | 题目id      | 不重复    |
| bid   | varchar | 练习册id     |        |
| page  | integer | 题目所在页码    | 不一定用得到 |
| place | integer | 题目为该页的第n题 | 不一定用得到 |

### RPQ

**R**elationship between **P**oint and **Q**usetion

用于记录题目有哪些知识点

| 字段   | 类型      | 含义     | 备注    |
| ---- | ------- | ------ | ----- |
| pqid | varchar | 关系记录id | 主键、自增 |
| pid  | varchar | 知识点id  |       |
| qid  | varchar | 题目id   |       |

---

## 统计数据库

本部分数据库用于记录统计的数据，如正确率等

TODO
