"""
游戏管理器模块
整合所有游戏系统，提供统一的游戏接口
"""

import random
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass

from config.settings import (
    Season, Weather, GameConfig, CropData, AchievementData
)
from models import Crop, Plot, Player, PlayerStats, Achievement, AchievementManager
from core.time_system import TimeSystem
from core.economy import EconomySystem
from core.event_system import EventSystem


@dataclass
class DayResult:
    """
    一天结束时的结果数据
    """
    day: int
    season: str
    weather: str
    crops_grown: int          # 生长的作物数
    crops_matured: int        # 成熟的作物数
    crops_died: int           # 枯萎的作物数
    crops_destroyed: int      # 被暴风雨摧毁的作物数
    events: List[str]         # 发生的事件列表


class GameManager:
    """
    游戏管理器类
    
    整合所有游戏子系统，提供统一的游戏操作接口
    """
    
    def __init__(self):
        """初始化游戏管理器"""
        # 核心系统
        self.time_system = TimeSystem()
        self.economy_system = EconomySystem()
        self.achievement_manager = AchievementManager()
        self.event_system = EventSystem()  # 事件系统
        
        # 玩家数据
        self.player = Player()
        
        # 农田数据
        self.plots: List[List[Plot]] = []
        self._init_plots()
        
        # 初始化成就
        self._init_achievements()
        
        # 游戏状态
        self.is_running = True
        self.messages: List[str] = []  # 消息队列
        
        # 自动运行机制
        self.auto_run = True  # 自动运行开关
        self.last_auto_advance = 0  # 上次自动推进时间
        self.auto_advance_interval = 30  # 自动推进间隔（秒）
    
    def _init_plots(self) -> None:
        """初始化农田"""
        size = self.player.get_plot_size()
        self.plots = [[Plot() for _ in range(size)] for _ in range(size)]
    
    def _init_achievements(self) -> None:
        """
        初始化成就系统
        
        遍历所有成就数据，创建成就对象并添加到成就管理器中
        """
        for achievement_id, achievement_data in AchievementData.ACHIEVEMENTS.items():
            achievement = Achievement(
                id=achievement_id,
                name=achievement_data["name"],
                description=achievement_data["description"],
                condition=achievement_data["condition"],
                reward_text=achievement_data["reward_text"],
            )
            
            # 设置进度目标
            condition = achievement_data["condition"]
            if ">=" in condition:
                parts = condition.split(">=")
                if len(parts) == 2:
                    try:
                        target = int(parts[1].strip())
                        achievement.progress_target = target
                    except ValueError:
                        pass
            
            self.achievement_manager.add_achievement(achievement)
    
    def _rebuild_plots(self, old_size: int, new_size: int) -> None:
        """
        重建农田（升级时保留原有作物）

        Args:
            old_size: 原有农田大小
            new_size: 新农田大小
        """
        try:
            old_plots = self.plots
            self.plots = [[Plot() for _ in range(new_size)] for _ in range(new_size)]
            
            # 复制原有作物
            for i in range(min(old_size, new_size)):
                for j in range(min(old_size, new_size)):
                    if i < len(old_plots) and j < len(old_plots[i]):
                        self.plots[i][j] = old_plots[i][j]
        except Exception as e:
            # 发生错误时，确保至少有一个有效的地块矩阵
            self.plots = [[Plot() for _ in range(max(old_size, 1))] for _ in range(max(old_size, 1))]
    
    # ========== 时间相关 ==========
    
    def get_current_date(self) -> str:
        """获取当前日期字符串"""
        return self.time_system.get_date_string()
    
    def get_current_season(self) -> Season:
        """获取当前季节"""
        return self.time_system.season
    
    def get_current_weather(self) -> Weather:
        """获取当前天气"""
        return self.time_system.weather
    
    def get_weather_description(self) -> str:
        """获取天气效果描述"""
        return self.time_system.get_weather_effect_description()
    
    # ========== 农田操作 ==========
    
    def get_plot(self, row: int, col: int) -> Optional[Plot]:
        """
        获取指定位置的地块
        
        Args:
            row: 行号
            col: 列号
            
        Returns:
            Optional[Plot]: 地块对象，无效位置返回None
        """
        if 0 <= row < len(self.plots) and 0 <= col < len(self.plots[0]):
            return self.plots[row][col]
        return None
    
    def get_plot_size(self) -> int:
        """获取农田大小"""
        return len(self.plots)
    
    def get_total_plots(self) -> int:
        """获取总地块数"""
        return len(self.plots) * len(self.plots[0])
    
    def get_used_plots(self) -> int:
        """获取已使用的地块数"""
        count = 0
        for row in self.plots:
            for plot in row:
                if not plot.is_empty():
                    count += 1
        return count
    
    def get_mature_plots_count(self) -> int:
        """获取成熟可收获的地块数"""
        count = 0
        for row in self.plots:
            for plot in row:
                if plot.is_mature():
                    count += 1
        return count
    
    # ========== 种植系统 ==========
    
    def plant_crop(self, row: int, col: int, crop_name: str) -> Tuple[bool, str]:
        """
        在指定位置种植作物
        
        Args:
            row: 行号
            col: 列号
            crop_name: 作物名称
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 检查位置是否有效
        plot = self.get_plot(row, col)
        if plot is None:
            return False, "❌ 无效的位置！"
        
        # 检查地块是否为空
        if not plot.is_empty():
            return False, f"❌ 这块地已经有作物了！"
        
        # 检查是否有种子
        if not self.player.has_seeds(crop_name):
            return False, f"❌ 你没有 {crop_name} 的种子！"
        
        # 获取作物数据
        crop = self.economy_system.get_crop(crop_name)
        if crop is None:
            return False, f"❌ 没有名为「{crop_name}」的作物！"
        
        # 检查季节是否适宜
        current_season = self.get_current_season()
        if not crop.can_plant_in_season(current_season):
            return False, f"❌ {crop_name} 不能在{current_season.value}种植！"
        
        # 执行种植
        self.player.remove_seeds(crop_name)
        plot.plant(crop, self.time_system.day)
        self.player.stats.add_crop_grown(crop_name)
        
        return True, f"✅ 成功种植 {crop.emoji} {crop_name}！"
    
    def water_plot(self, row: int, col: int) -> Tuple[bool, str]:
        """
        给指定地块浇水
        
        Args:
            row: 行号
            col: 列号
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 检查天气是否自动浇水
        if self.time_system.is_rainy():
            return False, "🌧️ 今天下雨，作物自动获得水分！"
        
        # 检查位置是否有效
        plot = self.get_plot(row, col)
        if plot is None:
            return False, "❌ 无效的位置！"
        
        # 检查是否有作物
        if plot.is_empty():
            return False, "❌ 这块地没有作物！"
        
        # 检查是否已浇水
        if plot.watered_today:
            return False, "💧 这块地今天已经浇过水了！"
        
        # 执行浇水
        plot.water()
        crop = plot.crop
        
        return True, f"💧 给 {crop.emoji} {crop.name} 浇水成功！"
    
    def water_all_plots(self) -> Tuple[int, int]:
        """
        给所有需要浇水的地块浇水
        
        Returns:
            Tuple[int, int]: (成功数量, 失败数量)
        """
        # 检查天气
        if self.time_system.is_rainy():
            return 0, 0
        
        success = 0
        failed = 0
        
        for row in self.plots:
            for plot in row:
                if not plot.is_empty() and not plot.watered_today and not plot.is_mature():
                    plot.water()
                    success += 1
        
        return success, failed
    
    def harvest_plot(self, row: int, col: int) -> Tuple[bool, str]:
        """
        收获指定地块的作物
        
        Args:
            row: 行号
            col: 列号
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 检查位置是否有效
        plot = self.get_plot(row, col)
        if plot is None:
            return False, "❌ 无效的位置！"
        
        # 检查是否有作物
        if plot.is_empty():
            return False, "❌ 这块地没有作物！"
        
        # 检查是否成熟
        if not plot.is_mature():
            progress = int(plot.get_growth_progress() * 100)
            return False, f"⏳ {plot.crop.emoji} {plot.crop.name} 还没成熟！进度: {progress}%"
        
        # 执行收获
        crop = plot.harvest()
        self.player.add_to_inventory(crop.name)
        
        # 更新成就进度
        self._update_harvest_achievements()
        
        return True, f"🎉 收获了 {crop.emoji} {crop.name}！"
    
    def harvest_all_mature(self) -> Tuple[int, List[str]]:
        """
        收获所有成熟的作物
        
        Returns:
            Tuple[int, List[str]]: (收获数量, 消息列表)
        """
        harvested = 0
        messages = []
        
        for i, row in enumerate(self.plots):
            for j, plot in enumerate(row):
                if plot.is_mature():
                    crop = plot.harvest()
                    self.player.add_to_inventory(crop.name)
                    harvested += 1
                    messages.append(f"🎉 [{i},{j}] 收获了 {crop.emoji} {crop.name}！")
        
        if harvested > 0:
            self._update_harvest_achievements()
        
        return harvested, messages
    
    # ========== 时间推进 ==========
    
    def advance_day(self) -> DayResult:
        """
        推进一天，处理所有日常事件

        Returns:
            DayResult: 当天结果数据
        """
        try:
            result = DayResult(
                day=self.time_system.day,
                season=self.time_system.season.value,
                weather=self.time_system.weather.value,
                crops_grown=0,
                crops_matured=0,
                crops_died=0,
                crops_destroyed=0,
                events=[]
            )
            
            # 玩家新的一天
            self.player.new_day()
            
            # 处理天气效果
            is_rainy = self.time_system.is_rainy()
            is_stormy = self.time_system.is_stormy()
            
            # 遍历所有地块
            for row in self.plots:
                for plot in row:
                    try:
                        if plot.is_empty():
                            continue
                        
                        crop = plot.crop
                        
                        # 检查季节是否适宜
                        if not crop.can_plant_in_season(self.time_system.season):
                            plot.clear()
                            result.crops_died += 1
                            result.events.append(f"💀 {crop.emoji} {crop.name} 因季节变换而枯萎")
                            continue
                        
                        # 雨天自动浇水
                        if is_rainy:
                            plot.force_water()
                        
                        # 暴风雨可能摧毁作物
                        if is_stormy and random.random() < GameConfig.STORM_DAMAGE_CHANCE:
                            plot.clear()
                            result.crops_destroyed += 1
                            result.events.append(f"⛈️ {crop.emoji} {crop.name} 被暴风雨摧毁")
                            continue
                        
                        # 作物生长
                        was_growing = plot.is_growing()
                        old_stage = plot.growth_stage
                        
                        if plot.watered_today:
                            plot.grow()
                            result.crops_grown += 1
                            
                            # 检查是否新成熟
                            if old_stage < 4 and plot.is_mature():
                                result.crops_matured += 1
                                result.events.append(f"🌿 {crop.emoji} {crop.name} 成熟了！")
                        
                        # 重置浇水状态（非雨天）
                        if not is_rainy:
                            plot.reset_water_status()
                    except Exception as e:
                        # 单个地块处理失败不影响其他地块
                        result.events.append(f"⚠️ 处理地块时出错: {str(e)}")
            
            # 推进时间
            time_events = self.time_system.advance_day()
            
            # 处理时间事件
            if time_events["new_season"]:
                result.events.append(f"🍂 季节变换：进入{time_events['season_changed_to'].value}！")
            
            if time_events["new_year"]:
                result.events.append(f"🎉 新年快乐！现在是第{self.time_system.year}年！")
            
            # 检查成就
            self._check_achievements()
            
            # 检查事件
            event_messages = self.event_system.check_events(self)
            for message in event_messages:
                result.events.append(f"📅 {message}")
            
            # 自动保存
            if self.time_system.day % GameConfig.AUTO_SAVE_INTERVAL == 0:
                result.events.append("💾 游戏已自动保存")
            
            return result
        except Exception as e:
            # 发生严重错误时，返回一个基本的结果对象
            return DayResult(
                day=self.time_system.day,
                season=self.time_system.season.value,
                weather=self.time_system.weather.value,
                crops_grown=0,
                crops_matured=0,
                crops_died=0,
                crops_destroyed=0,
                events=[f"❌ 推进日期时出错: {str(e)}"]
            )
    
    # ========== 商店与交易 ==========
    
    def buy_seeds(self, crop_name: str, quantity: int = 1) -> Tuple[bool, str]:
        """
        购买种子
        
        Args:
            crop_name: 作物名称
            quantity: 数量
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = self.economy_system.buy_seeds(self.player, crop_name, quantity)
        return result.success, result.message
    
    def sell_crop(self, crop_name: str, quantity: int = 1) -> Tuple[bool, str]:
        """
        出售作物
        
        Args:
            crop_name: 作物名称
            quantity: 数量
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = self.economy_system.sell_crop(self.player, crop_name, quantity)
        
        if result.success:
            self._check_achievements()
        
        return result.success, result.message
    
    def sell_all_crops(self) -> List[Tuple[bool, str]]:
        """
        出售所有作物
        
        Returns:
            List[Tuple[bool, str]]: 交易结果列表
        """
        results = self.economy_system.sell_all_crops(self.player)
        self._check_achievements()
        return [(r.success, r.message) for r in results]
    
    # ========== 农场升级 ==========
    
    def can_upgrade_farm(self) -> bool:
        """检查是否可以升级农场"""
        return self.player.can_upgrade()
    
    def get_upgrade_cost(self) -> int:
        """获取升级费用"""
        return self.player.get_upgrade_cost()
    
    def upgrade_farm(self) -> Tuple[bool, str]:
        """
        升级农场
        
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        if not self.player.can_upgrade():
            return False, "❌ 农场已达最高等级！"
        
        cost = self.player.get_upgrade_cost()
        
        if not self.player.can_afford(cost):
            return False, f"❌ 金币不足！升级需要 {cost} 金币。"
        
        old_size = self.player.get_plot_size()
        
        if not self.player.upgrade_farm():
            return False, "❌ 升级失败！"
        
        new_size = self.player.get_plot_size()
        self._rebuild_plots(old_size, new_size)
        
        # 检查升级成就
        self._check_achievements()
        
        return True, f"✅ 农场升级成功！田地扩大到 {new_size}x{new_size}！"
    
    # ========== 成就系统 ==========
    
    def _update_harvest_achievements(self) -> None:
        """更新收获相关成就进度"""
        total = self.player.stats.total_harvested
        
        # 更新进度
        self.achievement_manager.set_achievement_progress("first_harvest", total)
        self.achievement_manager.set_achievement_progress("farmer_100", total)
        self.achievement_manager.set_achievement_progress("farmer_500", total)
        self.achievement_manager.set_achievement_progress("farmer_1000", total)
    
    def _check_achievements(self) -> None:
        """检查所有成就"""
        stats = self.player.stats
        
        # 收获成就
        if stats.total_harvested >= 1:
            self._try_unlock_achievement("first_harvest", stats.total_harvested)
        if stats.total_harvested >= 100:
            self._try_unlock_achievement("farmer_100", stats.total_harvested)
        if stats.total_harvested >= 500:
            self._try_unlock_achievement("farmer_500", stats.total_harvested)
        if stats.total_harvested >= 1000:
            self._try_unlock_achievement("farmer_1000", stats.total_harvested)
        
        # 财富成就
        if stats.total_earnings >= 1000000:
            self._try_unlock_achievement("millionaire", stats.total_earnings)
        
        # 作物收集成就
        crops_count = stats.get_crops_grown_count()
        if crops_count >= 12:
            self._try_unlock_achievement("all_crops", crops_count)
        
        # 四季成就
        if self.time_system.year > 1:
            self._try_unlock_achievement("survive_year", self.time_system.year)
        
        # 农场等级成就
        if self.player.upgrade_level >= 4:
            self._try_unlock_achievement("max_farm", self.player.upgrade_level)
        
        # 单日收获成就
        if stats.single_day_harvest >= 10:
            self._try_unlock_achievement("rich_harvest", stats.single_day_harvest)
    
    def _try_unlock_achievement(self, achievement_id: str, current_value: int) -> bool:
        """
        尝试解锁成就
        
        Args:
            achievement_id: 成就ID
            current_value: 当前进度值
            
        Returns:
            bool: 是否新解锁
        """
        achievement = self.achievement_manager.get_achievement(achievement_id)
        
        if achievement is None or achievement.unlocked:
            return False
        
        # 更新进度
        achievement.set_progress(current_value)
        
        # 尝试解锁
        if self.achievement_manager.unlock_achievement(achievement_id):
            # 同步到玩家数据
            self.player.unlock_achievement(achievement_id)
            self.messages.append(f"🏆 解锁成就：{achievement.name}")
            return True
        
        return False
    
    def get_new_messages(self) -> List[str]:
        """获取并清空消息队列"""
        messages = self.messages.copy()
        self.messages.clear()
        return messages
    
    # ========== 游戏状态 ==========
    
    def get_game_summary(self) -> Dict:
        """
        获取游戏状态摘要

        Returns:
            Dict: 游戏状态字典
        """
        return {
            "date": self.get_current_date(),
            "year": self.time_system.year,
            "season": self.time_system.season.value,
            "weather": self.time_system.weather.value,
            "money": self.player.money,
            "total_earnings": self.player.stats.total_earnings,
            "total_harvested": self.player.stats.total_harvested,
            "plot_size": self.get_plot_size(),
            "upgrade_level": self.player.upgrade_level,
            "achievements": self.achievement_manager.get_unlocked_count(),
            "total_achievements": self.achievement_manager.get_total_count(),
        }
    
    def check_auto_advance(self, current_time: float) -> Optional[DayResult]:
        """
        检查是否需要自动推进时间

        Args:
            current_time: 当前时间（秒）

        Returns:
            Optional[DayResult]: 如果自动推进了时间，返回推进结果；否则返回None
        """
        if not self.auto_run:
            return None
        
        # 检查是否达到自动推进间隔
        if current_time - self.last_auto_advance >= self.auto_advance_interval:
            self.last_auto_advance = current_time
            return self.advance_day()
        
        return None
    
    def __str__(self) -> str:
        return f"GameManager({self.get_current_date()})"
    
    def __repr__(self) -> str:
        return f"GameManager(day={self.time_system.day}, money={self.player.money})"
