# 农场大亨 - 多平台游戏系统架构设计

## 1. 系统概述

### 1.1 项目愿景
农场大亨是一个跨平台农场经营模拟游戏，支持网页端和本地部署两种运行模式，实现统一的用户账户系统和实时数据同步。

### 1.2 系统架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│                        客户端层                                  │
│  ┌─────────────────┐              ┌─────────────────┐          │
│  │   网页端 (Web)  │              │  本地部署版     │          │
│  │   React + TS   │              │  Electron/Tauri │          │
│  └────────┬────────┘              └────────┬────────┘          │
│           │                                │                    │
│           └────────────┬───────────────────┘                    │
│                        │                                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    API 网关层                                ││
│  │              Nginx / API Gateway                            ││
│  │         (负载均衡 / 限流 / 缓存 / SSL)                       ││
│  └────────────────────────┬───────────────────────────────────┘│
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    服务层                                    ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   ││
│  │  │ 用户服务  │  │ 游戏服务  │  │ 社交服务  │  │ 统计服务  │   ││
│  │  │ (Auth)   │  │ (Game)   │  │ (Social) │  │ (Stats)  │   ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   ││
│  └────────────────────────┬───────────────────────────────────┘│
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    数据层                                    ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   ││
│  │  │ PostgreSQL│  │  Redis   │  │  MinIO   │  │   日志   │   ││
│  │  │ 主数据库  │  │ 缓存/会话 │  │ 文件存储 │  │ 聚合服务 │   ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 2. 技术选型

### 2.1 核心技术栈

| 层级 | 技术选型 | 版本要求 | 说明 |
|------|---------|---------|------|
| 前端框架 | React | 18.x | 现代前端UI框架 |
| 语言 | TypeScript | 5.x | 类型安全 |
| 状态管理 | Zustand | 4.x | 轻量级状态管理 |
| UI组件 | Ant Design | 5.x | 企业级UI组件库 |
| 后端框架 | FastAPI | 0.109.x | 高性能Python Web框架 |
| 数据库 | PostgreSQL | 15.x | 关系型数据库 |
| 缓存 | Redis | 7.x | 缓存与会话存储 |
| 认证 | JWT | - | 跨平台身份验证 |
| 容器化 | Docker | 24.x | 应用容器化 |
| 部署 | Docker Compose | 2.x | 本地部署编排 |

### 2.2 代码共享策略

```
代码复用结构：
├── core/                    # 核心业务逻辑 (100% 复用)
│   ├── game_manager.py      # 游戏管理器
│   ├── farming_system.py    # 农业系统
│   ├── economy.py           # 经济系统
│   └── time_system.py       # 时间系统
│
├── models/                  # 数据模型 (100% 复用)
│   ├── player.py            # 玩家模型
│   ├── crop.py             # 作物模型
│   └── achievement.py       # 成就模型
│
├── config/                  # 配置文件 (100% 复用)
│   ├── settings.py          # 全局设置
│   └── enums.py            # 枚举定义
│
├── backend/api/            # 后端API (仅服务器模式)
│   ├── auth.py             # 认证接口
│   ├── sync.py             # 数据同步接口
│   └── multiplayer.py      # 多人游戏接口
│
└── frontend/               # 前端界面 (差异化适配)
    ├── web/                # 网页端专用
    └── desktop/            # 桌面端专用
```

## 3. 功能模块设计

### 3.1 用户认证系统

#### 3.1.1 功能清单
- 用户注册（邮箱/用户名）
- 用户登录（JWT令牌）
- 密码重置
- 会话管理
- 跨平台身份验证

#### 3.1.2 API设计

```
POST   /api/auth/register     # 用户注册
POST   /api/auth/login        # 用户登录
POST   /api/auth/refresh     # 刷新令牌
POST   /api/auth/logout      # 登出
GET    /api/auth/me          # 获取当前用户信息
POST   /api/auth/password/reset  # 密码重置
```

#### 3.1.3 JWT令牌结构
```json
{
  "sub": "user_id",
  "username": "farm_master",
  "role": "player",
  "exp": 1700000000,
  "iat": 1699999999,
  "platform": "web|desktop"
}
```

### 3.2 数据同步系统

#### 3.2.1 同步策略
- **实时同步**：游戏进度使用WebSocket实时同步
- **增量同步**：仅同步变更的数据
- **冲突解决**：服务器时间戳优先策略
- **离线支持**：本地缓存 + 联网后自动同步

#### 3.2.2 API设计

```
GET    /api/sync/status      # 获取同步状态
POST   /api/sync/push        # 推送本地数据
GET    /api/sync/pull        # 获取服务器数据
POST   /api/sync/resolve     # 冲突解决
WS     /ws/sync              # 实时同步通道
```

#### 3.2.3 数据模型
```python
class GameSave(BaseModel):
    user_id: str
    version: str
    timestamp: datetime
    player_data: dict
    farm_data: dict
    inventory_data: dict
    achievements: List[str]
    statistics: dict
```

