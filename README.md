# 🌟 星露谷物语 - 农场模拟器 🌟

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

一款现代化的农场模拟游戏，让你体验田园生活的乐趣！

## 🎮 游戏特色

### 🌈 全新图形界面
- **直观操作**: 鼠标点击替代繁琐的命令行输入
- **实时反馈**: 动态更新的农田状态和作物生长进度
- **美观界面**: 现代化UI设计，色彩丰富的视觉体验

### 🌱 丰富游戏内容
- **四季系统**: 春夏秋冬四个季节，每季有不同的适宜作物
- **天气变化**: 晴天、雨天、暴风雨等多样天气影响 gameplay
- **作物多样性**: 12种不同作物，各有独特的生长特性和收益
- **农场升级**: 从小农场逐步扩建，解锁更多土地

### 🏆 成就系统
- **多样化成就**: 收获、财富、探索等各类成就
- **进度追踪**: 实时显示成就完成进度
- **奖励机制**: 解锁特殊奖励和称号

### 💰 经济系统
- **商店经营**: 购买种子，出售作物
- **投资回报**: 计算作物利润率，制定最优种植策略
- **财务管理**: 追踪收入支出，监控农场盈利状况

### 🎓 新手友好
- **引导教程**: 详细的step-by-step新手指导
- **智能提示**: 根据游戏状态提供操作建议
- **渐进难度**: 从基础操作到高级策略的平滑学习曲线

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

### 成就挑战
- 🌾 **初级农夫**: 收获第一个作物
- 💰 **小有成就**: 累计收入达到10万金币
- 🏅 **农业专家**: 收获1000个作物
- 👑 **农场大亨**: 解锁所有农场等级

## 🛠️ 技术架构

### 项目结构
```
farming_game/
├── ui/                 # 图形界面模块
│   ├── gui_main.py     # 主界面入口
│   ├── welcome_screen.py # 欢迎界面
│   └── game_window.py  # 游戏主窗口
├── controllers/        # 控制器层
│   └── game_controller.py # 游戏逻辑控制器
├── audio/             # 音频系统
│   └── sound_manager.py # 音效管理器
├── systems/           # 系统模块
│   ├── tutorial.py    # 新手引导系统
│   ├── tutorial_dialog.py # 教学对话框
│   └── event_system.py # 游戏事件系统
├── core/              # 核心逻辑
│   ├── game_manager.py # 游戏管理器
│   ├── economy.py     # 经济系统
│   └── time_system.py # 时间系统
├── models/            # 数据模型
│   ├── player.py      # 玩家模型
│   ├── crop.py        # 作物模型
│   └── plot.py        # 地块模型
├── config/            # 配置文件
│   └── settings.py    # 游戏配置
└── main.py           # 程序入口
```

### 核心技术
- **界面框架**: Tkinter (Python内置)
- **数据管理**: 面向对象设计模式
- **事件驱动**: 响应式UI更新机制
- **模块化架构**: 松耦合，易扩展

## 🎨 界面预览

### 主游戏界面
- 左侧: 农田网格显示 + 玩家状态
- 右侧: 操作菜单 + 信息面板
- 底部: 实时消息日志

### 视觉设计
- 🟩 **绿色**: 成熟作物
- 🟨 **黄色**: 生长期作物  
- ⬜ **白色**: 空闲土地
- 💧 **蓝色边框**: 已浇水状态

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

### v2.0 (当前版本)
- ✨ 全新图形界面
- 🎓 新手引导系统
- 🎵 音效系统
- 🎪 随机事件系统
- 📊 增强的统计功能

### v1.0
- 📝 基础控制台版本
- 🌱 简单种植系统
- 💰 基础经济系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

特别感谢以下开源项目和技术：
- Python 社区的强大支持
- Tkinter 提供的GUI框架
- 所有贡献者的宝贵建议和代码贡献

---

🎮 **开始你的农场之旅吧！** 🎮

有任何问题或建议？欢迎提交 Issue 或联系开发者！
