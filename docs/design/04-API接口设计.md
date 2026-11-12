# 南昌旅游自定义路线地图工具 API 接口设计文档

> 文档状态：待审查
> 实现框架：FastAPI（自动生成 Swagger/OpenAPI，路径 `/docs`）
> 接口风格：RESTful，数据格式 JSON，基础路径 `/api`

---

## 一、通用约定

### 1. 统一响应结构

**成功响应**
```json
{ "code": 0, "message": "success", "data": { } }
```

**失败响应**
```json
{ "code": 40001, "message": "参数校验失败", "data": null }
```

### 2. HTTP 状态码

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | 成功 | 查询、修改成功 |
| 201 | 已创建 | 路线、标签生成成功 |
| 400 | 参数错误 | 缺少必填、格式不正确 |
| 404 | 不存在 | 点位/路线 ID 查不到 |
| 409 | 冲突 | 同路线重复点位等 |
| 422 | 业务校验失败 | 空清单生成等 |
| 500 | 服务内部错误 | 未预期异常 |
| 502 | 上游错误 | 高德地图服务调用失败 |

### 3. 分页约定
请求参数：`page`（默认 1）、`page_size`（默认 20，最大 100）。
分页响应 data 结构：
```json
{ "total": 36, "page": 1, "page_size": 20, "items": [ ] }
```

### 4. 枚举值
- 点位类型 type：`spot`（景点）、`food`（正餐美食）、`leisure`（休闲市集小店）、`facility`（配套服务）
- 路线模式 gen_mode：`smart`（顺路最优）、`manual`（清单顺序）
- 出行方式 travel_mode：`driving`（驾车，默认）、`walking`（步行）

---

## 二、点位接口

### 1. GET /api/pois —— 点位列表（含筛选/搜索）

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 多类型逗号分隔，如 `spot,food` |
| district | string | 否 | 多区逗号分隔，如 `东湖区,西湖区` |
| keyword | string | 否 | 名称关键词 |
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页条数，默认 20 |

**请求示例**
```
GET /api/pois?type=spot,leisure&district=东湖区,西湖区&page=1&page_size=20
```

**响应示例**
```json
{
  "code": 0, "message": "success",
  "data": {
    "total": 2, "page": 1, "page_size": 20,
    "items": [
      {
        "poi_id": 1, "name": "滕王阁", "type": "spot", "district": "东湖区",
        "address": "仿古路58号", "longitude": 115.887, "latitude": 28.683,
        "description": "江南三大名楼之一，《滕王阁序》诞生地。",
        "open_time": "08:00 - 22:00", "stay_minutes": 90,
        "ticket": "门票 ¥50", "cost": null
      }
    ]
  }
}
```

### 2. GET /api/pois/{poi_id} —— 点位详情

**响应示例**
```json
{
  "code": 0, "message": "success",
  "data": {
    "poi_id": 1, "name": "滕王阁", "type": "spot", "district": "东湖区",
    "address": "仿古路58号", "longitude": 115.887, "latitude": 28.683,
    "description": "江南三大名楼之一，登楼可俯瞰赣江。",
    "open_time": "08:00 - 22:00", "stay_minutes": 90,
    "ticket": "门票 ¥50", "cost": null
  }
}
```
点位不存在返回 404。

### 3. GET /api/pois/{poi_id}/nearby —— 周边点位

**Query 参数**

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| radius | int | 500 | 半径（米），最大 2000 |
| type | string | 全部 | 类型过滤 |

**响应示例**
```json
{
  "code": 0, "message": "success",
  "data": [
    { "poi_id": 6, "name": "万寿宫历史文化街区", "type": "leisure",
      "district": "西湖区", "distance": 420, "stay_minutes": 90 }
  ]
}
```
列表项含 `distance`（直线距离，米），按距离升序。

---

## 三、路线接口

### 1. POST /api/routes —— 生成路线

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 否 | 路线名，不传则默认「路线N」 |
| gen_mode | string | 是 | `smart` / `manual` |
| poi_ids | int[] | 是 | 待选点位 ID 序列，不能为空 |
| travel_mode | string | 否 | `driving` / `walking`，默认驾车 |

**请求示例**
```json
{
  "gen_mode": "smart",
  "poi_ids": [1, 6, 13],
  "travel_mode": "driving"
}
```

**响应示例（201）**
```json
{
  "code": 0, "message": "路线生成成功",
  "data": {
    "route_id": 1, "name": "路线1", "gen_mode": "smart",
    "total_minutes": 265,
    "items": [
      { "seq": 1, "poi_id": 1, "name": "滕王阁", "stay_minutes": 90, "user_note": null },
      { "seq": 2, "poi_id": 13, "name": "老南昌瓦罐汤馆", "stay_minutes": 40, "user_note": null },
      { "seq": 3, "poi_id": 6, "name": "万寿宫历史文化街区", "stay_minutes": 90, "user_note": null }
    ]
  }
}
```

