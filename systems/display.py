"""
显示系统模块
负责游戏界面的渲染和展示
"""

import os
import platform
from typing import List, Optional

from core.game_manager import GameManager
from config.settings import Season


class DisplayManager:
    """
    显示管理类
    
    处理游戏的所有文本界面显示逻辑
    """
    
    def __init__(self, game: GameManager):
        """
        初始化显示管理器
        
        Args:
            game: 游戏管理器实例
        """
        self.game = game
    
    def clear_screen(self) -> None:
        """清空控制台屏幕"""
        system = platform.system()
        if system == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def render_frame(self, messages: List[str] = None) -> None:
        """
        渲染完整的游戏帧
        
        Args:
            messages: 要显示的消息列表
        """
        self.clear_screen()
        self.show_header()
        self.show_farm()
        self.show_player_status()
        
        if messages:
            self.show_messages(messages)
        
        self.show_main_menu()
    
    # ========== 头部显示 ==========
    
    def show_header(self) -> None:
        """显示游戏头部信息（日期、天气等）"""
        time_sys = self.game.time_system
        
        # 标题框
        print("\n" + "=" * 60)
        print(f"{'🌾 欢迎来到文字农场 🌾':^56}")
        print("=" * 60)
        
        # 日期信息
        print(f"📅 日期: {time_sys.get_date_string()}")
        
        # 天气信息
        weather_icon = time_sys.weather.value
        weather_desc = time_sys.get_weather_effect_description()
        print(f"🌤️ 天气: {weather_icon}")
        
        # 明日预报
        tomorrow_weather = time_sys.tomorrow_weather
        if tomorrow_weather:
            print(f"📺 明日预报: {tomorrow_weather.value}")
        
        print("-" * 60)
    
    # ========== 农田显示 ==========
    
    def show_farm(self) -> None:
        """显示农田状态"""
        plots = self.game.plots
        size = len(plots)
        
        print(f"\n{'🏘️ 我的农场 (大小: ' + str(size) + 'x' + str(size) + ')':^56}\n")
        
        # 列号标题
        header = "    " + " ".join([f" {i}  " for i in range(size)])
        print(header)
        
        # 分隔线
        separator = "   " + "+" + "---+" * size
        print(separator)
        
        # 绘制每一行
        for i, row in enumerate(plots):
            row_display = f" {i} |"
            for plot in row:
                # 获取显示图标
                icon = self._get_plot_icon(plot)
                row_display += f" {icon}|"
            
            print(row_display)
            print(separator)
        
        print()
    
    def _get_plot_icon(self, plot) -> str:
        """
        获取地块的显示图标
        
        Args:
            plot: 地块对象
            
        Returns:
            str: 显示图标
        """
        if plot.is_empty():
            return "⬜"
        
        crop = plot.crop
        
        if plot.is_mature():
            return f"{crop.emoji}✨"
        
        # 根据生长阶段显示不同图标
        stage = plot.growth_stage
        
        if stage == 0:
            return "🌱 "
        elif stage == 1:
            return "🌿 "
        elif stage == 2:
            return "🪴 "
        elif stage == 3:
            return f"{crop.emoji} "
        else:
            return f"{crop.emoji} "
    
    # ========== 玩家状态显示 ==========
    
    def show_player_status(self) -> None:
        """显示玩家状态信息"""
        player = self.game.player
        
        print("-" * 60)
        print(f"👤 农夫: {player.name}")
        print(f"💰 金币: {player.money}")
        
        # 显示种子
        if player.seeds:
            seeds_str = " | ".join([f"{name}: {count}" for name, count in player.seeds.items()])
            print(f"🌱 种子: {seeds_str}")
        
        # 显示收获物
        if player.inventory:
            inv_str = " | ".join([f"{name}: {count}" for name, count in player.inventory.items()])
            print(f"📦 仓库: {inv_str}")
        
        # 农场等级
        level = player.upgrade_level + 1
        print(f"🏘️ 农场等级: Lv.{level}")
        
        print("-" * 60)
    
    # ========== 消息显示 ==========
    
    def show_messages(self, messages: List[str]) -> None:
        """
        显示消息列表
        
        Args:
            messages: 消息列表
        """
        if not messages:
            return
        
        print("\n" + "=" * 60)
        print("📜 消息日志")
        print("=" * 60)
        
        for msg in messages:
            print(f"  {msg}")
        
        print("=" * 60 + "\n")
    
    # ========== 菜单显示 ==========
    
    def show_main_menu(self) -> None:
        """显示主菜单"""
        print("\n🎮 操作菜单:")
        print("  [1] 🌱 种植    [2] 💧 浇水    [3] 🎒 收获")
        print("  [4] 🛒 商店    [5] 💰 出售    [6] 🛏️ 睡觉(下一天)")
        print("  [7] 📊 详情    [8] 🏆 成就    [9] 💾 存档")
        print("  [0] 🚪 退出游戏")
        print("-" * 60)
    
    def show_shop_menu(self) -> None:
        """显示商店菜单"""
        season = self.game.get_current_season()
        
        print("\n" + "=" * 60)
        print(f"{'🏪 皮埃尔杂货店':^56}")
        print("=" * 60)
        
        print(f"\n{'当前季节: ' + season.value:^56}\n")
        
        print(f"{'作物':<8} | {'种子价':<6} | {'售价':<6} | {'周期':<6} | {'利润':<6} | {'状态':<6}")
        print("-" * 60)
        
        crops = self.game.economy_system.get_all_crops()
        
        for i, crop in enumerate(crops, 1):
            can_plant = crop.can_plant_in_season(season)
            status = "✅ 可种" if can_plant else "❌ 非季"
            
            print(
                f"{i}. {crop.emoji} {crop.name:<4} | "
                f"{crop.seed_price:<6}金 | "
                f"{crop.sell_price:<6}金 | "
                f"{crop.grow_days:<6}天 | "
                f"{crop.get_profit():<6}金 | "
                f"{status}"
            )
        
        print("-" * 60)
        print(f"{'[0] 返回主菜单':^56}")
        print("=" * 60)
    
    def show_plant_menu(self) -> None:
        """显示种植菜单"""
        print("\n" + "=" * 60)
        print(f"{'🌱 种植作物':^56}")
        print("=" * 60)
        
        if not self.game.player.seeds:
            print("\n  你没有种子！请先去商店购买。\n")
        else:
            print("\n  你拥有的种子:")
            for name, count in self.game.player.seeds.items():
                crop = self.game.economy_system.get_crop(name)
                emoji = crop.emoji if crop else "🌱"
                print(f"    {emoji} {name}: {count} 个")
        
        print("\n  输入格式: [行号] [列号] [作物名]")
        print("  示例: 0 0 土豆")
        print("-" * 60)
        print(f"{'[0] 返回主菜单':^56}")
        print("=" * 60)
    
    def show_sell_menu(self) -> None:
        """显示出售菜单"""
        print("\n" + "=" * 60)
        print(f"{'💰 出售作物':^56}")
        print("=" * 60)
        
        if not self.game.player.inventory:
            print("\n  你的仓库空空如也！\n")
        else:
            print("\n  仓库中的作物:")
            total_value = 0
            
            for name, count in self.game.player.inventory.items():
                crop = self.game.economy_system.get_crop(name)
                if crop:
                    value = crop.sell_price * count
                    total_value += value
                    print(f"    {crop.emoji} {name}: {count} 个 (价值: {value}金)")
            
            print(f"\n  总价值: {total_value} 金币")
        
        print("\n  输入格式: [作物名] [数量] (数量输入 'all' 全部出售)")
        print("  示例: 土豆 5  或  土豆 all")
        print("-" * 60)
        print(f"{'[0] 返回主菜单':^56}")
        print("=" * 60)
    
    def show_achievements(self) -> None:
        """显示成就列表"""
        ach_manager = self.game.achievement_manager
        
        print("\n" + "=" * 60)
        print(f"{'🏆 成就系统':^56}")
        print("=" * 60)
        
        print(f"\n  完成度: {ach_manager.get_unlocked_count()}/{ach_manager.get_total_count()}")
        print("-" * 60)
        
        for ach in ach_manager.get_all_achievements():
            if ach.unlocked:
                print(f"  ✅ {ach.name}")
                print(f"     └─ {ach.description}")
            else:
                progress = ach.get_progress_bar(10)
                print(f"  ⬜ {ach.name}")
                print(f"     └─ {ach.condition} [{progress}]")
        
        print("=" * 60)
        print(f"{'[回车键] 返回主菜单':^56}")
        print("=" * 60)
    
    def show_detail_menu(self) -> None:
        """显示详情查询菜单"""
        print("\n" + "=" * 60)
        print(f"{'📊 信息详情':^56}")
        print("=" * 60)
        print("  [1] 查看作物详情")
        print("  [2] 查看农田状态")
        print("  [3] 查看统计信息")
        print("  [0] 返回主菜单")
        print("=" * 60)
    
    def show_crop_detail(self, crop_name: str) -> None:
        """显示作物详细信息"""
        crop = self.game.economy_system.get_crop(crop_name)
        
        if not crop:
            print(f"\n  ❌ 没有找到作物: {crop_name}\n")
            return
        
        print("\n" + "=" * 60)
        print(f"{crop.emoji} {crop.name}")
        print("=" * 60)
        print(f"  种子价格: {crop.seed_price} 金币")
        print(f"  出售价格: {crop.sell_price} 金币")
        print(f"  利润: {crop.get_profit()} 金币")
        print(f"  生长周期: {crop.grow_days} 天")
        print(f"  适宜季节: {crop.get_seasons_str()}")
        print(f"  投资回报率: {crop.get_roi()}%")
        print(f"  日均收益: {crop.get_profit_per_day()} 金币/天")
        print("=" * 60)
    
    def show_statistics(self) -> None:
        """显示统计数据"""
        stats = self.game.player.stats
        
        print("\n" + "=" * 60)
        print(f"{'📊 农场统计':^56}")
        print("=" * 60)
        print(f"  游戏天数: {stats.days_played} 天")
        print(f"  总收获数: {stats.total_harvested} 个")
        print(f"  累计收入: {stats.total_earnings} 金币")
        print(f"  累计支出: {stats.total_spent} 金币")
        print(f"  净利润: {stats.total_earnings - stats.total_spent} 金币")
        print(f"  最高持有: {stats.max_money_held} 金币")
        print(f"  种植种类: {stats.get_crops_grown_count()} 种")
        print(f"  单日最多: {stats.single_day_harvest} 个")
        print("=" * 60)
    
    def show_plot_status(self, row: int, col: int) -> None:
        """显示指定地块的状态"""
        plot = self.game.get_plot(row, col)
        
        if not plot:
            print(f"\n  ❌ 无效的坐标: ({row}, {col})\n")
            return
        
        print(f"\n  地块 ({row}, {col}): {plot.get_status_text()}\n")
    
    def show_goodbye(self) -> None:
        """显示告别信息"""
        print("\n" + "=" * 60)
        print(f"{'👋 感谢游玩文字农场！':^56}")
        print(f"{'期待你的下次光临！':^56}")
        print("=" * 60 + "\n")
    
    def show_input_prompt(self, prompt: str = "请选择操作") -> str:
        """
        显示输入提示并获取用户输入
        
        Args:
            prompt: 提示文本
            
        Returns:
            str: 用户输入
        """
        return input(f"\n👉 {prompt}: ").strip()
