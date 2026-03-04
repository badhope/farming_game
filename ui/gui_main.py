"""
现代化图形界面主文件
使用 tkinter 构建可视化农场游戏界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import os
import sys
from datetime import datetime

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game_manager import GameManager
from systems.save_manager import SaveManager
from ui.game_window import GameWindow
from ui.welcome_screen import WelcomeScreen


class FarmingGameGUI:
    """
    农场游戏图形界面主类
    管理整个游戏的GUI生命周期
    """
    
    def __init__(self):
        """初始化GUI应用"""
        self.root = tk.Tk()
        self.game_manager = None
        self.save_manager = SaveManager()
        self.current_window = None
        
        # 设置窗口属性
        self._setup_window()
        
        # 显示欢迎界面
        self._show_welcome_screen()
    
    def _setup_window(self):
        """设置主窗口属性"""
        self.root.title("🌟 星露谷物语 - 农场模拟器 🌟")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 设置窗口图标（如果有的话）
        try:
            # self.root.iconbitmap("assets/icon.ico")
            pass
        except:
            pass
        
        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # 设置样式
        self._setup_styles()
    
    def _setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        
        # 配置主题
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('Title.TLabel', font=('微软雅黑', 16, 'bold'), foreground='#4CAF50')
        style.configure('Header.TLabel', font=('微软雅黑', 12, 'bold'), foreground='#2E7D32')
        style.configure('Normal.TLabel', font=('微软雅黑', 10), foreground='#333333')
        style.configure('Small.TLabel', font=('微软雅黑', 9), foreground='#666666')
        
        # 按钮样式
        style.configure('Action.TButton', font=('微软雅黑', 10, 'bold'), background='#4CAF50', foreground='white')
        style.configure('Action.TButton:hover', background='#45a049')
        style.configure('Menu.TButton', font=('微软雅黑', 11), background='#f0f0f0', foreground='#333333')
        style.configure('Menu.TButton:hover', background='#e0e0e0')
        
        # 种子按钮样式
        style.configure('SeedButton.TButton',
                      font=('微软雅黑', 10, 'bold'),
                      padding=10,
                      relief='raised',
                      borderwidth=2,
                      background='#E8F5E8',
                      foreground='#2E7D32')
        
        style.configure('SelectedSeedButton.TButton',
                      font=('微软雅黑', 10, 'bold'),
                      padding=10,
                      relief='sunken',
                      borderwidth=2,
                      background='#4CAF50',
                      foreground='white')
        
        style.configure('DisabledSeedButton.TButton',
                      font=('微软雅黑', 10),
                      padding=10,
                      relief='flat',
                      borderwidth=1,
                      background='#E0E0E0',
                      foreground='#9E9E9E')
        
        # 框架样式
        style.configure('TLabelFrame', borderwidth=2, relief='groove', foreground='#2E7D32', background='#F8FFF8')
        style.configure('TLabelFrame.Label', font=('微软雅黑', 11, 'bold'), foreground='#2E7D32')
        
        # 滚动条样式
        style.configure('TScrollbar', background='#f0f0f0', troughcolor='#e0e0e0')
        
        # 输入框样式
        style.configure('TEntry', font=('微软雅黑', 10), padding=5)
        
        # 文本框样式
        style.configure('TText', font=('微软雅黑', 10))
    
    def _show_welcome_screen(self):
        """显示欢迎界面"""
        if self.current_window:
            self.current_window.destroy()
        
        self.current_window = WelcomeScreen(
            parent=self.root,
            on_start_game=self._start_new_game,
            on_load_game=self._load_existing_game,
            on_quit=self._quit_game
        )
        self.current_window.pack(fill=tk.BOTH, expand=True)
    
    def _start_new_game(self):
        """开始新游戏"""
        try:
            # 初始化游戏管理器
            self.game_manager = GameManager()
            
            # 切换到游戏主界面
            self._switch_to_game_window()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动游戏失败: {str(e)}")
    
    def _load_existing_game(self):
        """加载已有存档"""
        try:
            if not self.save_manager.has_save():
                messagebox.showinfo("提示", "没有找到存档文件！")
                return
            
            # 显示存档信息
            save_info = self.save_manager.get_save_info()
            if save_info:
                result = messagebox.askyesno(
                    "加载存档",
                    f"检测到存档:\n\n"
                    f"农夫: {save_info['player_name']}\n"
                    f"进度: 第{save_info['year']}年 {save_info['season']} 第{save_info['day']}天\n"
                    f"金币: {save_info['money']}\n\n"
                    f"是否加载此存档？"
                )
                
                if result:
                    self.game_manager = GameManager()
                    if self.save_manager.load_game(self.game_manager):
                        self._switch_to_game_window()
                        messagebox.showinfo("成功", "存档加载成功！")
                    else:
                        messagebox.showerror("错误", "存档加载失败！")
            else:
                messagebox.showerror("错误", "无法读取存档信息！")
                
        except Exception as e:
            messagebox.showerror("错误", f"加载存档失败: {str(e)}")
    
    def _switch_to_game_window(self):
        """切换到游戏主窗口"""
        if self.current_window:
            self.current_window.destroy()
        
        self.current_window = GameWindow(
            parent=self.root,
            game_manager=self.game_manager,
            save_manager=self.save_manager,
            on_return_to_menu=self._show_welcome_screen,
            on_exit_game=self._quit_game
        )
        self.current_window.pack(fill=tk.BOTH, expand=True)
    
    def _quit_game(self):
        """退出游戏"""
        if self.game_manager and self.game_manager.is_running:
            # 询问是否保存
            result = messagebox.askyesnocancel(
                "退出游戏",
                "是否保存游戏进度后再退出？"
            )
            
            if result is True:  # 是
                self.save_manager.save_game(self.game_manager)
                self.root.quit()
            elif result is False:  # 否
                self.root.quit()
            # 如果是None（取消），则不执行任何操作
        else:
            self.root.quit()
    
    def _on_closing(self):
        """窗口关闭事件处理"""
        self._quit_game()
    
    def run(self):
        """运行GUI应用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._quit_game()
        except Exception as e:
            messagebox.showerror("严重错误", f"程序异常退出: {str(e)}")


def main():
    """主函数入口"""
    app = FarmingGameGUI()
    app.run()


if __name__ == "__main__":
    main()