### 3.3 多人游戏系统

#### 3.3.1 功能设计
- 玩家好友系统
- 农场访问（访问好友农场）
- 交易系统（玩家间作物交易）
- 排行榜（财富/成就/等级）
- 多人活动（节日活动）

#### 3.3.2 API设计
```
GET    /api/friends/list         # 好友列表
POST   /api/friends/add          # 添加好友
DELETE /api/friends/:id          # 删除好友
GET    /api/farm/:id             # 访问农场
POST   /api/trade/offer         # 发起交易
POST   /api/trade/accept         # 接受交易
GET    /api/leaderboard          # 排行榜
```

### 3.4 性能优化系统

#### 3.4.1 前端优化
- 代码分割（Code Splitting）
- 懒加载（Lazy Loading）
- 资源压缩与CDN
- 浏览器缓存策略
- Service Worker离线缓存

#### 3.4.2 后端优化
- 数据库连接池
- Redis缓存热点数据
- 异步任务队列（Celery）
- API响应压缩
- 数据库查询优化

## 4. 部署方案

### 4.1 网页端部署

#### 4.1.1 部署架构
```
用户访问 → CDN → 静态资源 (S3/OSS)
                ↓
           API Gateway → 后端服务 → 数据库
```

#### 4.1.2 环境要求
- Node.js 20.x
- Nginx 1.24.x
- PostgreSQL 15.x
- Redis 7.x

### 4.2 本地部署（Docker Compose）

#### 4.2.1 容器架构
```yaml
services:
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
  redis:
    image: redis:7-alpine
    
  backend:
    build: ./backend
    depends_on:
      - postgres
      - redis
    
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
```

#### 4.2.2 系统要求
- 最低配置：2核CPU / 4GB内存 / 20GB存储
- 推荐配置：4核CPU / 8GB内存 / 50GB存储
- 支持50+并发用户

### 4.3 环境变量配置

```env
# 数据库配置
DATABASE_URL=postgresql://user:pass@localhost:5432/farming_game
REDIS_URL=redis://localhost:6379/0

# JWT配置
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
MAX_CONNECTIONS=50

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/var/log/farming_game/app.log
```

## 5. 安全设计

### 5.1 认证安全
- JWT令牌 + 刷新令牌机制
- 密码bcrypt加密存储
- 登录失败次数限制
- CSRF防护

### 5.2 数据安全
- HTTPS全站加密
- SQL注入防护
- XSS防护
- 请求频率限制

### 5.3 隐私保护
- 用户数据加密存储
- 敏感信息脱敏
- GDPR合规支持

## 6. 监控与日志

### 6.1 日志系统
- 应用日志（结构化JSON）
- 访问日志（Nginx）
- 错误日志（统一收集）
- 审计日志（关键操作）

### 6.2 监控指标
- API响应时间
- 数据库查询性能
- 内存/CPU使用率
- 并发连接数
- 错误率

### 6.3 告警规则
- 错误率 > 5% 触发告警
- 响应时间 > 2s 触发告警
- CPU > 80% 持续5分钟告警

## 7. 测试策略

### 7.1 测试覆盖率目标
- 单元测试覆盖率 > 80%
- 集成测试覆盖率 > 70%
- E2E测试覆盖核心流程

### 7.2 测试类型
| 类型 | 工具 | 覆盖率目标 |
|-----|------|-----------|
| 单元测试 | pytest/jest | 80% |
| 集成测试 | pytest | 70% |
| E2E测试 | Playwright | 核心流程 |
| 压力测试 | Locust | 50+并发 |

## 8. 实施路线图

### Phase 1: 基础架构（1周）
- [x] 项目结构设计
- [ ] 用户认证系统实现
- [ ] 基础API框架搭建

### Phase 2: 核心功能（2周）
- [ ] 数据同步API
- [ ] 游戏进度保存/加载
- [ ] 好友系统基础

### Phase 3: 部署优化（1周）
- [ ] Docker配置
- [ ] 性能优化
- [ ] 监控告警

### Phase 4: 测试与文档（1周）
- [ ] 测试用例编写
- [ ] 部署文档
- [ ] 用户手册

## 9. 版本兼容性

### 9.1 客户端版本支持

| 平台 | 最低版本 | 测试频率 |
|-----|---------|---------|
| Chrome | 90+ | 每周 |
| Firefox | 88+ | 每周 |
| Safari | 14+ | 每周 |
| Edge | 90+ | 每周 |
| Windows | 10 | 每月 |
| macOS | 11 | 每月 |

### 9.2 向后兼容性
- API版本化管理（v1/v2）
- 数据结构版本字段
- 渐进式功能开关

---

**文档版本**: 1.0  
**最后更新**: 2026-03-13  
**维护者**: Development Team
