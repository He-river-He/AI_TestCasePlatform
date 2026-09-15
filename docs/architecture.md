# AI 测试用例管理平台架构分析 v0.1

## 1. 项目定位

本项目是一个 AI 测试用例管理平台，目标是帮助测试人员从需求文档中提取功能点，并自动生成、评审、管理和执行测试用例。

核心流程：

需求文档 → 功能点 → AI 生成用例 → 人工评审 → 用例库 → 测试执行 → 报告分析

## 2. 前后端职责划分

### 后端职责

- 提供 API 接口
- 管理用户登录和权限
- 管理项目、需求、测试用例、测试任务等数据
- 调用 AI 模型生成测试用例
- 管理知识库和 RAG 检索
- 保存数据到数据库

### 前端职责

- 提供用户操作界面
- 展示项目、需求、用例、任务等数据
- 调用后端 API
- 展示 AI 生成流程和结果
- 支持用户编辑、确认、筛选和执行测试用例

## 3. 后端目录理解

- main.py 只负责组装应用
- api/ 负责HTTP接口
- models/ 负责数据库表
- schemas/ 负责接口输入输出结构
- services/ 负责业务逻辑
- database.py 负责数据库连接和会话管理
- config.py 负责配置读取
## 4. 前端目录理解

参考项目前端主要目录：

- src/main.jsx：前端入口
- src/App.jsx：路由配置
- src/layouts/：后台管理系统布局
- src/pages/：页面组件
- src/components/：通用组件
- src/services/api.js：后端接口请求封装
- src/styles/：全局样式
- src/utils/：工具函数

## 5. 核心业务模块

当前我理解的平台核心模块包括：

- 用户认证模块
- 项目管理模块
- 需求文档模块
- 功能点管理模块
- AI 测试用例生成模块
- 测试用例评审模块
- 测试用例库模块
- 测试任务执行模块
- 知识库 / RAG 模块
- 系统设置模块
- AI 小助手模块

## 6. 核心数据流

核心数据关系大致是：

Project
→ RequirementDocument
→ RequirementItem
→ GenerationTask
→ GeneratedCaseDraft
→ TestCase
→ TestTask / TestBatch / TestBatchCase

含义：

- Project：项目
- RequirementDocument：需求文档
- RequirementItem：从需求中拆出来的功能点
- GenerationTask：一次 AI 生成任务
- GeneratedCaseDraft：AI 生成的用例草稿
- TestCase：人工确认后的正式测试用例
- TestTask：测试任务
- TestBatch：测试批次
- TestBatchCase：批次中的用例执行记录

## 7. AI 模块理解

AI 模块不是直接写在接口里，而是拆成：

- Prompt：告诉模型怎么生成
- Skill：某一种 AI 能力，例如需求解析、用例生成、质量评估
- Workflow：把多个步骤串起来，例如检索知识、生成用例、质检、保存结果
- Mock 模式：没有 API Key 时也能跑通流程

## 8. 暂时还不理解的问题

后续学习时需要继续搞清楚：

- SQLAlchemy 模型之间的关系怎么设计
- Pydantic Schema 和 ORM Model 有什么区别
- AI 生成任务为什么要拆成 workflow
- RAG 知识库怎么分块、向量化、检索
- 前端页面和 API 怎么对应