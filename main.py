"""
游戏主入口文件
农场模拟游戏 - Web API 版（准备中）
"""

import sys
import os

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """主函数入口"""
    print("🌟 欢迎来到农场模拟器！")
    print("=" * 50)
    print("\n💡 提示：Web 版本正在开发中...")
    print("\n当前可用的功能:")
    print("  1. 运行测试：python run_tests.py")
    print("  2. 查看文档：README.md")
    print("\n🚧 Web API 开发计划:")
    print("  - 后端：FastAPI")
    print("  - 前端：React + TypeScript")
    print("  - 部署：Docker")
    print("\n敬请期待！\n")


if __name__ == "__main__":
    main()
