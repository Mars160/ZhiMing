# 知明API设计

采用RESTful的设计风格，返回格式如下，版本为v1，资源采用小驼峰命名

```javascript
{
    "code": xx,        //结果码，0表示成果，当code为-1时，强制重新登录
    "data": Object,    //为dict、string，list或undefined
    "msg": "请求的信息（错误原因、成功等）"
}
```

具体请求方式如下，请求体若无特殊说明均为JSON

```http
/v1/token
```

除去token的GET方法外，所有的请求都应带有Authorization请求头，格式为

```
Authorization: Bear eyJ0eXasd123kgGTS891516DGrqoifjrjgo...
```

--------

----

## 通用API

### token

| 方法   | 含义  | URL参数 | 请求体                    | data类型 | data内容   | 备注    |
| ---- | --- | ----- | ---------------------- | ------ | -------- | ----- |
| POST | 登录  |       | `{"user":"","pwd":""}` | string | token字符串 | 获取JWT |

### password

| 方法  | 含义   | URL参数 | 请求体           | data类型    | data内容 | 备注  |
| --- | ---- | ----- | ------------- | --------- | ------ | --- |
| PUT | 修改密码 |       | `{'pwd':PWD}` | undefined |        |     |

### role

| 方法  | 含义        | URL参数 | 请求体 | data类型 | data内容 | 备注              |
| --- | --------- | ----- | --- | ------ | ------ | --------------- |
| GET | 获取当前用户的角色 |       |     | string | 角色字符串  | “学生”、“教师”、“管理员” |

### users

| 方法     | 含义         | URL参数      | 请求体                                     | data类型   | data内容                                    | 备注  |
| ------ | ---------- | ---------- | --------------------------------------- | -------- | ----------------------------------------- | --- |
| GET    | 获取可管理的所有用户 | limit,page |                                         | Object   | `[{'uid':uid,'uname':uname,'role':role}]` |     |
| POST   | 新增用户       |            | `{'uid':uid,'uname':uname,'role':role}` | String   | 新增User的id                                 |     |
| PUT    | 修改用户       | /uid       | `{'uname':uname,'pwd':pwd}`             | undefine |                                           |     |
| DELETE | 删除用户       | /uid       |                                         | undefine |                                           |     |
| DELETE | 批量删除用户     |            | `{'uids':[uid...]}`                     | undefine |                                           |     |

---

## 家长端API

### homework

| 方法   | 含义       | URL参数 | 请求体                                                   | data类型    | data内容       | 备注                           |
| ---- | -------- | ----- | ----------------------------------------------------- | --------- | ------------ | ---------------------------- |
| GET  | 获取新生成的作业 |       |                                                       | string    | https://xxxx | 作业的完整URL                     |
| POST | 上传作业情况   |       | `{"p123":[false,true,false],"p123":[true,true,true]}` | undefined |              | "pxx"指第xx页，数组中的第n个元素指第n题是否正确 |

---

## 教师端API

### books

| 方法     | 含义        | URL参数      | 请求体                             | data类型    | data内容                                         | 备注                                                 |
| ------ | --------- | ---------- | ------------------------------- | --------- | ---------------------------------------------- | -------------------------------------------------- |
| GET    | 获取当前有的练习册 | limit,page |                                 | Object    | `[{'bid':bid,'bname':bname,'grade':grade}...]` | limit指每页数量，page指当前是第几页，bid指当前练习册的ID，bname指每本练习册的名字 |
| POST   | 新增练习册     |            | `{'bname':'xxx','grade':grade}` | string    | bid                                            | 返回新增练习册的ID,grade为练习册适用年级                           |
| PUT    | 修改练习册名字   | /bid       | `{'bname':'yyy','grade':grade}` | undefined |                                                | 返                                                  |
| DELETE | 删除练习册     | /bid       |                                 | undefined |                                                |                                                    |

### questions

