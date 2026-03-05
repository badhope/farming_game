"""
增强版游戏窗口模块
包含剧情居中显示、弹出式剧情卡片、多标签功能面板
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional, Callable
from datetime import datetime


class StoryCardDialog(tk.Toplevel):
    
    def __init__(self, parent, story_node, on_choice: Callable, on_continue: Callable, on_skip: Callable):
        super().__init__(parent)
        
        self.story_node = story_node
        self.on_choice = on_choice
        self.on_continue = on_continue
        self.on_skip = on_skip
        
        self.title("📜 剧情")
        self.geometry("600x450")
        self.configure(bg="#FFF8E1")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self._setup_ui()
        
        self.center_on_parent(parent)
    
    def center_on_parent(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def _setup_ui(self):
        header_frame = tk.Frame(self, bg="#4CAF50", padx=15, pady=10)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text=self.story_node.title,
            font=("微软雅黑", 16, "bold"),
            fg="white",
            bg="#4CAF50"
        )
        title_label.pack()
        
        content_frame = tk.Frame(self, bg="#FFF8E1", padx=20, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        if self.story_node.speaker:
            speaker_frame = tk.Frame(content_frame, bg="#E8F5E9", padx=10, pady=5)
            speaker_frame.pack(fill=tk.X, pady=(0, 10))
            
            speaker_label = tk.Label(
                speaker_frame,
                text=f"💬 {self.story_node.speaker}",
                font=("微软雅黑", 11, "bold"),
                fg="#2E7D32",
                bg="#E8F5E9"
            )
            speaker_label.pack(anchor=tk.W)
        
        content_text = scrolledtext.ScrolledText(
            content_frame,
            font=("微软雅黑", 12),
            wrap=tk.WORD,
            height=10,
            bg="#FFFDE7",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        content_text.pack(fill=tk.BOTH, expand=True)
        content_text.insert(tk.END, self.story_node.content)
        content_text.config(state=tk.DISABLED)
        
        if self.story_node.has_choices():
            choices_frame = tk.Frame(self, bg="#FFF8E1", padx=20, pady=10)
            choices_frame.pack(fill=tk.X)
            
            choices_label = tk.Label(
                choices_frame,
                text="选择你的回应：",
                font=("微软雅黑", 11, "bold"),
                bg="#FFF8E1"
            )
            choices_label.pack(anchor=tk.W, pady=(0, 5))
            
            for choice in self.story_node.choices:
                btn = tk.Button(
                    choices_frame,
                    text=choice.text,
                    font=("微软雅黑", 10),
                    bg="#4CAF50",
                    fg="white",
                    relief=tk.FLAT,
                    cursor="hand2",
                    command=lambda c=choice: self._on_choice_selected(c)
                )
                btn.pack(fill=tk.X, pady=3)
        else:
            button_frame = tk.Frame(self, bg="#FFF8E1", padx=20, pady=15)
            button_frame.pack(fill=tk.X)
            
            if self.story_node.is_end_node():
                tk.Button(
                    button_frame,
                    text="完成章节",
                    font=("微软雅黑", 11, "bold"),
                    bg="#FF9800",
                    fg="white",
                    relief=tk.FLAT,
                    command=self._on_continue
                ).pack(side=tk.RIGHT, padx=5)
            else:
                tk.Button(
                    button_frame,
                    text="继续 →",
                    font=("微软雅黑", 11, "bold"),
                    bg="#4CAF50",
                    fg="white",
                    relief=tk.FLAT,
                    command=self._on_continue
                ).pack(side=tk.RIGHT, padx=5)
            
            tk.Button(
                button_frame,
                text="跳过剧情",
                font=("微软雅黑", 10),
                bg="#9E9E9E",
                fg="white",
                relief=tk.FLAT,
                command=self._on_skip
            ).pack(side=tk.LEFT)
    
    def _on_choice_selected(self, choice):
        self.on_choice(choice.choice_id)
        self.destroy()
    
    def _on_continue(self):
        self.on_continue()
        self.destroy()
    
    def _on_skip(self):
        self.on_skip()
        self.destroy()


class StoryPanel(tk.Frame):
    
    def __init__(self, parent, story_manager, on_story_event: Callable):
        super().__init__(parent)
        
        self.story_manager = story_manager
        self.on_story_event = on_story_event
        
        self._setup_ui()
        self._update_display()
    
    def _setup_ui(self):
        self.configure(bg="#F5F5F5", padx=10, pady=10)
        
        title_label = tk.Label(
            self,
            text="📜 故事进度",
            font=("微软雅黑", 12, "bold"),
            bg="#F5F5F5",
            fg="#2E7D32"
        )
        title_label.pack(anchor=tk.W)
        
        self.progress_label = tk.Label(
            self,
            text="",
            font=("微软雅黑", 10),
            bg="#F5F5F5",
            fg="#666666"
        )
        self.progress_label.pack(anchor=tk.W, pady=(5, 10))
        
        self.chapter_listbox = tk.Listbox(
            self,
            font=("微软雅黑", 10),
            height=8,
            selectmode=tk.SINGLE,
            bg="#FFFFFF",
            relief=tk.FLAT
        )
        self.chapter_listbox.pack(fill=tk.BOTH, expand=True)
        self.chapter_listbox.bind("<<ListboxSelect>>", self._on_chapter_select)
        
        self.start_btn = tk.Button(
            self,
            text="▶️ 开始章节",
            font=("微软雅黑", 10),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            command=self._start_selected_chapter
        )
        self.start_btn.pack(fill=tk.X, pady=(10, 0))
    
    def _update_display(self):
        progress = self.story_manager.get_chapter_progress()
        self.progress_label.config(
            text=f"完成进度: {progress['completed']}/{progress['total']} ({progress['percentage']:.0f}%)"
        )
        
        self.chapter_listbox.delete(0, tk.END)
        
        for chapter in self.story_manager.chapters.values():
            status_icon = {
                "locked": "🔒",
                "available": "⭕",
                "in_progress": "▶️",
                "completed": "✅"
            }.get(chapter.status.value, "❓")
            
            self.chapter_listbox.insert(
                tk.END,
                f"{status_icon} 第{chapter.chapter_number}章: {chapter.title}"
            )
    
    def _on_chapter_select(self, event):
        pass
    
    def _start_selected_chapter(self):
        selection = self.chapter_listbox.curselection()
        if not selection:
            messagebox.showinfo("提示", "请先选择一个章节！")
            return
        
        chapter_ids = list(self.story_manager.chapters.keys())
        selected_chapter_id = chapter_ids[selection[0]]
        
        chapter = self.story_manager.chapters.get(selected_chapter_id)
        if chapter and chapter.status.value in ["available", "in_progress"]:
            self.story_manager.start_chapter(selected_chapter_id)
            self._show_current_node()
        else:
            messagebox.showinfo("提示", "该章节尚未解锁！")
    
    def _show_current_node(self):
        node = self.story_manager.get_current_node()
        if node:
            self.on_story_event(node)
    
    def refresh(self):
        self._update_display()


class LevelPanel(tk.Frame):
    
    def __init__(self, parent, level_system):
        super().__init__(parent)
        
        self.level_system = level_system
        self._setup_ui()
    
    def _setup_ui(self):
        self.configure(bg="#F5F5F5", padx=10, pady=10)
        
        info = self.level_system.get_level_info()
        
        header_frame = tk.Frame(self, bg="#F5F5F5")
        header_frame.pack(fill=tk.X)
        
        level_label = tk.Label(
            header_frame,
            text=f"Lv.{info['level']}",
            font=("微软雅黑", 14, "bold"),
            bg="#F5F5F5",
            fg="#4CAF50"
        )
        level_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            header_frame,
            text=f"  {info['title']}",
            font=("微软雅黑", 11),
            bg="#F5F5F5",
            fg="#666666"
        )
        title_label.pack(side=tk.LEFT)
        
        self.progress_frame = tk.Frame(self, bg="#E0E0E0", height=20)
        self.progress_frame.pack(fill=tk.X, pady=10)
        self.progress_frame.pack_propagate(False)
        
        self.progress_bar = tk.Frame(self.progress_frame, bg="#4CAF50")
        self.progress_bar.place(relwidth=info['exp_progress'], relheight=1)
        
        exp_text = f"EXP: {info['exp']} / {info['exp'] + info['exp_to_next']}" if info['exp_to_next'] > 0 else "MAX LEVEL"
        self.exp_label = tk.Label(
            self,
            text=exp_text,
            font=("微软雅黑", 9),
            bg="#F5F5F5",
            fg="#888888"
        )
        self.exp_label.pack()
        
        unlocks_label = tk.Label(
            self,
            text=f"📖 {info['description']}",
            font=("微软雅黑", 9),
            bg="#F5F5F5",
            fg="#666666",
            wraplength=200,
            justify=tk.LEFT
        )
        unlocks_label.pack(anchor=tk.W, pady=(5, 0))
    
    def refresh(self):
        info = self.level_system.get_level_info()
        self.progress_bar.place(relwidth=info['exp_progress'], relheight=1)
        exp_text = f"EXP: {info['exp']} / {info['exp'] + info['exp_to_next']}" if info['exp_to_next'] > 0 else "MAX LEVEL"
        self.exp_label.config(text=exp_text)


class PetPanel(tk.Frame):
    
    def __init__(self, parent, pet_manager, on_action: Callable):
        super().__init__(parent)
        
        self.pet_manager = pet_manager
        self.on_action = on_action
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.configure(bg="#F5F5F5", padx=10, pady=10)
        
        title_label = tk.Label(
            self,
            text="🐾 我的宠物",
            font=("微软雅黑", 12, "bold"),
            bg="#F5F5F5",
            fg="#FF9800"
        )
        title_label.pack(anchor=tk.W)
        
        pet = self.pet_manager.get_active_pet()
        
        if pet:
            self._create_pet_info(pet)
        else:
            no_pet_label = tk.Label(
                self,
                text="你还没有宠物\n完成剧情可获得宠物",
                font=("微软雅黑", 10),
                bg="#F5F5F5",
                fg="#888888",
                justify=tk.CENTER
            )
            no_pet_label.pack(pady=20)
    
    def _create_pet_info(self, pet):
        info_frame = tk.Frame(self, bg="#FFF8E1", relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        header = tk.Frame(info_frame, bg="#FFF8E1")
        header.pack(fill=tk.X, padx=10, pady=5)
        
        emoji_label = tk.Label(
            header,
            text=pet.emoji,
            font=("Segoe UI Emoji", 24),
            bg="#FFF8E1"
        )
        emoji_label.pack(side=tk.LEFT)
        
        name_frame = tk.Frame(header, bg="#FFF8E1")
        name_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            name_frame,
            text=pet.name,
            font=("微软雅黑", 12, "bold"),
            bg="#FFF8E1"
        ).pack(anchor=tk.W)
        
        tk.Label(
            name_frame,
            text=f"Lv.{pet.level} {pet.type_name}",
            font=("微软雅黑", 9),
            bg="#FFF8E1",
            fg="#666666"
        ).pack(anchor=tk.W)
        
        stats_frame = tk.Frame(info_frame, bg="#FFF8E1")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        stats = [
            ("饱食", pet.stats.hunger, "❤️"),
            ("快乐", pet.stats.happiness, "💛"),
            ("体力", pet.stats.energy, "⚡"),
        ]
        
        for i, (name, value, icon) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg="#FFF8E1")
            stat_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                stat_frame,
                text=f"{icon} {name}:",
                font=("微软雅黑", 9),
                bg="#FFF8E1",
                width=8,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            progress_bg = tk.Frame(stat_frame, bg="#E0E0E0", height=10)
            progress_bg.pack(side=tk.LEFT, fill=tk.X, expand=True)
            progress_bg.pack_propagate(False)
            
            color = "#4CAF50" if value > 50 else "#FF9800" if value > 20 else "#F44336"
            progress = tk.Frame(progress_bg, bg=color)
            progress.place(relwidth=value/100, relheight=1)
        
        actions_frame = tk.Frame(self, bg="#F5F5F5")
        actions_frame.pack(fill=tk.X, pady=10)
        
        actions = [
            ("🍖 喂食", lambda: self.on_action("feed")),
            ("🎾 玩耍", lambda: self.on_action("play")),
            ("💕 抚摸", lambda: self.on_action("pet")),
        ]
        
        for text, cmd in actions:
            tk.Button(
                actions_frame,
                text=text,
                font=("微软雅黑", 9),
                bg="#4CAF50",
                fg="white",
                relief=tk.FLAT,
                command=cmd
            ).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)


class ExplorationPanel(tk.Frame):
    
    def __init__(self, parent, exploration_manager, on_explore: Callable):
        super().__init__(parent)
        
        self.exploration_manager = exploration_manager
        self.on_explore = on_explore
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.configure(bg="#F5F5F5", padx=10, pady=10)
        
        title_label = tk.Label(
            self,
            text="🗺️ 户外探险",
            font=("微软雅黑", 12, "bold"),
            bg="#F5F5F5",
            fg="#2196F3"
        )
        title_label.pack(anchor=tk.W)
        
        areas = self.exploration_manager.get_available_areas()
        
        if areas:
            for area in areas[:4]:
                area_frame = tk.Frame(self, bg="#E3F2FD", relief=tk.RAISED, bd=1)
                area_frame.pack(fill=tk.X, pady=5)
                
                header = tk.Frame(area_frame, bg="#E3F2FD")
                header.pack(fill=tk.X, padx=10, pady=5)
                
                tk.Label(
                    header,
                    text=area['icon'],
                    font=("Segoe UI Emoji", 16),
                    bg="#E3F2FD"
                ).pack(side=tk.LEFT)
                
                tk.Label(
                    header,
                    text=area['name'],
                    font=("微软雅黑", 10, "bold"),
                    bg="#E3F2FD"
                ).pack(side=tk.LEFT, padx=5)
                
                tk.Label(
                    header,
                    text=f"体力: {area['energy_cost']}",
                    font=("微软雅黑", 8),
                    bg="#E3F2FD",
                    fg="#666666"
                ).pack(side=tk.RIGHT)
                
                tk.Button(
                    area_frame,
                    text="探索",
                    font=("微软雅黑", 9),
                    bg="#2196F3",
                    fg="white",
                    relief=tk.FLAT,
                    command=lambda a=area: self.on_explore(a)
                ).pack(pady=5)
        else:
            tk.Label(
                self,
                text="暂无可用探险区域\n提升等级解锁更多区域",
                font=("微软雅黑", 10),
                bg="#F5F5F5",
                fg="#888888",
                justify=tk.CENTER
            ).pack(pady=20)


class EnhancedGameWindow(tk.Frame):
    
    def __init__(self, parent, game_manager, save_manager, on_return_to_menu, on_exit_game):
        super().__init__(parent)
        
        self.game_manager = game_manager
        self.save_manager = save_manager
        self.on_return_to_menu = on_return_to_menu
        self.on_exit_game = on_exit_game
        
        self.plot_buttons = {}
        self.status_labels = {}
        
        self._init_managers()
        self._setup_ui()
        self._update_display()
        self._start_auto_update()
    
    def _init_managers(self):
        from models.story import StoryManager
        from models.level_system import LevelSystem
        from models.pet import PetManager
        from models.item import ItemManager
        from models.exploration import ExplorationManager
        from models.home import HomeManager
        from models.game_mode import GameModeManager
        
        self.story_manager = StoryManager()
        self.level_system = LevelSystem()
        self.pet_manager = PetManager()
        self.item_manager = ItemManager()
        self.exploration_manager = ExplorationManager()
        self.home_manager = HomeManager()
        self.mode_manager = GameModeManager()
        
        self.story_manager.on_story_event = self._on_story_event
    
    def _setup_ui(self):
        self._create_styles()
        
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=2)
        
        center_frame = ttk.Frame(main_paned)
        main_paned.add(center_frame, weight=3)
        
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        self._setup_left_panel(left_frame)
        self._setup_center_panel(center_frame)
        self._setup_right_panel(right_frame)
    
    def _create_styles(self):
        style = ttk.Style()
        
        style.configure('SeedButton.TButton',
                      font=('微软雅黑', 10, 'bold'),
                      padding=10)
    
    def _setup_left_panel(self, parent):
        self._create_info_bar(parent)
        self._create_farm_area(parent)
        self._create_player_status(parent)
    
    def _setup_center_panel(self, parent):
        story_frame = ttk.LabelFrame(parent, text="📜 故事", padding=10)
        story_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.story_panel = StoryPanel(story_frame, self.story_manager, self._show_story_card)
        self.story_panel.pack(fill=tk.BOTH, expand=True)
        
        tabs_frame = ttk.LabelFrame(parent, text="📋 功能面板", padding=5)
        tabs_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        notebook = ttk.Notebook(tabs_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        self._create_shop_tab(notebook)
        self._create_inventory_tab(notebook)
        self._create_exploration_tab(notebook)
        self._create_home_tab(notebook)
    
    def _setup_right_panel(self, parent):
        level_frame = ttk.LabelFrame(parent, text="⭐ 等级", padding=5)
        level_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.level_panel = LevelPanel(level_frame, self.level_system)
        self.level_panel.pack(fill=tk.X)
        
        pet_frame = ttk.LabelFrame(parent, text="🐾 宠物", padding=5)
        pet_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.pet_panel = PetPanel(pet_frame, self.pet_manager, self._on_pet_action)
        self.pet_panel.pack(fill=tk.BOTH, expand=True)
        
        self._create_quick_actions(parent)
        self._create_message_log(parent)
    
    def _create_info_bar(self, parent):
        info_frame = ttk.LabelFrame(parent, text="📅 当前状态", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        date_frame = ttk.Frame(info_frame)
        date_frame.pack(fill=tk.X)
        
        self.date_label = ttk.Label(date_frame, text="", style='Header.TLabel')
        self.date_label.pack(side=tk.LEFT)
        
        self.weather_label = ttk.Label(date_frame, text="", style='Normal.TLabel')
        self.weather_label.pack(side=tk.RIGHT)
    
    def _create_farm_area(self, parent):
        farm_frame = ttk.LabelFrame(parent, text="🏠 我的农场", padding=10)
        farm_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        grid_frame = ttk.Frame(farm_frame)
        grid_frame.pack(expand=True)
        
        size = self.game_manager.get_plot_size()
        
        for row in range(size):
            for col in range(size):
                btn = tk.Button(
                    grid_frame,
                    width=6,
                    height=3,
                    font=('微软雅黑', 10),
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda r=row, c=col: self._on_plot_click(r, c)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.plot_buttons[(row, col)] = btn
    
    def _create_player_status(self, parent):
        status_frame = ttk.LabelFrame(parent, text="👤 农民信息", padding=10)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        money_frame = ttk.Frame(status_frame)
        money_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(money_frame, text="💰 金币:", style='Normal.TLabel').pack(side=tk.LEFT)
        self.money_label = ttk.Label(money_frame, text="", style='Header.TLabel', foreground='gold')
        self.money_label.pack(side=tk.LEFT, padx=(5, 0))
        
        seeds_frame = ttk.Frame(status_frame)
        seeds_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(seeds_frame, text="🌱 种子:", style='Normal.TLabel').pack(side=tk.LEFT)
        self.seeds_label = ttk.Label(seeds_frame, text="", style='Normal.TLabel')
        self.seeds_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def _create_shop_tab(self, parent):
        shop_frame = ttk.Frame(parent)
        parent.add(shop_frame, text="🛒 商店")
        
        canvas = tk.Canvas(shop_frame)
        scrollbar = ttk.Scrollbar(shop_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.seed_buttons = {}
        self.selected_seed = None
    
    def _create_inventory_tab(self, parent):
        inv_frame = ttk.Frame(parent)
        parent.add(inv_frame, text="📦 背包")
        
        self.inv_listbox = tk.Listbox(inv_frame, font=('微软雅黑', 10))
        self.inv_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        btn_frame = ttk.Frame(inv_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="使用", command=self._use_selected_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="出售", command=self._sell_selected_item).pack(side=tk.LEFT, padx=2)
    
    def _create_exploration_tab(self, parent):
        exp_frame = ttk.Frame(parent)
        parent.add(exp_frame, text="🗺️ 探险")
        
        self.exploration_panel = ExplorationPanel(exp_frame, self.exploration_manager, self._on_explore)
        self.exploration_panel.pack(fill=tk.BOTH, expand=True)
    
    def _create_home_tab(self, parent):
        home_frame = ttk.Frame(parent)
        parent.add(home_frame, text="🏠 家园")
        
        home_info = self.home_manager.get_home_info()
        
        info_frame = ttk.Frame(home_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            info_frame,
            text=f"房屋等级: {home_info['level']}/{home_info['max_level']}",
            font=('微软雅黑', 11, 'bold')
        ).pack()
        
        ttk.Label(
            info_frame,
            text=f"舒适度: {home_info['total_comfort']}  储物空间: {home_info['total_storage']}",
            font=('微软雅黑', 9)
        ).pack()
        
        ttk.Button(
            home_frame,
            text="升级房屋",
            command=self._upgrade_home
        ).pack(pady=10)
    
    def _create_quick_actions(self, parent):
        quick_frame = ttk.LabelFrame(parent, text="⚡ 快捷操作", padding=10)
        quick_frame.pack(fill=tk.X, padx=5, pady=5)
        
        btn_frame1 = ttk.Frame(quick_frame)
        btn_frame1.pack(fill=tk.X, pady=2)
        
        ttk.Button(btn_frame1, text="💧 浇水", command=self._water_all_plots).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_frame1, text="🌾 收获", command=self._harvest_all_mature).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        btn_frame2 = ttk.Frame(quick_frame)
        btn_frame2.pack(fill=tk.X, pady=2)
        
        ttk.Button(btn_frame2, text="⏭️ 下一天", command=self._advance_day).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_frame2, text="💾 保存", command=self._save_game).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
    
    def _create_message_log(self, parent):
        log_frame = ttk.LabelFrame(parent, text="📜 消息日志", padding=5)
        log_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('微软雅黑', 8),
            height=5,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def _on_plot_click(self, row, col):
        plot = self.game_manager.get_plot(row, col)
        
        if plot.is_empty():
            self._show_plant_dialog(row, col)
        elif plot.is_mature():
            self._harvest_plot(row, col)
        else:
            progress = int(plot.get_growth_progress() * 100)
            self._add_message(f"🌱 {plot.crop.name} 生长进度: {progress}%")
    
    def _show_plant_dialog(self, row, col):
        dialog = tk.Toplevel(self)
        dialog.title("🌱 选择作物")
        dialog.geometry("300x350")
        dialog.transient(self)
        dialog.grab_set()
        
        player_seeds = self.game_manager.player.seeds
        current_season = self.game_manager.get_current_season()
        
        for crop_name, seed_count in player_seeds.items():
            if seed_count > 0:
                crop = self.game_manager.economy_system.get_crop(crop_name)
                if crop:
                    btn = ttk.Button(
                        dialog,
                        text=f"{crop.emoji} {crop_name} (x{seed_count})",
                        command=lambda n=crop_name: self._plant_and_close(n, row, col, dialog)
                    )
                    btn.pack(fill=tk.X, padx=10, pady=2)
        
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack(fill=tk.X, padx=10, pady=10)
    
    def _plant_and_close(self, crop_name, row, col, dialog):
        success, msg = self.game_manager.plant_crop(row, col, crop_name)
        self._add_message(msg)
        if success:
            self._update_display()
        dialog.destroy()
    
    def _harvest_plot(self, row, col):
        success, msg = self.game_manager.harvest_plot(row, col)
        self._add_message(msg)
        if success:
            self._update_display()
    
    def _water_all_plots(self):
        if self.game_manager.time_system.is_rainy():
            self._add_message("🌧️ 今天下雨，作物自动获得水分！")
            return
        
        success_count, _ = self.game_manager.water_all_plots()
        if success_count > 0:
            self._add_message(f"💧 成功给 {success_count} 块地浇水！")
            self._update_display()
        else:
            self._add_message("💧 没有需要浇水的作物。")
    
    def _harvest_all_mature(self):
        count, messages = self.game_manager.harvest_all_mature()
        if count > 0:
            self._add_message(f"🎉 收获了 {count} 个作物！")
            self._update_display()
        else:
            self._add_message("🍂 没有成熟的作物可以收获。")
    
    def _advance_day(self):
        result = self.game_manager.advance_day()
        
        self._add_message("=" * 40)
        self._add_message(f"🌞 第{result.day}天 - {result.season} - {result.weather}")
        
        if result.events:
            for event in result.events:
                self._add_message(f"  {event}")
        
        pet_results = self.pet_manager.new_day_all()
        for pet_id, pet_result in pet_results.items():
            for event in pet_result.get("events", []):
                self._add_message(f"🐾 {event}")
        
        self._update_display()
    
    def _save_game(self):
        self.save_manager.save_game(self.game_manager)
        self._add_message("💾 游戏已保存！")
    
    def _update_display(self):
        self.date_label.config(text=self.game_manager.get_current_date())
        self.weather_label.config(text=f"🌤️ {self.game_manager.get_current_weather().value}")
        
        player = self.game_manager.player
        self.money_label.config(text=f"{player.money} 金")
        
        seeds_info = " | ".join([f"{name}:{count}" for name, count in list(player.seeds.items())[:3]])
        self.seeds_label.config(text=seeds_info if seeds_info else "无")
        
        self._update_farm_display()
        self._update_inventory_display()
        
        if hasattr(self, 'level_panel'):
            self.level_panel.refresh()
    
    def _update_farm_display(self):
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
                        stages = ["🌱", "🌿", "🪴", crop.emoji]
                        stage_text = stages[min(plot.growth_stage, 3)]
                        colors = ["#FFB6C1", "#98FB98", "#32CD32", "#228B22"]
                        color = colors[min(plot.growth_stage, 3)]
                        btn.config(text=f"{stage_text}\n{crop.name}", bg=color, fg="white")
    
    def _update_inventory_display(self):
        self.inv_listbox.delete(0, tk.END)
        
        for item_id, count in self.item_manager.inventory.items():
            item = self.item_manager.get_item_data(item_id)
            if item:
                self.inv_listbox.insert(tk.END, f"{item.icon} {item.name} x{count}")
        
        for crop_name, count in self.game_manager.player.inventory.items():
            self.inv_listbox.insert(tk.END, f"🌾 {crop_name} x{count}")
    
    def _use_selected_item(self):
        selection = self.inv_listbox.curselection()
        if not selection:
            return
        
        item_text = self.inv_listbox.get(selection[0])
        self._add_message(f"使用道具: {item_text}")
    
    def _sell_selected_item(self):
        selection = self.inv_listbox.curselection()
        if not selection:
            return
        
        item_text = self.inv_listbox.get(selection[0])
        self._add_message(f"出售: {item_text}")
    
    def _upgrade_home(self):
        success, msg = self.home_manager.upgrade_home(self.game_manager.player.money)
        if success:
            self.game_manager.player.spend_money(self.home_manager.home.get_upgrade_cost() // 2)
        self._add_message(msg)
        self._update_display()
    
    def _on_explore(self, area):
        self._add_message(f"🗺️ 探索 {area['name']}...")
    
    def _on_pet_action(self, action):
        pet = self.pet_manager.get_active_pet()
        if not pet:
            return
        
        if action == "feed":
            result = self.pet_manager.feed_pet(pet.pet_id)
        elif action == "play":
            result = self.pet_manager.play_with_pet(pet.pet_id)
        elif action == "pet":
            result = self.pet_manager.pet_the_pet(pet.pet_id)
        else:
            return
        
        self._add_message(f"🐾 {result['message']}")
    
    def _on_story_event(self, event_type, data):
        if event_type == "rewards":
            self._apply_story_rewards(data)
    
    def _apply_story_rewards(self, rewards):
        if rewards.get("money"):
            self.game_manager.player.earn_money(rewards["money"])
            self._add_message(f"💰 获得 {rewards['money']} 金币")
        
        if rewards.get("exp"):
            result = self.level_system.add_exp(rewards["exp"])
            self._add_message(f"⭐ 获得 {rewards['exp']} 经验")
            
            for level in result.get("level_ups", []):
                self._add_message(f"🎉 升级到 {level} 级！")
    
    def _show_story_card(self, node):
        StoryCardDialog(
            self,
            node,
            self._on_story_choice,
            self._on_story_continue,
            self._on_story_skip
        )
    
    def _on_story_choice(self, choice_id):
        next_node = self.story_manager.advance_to_next_node(choice_id)
        if next_node:
            self._show_story_card(next_node)
        else:
            self.story_panel.refresh()
    
    def _on_story_continue(self):
        next_node = self.story_manager.advance_to_next_node()
        if next_node:
            self._show_story_card(next_node)
        else:
            self.story_panel.refresh()
    
    def _on_story_skip(self):
        self.story_panel.refresh()
    
    def _add_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted_msg)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _start_auto_update(self):
        def auto_update():
            if self.winfo_exists():
                self._update_display()
                self.after(1000, auto_update)
        
        auto_update()
