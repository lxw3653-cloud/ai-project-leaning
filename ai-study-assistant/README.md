# AI 学习助手（AI Study Assistant）

一个前后端分离的学习计划管理应用。当前版本已经打通「页面 → 接口 → 数据库」的完整链路：可以在网页上创建、查看、编辑、删除学习计划，数据保存在本地 SQLite 数据库中。

> 目前只完成了学习计划管理这部分基础功能，AI 能力（答疑、总结、出题等）尚未开始。

## 技术栈

| 层次 | 技术 | 说明 |
| --- | --- | --- |
| 前端 | Vue 3 + Vite + JavaScript | 组合式 API（`<script setup>`），未引入路由和状态管理库 |
| 前端请求 | 原生 `fetch` | 在 `src/api/client.js` 中统一封装 |
| 后端 | Python + FastAPI | 异步接口，自带 Swagger 文档 |
| 数据库 | SQLite + SQLAlchemy 2.x（异步） | 单文件数据库，不需要额外安装数据库服务 |

## 已有功能

- **学习计划管理**：新建、列表、查看单条、编辑、删除
- **状态管理**：未开始 / 进行中 / 已完成，页面上显示中文
- **数据校验**：标题必填；结束日期不能早于开始日期（前端提示 + 数据库约束双重保障）
- **错误提示**：前端会读取后端返回的错误详情并显示，例如「学习计划不存在」「结束日期不能早于开始日期」
- **删除二次确认**
- **健康检查接口**：用于确认后端是否正常启动

## 快速开始

### 环境要求

- Python 3.10 或更高版本
- Node.js 20 或更高版本

### 1. 启动后端

```powershell
cd backend
python -m venv .venv                      # 创建虚拟环境
.\.venv\Scripts\Activate.ps1              # 激活（若被禁用可改用 activate.bat）
python -m pip install -r requirements.txt # 安装依赖
uvicorn app.main:app --reload             # 启动，改代码后自动重启
```

启动后可访问：

- 接口文档（推荐用它调试）：<http://127.0.0.1:8000/docs>
- 健康检查：<http://127.0.0.1:8000/api/health>

首次启动会自动创建数据库文件 `backend/data/app.db` 和数据表。

### 2. 启动前端

另开一个终端：

```powershell
cd frontend
npm install
npm run dev
```

然后打开 <http://localhost:5173>。

开发服务器会把所有以 `/api` 开头的请求代理到 `http://127.0.0.1:8000`，因此本地开发不需要额外配置跨域。注意：**前端不要用 `/api` 开头命名页面或静态资源**，它们会被同一规则转发给后端。

## API 接口

所有接口以 `/api` 为前缀（根路径 `/` 除外）。

| 方法 | 路径 | 说明 | 成功状态码 |
| --- | --- | --- | --- |
| GET | `/api/health` | 健康检查 | 200 |
| GET | `/api/study-plans` | 查询全部学习计划（按创建时间倒序） | 200 |
| POST | `/api/study-plans` | 创建学习计划 | 201 |
| GET | `/api/study-plans/{plan_id}` | 查询单个学习计划 | 200 |
| PATCH | `/api/study-plans/{plan_id}` | 局部更新学习计划（只传要改的字段） | 200 |
| DELETE | `/api/study-plans/{plan_id}` | 删除学习计划 | 204 |
| GET | `/` | 服务基本信息 | 200 |

记录不存在时返回 404，字段校验失败返回 422。

请求体字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `title` | 字符串 | 必填，最长 200 字 |
| `description` | 字符串或 null | 描述，可留空 |
| `status` | 字符串 | `not_started` / `in_progress` / `completed`，默认 `not_started` |
| `start_date` | 日期字符串或 null | 格式 `YYYY-MM-DD` |
| `end_date` | 日期字符串或 null | 格式 `YYYY-MM-DD` |

## 目录结构

```text
ai-study-assistant/
├── README.md
├── .gitignore
├── backend/                          后端（FastAPI）
│   ├── requirements.txt              Python 依赖
│   ├── .env.example                  环境变量示例（复制为 .env 后生效）
│   ├── data/                         SQLite 文件目录（app.db 运行时生成，不提交）
│   └── app/
│       ├── main.py                   应用入口：CORS、路由挂载、启动时建表
│       ├── core/config.py            配置：应用信息、跨域白名单、数据库地址
│       ├── api/
│       │   ├── router.py             汇总各业务路由
│       │   └── routes/
│       │       ├── health.py         健康检查接口
│       │       └── study_plans.py    学习计划 CRUD 接口
│       ├── models/study_plan.py      学习计划表模型与状态枚举
│       ├── schemas/                  请求 / 响应数据结构
│       │   ├── health.py
│       │   └── study_plan.py
│       └── db/
│           ├── base.py               ORM 基类
│           └── session.py            异步引擎、会话、建表函数
└── frontend/                         前端（Vue 3 + Vite）
    ├── package.json                  依赖与脚本
    ├── package-lock.json             依赖版本锁定文件
    ├── vite.config.js                路径别名与 /api 开发代理
    ├── index.html                    页面入口
    ├── .env.development              接口前缀配置
    └── src/
        ├── main.js                   前端入口
        ├── App.vue                   页面外壳（页头 / 内容 / 页脚）
        ├── api/
        │   ├── client.js             请求封装与错误处理（ApiError）
        │   └── studyPlans.js         学习计划接口封装
        ├── constants/studyPlan.js    状态枚举与中文标签
        ├── components/
        │   ├── StudyPlanForm.vue     新建 / 编辑共用表单
        │   ├── StudyPlanList.vue     学习计划列表
        │   └── HealthCheck.vue       后端连通性检测组件（当前未接入页面）
        ├── views/
        │   ├── StudyPlansView.vue    学习计划页面
        │   └── HomeView.vue          初始化阶段的欢迎页（当前未接入）
        └── assets/styles/main.css    全局样式与主题变量
```

## 数据库

只有一张业务表 `study_plans`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | 整数 | 主键，自增 |
| `title` | 文本（200） | 标题 |
| `description` | 长文本 | 描述，可为空 |
| `status` | 文本 | 只能是三个状态值之一（带 CHECK 约束） |
| `start_date` / `end_date` | 日期 | 可为空；结束日期不能早于开始日期（带 CHECK 约束） |
| `created_at` / `updated_at` | 日期时间 | 程序自动维护，以 UTC 存储 |

表结构由 `backend/app/db/session.py` 的 `init_db()` 在启动时创建，只会建缺失的表，**不会修改已有表的结构**。修改字段后可以直接删除 `backend/data/app.db` 让程序重建（数据会丢失）。

## 尚未实现

以下内容目前都还没有做，列出来是为了避免误解：用户登录与多用户、AI 相关能力、列表分页与筛选、自动化测试、部署配置。
