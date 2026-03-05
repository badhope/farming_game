"""
NPC系统模块
管理游戏中的NPC角色和社交互动
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class NPCOccupation(Enum):
    VILLAGE_HEAD = "村长"
    MERCHANT = "商人"
    FARMER = "农夫"
    RANCHER = "牧场主"
    CARPENTER = "木匠"
    SHOPKEEPER = "店主"
    CHEF = "厨师"
    FLORIST = "花店老板"


class RelationshipLevel(Enum):
    STRANGER = "陌生人"
    ACQUAINTANCE = "点头之交"
    FRIEND = "朋友"
    GOOD_FRIEND = "好朋友"
    BEST_FRIEND = "挚友"
    FAMILY = "家人"


@dataclass
class NPCSchedule:
    morning_location: str = "家"
    afternoon_location: str = "工作地点"
    evening_location: str = "广场"
    night_location: str = "家"


@dataclass
class NPCDialogue:
    greeting: str = "你好！"
    farewell: str = "再见！"
    low_friendship: List[str] = field(default_factory=list)
    medium_friendship: List[str] = field(default_factory=list)
    high_friendship: List[str] = field(default_factory=list)
    special_dialogues: Dict[str, str] = field(default_factory=dict)


@dataclass
class NPC:
    id: str
    name: str
    occupation: NPCOccupation
    emoji: str
    description: str
    friendship: int = 0
    max_friendship: int = 1000
    talked_today: bool = False
    gifted_today: bool = False
    birthday: Optional[Tuple[int, int]] = None
    loved_gifts: List[str] = field(default_factory=list)
    liked_gifts: List[str] = field(default_factory=list)
    neutral_gifts: List[str] = field(default_factory=list)
    hated_gifts: List[str] = field(default_factory=list)
    schedule: NPCSchedule = field(default_factory=NPCSchedule)
    dialogue: NPCDialogue = field(default_factory=NPCDialogue)
    quests_given: List[str] = field(default_factory=list)
    
    @property
    def relationship_level(self) -> RelationshipLevel:
        percentage = self.friendship / self.max_friendship
        if percentage >= 0.9:
            return RelationshipLevel.FAMILY
        elif percentage >= 0.7:
            return RelationshipLevel.BEST_FRIEND
        elif percentage >= 0.5:
            return RelationshipLevel.GOOD_FRIEND
        elif percentage >= 0.3:
            return RelationshipLevel.FRIEND
        elif percentage >= 0.1:
            return RelationshipLevel.ACQUAINTANCE
        return RelationshipLevel.STRANGER
    
    def add_friendship(self, amount: int) -> Tuple[bool, str]:
        old_level = self.relationship_level
        self.friendship = min(self.max_friendship, self.friendship + amount)
        new_level = self.relationship_level
        
        if new_level != old_level:
            return (True, f"与{self.name}的关系提升到了【{new_level.value}】！")
        return (False, "")
    
    def can_talk(self) -> bool:
        return not self.talked_today
    
    def talk(self) -> Tuple[bool, str]:
        if not self.can_talk():
            return (False, "今天已经和TA聊过天了")
        
        self.talked_today = True
        self.add_friendship(10)
        
        dialogue = self._get_appropriate_dialogue()
        return (True, dialogue)
    
    def can_gift(self) -> bool:
        return not self.gifted_today
    
    def give_gift(self, gift_name: str) -> Tuple[bool, int, str]:
        if not self.can_gift():
            return (False, 0, "今天已经送过礼物了")
        
        self.gifted_today = True
        reaction = ""
        points = 0
        
        if gift_name in self.loved_gifts:
            points = 80
            reaction = f"哇！这是我最喜欢的东西！太感谢你了！"
        elif gift_name in self.liked_gifts:
            points = 40
            reaction = f"这个我很喜欢，谢谢你！"
        elif gift_name in self.hated_gifts:
            points = -20
            reaction = f"呃...这个我不太喜欢..."
        else:
            points = 10
            reaction = f"谢谢你的礼物。"
        
        self.add_friendship(points)
        return (True, points, reaction)
    
    def _get_appropriate_dialogue(self) -> str:
        percentage = self.friendship / self.max_friendship
        
        if percentage >= 0.7:
            dialogues = self.dialogue.high_friendship or ["今天天气真不错！"]
        elif percentage >= 0.3:
            dialogues = self.dialogue.medium_friendship or ["你好啊！"]
        else:
            dialogues = self.dialogue.low_friendship or ["..."]
        
        return random.choice(dialogues)
    
    def new_day(self):
        self.talked_today = False
        self.gifted_today = False
    
    def get_location(self, time_of_day: str) -> str:
        locations = {
            "morning": self.schedule.morning_location,
            "afternoon": self.schedule.afternoon_location,
            "evening": self.schedule.evening_location,
            "night": self.schedule.night_location
        }
        return locations.get(time_of_day, "家")


class NPCManager:
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self._init_npcs()
    
    def _init_npcs(self):
        npc_data = [
            NPC(
                id="wang_elder",
                name="王大爷",
                occupation=NPCOccupation.VILLAGE_HEAD,
                emoji="👴",
                description="宁静村的村长，慈祥的老人，对年轻人很照顾。",
                dialogue=NPCDialogue(
                    greeting="你好啊，年轻人！",
                    farewell="有空常来坐坐！",
                    low_friendship=["欢迎来到宁静村！", "有什么需要帮助的吗？"],
                    medium_friendship=["你的农场经营得不错！", "村里的人都很喜欢你。"],
                    high_friendship=["你就像我的孩子一样！", "看到你成长我很欣慰。"],
                    special_dialogues={
                        "spring": "春天来了，是播种的好时节！",
                        "summer": "夏天要注意给作物浇水啊。",
                        "autumn": "秋天是收获的季节！",
                        "winter": "冬天要好好休息，为来年做准备。"
                    }
                ),
                loved_gifts=["金苹果", "玫瑰"],
                liked_gifts=["向日葵", "玉米", "南瓜"],
                schedule=NPCSchedule("家", "村委会", "广场", "家")
            ),
            NPC(
                id="aunt_li",
                name="李婶",
                occupation=NPCOccupation.FARMER,
                emoji="👩",
                description="热心的邻居，经常给玩家送来种子和蔬菜。",
                dialogue=NPCDialogue(
                    greeting="哎呀，来啦！",
                    farewell="有空来我家喝茶！",
                    low_friendship=["你刚来村子吧？有什么不懂的问我！"],
                    medium_friendship=["你的农场越来越好了！", "我给你带了一些种子。"],
                    high_friendship=["你就像我自己的孩子！", "有什么困难尽管说！"]
                ),
                loved_gifts=["草莓", "郁金香"],
                liked_gifts=["胡萝卜", "白菜", "番茄"],
                schedule=NPCSchedule("家", "农田", "广场", "家")
            ),
            NPC(
                id="merchant_zhang",
                name="张商人",
                occupation=NPCOccupation.MERCHANT,
                emoji="🧔",
                description="神秘的旅行商人，出售稀有物品。",
                dialogue=NPCDialogue(
                    greeting="欢迎光临！",
                    farewell="期待下次见面！",
                    low_friendship=["看看有什么需要的？"],
                    medium_friendship=["你是我的老顾客了！", "给你打个折吧。"],
                    high_friendship=["我特意给你留了些好东西！", "你是我最好的顾客！"]
                ),
                loved_gifts=["葡萄", "玫瑰"],
                liked_gifts=["西瓜", "向日葵"],
                schedule=NPCSchedule("旅馆", "商店", "广场", "旅馆")
            ),
            NPC(
                id="carpenter_liu",
                name="刘木匠",
                occupation=NPCOccupation.CARPENTER,
                emoji="👨",
                description="村里的木匠，可以帮玩家升级农场建筑。",
                dialogue=NPCDialogue(
                    greeting="需要帮忙吗？",
                    farewell="有活儿随时找我！",
                    low_friendship=["我是村里的木匠。", "农场扩建可以找我。"],
                    medium_friendship=["你的农场发展得不错！", "升级建筑可以提高效率。"],
                    high_friendship=["你是我最好的客户！", "有什么大工程尽管说！"]
                ),
                loved_gifts=["南瓜", "向日葵"],
                liked_gifts=["玉米", "小麦"],
                schedule=NPCSchedule("家", "木工坊", "酒馆", "家")
            ),
            NPC(
                id="chef_chen",
                name="陈大厨",
                occupation=NPCOccupation.CHEF,
                emoji="👨‍🍳",
                description="村里餐厅的厨师，经常收购农产品。",
                dialogue=NPCDialogue(
                    greeting="新鲜食材！",
                    farewell="下次再来！",
                    low_friendship=["我需要新鲜的食材。", "有农产品可以卖给我。"],
                    medium_friendship=["你的农产品品质不错！", "我给你开个好价钱。"],
                    high_friendship=["你是最好的供应商！", "我特意为你研发了新菜！"]
                ),
                loved_gifts=["番茄", "玉米", "南瓜"],
                liked_gifts=["胡萝卜", "土豆", "白菜"],
                schedule=NPCSchedule("家", "餐厅", "市场", "家")
            ),
            NPC(
                id="florist_xiaomei",
                name="小美",
                occupation=NPCOccupation.FLORIST,
                emoji="👧",
                description="花店的年轻女孩，热爱花卉，性格开朗。",
                dialogue=NPCDialogue(
                    greeting="你好呀！",
                    farewell="下次再来玩！",
                    low_friendship=["你喜欢花吗？", "我家的花都很漂亮哦！"],
                    medium_friendship=["你种的花真好看！", "我们可以交流养花心得！"],
                    high_friendship=["你是我最好的朋友！", "这些花送给你！"]
                ),
                loved_gifts=["玫瑰", "郁金香", "向日葵"],
                liked_gifts=["草莓", "葡萄"],
                schedule=NPCSchedule("家", "花店", "广场", "家")
            ),
            NPC(
                id="rancher_zhao",
                name="赵牧场主",
                occupation=NPCOccupation.RANCHER,
                emoji="🧑",
                description="经验丰富的牧场主，可以教玩家饲养动物。",
                dialogue=NPCDialogue(
                    greeting="你好！",
                    farewell="有空来牧场看看！",
                    low_friendship=["想养动物吗？", "动物需要细心照料。"],
                    medium_friendship=["你的动物养得不错！", "养动物要有耐心。"],
                    high_friendship=["你是个天生的牧场主！", "这些饲料送给你！"]
                ),
                loved_gifts=["羊毛", "牛奶", "鸡蛋"],
                liked_gifts=["玉米", "小麦"],
                schedule=NPCSchedule("家", "牧场", "酒馆", "家")
            ),
            NPC(
                id="shopkeeper_wang",
                name="王店主",
                occupation=NPCOccupation.SHOPKEEPER,
                emoji="👨",
                description="杂货店老板，出售各种日用品和种子。",
                dialogue=NPCDialogue(
                    greeting="欢迎光临！",
                    farewell="慢走！",
                    low_friendship=["看看需要什么？", "种子和工具都有。"],
                    medium_friendship=["你是老顾客了！", "给你优惠。"],
                    high_friendship=["你是我最好的顾客！", "有好东西我会先留给你！"]
                ),
                loved_gifts=["葡萄", "西瓜"],
                liked_gifts=["番茄", "玉米"],
                schedule=NPCSchedule("家", "杂货店", "广场", "家")
            )
        ]
        
        for npc in npc_data:
            self.npcs[npc.id] = npc
    
    def get_npc(self, npc_id: str) -> Optional[NPC]:
        return self.npcs.get(npc_id)
    
    def get_all_npcs(self) -> List[NPC]:
        return list(self.npcs.values())
    
    def get_npc_by_occupation(self, occupation: NPCOccupation) -> List[NPC]:
        return [npc for npc in self.npcs.values() if npc.occupation == occupation]
    
    def talk_to_npc(self, npc_id: str) -> Tuple[bool, str]:
        npc = self.get_npc(npc_id)
        if not npc:
            return (False, "找不到这个人")
        return npc.talk()
    
    def give_gift_to_npc(self, npc_id: str, gift_name: str) -> Tuple[bool, int, str]:
        npc = self.get_npc(npc_id)
        if not npc:
            return (False, 0, "找不到这个人")
        return npc.give_gift(gift_name)
    
    def new_day(self):
        for npc in self.npcs.values():
            npc.new_day()
    
    def get_npc_at_location(self, location: str, time_of_day: str) -> List[NPC]:
        result = []
        for npc in self.npcs.values():
            if npc.get_location(time_of_day) == location:
                result.append(npc)
        return result
    
    def to_dict(self) -> dict:
        return {
            npc_id: {
                "friendship": npc.friendship,
                "talked_today": npc.talked_today,
                "gifted_today": npc.gifted_today
            }
            for npc_id, npc in self.npcs.items()
        }
    
    def from_dict(self, data: dict):
        for npc_id, npc_data in data.items():
            npc = self.npcs.get(npc_id)
            if npc:
                npc.friendship = npc_data.get("friendship", 0)
                npc.talked_today = npc_data.get("talked_today", False)
                npc.gifted_today = npc_data.get("gifted_today", False)
