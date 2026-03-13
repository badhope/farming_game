# 农场大亨 - 部署指南

## 目录
- [快速开始](#快速开始)
- [系统要求](#系统要求)
- [部署方式](#部署方式)
  - [Docker Compose 部署（推荐）](#docker-compose-部署推荐)
  - [手动部署](#手动部署)
- [配置说明](#配置说明)
- [验证部署](#验证部署)
- [运维指南](#运维指南)
- [故障排查](#故障排查)

---

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/badhope/farming_game.git
cd farming_game
```

### 2. 启动服务
```bash
# 使用 Docker Compose 一键启动
docker-compose up -d

# 或者启动开发版本
docker-compose -f docker-compose.dev.yml up -d
```

### 3. 访问应用
- 前端：http://localhost
- API文档：http://localhost/api/docs

---

## 系统要求

### 最低配置
| 项目 | 要求 |
|------|------|
| CPU | 2 核 |
| 内存 | 4 GB |
| 磁盘 | 20 GB |
| 系统 | Ubuntu 20.04+ / Windows 10+ / macOS 11+ |
| Docker | 24.0+ |
| Docker Compose | 2.0+ |

### 推荐配置
| 项目 | 要求 |
|------|------|
| CPU | 4 核 |
| 内存 | 8 GB |
| 磁盘 | 50 GB SSD |
| 系统 | Ubuntu 22.04+ |
| 网络 | 带宽 10Mbps+ |

---

## 部署方式

### Docker Compose 部署（推荐）

#### 1. 环境准备
```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. 配置环境变量
```bash
# 复制环境配置示例
cp .env.example .env

# 编辑 .env 文件，修改以下关键配置：
# - JWT_SECRET: 生成一个强随机密钥
# - POSTGRES_PASSWORD: 设置数据库密码
```

#### 3. 启动服务
```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 4. 服务端口
| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 80, 443 | Web 应用 |
| API | 8000 | 后端服务 |
| PostgreSQL | 5432 | 数据库 |
| Redis | 6379 | 缓存 |

---

### 手动部署

#### 1. 安装依赖

**Ubuntu/Debian:**
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# 安装 Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 安装 PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# 安装 Redis
sudo apt install -y redis-server

# 安装 Nginx
sudo apt install -y nginx
```

**Windows:**
```powershell
# 使用 Chocolatey 安装
choco install python nodejs.postgresql redis nginx
```

#### 2. 数据库设置
```bash
# 创建数据库
sudo -u postgres psql
CREATE DATABASE farming_game;
CREATE USER farming_game WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE farming_game TO farming_game;
\q
```

#### 3. 配置后端
```bash
# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python -m backend.database.init_db

# 启动后端服务
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 4. 配置前端
```bash
cd frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 配置 Nginx
sudo cp nginx.conf /etc/nginx/sites-available/farming_game
sudo ln -s /etc/nginx/sites-available/faming_game /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

---

## 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DATABASE_URL` | - | PostgreSQL 连接字符串 |
| `REDIS_URL` | - | Redis 连接字符串 |
| `JWT_SECRET` | - | JWT 密钥（必须修改） |
| `JWT_ALGORITHM` | HS256 | JWT 算法 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 | 访问令牌过期时间 |
| `SERVER_HOST` | 0.0.0.0 | 服务器监听地址 |
| `SERVER_PORT` | 8000 | 服务器监听端口 |
| `MAX_CONNECTIONS` | 50 | 最大连接数 |
| `LOG_LEVEL` | INFO | 日志级别 |
| `CORS_ORIGINS` | - | CORS 允许的来源 |

### 性能调优

#### PostgreSQL 配置
```sql
-- 编辑 postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB
maintenance_work_mem = 128MB
```

#### Redis 配置
```conf
# 编辑 redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
appendonly yes
```

#### Nginx 配置
```nginx
# 启用 gzip 压缩
gzip on;
gzip_types text/plain application/json application/javascript;

# 静态资源缓存
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## 验证部署

### 1. 检查服务状态
```bash
# Docker 方式
docker-compose ps

# 手动方式
curl http://localhost/health
curl http://localhost/api/health
```

### 2. API 测试
```bash
# 测试注册
curl -X POST http://localhost/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'

# 测试登录
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

### 3. 压力测试（可选）
```bash
# 使用 ab 进行压力测试
ab -n 1000 -c 10 http://localhost/

# 或使用 wrk
wrk -t12 -c400 -d30s http://localhost/
```

---

## 运维指南

### 日志管理
```bash
# 查看应用日志
docker-compose logs -f backend

# 查看 Nginx 日志
docker-compose logs -f nginx

# 日志轮转
sudo logrotate -f /etc/logrotate.d/nginx
```

### 备份与恢复
```bash
# 备份数据库
docker-compose exec postgres pg_dump -U farming_game farming_game > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker-compose exec -T postgres psql -U farming_game farming_game < backup_20240313.sql
```

### 更新部署
```bash
# 拉取最新代码
git pull origin main

# 重新构建并重启
docker-compose up -d --build

# 迁移数据库（如有）
docker-compose exec backend python -m alembic upgrade head
```

### 监控
```bash
# 查看资源使用
docker stats

# 查看详细指标
curl http://localhost/api/health/detailed
```

---

## 故障排查

### 常见问题

#### 1. 服务无法启动
```bash
# 检查端口占用
netstat -tulpn | grep :8000

# 检查日志
docker-compose logs backend
```

#### 2. 数据库连接失败
```bash
# 检查数据库容器
docker-compose ps postgres

# 测试数据库连接
docker-compose exec backend python -c "from backend.database.db_config import engine; engine.connect()"
```

#### 3. 前端加载失败
```bash
# 检查 Nginx 配置
nginx -t

# 检查前端构建
docker-compose logs frontend

# 检查静态文件
ls -la frontend/dist/
```

#### 4. 性能问题
```bash
# 检查资源使用
docker stats

# 检查慢查询日志
docker-compose exec postgres cat /var/log/postgresql/postgresql-*.log

# 检查 Redis 状态
docker-compose exec redis redis-cli info
```

### 获取帮助
- 提交 Issue: https://github.com/badhope/farming_game/issues
- 文档 Wiki: https://github.com/badhope/farming_game/wiki

---

**文档版本**: 1.0  
**最后更新**: 2026-03-13
