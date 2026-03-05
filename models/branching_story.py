"""
分支剧情系统模块
提供基于玩家选择的分支剧情和后果系统
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import random


class ChoiceImpact(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class ConsequenceType(Enum):
    MONEY = "money"
    REPUTATION = "reputation"
    RELATIONSHIP = "relationship"
    ITEM = "item"
    UNLOCK = "unlock"
    STORY = "story"
    WORLD = "world"
    KARMA = "karma"


@dataclass
class Consequence:
    consequence_type: ConsequenceType
    target: str
    value: int
    description: str
    is_permanent: bool = False
    duration: int = 0
    
    def get_display_text(self) -> str:
        sign = "+" if self.value > 0 else ""
        return f"{self.description} ({sign}{self.value})"


@dataclass
class StoryChoice:
    choice_id: str
    text: str
    consequences: List[Consequence] = field(default_factory=list)
    next_node_id: Optional[str] = None
    required_conditions: Dict = field(default_factory=dict)
    impact: ChoiceImpact = ChoiceImpact.NEUTRAL
    hint: str = ""
    
    def can_choose(self, player_state: Dict) -> Tuple[bool, str]:
        for key, value in self.required_conditions.items():
            if player_state.get(key, 0) < value:
                return False, f"需要 {key}: {value}"
        return True, ""
    
    def apply_consequences(self) -> List[str]:
        results = []
        for cons in self.consequences:
            results.append(cons.get_display_text())
        return results


@dataclass
class BranchNode:
    node_id: str
    title: str
    content: str
    speaker: Optional[str] = None
    choices: List[StoryChoice] = field(default_factory=list)
    auto_consequences: List[Consequence] = field(default_factory=list)
    background: str = ""
    mood: str = "normal"
    
    def has_choices(self) -> bool:
        return len(self.choices) > 0
    
    def get_available_choices(self, player_state: Dict) -> List[Tuple[StoryChoice, bool, str]]:
        result = []
        for choice in self.choices:
            can_choose, reason = choice.can_choose(player_state)
            result.append((choice, can_choose, reason))
        return result


@dataclass
class StoryBranch:
    branch_id: str
    name: str
    description: str
    start_node_id: str
    nodes: Dict[str, BranchNode] = field(default_factory=dict)
    is_repeatable: bool = False
    min_level: int = 1
    prerequisites: List[str] = field(default_factory=list)


@dataclass
class WorldState:
    npc_relationships: Dict[str, int] = field(default_factory=dict)
    world_flags: Dict[str, bool] = field(default_factory=dict)
    event_history: List[str] = field(default_factory=list)
    reputation: int = 0
    karma: int = 0
    
    def modify_relationship(self, npc_name: str, amount: int) -> int:
        current = self.npc_relationships.get(npc_name, 50)
        new_value = max(0, min(100, current + amount))
        self.npc_relationships[npc_name] = new_value
        return new_value
    
    def get_relationship_level(self, npc_name: str) -> str:
        value = self.npc_relationships.get(npc_name, 50)
        if value >= 80:
            return "挚友"
        elif value >= 60:
            return "好友"
        elif value >= 40:
            return "普通"
        elif value >= 20:
            return "疏远"
        return "敌对"
    
    def set_flag(self, flag_name: str, value: bool = True):
        self.world_flags[flag_name] = value
    
    def has_flag(self, flag_name: str) -> bool:
        return self.world_flags.get(flag_name, False)
    
    def add_karma(self, amount: int):
        self.karma += amount
        if amount > 0:
            self.reputation += amount // 2
        else:
            self.reputation += amount


class BranchingNarrativeSystem:
    
    MAIN_STORY_BRANCHES = {
        "intro": StoryBranch(
            branch_id="intro",
            name="序章：新的开始",
            description="你刚刚来到星露谷，开始新的农场生活",
            start_node_id="intro_1",
            nodes={
                "intro_1": BranchNode(
                    node_id="intro_1",
                    title="抵达星露谷",
                    content="经过长途跋涉，你终于来到了星露谷。\n\n爷爷留下的农场就在眼前，虽然有些破旧，但充满了希望。\n\n村长威利正在村口等你。",
                    speaker="旁白",
                    choices=[
                        StoryChoice(
                            choice_id="intro_greet_polite",
                            text="礼貌地向村长问好",
                            consequences=[
                                Consequence(ConsequenceType.RELATIONSHIP, "威利", 10, "威利对你的印象很好"),
                            ],
                            next_node_id="intro_2_polite",
                            impact=ChoiceImpact.POSITIVE,
                            hint="建立良好的第一印象"
                        ),
                        StoryChoice(
                            choice_id="intro_greet_casual",
                            text="随意地打个招呼",
                            consequences=[
                                Consequence(ConsequenceType.RELATIONSHIP, "威利", 0, "威利对你点点头"),
                            ],
                            next_node_id="intro_2_casual",
                            impact=ChoiceImpact.NEUTRAL
                        ),
                        StoryChoice(
                            choice_id="intro_greet_cold",
                            text="冷淡地点点头",
                            consequences=[
                                Consequence(ConsequenceType.RELATIONSHIP, "威利", -5, "威利似乎有些失望"),
                            ],
                            next_node_id="intro_2_cold",
                            impact=ChoiceImpact.NEGATIVE
                        )
                    ]
                ),
                "intro_2_polite": BranchNode(
                    node_id="intro_2_polite",
                    title="热情的欢迎",
                    content="「欢迎来到星露谷！我是村长威利。」\n\n威利热情地握住你的手。\n\n「你爷爷是个好人，我相信你也会成为出色的农场主！」\n\n他递给你一袋种子。",
                    speaker="威利",
                    choices=[
                        StoryChoice(
                            choice_id="accept_seeds",
                            text="感激地接过种子",
                            consequences=[
                                Consequence(ConsequenceType.ITEM, "种子包", 1, "获得基础种子包"),
                                Consequence(ConsequenceType.RELATIONSHIP, "威利", 5, "威利很高兴"),
                            ],
                            next_node_id="intro_3",
                            impact=ChoiceImpact.POSITIVE
                        )
                    ]
                ),
                "intro_2_casual": BranchNode(
                    node_id="intro_2_casual",
                    title="平常的相遇",
                    content="「嗯，欢迎。」威利点点头。\n\n「这是你爷爷的农场，希望你能好好经营。」\n\n他递给你一袋种子。",
                    speaker="威利",
                    choices=[
                        StoryChoice(
                            choice_id="accept_seeds_casual",
                            text="接过种子",
                            consequences=[
                                Consequence(ConsequenceType.ITEM, "种子包", 1, "获得基础种子包"),
                            ],
                            next_node_id="intro_3",
                            impact=ChoiceImpact.NEUTRAL
                        )
                    ]
                ),
                "intro_2_cold": BranchNode(
                    node_id="intro_2_cold",
                    title="尴尬的沉默",
                    content="威利看着你，有些尴尬。\n\n「呃...好吧。这是你爷爷的农场。」\n\n他把种子放在地上，转身离开。",
                    speaker="威利",
                    choices=[
                        StoryChoice(
                            choice_id="pick_seeds",
                            text="捡起地上的种子",
                            consequences=[
                                Consequence(ConsequenceType.ITEM, "种子包", 1, "获得基础种子包"),
                            ],
                            next_node_id="intro_3",
                            impact=ChoiceImpact.NEUTRAL
                        )
                    ]
                ),
                "intro_3": BranchNode(
                    node_id="intro_3",
                    title="新的旅程",
                    content="你站在农场入口，望着眼前的一切。\n\n新的生活即将开始，未来会怎样，取决于你的选择。\n\n「祝你好运，年轻人。」远处传来威利的声音。",
                    speaker="旁白",
                    auto_consequences=[
                        Consequence(ConsequenceType.UNLOCK, "tutorial", 1, "解锁新手教程"),
                    ]
                )
            }
        ),
        "merchant_choice": StoryBranch(
            branch_id="merchant_choice",
            name="第一章：商人的抉择",
            description="一个神秘的商人来到村庄，带来了一些特殊的商品",
            start_node_id="merchant_1",
            min_level=3,
            nodes={
                "merchant_1": BranchNode(
                    node_id="merchant_1",
                    title="神秘商人",
                    content="一个穿着华丽长袍的商人出现在村口。\n\n「各位村民，我带来了来自远方的珍稀种子！」\n\n他的货物看起来确实很特别，但价格不菲。",
                    speaker="神秘商人",
                    choices=[
                        StoryChoice(
                            choice_id="buy_expensive",
                            text="花大价钱购买珍稀种子",
                            consequences=[
                                Consequence(ConsequenceType.MONEY, "gold", -500, "花费500金币"),
                                Consequence(ConsequenceType.ITEM, "珍稀种子", 5, "获得珍稀种子"),
                                Consequence(ConsequenceType.REPUTATION, "village", 5, "村民认为你很慷慨"),
                            ],
                            next_node_id="merchant_2_good",
                            impact=ChoiceImpact.POSITIVE,
                            required_conditions={"money": 500}
                        ),
                        StoryChoice(
                            choice_id="buy_normal",
                            text="只买一些普通种子",
                            consequences=[
                                Consequence(ConsequenceType.MONEY, "gold", -100, "花费100金币"),
                                Consequence(ConsequenceType.ITEM, "普通种子", 10, "获得普通种子"),
                            ],
                            next_node_id="merchant_2_neutral",
                            impact=ChoiceImpact.NEUTRAL,
                            required_conditions={"money": 100}
                        ),
                        StoryChoice(
                            choice_id="buy_nothing",
                            text="什么都不买",
                            consequences=[
                                Consequence(ConsequenceType.RELATIONSHIP, "商人", -10, "商人有些失望"),
                            ],
                            next_node_id="merchant_2_bad",
                            impact=ChoiceImpact.NEGATIVE
                        ),
                        StoryChoice(
                            choice_id="warn_villagers",
                            text="警告村民这可能是个骗局",
                            consequences=[
                                Consequence(ConsequenceType.REPUTATION, "village", 10, "村民感谢你的提醒"),
                                Consequence(ConsequenceType.RELATIONSHIP, "商人", -20, "商人愤怒地离开了"),
                            ],
                            next_node_id="merchant_2_warn",
                            impact=ChoiceImpact.MIXED
                        )
                    ]
                ),
                "merchant_2_good": BranchNode(
                    node_id="merchant_2_good",
                    title="慷慨的投资",
                    content="商人露出了灿烂的笑容。\n\n「明智的选择！这些种子会给你带来丰收！」\n\n村民们对你投来赞许的目光。",
                    speaker="神秘商人",
                    auto_consequences=[
                        Consequence(ConsequenceType.UNLOCK, "rare_crops", 1, "解锁珍稀作物种植"),
                    ]
                ),
                "merchant_2_neutral": BranchNode(
                    node_id="merchant_2_neutral",
                    title="平常的交易",
                    content="商人点点头，递给你种子。\n\n「希望下次你能多买一些。」",
                    speaker="神秘商人"
                ),
                "merchant_2_bad": BranchNode(
                    node_id="merchant_2_bad",
                    title="冷淡的告别",
                    content="商人耸耸肩。\n\n「好吧，也许下次你会改变主意。」\n\n他收拾东西离开了。",
                    speaker="神秘商人"
                ),
                "merchant_2_warn": BranchNode(
                    node_id="merchant_2_warn",
                    title="英雄之举",
                    content="你的警告让村民们警觉起来。\n\n商人见状不妙，匆忙离开了村子。\n\n村长威利走过来：「谢谢你，年轻人。你保护了村子。」",
                    speaker="威利",
                    auto_consequences=[
                        Consequence(ConsequenceType.RELATIONSHIP, "威利", 15, "威利对你的信任大增"),
                        Consequence(ConsequenceType.REPUTATION, "village", 20, "你在村里的声望大增"),
                    ]
                )
            }
        ),
        "animal_rescue": StoryBranch(
            branch_id="animal_rescue",
            name="第二章：动物救援",
            description="一只受伤的小动物需要你的帮助",
            start_node_id="animal_1",
            min_level=5,
            nodes={
                "animal_1": BranchNode(
                    node_id="animal_1",
                    title="受伤的小动物",
                    content="在森林边缘，你发现了一只受伤的小狐狸。\n\n它看起来很虚弱，眼神中充满了恐惧。\n\n你该怎么办？",
                    speaker="旁白",
                    choices=[
                        StoryChoice(
                            choice_id="help_animal",
                            text="小心地救助它",
                            consequences=[
                                Consequence(ConsequenceType.ITEM, "绷带", -1, "使用绷带"),
                                Consequence(ConsequenceType.KARMA, "karma", 10, "善有善报"),
                            ],
                            next_node_id="animal_2_help",
                            impact=ChoiceImpact.POSITIVE
                        ),
                        StoryChoice(
                            choice_id="ignore_animal",
                            text="无视它离开",
                            consequences=[
                                Consequence(ConsequenceType.KARMA, "karma", -5, "你感到有些内疚"),
                            ],
                            next_node_id="animal_2_ignore",
                            impact=ChoiceImpact.NEGATIVE
                        ),
                        StoryChoice(
                            choice_id="call_help",
                            text="去村里找人帮忙",
                            consequences=[
                                Consequence(ConsequenceType.RELATIONSHIP, "村民", 5, "村民赞赏你的善良"),
                            ],
                            next_node_id="animal_2_call",
                            impact=ChoiceImpact.POSITIVE
                        )
                    ]
                ),
                "animal_2_help": BranchNode(
                    node_id="animal_2_help",
                    title="新的伙伴",
                    content="你小心地包扎了小狐狸的伤口。\n\n它感激地看着你，似乎想跟着你。\n\n「我可以收养它吗？」你心想。",
                    speaker="旁白",
                    auto_consequences=[
                        Consequence(ConsequenceType.UNLOCK, "fox_pet", 1, "解锁狐狸宠物"),
                        Consequence(ConsequenceType.RELATIONSHIP, "自然", 20, "你与自然的联系加深了"),
                    ]
                ),
                "animal_2_ignore": BranchNode(
                    node_id="animal_2_ignore",
                    title="离去",
                    content="你转身离开，不忍再看。\n\n身后传来微弱的呜咽声，但你没有回头。\n\n也许这是正确的选择，也许不是...",
                    speaker="旁白"
                ),
                "animal_2_call": BranchNode(
                    node_id="animal_2_call",
                    title="村民的帮助",
                    content="你跑回村子，找到了一位猎人。\n\n「别担心，我会照顾它的。」\n\n他带着你回到森林，救助了小狐狸。",
                    speaker="猎人",
                    auto_consequences=[
                        Consequence(ConsequenceType.RELATIONSHIP, "猎人", 10, "猎人对你印象很好"),
                    ]
                )
            }
        )
    }
    
    def __init__(self):
        self.world_state = WorldState()
        self.current_branch: Optional[str] = None
        self.current_node: Optional[str] = None
        self.completed_branches: List[str] = []
        self.active_flags: Dict[str, bool] = {}
        self.choice_history: List[Tuple[str, str]] = []
    
    def start_branch(self, branch_id: str) -> Tuple[bool, str, Optional[BranchNode]]:
        branch = self.MAIN_STORY_BRANCHES.get(branch_id)
        if not branch:
            return False, "未知的剧情分支", None
        
        if branch_id in self.completed_branches and not branch.is_repeatable:
            return False, "该剧情已完成", None
        
        for prereq in branch.prerequisites:
            if prereq not in self.completed_branches:
                return False, f"需要先完成: {prereq}", None
        
        self.current_branch = branch_id
        self.current_node = branch.start_node_id
        
        node = branch.nodes.get(self.current_node)
        return True, f"开始剧情: {branch.name}", node
    
    def make_choice(self, choice_id: str, player_state: Dict) -> Tuple[bool, str, List[str], Optional[BranchNode]]:
        if not self.current_branch or not self.current_node:
            return False, "没有进行中的剧情", [], None
        
        branch = self.MAIN_STORY_BRANCHES.get(self.current_branch)
        if not branch:
            return False, "剧情数据错误", [], None
        
        node = branch.nodes.get(self.current_node)
        if not node:
            return False, "节点数据错误", [], None
        
        chosen = None
        for choice in node.choices:
            if choice.choice_id == choice_id:
                chosen = choice
                break
        
        if not chosen:
            return False, "无效的选择", [], None
        
        can_choose, reason = chosen.can_choose(player_state)
        if not can_choose:
            return False, reason, [], None
        
        self.choice_history.append((self.current_node, choice_id))
        
        results = chosen.apply_consequences()
        self._apply_consequences(chosen.consequences)
        
        if chosen.next_node_id:
            self.current_node = chosen.next_node_id
            next_node = branch.nodes.get(self.current_node)
            
            if next_node and next_node.auto_consequences:
                for cons in next_node.auto_consequences:
                    self._apply_consequence(cons)
                    results.append(cons.get_display_text())
            
            if not next_node or not next_node.has_choices():
                self.completed_branches.append(self.current_branch)
                self.current_branch = None
                self.current_node = None
            
            return True, "", results, next_node
        
        self.completed_branches.append(self.current_branch)
        self.current_branch = None
        self.current_node = None
        
        return True, "剧情完成", results, None
    
    def _apply_consequences(self, consequences: List[Consequence]):
        for cons in consequences:
            self._apply_consequence(cons)
    
    def _apply_consequence(self, cons: Consequence):
        if cons.consequence_type == ConsequenceType.RELATIONSHIP:
            self.world_state.modify_relationship(cons.target, cons.value)
        elif cons.consequence_type == ConsequenceType.REPUTATION:
            self.world_state.reputation += cons.value
        elif cons.consequence_type == ConsequenceType.WORLD:
            self.world_state.set_flag(cons.target, cons.value > 0)
        elif cons.consequence_type == ConsequenceType.STORY:
            self.active_flags[cons.target] = cons.value > 0
        elif cons.consequence_type == ConsequenceType.KARMA:
            self.world_state.add_karma(cons.value)
    
    def get_available_branches(self, player_level: int) -> List[StoryBranch]:
        result = []
        for branch in self.MAIN_STORY_BRANCHES.values():
            if player_level >= branch.min_level:
                if all(p in self.completed_branches for p in branch.prerequisites):
                    result.append(branch)
        return result
    
    def get_relationship(self, npc_name: str) -> Tuple[int, str]:
        value = self.world_state.npc_relationships.get(npc_name, 50)
        level = self.world_state.get_relationship_level(npc_name)
        return value, level
    
    def get_reputation(self) -> int:
        return self.world_state.reputation
    
    def get_karma(self) -> int:
        return self.world_state.karma
    
    def has_world_flag(self, flag_name: str) -> bool:
        return self.world_state.has_flag(flag_name)
    
    def get_save_data(self) -> Dict:
        return {
            "world_state": {
                "npc_relationships": self.world_state.npc_relationships,
                "world_flags": self.world_state.world_flags,
                "event_history": self.world_state.event_history,
                "reputation": self.world_state.reputation,
                "karma": self.world_state.karma
            },
            "current_branch": self.current_branch,
            "current_node": self.current_node,
            "completed_branches": self.completed_branches,
            "active_flags": self.active_flags,
            "choice_history": self.choice_history
        }
    
    def load_save_data(self, data: Dict):
        ws_data = data.get("world_state", {})
        self.world_state = WorldState(
            npc_relationships=ws_data.get("npc_relationships", {}),
            world_flags=ws_data.get("world_flags", {}),
            event_history=ws_data.get("event_history", []),
            reputation=ws_data.get("reputation", 0),
            karma=ws_data.get("karma", 0)
        )
        
        self.current_branch = data.get("current_branch")
        self.current_node = data.get("current_node")
        self.completed_branches = data.get("completed_branches", [])
        self.active_flags = data.get("active_flags", {})
        self.choice_history = data.get("choice_history", [])
