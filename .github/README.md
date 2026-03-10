# GitHub Actions 工作流说明

本项目包含三个 CI/CD 工作流：

## 📁 工作流文件

### 1. `ci.yml` (推荐使用)
完整的前后端联合 CI 工作流，会在推送和 PR 时自动运行。

**触发条件：**
- 推送到 `main` 或 `develop` 分支
- 任何 PR 指向 `main` 或 `develop` 分支

**检查项目：**
- ✅ Python 后端代码格式化检查 (Black)
- ✅ Python 后端代码风格检查 (Flake8)
- ✅ Python 后端单元测试 (pytest)
- ✅ Python 后端导入验证
- ✅ 前端 ESLint 检查
- ✅ 前端 TypeScript 类型检查
- ✅ 前端构建检查

### 2. `backend-ci.yml`
独立的后端 CI 工作流，仅在 Python 文件变更时运行。

### 3. `frontend-ci.yml`
独立的前端 CI 工作流，仅在 `frontend/` 目录文件变更时运行。

## 🚀 使用方法

1. **推送代码到 GitHub**：
   ```bash
   git push origin main
   ```

2. **创建 Pull Request**：
   - 前往 GitHub 仓库
   - 点击 "Compare & pull request"
   - CI 会自动运行

3. **查看结果**：
   - 在 PR 页面查看检查状态
   - 点击 "Actions" 标签查看详细日志

## ⚙️ 配置说明

- **Python 版本**: 3.11
- **Node.js 版本**: 20
- **依赖缓存**: 启用（加快构建速度）
- **失败策略**: 使用 `|| true` 避免阻塞提交（可改为严格模式）

## 🎯 建议

生产环境建议将 `|| true` 移除，使检查失败时阻止合并。
