# 🌟 星露谷物语 - 农场模拟器 🌟

![Version](https://img.shields.io/badge/version-2.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Tests](https://img.shields.io/badge/tests-50%2B%20passing-brightgreen.svg)

一款现代化的农场模拟游戏，体验田园生活的乐趣！经过全面重构，代码更清晰、更易维护。

## 🎮 游戏特色

### 🌈 全新图形界面
- **直观操作**: 鼠标点击替代繁琐的命令行输入
- **实时反馈**: 动态更新的农田状态和作物生长进度
- **美观界面**: 现代化 UI 设计，色彩丰富的视觉体验

### 🌱 丰富游戏内容
- **四季系统**: 春夏秋冬四个季节，每季有不同的适宜作物
- **天气变化**: 晴天、雨天、暴风雨等多样天气影响 gameplay
- **作物多样性**: 16 种不同作物，各有独特的生长特性和收益
- **农场升级**: 从小农场逐步扩建，解锁更多土地

### 🏆 成就系统
- **多样化成就**: 收获、财富、探索等各类成就
- **进度追踪**: 实时显示成就完成进度
- **奖励机制**: 解锁特殊奖励和称号

### 💰 经济系统
- **商店经营**: 购买种子，出售作物
- **投资回报**: 计算作物利润率，制定最优种植策略
- **财务管理**: 追踪收入支出，监控农场盈利状况

### 🛠️ 技术亮点（2026 重构版）
- ✅ **模块化架构**: 清晰的职责分离
- ✅ **配置驱动**: JSON 配置文件，支持热更新
- ✅ **单元测试**: 50+ 测试用例，保证质量
- ✅ **代码规范**: 统一枚举、类型注解、文档完整

## 🚀 快速开始

### 系统要求
- Python 3.8 或更高版本
- Windows/Linux/macOS 操作系统

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/farming_game.git
cd farming_game
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动游戏**
```bash
# 图形界面模式（推荐）
python main.py

# 或指定模式
python main.py --mode gui

# 控制台模式（兼容旧版本）
python main.py --mode console
```

4. **运行测试**
```bash
# 运行所有单元测试
python run_tests.py

# 或使用 pytest
pytest
```

## 🎯 游戏玩法

### 基础操作
1. **种植作物**: 点击空地 → 选择种子 → 确认种植
2. **日常护理**: 点击【全部浇水】或单独给作物浇水
3. **收获作物**: 点击成熟作物（带✨标志）直接收获
4. **推进时间**: 点击睡眠按钮进入下一天

### 经营策略
- **季节规划**: 根据季节选择最适合的作物
- **资金管理**: 平衡种子投资和作物销售
- **风险控制**: 关注天气预报，防范暴风雨损失
- **规模扩张**: 积累资金升级农场获得更多土地

## �️ 技术架构

### 项目结构（重构后）
```
farming_game/
├── ui/                     # 图形界面模块
│   ├── gui_main.py         # 主界面入口
│   ├── welcome_screen.py   # 欢迎界面
│   └── game_window.py      # 游戏主窗口
├── controllers/            # 控制器层
│   └── game_controller.py  # 游戏逻辑控制器
├── models/                 # 数据模型层
│   ├── farming_system.py   # 🆕 农耕系统
│   ├── building_system.py  # 🆕 建筑系统
│   ├── cooking_system.py   # 🆕 烹饪系统
│   ├── inventory_system_simple.py  # 🆕 简化背包
│   ├── player.py           # 玩家模型
│   ├── crop.py             # 作物模型
│   └── plot.py             # 地块模型
├── config/                 # 配置层
│   ├── enums.py            # 🆕 统一枚举定义
│   ├── config_loader.py    # 🆕 JSON 配置加载器
│   └── settings.py         # 游戏配置
├── data/                   # 🆕 配置数据
│   ├── crops.json          # 作物配置
│   └── achievements.json   # 成就配置
├── core/                   # 核心逻辑
│   ├── game_manager.py     # 游戏管理器
│   ├── economy.py          # 经济系统
│   └── time_system.py      # 时间系统
├── tests/                  # 🆕 单元测试
│   ├── test_farming_system.py
│   └── test_config_loader.py
├── audio/                  # 音频系统
│   └── sound_manager.py    # 音效管理器
├── systems/                # 系统模块
│   ├── tutorial.py         # 新手引导
│   └── event_system.py     # 事件系统
├── main.py                 # 程序入口
├── run_tests.py            # 🆕 测试运行脚本
├── pytest.ini              # 🆕 pytest 配置
└── REFACTOR_PROGRESS.md    # 🆕 重构进度报告
```

### 核心架构改进

#### 1. 配置驱动设计
```python
# 从 JSON 加载配置，而非硬编码
from config.config_loader import get_crop_config

potato = get_crop_config("potato")
# 支持热更新，无需修改代码
```

#### 2. 统一枚举管理
```python
# 所有枚举集中定义在 config/enums.py
from config.enums import Season, CropType, Weather

# 避免重复定义，统一使用英文
```

#### 3. 模块化系统
```python
# 每个系统职责单一，易于维护
from models.farming_system import FarmingManager
from models.building_system import BuildingManager
from models.cooking_system import CookingManager
```

#### 4. 测试保障
```python
# 50+ 测试用例覆盖核心功能
# 运行测试：python run_tests.py
```

## 📊 重构成果（2026）

本次重构解决了以下核心问题：

| 指标 | 重构前 | 重构后 | 改善 |
|------|--------|--------|------|
| 代码行数 | ~8000 | ~6500 | **-19%** |
| 重复枚举 | 3 处 | 1 处 | **-67%** |
| 硬编码配置 | 100% | 50% | **-50%** |
| 巨型类 | 1 个 | 0 个 | **-100%** |
| 死代码 | 2500 行 | 0 行 | **-100%** |
| 测试用例 | 0 个 | 50+ 个 | **+∞** |

### 删除的系统
- ❌ 生化危机战斗系统（与农场无关）
- ❌ MMORPG 装备系统（过度设计）
- ❌ 分支剧情系统（功能冗余）

### 新增的系统
- ✅ 农耕系统（独立模块）
- ✅ 建筑系统（独立模块）
- ✅ 烹饪系统（独立模块）
- ✅ 配置加载器（JSON 驱动）
- ✅ 单元测试框架

## 🤝 贡献指南

欢迎任何形式的贡献！

### 开发环境搭建
```bash
# 克隆项目
git clone https://github.com/yourusername/farming_game.git
cd farming_game

# 安装开发依赖
pip install pytest mypy black flake8

# 运行测试
pytest

# 代码检查
mypy .
flake8 .
```

### 贡献流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 版本历史

### v2.1 (2026 重构版) - 当前版本
- ✨ 全面重构代码架构
- 🗑️ 删除 2500 行死代码
- 🧪 添加 50+ 单元测试
- 📝 配置驱动设计（JSON）
- 🏗️ 拆分巨型类为独立模块
- 📚 统一枚举定义

### v2.0
- ✨ 全新图形界面
- 🎓 新手引导系统
- 🎵 音效系统
- 🎪 随机事件系统

### v1.0
- 📝 基础控制台版本
- 🌱 简单种植系统
- 💰 基础经济系统

## 📚 开发资源

- [重构进度报告](REFACTOR_PROGRESS.md) - 详细的重构文档
- [运行测试](run_tests.py) - 测试运行脚本
- [pytest 配置](pytest.ini) - 测试配置

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

特别感谢：
- Python 社区的强大支持
- Tkinter 提供的 GUI 框架
- 所有贡献者的宝贵建议
- 2026 年重构团队的努力

---

🎮 **开始你的农场之旅吧！** 🎮

有任何问题或建议？欢迎提交 Issue 或联系开发者！
