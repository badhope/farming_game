"""
存档管理模块
处理游戏的保存和读取功能
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import asdict

from config.settings import GameConfig, Season, Weather
from core.game_manager import GameManager


class SaveManager:
    """
    存档管理类
    
    负责游戏数据的序列化、反序列化及文件读写
    """
    
    def __init__(self, save_dir: str = "."):
        """
        初始化存档管理器
        
        Args:
            save_dir: 存档文件保存目录
        """
        self.save_dir = save_dir
        self.save_path = os.path.join(save_dir, GameConfig.SAVE_FILENAME)
    
    def save_game(self, game: GameManager) -> bool:
        """
        保存游戏
        
        Args:
            game: 游戏管理器实例
            
        Returns:
            bool: 是否保存成功
        """
        try:
            # 构建存档数据结构
            save_data = {
                "meta": {
                    "version": "1.0.0",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "game_name": "Python Text Farm"
                },
                "time": self._serialize_time(game),
                "player": self._serialize_player(game),
                "plots": self._serialize_plots(game),
                "achievements": self._serialize_achievements(game),
            }
            
            # 写入文件
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=4)
            
            return True
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False
    
    def load_game(self, game: GameManager) -> bool:
        """
        读取游戏
        
        Args:
            game: 要加载数据的游戏管理器实例
            
        Returns:
            bool: 是否读取成功
        """
        if not self.has_save():
            return False
        
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # 加载各部分数据
            self._deserialize_time(game, save_data.get("time", {}))
            self._deserialize_player(game, save_data.get("player", {}))
            self._deserialize_plots(game, save_data.get("plots", []))
            self._deserialize_achievements(game, save_data.get("achievements", {}))
            
            return True
            
        except Exception as e:
            print(f"❌ 读取失败: {e}")
            return False
    
    def has_save(self) -> bool:
        """
        检查是否存在存档文件
        
        Returns:
            bool: 是否存在存档
        """
        return os.path.exists(self.save_path)
    
    def get_save_info(self) -> Optional[Dict[str, str]]:
        """
        获取存档信息（不加载完整游戏）
        
        Returns:
            Optional[Dict]: 存档元数据，不存在返回None
        """
        if not self.has_save():
            return None
        
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            meta = save_data.get("meta", {})
            player = save_data.get("player", {})
            time_data = save_data.get("time", {})
            
            return {
                "timestamp": meta.get("timestamp", "未知时间"),
                "version": meta.get("version", "未知版本"),
                "player_name": player.get("name", "农夫"),
                "money": player.get("money", 0),
                "year": time_data.get("year", 1),
                "season": time_data.get("season", "SPRING"),
                "day": time_data.get("day", 1),
            }
        except:
            return None
    
    def delete_save(self) -> bool:
        """
        删除存档
        
        Returns:
            bool: 是否删除成功
        """
        if not self.has_save():
            return False
        
        try:
            os.remove(self.save_path)
            return True
        except Exception as e:
            print(f"❌ 删除存档失败: {e}")
            return False
    
    # ========== 序列化方法 ==========
    
    def _serialize_time(self, game: GameManager) -> Dict:
        """序列化时间系统"""
        return {
            "year": game.time_system.year,
            "day": game.time_system.day,
            "season": game.time_system.season.name,
            "weather": game.time_system.weather.name,
            "tomorrow_weather": game.time_system.tomorrow_weather.name if game.time_system.tomorrow_weather else None,
        }
    
    def _serialize_player(self, game: GameManager) -> Dict:
        """序列化玩家数据"""
        player = game.player
        stats = player.stats
        
        return {
            "name": player.name,
            "money": player.money,
            "inventory": player.inventory,
            "seeds": player.seeds,
            "upgrade_level": player.upgrade_level,
            "unlocked_achievements": player.unlocked_achievements,
            "stats": {
                "total_harvested": stats.total_harvested,
                "total_earnings": stats.total_earnings,
                "total_spent": stats.total_spent,
                "crops_grown": list(stats.crops_grown),  # Set转List
                "days_played": stats.days_played,
                "max_money_held": stats.max_money_held,
                "storm_survived": stats.storm_survived,
                "single_day_harvest": stats.single_day_harvest,
            }
        }
    
    def _serialize_plots(self, game: GameManager) -> list:
        """序列化农田数据"""
        plots_data = []
        
        for row in game.plots:
            row_data = []
            for plot in row:
                if plot.is_empty():
                    row_data.append({"empty": True})
                else:
                    row_data.append({
                        "empty": False,
                        "crop_name": plot.crop.name,
                        "planted_day": plot.planted_day,
                        "growth_stage": plot.growth_stage,
                        "days_watered": plot.days_watered,
                        # 注意：watered_today 不需要保存，每天开始会重置
                    })
            plots_data.append(row_data)
        
        return plots_data
    
    def _serialize_achievements(self, game: GameManager) -> Dict:
        """序列化成就数据"""
        achievements_data = {}
        
        for ach_id, achievement in game.achievement_manager.achievements.items():
            achievements_data[ach_id] = {
                "unlocked": achievement.unlocked,
                "unlocked_date": achievement.unlocked_date,
                "progress_current": achievement.progress_current,
            }
        
        return achievements_data
    
    # ========== 反序列化方法 ==========
    
    def _deserialize_time(self, game: GameManager, data: Dict) -> None:
        """反序列化时间系统"""
        game.time_system.year = data.get("year", 1)
        game.time_system.day = data.get("day", 1)
        
        season_str = data.get("season", "SPRING")
        game.time_system.season = Season[season_str]
        
        weather_str = data.get("weather", "SUNNY")
        game.time_system.weather = Weather[weather_str]
        
        tomorrow_str = data.get("tomorrow_weather")
        game.time_system.tomorrow_weather = Weather[tomorrow_str] if tomorrow_str else None
    
    def _deserialize_player(self, game: GameManager, data: Dict) -> None:
        """反序列化玩家数据"""
        player = game.player
        
        player.name = data.get("name", "农夫")
        player.money = data.get("money", GameConfig.INITIAL_MONEY)
        player.inventory = data.get("inventory", {})
        player.seeds = data.get("seeds", {})
        player.upgrade_level = data.get("upgrade_level", 0)
        player.unlocked_achievements = data.get("unlocked_achievements", [])
        
        # 恢复统计数据
        stats_data = data.get("stats", {})
        stats = player.stats
        
        stats.total_harvested = stats_data.get("total_harvested", 0)
        stats.total_earnings = stats_data.get("total_earnings", 0)
        stats.total_spent = stats_data.get("total_spent", 0)
        stats.crops_grown = set(stats_data.get("crops_grown", []))  # List转Set
        stats.days_played = stats_data.get("days_played", 0)
        stats.max_money_held = stats_data.get("max_money_held", 0)
        stats.storm_survived = stats_data.get("storm_survived", False)
        stats.single_day_harvest = stats_data.get("single_day_harvest", 0)
    
    def _deserialize_plots(self, game: GameManager, data: list) -> None:
        """反序列化农田数据"""
        # 根据存档重新调整农田大小
        # 注意：这里需要根据玩家等级重建农田，而不是直接用存档的大小
        # 但如果存档数据异常，需要处理
        
        # 先确保农田大小正确
        correct_size = game.player.get_plot_size()
        
        # 如果存档大小与玩家等级不符，需要重新初始化
        # 这里简单处理：重新生成农田
        game._init_plots()
        
        # 填充作物数据
        for i, row_data in enumerate(data):
            if i >= correct_size:
                break  # 防止越界
            
            for j, plot_data in enumerate(row_data):
                if j >= correct_size:
                    break
                
                if not plot_data.get("empty", True):
                    crop_name = plot_data.get("crop_name")
                    crop = game.economy_system.get_crop(crop_name)
                    
                    if crop:
                        # 恢复作物状态
                        game.plots[i][j].crop = crop
                        game.plots[i][j].planted_day = plot_data.get("planted_day", 0)
                        game.plots[i][j].growth_stage = plot_data.get("growth_stage", 0)
                        game.plots[i][j].days_watered = plot_data.get("days_watered", 0)
                        game.plots[i][j].watered_today = False  # 重置浇水状态
    
    def _deserialize_achievements(self, game: GameManager, data: Dict) -> None:
        """反序列化成就数据"""
        for ach_id, ach_data in data.items():
            achievement = game.achievement_manager.get_achievement(ach_id)
            
            if achievement:
                if ach_data.get("unlocked", False):
                    achievement.unlocked = True
                    achievement.unlocked_date = ach_data.get("unlocked_date")
                    achievement.progress_current = achievement.progress_target
                else:
                    achievement.progress_current = ach_data.get("progress_current", 0)
    
    def __str__(self) -> str:
        return f"SaveManager(path='{self.save_path}')"
    
    def __repr__(self) -> str:
        return self.__str__()
