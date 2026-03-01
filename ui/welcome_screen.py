"""
欢迎界面模块
提供游戏启动选项和基本信息展示
"""

import tkinter as tk
from tkinter import ttk, font
import random


class WelcomeScreen(tk.Frame):
    """
    欢迎界面类
    展示游戏标题、选项按钮和基本信息
    """
    
    def __init__(self, parent, on_start_game, on_load_game, on_quit):
        """
        初始化欢迎界面
        
        Args:
            parent: 父容器
            on_start_game: 开始新游戏回调函数
            on_load_game: 加载游戏回调函数
            on_quit: 退出游戏回调函数
        """
        super().__init__(parent)
        self.on_start_game = on_start_game
        self.on_load_game = on_load_game
        self.on_quit = on_quit
        
        self._setup_ui()
        self._animate_title()
    
    def _setup_ui(self):
        """设置界面布局"""
        # 主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # 标题区域
        self._create_title_section(main_frame)
        
        # 游戏介绍
        self._create_intro_section(main_frame)
        
        # 按钮区域
        self._create_button_section(main_frame)
        
        # 底部信息
        self._create_footer_section(main_frame)
    
    def _create_title_section(self, parent):
        """创建标题区域"""
        title_frame = ttk.Frame(parent)
        title_frame.pack(pady=(50, 30))
        
        # 主标题
        self.title_label = ttk.Label(
            title_frame,
            text="🌟 星露谷物语 🌟",
            style='Title.TLabel',
            foreground='#2E8B57'
        )
        self.title_label.pack()
        
        # 副标题
        subtitle_label = ttk.Label(
            title_frame,
            text="Farm Simulator",
            font=('Arial', 12, 'italic'),
            foreground='#666666'
        )
        subtitle_label.pack(pady=(5, 0))
    
    def _create_intro_section(self, parent):
        """创建游戏介绍区域"""
        intro_frame = ttk.LabelFrame(parent, text="游戏介绍", padding=15)
        intro_frame.pack(fill=tk.X, padx=50, pady=(0, 30))
        
        intro_text = (
            "欢迎来到星露谷物语！在这里你可以：\n\n"
            "🌱 种植各种农作物，体验四季变化\n"
            "💰 经营农场，赚取金币升级设施\n"
            "🏆 完成成就，成为传奇农夫\n"
            "🌤️ 应对多变天气，享受田园生活\n\n"
            "准备好开始你的农场之旅了吗？"
        )
        
        intro_label = ttk.Label(
            intro_frame,
            text=intro_text,
            style='Normal.TLabel',
            justify=tk.LEFT
        )
        intro_label.pack()
    
    def _create_button_section(self, parent):
        """创建按钮区域"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        # 开始新游戏按钮
        start_btn = ttk.Button(
            button_frame,
            text="🎮 开始新游戏",
            style='Action.TButton',
            command=self.on_start_game,
            width=20
        )
        start_btn.pack(pady=5)
        
        # 加载游戏按钮
        load_btn = ttk.Button(
            button_frame,
            text="📂 加载游戏",
            style='Menu.TButton',
            command=self.on_load_game,
            width=20
        )
        load_btn.pack(pady=5)
        
        # 退出游戏按钮
        quit_btn = ttk.Button(
            button_frame,
            text="🚪 退出游戏",
            style='Menu.TButton',
            command=self.on_quit,
            width=20
        )
        quit_btn.pack(pady=5)
    
    def _create_footer_section(self, parent):
        """创建底部信息区域"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(side=tk.BOTTOM, pady=20)
        
        # 版本信息
        version_label = ttk.Label(
            footer_frame,
            text="Version 2.0 | Python Farming Game",
            style='Small.TLabel',
            foreground='#888888'
        )
        version_label.pack()
        
        # 随机提示
        tips = [
            "💡 提示：不同的作物适合不同的季节哦！",
            "💡 提示：记得每天给作物浇水！",
            "💡 提示：暴风雨可能会摧毁你的作物！",
            "💡 提示：升级农场可以获得更多土地！",
            "💡 提示：完成成就可以获得特殊奖励！"
        ]
        
        tip_label = ttk.Label(
            footer_frame,
            text=random.choice(tips),
            style='Small.TLabel',
            foreground='#555555'
        )
        tip_label.pack(pady=(5, 0))
    
    def _animate_title(self):
        """标题动画效果"""
        colors = ['#2E8B57', '#3CB371', '#20B2AA', '#3CB371']
        current_color_index = 0
        
        def change_color():
            nonlocal current_color_index
            if self.winfo_exists():  # 检查窗口是否存在
                self.title_label.configure(foreground=colors[current_color_index])
                current_color_index = (current_color_index + 1) % len(colors)
                self.after(1000, change_color)  # 每秒改变一次颜色
        
        change_color()
