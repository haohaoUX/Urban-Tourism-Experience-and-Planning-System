# 洪城漫游 · 南昌旅游自定义路线地图工具

> 面向南昌城市短途旅游的轻量化路线规划工具：在地图上挑几个想去的点，一键排出顺路的行程并估算耗时。
> 纯浏览器访问，免安装、免登录，前后端分离部署。

![version](https://img.shields.io/badge/version-0.1.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)

## 一、项目简介

洪城漫游解决的是「到南昌玩一两天，怎么把想去的点串成一条不绕路的线」这个问题。用户不需要注册账号，打开网页即可：

```
地图浏览选点 → 筛选/搜索 → 点位详情 → 加入待选清单 → 一键生成路线 → 查看与管理路线
```

点位分为 4 类，以不同颜色与图标区分：

| 类型 | 标识 | 颜色 | 能否加入路线 |
| --- | --- | --- | --- |
| 景点 `spot` | 星标 | 蓝 | 可以 |
| 正餐美食 `food` | 餐具 | 橙 | 可以 |
| 休闲市集小店 `leisure` | 购物袋 | 绿 | 可以 |
| 配套服务 `facility` | 信息 i | 灰 | 仅可浏览，不能加入 |

中期版本内置 16 个南昌真实点位，使用自制模拟地图渲染，数据库默认 SQLite，无需额外安装数据库服务。

## 二、功能特性

| 功能 | 状态 | 说明 |
| --- | --- | --- |
| 地图浏览与点位标注 | ✅ 已完成 | 模拟地图渲染 16 个点位，按类型着色 |
| 按行政区 / 类型筛选 | ✅ 已完成 | 左侧筛选面板，支持多选 |
| 关键字搜索 | ✅ 已完成 | 点位名称模糊匹配 |
| 点位详情 | ✅ 已完成 | 简介、开放时间、停留时长、门票/消费 |
| 待选清单 | ✅ 已完成 | 加入 / 移除，同一点位不可重复 |
| 一键生成路线（顺路最优） | ✅ 已完成 | 最近邻启发式排序 |
| 一键生成路线（清单顺序） | ✅ 已完成 | 按用户添加顺序直连 |
| 驾车 / 步行耗时估算 | ✅ 已完成 | Haversine 距离 + 停留时长 |
| 路线重命名 / 复制 / 删除 | ✅ 已完成 | 路线卡片内操作 |
| 我的标记（收藏打卡） | 🚧 规划中 | 数据表已建，前端下一迭代接入 |
| 高德地图 JS API 真实底图 | 🚧 规划中 | Web 端 Key 已申请，替换模拟地图 |
| 备注 / 拖拽排序 / 打卡 | 🚧 规划中 | 末期规划 |

## 三、技术栈

| 层 | 技术选型 | 说明 |
| --- | --- | --- |
| 表现层 | Vue 3 + Vite 5 + Vue Router | 手写 CSS，不引入重型组件库 |
| 业务层 | Python + FastAPI + Pydantic v2 | 分层路由，统一响应结构 |
| 数据层 | SQLAlchemy 2.0 + SQLite / MySQL | 默认 SQLite，零配置启动；MySQL 保留配置 |
| 地图 | 自制模拟地图（中期）→ 高德 JS API | 中期不需要 Key |
| 测试 / CI | pytest + pytest-cov + GitHub Actions | 见 `.github/workflows/ci.yml` |

## 四、快速开始

### 4.1 环境要求

| 软件 | 版本要求 | 说明 |
| --- | --- | --- |
| Node.js | 18 及以上（开发环境 v22） | 含 npm |
| Python | 3.10 及以上（开发环境 3.13） | 建议使用虚拟环境 |
| 浏览器 | Edge / Chrome / Safari / Firefox 近两年版本 | 需启用 JavaScript |

### 4.2 启动后端

```powershell
cd backend

# 创建并激活虚拟环境（首次）
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 安装依赖（首次）
pip install -r requirements.txt

# 初始化数据库（首次，写入 16 个点位）
python scripts\init_data.py

# 启动后端服务
uvicorn app.main:app --reload
```

启动后：

- 接口地址：`http://127.0.0.1:8000`
- 在线接口文档（Swagger）：`http://127.0.0.1:8000/docs`

### 4.3 启动前端

另开一个 PowerShell 窗口：

```powershell
cd frontend
npm install        # 首次
npm run dev
```

浏览器访问 `http://127.0.0.1:5173`。前端已配置代理，`/api` 请求自动转发到后端 `http://127.0.0.1:8000`，无需处理跨域。

### 4.4 演示账号

本系统当前无需登录，打开即用；用户侧的收藏、标记等数据保存在浏览器本地存储。若后续引入账号体系，将在此处补充演示账号。

## 五、演示主流程

1. 打开 `http://127.0.0.1:5173`，在地图上浏览 16 个点位。
2. 点击左侧「筛选」选择行政区与点位类型，地图实时更新；点击「标记」可只看自己标记的点位。
3. 点击任意点位，右侧弹出详情卡片，查看简介、开放时间、停留时长、门票或消费。
4. 点击「添加到路线」，点位进入左侧待选清单；同一点位不能重复添加。
5. 切换到底部「规划」页，选择顺路最优 / 清单顺序、驾车 / 步行，点击「一键生成路线」。
6. 在右侧路线卡片中点击展开，查看迷你地图、连线与行程顺序，可重命名、复制、删除。

## 六、架构设计

系统采用前后端分离的三层架构，浏览器只与 FastAPI 通信，数据落在关系型数据库：

```mermaid
flowchart LR
    U[浏览器用户] -->|HTTP / JSON| F[Vue 3 前端<br/>MapView / PlanView]
    F -->|/api 代理| A[FastAPI 应用层<br/>api/poi.py · api/route.py]
    A --> S[业务服务层<br/>services/algorithm.py]
    S --> M[ORM 模型层<br/>7 张表]
    M --> D[(SQLite / MySQL)]
    F -.规划中.-> G[高德地图 JS API]
```

| 层 | 职责 | 代码位置 |
| --- | --- | --- |
| 表现层 | 页面渲染、交互、本地状态持久化 | `frontend/src/views`、`components`、`stores` |
| 接口层 | 路由注册、参数校验、统一响应与错误码 | `backend/app/api`、`schemas` |
| 业务层 | 距离计算、路线排序、时长估算 | `backend/app/services` |
| 数据层 | ORM 映射、会话管理、建表 | `backend/app/models`、`core/database.py` |

**关键接口数据流**：`POST /api/routes` → `RouteCreate` 校验（非空 / 去重 / 点位有效 / `facility` 拦截）→ `services.algorithm.nearest_neighbor` 排序 → `estimate_total_minutes` 估算总时长 → 写入 `route` + `route_item` → 返回统一结构 `{code, message, data}`。

关键设计决策记录见 [`docs/adr/`](docs/adr/)，完整设计文档见 [`docs/`](docs/)。

## 七、项目结构

```
洪城漫游/
├── README.md
├── CONTRIBUTING.md            # 分支 / 提交 / PR / 评审规范
├── CHANGELOG.md               # 版本变更记录
├── LICENSE                    # MIT
├── 代码说明书.md              # 文件职责、人员归属、功能完成度
├── .github/
│   ├── workflows/ci.yml       # GitHub Actions
│   ├── ISSUE_TEMPLATE/        # Issue 模板
│   └── pull_request_template.md
├── docs/
│   ├── adr/                   # 架构决策记录
│   ├── requirements/          # 需求规格说明书、功能需求
│   ├── plan/                  # 可行性研究、开发计划、Issue 清单
│   └── design/                # 架构、数据库、API、详细设计、技术选型、视觉规范
├── backend/
│   ├── requirements.txt
│   ├── .env.example
│   ├── pytest.ini
│   ├── scripts/init_data.py   # 初始化数据
│   ├── tests/                 # pytest 用例
│   └── app/
│       ├── main.py            # 应用入口
│       ├── core/              # 配置、数据库连接
│       ├── models/            # ORM 模型（7 张表）
│       ├── schemas/           # 数据校验
│       ├── services/          # 路线算法
│       └── api/               # 点位、路线接口
└── frontend/
    ├── vite.config.js         # 含 /api 代理
    └── src/
        ├── api/               # 接口封装
        ├── stores/            # 全局状态与本地持久化
        ├── utils/             # 投影与模拟地图布局
        ├── styles/            # 设计 Token 与全局样式
        ├── components/        # 8 个组件
        └── views/             # 地图页、规划页
```

## 八、团队与分工

| 成员 | GitHub | 角色 | 主要职责 |
| --- | --- | --- | --- |
| 刘昊 | [@haohaoUX](https://github.com/haohaoUX) | Maintainer / Tech Lead | 项目统筹与进度、总体架构与技术选型、代码审查、答辩主讲 |
| 刘克 | [@kirito0714-lk](https://github.com/kirito0714-lk) | Frontend Developer | 地图页与规划页、液态玻璃风格落地、接口对接与联调 |
| 肖睿 | 待补充 | Backend Developer | 后端服务与数据库、点位/路线接口、路线算法、数据初始化 |
| 张仕琪 | 待补充 | QA / Docs | 测试用例与验证、SRS 与 README 等文档、设计 Token 与素材 |

## 九、配置说明

### 9.1 数据库

默认使用 SQLite，连接串 `sqlite:///./nanchang_trip.sqlite3`，数据库文件位于 `backend` 目录下，零配置即可使用。

切换 MySQL：

1. 复制 `backend/.env.example` 为 `backend/.env`。
2. 修改 `DATABASE_URL`：

```
DATABASE_URL=mysql+pymysql://root:你的密码@127.0.0.1:3306/nanchang_trip?charset=utf8mb4
```

3. 提前创建 `nanchang_trip` 数据库，再执行 `python scripts\init_data.py`。

`.env` 已被 `.gitignore` 忽略，仓库中只保留不含密钥的 `.env.example`。

### 9.2 高德地图 Key

中期模拟地图不需要 Key。后续接入真实地图时，在 `.env` 中填写 `AMAP_KEY` 与 `AMAP_SECRET`，前端通过后端下发的配置初始化地图。

## 十、测试与持续集成

```powershell
cd backend
pip install -r requirements.txt -r requirements-dev.txt
pytest --cov=app/services --cov-report=term-missing
```

CI 配置见 `.github/workflows/ci.yml`：后端执行语法检查与单元测试（含覆盖率），前端执行 `npm ci` 与 `npm run build`。

## 十一、参与贡献

分支命名、Commit Message、PR 描述与评审要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。任何进入 `main` 的变更都需要经过 PR 与至少一名非作者的 Approve。

## 十二、常见问题

**1. 前端页面能打开，但数据加载失败？**
请确认后端已在 `8000` 端口启动，并访问 `http://127.0.0.1:8000/docs` 检查。

**2. 执行 PowerShell 脚本提示无法加载脚本？**
可执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 后重试，或不激活虚拟环境，直接用 `.\.venv\Scripts\python.exe` 与 `.\.venv\Scripts\uvicorn.exe` 运行。

**3. 重新初始化时报主键或数据错误？**
删除 `backend\nanchang_trip.sqlite3` 后重新执行 `python scripts\init_data.py` 即可。

**4. 玻璃模糊效果不显示？**
部分旧浏览器不支持 `backdrop-filter`，系统会自动降级为半透明纯色，功能不受影响。

**5. npm install 速度慢？**
可切换国内镜像：`npm config set registry https://registry.npmmirror.com`。

## 十三、许可证

本项目采用 [MIT](LICENSE) 许可证。
