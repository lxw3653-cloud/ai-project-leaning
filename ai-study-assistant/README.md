# AI 学习助手（AI Study Assistant）

一个前后端分离的 AI 学习助手 Web 项目。当前处于**项目初始化阶段**：只搭建骨架、跑通前后端连接，尚未实现业务功能。

## 技术栈

| 层次 | 技术 | 说明 |
| --- | --- | --- |
| 前端 | Vue 3 + Vite + JavaScript | 不做 TypeScript，先用 JS 打好基础 |
| 后端 | Python + FastAPI | 提供 REST 接口，自带 Swagger 文档 |
| 数据库 | SQLite | 目前只做规划与连接配置，未建表 |

## 目录结构

```text
ai-study-assistant/
├── README.md                 项目说明（本文件）
├── .gitignore                Git 忽略规则
├── frontend/                 前端项目
│   ├── package.json          前端依赖与启动脚本
│   ├── vite.config.js        Vite 配置（含 /api 开发代理）
│   ├── index.html            页面入口 HTML
│   ├── .env.development      开发环境变量
│   └── src/
│       ├── main.js           前端 JS 入口
│       ├── App.vue           根组件（整体布局）
│       ├── api/client.js     后端请求封装
│       ├── components/       可复用组件
│       ├── views/            页面级组件
│       └── assets/styles/    全局样式
└── backend/                  后端项目
    ├── requirements.txt      Python 依赖清单
    ├── .env.example          环境变量示例
    ├── data/                 SQLite 数据库文件目录（规划中）
    └── app/
        ├── main.py           FastAPI 应用入口
        ├── core/             全局配置
        ├── api/              路由层
        ├── schemas/          请求/响应数据结构
        ├── models/           ORM 模型（study_plan）
        └── db/               数据库连接与会话
```

## 环境要求（请先自行安装）

本项目需要以下软件。**安装前请确认来源可信，本仓库不包含也不自动安装它们。**

1. **Node.js 20 LTS 或更高版本**（自带 npm）：<https://nodejs.org/>
   安装后在终端执行 `node -v` 和 `npm -v`，两条命令都能输出版本号才算成功。
2. **Python 3.10 或更高版本**：<https://www.python.org/downloads/>
   安装时务必勾选 **Add python.exe to PATH**。安装后执行 `python --version` 验证。
3. **Git**（可选，用于版本管理）。

> 注意：如果你的 `node -v` 能输出结果、但 `npm -v` 报“无法识别”，通常说明当前 PATH 指向的是别的运行环境，而不是你自己安装的 Node.js。装好 Node.js 后请**重开一个终端**再试。

## 启动后端

在项目根目录执行（Windows PowerShell / CMD）：

```powershell
cd backend
python -m venv .venv                                   # 1. 创建虚拟环境（隔离依赖，不污染全局 Python）
.\.venv\Scripts\Activate.ps1                           # 2. 激活虚拟环境
python -m pip install -r requirements.txt              # 3. 安装依赖（从 PyPI 下载）
uvicorn app.main:app --reload                          # 4. 启动开发服务器
```

- `python -m venv .venv`：在 `backend/.venv` 建一个独立的 Python 环境。
- `.\.venv\Scripts\Activate.ps1`：进入该环境（后续 `python`、`pip` 都作用于它）。若提示脚本被禁止执行，可改用 `.\.venv\Scripts\activate.bat`。
- `python -m pip install -r requirements.txt`：按清单安装 FastAPI 等依赖，需要联网。
- `uvicorn app.main:app --reload`：启动后端，`--reload` 表示改代码后自动重启。

启动后访问：

- 接口根路径：<http://127.0.0.1:8000/>
- 健康检查：<http://127.0.0.1:8000/api/health>
- 交互式接口文档：<http://127.0.0.1:8000/docs>

## 启动前端

另开一个终端，在项目根目录执行：

```powershell
cd frontend
npm install            # 1. 安装前端依赖（从 npm 仓库下载）
npm run dev            # 2. 启动 Vite 开发服务器
```

启动后打开 <http://localhost:5173>，点击页面上的「检测后端连接」按钮，如果后端已启动，会显示后端服务名和版本号。

前端 `npm run dev` 默认端口是 `5173`，并且会把 `/api` 开头的请求代理到 `http://127.0.0.1:8000`，因此开发阶段不需要额外处理跨域。

## 可用命令速查

后端（在 `backend/` 目录、虚拟环境已激活时）：

```powershell
uvicorn app.main:app --reload      # 开发模式启动
uvicorn app.main:app --port 8001   # 换端口启动
```

前端（在 `frontend/` 目录）：

```powershell
npm run dev        # 开发服务器（热更新）
npm run build      # 打包到 dist/
npm run preview    # 本地预览打包结果
```

## 当前接口

| 方法 | 路径 | 作用 |
| --- | --- | --- |
| GET | `/` | 返回服务基本信息 |
| GET | `/api/health` | 健康检查，前端用它验证连通性 |

## 数据库说明

数据库使用 SQLite，文件路径为 `backend/data/app.db`（首次启动后端时自动创建，该文件不提交到 Git）。

建表逻辑在 `backend/app/db/session.py` 的 `init_db()` 中，由 `backend/app/main.py` 在应用启动时自动调用。`create_all` 只会创建缺失的表，不会改动已存在的表结构——所以以后修改字段时，要么引入 Alembic 迁移，要么删掉 `app.db` 让它重建。

目前只有一张业务表 `study_plans`（学习计划），定义在 `backend/app/models/study_plan.py`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | 整数 | 主键，自增 |
| `title` | 文本（200） | 计划标题，必填 |
| `description` | 长文本 | 计划描述，可为空 |
| `status` | 文本 | 状态，只能是 `not_started` / `in_progress` / `completed` |
| `start_date` | 日期 | 开始日期，可为空 |
| `end_date` | 日期 | 结束日期，可为空，且不能早于开始日期 |
| `created_at` | 日期时间 | 创建时间，程序自动写入（UTC） |
| `updated_at` | 日期时间 | 更新时间，每次修改自动刷新（UTC） |

> 注意：CRUD 接口尚未实现，现在只能通过数据库层面（或未来的接口）操作这张表。

## 数据模型说明

- 状态用 `StudyPlanStatus` 枚举表示，数据库层带 CHECK 约束，非法状态写不进去。
- 表定义在 `backend/app/models/study_plan.py`，并且必须在 `backend/app/models/__init__.py` 中导入，否则建表时会漏掉这张表。
- SQLite 不保存时区信息，时间以 UTC 写入，读出来是不带时区的值。

## 下一步计划（建议顺序）

1. ~~定义学习计划数据模型并初始化数据库~~（已完成）
2. 为学习计划编写 Pydantic 出入参结构（`app/schemas/study_plan.py`）。
3. 实现学习计划的 CRUD 接口（`app/api/routes/study_plans.py`）。
4. 前端接入 Vue Router 与 Pinia，做「首页 / 学习计划」页面。
5. 接入大模型 API，做「答疑 / 总结 / 出题」等核心能力。
