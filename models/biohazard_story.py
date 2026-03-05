"""
生化危机世界观剧情系统模块
提供完整的生化世界观设定、主线剧情和分支剧情
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import random


class InfectionLevel(Enum):
    CLEAN = 0
    EXPOSED = 1
    INFECTED = 2
    CRITICAL = 3
    MUTATED = 4


class FactionType(Enum):
    SURVIVOR = "survivor"
    RESISTANCE = "resistance"
    SCIENTIST = "scientist"
    MILITARY = "military"
    INFECTED = "infected"
    UNKNOWN = "unknown"


class StoryArcType(Enum):
    MAIN = "main"
    SIDE = "side"
    HIDDEN = "hidden"
    SURVIVAL = "survival"


@dataclass
class WorldLore:
    year: int = 2047
    outbreak_day: int = 0
    current_day: int = 1
    infection_rate: float = 0.0
    safe_zones: List[str] = field(default_factory=list)
    destroyed_areas: List[str] = field(default_factory=list)
    active_mutations: List[str] = field(default_factory=list)
    discovered_cures: List[str] = field(default_factory=list)
    
    def get_world_state_description(self) -> str:
        return f"""
        ═══════════════════════════════════
        🌍 世界状态报告 - 第{self.current_day}天
        ═══════════════════════════════════
        📅 年份: {self.year}年
        🦠 全球感染率: {self.infection_rate * 100:.1f}%
        🏠 安全区数量: {len(self.safe_zones)}
        💀 毁灭区域: {len(self.destroyed_areas)}
        🧬 活跃变异株: {len(self.active_mutations)}
        💊 已发现解药: {len(self.discovered_cures)}
        ═══════════════════════════════════
        """


@dataclass
class StoryKeyPoint:
    point_id: str
    chapter: int
    title: str
    description: str
    trigger_condition: Dict = field(default_factory=dict)
    consequences: Dict = field(default_factory=dict)
    choices: List[Dict] = field(default_factory=list)
    is_completed: bool = False
    rewards: Dict = field(default_factory=dict)


@dataclass
class CharacterMemory:
    character_id: str
    name: str
    faction: FactionType
    trust_level: int = 50
    is_alive: bool = True
    infection_status: InfectionLevel = InfectionLevel.CLEAN
    memories: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    
    def update_trust(self, amount: int) -> int:
        self.trust_level = max(0, min(100, self.trust_level + amount))
        return self.trust_level
    
    def get_relationship_status(self) -> str:
        if self.trust_level >= 80:
            return "🤝 挚友"
        elif self.trust_level >= 60:
            return "😊 信任"
        elif self.trust_level >= 40:
            return "😐 中立"
        elif self.trust_level >= 20:
            return "😠 警惕"
        return "💀 敌对"


class BiohazardStoryManager:
    
    MAIN_STORY_KEY_POINTS = [
        StoryKeyPoint(
            point_id="outbreak_begin",
            chapter=1,
            title="🦠 爆发之日",
            description="""
            2047年3月15日，一个看似平常的早晨。

            你在农场醒来，发现天空呈现出诡异的橙红色。
            收音机里传来断断续续的广播：

            "紧急通知...不明病毒...请待在家中...
            不要接触任何...感染者...重复...不要..."

            远处传来尖叫声，你意识到，世界已经改变了。
            """,
            trigger_condition={"day": 1},
            choices=[
                {"id": "stay_calm", "text": "保持冷静，加固农场", "trust_change": {"self": 10}},
                {"id": "investigate", "text": "前往镇上查看情况", "danger": 0.3},
                {"id": "contact_family", "text": "尝试联系家人", "stress": 0.2}
            ],
            rewards={"item": {"应急物资": 1}, "exp": 50}
        ),
        StoryKeyPoint(
            point_id="first_survivor",
            chapter=1,
            title="👤 第一个幸存者",
            description="""
            第三天，一个浑身是血的人出现在农场门口。

            "求求你...救救我...他们...他们疯了..."

            他看起来像是被什么东西抓伤了，但你不确定是否安全。
            他的眼神中充满了恐惧和绝望。

            你该如何选择？
            """,
            trigger_condition={"day": 3},
            choices=[
                {"id": "help_him", "text": "让他进来并治疗伤口", "karma": 10, "risk": 0.4},
                {"id": "refuse_entry", "text": "拒绝让他进入", "karma": -5},
                {"id": "observe_first", "text": "先观察他的症状", "safe": True}
            ],
            consequences={"help_him": {"new_survivor": "受伤的旅人"}},
            rewards={"exp": 30}
        ),
        StoryKeyPoint(
            point_id="infection_discovery",
            chapter=2,
            title="🔬 感染真相",
            description="""
            在一个废弃的研究所里，你发现了一份机密文件：

            "项目代号：T-病毒
            目的：创造超级士兵
            状态：实验失控
            预计感染范围：全球
            备注：唯一的解药配方藏在..."

            文件的其余部分被撕毁了。
            你意识到这场灾难并非偶然。
            """,
            trigger_condition={"day": 10, "has_item": "研究所钥匙"},
            choices=[
                {"id": "search_more", "text": "继续搜索更多文件", "exp": 100},
                {"id": "take_document", "text": "带走这份文件", "item": "机密文件"},
                {"id": "destroy_evidence", "text": "销毁所有证据", "karma": -20}
            ],
            rewards={"item": {"机密文件": 1}, "exp": 200}
        ),
        StoryKeyPoint(
            point_id="safe_zone",
            chapter=2,
            title="🏠 安全区",
            description="""
            经过艰难的旅程，你终于找到了传说中的安全区。

            高墙、电网、持枪的守卫...这里看起来很安全。
            但你注意到墙上有奇怪的标记，似乎在警告着什么。

            守卫拦住了你："新来的？需要检查。"
            """,
            trigger_condition={"day": 15},
            choices=[
                {"id": "submit_check", "text": "配合检查", "safe": True},
                {"id": "sneak_in", "text": "尝试潜入", "danger": 0.5},
                {"id": "bribe_guard", "text": "贿赂守卫", "cost": 500}
            ],
            rewards={"exp": 150}
        ),
        StoryKeyPoint(
            point_id="mutation_reveal",
            chapter=3,
            title="🧬 变异体",
            description="""
            安全区并不像表面那样安全。

            在深夜，你听到了地下室传来的惨叫声。
            偷偷潜入后，你看到了令人毛骨悚然的一幕：

            科学家们正在进行活体实验，被实验者正在变异...

            "你看到了不该看的东西。"一个声音从背后传来。
            """,
            trigger_condition={"day": 20, "in_safe_zone": True},
            choices=[
                {"id": "fight", "text": "战斗", "danger": 0.7},
                {"id": "escape", "text": "逃跑", "danger": 0.4},
                {"id": "negotiate", "text": "谈判", "charisma_check": 60}
            ],
            rewards={"exp": 300}
        ),
        StoryKeyPoint(
            point_id="cure_hint",
            chapter=3,
            title="💊 解药线索",
            description="""
            从科学家那里，你得知了解药的关键信息：

            "解药的核心成分...在原始感染源附近...
            那个地方...被我们称为'零号区域'...
            没有人从那里活着回来过..."

            地图上标记了一个位置，那是城市的最中心。
            """,
            trigger_condition={"day": 25},
            choices=[
                {"id": "go_to_zero", "text": "前往零号区域", "danger": 0.9},
                {"id": "gather_team", "text": "组建探险队", "safe": True},
                {"id": "find_alternative", "text": "寻找替代方案", "exp": 50}
            ],
            rewards={"item": {"零号区域地图": 1}, "exp": 250}
        ),
        StoryKeyPoint(
            point_id="final_stand",
            chapter=4,
            title="⚔️ 最终决战",
            description="""
            你站在零号区域的入口。

            这里是感染最严重的地方，空气中弥漫着死亡的气息。
            但你知道，解药就在里面。

            身后是你的同伴们，他们信任你，跟随你来到这里。

            "准备好了吗？"有人问道。
            """,
            trigger_condition={"day": 30, "has_item": "零号区域地图"},
            choices=[
                {"id": "charge_in", "text": "直接冲进去", "danger": 0.8},
                {"id": "tactical_entry", "text": "战术进入", "danger": 0.5},
                {"id": "solo_mission", "text": "独自潜入", "danger": 0.6}
            ],
            rewards={"exp": 500}
        ),
        StoryKeyPoint(
            point_id="truth_revealed",
            chapter=4,
            title="📖 真相大白",
            description="""
            在零号区域的核心，你发现了真相：

            这场灾难是一个名为"新世界"的秘密组织策划的。
            他们认为人类需要"进化"，而病毒就是进化的催化剂。

            在实验室中央，你看到了解药的配方。
            但要制造解药，需要付出巨大的代价...
            """,
            trigger_condition={"completed": "final_stand"},
            choices=[
                {"id": "make_cure", "text": "制造解药", "sacrifice": True},
                {"id": "destroy_all", "text": "销毁一切", "ending": "destruction"},
                {"id": "take_control", "text": "掌控病毒", "ending": "power"}
            ],
            rewards={"exp": 1000}
        ),
        StoryKeyPoint(
            point_id="new_dawn",
            chapter=5,
            title="🌅 新的黎明",
            description="""
            解药成功制造并分发。

            感染者开始恢复，世界慢慢回到正轨。
            但你知道，这场灾难留下的伤痕永远不会消失。

            站在农场的废墟上，你望着升起的太阳。
            新的世界正在诞生，而你，是它的见证者。

            恭喜你完成了主线剧情！
            """,
            trigger_condition={"completed": "truth_revealed", "has_item": "解药"},
            choices=[
                {"id": "rebuild", "text": "重建农场", "ending": "hope"},
                {"id": "explore", "text": "探索新世界", "ending": "adventure"},
                {"id": "lead", "text": "成为领袖", "ending": "leader"}
            ],
            rewards={"achievement": "生化危机：幸存者", "exp": 2000, "money": 10000}
        ),
    ]
    
    SIDE_STORIES = [
        {
            "story_id": "lost_child",
            "title": "👧 走失的孩子",
            "description": "在废墟中，你听到了孩子的哭声...",
            "trigger": {"day": 5},
            "choices": [
                {"text": "寻找孩子", "karma": 15, "danger": 0.3},
                {"text": "忽略声音", "karma": -10}
            ]
        },
        {
            "story_id": "supply_convoy",
            "title": "🚚 补给车队",
            "description": "一支补给车队请求护送...",
            "trigger": {"day": 8},
            "choices": [
                {"text": "接受护送", "reward": {"money": 500, "item": "弹药"}},
                {"text": "拒绝", "trust": -5}
            ]
        },
        {
            "story_id": "infected_pet",
            "title": "🐕 感染的宠物",
            "description": "你的宠物似乎被感染了...",
            "trigger": {"day": 12, "has_pet": True},
            "choices": [
                {"text": "尝试治疗", "cost": {"medicine": 5}},
                {"text": "放它离开", "karma": -5},
                {"text": "...", "karma": -20}
            ]
        },
        {
            "story_id": "mysterious_signal",
            "title": "📡 神秘信号",
            "description": "收音机收到一个加密信号...",
            "trigger": {"day": 18},
            "choices": [
                {"text": "尝试解码", "exp": 100},
                {"text": "忽略信号"},
                {"text": "追踪信号源", "danger": 0.5}
            ]
        },
        {
            "story_id": "traitor",
            "title": "🎭 叛徒",
            "description": "你发现有人在暗中与感染者交易...",
            "trigger": {"day": 22, "group_size": 3},
            "choices": [
                {"text": "对质", "danger": 0.4},
                {"text": "暗中调查", "safe": True},
                {"text": "报告领导", "trust": 10}
            ]
        }
    ]
    
    def __init__(self):
        self.world_lore = WorldLore()
        self.current_key_point: Optional[str] = None
        self.completed_points: List[str] = []
        self.character_memories: Dict[str, CharacterMemory] = {}
        self.story_flags: Dict[str, bool] = {}
        self.player_karma: int = 0
        self.player_stress: float = 0.0
        self.on_story_event: Optional[Callable] = None
        
        self._init_characters()
    
    def _init_characters(self):
        default_characters = [
            CharacterMemory("dr_chen", "陈博士", FactionType.SCIENTIST, 60),
            CharacterMemory("captain_miller", "米勒队长", FactionType.MILITARY, 40),
            CharacterMemory("survivor_lily", "莉莉", FactionType.SURVIVOR, 70),
            CharacterMemory("resistance_leader", "反抗军领袖", FactionType.RESISTANCE, 30),
        ]
        
        for char in default_characters:
            self.character_memories[char.character_id] = char
    
    def advance_day(self) -> Dict:
        self.world_lore.current_day += 1
        
        self.world_lore.infection_rate = min(1.0, self.world_lore.infection_rate + random.uniform(0.01, 0.05))
        
        triggered_points = []
        for point in self.MAIN_STORY_KEY_POINTS:
            if point.point_id in self.completed_points:
                continue
            
            if self._check_trigger_condition(point.trigger_condition):
                triggered_points.append(point)
        
        return {
            "day": self.world_lore.current_day,
            "infection_rate": self.world_lore.infection_rate,
            "triggered_events": triggered_points
        }
    
    def _check_trigger_condition(self, condition: Dict) -> bool:
        if "day" in condition and self.world_lore.current_day < condition["day"]:
            return False
        if "completed" in condition and condition["completed"] not in self.completed_points:
            return False
        return True
    
    def start_key_point(self, point_id: str) -> Tuple[bool, str, Optional[StoryKeyPoint]]:
        for point in self.MAIN_STORY_KEY_POINTS:
            if point.point_id == point_id:
                if point_id in self.completed_points:
                    return False, "该剧情已完成", None
                
                self.current_key_point = point_id
                return True, f"开始剧情: {point.title}", point
        
        return False, "未知的剧情节点", None
    
    def make_choice(self, choice_id: str) -> Tuple[bool, str, Dict]:
        if not self.current_key_point:
            return False, "没有进行中的剧情", {}
        
        point = None
        for p in self.MAIN_STORY_KEY_POINTS:
            if p.point_id == self.current_key_point:
                point = p
                break
        
        if not point:
            return False, "剧情数据错误", {}
        
        choice = None
        for c in point.choices:
            if c["id"] == choice_id:
                choice = c
                break
        
        if not choice:
            return False, "无效的选择", {}
        
        results = self._apply_choice_effects(choice)
        
        self.completed_points.append(self.current_key_point)
        self.current_key_point = None
        
        return True, "选择已确认", results
    
    def _apply_choice_effects(self, choice: Dict) -> Dict:
        results = {"effects": [], "rewards": {}}
        
        if "karma" in choice:
            self.player_karma += choice["karma"]
            results["effects"].append(f"业力 {'+' if choice['karma'] > 0 else ''}{choice['karma']}")
        
        if "trust_change" in choice:
            for char_id, change in choice["trust_change"].items():
                if char_id in self.character_memories:
                    new_trust = self.character_memories[char_id].update_trust(change)
                    results["effects"].append(f"{self.character_memories[char_id].name} 信任度: {new_trust}")
        
        if "exp" in choice:
            results["rewards"]["exp"] = choice["exp"]
        
        if "item" in choice:
            results["rewards"]["item"] = choice["item"]
        
        if "danger" in choice:
            if random.random() < choice["danger"]:
                results["effects"].append("⚠️ 遭遇危险！")
                results["danger_encountered"] = True
        
        return results
    
    def get_world_status(self) -> Dict:
        return {
            "day": self.world_lore.current_day,
            "infection_rate": self.world_lore.infection_rate,
            "karma": self.player_karma,
            "stress": self.player_stress,
            "completed_chapters": len(set(p.chapter for p in self.MAIN_STORY_KEY_POINTS if p.point_id in self.completed_points)),
            "total_chapters": 5
        }
    
    def get_character_relationships(self) -> List[Dict]:
        return [
            {
                "name": char.name,
                "faction": char.faction.value,
                "trust": char.trust_level,
                "status": char.get_relationship_status(),
                "alive": char.is_alive,
                "infection": char.infection_status.name
            }
            for char in self.character_memories.values()
        ]
    
    def get_available_side_stories(self) -> List[Dict]:
        available = []
        for story in self.SIDE_STORIES:
            trigger = story["trigger"]
            if "day" in trigger and self.world_lore.current_day >= trigger["day"]:
                available.append(story)
        return available
    
    def get_save_data(self) -> Dict:
        return {
            "world_lore": {
                "current_day": self.world_lore.current_day,
                "infection_rate": self.world_lore.infection_rate,
                "safe_zones": self.world_lore.safe_zones,
                "destroyed_areas": self.world_lore.destroyed_areas,
                "active_mutations": self.world_lore.active_mutations,
                "discovered_cures": self.world_lore.discovered_cures
            },
            "current_key_point": self.current_key_point,
            "completed_points": self.completed_points,
            "story_flags": self.story_flags,
            "player_karma": self.player_karma,
            "player_stress": self.player_stress,
            "character_trust": {
                char_id: char.trust_level 
                for char_id, char in self.character_memories.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        lore_data = data.get("world_lore", {})
        self.world_lore.current_day = lore_data.get("current_day", 1)
        self.world_lore.infection_rate = lore_data.get("infection_rate", 0.0)
        self.world_lore.safe_zones = lore_data.get("safe_zones", [])
        self.world_lore.destroyed_areas = lore_data.get("destroyed_areas", [])
        self.world_lore.active_mutations = lore_data.get("active_mutations", [])
        self.world_lore.discovered_cures = lore_data.get("discovered_cures", [])
        
        self.current_key_point = data.get("current_key_point")
        self.completed_points = data.get("completed_points", [])
        self.story_flags = data.get("story_flags", {})
        self.player_karma = data.get("player_karma", 0)
        self.player_stress = data.get("player_stress", 0.0)
        
        for char_id, trust in data.get("character_trust", {}).items():
            if char_id in self.character_memories:
                self.character_memories[char_id].trust_level = trust
