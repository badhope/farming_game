"""
农耕系统模块
负责作物种植、生长和收获管理
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import random
from config.enums import Season, CropStage, CropQuality, CropType
from config.config_loader import get_crop_config


@dataclass
class CropInfo:
    """作物信息"""
    crop_id: str
    name: str
    icon: str
    description: str
    
    seed_price: int = 10
    base_sell_price: int = 20
    
    grow_days: int = 5
    water_per_day: int = 1
    
    seasons: List[str] = field(default_factory=list)
    
    min_temp: int = 5
    max_temp: int = 35
    min_humidity: int = 30
    max_humidity: int = 80
    
    base_yield: int = 3
    yield_variance: int = 1
    
    quality_modifiers: Dict[str, float] = field(default_factory=dict)
    
    requires_trellis: bool = False
    requires_greenhouse: bool = False
    
    exp_reward: int = 10
    
    @classmethod
    def from_config(cls, crop_id: str, config: dict) -> 'CropInfo':
        """从配置字典创建作物信息"""
        return cls(
            crop_id=crop_id,
            name=config.get('name', crop_id),
            icon=config.get('emoji', '🌱'),
            description=config.get('description', ''),
            seed_price=config.get('seed_price', 10),
            base_sell_price=config.get('sell_price', 20),
            grow_days=config.get('grow_days', 5),
            water_per_day=config.get('water_needed', 1),
            seasons=config.get('seasons', []),
            base_yield=config.get('base_yield', 3),
            exp_reward=config.get('exp_reward', 10),
        )


@dataclass
class PlantedCrop:
    """已种植的作物"""
    crop_info: CropInfo
    planted_day: int = 0
    current_stage: CropStage = CropStage.SEED
    days_grown: int = 0
    water_level: int = 0
    health: int = 100
    quality: CropQuality = CropQuality.NORMAL
    
    fertilized: bool = False
    fertilizer_type: str = ""
    
    daily_growth_progress: float = 0.0
    
    def water(self, amount: int = 1):
        """浇水"""
        self.water_level = min(self.water_level + amount, 3)
    
    def advance_day(self, weather_effects: Dict, current_season: str) -> Dict:
        """
        过一天
        返回生长结果
        """
        result = {
            "growth": 0,
            "stage_change": False,
            "withered": False,
            "harvestable": False,
            "quality_change": False,
            "messages": []
        }
        
        # 检查季节是否合适
        season_str = current_season
        if season_str not in self.crop_info.seasons and not self.fertilized:
            self.health -= 20
            result["messages"].append("季节不适合，作物健康下降")
        
        # 计算生长速率
        growth_rate = 1.0
        
        # 水分影响
        if self.water_level >= self.crop_info.water_per_day:
            growth_rate *= 1.2
            self.water_level -= self.crop_info.water_per_day
        else:
            growth_rate *= 0.5
            self.health -= 10
            result["messages"].append("缺水，生长减缓")
        
        # 天气影响
        growth_rate *= weather_effects.get("growth", 1.0)
        
        # 肥料影响
        if self.fertilized:
            growth_rate *= 1.3
        
        # 更新生长进度
        self.daily_growth_progress += growth_rate
        self.days_grown += 1
        
        if self.daily_growth_progress >= 1.0:
            self.daily_growth_progress = 0.0
            result["growth"] = 1
        
        # 检查是否枯萎
        if self.health <= 0:
            self.current_stage = CropStage.WITHERED
            result["withered"] = True
            result["messages"].append("作物枯萎了")
            return result
        
        # 更新生长阶段
        old_stage = self.current_stage
        progress = self.days_grown / self.crop_info.grow_days
        
        if progress >= 1.0:
            self.current_stage = CropStage.MATURE
            result["harvestable"] = True
        elif progress >= 0.7:
            self.current_stage = CropStage.GROWING
        elif progress >= 0.3:
            self.current_stage = CropStage.SPROUT
        
        if self.current_stage != old_stage:
            result["stage_change"] = True
            result["messages"].append(f"作物进入{self.current_stage.value}阶段")
        
        # 品质可能下降
        if random.random() < 0.1 and self.health < 70:
            qualities = list(CropQuality)
            current_idx = qualities.index(self.quality)
            if current_idx > 0:
                self.quality = qualities[current_idx - 1]
                result["quality_change"] = True
        
        return result
    
    def harvest(self) -> Tuple[bool, int, CropQuality, str]:
        """
        收获作物
        返回：(是否成功，产量，品质，消息)
        """
        if self.current_stage != CropStage.MATURE:
            return False, 0, self.quality, "作物还未成熟"
        
        base_yield = self.crop_info.base_yield
        variance = random.randint(-self.crop_info.yield_variance, self.crop_info.yield_variance)
        yield_amount = max(1, base_yield + variance)
        
        quality_mult = {
            CropQuality.POOR: 0.5,
            CropQuality.NORMAL: 1.0,
            CropQuality.GOOD: 1.5,
            CropQuality.EXCELLENT: 2.0,
            CropQuality.LEGENDARY: 3.0
        }
        
        final_yield = int(yield_amount * quality_mult.get(self.quality, 1.0))
        
        return True, final_yield, self.quality, f"收获了{final_yield}个{self.crop_info.name}"


@dataclass
class FarmField:
    """农田地块"""
    row: int
    col: int
    
    is_watered: bool = False
    fertilized: bool = False
    fertilizer_type: Optional[str] = None
    
    planted_crop: Optional[PlantedCrop] = None
    
    def is_empty(self) -> bool:
        """是否为空"""
        return self.planted_crop is None
    
    def is_mature(self) -> bool:
        """作物是否成熟"""
        return self.planted_crop is not None and self.planted_crop.current_stage == CropStage.MATURE
    
    def plant(self, crop_info: CropInfo, day: int):
        """种植作物"""
        if not self.is_empty():
            raise ValueError("地块已有作物")
        
        self.planted_crop = PlantedCrop(crop_info=crop_info, planted_day=day)
    
    def water(self):
        """浇水"""
        if not self.is_empty():
            self.planted_crop.water()
        self.is_watered = True
    
    def harvest(self) -> Tuple[bool, int, CropQuality, str]:
        """收获"""
        if self.is_empty():
            return False, 0, CropQuality.NORMAL, "没有作物可收获"
        
        success, amount, quality, message = self.planted_crop.harvest()
        if success:
            self.planted_crop = None
            self.is_watered = False
        
        return success, amount, quality, message
    
    def clear(self):
        """清除作物"""
        self.planted_crop = None
        self.is_watered = False
        self.fertilized = False


class CropRegistry:
    """作物注册表"""
    
    _crops: Dict[str, CropInfo] = {}
    _initialized: bool = False
    
    @classmethod
    def _init_crops(cls):
        """初始化作物注册表"""
        if cls._initialized:
            return
        
        from config.config_loader import config_loader
        crop_data = config_loader.get_crop_data()
        
        for crop_id, config in crop_data.items():
            crop_info = CropInfo.from_config(crop_id, config)
            cls._crops[crop_id] = crop_info
        
        cls._initialized = True
    
    @classmethod
    def get_crop(cls, crop_id: str) -> Optional[CropInfo]:
        """获取作物信息"""
        cls._init_crops()
        return cls._crops.get(crop_id)
    
    @classmethod
    def get_all_crops(cls) -> Dict[str, CropInfo]:
        """获取所有作物"""
        cls._init_crops()
        return cls._crops.copy()
    
    @classmethod
    def get_crops_by_season(cls, season: str) -> List[CropInfo]:
        """获取指定季节可种植的作物"""
        cls._init_crops()
        return [
            crop for crop in cls._crops.values()
            if season in crop.seasons
        ]
    
    @classmethod
    def get_crops_by_type(cls, crop_type: CropType) -> List[CropInfo]:
        """获取指定类型的作物"""
        cls._init_crops()
        return [
            crop for crop in cls._crops.values()
            if crop.crop_type == crop_type
        ]


class FarmingManager:
    """农耕管理器"""
    
    def __init__(self):
        self.fields: Dict[Tuple[int, int], FarmField] = {}
        self.harvest_count = 0
        self.total_yield = 0
    
    def get_or_create_field(self, row: int, col: int) -> FarmField:
        """获取或创建地块"""
        pos = (row, col)
        if pos not in self.fields:
            self.fields[pos] = FarmField(row=row, col=col)
        return self.fields[pos]
    
    def plant_crop(self, row: int, col: int, crop_id: str, day: int) -> Tuple[bool, str]:
        """种植作物"""
        crop_info = CropRegistry.get_crop(crop_id)
        if not crop_info:
            return False, f"未知的作物：{crop_id}"
        
        field = self.get_or_create_field(row, col)
        
        if not field.is_empty():
            return False, "此地块已有作物"
        
        field.plant(crop_info, day)
        return True, f"种植了{crop_info.name}"
    
    def water_crop(self, row: int, col: int) -> Tuple[bool, str]:
        """浇水"""
        field = self.get_or_create_field(row, col)
        
        if field.is_empty():
            return False, "没有作物可浇水"
        
        field.water()
        return True, "已浇水"
    
    def advance_day(self, weather_effects: Dict, season: str) -> Dict:
        """
        推进一天
        返回所有地块的生长结果
        """
        results = {
            "growth": 0,
            "stage_changes": 0,
            "withered": 0,
            "harvestable": 0,
            "messages": []
        }
        
        for field in self.fields.values():
            if not field.is_empty():
                field_result = field.planted_crop.advance_day(weather_effects, season)
                
                results["growth"] += field_result["growth"]
                if field_result["stage_change"]:
                    results["stage_changes"] += 1
                if field_result["withered"]:
                    results["withered"] += 1
                if field_result["harvestable"]:
                    results["harvestable"] += 1
                results["messages"].extend(field_result["messages"])
        
        return results
    
    def harvest_crop(self, row: int, col: int) -> Tuple[bool, int, CropQuality, str]:
        """收获作物"""
        field = self.get_or_create_field(row, col)
        
        if field.is_empty():
            return False, 0, CropQuality.NORMAL, "没有作物可收获"
        
        success, amount, quality, message = field.harvest()
        
        if success:
            self.harvest_count += 1
            self.total_yield += amount
        
        return success, amount, quality, message
    
    def get_field(self, row: int, col: int) -> Optional[FarmField]:
        """获取地块"""
        return self.fields.get((row, col))
    
    def get_all_fields(self) -> List[FarmField]:
        """获取所有地块"""
        return list(self.fields.values())
    
    def get_mature_fields(self) -> List[FarmField]:
        """获取成熟的地块"""
        return [f for f in self.fields.values() if f.is_mature()]
    
    def clear_field(self, row: int, col: int):
        """清除地块"""
        field = self.get_field(row, col)
        if field:
            field.clear()
