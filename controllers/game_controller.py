"""
游戏控制器模块
处理游戏逻辑和UI之间的协调，提供统一的操作接口
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
from typing import Callable, Optional

from core.game_manager import GameManager
from systems.save_manager import SaveManager


class GameController:
    """
    游戏控制器类
    负责协调游戏逻辑、数据管理和UI更新
    """
    
    def __init__(self, game_manager: GameManager, save_manager: SaveManager):
        """
        初始化游戏控制器
        
        Args:
            game_manager: 游戏管理器实例
            save_manager: 存档管理器实例
        """
        self.game_manager = game_manager
        self.save_manager = save_manager
        self.ui_callback: Optional[Callable] = None
        self.is_paused = False
        self.auto_save_enabled = True
    
    def set_ui_callback(self, callback: Callable):
        """
        设置UI更新回调函数
        
        Args:
            callback: UI更新函数
        """
        self.ui_callback = callback
    
    def start_game(self) -> bool:
        """
        开始游戏
        
        Returns:
            bool: 是否成功启动
        """
        try:
            # 初始化游戏数据
            self.game_manager.__init__()
            self._trigger_ui_update()
            return True
        except Exception as e:
            print(f"启动游戏失败: {e}")
            return False
    
    def load_game(self) -> bool:
        """
        加载游戏存档
        
        Returns:
            bool: 是否成功加载
        """
        try:
            if not self.save_manager.has_save():
                return False
            
            success = self.save_manager.load_game(self.game_manager)
            if success:
                self._trigger_ui_update()
            return success
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return False
    
    def save_game(self) -> bool:
        """
        保存游戏
        
        Returns:
            bool: 是否成功保存
        """
        try:
            return self.save_manager.save_game(self.game_manager)
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False
    
    # ========== 农田操作 ==========
    
    def plant_crop(self, row: int, col: int, crop_name: str) -> tuple[bool, str]:
        """
        种植作物
        
        Args:
            row: 行号
            col: 列号
            crop_name: 作物名称
            
        Returns:
            tuple[bool, str]: (是否成功, 消息)
        """
        if self.is_paused:
            return False, "⚠️ 游戏已暂停！"
        
        success, message = self.game_manager.plant_crop(row, col, crop_name)
        if success:
            self._trigger_ui_update()
        return success, message
    
    def water_plot(self, row: int, col: int) -> tuple[bool, str]:
        """
        给地块浇水
        
        Args:
            row: 行号
            col: 列号
            
        Returns:
            tuple[bool, str]: (是否成功, 消息)
        """
        if self.is_paused:
            return False, "⚠️ 游戏已暂停！"
        
        success, message = self.game_manager.water_plot(row, col)
        if success:
            self._trigger_ui_update()
        return success, message
    
    def water_all_plots(self) -> tuple[int, int]:
        """
        给所有地块浇水
        
        Returns:
            tuple[int, int]: (成功数量, 失败数量)
        """
        if self.is_paused:
            return 0, 0
        
        success, failed = self.game_manager.water_all_plots()
        if success > 0:
            self._trigger_ui_update()
        return success, failed
    
    def harvest_plot(self, row: int, col: int) -> tuple[bool, str]:
        """
        收获地块作物
        
        Args:
            row: 行号
            col: 列号
            
        Returns:
            tuple[bool, str]: (是否成功, 消息)
        """
        if self.is_paused:
            return False, "⚠️ 游戏已暂停！"
        
        success, message = self.game_manager.harvest_plot(row, col)
        if success:
            self._trigger_ui_update()
        return success, message
    
    def harvest_all_mature(self) -> tuple[int, list[str]]:
        """
        收获所有成熟作物
        
        Returns:
            tuple[int, list[str]]: (收获数量, 消息列表)
        """
        if self.is_paused:
            return 0, []
        
        count, messages = self.game_manager.harvest_all_mature()
        if count > 0:
            self._trigger_ui_update()
        return count, messages
    
    # ========== 商店与经济 ==========
    
    def buy_seeds(self, crop_name: str, quantity: int = 1) -> tuple[bool, str]:
        """
        购买种子
        
        Args:
            crop_name: 作物名称
            quantity: 购买数量
            
        Returns:
            tuple[bool, str]: (是否成功, 消息)
        """
        if self.is_paused:
            return False, "⚠️ 游戏已暂停！"
        
        success, message = self.game_manager.buy_seeds(crop_name, quantity)
        if success:
            self._trigger_ui_update()
        return success, message
    
    def sell_crop(self, crop_name: str, quantity: int = 1) -> tuple[bool, str]:
        """
        出售作物
        
        Args:
            crop_name: 作物名称
            quantity: 出售数量
            
        Returns:
            tuple[bool, str]: (是否成功, 消息)
        """
        if self.is_paused:
            return False, "⚠️ 游戏已暂停！"
        
        success, message = self.game_manager.sell_crop(crop_name, quantity)
        if success:
            self._trigger_ui_update()
        return success, message
    
    def sell_all_crops(self) -> list[tuple[bool, str]]:
        """
        出售所有作物
        
        Returns:
            list[tuple[bool, str]]: 结果列表
        """
        if self.is_paused:
            return []
        
        results = self.game_manager.sell_all_crops()
        self._trigger_ui_update()
        return results
    
    # ========== 时间推进 ==========
    
    def advance_day(self) -> dict:
        """
        推进到下一天
        
        Returns:
            dict: 当天结果数据
        """
        if self.is_paused:
            return {}
        
        result = self.game_manager.advance_day()
        self._trigger_ui_update()
        
        # 自动保存检查
        if self.auto_save_enabled and result.day % 5 == 0:  # 每5天自动保存
            self.save_game()
        
        return result
    
    def toggle_pause(self):
        """切换暂停状态"""
        self.is_paused = not self.is_paused
        self._trigger_ui_update()
        return self.is_paused
    
    # ========== 农场管理 ==========
    
    def upgrade_farm(self) -> tuple[bool, str]:
        """
        升级农场
        
        Returns:
            tuple[bool, str]: (是否成功, 消息)
        """
        if self.is_paused:
            return False, "⚠️ 游戏已暂停！"
        
        success, message = self.game_manager.upgrade_farm()
        if success:
            self._trigger_ui_update()
        return success, message
    
    def get_farm_info(self) -> dict:
        """
        获取农场信息
        
        Returns:
            dict: 农场信息
        """
        return {
            'size': self.game_manager.get_plot_size(),
            'total_plots': self.game_manager.get_total_plots(),
            'used_plots': self.game_manager.get_used_plots(),
            'mature_plots': self.game_manager.get_mature_plots_count(),
            'can_upgrade': self.game_manager.can_upgrade_farm(),
            'upgrade_cost': self.game_manager.get_upgrade_cost()
        }
    
    # ========== 数据获取 ==========
    
    def get_game_state(self) -> dict:
        """
        获取完整游戏状态
        
        Returns:
            dict: 游戏状态数据
        """
        return {
            'date': self.game_manager.get_current_date(),
            'season': self.game_manager.get_current_season().value,
            'weather': self.game_manager.get_current_weather().value,
            'player': {
                'name': self.game_manager.player.name,
                'money': self.game_manager.player.money,
                'seeds': dict(self.game_manager.player.seeds),
                'inventory': dict(self.game_manager.player.inventory),
                'upgrade_level': self.game_manager.player.upgrade_level
            },
            'farm': self.get_farm_info(),
            'achievements': {
                'unlocked': self.game_manager.achievement_manager.get_unlocked_count(),
                'total': self.game_manager.achievement_manager.get_total_count()
            },
            'stats': {
                'days_played': self.game_manager.player.stats.days_played,
                'total_harvested': self.game_manager.player.stats.total_harvested,
                'total_earnings': self.game_manager.player.stats.total_earnings
            }
        }
    
    def get_available_crops_for_season(self) -> list:
        """
        获取当前季节可种植的作物
        
        Returns:
            list: 作物列表
        """
        current_season = self.game_manager.get_current_season()
        all_crops = self.game_manager.economy_system.get_all_crops()
        return [crop for crop in all_crops if crop.can_plant_in_season(current_season)]
    
    def get_player_seeds(self) -> dict:
        """
        获取玩家种子库存
        
        Returns:
            dict: 种子库存
        """
        return dict(self.game_manager.player.seeds)
    
    def get_player_inventory(self) -> dict:
        """
        获取玩家仓库
        
        Returns:
            dict: 仓库物品
        """
        return dict(self.game_manager.player.inventory)
    
    # ========== 辅助方法 ==========
    
    def _trigger_ui_update(self):
        """触发UI更新"""
        if self.ui_callback:
            # 在主线程中调用UI更新
            try:
                self.ui_callback()
            except Exception as e:
                print(f"UI更新失败: {e}")
