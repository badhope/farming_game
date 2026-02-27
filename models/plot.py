"""
农田地块数据模型
定义地块类的数据结构
"""

from dataclasses import dataclass, field
from typing import Optional
from models.crop import Crop


@dataclass
class Plot:
    """
    农田地块数据类
    
    属性：
        crop: 当前种植的作物（None表示空地）
        planted_day: 种植时的游戏天数
        watered_today: 今天是否已浇水
        growth_stage: 生长阶段 (0-4, 4表示成熟可收获)
        days_watered: 累计浇水天数
    """
    crop: Optional[Crop] = None
    planted_day: int = 0
    watered_today: bool = False
    growth_stage: int = 0
    days_watered: int = 0
    
    def is_empty(self) -> bool:
        """
        检查地块是否为空
        
        Returns:
            bool: 是否为空地
        """
        return self.crop is None
    
    def is_mature(self) -> bool:
        """
        检查作物是否成熟
        
        Returns:
            bool: 是否成熟可收获
        """
        return self.crop is not None and self.growth_stage >= 4
    
    def is_growing(self) -> bool:
        """
        检查是否有正在生长的作物
        
        Returns:
            bool: 是否有生长中的作物
        """
        return self.crop is not None and self.growth_stage < 4
    
    def get_growth_progress(self) -> float:
        """
        获取生长进度百分比
        
        Returns:
            float: 0.0 到 1.0 之间的进度值
        """
        if self.crop is None:
            return 0.0
        return min(self.growth_stage / 4.0, 1.0)
    
    def get_remaining_days(self) -> int:
        """
        获取距离成熟还需的天数
        
        Returns:
            int: 剩余天数，成熟后返回0
        """
        if self.crop is None:
            return 0
        remaining = 4 - self.growth_stage
        return max(0, remaining)
    
    def plant(self, crop: Crop, current_day: int) -> bool:
        """
        在地块上种植作物
        
        Args:
            crop: 要种植的作物
            current_day: 当前游戏天数
            
        Returns:
            bool: 是否种植成功
        """
        if not self.is_empty():
            return False
        
        self.crop = crop
        self.planted_day = current_day
        self.growth_stage = 0
        self.watered_today = False
        self.days_watered = 0
        return True
    
    def water(self) -> bool:
        """
        给地块浇水
        
        Returns:
            bool: 是否浇水成功
        """
        if self.is_empty() or self.watered_today:
            return False
        
        self.watered_today = True
        return True
    
    def grow(self) -> bool:
        """
        作物生长一天
        
        Returns:
            bool: 是否成功生长
        """
        if self.is_empty() or self.is_mature():
            return False
        
        if self.watered_today:
            self.growth_stage += 1
            self.days_watered += 1
            
            # 防止超过最大阶段
            if self.growth_stage > 4:
                self.growth_stage = 4
            
            return True
        
        return False
    
    def harvest(self) -> Optional[Crop]:
        """
        收获作物
        
        Returns:
            Optional[Crop]: 收获的作物，未成熟返回None
        """
        if not self.is_mature():
            return None
        
        harvested_crop = self.crop
        self.clear()
        return harvested_crop
    
    def clear(self) -> None:
        """
        清空地块（作物枯萎或被摧毁时使用）
        """
        self.crop = None
        self.planted_day = 0
        self.watered_today = False
        self.growth_stage = 0
        self.days_watered = 0
    
    def reset_water_status(self) -> None:
        """
        重置浇水状态（新的一天开始时调用）
        """
        self.watered_today = False
    
    def force_water(self) -> None:
        """
        强制浇水（雨天自动浇水时使用）
        """
        if not self.is_empty() and not self.is_mature():
            self.watered_today = True
    
    def get_display_icon(self) -> str:
        """
        获取地块的显示图标
        
        Returns:
            str: 显示用的图标字符串
        """
        if self.is_empty():
            return "⬜"
        
        if self.is_mature():
            return f"{self.crop.emoji}✨"
        
        if self.watered_today:
            return f"{self.crop.emoji}💧"
        
        return f"{self.crop.emoji} "
    
    def get_status_text(self) -> str:
        """
        获取地块状态文本描述
        
        Returns:
            str: 状态描述文本
        """
        if self.is_empty():
            return "空地"
        
        if self.is_mature():
            return f"{self.crop.emoji} {self.crop.name} (已成熟，可收获)"
        
        progress = int(self.get_growth_progress() * 100)
        water_status = "已浇水" if self.watered_today else "未浇水"
        return (
            f"{self.crop.emoji} {self.crop.name} | "
            f"生长: {progress}% | "
            f"{water_status} | "
            f"剩余: {self.get_remaining_days()}天"
        )
    
    def __str__(self) -> str:
        return self.get_display_icon()
    
    def __repr__(self) -> str:
        if self.is_empty():
            return "Plot(empty=True)"
        return (
            f"Plot(crop='{self.crop.name}', "
            f"stage={self.growth_stage}, "
            f"watered={self.watered_today})"
        )
