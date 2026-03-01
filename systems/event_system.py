"""
游戏事件系统模块
处理随机事件、特殊互动和剧情发展
"""

import random
import time
from typing import List, Dict, Callable, Optional
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """事件类型枚举"""
    WEATHER = "weather"
    RANDOM = "random"
    ACHIEVEMENT = "achievement"
    SPECIAL = "special"


@dataclass
class GameEvent:
    """
    游戏事件数据类
    """
    event_type: EventType
    title: str
    description: str
    effect: Optional[Callable] = None
    probability: float = 1.0
    conditions: Optional[Dict] = None


class EventSystem:
    """
    游戏事件系统类
    管理游戏中各种随机事件的发生
    """
    
    def __init__(self):
        """初始化事件系统"""
        self.events: List[GameEvent] = []
        self.active_events: List[GameEvent] = []
        self.event_history: List[Dict] = []
        self._initialize_events()
    
    def _initialize_events(self):
        """初始化预定义事件"""
        # 天气相关事件
        weather_events = [
            GameEvent(
                event_type=EventType.WEATHER,
                title="☀️ 阳光明媚",
                description="今天阳光充足，作物生长速度提升20%！",
                effect=self._boost_growth,
                probability=0.3
            ),
            GameEvent(
                event_type=EventType.WEATHER,
                title="🌧️ 春雨绵绵",
                description="春雨贵如油，作物自动获得充足水分！",
                effect=self._auto_water_all,
                probability=0.25
            ),
            GameEvent(
                event_type=EventType.WEATHER,
                title="⛈️ 暴风骤雨",
                description="暴风雨来袭！部分作物可能受损...",
                effect=self._storm_damage,
                probability=0.1
            )
        ]
        
        # 随机事件
        random_events = [
            GameEvent(
                event_type=EventType.RANDOM,
                title="🎁 神秘礼物",
                description="村民送给你一些免费的种子！",
                effect=self._gift_seeds,
                probability=0.15
            ),
            GameEvent(
                event_type=EventType.RANDOM,
                title="💰 意外之财",
                description="你在田边发现了遗落的钱袋！",
                effect=self._find_money,
                probability=0.1
            ),
            GameEvent(
                event_type=EventType.RANDOM,
                title="🐛 虫害侵袭",
                description="有害虫入侵，部分作物受到损害！",
                effect=self._pest_damage,
                probability=0.08
            ),
            GameEvent(
                event_type=EventType.RANDOM,
                title="🚜 邻居帮忙",
                description="好心的邻居帮你照料了一天的农田！",
                effect=self._neighbor_help,
                probability=0.12
            )
        ]
        
        # 特殊事件
        special_events = [
            GameEvent(
                event_type=EventType.SPECIAL,
                title="🎪 集市开放",
                description="镇上的集市今天开放，所有作物价格提升30%！",
                effect=self._market_boost,
                probability=0.2,
                conditions={"day_of_week": 6}  # 周六
            ),
            GameEvent(
                event_type=EventType.SPECIAL,
                title="🏆 农业比赛",
                description="年度农业比赛开始了！获胜者将获得丰厚奖励！",
                effect=self._agriculture_competition,
                probability=0.3,
                conditions={"season": "spring", "day": 15}
            )
        ]
        
        # 合并所有事件
        self.events.extend(weather_events)
        self.events.extend(random_events)
        self.events.extend(special_events)
    
    def check_daily_events(self, game_state: Dict) -> List[GameEvent]:
        """
        检查每日可能发生的事件
        
        Args:
            game_state: 当前游戏状态
            
        Returns:
            List[GameEvent]: 今天发生的事件列表
        """
        today_events = []
        
        for event in self.events:
            # 检查条件
            if not self._check_conditions(event, game_state):
                continue
            
            # 检查概率
            if random.random() < event.probability:
                today_events.append(event)
                self.active_events.append(event)
        
        # 记录事件历史
        if today_events:
            self._record_events(today_events, game_state)
        
        return today_events
    
    def _check_conditions(self, event: GameEvent, game_state: Dict) -> bool:
        """
        检查事件发生条件
        
        Args:
            event: 事件对象
            game_state: 游戏状态
            
        Returns:
            bool: 是否满足条件
        """
        if not event.conditions:
            return True
        
        for key, value in event.conditions.items():
            if key == "day_of_week":
                # 检查星期几
                day_of_week = game_state.get("day", 1) % 7
                if day_of_week != value:
                    return False
            elif key == "season":
                # 检查季节
                if game_state.get("season") != value:
                    return False
            elif key == "day":
                # 检查具体日期
                if game_state.get("day") != value:
                    return False
        
        return True
    
    def trigger_event_effects(self, game_manager):
        """
        触发活跃事件的效果
        
        Args:
            game_manager: 游戏管理器实例
        """
        for event in self.active_events:
            if event.effect:
                try:
                    event.effect(game_manager)
                except Exception as e:
                    print(f"事件效果执行失败: {e}")
        
        # 清空当日事件
        self.active_events.clear()
    
    def get_recent_events(self, limit: int = 5) -> List[Dict]:
        """
        获取最近的事件记录
        
        Args:
            limit: 限制数量
            
        Returns:
            List[Dict]: 事件记录列表
        """
        return self.event_history[-limit:] if self.event_history else []
    
    # ========== 事件效果方法 ==========
    
    def _boost_growth(self, game_manager):
        """提升作物生长速度"""
        # 这里可以实现具体的生长加速逻辑
        pass
    
    def _auto_water_all(self, game_manager):
        """自动给所有作物浇水"""
        game_manager.water_all_plots()
    
    def _storm_damage(self, game_manager):
        """暴风雨损害作物"""
        # 实现暴风雨损害逻辑
        pass
    
    def _gift_seeds(self, game_manager):
        """赠送种子"""
        player = game_manager.player
        # 随机赠送几种种子
        crops = ["土豆", "萝卜", "番茄"]
        gift_crop = random.choice(crops)
        player.add_seeds(gift_crop, random.randint(2, 5))
    
    def _find_money(self, game_manager):
        """发现金钱"""
        player = game_manager.player
        found_amount = random.randint(50, 200)
        player.add_money(found_amount)
    
    def _pest_damage(self, game_manager):
        """虫害损害"""
        # 实现虫害损害逻辑
        pass
    
    def _neighbor_help(self, game_manager):
        """邻居帮助"""
        # 实现邻居帮助逻辑
        pass
    
    def _market_boost(self, game_manager):
        """集市加成"""
        # 实现价格提升逻辑
        pass
    
    def _agriculture_competition(self, game_manager):
        """农业比赛"""
        # 实现比赛逻辑
        pass
    
    def _record_events(self, events: List[GameEvent], game_state: Dict):
        """
        记录事件到历史
        
        Args:
            events: 事件列表
            game_state: 游戏状态
        """
        for event in events:
            record = {
                "timestamp": time.time(),
                "date": game_state.get("date", ""),
                "event_title": event.title,
                "event_description": event.description
            }
            self.event_history.append(record)
