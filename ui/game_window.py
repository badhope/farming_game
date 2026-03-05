"""
游戏主窗口模块
包含农场可视化界面和所有游戏操作功能
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
from datetime import datetime


class GameWindow(tk.Frame):
    """
    游戏主窗口类
    提供完整的农场游戏界面
    """
    
    def __init__(self, parent, game_manager, save_manager, on_return_to_menu, on_exit_game):
        """
        初始化游戏窗口
        
        Args:
            parent: 父容器
            game_manager: 游戏管理器实例
            save_manager: 存档管理器实例
            on_return_to_menu: 返回主菜单回调
            on_exit_game: 退出游戏回调
        """
        super().__init__(parent)
        self.game_manager = game_manager
        self.save_manager = save_manager
        self.on_return_to_menu = on_return_to_menu
        self.on_exit_game = on_exit_game
        
        # UI组件引用
        self.plot_buttons = {}  # 地块按钮字典
        self.status_labels = {}  # 状态标签字典
        
        self._setup_ui()
        self._update_display()
        
        # 启动定时更新
        self._start_auto_update()
    
    def _setup_ui(self):
        """设置主界面布局"""
        # 创建样式
        self._create_styles()
        
        # 创建主框架
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板 - 农田和基本信息
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=2)
        
        # 右侧面板 - 操作菜单和信息
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # 设置左右面板内容
        self._setup_left_panel(left_frame)
        self._setup_right_panel(right_frame)
    
    def _create_styles(self):
        """创建自定义样式"""
        style = ttk.Style()
        
        # 种子按钮样式
        style.configure('SeedButton.TButton',
                      font=('微软雅黑', 10, 'bold'),
                      padding=10,
                      relief='raised',
                      borderwidth=2)
        
        # 选中的种子按钮样式
        style.configure('SelectedSeedButton.TButton',
                      font=('微软雅黑', 10, 'bold'),
                      padding=10,
                      relief='sunken',
                      borderwidth=2,
                      background='#4CAF50',
                      foreground='white')
        
        # 禁用的种子按钮样式
        style.configure('DisabledSeedButton.TButton',
                      font=('微软雅黑', 10),
                      padding=10,
                      relief='flat',
                      borderwidth=1,
                      background='#E0E0E0',
                      foreground='#9E9E9E')
    
    def _setup_left_panel(self, parent):
        """设置左侧面板"""
        # 顶部信息栏
        self._create_info_bar(parent)
        
        # 农田显示区域
        self._create_farm_area(parent)
        
        # 玩家状态栏
        self._create_player_status(parent)
    
    def _setup_right_panel(self, parent):
        """设置右侧面板"""
        # 快捷操作区
        self._create_quick_actions(parent)
        
        # 详细菜单区
        self._create_detailed_menus(parent)
        
        # 消息日志区
        self._create_message_log(parent)
    
    def _create_info_bar(self, parent):
        """创建顶部信息栏"""
        info_frame = ttk.LabelFrame(parent, text="📅 当前状态", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 日期信息
        date_frame = ttk.Frame(info_frame)
        date_frame.pack(fill=tk.X)
        
        self.date_label = ttk.Label(date_frame, text="", style='Header.TLabel')
        self.date_label.pack(side=tk.LEFT)
        
        # 天气信息
        self.weather_label = ttk.Label(date_frame, text="", style='Normal.TLabel')
        self.weather_label.pack(side=tk.RIGHT)
    
    def _create_farm_area(self, parent):
        """创建农田显示区域"""
        farm_frame = ttk.LabelFrame(parent, text="🏠 我的农场", padding=10)
        farm_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 农田网格
        grid_frame = ttk.Frame(farm_frame)
        grid_frame.pack(expand=True)
        
        size = self.game_manager.get_plot_size()
        
        # 创建地块按钮网格
        for row in range(size):
            for col in range(size):
                btn = tk.Button(
                    grid_frame,
                    width=8,
                    height=4,
                    font=('微软雅黑', 12),
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda r=row, c=col: self._on_plot_click(r, c)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.plot_buttons[(row, col)] = btn
    
    def _create_player_status(self, parent):
        """创建玩家状态栏"""
        status_frame = ttk.LabelFrame(parent, text="👤 农民信息", padding=10)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 金币信息
        money_frame = ttk.Frame(status_frame)
        money_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(money_frame, text="💰 金币:", style='Normal.TLabel').pack(side=tk.LEFT)
        self.money_label = ttk.Label(money_frame, text="", style='Header.TLabel', foreground='gold')
        self.money_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 种子库存
        seeds_frame = ttk.Frame(status_frame)
        seeds_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(seeds_frame, text="🌱 种子:", style='Normal.TLabel').pack(side=tk.LEFT)
        self.seeds_label = ttk.Label(seeds_frame, text="", style='Normal.TLabel')
        self.seeds_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 仓库信息
        inventory_frame = ttk.Frame(status_frame)
        inventory_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(inventory_frame, text="📦 仓库:", style='Normal.TLabel').pack(side=tk.LEFT)
        self.inventory_label = ttk.Label(inventory_frame, text="", style='Normal.TLabel')
        self.inventory_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def _create_quick_actions(self, parent):
        """创建快捷操作区"""
        quick_frame = ttk.LabelFrame(parent, text="⚡ 快捷操作", padding=10)
        quick_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 第一行按钮
        button_frame1 = ttk.Frame(quick_frame)
        button_frame1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(
            button_frame1,
            text="💧 全部浇水",
            command=self._water_all_plots
        ).pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        ttk.Button(
            button_frame1,
            text="🌾 全部收获",
            command=self._harvest_all_mature
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 第二行按钮
        button_frame2 = ttk.Frame(quick_frame)
        button_frame2.pack(fill=tk.X)
        
        # 自动运行开关
        auto_run_frame = ttk.Frame(button_frame2)
        auto_run_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(auto_run_frame, text="自动运行:").pack(side=tk.LEFT, padx=(0, 5))
        self.auto_run_var = tk.BooleanVar(value=self.game_manager.auto_run)
        ttk.Checkbutton(
            auto_run_frame,
            variable=self.auto_run_var,
            command=self._toggle_auto_run
        ).pack(side=tk.LEFT)
        
        # 手动推进按钮
        ttk.Button(
            button_frame2,
            text="⏭️ 推进一天",
            command=self._advance_day
        ).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # 第三行按钮 - 返回和退出
        button_frame3 = ttk.Frame(quick_frame)
        button_frame3.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(
            button_frame3,
            text="🏠 返回主菜单",
            command=self._return_to_menu
        ).pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        ttk.Button(
            button_frame3,
            text="🚪 退出游戏",
            command=self._exit_game
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _create_detailed_menus(self, parent):
        """创建详细菜单区"""
        menu_frame = ttk.LabelFrame(parent, text="📋 游戏菜单", padding=10)
        menu_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建选项卡
        notebook = ttk.Notebook(menu_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 商店选项卡
        self._create_shop_tab(notebook)
        
        # 成就选项卡
        self._create_achievements_tab(notebook)
        
        # 统计选项卡
        self._create_stats_tab(notebook)
    
    def _create_shop_tab(self, parent):
        """创建商店选项卡"""
        shop_frame = ttk.Frame(parent)
        parent.add(shop_frame, text="🛒 商店")
        
        # 作物按钮网格
        buttons_frame = ttk.Frame(shop_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建滚动条
        canvas = tk.Canvas(buttons_frame)
        scrollbar = ttk.Scrollbar(buttons_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 存储种子按钮
        self.seed_buttons = {}
        self.selected_seed = None
        
        # 购买按钮
        ttk.Button(
            shop_frame,
            text="💰 购买选中种子",
            command=self._buy_selected_seed
        ).pack(fill=tk.X)
        
        # 数量输入
        qty_frame = ttk.Frame(shop_frame)
        qty_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(qty_frame, text="数量:").pack(side=tk.LEFT)
        self.quantity_var = tk.StringVar(value="1")
        ttk.Entry(qty_frame, textvariable=self.quantity_var, width=10).pack(side=tk.LEFT, padx=(5, 0))
        
        # 文本输入字段
        input_frame = ttk.Frame(shop_frame)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(input_frame, text="快速选择:").pack(side=tk.LEFT)
        self.seed_input_var = tk.StringVar()
        seed_input = ttk.Entry(input_frame, textvariable=self.seed_input_var, width=20)
        seed_input.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        seed_input.insert(0, "输入种子名称或编号")
        seed_input.bind("<FocusIn>", lambda e: seed_input.delete(0, tk.END))
        seed_input.bind("<Return>", self._on_seed_input_submit)
        
        # 输入验证按钮
        ttk.Button(
            input_frame,
            text="确认",
            command=self._on_seed_input_submit
        ).pack(side=tk.LEFT, padx=(5, 0))
    
    def _create_achievements_tab(self, parent):
        """创建成就选项卡"""
        ach_frame = ttk.Frame(parent)
        parent.add(ach_frame, text="🏆 成就")
        
        # 成就列表
        self.ach_listbox = tk.Listbox(ach_frame, font=('微软雅黑', 9))
        self.ach_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 刷新按钮
        ttk.Button(
            ach_frame,
            text="🔄 刷新成就",
            command=self._update_achievements_display
        ).pack(fill=tk.X)
    
    def _create_stats_tab(self, parent):
        """创建统计选项卡"""
        stats_frame = ttk.Frame(parent)
        parent.add(stats_frame, text="📊 统计")
        
        # 统计信息文本框
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            font=('微软雅黑', 9),
            height=15,
            state=tk.DISABLED
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_message_log(self, parent):
        """创建消息日志区"""
        log_frame = ttk.LabelFrame(parent, text="📜 消息日志", padding=5)
        log_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('微软雅黑', 8),
            height=6,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def _on_plot_click(self, row, col):
        """处理地块点击事件"""
        plot = self.game_manager.get_plot(row, col)
        
        if plot.is_empty():
            # 空地块 - 弹出种植菜单
            self._show_plant_dialog(row, col)
        elif plot.is_mature():
            # 成熟作物 - 直接收获
            self._harvest_plot(row, col)
        else:
            # 生长中的作物 - 显示状态
            progress = int(plot.get_growth_progress() * 100)
            self._add_message(f"🌱 {plot.crop.name} 生长进度: {progress}%")
    
    def _show_plant_dialog(self, row, col):
        """显示种植对话框"""
        dialog = tk.Toplevel(self)
        dialog.title("🌱 选择要种植的作物")
        dialog.geometry("300x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # 可种植作物列表
        available_crops = []
        player_seeds = self.game_manager.player.seeds
        current_season = self.game_manager.get_current_season()
        
        for crop_name, seed_count in player_seeds.items():
            if seed_count > 0:
                crop = self.game_manager.economy_system.get_crop(crop_name)
                if crop and crop.can_plant_in_season(current_season):
                    available_crops.append((crop_name, crop, seed_count))
        
        if not available_crops:
            messagebox.showinfo("提示", "你没有可以在这个季节种植的种子！")
            dialog.destroy()
            return
        
        # 创建作物按钮
        for crop_name, crop, seed_count in available_crops:
            btn_text = f"{crop.emoji} {crop_name} (剩余:{seed_count})"
            btn = ttk.Button(
                dialog,
                text=btn_text,
                command=lambda n=crop_name: self._plant_crop_and_close(n, row, col, dialog)
            )
            btn.pack(fill=tk.X, padx=10, pady=2)
        
        # 取消按钮
        ttk.Button(
            dialog,
            text="❌ 取消",
            command=dialog.destroy
        ).pack(fill=tk.X, padx=10, pady=(10, 0))
    
    def _plant_crop_and_close(self, crop_name, row, col, dialog):
        """种植作物并关闭对话框"""
        success, msg = self.game_manager.plant_crop(row, col, crop_name)
        self._add_message(msg)
        if success:
            self._update_display()
        dialog.destroy()
    
    def _water_all_plots(self):
        """给所有作物浇水"""
        if self.game_manager.time_system.is_rainy():
            self._add_message("🌧️ 今天下雨，作物自动获得水分！")
            return
        
        success_count, _ = self.game_manager.water_all_plots()
        if success_count > 0:
            self._add_message(f"💧 成功给 {success_count} 块地浇水！")
            self._update_display()
        else:
            self._add_message("💧 没有需要浇水的作物。")
    
    def _harvest_plot(self, row, col):
        """收获指定地块"""
        success, msg = self.game_manager.harvest_plot(row, col)
        self._add_message(msg)
        if success:
            self._update_display()
    
    def _harvest_all_mature(self):
        """收获所有成熟作物"""
        count, messages = self.game_manager.harvest_all_mature()
        if count > 0:
            self._add_message(f"🎉 收获了 {count} 个作物！")
            for msg in messages:
                self._add_message(msg)
            self._update_display()
        else:
            self._add_message("🍂 没有成熟的作物可以收获。")
    
    def _buy_selected_seed(self):
        """购买选中的种子"""
        if not self.selected_seed:
            messagebox.showwarning("警告", "请先选择要购买的种子！")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的购买数量！")
            return
        
        crop_name = self.selected_seed
        
        success, msg = self.game_manager.buy_seeds(crop_name, quantity)
        self._add_message(msg)
        if success:
            self._update_display()
        else:
            # 购买失败时，显示详细的错误信息
            messagebox.showinfo("购买失败", msg)
    
    def _advance_day(self):
        """推进到下一天"""
        result = self.game_manager.advance_day()
        
        # 显示结果
        self._add_message("=" * 50)
        self._add_message(f"🌞 第{result.day}天 - {result.season} - {result.weather}")
        self._add_message("=" * 50)
        
        if result.events:
            self._add_message("📜 今日事件:")
            for event in result.events:
                self._add_message(f"   {event}")
        
        if result.crops_matured > 0:
            self._add_message(f"🌿 有 {result.crops_matured} 个作物成熟了！")
        
        if result.crops_died > 0 or result.crops_destroyed > 0:
            self._add_message(f"💀 损失了 {result.crops_died + result.crops_destroyed} 个作物。")
        
        self._add_message("=" * 50)
        
        self._update_display()
    
    def _update_display(self):
        """更新所有显示内容"""
        # 更新日期和天气
        self.date_label.config(text=self.game_manager.get_current_date())
        self.weather_label.config(text=f"🌤️ {self.game_manager.get_current_weather().value}")
        
        # 更新玩家状态
        player = self.game_manager.player
        self.money_label.config(text=f"{player.money} 金")
        
        # 更新种子信息
        seeds_info = " | ".join([f"{name}:{count}" for name, count in player.seeds.items()][:3])
        if len(player.seeds) > 3:
            seeds_info += " ..."
        self.seeds_label.config(text=seeds_info if seeds_info else "无")
        
        # 更新仓库信息
        inv_info = " | ".join([f"{name}:{count}" for name, count in player.inventory.items()][:3])
        if len(player.inventory) > 3:
            inv_info += " ..."
        self.inventory_label.config(text=inv_info if inv_info else "空")
        
        # 更新农田显示
        self._update_farm_display()
        
        # 更新商店显示
        self._update_shop_display()
        
        # 更新成就显示
        self._update_achievements_display()
        
        # 更新统计信息
        self._update_stats_display()
        
        # 显示新消息
        messages = self.game_manager.get_new_messages()
        for msg in messages:
            self._add_message(msg)
    
    def _update_farm_display(self):
        """更新农田显示"""
        size = self.game_manager.get_plot_size()
        for row in range(size):
            for col in range(size):
                plot = self.game_manager.get_plot(row, col)
                btn = self.plot_buttons[(row, col)]
                
                if plot.is_empty():
                    btn.config(text="⬜\n空地", bg="#F0F0F0", fg="black")
                else:
                    crop = plot.crop
                    if plot.is_mature():
                        btn.config(text=f"{crop.emoji}✨\n{crop.name}", bg="#90EE90", fg="black")
                    else:
                        # 根据生长阶段显示不同颜色
                        stages = ["🌱", "🌿", "🪴", crop.emoji]
                        stage_text = stages[min(plot.growth_stage, 3)]
                        colors = ["#FFB6C1", "#98FB98", "#32CD32", "#228B22"]
                        color = colors[min(plot.growth_stage, 3)]
                        btn.config(text=f"{stage_text}\n{crop.name}", bg=color, fg="white")
                    
                    # 显示浇水状态
                    if plot.watered_today:
                        btn.config(relief=tk.SUNKEN)
                    else:
                        btn.config(relief=tk.RAISED)
    
    def _update_shop_display(self):
        """更新商店显示"""
        # 清空现有按钮
        for button in self.seed_buttons.values():
            button.destroy()
        self.seed_buttons.clear()
        
        # 获取作物列表
        crops = self.game_manager.economy_system.get_all_crops()
        current_season = self.game_manager.get_current_season()
        
        # 创建种子按钮网格
        row = 0
        col = 0
        max_cols = 2
        
        for i, crop in enumerate(crops):
            can_plant = crop.can_plant_in_season(current_season)
            status = "✅" if can_plant else "❌"
            
            # 创建按钮
            btn_text = f"{crop.emoji} {crop.name}\n{crop.seed_price}金/个\n{status}"
            btn = ttk.Button(
                self.scrollable_frame,
                text=btn_text,
                style='SeedButton.TButton' if can_plant else 'DisabledSeedButton.TButton',
                command=lambda c=crop: self._select_seed(c)
            )
            
            # 放置按钮
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            # 存储按钮
            self.seed_buttons[crop.name] = btn
            
            # 更新行列
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # 确保滚动区域更新
        if hasattr(self, 'scrollable_frame'):
            self.scrollable_frame.update_idletasks()
    
    def _select_seed(self, crop):
        """选择种子"""
        # 取消之前的选择
        if self.selected_seed and self.selected_seed in self.seed_buttons:
            self.seed_buttons[self.selected_seed].configure(style='SeedButton.TButton')
        
        # 设置新选择
        self.selected_seed = crop.name
        if crop.name in self.seed_buttons:
            self.seed_buttons[crop.name].configure(style='SelectedSeedButton.TButton')
        
        # 更新输入字段
        self.seed_input_var.set(crop.name)
        self._add_message(f"🌱 已选择: {crop.emoji} {crop.name}")
    
    def _on_seed_input_submit(self, event=None):
        """处理种子输入提交"""
        input_text = self.seed_input_var.get().strip()
        if not input_text:
            messagebox.showwarning("警告", "请输入种子名称或编号！")
            return
        
        # 验证输入
        if not self._validate_seed_input(input_text):
            messagebox.showwarning("警告", "输入格式不正确！请输入有效的种子名称或编号。")
            return
        
        # 查找种子
        crops = self.game_manager.economy_system.get_all_crops()
        found = False
        
        # 尝试按名称匹配
        for crop in crops:
            if input_text.lower() == crop.name.lower():
                self._select_seed(crop)
                found = True
                break
        
        # 尝试按编号匹配
        if not found:
            try:
                index = int(input_text) - 1
                if 0 <= index < len(crops):
                    self._select_seed(crops[index])
                    found = True
            except ValueError:
                pass
        
        if not found:
            messagebox.showwarning("警告", f"未找到种子: {input_text}")
    
    def _validate_seed_input(self, input_text):
        """验证种子输入"""
        # 允许字母、数字和空格
        return all(c.isalnum() or c.isspace() for c in input_text)
    
    def _update_achievements_display(self):
        """更新成就显示"""
        self.ach_listbox.delete(0, tk.END)
        ach_manager = self.game_manager.achievement_manager
        
        unlocked = ach_manager.get_unlocked_count()
        total = ach_manager.get_total_count()
        self.ach_listbox.insert(tk.END, f"🏆 完成度: {unlocked}/{total}")
        self.ach_listbox.insert(tk.END, "-" * 30)
        
        for ach in ach_manager.get_all_achievements():
            if ach.unlocked:
                self.ach_listbox.insert(tk.END, f"✅ {ach.name}")
            else:
                progress = ach.get_progress_percentage()
                self.ach_listbox.insert(tk.END, f"⬜ {ach.name} ({progress}%)")
    
    def _update_stats_display(self):
        """更新统计信息显示"""
        stats = self.game_manager.player.stats
        summary = self.game_manager.get_game_summary()
        
        stats_text = f"""📊 游戏统计信息

