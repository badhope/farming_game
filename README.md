# 🌾 农场模拟器 - Web 版

![Version](https://img.shields.io/badge/version-4.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Node](https://img.shields.io/badge/node-18%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

> **这是一个 AI 驱动的农场模拟游戏**，正在从桌面版迁移到 Web 平台。

> **当前状态**: 🚧 开发中 (v4.1.0)

---

## ⚠️ 重要提示

**本项目正在进行 Web 化改造，核心功能已基本完成！**

---

## 📋 开发进度

### ✅ 已完成 (v4.1.0 - 2026.03.10)

#### 1. 代码清理和重构
- ✅ 删除 Tkinter GUI 相关代码（ui/ 目录）
- ✅ 删除冗余系统（systems/, demos/, audio/ 目录）
- ✅ 简化 models 模块，移除不必要的模块
- ✅ 优化项目结构，为 Web API 做准备
- ✅ 修复属性名不匹配问题（gold -> money, level/exp/stamina 属性缺失）

#### 2. FastAPI 后端架构
- ✅ 创建 FastAPI 应用框架
- ✅ 配置 CORS 中间件 + Vite 代理支持
- ✅ 创建 API 路由：
  - `/api/farm` - 农场管理（获取地块、种植、浇水、收获、清空）
  - `/api/player` - 玩家数据（创建游戏、获取信息、统计、成就）
  - `/api/ai` - AI 功能（聊天、种植建议、农场分析、知识库、API配置）
  - `/api/game` - 游戏控制（时间推进、保存、加载、存档列表、重置）
  - `/api/shop` - 商店系统（商品列表、购买、购买历史）
- ✅ 创建 Pydantic Schemas
- ✅ 配置 SQLite 数据库（SQLAlchemy）
- ✅ 创建数据库模型

#### 3. 游戏会话服务
- ✅ 创建 GameSessionService 管理游戏状态
- ✅ 集成核心游戏逻辑（GameManager）
- ✅ 实现存档/读档功能（JSON 文件）
- ✅ 实现游戏时间推进逻辑

#### 4. React 前端架构
- ✅ 使用 Vite 创建 React + TypeScript 项目
- ✅ 安装核心依赖：
  - Ant Design (UI 组件库)
  - React Router (路由)
  - Axios (HTTP 客户端)
- ✅ 响应式布局（移动端适配）
- ✅ 页面组件：
  - Home (游戏开始页)
  - Farm (农场页面)
  - Shop (商店页面)
  - Achievements (成就页面)
  - Statistics (统计页面)
  - AIAssistant (AI助手页面)
  - GameLayout (游戏布局)

#### 5. 核心功能
- ✅ 农场系统：种植、浇水、收获、作物生长
- ✅ 商店系统：购买种子、肥料、工具、建筑
- ✅ AI助手：聊天、种植建议、农场分析
- ✅ 自定义AI API配置：支持 OpenAI/Claude/自定义API
- ✅ 存档系统：保存、加载、删除存档
- ✅ 游戏状态：金币、体力、时间、天气

#### 6. 界面优化
- ✅ 移动端适配（Drawer 菜单、响应式布局）
- ✅ 设置面板（快捷操作、游戏状态）
- ✅ 友好的错误提示

---

## 🚀 快速开始

### 前置要求
- Python 3.8+
- Node.js 18+

### 安装依赖

```bash
# 安装后端依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
```

### 启动开发服务器

```bash
# 启动后端 (终端1)
uvicorn backend.main:app --reload --port 8000

# 启动前端 (终端2)
cd frontend
npm run dev
```

访问 http://localhost:5173 开始游戏！

---

## 📁 项目结构

```
farming_game/
├── backend/
│   ├── api/              # API 路由
│   │   ├── farm.py       # 农场API
│   │   ├── player.py     # 玩家API
│   │   ├── ai.py         # AI API
│   │   ├── game.py       # 游戏控制API
│   │   └── shop.py       # 商店API
│   ├── services/         # 业务逻辑
│   │   └── game_session.py
│   └── main.py           # FastAPI 应用
├── frontend/
│   ├── src/
│   │   ├── api/         # API 客户端
│   │   ├── pages/       # 页面组件
│   │   ├── store/       # 状态管理
│   │   └── types/       # TypeScript 类型
│   └── vite.config.ts   # Vite 配置
├── core/                # 核心游戏逻辑
├── models/              # 数据模型
└── data/                # 游戏数据存档
```

---

## � 待完成功能

- [ ] 完善游戏事件系统
- [ ] 添加更多作物和道具
- [ ] 成就系统完善
- [ ] 统计页面图表
- [ ] 玩家交互系统
- [ ] 任务系统
- [ ] 部署文档

---

## � License

MIT License
