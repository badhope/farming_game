"""
时间系统模块
管理游戏时间、季节、天气等
"""

import random
from dataclasses import dataclass, field
from typing import Optional, Tuple
from config.settings import Season, Weather, GameConfig


@dataclass
class TimeSystem:
    """
    时间系统类
    
    管理游戏中的时间流逝、季节变化和天气
    
    属性：
        year: 当前年份
        day: 当前天数（每季28天）
        season: 当前季节
        weather: 当前天气
        tomorrow_weather: 明天天气（预报）
    """
    year: int = 1
    day: int = 1
    season: Season = Season.SPRING
    weather: Weather = Weather.SUNNY
    tomorrow_weather: Optional[Weather] = None
    
    def __post_init__(self):
        """初始化后处理"""
        # 初始化天气
        self.weather = self._generate_weather()
        self.tomorrow_weather = self._generate_weather()
    
    # ========== 时间获取 ==========
    
    def get_date_string(self) -> str:
        """
        获取日期字符串
        
        Returns:
            str: 格式化的日期字符串
        """
        return f"第{self.year}年 {self.season.value} 第{self.day}天"
    
    def get_short_date(self) -> str:
        """
        获取简短日期字符串
        
        Returns:
            str: 简短格式日期
        """
        return f"Y{self.year}D{self.day}"
    
    def get_total_days(self) -> int:
        """
        获取总游戏天数
        
        Returns:
            int: 从游戏开始到现在的总天数
        """
        days_per_year = GameConfig.DAYS_PER_SEASON * GameConfig.SEASONS_PER_YEAR
        return (self.year - 1) * days_per_year + \
               (list(Season).index(self.season) * GameConfig.DAYS_PER_SEASON) + \
               self.day
    
    def get_season_progress(self) -> float:
        """
        获取当前季节进度
        
        Returns:
            float: 0.0 到 1.0 之间的进度值
        """
        return self.day / GameConfig.DAYS_PER_SEASON
    
    def get_year_progress(self) -> float:
        """
        获取当前年份进度
        
        Returns:
            float: 0.0 到 1.0 之间的进度值
        """
        days_in_year = GameConfig.DAYS_PER_SEASON * GameConfig.SEASONS_PER_YEAR
        season_days = list(Season).index(self.season) * GameConfig.DAYS_PER_SEASON
        total_days = season_days + self.day
        return total_days / days_in_year
    
    # ========== 时间推进 ==========
    
    def advance_day(self) -> dict:
        """
        推进一天
        
        Returns:
            dict: 包含当天变化信息的字典
        """
        events = {
            "new_day": True,
            "new_season": False,
            "new_year": False,
            "season_changed_to": None,
            "weather_changed": False,
            "old_weather": self.weather,
            "new_weather": None,
        }
        
        # 推进天数
        self.day += 1
        
        # 检查是否进入新季节
        if self.day > GameConfig.DAYS_PER_SEASON:
            self.day = 1
            events["new_season"] = True
            events["season_changed_to"] = self._advance_season()
            
            # 检查是否进入新年
            if self.season == Season.SPRING:
                self.year += 1
                events["new_year"] = True
        
        # 更新天气
        old_weather = self.weather
        self.weather = self.tomorrow_weather
        self.tomorrow_weather = self._generate_weather()
        
        events["weather_changed"] = (old_weather != self.weather)
        events["new_weather"] = self.weather
        
        return events
    
    def _advance_season(self) -> Season:
        """
        推进季节
        
        Returns:
            Season: 新的季节
        """
        seasons = list(Season)
        current_idx = seasons.index(self.season)
        self.season = seasons[(current_idx + 1) % 4]
        return self.season
    
    # ========== 天气系统 ==========
    
    def _generate_weather(self) -> Weather:
        """
        根据当前季节生成天气
        
        Returns:
            Weather: 生成的天气
        """
        weights = GameConfig.WEATHER_WEIGHTS.get(self.season, [0.5, 0.25, 0.2, 0.05])
        return random.choices(list(Weather), weights=weights)[0]
    
    def get_weather_info(self) -> Tuple[str, str]:
        """
        获取天气信息
        
        Returns:
            Tuple[str, str]: (当前天气字符串, 明天天气字符串)
        """
        current = f"{self.weather.value}"
        tomorrow = f"{self.tomorrow_weather.value}" if self.tomorrow_weather else "未知"
        return current, tomorrow
    
    def is_rainy(self) -> bool:
        """
        检查今天是否下雨
        
        Returns:
            bool: 是否下雨
        """
        return self.weather in [Weather.RAINY, Weather.STORMY]
    
    def is_stormy(self) -> bool:
        """
        检查今天是否暴风雨
        
        Returns:
            bool: 是否暴风雨
        """
        return self.weather == Weather.STORMY
    
    def is_good_weather(self) -> bool:
        """
        检查是否是好天气（晴天或阴天）
        
        Returns:
            bool: 是否好天气
        """
        return self.weather in [Weather.SUNNY, Weather.CLOUDY]
    
    def get_weather_effect_description(self) -> str:
        """
        获取天气效果描述
        
        Returns:
            str: 天气效果说明
        """
        descriptions = {
            Weather.SUNNY: "☀️ 阳光明媚，适合农作，记得浇水！",
            Weather.CLOUDY: "☁️ 多云天气，温度适宜。",
            Weather.RAINY: "🌧️ 下雨天，作物自动获得水分！",
            Weather.STORMY: "⛈️ 暴风雨！作物可能受损！",
        }
        return descriptions.get(self.weather, "")
    
    def get_forecast(self, days: int = 3) -> list:
        """
        获取未来几天的天气预报
        
        注意：这是一个简化版本，实际游戏中可能需要更复杂的预测
        
        Args:
            days: 预报天数
            
        Returns:
            list: 天气预报列表
        """
        forecast = []
        
        # 第一天是确定的明天天气
        if self.tomorrow_weather:
            forecast.append(self.tomorrow_weather)
        
        # 后续天数随机生成（简化处理）
        for _ in range(days - 1):
            forecast.append(self._generate_weather())
        
        return forecast
    
    # ========== 季节相关 ==========
    
    def get_season_info(self) -> dict:
        """
        获取季节详细信息
        
        Returns:
            dict: 季节信息字典
        """
        return {
            "name": self.season.value,
            "day": self.day,
            "total_days": GameConfig.DAYS_PER_SEASON,
            "remaining_days": GameConfig.DAYS_PER_SEASON - self.day,
            "progress": self.get_season_progress() * 100,
            "year": self.year,
        }
    
    def get_next_season(self) -> Season:
        """
        获取下一个季节
        
        Returns:
            Season: 下一个季节
        """
        seasons = list(Season)
        current_idx = seasons.index(self.season)
        return seasons[(current_idx + 1) % 4]
    
    def get_days_until_season_change(self) -> int:
        """
        获取距离换季还有多少天
        
        Returns:
            int: 剩余天数
        """
        return GameConfig.DAYS_PER_SEASON - self.day
    
    # ========== 存档相关 ==========
    
    def to_dict(self) -> dict:
        """
        将时间系统转换为字典（用于存档）
        
        Returns:
            dict: 时间数据字典
        """
        return {
            "year": self.year,
            "day": self.day,
            "season": self.season.name,
            "weather": self.weather.name,
            "tomorrow_weather": self.tomorrow_weather.name if self.tomorrow_weather else None,
        }
    
    def from_dict(self, data: dict) -> None:
        """
        从字典加载时间系统（用于读档）
        
        Args:
            data: 时间数据字典
        """
        self.year = data.get("year", 1)
        self.day = data.get("day", 1)
        self.season = Season[data.get("season", "SPRING")]
        self.weather = Weather[data.get("weather", "SUNNY")]
        
        tomorrow = data.get("tomorrow_weather")
        self.tomorrow_weather = Weather[tomorrow] if tomorrow else self._generate_weather()
    
    # ========== 显示相关 ==========
    
    def get_display_header(self) -> str:
        """
        获取显示标题（用于UI）
        
        Returns:
            str: 格式化的标题字符串
        """
        lines = [
            "=" * 50,
            f"📅 {self.get_date_string()}",
            f"🌡️ 季节: {self.season.value}",
            f"{self.weather.value}",
            f"📢 {self.get_weather_effect_description()}",
            "=" * 50,
        ]
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.get_date_string()
    
    def __repr__(self) -> str:
        return (
            f"TimeSystem(year={self.year}, day={self.day}, "
            f"season={self.season.name}, weather={self.weather.name})"
        )
