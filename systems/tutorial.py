"""
新手引导系统模块
提供逐步的教学引导，帮助新玩家熟悉游戏
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable, Optional
import json
import os


class TutorialStep:
    """
    教学步骤类
    定义单个教学步骤的信息
    """
    
    def __init__(self, title: str, content: str, target_widget: Optional[str] = None):
        """
        初始化教学步骤
        
        Args:
            title: 步骤标题
            content: 步骤内容
            target_widget: 目标控件标识符
        """
        self.title = title
        self.content = content
        self.target_widget = target_widget
        self.completed = False


class TutorialManager:
    """
    新手引导管理器
    管理整个教学流程
    """
    
    def __init__(self, parent_window):
        """
        初始化引导管理器
        
        Args:
            parent_window: 父窗口引用
        """
        self.parent = parent_window
        self.steps: List[TutorialStep] = []
        self.current_step_index = 0
        self.is_active = False
        self.callback_on_complete: Optional[Callable] = None
        
        self._load_tutorial_steps()
    
    def _load_tutorial_steps(self):
        """加载教学步骤"""
        tutorial_data = [
            {
                "title": "🌱 欢迎来到农场世界！",
                "content": "你好！我是你的农业助手。\n\n让我们一起学习如何经营这个美丽的农场吧！\n\n点击【下一步】开始我们的冒险之旅！"
            },
            {
                "title": "📅 时间与季节",
                "content": "在农场里，时间和季节非常重要：\n\n• 每个季节有不同的适宜作物\n• 天气会影响作物生长\n• 记得每天都要照顾你的作物\n\n现在看看顶部的时间和天气信息吧！",
                "target_widget": "info_bar"
            },
            {
                "title": "🌾 农田操作",
                "content": "这是你的农田区域：\n\n• 白色方块表示空地\n• 点击空地可以种植作物\n• 绿色方块表示成熟作物\n• 点击成熟作物可以直接收获\n\n试着点击一块空地看看！",
                "target_widget": "farm_grid"
            },
            {
                "title": "🛒 购买种子",
                "content": "要开始种植，首先需要购买种子：\n\n1. 切换到右侧的【商店】选项卡\n2. 选择你想种植的作物\n3. 输入购买数量\n4. 点击【购买选中种子】\n\n不同的作物适合不同的季节哦！",
                "target_widget": "shop_tab"
            },
            {
                "title": "🌱 种植作物",
                "content": "现在你有了种子，让我们开始种植：\n\n1. 点击农田中的空地\n2. 选择你要种植的作物\n3. 确认种植\n\n记得选择适合当前季节的作物！",
                "target_widget": "farm_grid"
            },
            {
                "title": "💧 日常护理",
                "content": "作物需要日常护理才能健康成长：\n\n• 晴天时需要浇水（雨天会自动浇水）\n• 可以点击【全部浇水】快速完成\n• 也可以单独点击地块浇水\n\n试试给你的作物浇水吧！",
                "target_widget": "quick_actions"
            },
            {
                "title": "🏆 成就系统",
                "content": "完成特定目标可以获得成就奖励：\n\n• 切换到【成就】选项卡查看进度\n• 完成成就可以获得特殊奖励\n• 收集所有成就成为传奇农夫！\n\n看看你现在有什么成就吧！",
                "target_widget": "achievements_tab"
            },
            {
                "title": "📊 统计信息",
                "content": "随时关注你的农场发展：\n\n• 【统计】选项卡显示详细数据\n• 了解你的收入、支出和生产情况\n• 监控农场的成长轨迹\n\n这里有很多有用的信息！",
                "target_widget": "stats_tab"
            },
            {
                "title": "🌅 推进时间",
                "content": "当一天结束时：\n\n• 点击右下角的睡眠按钮\n• 或使用快捷键推进到第二天\n• 作物会在夜间继续生长\n• 注意天气预报做好准备\n\n现在你可以结束这一天了！",
                "target_widget": "day_advance"
            },
            {
                "title": "🎉 恭喜完成教程！",
                "content": "太棒了！你已经掌握了基本的农场经营技巧！\n\n记住这些要点：\n✓ 根据季节选择作物\n✓ 每天浇水和收获\n✓ 关注天气变化\n✓ 完成成就目标\n✓ 逐步升级农场\n\n祝你在农场生活中一切顺利！"
            }
        ]
        
        self.steps = [
            TutorialStep(step["title"], step["content"], step.get("target_widget"))
            for step in tutorial_data
        ]
    
    def start_tutorial(self, on_complete: Optional[Callable] = None):
        """
        开始新手引导
        
        Args:
            on_complete: 完成后的回调函数
        """
        self.callback_on_complete = on_complete
        self.current_step_index = 0
        self.is_active = True
        self._show_current_step()
    
    def next_step(self):
        """进入下一步"""
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            self._show_current_step()
        else:
            self.complete_tutorial()
    
    def previous_step(self):
        """返回上一步"""
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self._show_current_step()
    
    def skip_tutorial(self):
        """跳过教程"""
        result = messagebox.askyesno(
            "跳过教程",
            "确定要跳过新手教程吗？\n\n你可以在设置中重新开启教程。"
        )
        
        if result:
            self.complete_tutorial()
    
    def complete_tutorial(self):
        """完成教程"""
        self.is_active = False
        if self.callback_on_complete:
            self.callback_on_complete()
        
        # 显示完成提示
        messagebox.showinfo(
            "教程完成",
            "🎉 恭喜完成新手教程！\n\n现在你可以自由探索农场世界了！\n如果有任何疑问，随时可以查看帮助文档。"
        )
    
    def _show_current_step(self):
        """显示当前步骤"""
        if not self.is_active or self.current_step_index >= len(self.steps):
            return
        
        step = self.steps[self.current_step_index]
        
        # 创建教学对话框
        dialog = TutorialDialog(
            self.parent,
            step,
            self.current_step_index + 1,
            len(self.steps),
            self.next_step,
            self.previous_step,
            self.skip_tutorial
        )
        dialog.show()
