"""
作物数据模型
定义作物类的数据结构
"""

from dataclasses import dataclass
from typing import List
from config.settings import Season, CropType


@dataclass
class Crop:
    """
    作物数据类
    
    属性：
        name: 作物名称
        seed_price: 种子购买价格
        sell_price: 成熟后出售价格
        grow_days: 生长所需天数
        seasons: 适宜种植的季节列表
        water_needed: 每天需要的浇水次数
        emoji: 显示用的表情符号
        crop_type: 作物类型（蔬菜/水果/谷物/花卉）
        description: 作物描述
    """
    name: str
    seed_price: int
    sell_price: int
    grow_days: int
    seasons: List[Season]
    water_needed: int
    emoji: str
    crop_type: CropType
    description: str = ""
    
    def can_plant_in_season(self, season: Season) -> bool:
        """
        检查是否可以在指定季节种植
        
        Args:
            season: 要检查的季节
            
        Returns:
            bool: 是否可以种植
        """
        return season in self.seasons
    
    def get_profit(self) -> int:
        """
        计算种植该作物的利润
        
        Returns:
            int: 利润 = 出售价格 - 种子价格
        """
        return self.sell_price - self.seed_price
    
    def get_profit_per_day(self) -> float:
        """
        计算每日利润率
        
        Returns:
            float: 每日利润 = 利润 / 生长天数
        """
        profit = self.get_profit()
        return round(profit / self.grow_days, 2)
    
    def get_seasons_str(self) -> str:
        """
        获取适宜季节的字符串表示
        
        Returns:
            str: 季节字符串，如 "春天/夏天"
        """
        return "/".join([s.value for s in self.seasons])
    
    def get_roi(self) -> float:
        """
        计算投资回报率
        
        Returns:
            float: ROI = 利润 / 种子价格 * 100%
        """
        if self.seed_price == 0:
            return 0.0
        roi = (self.get_profit() / self.seed_price) * 100
        return round(roi, 1)
    
    def __str__(self) -> str:
        """
        字符串表示
        
        Returns:
            str: 作物的简要描述
        """
        return (
            f"{self.emoji} {self.name} | "
            f"种子:{self.seed_price}金 | "
            f"售价:{self.sell_price}金 | "
            f"周期:{self.grow_days}天 | "
            f"季节:{self.get_seasons_str()}"
        )
    
    def __repr__(self) -> str:
        return f"Crop(name='{self.name}', price={self.seed_price})"