📅 游戏进度:
   游戏天数: {stats.days_played} 天
   当前年份: 第{summary['year']}年
   当前季节: {summary['season']}

💰 经济状况:
   当前金币: {summary['money']} 金
   累计收入: {stats.total_earnings} 金
   累计支出: {stats.total_spent} 金
   净利润: {stats.total_earnings - stats.total_spent} 金

🌱 农业生产:
   总收获数: {stats.total_harvested} 个
   种植种类: {stats.get_crops_grown_count()} 种
   单日最多: {stats.single_day_harvest} 个
   最高持有: {stats.max_money_held} 金

🏘️ 农场发展:
   农场等级: Lv.{summary['upgrade_level']}
   农田大小: {summary['plot_size']}x{summary['plot_size']}
   
🏆 成就进度:
   已解锁: {summary['achievements']}/{summary['total_achievements']}
"""
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state=tk.DISABLED)
    
    def _add_message(self, message):
        """添加消息到日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted_msg)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _start_auto_update(self):
        """启动自动更新"""
        import time
        
        def auto_update():
            if self.winfo_exists():
                # 检查自动推进时间
                current_time = time.time()
                day_result = self.game_manager.check_auto_advance(current_time)
                
                # 处理自动推进结果
                if day_result:
                    # 显示结果
                    self._add_message("=" * 50)
                    self._add_message(f"🌞 第{day_result.day}天 - {day_result.season} - {day_result.weather}")
                    self._add_message("=" * 50)
                    
                    if day_result.events:
                        self._add_message("📜 今日事件:")
                        for event in day_result.events:
                            self._add_message(f"   {event}")
                    
                    if day_result.crops_matured > 0:
                        self._add_message(f"🌿 有 {day_result.crops_matured} 个作物成熟了！")
                    
                    if day_result.crops_died > 0 or day_result.crops_destroyed > 0:
                        self._add_message(f"💀 损失了 {day_result.crops_died + day_result.crops_destroyed} 个作物。")
                    
                    self._add_message("=" * 50)
                
                self._update_display()
                self.after(1000, auto_update)  # 每秒更新一次
        
        auto_update()
        
        # 绑定窗口大小变化事件
        self.bind('<Configure>', self._on_resize)
    
    def _on_resize(self, event):
        """处理窗口大小变化事件"""
        # 当窗口大小变化时，更新农田显示
        if hasattr(self, 'plot_buttons') and self.plot_buttons:
            self._update_farm_display()
    
    def _toggle_auto_run(self):
        """切换自动运行状态"""
        self.game_manager.auto_run = self.auto_run_var.get()
        status = "开启" if self.game_manager.auto_run else "关闭"
        self._add_message(f"⚙️ 自动运行已{status}")
    
    def _return_to_menu(self):
        """返回主菜单"""
        result = messagebox.askyesno(
            "返回主菜单",
            "确定要返回主菜单吗？\n\n请确保已保存游戏进度！"
        )
        
        if result:
            self.on_return_to_menu()
    
    def _exit_game(self):
        """退出游戏"""
        result = messagebox.askyesnocancel(
            "退出游戏",
            "确定要退出游戏吗？\n\n是否保存游戏进度？"
        )
        
        if result is True:
            self._save_game()
            self.on_exit_game()
        elif result is False:
            self.on_exit_game()
    
    def _save_game(self):
        """保存游戏"""
        self.save_manager.save_game(self.game_manager)
        self._add_message("💾 游戏已保存！")
