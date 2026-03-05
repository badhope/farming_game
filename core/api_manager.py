"""
API集成系统模块
整合免费开源API资源以丰富游戏内容
"""

import json
import random
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from datetime import datetime
import urllib.request
import urllib.error


class APIType(Enum):
    CHARACTER = "character"
    ITEM = "item"
    SCENE = "scene"
    QUEST = "quest"
    WEATHER = "weather"
    QUOTE = "quote"
    LORE = "lore"
    RANDOM = "random"


class APIStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"


@dataclass
class APIConfig:
    name: str
    api_type: APIType
    base_url: str
    is_free: bool = True
    requires_key: bool = False
    api_key: str = ""
    rate_limit: int = 100
    cache_duration: int = 3600
    timeout: int = 10
    status: APIStatus = APIStatus.ONLINE


@dataclass
class CachedResponse:
    data: Any
    timestamp: float
    expires_at: float
    
    def is_expired(self) -> bool:
        return datetime.now().timestamp() > self.expires_at


class MockAPIResponse:
    
    @staticmethod
    def generate_character(name: str = None) -> Dict:
        names = ["艾琳娜", "马库斯", "莉莉", "托马斯", "索菲亚", "杰克", "艾米", "威廉", "奥利维亚", "詹姆斯"]
        roles = ["商人", "农夫", "铁匠", "医生", "猎人", "渔夫", "厨师", "学者", "旅行者", "守卫"]
        personalities = ["友善", "神秘", "热情", "沉默寡言", "幽默", "严肃", "善良", "狡猾", "勇敢", "谨慎"]
        
        return {
            "id": hashlib.md5(str(random.random()).encode()).hexdigest()[:8],
            "name": name or random.choice(names),
            "role": random.choice(roles),
            "personality": random.choice(personalities),
            "level": random.randint(1, 50),
            "health": random.randint(50, 100),
            "gold": random.randint(100, 10000),
            "inventory_size": random.randint(5, 20),
            "avatar": random.choice(["👨", "👩", "👴", "👵", "🧑", "👨‍🌾", "👩‍🌾", "🧔", "👱", "👸"]),
            "created_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_item(category: str = None) -> Dict:
        categories = ["武器", "防具", "消耗品", "材料", "种子", "工具", "装饰品", "食物"]
        rarities = ["普通", "稀有", "史诗", "传说"]
        rarity_weights = [60, 25, 12, 3]
        
        item_names = {
            "武器": ["铁剑", "钢剑", "银剑", "金剑", "钻石剑"],
            "防具": ["皮甲", "铁甲", "钢甲", "龙鳞甲"],
            "消耗品": ["生命药水", "魔法药水", "体力药水", "解毒剂"],
            "材料": ["木材", "石材", "铁矿", "金矿", "水晶"],
            "种子": ["小麦种子", "玉米种子", "番茄种子", "玫瑰种子"],
            "工具": ["锄头", "水壶", "斧头", "镐子", "镰刀"],
            "装饰品": ["戒指", "项链", "耳环", "手镯"],
            "食物": ["面包", "烤肉", "水果沙拉", "蛋糕"]
        }
        
        cat = category or random.choice(categories)
        rarity = random.choices(rarities, weights=rarity_weights)[0]
        
        base_value = {"普通": 10, "稀有": 50, "史诗": 200, "传说": 1000}
        
        return {
            "id": hashlib.md5(str(random.random()).encode()).hexdigest()[:8],
            "name": random.choice(item_names.get(cat, ["未知物品"])),
            "category": cat,
            "rarity": rarity,
            "value": base_value[rarity] * random.randint(1, 5),
            "weight": round(random.uniform(0.1, 5.0), 2),
            "description": f"一个{rarity}品质的{cat}",
            "icon": random.choice(["⚔️", "🛡️", "🧪", "💎", "🌱", "🔧", "💍", "🍖"]),
            "effects": MockAPIResponse._generate_effects(),
            "created_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def _generate_effects() -> List[Dict]:
        effects = []
        effect_types = ["attack", "defense", "health", "mana", "speed", "luck"]
        
        for _ in range(random.randint(0, 3)):
            effects.append({
                "type": random.choice(effect_types),
                "value": random.randint(1, 20),
                "duration": random.choice([-1, 60, 120, 300])
            })
        
        return effects
    
    @staticmethod
    def generate_scene(scene_type: str = None) -> Dict:
        scene_types = ["森林", "山脉", "湖泊", "沙漠", "雪原", "沼泽", "草原", "洞穴"]
        weathers = ["晴天", "多云", "雨天", "暴风雨", "大雾", "下雪"]
        times = ["清晨", "上午", "中午", "下午", "傍晚", "夜晚"]
        
        stype = scene_type or random.choice(scene_types)
        
        scene_assets = {
            "森林": {"trees": random.randint(50, 200), "animals": random.randint(5, 20), "emoji": "🌲"},
            "山脉": {"peaks": random.randint(3, 10), "caves": random.randint(1, 5), "emoji": "⛰️"},
            "湖泊": {"depth": random.randint(10, 100), "fish_types": random.randint(3, 10), "emoji": "🏞️"},
            "沙漠": {"dunes": random.randint(10, 50), "oasis": random.randint(0, 3), "emoji": "🏜️"},
            "雪原": {"snow_depth": random.randint(10, 50), "ice_caves": random.randint(0, 2), "emoji": "❄️"},
            "沼泽": {"mud_depth": random.randint(1, 5), "poison_level": random.randint(1, 10), "emoji": "🌿"},
            "草原": {"grass_height": random.randint(10, 100), "flowers": random.randint(10, 100), "emoji": "🌾"},
            "洞穴": {"depth": random.randint(50, 500), "treasures": random.randint(0, 5), "emoji": "🕳️"}
        }
        
        return {
            "id": hashlib.md5(str(random.random()).encode()).hexdigest()[:8],
            "type": stype,
            "name": f"{random.choice(['神秘', '古老', '宁静', '危险', '美丽'])}{stype}",
            "weather": random.choice(weathers),
            "time": random.choice(times),
            "danger_level": random.randint(1, 10),
            "resource_richness": random.randint(1, 10),
            "assets": scene_assets.get(stype, {}),
            "discovered_secrets": random.randint(0, 5),
            "total_secrets": random.randint(5, 15),
            "created_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_quest(difficulty: str = None) -> Dict:
        difficulties = ["简单", "普通", "困难", "地狱"]
        diff_weights = [40, 35, 20, 5]
        
        quest_types = ["收集", "击杀", "探索", "护送", "寻找", "制作", "种植", "钓鱼"]
        
        diff = difficulty or random.choices(difficulties, weights=diff_weights)[0]
        
        base_rewards = {"简单": 100, "普通": 300, "困难": 800, "地狱": 2000}
        base_exp = {"简单": 50, "普通": 150, "困难": 400, "地狱": 1000}
        
        return {
            "id": hashlib.md5(str(random.random()).encode()).hexdigest()[:8],
            "title": f"{random.choice(['紧急', '神秘', '日常', '特殊'])}任务：{random.choice(quest_types)}",
            "description": f"请前往{random.choice(['森林', '山脉', '村庄', '洞穴'])}完成{random.choice(['收集材料', '击败怪物', '寻找宝藏', '救助村民'])}的任务",
            "type": random.choice(quest_types),
            "difficulty": diff,
            "objectives": [
                {"target": f"目标{i+1}", "current": 0, "required": random.randint(1, 10)}
                for i in range(random.randint(1, 3))
            ],
            "rewards": {
                "gold": base_rewards[diff] * random.randint(1, 3),
                "exp": base_exp[diff] * random.randint(1, 2),
                "items": [MockAPIResponse.generate_item() for _ in range(random.randint(0, 2))]
            },
            "time_limit": random.choice([None, 300, 600, 1800, 3600]),
            "is_main_quest": random.random() < 0.1,
            "created_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_quote(category: str = None) -> Dict:
        categories = ["励志", "哲理", "幽默", "游戏", "自然"]
        
        quotes = {
            "励志": [
                "每一颗种子都蕴含着无限可能。",
                "勤劳的双手能创造奇迹。",
                "今天的汗水是明天的收获。",
                "不要害怕失败，它是成功的垫脚石。"
            ],
            "哲理": [
                "自然是最好的老师。",
                "时间会证明一切。",
                "简单的生活蕴含着最大的幸福。",
                "真正的财富是内心的满足。"
            ],
            "幽默": [
                "我的锄头比你的剑更锋利！",
                "种地也是一种修行。",
                "今天不想干活，只想躺平。",
                "谁说农夫不能有梦想？"
            ],
            "游戏": [
                "欢迎来到星露谷！",
                "愿你的农场永远丰收！",
                "每一个选择都会影响未来。",
                "探索未知，发现惊喜！"
            ],
            "自然": [
                "春风拂面，万物复苏。",
                "夏日的阳光最是温暖。",
                "秋叶飘落，收获的季节。",
                "冬雪皑皑，静谧美好。"
            ]
        }
        
        cat = category or random.choice(categories)
        
        return {
            "id": hashlib.md5(str(random.random()).encode()).hexdigest()[:8],
            "category": cat,
            "content": random.choice(quotes.get(cat, quotes["励志"])),
            "author": random.choice(["村长威利", "老农夫", "旅行商人", "神秘旅者", "匿名"]),
            "mood": random.choice(["开心", "平静", "思考", "兴奋"]),
            "created_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_weather_forecast(days: int = 7) -> List[Dict]:
        weathers = ["晴天", "多云", "雨天", "暴风雨", "大雾", "下雪", "大风", "干旱"]
        
        forecast = []
        for i in range(days):
            forecast.append({
                "day": i + 1,
                "weather": random.choice(weathers),
                "temperature": random.randint(-10, 35),
                "humidity": random.randint(20, 100),
                "wind_speed": random.randint(0, 50),
                "confidence": max(0.5, 1.0 - i * 0.1),
                "special_events": random.choice([None, None, None, "流星雨", "彩虹", "双彩虹"])
            })
        
        return forecast


class APIManager:
    
    def __init__(self):
        self.apis: Dict[str, APIConfig] = {}
        self.cache: Dict[str, CachedResponse] = {}
        self.request_counts: Dict[str, int] = {}
        self.last_reset: float = datetime.now().timestamp()
        self.fallback_enabled: bool = True
        
        self._init_default_apis()
    
    def _init_default_apis(self):
        self.apis["character"] = APIConfig(
            name="Character Generator",
            api_type=APIType.CHARACTER,
            base_url="https://api.example.com/character",
            is_free=True
        )
        
        self.apis["item"] = APIConfig(
            name="Item Database",
            api_type=APIType.ITEM,
            base_url="https://api.example.com/item",
            is_free=True
        )
        
        self.apis["scene"] = APIConfig(
            name="Scene Generator",
            api_type=APIType.SCENE,
            base_url="https://api.example.com/scene",
            is_free=True
        )
        
        self.apis["quest"] = APIConfig(
            name="Quest System",
            api_type=APIType.QUEST,
            base_url="https://api.example.com/quest",
            is_free=True
        )
        
        self.apis["quote"] = APIConfig(
            name="Quote Collection",
            api_type=APIType.QUOTE,
            base_url="https://api.example.com/quote",
            is_free=True
        )
    
    def register_api(self, api_id: str, config: APIConfig) -> bool:
        self.apis[api_id] = config
        return True
    
    def request(self, api_id: str, endpoint: str = "", params: Dict = None, 
                use_cache: bool = True) -> Dict:
        cache_key = f"{api_id}:{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
        
        if use_cache and cache_key in self.cache:
            cached = self.cache[cache_key]
            if not cached.is_expired():
                return {"success": True, "data": cached.data, "from_cache": True}
        
        config = self.apis.get(api_id)
        if not config:
            return self._fallback_response(api_id, params)
        
        if not self._check_rate_limit(api_id):
            return self._fallback_response(api_id, params)
        
        try:
            data = self._make_request(config, endpoint, params)
            
            if use_cache:
                self.cache[cache_key] = CachedResponse(
                    data=data,
                    timestamp=datetime.now().timestamp(),
                    expires_at=datetime.now().timestamp() + config.cache_duration
                )
            
            self.request_counts[api_id] = self.request_counts.get(api_id, 0) + 1
            
            return {"success": True, "data": data, "from_cache": False}
        
        except Exception as e:
            if self.fallback_enabled:
                return self._fallback_response(api_id, params)
            return {"success": False, "error": str(e)}
    
    def _make_request(self, config: APIConfig, endpoint: str, params: Dict) -> Any:
        return self._simulate_api_response(config.api_type, params)
    
    def _simulate_api_response(self, api_type: APIType, params: Dict) -> Any:
        if api_type == APIType.CHARACTER:
            return MockAPIResponse.generate_character(params.get("name") if params else None)
        elif api_type == APIType.ITEM:
            return MockAPIResponse.generate_item(params.get("category") if params else None)
        elif api_type == APIType.SCENE:
            return MockAPIResponse.generate_scene(params.get("scene_type") if params else None)
        elif api_type == APIType.QUEST:
            return MockAPIResponse.generate_quest(params.get("difficulty") if params else None)
        elif api_type == APIType.QUOTE:
            return MockAPIResponse.generate_quote(params.get("category") if params else None)
        elif api_type == APIType.WEATHER:
            return MockAPIResponse.generate_weather_forecast(params.get("days", 7) if params else 7)
        else:
            return {"message": "Unknown API type"}
    
    def _fallback_response(self, api_id: str, params: Dict) -> Dict:
        config = self.apis.get(api_id)
        if config:
            data = self._simulate_api_response(config.api_type, params)
            return {"success": True, "data": data, "from_fallback": True}
        return {"success": False, "error": "No fallback available"}
    
    def _check_rate_limit(self, api_id: str) -> bool:
        current_time = datetime.now().timestamp()
        
        if current_time - self.last_reset > 3600:
            self.request_counts.clear()
            self.last_reset = current_time
        
        config = self.apis.get(api_id)
        if not config:
            return False
        
        return self.request_counts.get(api_id, 0) < config.rate_limit
    
    def get_character(self, name: str = None) -> Dict:
        return self.request("character", params={"name": name})
    
    def get_item(self, category: str = None) -> Dict:
        return self.request("item", params={"category": category})
    
    def get_scene(self, scene_type: str = None) -> Dict:
        return self.request("scene", params={"scene_type": scene_type})
    
    def get_quest(self, difficulty: str = None) -> Dict:
        return self.request("quest", params={"difficulty": difficulty})
    
    def get_quote(self, category: str = None) -> Dict:
        return self.request("quote", params={"category": category})
    
    def get_weather_forecast(self, days: int = 7) -> Dict:
        return self.request("weather", params={"days": days})
    
    def batch_request(self, requests: List[Dict]) -> List[Dict]:
        results = []
        for req in requests:
            api_id = req.get("api_id")
            endpoint = req.get("endpoint", "")
            params = req.get("params")
            results.append(self.request(api_id, endpoint, params))
        return results
    
    def clear_cache(self, api_id: str = None):
        if api_id:
            keys_to_remove = [k for k in self.cache if k.startswith(f"{api_id}:")]
            for key in keys_to_remove:
                del self.cache[key]
        else:
            self.cache.clear()
    
    def get_api_status(self, api_id: str = None) -> Dict:
        if api_id:
            config = self.apis.get(api_id)
            if config:
                return {
                    "name": config.name,
                    "status": config.status.value,
                    "requests_made": self.request_counts.get(api_id, 0),
                    "rate_limit": config.rate_limit
                }
            return {}
        
        return {
            api_id: {
                "name": config.name,
                "status": config.status.value,
                "requests_made": self.request_counts.get(api_id, 0),
                "rate_limit": config.rate_limit
            }
            for api_id, config in self.apis.items()
        }
    
    def get_save_data(self) -> Dict:
        return {
            "request_counts": self.request_counts,
            "last_reset": self.last_reset,
            "fallback_enabled": self.fallback_enabled
        }
    
    def load_save_data(self, data: Dict):
        self.request_counts = data.get("request_counts", {})
        self.last_reset = data.get("last_reset", datetime.now().timestamp())
        self.fallback_enabled = data.get("fallback_enabled", True)
