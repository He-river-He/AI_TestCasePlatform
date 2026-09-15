# AI Testcase Studio

AI Testcase Studio（AI 测试用例管理平台）是一套面向测试团队的 AI 用例生产与管理工具。平台将需求解析、功能点确认、测试用例生成、人工评审、用例入库、测试执行、知识沉淀和 AI 效果评测串成一条可追溯的工作流。

项目适合用于：

- 从 PRD 或功能清单快速生成候选测试用例
- 结合业务知识库减少 AI 生成偏离业务规则的问题
- 通过人工评审将高质量候选用例沉淀到项目用例库
- 管理测试任务、执行批次、执行结果和缺陷信息
- 对不同模型、Prompt 或生成策略进行回归评测

## 核心流程

```text
需求导入
  -> 设计稿导入（可跳过）
  -> 功能点解析与确认
  -> 测试范围维护
  -> AI 生成测试用例
  -> 规则质检与 AI Judge
  -> 人工评审入库
  -> 测试任务执行
  -> 知识沉淀与效果评测
```

每一步都会保留前后关联关系，方便从正式用例回溯到生成任务、功能点和原始需求。

## 主要功能

### 项目与需求管理

- 创建、编辑、删除和搜索项目
- 支持粘贴文本、上传 `.docx` / `.md` / `.markdown` 文件导入需求
- 支持导入和导出 `.xlsx` / `.md` 功能清单
- 自动将需求结构化为模块、功能点、描述、验收标准、约束和优先级
- 支持维护不测范围、风险和待澄清事项

### 设计稿解析

- 支持上传 PNG、JPG、WebP 设计稿
- 使用视觉模型识别页面元素、交互、状态、校验和错误提示
- 设计功能点可编辑、筛选和确认
- 确认后可合并到需求功能点列表，并保留设计稿来源
- 支持关联 Figma 官方链接；当前版本不读取远程画板，自动解析需要同时提供页面截图

### AI 用例生成

- 快速冒烟：围绕每个功能点快速生成少量冒烟用例
- 完整覆盖：覆盖功能、边界和异常场景
- 支持叠加安全/权限、接口测试等专项 Skill
- 支持按功能点检索项目知识库，将相关业务规则注入生成上下文
- 支持异步生成、进度展示、暂停、恢复和失败任务重试
- 自动执行规则质检和 AI Judge，输出质量分数、问题标记和覆盖率信息

### 评审与用例库

- 候选用例支持采纳、驳回和编辑
- 驳回必须填写原因，便于后续进行 badcase 分析
- 支持导出候选用例
- 正式用例按项目、模块、功能点三级目录组织
- 支持列表视图和脑图视图
- 支持按冒烟用例筛选和目录重命名

### 测试任务执行

- 创建测试任务并选择需要执行的用例
- 支持多个执行批次，例如线下测试、预发测试和线上测试
- 单条或批量标记通过、失败、阻塞和未执行
- 记录执行备注和缺陷编号
- 汇总通过率、失败数、阻塞数和待执行数

### 知识库与 RAG

- 每个项目拥有独立知识库
- 支持业务文档、历史用例和缺陷记录三类知识来源
- Markdown 文档按标题路径分块，便于检索结果溯源
- 使用向量检索和 BM25 关键词检索进行混合召回
- 可选配置 Rerank 模型进行精排
- 支持检索测试，帮助验证知识库召回效果

### AI 效果评测

- 创建包含 PRD 和人工标准测试点的评测样本
- 按不同运行标签执行批量生成和评分
- 统计生成成功率、可用率、场景召回率、重复率、幻觉数和 Token 消耗
- 支持查看单个样本的未覆盖测试点和问题用例
- 评测数据与业务项目隔离保存

### 模型与系统设置

- 独立配置生成、视觉解析、评测、Embedding 和 Rerank 模型
- 使用 OpenAI 兼容接口接入不同模型服务
- API Key 保存后仅返回掩码，不在页面明文回显
- 未配置 API Key 时可使用 Mock 模式体验完整流程

## 技术架构

| 层级 | 技术 |
| --- | --- |
| 前端 | React、React Router、Ant Design、Vite |
| 后端 | FastAPI、SQLAlchemy、Pydantic |
| 数据库 | SQLite（开发环境默认） |
| AI 编排 | LangChain、LangGraph |
| 模型接口 | OpenAI 兼容 Chat、Vision、Embeddings API |
| 向量检索 | ChromaDB、BM25、可选 Rerank |
| 文件处理 | python-docx、openpyxl |

前后端职责划分如下：

- 前端负责页面、交互、流程状态展示和 API 请求封装
- 后端负责认证、业务数据、文件解析、AI 调用、工作流编排和知识库管理
- Skill 目录负责维护不同 AI 能力的 Manifest、Prompt 和 Handler

## 目录结构

