"""
天气效果系统模块
管理天气对农业的影响
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class WeatherType(Enum):
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"
    SNOWY = "snowy"
    WINDY = "windy"
    FOGGY = "foggy"
    DROUGHT = "drought"
    HEATWAVE = "heatwave"


class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


@dataclass
class WeatherEffect:
    weather_type: WeatherType
    name: str
    description: str
    growth_modifier: float
    water_modifier: float
    crop_damage_chance: float
    quality_modifier: float
    stamina_modifier: float
    icon: str
    duration_range: Tuple[int, int] = (1, 3)
    
    def get_display_name(self) -> str:
        return f"{self.icon} {self.name}"


@dataclass
class WeatherForecast:
    day: int
    weather_type: WeatherType
    confidence: float
    special_events: List[str] = field(default_factory=list)


class WeatherEffects:
    
    WEATHER_EFFECTS = {
        WeatherType.SUNNY: WeatherEffect(
            weather_type=WeatherType.SUNNY,
            name="晴天",
            description="阳光明媚，适合户外活动",
            growth_modifier=1.1,
            water_modifier=1.3,
            crop_damage_chance=0.0,
            quality_modifier=1.05,
            stamina_modifier=1.0,
            icon="☀️",
            duration_range=(1, 5)
        ),
        WeatherType.CLOUDY: WeatherEffect(
            weather_type=WeatherType.CLOUDY,
            name="多云",
            description="云层遮蔽，温度适宜",
            growth_modifier=1.0,
            water_modifier=0.9,
            crop_damage_chance=0.0,
            quality_modifier=1.0,
            stamina_modifier=1.0,
            icon="☁️",
            duration_range=(1, 4)
        ),
        WeatherType.RAINY: WeatherEffect(
            weather_type=WeatherType.RAINY,
            name="雨天",
            description="雨水滋润大地",
            growth_modifier=1.15,
            water_modifier=0.0,
            crop_damage_chance=0.02,
            quality_modifier=1.1,
            stamina_modifier=0.9,
            icon="🌧️",
            duration_range=(1, 3)
        ),
        WeatherType.STORMY: WeatherEffect(
            weather_type=WeatherType.STORMY,
            name="暴风雨",
            description="狂风暴雨，小心作物受损",
            growth_modifier=0.5,
            water_modifier=0.0,
            crop_damage_chance=0.25,
            quality_modifier=0.8,
            stamina_modifier=0.7,
            icon="⛈️",
            duration_range=(1, 2)
        ),
        WeatherType.SNOWY: WeatherEffect(
            weather_type=WeatherType.SNOWY,
            name="下雪",
            description="银装素裹，作物休眠",
            growth_modifier=0.3,
            water_modifier=0.5,
            crop_damage_chance=0.1,
            quality_modifier=0.9,
            stamina_modifier=0.8,
            icon="❄️",
            duration_range=(1, 5)
        ),
        WeatherType.WINDY: WeatherEffect(
            weather_type=WeatherType.WINDY,
            name="大风",
            description="狂风呼啸，注意防护",
            growth_modifier=0.9,
            water_modifier=1.2,
            crop_damage_chance=0.08,
            quality_modifier=0.95,
            stamina_modifier=0.9,
            icon="💨",
            duration_range=(1, 3)
        ),
        WeatherType.FOGGY: WeatherEffect(
            weather_type=WeatherType.FOGGY,
            name="大雾",
            description="雾气弥漫，视野受限",
            growth_modifier=0.95,
            water_modifier=0.8,
            crop_damage_chance=0.0,
            quality_modifier=1.0,
            stamina_modifier=1.0,
            icon="🌫️",
            duration_range=(1, 2)
        ),
        WeatherType.DROUGHT: WeatherEffect(
            weather_type=WeatherType.DROUGHT,
            name="干旱",
            description="久旱无雨，急需浇水",
            growth_modifier=0.6,
            water_modifier=2.0,
            crop_damage_chance=0.15,
            quality_modifier=0.7,
            stamina_modifier=1.2,
            icon="🏜️",
            duration_range=(3, 7)
        ),
        WeatherType.HEATWAVE: WeatherEffect(
            weather_type=WeatherType.HEATWAVE,
            name="热浪",
            description="酷暑难耐，作物易枯萎",
            growth_modifier=0.7,
            water_modifier=2.5,
            crop_damage_chance=0.2,
            quality_modifier=0.6,
            stamina_modifier=1.3,
            icon="🔥",
            duration_range=(2, 5)
        ),
    }
    
    SEASON_WEATHER_WEIGHTS = {
        Season.SPRING: {
            WeatherType.SUNNY: 30,
            WeatherType.CLOUDY: 25,
            WeatherType.RAINY: 30,
            WeatherType.STORMY: 5,
            WeatherType.WINDY: 8,
            WeatherType.FOGGY: 2,
        },
        Season.SUMMER: {
            WeatherType.SUNNY: 40,
            WeatherType.CLOUDY: 15,
            WeatherType.RAINY: 15,
            WeatherType.STORMY: 10,
            WeatherType.DROUGHT: 10,
            WeatherType.HEATWAVE: 10,
        },
        Season.AUTUMN: {
            WeatherType.SUNNY: 25,
            WeatherType.CLOUDY: 30,
            WeatherType.RAINY: 25,
            WeatherType.WINDY: 15,
            WeatherType.FOGGY: 5,
        },
        Season.WINTER: {
            WeatherType.SUNNY: 20,
            WeatherType.CLOUDY: 30,
            WeatherType.SNOWY: 35,
            WeatherType.WINDY: 10,
            WeatherType.FOGGY: 5,
        }
    }
    
    @classmethod
    def get_weather_effect(cls, weather_type: WeatherType) -> Optional[WeatherEffect]:
        return cls.WEATHER_EFFECTS.get(weather_type)
    
    @classmethod
    def get_random_weather(cls, season: Season) -> WeatherType:
        weights = cls.SEASON_WEATHER_WEIGHTS.get(season, cls.SEASON_WEATHER_WEIGHTS[Season.SPRING])
        
        weather_types = list(weights.keys())
        weight_values = list(weights.values())
        
        return random.choices(weather_types, weights=weight_values)[0]


@dataclass
class CropWeatherInteraction:
    crop_type: str
    preferred_weather: List[WeatherType]
    avoided_weather: List[WeatherType]
    weather_growth_bonus: Dict[WeatherType, float] = field(default_factory=dict)
    weather_damage_bonus: Dict[WeatherType, float] = field(default_factory=dict)
    
    def get_growth_modifier(self, weather_type: WeatherType) -> float:
        base = 1.0
        
        if weather_type in self.preferred_weather:
            base += 0.2
        elif weather_type in self.avoided_weather:
            base -= 0.3
        
        base *= self.weather_growth_bonus.get(weather_type, 1.0)
        
        return max(0.1, base)
    
    def get_damage_chance(self, weather_type: WeatherType, base_damage: float) -> float:
        damage = base_damage
        damage *= self.weather_damage_bonus.get(weather_type, 1.0)
        
        if weather_type in self.avoided_weather:
            damage *= 1.5
        
        return min(1.0, damage)


class CropWeatherRegistry:
    
    CROP_WEATHER_DATA = {
        "土豆": CropWeatherInteraction(
            crop_type="土豆",
            preferred_weather=[WeatherType.CLOUDY, WeatherType.RAINY],
            avoided_weather=[WeatherType.HEATWAVE, WeatherType.DROUGHT],
            weather_growth_bonus={WeatherType.RAINY: 1.2},
            weather_damage_bonus={WeatherType.HEATWAVE: 2.0}
        ),
        "胡萝卜": CropWeatherInteraction(
            crop_type="胡萝卜",
            preferred_weather=[WeatherType.SUNNY, WeatherType.CLOUDY],
            avoided_weather=[WeatherType.STORMY],
            weather_growth_bonus={WeatherType.SUNNY: 1.15}
        ),
        "小麦": CropWeatherInteraction(
            crop_type="小麦",
            preferred_weather=[WeatherType.SUNNY],
            avoided_weather=[WeatherType.STORMY, WeatherType.SNOWY],
            weather_growth_bonus={WeatherType.SUNNY: 1.1}
        ),
        "番茄": CropWeatherInteraction(
            crop_type="番茄",
            preferred_weather=[WeatherType.SUNNY, WeatherType.HEATWAVE],
            avoided_weather=[WeatherType.SNOWY, WeatherType.FOGGY],
            weather_growth_bonus={WeatherType.SUNNY: 1.25, WeatherType.HEATWAVE: 1.1},
            weather_damage_bonus={WeatherType.SNOWY: 3.0}
        ),
        "玉米": CropWeatherInteraction(
            crop_type="玉米",
            preferred_weather=[WeatherType.SUNNY],
            avoided_weather=[WeatherType.STORMY, WeatherType.WINDY],
            weather_growth_bonus={WeatherType.SUNNY: 1.2},
            weather_damage_bonus={WeatherType.STORMY: 1.5, WeatherType.WINDY: 1.3}
        ),
        "南瓜": CropWeatherInteraction(
            crop_type="南瓜",
            preferred_weather=[WeatherType.SUNNY, WeatherType.CLOUDY],
            avoided_weather=[WeatherType.RAINY, WeatherType.SNOWY],
            weather_growth_bonus={WeatherType.SUNNY: 1.15}
        ),
        "西瓜": CropWeatherInteraction(
            crop_type="西瓜",
            preferred_weather=[WeatherType.SUNNY, WeatherType.HEATWAVE],
            avoided_weather=[WeatherType.SNOWY, WeatherType.FOGGY],
            weather_growth_bonus={WeatherType.HEATWAVE: 1.3},
            weather_damage_bonus={WeatherType.SNOWY: 5.0}
        ),
        "草莓": CropWeatherInteraction(
            crop_type="草莓",
            preferred_weather=[WeatherType.CLOUDY, WeatherType.RAINY],
            avoided_weather=[WeatherType.HEATWAVE, WeatherType.DROUGHT],
            weather_growth_bonus={WeatherType.RAINY: 1.2},
            weather_damage_bonus={WeatherType.HEATWAVE: 2.5}
        ),
        "葡萄": CropWeatherInteraction(
            crop_type="葡萄",
            preferred_weather=[WeatherType.SUNNY],
            avoided_weather=[WeatherType.RAINY, WeatherType.SNOWY],
            weather_growth_bonus={WeatherType.SUNNY: 1.2},
            weather_damage_bonus={WeatherType.RAINY: 1.5}
        ),
    }
    
    @classmethod
    def get_crop_weather_data(cls, crop_type: str) -> Optional[CropWeatherInteraction]:
        return cls.CROP_WEATHER_DATA.get(crop_type)
    
    @classmethod
    def get_crop_growth_modifier(cls, crop_type: str, weather_type: WeatherType) -> float:
        crop_data = cls.get_crop_weather_data(crop_type)
        if crop_data:
            return crop_data.get_growth_modifier(weather_type)
        return 1.0
    
    @classmethod
    def get_crop_damage_chance(cls, crop_type: str, weather_type: WeatherType, base_damage: float) -> float:
        crop_data = cls.get_crop_weather_data(crop_type)
        if crop_data:
            return crop_data.get_damage_chance(weather_type, base_damage)
        return base_damage


class WeatherAgricultureSystem:
    
    def __init__(self):
        self.current_weather: WeatherType = WeatherType.SUNNY
        self.weather_duration: int = 1
        self.days_remaining: int = 1
        self.forecast: List[WeatherForecast] = []
        self.weather_history: List[Tuple[int, WeatherType]] = []
    
    def set_weather(self, weather_type: WeatherType, duration: int = 1):
        self.current_weather = weather_type
        self.weather_duration = duration
        self.days_remaining = duration
    
    def generate_weather(self, season: Season, day: int):
        new_weather = WeatherEffects.get_random_weather(season)
        effect = WeatherEffects.get_weather_effect(new_weather)
        
        if effect:
            min_dur, max_dur = effect.duration_range
            duration = random.randint(min_dur, max_dur)
        else:
            duration = 1
        
        self.set_weather(new_weather, duration)
        self.weather_history.append((day, new_weather))
        
        if len(self.weather_history) > 30:
            self.weather_history.pop(0)
    
    def advance_day(self) -> Dict:
        result = {
            "weather_changed": False,
            "new_weather": None,
            "effects": {}
        }
        
        self.days_remaining -= 1
        
        if self.days_remaining <= 0:
            result["weather_changed"] = True
            result["new_weather"] = self.current_weather
        
        effect = WeatherEffects.get_weather_effect(self.current_weather)
        if effect:
            result["effects"] = {
                "growth_modifier": effect.growth_modifier,
                "water_modifier": effect.water_modifier,
                "crop_damage_chance": effect.crop_damage_chance,
                "quality_modifier": effect.quality_modifier,
                "stamina_modifier": effect.stamina_modifier
            }
        
        return result
    
    def get_crop_growth_modifier(self, crop_type: str) -> float:
        weather_effect = WeatherEffects.get_weather_effect(self.current_weather)
        if not weather_effect:
            return 1.0
        
        base_modifier = weather_effect.growth_modifier
        crop_modifier = CropWeatherRegistry.get_crop_growth_modifier(crop_type, self.current_weather)
        
        return base_modifier * crop_modifier
    
    def check_crop_damage(self, crop_type: str) -> Tuple[bool, str]:
        weather_effect = WeatherEffects.get_weather_effect(self.current_weather)
        if not weather_effect or weather_effect.crop_damage_chance <= 0:
            return False, ""
        
        damage_chance = CropWeatherRegistry.get_crop_damage_chance(
            crop_type, 
            self.current_weather, 
            weather_effect.crop_damage_chance
        )
        
        if random.random() < damage_chance:
            return True, f"{weather_effect.icon} {weather_effect.name}导致{crop_type}受损"
        
        return False, ""
    
    def get_water_need(self) -> float:
        weather_effect = WeatherEffects.get_weather_effect(self.current_weather)
        if weather_effect:
            return weather_effect.water_modifier
        return 1.0
    
    def auto_water_check(self) -> bool:
        return self.current_weather in [WeatherType.RAINY, WeatherType.STORMY]
    
    def get_stamina_modifier(self) -> float:
        weather_effect = WeatherEffects.get_weather_effect(self.current_weather)
        if weather_effect:
            return weather_effect.stamina_modifier
        return 1.0
    
    def generate_forecast(self, season: Season, current_day: int, days: int = 7):
        self.forecast.clear()
        
        for i in range(days):
            forecast_day = current_day + i
            weather = WeatherEffects.get_random_weather(season)
            confidence = max(0.5, 1.0 - i * 0.1)
            
            special_events = []
            if weather == WeatherType.STORMY:
                special_events.append("建议提前收获成熟作物")
            elif weather == WeatherType.DROUGHT:
                special_events.append("注意补充浇水")
            elif weather == WeatherType.HEATWAVE:
                special_events.append("避免中午户外活动")
            
            self.forecast.append(WeatherForecast(
                day=forecast_day,
                weather_type=weather,
                confidence=confidence,
                special_events=special_events
            ))
    
    def get_forecast_display(self) -> List[str]:
        result = []
        for fc in self.forecast:
            effect = WeatherEffects.get_weather_effect(fc.weather_type)
            if effect:
                result.append(f"第{fc.day}天: {effect.icon} {effect.name} (置信度: {int(fc.confidence * 100)}%)")
        return result
    
    def get_weather_display(self) -> str:
        effect = WeatherEffects.get_weather_effect(self.current_weather)
        if effect:
            return f"{effect.icon} {effect.name}"
        return "☀️ 晴天"
    
    def get_weather_info(self) -> Dict:
        effect = WeatherEffects.get_weather_effect(self.current_weather)
        
        return {
            "type": self.current_weather.value,
            "name": effect.name if effect else "晴天",
            "icon": effect.icon if effect else "☀️",
            "description": effect.description if effect else "",
            "duration": self.weather_duration,
            "days_remaining": self.days_remaining,
            "growth_modifier": effect.growth_modifier if effect else 1.0,
            "water_modifier": effect.water_modifier if effect else 1.0,
            "damage_chance": effect.crop_damage_chance if effect else 0.0
        }
    
    def get_save_data(self) -> Dict:
        return {
            "current_weather": self.current_weather.value,
            "weather_duration": self.weather_duration,
            "days_remaining": self.days_remaining,
            "weather_history": [(d, w.value) for d, w in self.weather_history]
        }
    
    def load_save_data(self, data: Dict):
        self.current_weather = WeatherType(data.get("current_weather", "sunny"))
        self.weather_duration = data.get("weather_duration", 1)
        self.days_remaining = data.get("days_remaining", 1)
        
        self.weather_history = []
        for day, weather_str in data.get("weather_history", []):
            try:
                self.weather_history.append((day, WeatherType(weather_str)))
            except ValueError:
                pass
