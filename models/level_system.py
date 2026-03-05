"""
玩家等级系统模块
提供等级成长、经验获取和内容解锁功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum


class UnlockType(Enum):
    CROP = "crop"
    TOOL = "tool"
    BUILDING = "building"
    AREA = "area"
    FEATURE = "feature"
    QUEST = "quest"
    PET = "pet"
    ITEM = "item"


@dataclass
class LevelReward:
    level: int
    exp_required: int
    rewards: Dict = field(default_factory=dict)
    unlocks: List[Dict] = field(default_factory=list)
    title: str = ""
    description: str = ""


@dataclass
class UnlockableContent:
    content_id: str
    unlock_type: UnlockType
    name: str
    description: str
    required_level: int
    icon: str = "🔒"
    is_unlocked: bool = False


class LevelSystem:
    
    LEVEL_DATA = {
        1: LevelReward(
            level=1,
            exp_required=0,
            title="🌱 新手农夫",
            description="刚刚开始农场生活的新人",
            unlocks=[
                {"type": UnlockType.CROP, "id": "土豆"},
                {"type": UnlockType.CROP, "id": "胡萝卜"},
                {"type": UnlockType.CROP, "id": "小麦"},
                {"type": UnlockType.FEATURE, "id": "basic_farming"},
            ]
        ),
        2: LevelReward(
            level=2,
            exp_required=100,
            title="🧑‍🌾 见习农夫",
            description="开始熟悉农作物的生长规律",
            rewards={"money": 200},
            unlocks=[
                {"type": UnlockType.CROP, "id": "白菜"},
                {"type": UnlockType.TOOL, "id": "watering_can_upgrade"},
            ]
        ),
        3: LevelReward(
            level=3,
            exp_required=300,
            title="👨‍🌾 初级农夫",
            description="能够熟练种植基本作物",
            rewards={"money": 500},
            unlocks=[
                {"type": UnlockType.CROP, "id": "番茄"},
                {"type": UnlockType.CROP, "id": "茄子"},
                {"type": UnlockType.FEATURE, "id": "shop_discount"},
            ]
        ),
        4: LevelReward(
            level=4,
            exp_required=600,
            title="🌾 熟练农夫",
            description="对各种作物了如指掌",
            rewards={"money": 800, "seeds": {"玉米": 5}},
            unlocks=[
                {"type": UnlockType.CROP, "id": "玉米"},
                {"type": UnlockType.BUILDING, "id": "greenhouse"},
            ]
        ),
        5: LevelReward(
            level=5,
            exp_required=1000,
            title="🌻 专业农夫",
            description="开始尝试种植高价值作物",
            rewards={"money": 1000},
            unlocks=[
                {"type": UnlockType.CROP, "id": "南瓜"},
                {"type": UnlockType.AREA, "id": "forest"},
                {"type": UnlockType.FEATURE, "id": "exploration"},
            ]
        ),
        6: LevelReward(
            level=6,
            exp_required=1500,
            title="🍉 高级农夫",
            description="农场经营有方，收入稳定",
            rewards={"money": 1500},
            unlocks=[
                {"type": UnlockType.CROP, "id": "西瓜"},
                {"type": UnlockType.PET, "id": "dog"},
                {"type": UnlockType.PET, "id": "cat"},
            ]
        ),
        7: LevelReward(
            level=7,
            exp_required=2200,
            title="🍓 资深农夫",
            description="开始种植珍稀作物",
            rewards={"money": 2000},
            unlocks=[
                {"type": UnlockType.CROP, "id": "草莓"},
                {"type": UnlockType.BUILDING, "id": "barn"},
            ]
        ),
        8: LevelReward(
            level=8,
            exp_required=3000,
            title="🍇 农场专家",
            description="精通各种农业技术",
            rewards={"money": 3000},
            unlocks=[
                {"type": UnlockType.CROP, "id": "葡萄"},
                {"type": UnlockType.AREA, "id": "mountain"},
                {"type": UnlockType.FEATURE, "id": "crafting"},
            ]
        ),
        9: LevelReward(
            level=9,
            exp_required=4000,
            title="🌻 花卉大师",
            description="开始种植美丽的花卉",
            rewards={"money": 4000},
            unlocks=[
                {"type": UnlockType.CROP, "id": "向日葵"},
                {"type": UnlockType.CROP, "id": "玫瑰"},
                {"type": UnlockType.CROP, "id": "郁金香"},
            ]
        ),
        10: LevelReward(
            level=10,
            exp_required=5500,
            title="👑 农场大师",
            description="达到了农业的巅峰",
            rewards={"money": 5000, "achievement": "farm_master"},
            unlocks=[
                {"type": UnlockType.BUILDING, "id": "mansion"},
                {"type": UnlockType.AREA, "id": "secret_garden"},
                {"type": UnlockType.FEATURE, "id": "auto_harvest"},
            ]
        ),
        11: LevelReward(
            level=11,
            exp_required=7500,
            title="⭐ 传奇农夫",
            description="传说中的农场主",
            rewards={"money": 8000},
            unlocks=[
                {"type": UnlockType.CROP, "id": "萝卜"},
                {"type": UnlockType.CROP, "id": "大白菜"},
            ]
        ),
        12: LevelReward(
            level=12,
            exp_required=10000,
            title="🌟 农场之神",
            description="超越了凡人的农业之神",
            rewards={"money": 10000, "achievement": "farm_god"},
            unlocks=[
                {"type": UnlockType.FEATURE, "id": "golden_tools"},
                {"type": UnlockType.FEATURE, "id": "infinite_storage"},
            ]
        ),
    }
    
    MAX_LEVEL = max(LEVEL_DATA.keys())
    
    def __init__(self):
        self.current_level: int = 1
        self.current_exp: int = 0
        self.total_exp: int = 0
        self.unlocked_content: Dict[UnlockType, List[str]] = {
            unlock_type: [] for unlock_type in UnlockType
        }
        self.on_level_up: Optional[Callable] = None
        self.on_unlock: Optional[Callable] = None
        
        self._init_unlocks()
    
    def _init_unlocks(self):
        level_1_data = self.LEVEL_DATA.get(1)
        if level_1_data:
            for unlock in level_1_data.unlocks:
                self._add_unlock(unlock["type"], unlock["id"])
    
    def add_exp(self, amount: int) -> Dict:
        result = {
            "exp_gained": amount,
            "level_ups": [],
            "rewards": [],
            "unlocks": []
        }
        
        self.current_exp += amount
        self.total_exp += amount
        
        while self._can_level_up():
            level_up_result = self._level_up()
            result["level_ups"].append(level_up_result["new_level"])
            if level_up_result.get("rewards"):
                result["rewards"].append(level_up_result["rewards"])
            if level_up_result.get("unlocks"):
                result["unlocks"].extend(level_up_result["unlocks"])
        
        return result
    
    def _can_level_up(self) -> bool:
        if self.current_level >= self.MAX_LEVEL:
            return False
        
        next_level_data = self.LEVEL_DATA.get(self.current_level + 1)
        if next_level_data:
            return self.current_exp >= next_level_data.exp_required
        
        return False
    
    def _level_up(self) -> Dict:
        self.current_level += 1
        
        level_data = self.LEVEL_DATA.get(self.current_level)
        result = {
            "new_level": self.current_level,
            "title": level_data.title if level_data else "",
            "rewards": {},
            "unlocks": []
        }
        
        if level_data:
            result["rewards"] = level_data.rewards.copy()
            
            for unlock in level_data.unlocks:
                self._add_unlock(unlock["type"], unlock["id"])
                result["unlocks"].append(unlock)
        
        if self.on_level_up:
            self.on_level_up(self.current_level, level_data)
        
        return result
    
    def _add_unlock(self, unlock_type: UnlockType, content_id: str):
        if content_id not in self.unlocked_content[unlock_type]:
            self.unlocked_content[unlock_type].append(content_id)
            
            if self.on_unlock:
                self.on_unlock(unlock_type, content_id)
    
    def is_unlocked(self, unlock_type: UnlockType, content_id: str) -> bool:
        return content_id in self.unlocked_content.get(unlock_type, [])
    
    def get_exp_progress(self) -> float:
        if self.current_level >= self.MAX_LEVEL:
            return 1.0
        
        current_level_data = self.LEVEL_DATA.get(self.current_level)
        next_level_data = self.LEVEL_DATA.get(self.current_level + 1)
        
        if not next_level_data:
            return 1.0
        
        current_threshold = current_level_data.exp_required if current_level_data else 0
        next_threshold = next_level_data.exp_required
        
        exp_in_level = self.current_exp - current_threshold
        exp_needed = next_threshold - current_threshold
        
        return min(1.0, exp_in_level / exp_needed) if exp_needed > 0 else 1.0
    
    def get_exp_to_next_level(self) -> int:
        if self.current_level >= self.MAX_LEVEL:
            return 0
        
        next_level_data = self.LEVEL_DATA.get(self.current_level + 1)
        if next_level_data:
            return max(0, next_level_data.exp_required - self.current_exp)
        
        return 0
    
    def get_current_title(self) -> str:
        level_data = self.LEVEL_DATA.get(self.current_level)
        return level_data.title if level_data else "农夫"
    
    def get_level_info(self) -> Dict:
        level_data = self.LEVEL_DATA.get(self.current_level)
        return {
            "level": self.current_level,
            "title": self.get_current_title(),
            "exp": self.current_exp,
            "total_exp": self.total_exp,
            "exp_progress": self.get_exp_progress(),
            "exp_to_next": self.get_exp_to_next_level(),
            "max_level": self.MAX_LEVEL,
            "description": level_data.description if level_data else ""
        }
    
    def get_all_unlocks(self) -> Dict[UnlockType, List[str]]:
        return self.unlocked_content.copy()
    
    def get_unlocks_for_level(self, level: int) -> List[Dict]:
        level_data = self.LEVEL_DATA.get(level)
        return level_data.unlocks if level_data else []
    
    def get_level_rewards(self, level: int) -> Dict:
        level_data = self.LEVEL_DATA.get(level)
        return level_data.rewards if level_data else {}
    
    def get_save_data(self) -> Dict:
        return {
            "current_level": self.current_level,
            "current_exp": self.current_exp,
            "total_exp": self.total_exp,
            "unlocked_content": {
                ut.value: content for ut, content in self.unlocked_content.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.current_level = data.get("current_level", 1)
        self.current_exp = data.get("current_exp", 0)
        self.total_exp = data.get("total_exp", 0)
        
        unlocked_data = data.get("unlocked_content", {})
        for type_str, content_list in unlocked_data.items():
            try:
                unlock_type = UnlockType(type_str)
                self.unlocked_content[unlock_type] = content_list
            except ValueError:
                pass


class ContentUnlockManager:
    
    UNLOCKABLE_CONTENT = {
        UnlockType.CROP: {
            "土豆": UnlockableContent("土豆", UnlockType.CROP, "土豆", "常见蔬菜，生长周期短", 1, "🥔"),
            "胡萝卜": UnlockableContent("胡萝卜", UnlockType.CROP, "胡萝卜", "生长最快的作物", 1, "🥕"),
            "小麦": UnlockableContent("小麦", UnlockType.CROP, "小麦", "最便宜的作物", 1, "🌾"),
            "白菜": UnlockableContent("白菜", UnlockType.CROP, "白菜", "适应性强", 2, "🥬"),
            "番茄": UnlockableContent("番茄", UnlockType.CROP, "番茄", "夏季特产", 3, "🍅"),
            "茄子": UnlockableContent("茄子", UnlockType.CROP, "茄子", "秋季蔬菜", 3, "🍆"),
            "玉米": UnlockableContent("玉米", UnlockType.CROP, "玉米", "适应性强", 4, "🌽"),
            "南瓜": UnlockableContent("南瓜", UnlockType.CROP, "南瓜", "秋季代表", 5, "🎃"),
            "西瓜": UnlockableContent("西瓜", UnlockType.CROP, "西瓜", "夏季高价值水果", 6, "🍉"),
            "草莓": UnlockableContent("草莓", UnlockType.CROP, "草莓", "春季珍品", 7, "🍓"),
            "葡萄": UnlockableContent("葡萄", UnlockType.CROP, "葡萄", "高价值水果", 8, "🍇"),
            "向日葵": UnlockableContent("向日葵", UnlockType.CROP, "向日葵", "夏季花卉", 9, "🌻"),
            "玫瑰": UnlockableContent("玫瑰", UnlockType.CROP, "玫瑰", "美丽花卉", 9, "🌹"),
            "郁金香": UnlockableContent("郁金香", UnlockType.CROP, "郁金香", "春季花卉", 9, "🌷"),
            "萝卜": UnlockableContent("萝卜", UnlockType.CROP, "萝卜", "冬季蔬菜", 11, "🥬"),
            "大白菜": UnlockableContent("大白菜", UnlockType.CROP, "大白菜", "冬季主要蔬菜", 11, "🥬"),
        },
        UnlockType.FEATURE: {
            "basic_farming": UnlockableContent("basic_farming", UnlockType.FEATURE, "基础种植", "基本的种植功能", 1, "🌱"),
            "shop_discount": UnlockableContent("shop_discount", UnlockType.FEATURE, "商店折扣", "购买物品享受9折优惠", 3, "💰"),
            "exploration": UnlockableContent("exploration", UnlockType.FEATURE, "户外探险", "探索未知区域", 5, "🗺️"),
            "crafting": UnlockableContent("crafting", UnlockType.FEATURE, "道具合成", "合成各种道具", 8, "🔨"),
            "auto_harvest": UnlockableContent("auto_harvest", UnlockType.FEATURE, "自动收获", "自动收获成熟作物", 10, "🤖"),
            "golden_tools": UnlockableContent("golden_tools", UnlockType.FEATURE, "黄金工具", "效率提升50%", 12, "✨"),
            "infinite_storage": UnlockableContent("infinite_storage", UnlockType.FEATURE, "无限仓库", "仓库容量无限制", 12, "📦"),
        },
        UnlockType.AREA: {
            "forest": UnlockableContent("forest", UnlockType.AREA, "神秘森林", "探索森林获取资源", 5, "🌲"),
            "mountain": UnlockableContent("mountain", UnlockType.AREA, "高山矿区", "挖掘珍贵矿石", 8, "⛰️"),
            "secret_garden": UnlockableContent("secret_garden", UnlockType.AREA, "秘密花园", "传说中的花园", 10, "🌸"),
        },
        UnlockType.PET: {
            "dog": UnlockableContent("dog", UnlockType.PET, "小狗", "忠诚的伙伴", 6, "🐕"),
            "cat": UnlockableContent("cat", UnlockType.PET, "小猫", "可爱的伙伴", 6, "🐱"),
        },
        UnlockType.BUILDING: {
            "greenhouse": UnlockableContent("greenhouse", UnlockType.BUILDING, "温室", "四季都可种植", 4, "🏡"),
            "barn": UnlockableContent("barn", UnlockType.BUILDING, "畜棚", "饲养动物", 7, "🏠"),
            "mansion": UnlockableContent("mansion", UnlockType.BUILDING, "豪宅", "豪华住宅", 10, "🏰"),
        },
    }
    
    @classmethod
    def get_content_info(cls, unlock_type: UnlockType, content_id: str) -> Optional[UnlockableContent]:
        type_content = cls.UNLOCKABLE_CONTENT.get(unlock_type, {})
        return type_content.get(content_id)
    
    @classmethod
    def get_all_content_for_type(cls, unlock_type: UnlockType) -> Dict[str, UnlockableContent]:
        return cls.UNLOCKABLE_CONTENT.get(unlock_type, {})
    
    @classmethod
    def get_content_for_level(cls, level: int) -> List[UnlockableContent]:
        result = []
        for unlock_type, content_dict in cls.UNLOCKABLE_CONTENT.items():
            for content in content_dict.values():
                if content.required_level == level:
                    result.append(content)
        return result