```text
AITC/
├── backend/
│   ├── app/
│   │   ├── api/              # HTTP API 路由
│   │   ├── ai/               # 模型、Embedding、检索相关封装
│   │   ├── models/           # SQLAlchemy 数据模型
│   │   ├── schemas/          # Pydantic 请求与响应模型
│   │   ├── services/         # 业务服务
│   │   ├── skills/           # AI Skill、Prompt 和 Handler
│   │   └── workflows/        # LangGraph 工作流
│   ├── pyproject.toml        # 后端依赖与项目配置
│   └── uv.lock               # Python 依赖锁定文件
├── web/
│   ├── src/
│   │   ├── components/       # 通用组件
│   │   ├── layouts/          # 应用布局
│   │   ├── pages/            # 页面
│   │   ├── services/         # API 请求封装
│   │   ├── styles/           # 全局样式
│   │   └── utils/            # 工具函数
│   ├── package.json          # 前端依赖与脚本
│   └── vite.config.js        # Vite 配置
├── docs/                     # PRD、架构、接口和开发文档
├── .env.example              # 环境变量模板
├── setup.bat                 # Windows 首次安装脚本
├── start.bat                 # Windows 启动脚本
└── restart.bat               # Windows 清理端口并重启脚本
```

运行时数据默认写入 `backend/data/`，包括 SQLite 数据库、向量库和设计稿资源。该目录不应提交到代码仓库，也不应在团队间直接共享。

## 快速开始

### 环境要求

- Python 3.12 或更高版本
- Node.js 20 或更高版本
- npm

开发环境默认使用 SQLite 和 Mock 模式，不需要单独安装数据库，也不要求一开始配置真实模型 Key。

### 1. 准备环境变量

在项目根目录执行：

```powershell
Copy-Item .env.example .env
```

### 2. 安装并启动后端

```powershell
Set-Location backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m uvicorn app.main:app --reload --port 8000
```

后端启动后：

- API 地址：`http://localhost:8000`
- Swagger 文档：`http://localhost:8000/docs`

### 3. 安装并启动前端

新开一个终端窗口：

```powershell
Set-Location web
npm install
npm run dev
```

前端地址：`http://localhost:5173`

Vite 会将前端的 `/api` 请求代理到后端 `http://localhost:8000`，因此前后端需要同时运行。

Windows 用户也可以在完成依赖安装后使用根目录的 `start.bat` 启动前后端，使用 `restart.bat` 清理 `8000` 和 `5173` 端口后重新启动。

## 配置说明

`.env.example` 已提供完整配置模板，常用配置如下：

| 配置 | 说明 |
| --- | --- |
| `LLM_API_KEY` | 用例生成模型的 API Key |
| `LLM_BASE_URL` | OpenAI 兼容模型服务地址 |
| `LLM_MODEL` | 用例生成模型名称 |
| `LLM_MOCK_MODE` | 是否启用 Mock 模式，默认 `true` |
| `VISION_API_KEY` / `VISION_BASE_URL` / `VISION_MODEL` | 设计稿视觉解析模型 |
| `EMBEDDING_API_KEY` / `EMBEDDING_BASE_URL` / `EMBEDDING_MODEL` | 知识库 Embedding 模型 |
| `RERANK_API_KEY` / `RERANK_BASE_URL` / `RERANK_MODEL` | 可选的知识库精排模型 |
| `EVAL_LLM_API_KEY` / `EVAL_LLM_BASE_URL` / `EVAL_LLM_MODEL` | 评测专用模型，留空时复用生成模型 |
| `DATABASE_URL` | 数据库连接地址，默认使用 SQLite |
| `CORS_ORIGINS` | 允许访问后端的前端地址 |
| `AUTH_USERNAME` / `AUTH_PASSWORD` | 默认登录账号配置 |

建议先保持 `LLM_MOCK_MODE=true` 验证业务链路，再配置真实模型。配置真实模型后，也可以在页面的「设置」中维护模型信息并测试连通性。

生产环境需要：

- 设置 `DEBUG=false`
- 将 `AUTH_PASSWORD` 修改为至少 16 位且非默认值的强密码
- 妥善保管 `.env` 和数据库文件
- 根据部署环境配置 `CORS_ORIGINS`
- 为视觉解析和知识库检索分别配置对应模型

## 首次体验

1. 打开 `http://localhost:5173` 并登录或注册账号。
2. 创建一个项目。
3. 进入 AI 生成流程，粘贴一段需求文本，或上传 `.docx` / Markdown 文件。
4. 解析并确认功能点，维护测试范围。
5. 选择快速冒烟或完整覆盖策略，按需开启专项 Skill 和知识库检索。
6. 查看生成进度，完成候选用例评审。
7. 将采纳的用例加入用例库，并创建测试任务执行。
8. 在知识库和评测页面继续沉淀业务知识、验证召回效果和对比模型配置。

## 注意事项

- API 除登录、注册和健康检查接口外，都需要携带登录 Token。
- 服务重启后，内存中的登录会话会失效，需要重新登录。
- Figma 链接当前用于关联展示，不会直接读取远程画板内容。
- 没有配置真实视觉模型时，设计稿解析只能在 Mock 条件下使用示例数据。
- 没有配置 Embedding 模型时，知识库可在 Mock 模式下体验流程，但真实语义检索能力会受限。

