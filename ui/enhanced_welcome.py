"""
增强版主界面模块
提供动态背景、大标题、模式选择和角色自定义功能
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, List
import random
import math


class AnimatedBackground(tk.Canvas):
    
    def __init__(self, parent, width: int, height: int):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        
        self.width = width
        self.height = height
        self.particles = []
        self.clouds = []
        self.stars = []
        
        self._create_gradient_background()
        self._create_particles()
        self._create_clouds()
        self._create_stars()
        
        self._animate()
    
    def _create_gradient_background(self):
        colors = [
            "#87CEEB",
            "#98D8E8",
            "#A8E6CF",
            "#B8E6B8",
        ]
        
        steps = len(colors)
        height_step = self.height // steps
        
        for i, color in enumerate(colors):
            self.create_rectangle(
                0, i * height_step,
                self.width, (i + 1) * height_step,
                fill=color, outline=color
            )
    
    def _create_particles(self):
        for _ in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 5)
            speed = random.uniform(0.5, 2)
            
            particle = {
                "id": self.create_oval(
                    x, y, x + size, y + size,
                    fill="#FFFFFF", outline=""
                ),
                "x": x,
                "y": y,
                "size": size,
                "speed": speed,
                "angle": random.uniform(0, 2 * math.pi)
            }
            self.particles.append(particle)
    
    def _create_clouds(self):
        for i in range(5):
            x = random.randint(0, self.width)
            y = random.randint(20, 150)
            size = random.randint(40, 80)
            speed = random.uniform(0.2, 0.5)
            
            cloud_group = []
            for j in range(3):
                cx = x + j * size // 2
                cy = y + random.randint(-10, 10)
                cs = size - j * 5
                
                cloud_id = self.create_oval(
                    cx, cy, cx + cs, cy + cs // 2,
                    fill="#FFFFFF", outline=""
                )
                cloud_group.append(cloud_id)
            
            self.clouds.append({
                "ids": cloud_group,
                "x": x,
                "y": y,
                "size": size,
                "speed": speed
            })
    
    def _create_stars(self):
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height // 2)
            size = random.randint(1, 3)
            alpha = random.randint(100, 255)
            
            star = {
                "id": self.create_oval(
                    x, y, x + size, y + size,
                    fill="#FFFF99", outline=""
                ),
                "x": x,
                "y": y,
                "size": size,
                "alpha": alpha,
                "direction": 1
            }
            self.stars.append(star)
    
    def _animate(self):
        for particle in self.particles:
            particle["x"] += math.cos(particle["angle"]) * particle["speed"]
            particle["y"] += math.sin(particle["angle"]) * particle["speed"]
            
            if particle["x"] < 0 or particle["x"] > self.width:
                particle["angle"] = math.pi - particle["angle"]
            if particle["y"] < 0 or particle["y"] > self.height:
                particle["angle"] = -particle["angle"]
            
            self.coords(
                particle["id"],
                particle["x"], particle["y"],
                particle["x"] + particle["size"],
                particle["y"] + particle["size"]
            )
        
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > self.width + cloud["size"]:
                cloud["x"] = -cloud["size"]
            
            for i, cloud_id in enumerate(cloud["ids"]):
                cx = cloud["x"] + i * cloud["size"] // 2
                cy = cloud["y"]
                self.coords(
                    cloud_id,
                    cx, cy,
                    cx + cloud["size"] - i * 5,
                    cy + (cloud["size"] - i * 5) // 2
                )
        
        self.after(50, self._animate)


class ModeSelectionCard(tk.Frame):
    
    def __init__(self, parent, mode_data: Dict, on_select: Callable, is_unlocked: bool = True):
        super().__init__(parent, relief=tk.RAISED, bd=2)
        
        self.mode_data = mode_data
        self.on_select = on_select
        self.is_unlocked = is_unlocked
        
        self._setup_ui()
    
    def _setup_ui(self):
        bg_color = "#FFFFFF" if self.is_unlocked else "#CCCCCC"
        self.configure(bg=bg_color, padx=20, pady=15)
        
        header_frame = tk.Frame(self, bg=bg_color)
        header_frame.pack(fill=tk.X)
        
        icon_label = tk.Label(
            header_frame,
            text=self.mode_data.get("icon", "🎮"),
            font=("Segoe UI Emoji", 32),
            bg=bg_color
        )
        icon_label.pack(side=tk.LEFT)
        
        name_label = tk.Label(
            header_frame,
            text=self.mode_data.get("name", "未知模式"),
            font=("微软雅黑", 14, "bold"),
            bg=bg_color,
            fg="#2E8B57" if self.is_unlocked else "#888888"
        )
        name_label.pack(side=tk.LEFT, padx=(10, 0))
        
        if not self.is_unlocked:
            lock_label = tk.Label(
                header_frame,
                text="🔒",
                font=("Segoe UI Emoji", 16),
                bg=bg_color
            )
            lock_label.pack(side=tk.RIGHT)
        
        desc_text = self.mode_data.get("description", "")
        desc_label = tk.Label(
            self,
            text=desc_text,
            font=("微软雅黑", 10),
            bg=bg_color,
            fg="#555555",
            justify=tk.LEFT,
            wraplength=250
        )
        desc_label.pack(fill=tk.X, pady=(10, 0))
        
        if self.is_unlocked:
            select_btn = tk.Button(
                self,
                text="选择此模式",
                font=("微软雅黑", 10),
                bg="#4CAF50",
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda: self.on_select(self.mode_data["mode_type"])
            )
            select_btn.pack(fill=tk.X, pady=(15, 0))
        else:
            unlock_text = f"需要等级 {self.mode_data.get('required_level', '?')} 解锁"
            unlock_label = tk.Label(
                self,
                text=unlock_text,
                font=("微软雅黑", 9),
                bg=bg_color,
                fg="#888888"
            )
            unlock_label.pack(pady=(10, 0))


class CharacterCreationDialog(tk.Toplevel):
    
    def __init__(self, parent, on_complete: Callable):
        super().__init__(parent)
        
        self.on_complete = on_complete
        self.character_data = {
            "name": "农夫",
            "age": 25,
            "gender": "male",
            "avatar": "👨‍🌾"
        }
        
        self.title("创建角色")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(bg="#F5F5F5")
        
        self.transient(parent)
        self.grab_set()
        
        self._setup_ui()
    
    def _setup_ui(self):
        title_label = tk.Label(
            self,
            text="👤 创建你的角色",
            font=("微软雅黑", 16, "bold"),
            bg="#F5F5F5",
            fg="#2E8B57"
        )
        title_label.pack(pady=20)
        
        avatar_frame = tk.Frame(self, bg="#F5F5F5")
        avatar_frame.pack(pady=10)
        
        self.avatars = ["👨‍🌾", "👩‍🌾", "🧑‍🌾", "👴", "👵", "🧔"]
        self.selected_avatar = tk.StringVar(value=self.avatars[0])
        
        for i, avatar in enumerate(self.avatars):
            rb = tk.Radiobutton(
                avatar_frame,
                text=avatar,
                variable=self.selected_avatar,
                value=avatar,
                font=("Segoe UI Emoji", 20),
                bg="#F5F5F5",
                selectcolor="#E8F5E9",
                indicatoron=False,
                width=2,
                height=1
            )
            rb.grid(row=0, column=i, padx=5)
        
        name_frame = tk.Frame(self, bg="#F5F5F5")
        name_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(
            name_frame,
            text="角色名称:",
            font=("微软雅黑", 11),
            bg="#F5F5F5"
        ).pack(anchor=tk.W)
        
        self.name_entry = tk.Entry(
            name_frame,
            font=("微软雅黑", 12),
            width=25
        )
        self.name_entry.pack(fill=tk.X, pady=5)
        self.name_entry.insert(0, "农夫")
        
        age_frame = tk.Frame(self, bg="#F5F5F5")
        age_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(
            age_frame,
            text="年龄:",
            font=("微软雅黑", 11),
            bg="#F5F5F5"
        ).pack(anchor=tk.W)
        
        self.age_var = tk.IntVar(value=25)
        age_scale = tk.Scale(
            age_frame,
            from_=18,
            to=60,
            orient=tk.HORIZONTAL,
            variable=self.age_var,
            font=("微软雅黑", 10),
            bg="#F5F5F5",
            length=300
        )
        age_scale.pack(fill=tk.X, pady=5)
        
        gender_frame = tk.Frame(self, bg="#F5F5F5")
        gender_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(
            gender_frame,
            text="性别:",
            font=("微软雅黑", 11),
            bg="#F5F5F5"
        ).pack(anchor=tk.W)
        
        self.gender_var = tk.StringVar(value="male")
        
        gender_options = tk.Frame(gender_frame, bg="#F5F5F5")
        gender_options.pack(fill=tk.X, pady=5)
        
        tk.Radiobutton(
            gender_options,
            text="男性 👨",
            variable=self.gender_var,
            value="male",
            font=("微软雅黑", 10),
            bg="#F5F5F5"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            gender_options,
            text="女性 👩",
            variable=self.gender_var,
            value="female",
            font=("微软雅黑", 10),
            bg="#F5F5F5"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            gender_options,
            text="其他 🧑",
            variable=self.gender_var,
            value="other",
            font=("微软雅黑", 10),
            bg="#F5F5F5"
        ).pack(side=tk.LEFT, padx=10)
        
        button_frame = tk.Frame(self, bg="#F5F5F5")
        button_frame.pack(fill=tk.X, padx=30, pady=30)
        
        tk.Button(
            button_frame,
            text="使用默认角色",
            font=("微软雅黑", 10),
            bg="#9E9E9E",
            fg="white",
            relief=tk.FLAT,
            command=self._use_default
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="开始游戏",
            font=("微软雅黑", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            command=self._confirm
        ).pack(side=tk.RIGHT, padx=5)
    
    def _use_default(self):
        self.character_data = {
            "name": "农夫",
            "age": 25,
            "gender": "male",
            "avatar": "👨‍🌾"
        }
        self.on_complete(self.character_data)
        self.destroy()
    
    def _confirm(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("提示", "请输入角色名称！")
            return
        
        self.character_data = {
            "name": name,
            "age": self.age_var.get(),
            "gender": self.gender_var.get(),
            "avatar": self.selected_avatar.get()
        }
        
        self.on_complete(self.character_data)
        self.destroy()


class EnhancedWelcomeScreen(tk.Frame):
    
    def __init__(self, parent, on_start_game: Callable, on_load_game: Callable, on_quit: Callable):
        super().__init__(parent)
        
        self.on_start_game = on_start_game
        self.on_load_game = on_load_game
        self.on_quit = on_quit
        
        self.selected_mode = None
        self.character_data = None
        self.player_level = 1
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.configure(bg="#87CEEB")
        
        self.canvas = AnimatedBackground(self, 900, 700)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self._create_title()
        self._create_menu_buttons()
        self._create_footer()
    
    def _create_title(self):
        title_frame = tk.Frame(self.canvas, bg="#87CEEB")
        
        self.canvas.create_window(450, 80, window=title_frame)
        
        title_label = tk.Label(
            title_frame,
            text="🌟 星露谷物语 🌟",
            font=("微软雅黑", 36, "bold"),
            fg="#2E8B57",
            bg="#87CEEB"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Farm Simulator - 农场模拟器",
            font=("Arial", 14, "italic"),
            fg="#555555",
            bg="#87CEEB"
        )
        subtitle_label.pack(pady=(5, 0))
    
    def _create_menu_buttons(self):
        menu_frame = tk.Frame(self.canvas, bg="#FFFFFF", relief=tk.RAISED, bd=2)
        
        self.canvas.create_window(450, 320, window=menu_frame)
        
        menu_frame.configure(padx=40, pady=30)
        
        welcome_label = tk.Label(
            menu_frame,
            text="欢迎来到星露谷！",
            font=("微软雅黑", 14, "bold"),
            fg="#2E8B57",
            bg="#FFFFFF"
        )
        welcome_label.pack(pady=(0, 20))
        
        new_game_btn = tk.Button(
            menu_frame,
            text="🎮 开始新游戏",
            font=("微软雅黑", 14),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            width=20,
            height=2,
            cursor="hand2",
            command=self._show_mode_selection
        )
        new_game_btn.pack(pady=8)
        
        load_game_btn = tk.Button(
            menu_frame,
            text="📂 加载存档",
            font=("微软雅黑", 14),
            bg="#2196F3",
            fg="white",
            relief=tk.FLAT,
            width=20,
            height=2,
            cursor="hand2",
            command=self.on_load_game
        )
        load_game_btn.pack(pady=8)
        
        settings_btn = tk.Button(
            menu_frame,
            text="⚙️ 设置",
            font=("微软雅黑", 14),
            bg="#FF9800",
            fg="white",
            relief=tk.FLAT,
            width=20,
            height=2,
            cursor="hand2",
            command=self._show_settings
        )
        settings_btn.pack(pady=8)
        
        quit_btn = tk.Button(
            menu_frame,
            text="🚪 退出游戏",
            font=("微软雅黑", 14),
            bg="#9E9E9E",
            fg="white",
            relief=tk.FLAT,
            width=20,
            height=2,
            cursor="hand2",
            command=self.on_quit
        )
        quit_btn.pack(pady=8)
    
    def _create_footer(self):
        footer_frame = tk.Frame(self.canvas, bg="#87CEEB")
        
        self.canvas.create_window(450, 550, window=footer_frame)
        
        tips = [
            "💡 提示：不同的作物适合不同的季节哦！",
            "💡 提示：记得每天给作物浇水！",
            "💡 提示：暴风雨可能会摧毁你的作物！",
            "💡 提示：升级农场可以获得更多土地！",
            "💡 提示：完成成就可以获得特殊奖励！"
        ]
        
        tip_label = tk.Label(
            footer_frame,
            text=random.choice(tips),
            font=("微软雅黑", 10),
            fg="#555555",
            bg="#87CEEB"
        )
        tip_label.pack()
        
        version_label = tk.Label(
            footer_frame,
            text="Version 3.0 | Enhanced Edition",
            font=("Arial", 9),
            fg="#888888",
            bg="#87CEEB"
        )
        version_label.pack(pady=(5, 0))
    
    def _show_mode_selection(self):
        mode_window = tk.Toplevel(self)
        mode_window.title("选择游戏模式")
        mode_window.geometry("900x500")
        mode_window.configure(bg="#F5F5F5")
        mode_window.transient(self.winfo_toplevel())
        mode_window.grab_set()
        
        title_label = tk.Label(
            mode_window,
            text="🎯 选择游戏模式",
            font=("微软雅黑", 18, "bold"),
            bg="#F5F5F5",
            fg="#2E8B57"
        )
        title_label.pack(pady=20)
        
        modes_frame = tk.Frame(mode_window, bg="#F5F5F5")
        modes_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        from models.game_mode import GameModeType, GameModeManager
        
        mode_manager = GameModeManager()
        mode_manager.check_unlock_conditions(self.player_level)
        
        modes_data = [
            {
                "mode_type": GameModeType.CLASSIC.value,
                "name": "🌾 经典模式",
                "icon": "🌾",
                "description": "传统的农场经营体验。\n\n按自己的节奏经营农场，\n没有时间限制，\n享受悠闲的田园生活。",
                "required_level": 1
            },
            {
                "mode_type": GameModeType.ENDLESS.value,
                "name": "♾️ 无限模式",
                "icon": "♾️",
                "description": "没有限制的农场生活。\n\n无限金币、无限种子，\n专注于建设和装饰，\n打造你梦想中的农场。",
                "required_level": 1
            },
            {
                "mode_type": GameModeType.ADVENTURE.value,
                "name": "⚔️ 冒险模式",
                "icon": "⚔️",
                "description": "充满挑战的冒险之旅。\n\n完成各种目标，\n应对随机事件，\n成为传奇农场主！",
                "required_level": 3
            },
        ]
        
        for i, mode_data in enumerate(modes_data):
            is_unlocked = mode_manager.is_mode_unlocked(GameModeType(mode_data["mode_type"]))
            
            card = ModeSelectionCard(
                modes_frame,
                mode_data,
                lambda m: self._on_mode_selected(m, mode_window),
                is_unlocked
            )
            card.grid(row=0, column=i, padx=15, pady=10, sticky=tk.NSEW)
            
            modes_frame.columnconfigure(i, weight=1)
    
    def _on_mode_selected(self, mode_type: str, mode_window):
        self.selected_mode = mode_type
        mode_window.destroy()
        
        CharacterCreationDialog(self, self._on_character_created)
    
    def _on_character_created(self, character_data: Dict):
        self.character_data = character_data
        self.on_start_game(self.selected_mode, self.character_data)
    
    def _show_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("设置")
        settings_window.geometry("400x300")
        settings_window.configure(bg="#F5F5F5")
        settings_window.transient(self.winfo_toplevel())
        settings_window.grab_set()
        
        title_label = tk.Label(
            settings_window,
            text="⚙️ 游戏设置",
            font=("微软雅黑", 16, "bold"),
            bg="#F5F5F5",
            fg="#2E8B57"
        )
        title_label.pack(pady=20)
        
        settings_frame = tk.Frame(settings_window, bg="#F5F5F5")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=30)
        
        sound_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            settings_frame,
            text="音效",
            variable=sound_var,
            font=("微软雅黑", 11),
            bg="#F5F5F5"
        ).pack(anchor=tk.W, pady=5)
        
        music_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            settings_frame,
            text="背景音乐",
            variable=music_var,
            font=("微软雅黑", 11),
            bg="#F5F5F5"
        ).pack(anchor=tk.W, pady=5)
        
        auto_save_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            settings_frame,
            text="自动保存",
            variable=auto_save_var,
            font=("微软雅黑", 11),
            bg="#F5F5F5"
        ).pack(anchor=tk.W, pady=5)
        
        tutorial_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            settings_frame,
            text="显示新手引导",
            variable=tutorial_var,
            font=("微软雅黑", 11),
            bg="#F5F5F5"
        ).pack(anchor=tk.W, pady=5)
        
        tk.Button(
            settings_window,
            text="保存设置",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            command=settings_window.destroy
        ).pack(pady=20)
    
    def update_player_level(self, level: int):
        self.player_level = level
