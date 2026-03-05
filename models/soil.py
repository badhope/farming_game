"""
土壤质量和肥料系统模块
管理土壤状态和肥料效果
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class SoilQuality(Enum):
    POOR = "poor"
    NORMAL = "normal"
    GOOD = "good"
    EXCELLENT = "excellent"


class FertilizerType(Enum):
    BASIC = "basic"
    QUALITY = "quality"
    DELUXE = "deluxe"
    ORGANIC = "organic"
    SPEED_GROW = "speed_grow"
    WATER_RETAIN = "water_retain"


@dataclass
class Fertilizer:
    fertilizer_type: FertilizerType
    name: str
    description: str
    growth_bonus: float
    quality_bonus: float
    water_retention: int
    duration: int
    price: int
    icon: str
    
    def get_display_name(self) -> str:
        return f"{self.icon} {self.name}"


@dataclass
class SoilState:
    quality: SoilQuality
    fertility: int
    water_level: int
    fertilizer: Optional[Fertilizer] = None
    fertilizer_days_remaining: int = 0
    crop_history: List[str] = field(default_factory=list)
    tillage_level: int = 0
    
    def get_growth_multiplier(self) -> float:
        base = {
            SoilQuality.POOR: 0.7,
            SoilQuality.NORMAL: 1.0,
            SoilQuality.GOOD: 1.2,
            SoilQuality.EXCELLENT: 1.5
        }
        multiplier = base.get(self.quality, 1.0)
        
        if self.fertilizer:
            multiplier *= (1 + self.fertilizer.growth_bonus)
        
        multiplier *= (1 + self.tillage_level * 0.05)
        
        return multiplier
    
    def get_quality_bonus(self) -> float:
        bonus = 0.0
        
        if self.fertilizer:
            bonus += self.fertilizer.quality_bonus
        
        bonus += self.tillage_level * 0.02
        
        return bonus
    
    def needs_water(self) -> bool:
        if self.fertilizer and self.fertilizer.water_retention > 0:
            return self.water_level < 30
        return self.water_level < 50


class FertilizerRegistry:
    
    FERTILIZERS = {
        FertilizerType.BASIC: Fertilizer(
            fertilizer_type=FertilizerType.BASIC,
            name="基础肥料",
            description="提供基本的营养，略微加速生长",
            growth_bonus=0.1,
            quality_bonus=0.05,
            water_retention=0,
            duration=7,
            price=50,
            icon="🧪"
        ),
        FertilizerType.QUALITY: Fertilizer(
            fertilizer_type=FertilizerType.QUALITY,
            name="优质肥料",
            description="提高作物品质和生长速度",
            growth_bonus=0.2,
            quality_bonus=0.15,
            water_retention=1,
            duration=14,
            price=150,
            icon="⚗️"
        ),
        FertilizerType.DELUXE: Fertilizer(
            fertilizer_type=FertilizerType.DELUXE,
            name="豪华肥料",
            description="顶级肥料，大幅提升所有属性",
            growth_bonus=0.35,
            quality_bonus=0.25,
            water_retention=2,
            duration=21,
            price=300,
            icon="✨"
        ),
        FertilizerType.ORGANIC: Fertilizer(
            fertilizer_type=FertilizerType.ORGANIC,
            name="有机肥料",
            description="天然肥料，可持续改善土壤质量",
            growth_bonus=0.15,
            quality_bonus=0.3,
            water_retention=1,
            duration=28,
            price=200,
            icon="🌿"
        ),
        FertilizerType.SPEED_GROW: Fertilizer(
            fertilizer_type=FertilizerType.SPEED_GROW,
            name="速生肥料",
            description="大幅加速生长，但不提升品质",
            growth_bonus=0.5,
            quality_bonus=0.0,
            water_retention=0,
            duration=5,
            price=250,
            icon="⚡"
        ),
        FertilizerType.WATER_RETAIN: Fertilizer(
            fertilizer_type=FertilizerType.WATER_RETAIN,
            name="保水肥料",
            description="保持土壤湿润，减少浇水需求",
            growth_bonus=0.1,
            quality_bonus=0.1,
            water_retention=3,
            duration=14,
            price=180,
            icon="💧"
        ),
    }
    
    @classmethod
    def get_fertilizer(cls, fertilizer_type: FertilizerType) -> Optional[Fertilizer]:
        return cls.FERTILIZERS.get(fertilizer_type)
    
    @classmethod
    def get_all_fertilizers(cls) -> Dict[FertilizerType, Fertilizer]:
        return cls.FERTILIZERS.copy()
    
    @classmethod
    def get_available_fertilizers(cls, player_level: int) -> List[Fertilizer]:
        result = []
        for fert_type, fert in cls.FERTILIZERS.items():
            if fert_type == FertilizerType.BASIC:
                result.append(fert)
            elif fert_type == FertilizerType.QUALITY and player_level >= 3:
                result.append(fert)
            elif fert_type == FertilizerType.SPEED_GROW and player_level >= 4:
                result.append(fert)
            elif fert_type == FertilizerType.WATER_RETAIN and player_level >= 5:
                result.append(fert)
            elif fert_type == FertilizerType.ORGANIC and player_level >= 6:
                result.append(fert)
            elif fert_type == FertilizerType.DELUXE and player_level >= 8:
                result.append(fert)
        return result


class SoilManager:
    
    QUALITY_THRESHOLDS = {
        SoilQuality.POOR: (0, 30),
        SoilQuality.NORMAL: (30, 60),
        SoilQuality.GOOD: (60, 85),
        SoilQuality.EXCELLENT: (85, 100)
    }
    
    def __init__(self, plot_size: int = 3):
        self.plot_size = plot_size
        self.soil_states: Dict[Tuple[int, int], SoilState] = {}
        self._init_soil_states()
    
    def _init_soil_states(self):
        for row in range(self.plot_size):
            for col in range(self.plot_size):
                self.soil_states[(row, col)] = SoilState(
                    quality=SoilQuality.NORMAL,
                    fertility=50,
                    water_level=50
                )
    
    def expand_plots(self, new_size: int):
        for row in range(self.plot_size, new_size):
            for col in range(new_size):
                self.soil_states[(row, col)] = SoilState(
                    quality=SoilQuality.NORMAL,
                    fertility=50,
                    water_level=50
                )
        
        for row in range(self.plot_size):
            for col in range(self.plot_size, new_size):
                self.soil_states[(row, col)] = SoilState(
                    quality=SoilQuality.NORMAL,
                    fertility=50,
                    water_level=50
                )
        
        self.plot_size = new_size
    
    def get_soil_state(self, row: int, col: int) -> Optional[SoilState]:
        return self.soil_states.get((row, col))
    
    def apply_fertilizer(self, row: int, col: int, fertilizer_type: FertilizerType) -> Tuple[bool, str]:
        soil = self.get_soil_state(row, col)
        if not soil:
            return False, "无效的地块"
        
        fertilizer = FertilizerRegistry.get_fertilizer(fertilizer_type)
        if not fertilizer:
            return False, "未知的肥料类型"
        
        if soil.fertilizer and soil.fertilizer_days_remaining > 0:
            return False, "该地块已有肥料生效中"
        
        soil.fertilizer = fertilizer
        soil.fertilizer_days_remaining = fertilizer.duration
        
        return True, f"成功施用 {fertilizer.name}！"
    
    def water_soil(self, row: int, col: int, amount: int = 50) -> Tuple[bool, str]:
        soil = self.get_soil_state(row, col)
        if not soil:
            return False, "无效的地块"
        
        soil.water_level = min(100, soil.water_level + amount)
        
        return True, f"土壤湿度提升至 {soil.water_level}%"
    
    def till_soil(self, row: int, col: int) -> Tuple[bool, str]:
        soil = self.get_soil_state(row, col)
        if not soil:
            return False, "无效的地块"
        
        if soil.tillage_level >= 5:
            return False, "该地块已达最大耕作等级"
        
        soil.tillage_level += 1
        soil.fertility = min(100, soil.fertility + 5)
        self._update_quality(row, col)
        
        return True, f"耕地等级提升至 {soil.tillage_level}"
    
    def record_harvest(self, row: int, col: int, crop_name: str):
        soil = self.get_soil_state(row, col)
        if soil:
            soil.crop_history.append(crop_name)
            if len(soil.crop_history) > 10:
                soil.crop_history.pop(0)
    
    def new_day(self, row: int, col: int, was_watered: bool, had_crop: bool) -> Dict:
        soil = self.get_soil_state(row, col)
        if not soil:
            return {}
        
        result = {
            "fertilizer_expired": False,
            "quality_changed": False,
            "needs_water": False
        }
        
        if was_watered:
            soil.water_level = min(100, soil.water_level + 40)
        else:
            evaporation = 20
            if soil.fertilizer:
                evaporation -= soil.fertilizer.water_retention * 5
            soil.water_level = max(0, soil.water_level - evaporation)
        
        if soil.fertilizer and soil.fertilizer_days_remaining > 0:
            soil.fertilizer_days_remaining -= 1
            if soil.fertilizer_days_remaining <= 0:
                result["fertilizer_expired"] = True
                soil.fertilizer = None
        
        if had_crop:
            soil.fertility = max(0, soil.fertility - 2)
        else:
            soil.fertility = min(100, soil.fertility + 1)
        
        old_quality = soil.quality
        self._update_quality(row, col)
        result["quality_changed"] = (old_quality != soil.quality)
        
        result["needs_water"] = soil.needs_water()
        
        return result
    
    def _update_quality(self, row: int, col: int):
        soil = self.get_soil_state(row, col)
        if not soil:
            return
        
        for quality, (low, high) in self.QUALITY_THRESHOLDS.items():
            if low <= soil.fertility < high:
                soil.quality = quality
                break
    
    def improve_soil(self, row: int, col: int, amount: int = 10) -> Tuple[bool, str]:
        soil = self.get_soil_state(row, col)
        if not soil:
            return False, "无效的地块"
        
        old_quality = soil.quality
        soil.fertility = min(100, soil.fertility + amount)
        self._update_quality(row, col)
        
        if soil.quality != old_quality:
            return True, f"土壤质量提升至 {soil.quality.value}！"
        
        return True, f"土壤肥力提升至 {soil.fertility}"
    
    def get_growth_multiplier(self, row: int, col: int) -> float:
        soil = self.get_soil_state(row, col)
        if soil:
            return soil.get_growth_multiplier()
        return 1.0
    
    def get_quality_bonus(self, row: int, col: int) -> float:
        soil = self.get_soil_state(row, col)
        if soil:
            return soil.get_quality_bonus()
        return 0.0
    
    def get_soil_info(self, row: int, col: int) -> Dict:
        soil = self.get_soil_state(row, col)
        if not soil:
            return {}
        
        return {
            "quality": soil.quality.value,
            "fertility": soil.fertility,
            "water_level": soil.water_level,
            "tillage_level": soil.tillage_level,
            "fertilizer": soil.fertilizer.name if soil.fertilizer else None,
            "fertilizer_days": soil.fertilizer_days_remaining,
            "growth_multiplier": soil.get_growth_multiplier(),
            "quality_bonus": soil.get_quality_bonus(),
            "needs_water": soil.needs_water()
        }
    
    def get_save_data(self) -> Dict:
        data = {
            "plot_size": self.plot_size,
            "soil_states": {}
        }
        
        for (row, col), soil in self.soil_states.items():
            data["soil_states"][f"{row},{col}"] = {
                "quality": soil.quality.value,
                "fertility": soil.fertility,
                "water_level": soil.water_level,
                "fertilizer_type": soil.fertilizer.fertilizer_type.value if soil.fertilizer else None,
                "fertilizer_days": soil.fertilizer_days_remaining,
                "tillage_level": soil.tillage_level,
                "crop_history": soil.crop_history
            }
        
        return data
    
    def load_save_data(self, data: Dict):
        self.plot_size = data.get("plot_size", 3)
        self.soil_states.clear()
        
        for key, soil_data in data.get("soil_states", {}).items():
            row, col = map(int, key.split(","))
            
            fertilizer = None
            if soil_data.get("fertilizer_type"):
                fert_type = FertilizerType(soil_data["fertilizer_type"])
                fertilizer = FertilizerRegistry.get_fertilizer(fert_type)
            
            self.soil_states[(row, col)] = SoilState(
                quality=SoilQuality(soil_data.get("quality", "normal")),
                fertility=soil_data.get("fertility", 50),
                water_level=soil_data.get("water_level", 50),
                fertilizer=fertilizer,
                fertilizer_days_remaining=soil_data.get("fertilizer_days", 0),
                crop_history=soil_data.get("crop_history", []),
                tillage_level=soil_data.get("tillage_level", 0)
            )
