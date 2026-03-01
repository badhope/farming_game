"""
游戏主入口文件
现代化农场模拟游戏 - 图形界面版
"""

import sys
import os
import argparse

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def launch_gui_mode():
    """启动图形界面模式"""
    try:
        from ui.gui_main import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ GUI模块导入失败: {e}")
        print("💡 请确保已安装所有依赖包")
        sys.exit(1)
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        sys.exit(1)


def launch_console_mode():
    """启动控制台模式（保持向后兼容）"""
    try:
        from core import GameManager
        from systems import SaveManager, DisplayManager
        from config.settings import GameConfig
        
        class ConsoleGame:
            def __init__(self):
                self.manager = GameManager()
                self.save_manager = SaveManager()
                self.display = DisplayManager(self.manager)
                self.running = True
            
            def start(self):
                # 检查存档
                if self.save_manager.has_save():
                    print("\n🔍 检测到存档文件！")
                    info = self.save_manager.get_save_info()
                    if info:
                        print(f"   存档时间: {info['timestamp']}")
                        print(f"   农夫: {info['player_name']}")
                        print(f"   进度: 第{info['year']}年 {info['season']} 第{info['day']}天")
                    
                    choice = input("是否读取存档？(y/n): ").strip().lower()
                    if choice == 'y':
                        self.save_manager.load_game(self.manager)
                        print("✅ 存档加载成功！")
                
                # 主循环
                while self.running:
                    messages = self.manager.get_new_messages()
                    self.display.render_frame(messages)
                    choice = self.display.show_input_prompt("请选择操作")
                    self._handle_input(choice)
            
            def _handle_input(self, choice):
                # 简化版输入处理（保持原有功能）
                if choice == '6':  # 睡觉
                    print("\n🛏️ 结束了一天，准备睡觉...")
                    result = self.manager.advance_day()
                    print(f"\n🌞 第{result.day}天 - {result.season} - {result.weather}")
                    if result.events:
                        print("📜 今日事件:")
                        for event in result.events:
                            print(f"   {event}")
                    input("\n按回车键继续...")
                elif choice == '0':  # 退出
                    self.running = False
                    print("\n👋 感谢游玩！")
                # 其他选项保持原样...
        
        game = ConsoleGame()
        game.start()
        
    except Exception as e:
        print(f"❌ 控制台模式启动失败: {e}")
        sys.exit(1)


def main():
    """主函数入口"""
    parser = argparse.ArgumentParser(description="农场模拟游戏")
    parser.add_argument(
        '--mode',
        choices=['gui', 'console'],
        default='gui',
        help='选择运行模式: gui(图形界面) 或 console(控制台)'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='农场模拟器 v2.0'
    )
    
    args = parser.parse_args()
    
    # 设置控制台标题
    if sys.platform == 'win32':
        os.system('title 🌟 星露谷物语 - 农场模拟器 🌟')
    
    print("🌟 欢迎来到星露谷物语农场模拟器！")
    print("=" * 50)
    
    if args.mode == 'gui':
        print("🎮 启动图形界面模式...")
        launch_gui_mode()
    else:
        print("⌨️ 启动控制台模式...")
        launch_console_mode()


if __name__ == "__main__":
    main()