| 方法     | 含义         | URL参数                        | 请求体                                                                      | data类型    | data内容                                                                                               | 备注                                                                                        |
| ------ | ---------- | ---------------------------- | ------------------------------------------------------------------------ | --------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| GET    | 获取当前练习册的题目 | bid,limit,page,orderby,order |                                                                          | Object    | `[{"qid":qid,"qname":qname,"point":[points],"rightnum":80,"totalnum":100,page":page,"place":place}]` | URL参数中，bid指当前的练习册id,orderby为排序依据（id，rate等）,order分辨升降序。data中的id1为当前题目id，qname指题干，point指考察点 |
| POST   | 新建题目       |                              | `{'bid':bid,'qname':qname,'point':[pname...],'page':page,'place':place}` | string    | qid                                                                                                  | 返回当前题目id，pid指知识点id                                                                        |
| PUT    | 修改题目       | /qid                         | `{'qname':qname,'point':[pname...],'page':page,'place':place}`           | undefined |                                                                                                      |                                                                                           |
| DELETE | 删除题目       | /qid                         |                                                                          | undefined |                                                                                                      |                                                                                           |

### classes

| 方法     | 含义          | URL参数 | 请求体                                                              | data类型    | data内容                                                                                                                     | 备注                  |
| ------ | ----------- | ----- | ---------------------------------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| GET    | 获取当前教师的所有班级 |       |                                                                  | Object    | `[{'cid':cid,'cname':cname,'grade':grade,'teachers':[{'tid':tid,'tname':tname}],'students':[{'sid':sid, 'sname':sname}]}]` | cid为班级id            |
| POST   | 新建班级        |       | `{'cname': cname, 'grade': grade, 'tids': [tid], 'sids': [sid]}` | string    | cid                                                                                                                        | 上传包含学生学号、姓名的excel文件 |
| PUT    | 修改班级        | /cid  | `{'cname':cname,'grade':grade, 'tids': [tid], 'sids': [sid]}`    | undefined |                                                                                                                            |                     |
| DELETE | 删除班级        | /cid  |                                                                  | undefined |                                                                                                                            |                     |

### students

| 方法     | 含义        | URL参数          | 请求体               | data类型    | data内容                                                      | 备注                                           |
| ------ | --------- | -------------- | ----------------- | --------- | ----------------------------------------------------------- | -------------------------------------------- |
| GET    | 获取当前班级的学生 | cid,limit,page |                   | Object    | `{sid:{'sname':sname,'rate':rate,'points':{pid:rate1...}}}` | sid指学生id（学号），rate指总正确率。pid指考点ID，raten指该考点正确率 |
| POST   | 在班级中新增学生  | cid            | `{'sname':sname}` | string    | sid                                                         |                                              |
| PUT    | 修改学生信息    | /sid           | `{'sname':sname}` | undefined |                                                             |                                              |
| DELETE | 移除该学生     | /sid           |                   | undefined |                                                             |                                              |

### points

| 方法     | 含义       | URL参数      | 请求体               | data类型    | data内容            | 备注                |
| ------ | -------- | ---------- | ----------------- | --------- | ----------------- | ----------------- |
| GET    | 获取当前所有考点 | limit,page |                   | Object    | `{pid1:pname...}` |                   |
| POST   | 新建考点     |            | `{'pname':pname}` | string    | pid               |                   |
| PUT    | 修改题目     | /pid       | `{'pname':pname}` | undefined |                   | 这会导致所有原先该知识点的位置更名 |
| DELETE | 删除题目     | /pid       |                   | undefined |                   |                   |

---

## 管理员API

### teachers

| 方法     | 含义     | URL参数      | 请求体                          | data类型    | data内容           | 备注                  |
| ------ | ------ | ---------- | ---------------------------- | --------- | ---------------- | ------------------- |
| GET    | 获取所有教师 | limit,page |                              | Object    | `{tid:tname...}` | tid指教师id,tname为教师名字 |
| POST   | 新增教师账号 |            | `{'tid':tid,'tname':tname}`  | string    | tid              |                     |
| PUT    | 修改教师信息 | /tid       | `{'tname':tname, 'pwd':pwd}` | undefined |                  |                     |
| DELETE | 删除教师信息 | /tid       |                              | undefined |                  |                     |
