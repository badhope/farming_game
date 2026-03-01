"""
教学对话框模块
显示新手引导的每个具体步骤
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable
from systems.tutorial import TutorialStep


class TutorialDialog:
    """
    教学对话框类
    显示单个教学步骤的内容和操作按钮
    """
    
    def __init__(self, parent, step: TutorialStep, current_step: int, total_steps: int,
                 on_next: Callable, on_previous: Callable, on_skip: Callable):
        """
        初始化教学对话框
        
        Args:
            parent: 父窗口
            step: 教学步骤对象
            current_step: 当前步骤编号
            total_steps: 总步骤数
            on_next: 下一步回调
            on_previous: 上一步回调
            on_skip: 跳过回调
        """
        self.parent = parent
        self.step = step
        self.current_step = current_step
        self.total_steps = total_steps
        self.on_next = on_next
        self.on_previous = on_previous
        self.on_skip = on_skip
        
        self.dialog = None
    
    def show(self):
        """显示对话框"""
        # 创建顶层窗口
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("🎓 新手教程")
        self.dialog.geometry("500x400")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # 居中显示
        self._center_window()
        
        # 创建界面
        self._create_widgets()
        
        # 绑定键盘事件
        self.dialog.bind('<Return>', lambda e: self.on_next())
        self.dialog.bind('<Escape>', lambda e: self.on_skip())
    
    def _center_window(self):
        """将窗口居中显示"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
    
    def _create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text=self.step.title,
            font=('微软雅黑', 14, 'bold'),
            foreground='#2E8B57'
        )
        title_label.pack(pady=(0, 15))
        
        # 进度信息
        progress_text = f"步骤 {self.current_step} / {self.total_steps}"
        progress_label = ttk.Label(
            main_frame,
            text=progress_text,
            font=('微软雅黑', 10),
            foreground='#666666'
        )
        progress_label.pack()
        
        # 分隔线
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        # 内容文本
        content_text = tk.Text(
            main_frame,
            font=('微软雅黑', 11),
            wrap=tk.WORD,
            padx=10,
            pady=10,
            height=12,
            state=tk.DISABLED
        )
        content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 插入内容
        content_text.config(state=tk.NORMAL)
        content_text.insert('1.0', self.step.content)
        content_text.config(state=tk.DISABLED)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # 上一步按钮（如果不是第一步）
        if self.current_step > 1:
            prev_btn = ttk.Button(
                button_frame,
                text="⬅ 上一步",
                command=self.on_previous,
                width=10
            )
            prev_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 跳过按钮
        skip_btn = ttk.Button(
            button_frame,
            text="⏭ 跳过",
            command=self.on_skip,
            width=10
        )
        skip_btn.pack(side=tk.LEFT, padx=5)
        
        # 占位符（用于右对齐）
        ttk.Frame(button_frame).pack(side=tk.LEFT, expand=True)
        
        # 下一步/完成按钮
        if self.current_step < self.total_steps:
            next_text = "下一步 ➡"
        else:
            next_text = "完成教程 🎉"
        
        next_btn = ttk.Button(
            button_frame,
            text=next_text,
            command=self.on_next,
            style='Accent.TButton' if self.current_step == self.total_steps else 'TButton',
            width=12
        )
        next_btn.pack(side=tk.RIGHT)