**业务校验**
- poi_ids 为空：422，提示「请先添加点位」；
- 含配套点（facility）：400，提示「配套服务点位不能加入路线」；
- 点位重复：409，提示「同一点位不能重复」。

### 2. GET /api/routes —— 路线列表

**响应示例（折叠态所需字段）**
```json
{
  "code": 0, "message": "success",
  "data": [
    { "route_id": 1, "name": "路线1", "gen_mode": "smart",
      "poi_count": 3, "total_minutes": 265, "created_at": "2026-11-10 15:20:00" }
  ]
}
```

### 3. GET /api/routes/{route_id} —— 路线详情

**响应示例**
```json
{
  "code": 0, "message": "success",
  "data": {
    "route_id": 1, "name": "路线1", "gen_mode": "smart", "total_minutes": 265,
    "items": [
      { "seq": 1, "poi_id": 1, "name": "滕王阁", "type": "spot",
        "longitude": 115.887, "latitude": 28.683,
        "stay_minutes": 90, "open_time": "08:00 - 22:00", "user_note": null }
    ]
  }
}
```
详情含点位坐标，供前端独立小地图绘制。

### 4. PATCH /api/routes/{route_id} —— 重命名

**请求体**
```json
{ "name": "南昌一日精华游" }
```
**响应**：返回更新后的路线概要（200）。

### 5. PUT /api/routes/{route_id}/items —— 顺序微调/备注

**请求体**
```json
{
  "items": [
    { "poi_id": 6, "user_note": "晚上逛夜景" },
    { "poi_id": 1, "user_note": null },
    { "poi_id": 13, "user_note": null }
  ]
}
```
后端按数组顺序重排 seq，重新计算 total_minutes，返回完整路线详情。

### 6. POST /api/routes/{route_id}/copy —— 复制路线

**响应（201）**
```json
{ "code": 0, "message": "复制成功",
  "data": { "route_id": 2, "name": "南昌一日精华游 副本", "total_minutes": 265 } }
```

### 7. DELETE /api/routes/{route_id} —— 删除路线

**响应**
```json
{ "code": 0, "message": "路线已删除", "data": null }
```
行程项由数据库外键级联删除，点位数据保留。

---

## 四、地图代理接口

### 1. GET /api/map/duration —— 通勤时长（代理高德路径规划）

**Query 参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| from_poi | int | 二选一 | 起点点位 ID |
| to_poi | int | 二选一 | 终点点位 ID |
| from_loc | string | 备选 | 经纬度 `lng,lat` |
| to_loc | string | 备选 | 经纬度 `lng,lat` |
| travel_mode | string | 否 | driving / walking |

**响应示例**
```json
{
  "code": 0, "message": "success",
  "data": { "distance_m": 1800, "duration_minutes": 12, "travel_mode": "driving" }
}
```
上游高德服务异常返回 502。

### 2. GET /api/map/geocode —— 地理编码（代理）

**Query**：`address`（地址）或 `location`（经纬度反解）。
**响应**：返回经纬度或结构化地址，供批量导入脚本使用。

---

## 五、标签接口（分组标签）

| 方法路径 | 说明 |
|----------|------|
| GET /api/tags | 标签列表 |
| POST /api/tags | 新建标签，请求体 `{ "name": "第一天" }` |
| POST /api/pois/{poi_id}/tags | 给点位打标签，请求体 `{ "tag_ids": [1,2] }` |
| DELETE /api/tags/{tag_id} | 删除标签（关联关系级联清除） |

---

## 六、接口与需求追溯

| 功能需求 | 对应接口 |
|----------|----------|
| FR-03 双维度筛选 | GET /api/pois（type、district） |
| FR-06 搜索 | GET /api/pois（keyword） |
| FR-14 周边 | GET /api/pois/{id}/nearby |
| FR-23/24 生成 | POST /api/routes |
| FR-26 命名/删除 | PATCH、DELETE /api/routes/{id} |
| FR-28 微调 | PUT /api/routes/{id}/items |
| FR-29 时长 | GET /api/map/duration + total_minutes |
| FR-30 复制/导出 | POST /api/routes/{id}/copy（文本导出在前端完成） |

---

## 七、前端调用说明

- 前端通过统一封装的 request 模块调用，自动处理基础路径、分页和错误提示；
- 开发期跨域由 Vite 代理转发到 FastAPI；
- 纯文本导出（复制行程）不经过后端，由前端用路线详情数据拼装后写入剪贴板；
- 本地筛选记忆、临时清单走 localStorage，不占用接口。
