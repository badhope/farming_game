# 🌾 农场模拟器 - Web 版开发中

![Version](https://img.shields.io/badge/version-4.0--dev-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Node](https://img.shields.io/badge/node-18%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

> **这是一个 AI 驱动的农场模拟游戏**，正在从桌面版迁移到 Web 平台。
> 
> **当前状态**: 🚧 开发中 (v4.0 Web 迁移)

---

## ⚠️ 重要提示

**本项目正在进行 Web 化改造，尚未完成！**

当前版本只包含**后端 API 框架**和**前端基础架构**，核心游戏逻辑正在迁移中。

---

## 📋 开发进度

### ✅ 已完成 (v3.0 - 2026.03.10)

#### 1. 代码清理和重构
- ✅ 删除 Tkinter GUI 相关代码（ui/ 目录）
- ✅ 删除冗余系统（systems/, demos/, audio/ 目录）
- ✅ 简化 models 模块，移除不必要的模块
- ✅ 优化项目结构，为 Web API 做准备

#### 2. FastAPI 后端架构
- ✅ 创建 FastAPI 应用框架
- ✅ 配置 CORS 中间件
- ✅ 创建 API 路由骨架：
  - `/api/farm` - 农场管理
  - `/api/player` - 玩家数据
  - `/api/ai` - AI 功能
  - `/api/game` - 游戏控制
- ✅ 创建 Pydantic Schemas
- ✅ 配置 SQLite 数据库（SQLAlchemy）
- ✅ 创建数据库模型

#### 3. React 前端架构
- ✅ 使用 Vite 创建 React + TypeScript 项目
- ✅ 安装核心依赖：
  - Ant Design (UI 组件库)
  - React Router (路由)
  - Axios (HTTP 客户端)
  - Recharts (图表)
  - Framer Motion (动画)
  - React Hot Toast (通知)

#### 4. 项目文档
- ✅ 更新 requirements.txt
- ✅ 创建基础启动脚本

---

### 🚧 进行中 (v4.0 - 当前阶段)

#### 待完成的后端功能
- [ ] 实现农场管理 API 的具体逻辑
- [ ] 实现玩家数据 API 的具体逻辑
- [ ] 实现游戏控制 API 的具体逻辑
- [ ] 集成现有的 AI 系统（ai_assistant, ai_advisor, ai_analyzer）
- [ ] 实现存档/读档功能
- [ ] 实现游戏时间推进逻辑
- [ ] 添加用户认证和授权
- [ ] 添加 API 单元测试

#### 待完成的前端功能
- [ ] 创建游戏主界面组件
- [ ] 实现农田渲染和交互
- [ ] 实现种植、浇水、收获功能
- [ ] 创建玩家信息面板
- [ ] 创建背包界面
- [ ] 实现 AI 助手对话框
- [ ] 实现种植建议界面
- [ ] 实现农场分析图表
- [ ] 添加响应式设计支持

#### 待完成的部署配置
- [ ] 创建 Dockerfile（后端）
- [ ] 创建 Dockerfile（前端）
- [ ] 创建 docker-compose.yml
- [ ] 配置 Nginx 反向代理
- [ ] 编写部署文档

---

### 📅 计划中 (未来版本)

#### v4.1 - 核心玩法
- [ ] 完整的种植系统
- [ ] 天气影响系统
- [ ] 经济系统平衡
- [ ] 成就系统实现
- [ ] 任务系统实现

#### v4.2 - 社交功能
- [ ] 用户注册/登录
- [ ] 访问其他玩家农场
- [ ] 排行榜系统
- [ ] 成就分享

#### v4.3 - 移动端适配
- [ ] 响应式布局优化
- [ ] 触摸手势支持
- [ ] PWA 支持

---

## 🏗️ 技术架构

### 后端技术栈
- **框架**: FastAPI
- **语言**: Python 3.8+
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **ORM**: SQLAlchemy
- **数据验证**: Pydantic
- **AI 功能**: 规则引擎 (可接入 LLM)

### 前端技术栈
- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **UI 库**: Ant Design
- **路由**: React Router
- **状态管理**: React Context (或未来迁移到 Zustand)
- **图表**: Recharts
- **动画**: Framer Motion
- **HTTP**: Axios

### 部署方案
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **后端服务**: Uvicorn
- **前端服务**: Nginx 静态文件服务

---

## 📁 项目结构

```
farming_game/
├── backend/              # FastAPI 后端
│   ├── api/             # API 路由
│   │   ├── farm.py      # 农场管理
│   │   ├── player.py    # 玩家数据
│   │   ├── ai.py        # AI 功能
│   │   └── game.py      # 游戏控制
│   ├── database/        # 数据库配置
│   │   ├── db_config.py
│   │   └── init_db.py
│   ├── models/          # 数据库模型
│   │   └── db_models.py
│   ├── schemas/         # Pydantic Schemas
│   ├── services/        # 业务逻辑层
│   └── main.py          # FastAPI 应用入口
├── frontend/            # React 前端
│   ├── src/
│   │   ├── components/  # React 组件
│   │   ├── pages/       # 页面组件
│   │   ├── api/         # API 调用
│   │   ├── hooks/       # 自定义 Hooks
│   │   ├── store/       # 状态管理
│   │   └── App.tsx      # 应用入口
│   └── package.json
├── core/                # 核心游戏逻辑 (待迁移)
│   ├── game_manager.py
│   ├── time_system.py
│   └── economy.py
├── models/              # 数据模型 (待迁移)
├── ai/                  # AI 系统 (待集成)
├── config/              # 配置文件
├── data/                # 游戏数据 (JSON)
├── tests/               # 测试文件
├── requirements.txt     # Python 依赖
├── start_backend.py     # 后端启动脚本
└── README.md            # 本文档
```

---

## 🚀 开发环境搭建

### 后端开发

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 初始化数据库
python backend/database/init_db.py

# 3. 启动后端服务器
python start_backend.py

# 访问 API 文档
# http://localhost:8000/api/docs
```

### 前端开发

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖 (已完成)
npm install

# 3. 启动开发服务器
npm run dev

# 访问前端
# http://localhost:5173
```

---

## 🎮 当前可用的功能

### 后端 API
- ✅ 健康检查：`GET /api/health`
- ✅ API 文档：`GET /api/docs`
- ⚠️ 农场管理：基础框架（未实现具体逻辑）
- ⚠️ 玩家数据：基础框架（未实现具体逻辑）
- ⚠️ AI 功能：基础框架（未实现具体逻辑）
- ⚠️ 游戏控制：基础框架（未实现具体逻辑）

### 前端
- ✅ Vite + React + TypeScript 项目框架
- ✅ Ant Design UI 库集成
- ⚠️ 游戏界面：待开发

---

## 📝 下一步工作

### 立即可做
1. **实现后端 API 逻辑** - 将现有 Python 游戏逻辑迁移到 FastAPI
2. **开发前端界面** - 创建游戏主界面和基础交互
3. **前后端联调** - 测试 API 和 UI 集成

### 优先级排序
1. 🔴 **高优先级**: 后端农场管理 API 实现
2. 🔴 **高优先级**: 前端游戏主界面开发
3. 🟡 **中优先级**: 后端游戏逻辑迁移
4. 🟡 **中优先级**: Docker 容器化配置
5. 🟢 **低优先级**: 移动端适配

---

## 🤝 贡献指南

如果你想参与开发：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- **项目状态**: 开发中
- **最后更新**: 2026-03-10
- **当前版本**: v4.0-dev

---

## 🙏 致谢

感谢所有参与开发的贡献者！

**注意**: 这是一个个人学习项目，主要用于技术实验和农业知识学习。
