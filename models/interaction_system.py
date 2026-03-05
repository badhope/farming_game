"""
角色交互系统模块
提供关系系统、声望系统和动态任务生成
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set, Callable
from enum import Enum
import random


class RelationshipType(Enum):
    STRANGER = "陌生人"
    ACQUAINTANCE = "点头之交"
    FRIEND = "朋友"
    GOOD_FRIEND = "好友"
    BEST_FRIEND = "挚友"
    FAMILY = "家人"
    RIVAL = "对手"
    ENEMY = "敌人"
    LOVER = "恋人"


class ReputationLevel(Enum):
    HATED = "憎恨"
    HOSTILE = "敌对"
    UNFRIENDLY = "不友好"
    NEUTRAL = "中立"
    FRIENDLY = "友好"
    HONORED = "尊敬"
    EXALTED = "崇敬"


class FactionType(Enum):
    VILLAGE = "村庄"
    MERCHANTS_GUILD = "商人公会"
    ADVENTURERS_GUILD = "冒险者公会"
    MAGES_GUILD = "法师公会"
    WARRIORS_GUILD = "战士公会"
    FARMERS_UNION = "农夫联盟"
    CHURCH = "教会"
    THIEVES_GUILD = "盗贼公会"
    ROYAL_COURT = "王室"
    REBELS = "反抗军"


class QuestType(Enum):
    MAIN = "主线任务"
    SIDE = "支线任务"
    DAILY = "日常任务"
    WEEKLY = "周常任务"
    EVENT = "事件任务"
    REPUTATION = "声望任务"
    HUNTING = "狩猎任务"
    GATHERING = "采集任务"
    DELIVERY = "运送任务"
    ESCORT = "护送任务"
    INVESTIGATION = "调查任务"
    BOSS = "首领任务"


class QuestStatus(Enum):
    LOCKED = "未解锁"
    AVAILABLE = "可接取"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    FAILED = "失败"
    ABANDONED = "已放弃"


class InteractionType(Enum):
    TALK = "交谈"
    GIFT = "送礼"
    TRADE = "交易"
    QUEST = "任务"
    FIGHT = "战斗"
    FLIRT = "调情"
    INSULT = "侮辱"
    HELP = "帮助"
    IGNORE = "无视"
    INVITE = "邀请"


@dataclass
class RelationshipEvent:
    event_id: str
    event_type: str
    description: str
    relationship_change: int
    timestamp: int = 0
    
    def get_display(self) -> str:
        change_str = f"+{self.relationship_change}" if self.relationship_change > 0 else str(self.relationship_change)
        return f"[{self.event_type}] {self.description} ({change_str})"


@dataclass
class CharacterRelationship:
    character_id: str
    character_name: str
    
    friendship_points: int = 0
    max_friendship: int = 1000
    
    romance_points: int = 0
    max_romance: int = 500
    
    trust_points: int = 0
    max_trust: int = 500
    
    respect_points: int = 0
    max_respect: int = 500
    
    interaction_count: int = 0
    gift_count: int = 0
    quest_count: int = 0
    
    first_met_day: int = 0
    last_interaction_day: int = 0
    
    events: List[RelationshipEvent] = field(default_factory=list)
    
    is_romanceable: bool = False
    is_married: bool = False
    marriage_day: int = 0
    
    special_flags: Dict[str, bool] = field(default_factory=dict)
    
    @property
    def relationship_type(self) -> RelationshipType:
        if self.is_married:
            return RelationshipType.FAMILY
        
        if self.friendship_points < 0:
            if self.friendship_points < -300:
                return RelationshipType.ENEMY
            return RelationshipType.RIVAL
        
        percentage = self.friendship_points / self.max_friendship
        
        if percentage >= 0.9:
            if self.is_romanceable and self.romance_points >= 400:
                return RelationshipType.LOVER
            return RelationshipType.BEST_FRIEND
        elif percentage >= 0.7:
            return RelationshipType.GOOD_FRIEND
        elif percentage >= 0.5:
            return RelationshipType.FRIEND
        elif percentage >= 0.2:
            return RelationshipType.ACQUAINTANCE
        
        return RelationshipType.STRANGER
    
    def add_friendship(self, amount: int, event_type: str, description: str, current_day: int) -> Tuple[bool, str]:
        old_type = self.relationship_type
        self.friendship_points = max(-self.max_friendship, min(self.max_friendship, self.friendship_points + amount))
        new_type = self.relationship_type
        
        event = RelationshipEvent(
            event_id=f"rel_{current_day}_{len(self.events)}",
            event_type=event_type,
            description=description,
            relationship_change=amount,
            timestamp=current_day
        )
        self.events.append(event)
        self.last_interaction_day = current_day
        
        if new_type != old_type:
            return True, f"关系变化：{old_type.value} → {new_type.value}"
        
        return False, ""
    
    def add_romance(self, amount: int) -> Tuple[bool, str]:
        if not self.is_romanceable:
            return False, "该角色不可攻略"
        
        old_points = self.romance_points
        self.romance_points = max(0, min(self.max_romance, self.romance_points + amount))
        
        if self.romance_points >= 400 and old_points < 400:
            return True, "你们的关系更进一步了！"
        
        return False, ""
    
    def can_marry(self) -> Tuple[bool, str]:
        if self.is_married:
            return False, "已经结婚了"
        
        if not self.is_romanceable:
            return False, "该角色不可结婚"
        
        if self.friendship_points < 800:
            return False, "好感度不足"
        
        if self.romance_points < 400:
            return False, "爱情值不足"
        
        return True, "可以求婚"
    
    def marry(self, current_day: int) -> Tuple[bool, str]:
        can_marry, reason = self.can_marry()
        if not can_marry:
            return False, reason
        
        self.is_married = True
        self.marriage_day = current_day
        
        return True, f"与{self.character_name}结婚了！"
    
    def get_relationship_summary(self) -> str:
        lines = [
            f"【{self.character_name}】",
            f"关系：{self.relationship_type.value}",
            f"好感度：{self.friendship_points}/{self.max_friendship}"
        ]
        
        if self.is_romanceable:
            lines.append(f"爱情值：{self.romance_points}/{self.max_romance}")
        
        lines.append(f"信任度：{self.trust_points}/{self.max_trust}")
        lines.append(f"尊重度：{self.respect_points}/{self.max_respect}")
        
        if self.is_married:
            lines.append(f"结婚纪念日：第{self.marriage_day}天")
        
        return "\n".join(lines)


@dataclass
class FactionReputation:
    faction_type: FactionType
    faction_name: str
    
    reputation_points: int = 0
    max_reputation: int = 3000
    
    completed_quests: int = 0
    failed_quests: int = 0
    
    special_titles: List[str] = field(default_factory=list)
    unlocked_rewards: List[str] = field(default_factory=list)
    
    @property
    def reputation_level(self) -> ReputationLevel:
        percentage = self.reputation_points / self.max_reputation
        
        if percentage >= 0.9:
            return ReputationLevel.EXALTED
        elif percentage >= 0.7:
            return ReputationLevel.HONORED
        elif percentage >= 0.5:
            return ReputationLevel.FRIENDLY
        elif percentage >= 0.2:
            return ReputationLevel.NEUTRAL
        elif percentage >= -0.2:
            return ReputationLevel.UNFRIENDLY
        elif percentage >= -0.5:
            return ReputationLevel.HOSTILE
        else:
            return ReputationLevel.HATED
    
    def add_reputation(self, amount: int) -> Tuple[bool, str]:
        old_level = self.reputation_level
        self.reputation_points = max(-self.max_reputation, min(self.max_reputation, self.reputation_points + amount))
        new_level = self.reputation_level
        
        if new_level != old_level:
            return True, f"在{self.faction_name}的声望变为【{new_level.value}】"
        
        return False, ""
    
    def get_discount(self) -> float:
        level_discounts = {
            ReputationLevel.EXALTED: 0.3,
            ReputationLevel.HONORED: 0.2,
            ReputationLevel.FRIENDLY: 0.1,
            ReputationLevel.NEUTRAL: 0.0,
            ReputationLevel.UNFRIENDLY: -0.1,
            ReputationLevel.HOSTILE: -0.2,
            ReputationLevel.HATED: -0.3
        }
        return level_discounts.get(self.reputation_level, 0.0)
    
    def can_access_content(self, required_level: ReputationLevel) -> bool:
        level_order = [
            ReputationLevel.HATED,
            ReputationLevel.HOSTILE,
            ReputationLevel.UNFRIENDLY,
            ReputationLevel.NEUTRAL,
            ReputationLevel.FRIENDLY,
            ReputationLevel.HONORED,
            ReputationLevel.EXALTED
        ]
        
        current_idx = level_order.index(self.reputation_level)
        required_idx = level_order.index(required_level)
        
        return current_idx >= required_idx


@dataclass
class QuestObjective:
    objective_id: str
    description: str
    objective_type: str
    target: str
    required_amount: int
    current_amount: int = 0
    
    is_completed: bool = False
    is_optional: bool = False
    
    def update_progress(self, amount: int = 1) -> bool:
        if self.is_completed:
            return False
        
        self.current_amount = min(self.required_amount, self.current_amount + amount)
        
        if self.current_amount >= self.required_amount:
            self.is_completed = True
            return True
        
        return False
    
    def get_progress_text(self) -> str:
        if self.is_completed:
            return f"✓ {self.description}"
        return f"○ {self.description} ({self.current_amount}/{self.required_amount})"


@dataclass
class QuestReward:
    gold: int = 0
    exp: int = 0
    items: Dict[str, int] = field(default_factory=dict)
    reputation: Dict[FactionType, int] = field(default_factory=dict)
    friendship: Dict[str, int] = field(default_factory=dict)
    unlock_content: List[str] = field(default_factory=list)
    
    def get_summary(self) -> str:
        rewards = []
        
        if self.gold > 0:
            rewards.append(f"💰 {self.gold}金币")
        if self.exp > 0:
            rewards.append(f"⭐ {self.exp}经验")
        
        for item_id, count in self.items.items():
            rewards.append(f"📦 {item_id} x{count}")
        
        for faction, amount in self.reputation.items():
            rewards.append(f"🏆 {faction.value}声望 +{amount}")
        
        return " | ".join(rewards)


@dataclass
class Quest:
    quest_id: str
    name: str
    description: str
    quest_type: QuestType
    
    giver_id: str = ""
    giver_name: str = ""
    
    objectives: List[QuestObjective] = field(default_factory=list)
    rewards: QuestReward = field(default_factory=QuestReward)
    
    status: QuestStatus = QuestStatus.LOCKED
    
    time_limit: int = 0
    start_day: int = 0
    complete_day: int = 0
    
    prerequisite_quests: List[str] = field(default_factory=list)
    required_level: int = 1
    required_reputation: Dict[FactionType, ReputationLevel] = field(default_factory=dict)
    
    is_repeatable: bool = False
    repeat_cooldown: int = 0
    last_complete_day: int = 0
    
    dialogue_start: str = ""
    dialogue_progress: str = ""
    dialogue_complete: str = ""
    
    chain_next: str = ""
    chain_prev: str = ""
    
    def can_accept(self, player_level: int, completed_quests: Set[str], 
                   reputations: Dict[FactionType, FactionReputation]) -> Tuple[bool, str]:
        if self.status not in [QuestStatus.LOCKED, QuestStatus.AVAILABLE]:
            return False, "任务状态不允许接取"
        
        if player_level < self.required_level:
            return False, f"需要等级{self.required_level}"
        
        for prereq in self.prerequisite_quests:
            if prereq not in completed_quests:
                return False, f"需要先完成任务：{prereq}"
        
        for faction, required_level in self.required_reputation.items():
            if faction in reputations:
                if not reputations[faction].can_access_content(required_level):
                    return False, f"需要{faction.value}声望达到{required_level.value}"
        
        return True, "可以接取任务"
    
    def accept(self, current_day: int) -> Tuple[bool, str]:
        self.status = QuestStatus.IN_PROGRESS
        self.start_day = current_day
        return True, f"接取了任务：{self.name}"
    
    def update_objective(self, objective_type: str, target: str, amount: int = 1) -> Tuple[bool, str]:
        if self.status != QuestStatus.IN_PROGRESS:
            return False, "任务未在进行中"
        
        completed_objectives = []
        
        for objective in self.objectives:
            if objective.objective_type == objective_type and objective.target == target:
                if objective.update_progress(amount):
                    completed_objectives.append(objective)
        
        if completed_objectives:
            if self.is_complete():
                return True, "任务完成！请回去交付任务。"
            return True, f"目标更新：{completed_objectives[0].description}"
        
        return False, ""
    
    def is_complete(self) -> bool:
        required_objectives = [o for o in self.objectives if not o.is_optional]
        return all(o.is_completed for o in required_objectives)
    
    def complete(self, current_day: int) -> Tuple[bool, str]:
        if not self.is_complete():
            return False, "任务目标未完成"
        
        self.status = QuestStatus.COMPLETED
        self.complete_day = current_day
        self.last_complete_day = current_day
        
        return True, f"完成任务：{self.name}"
    
    def abandon(self) -> Tuple[bool, str]:
        if self.status != QuestStatus.IN_PROGRESS:
            return False, "无法放弃此任务"
        
        self.status = QuestStatus.ABANDONED
        return True, f"放弃了任务：{self.name}"
    
    def reset(self):
        if self.is_repeatable:
            self.status = QuestStatus.AVAILABLE
            for objective in self.objectives:
                objective.current_amount = 0
                objective.is_completed = False
            self.start_day = 0
            self.complete_day = 0
    
    def get_progress_display(self) -> str:
        lines = [f"【{self.name}】", self.description, ""]
        
        for objective in self.objectives:
            lines.append(objective.get_progress_text())
        
        lines.append("")
        lines.append(f"奖励：{self.rewards.get_summary()}")
        
        if self.time_limit > 0:
            remaining = self.time_limit - (0 - self.start_day)
            lines.append(f"剩余时间：{remaining}天")
        
        return "\n".join(lines)


class RelationshipManager:
    
    def __init__(self):
        self.relationships: Dict[str, CharacterRelationship] = {}
        self.current_day: int = 1
    
    def get_or_create_relationship(self, character_id: str, character_name: str, 
                                   is_romanceable: bool = False) -> CharacterRelationship:
        if character_id not in self.relationships:
            self.relationships[character_id] = CharacterRelationship(
                character_id=character_id,
                character_name=character_name,
                first_met_day=self.current_day,
                is_romanceable=is_romanceable
            )
        
        return self.relationships[character_id]
    
    def interact(self, character_id: str, character_name: str, 
                 interaction_type: InteractionType, context: Dict) -> Tuple[bool, str]:
        relationship = self.get_or_create_relationship(character_id, character_name)
        
        interaction_effects = {
            InteractionType.TALK: (10, "交谈", "与{name}进行了愉快的交谈"),
            InteractionType.GIFT: (30, "送礼", "给{name}送了礼物"),
            InteractionType.TRADE: (5, "交易", "与{name}进行了交易"),
            InteractionType.HELP: (25, "帮助", "帮助了{name}"),
            InteractionType.INVITE: (20, "邀请", "邀请{name}一起活动"),
            InteractionType.INSULT: (-50, "侮辱", "侮辱了{name}"),
            InteractionType.IGNORE: (-5, "无视", "无视了{name}"),
            InteractionType.FLIRT: (15, "调情", "向{name}示好")
        }
        
        if interaction_type in interaction_effects:
            points, event_type, description = interaction_effects[interaction_type]
            description = description.format(name=character_name)
            
            relationship.interaction_count += 1
            
            level_up, message = relationship.add_friendship(points, event_type, description, self.current_day)
            
            if interaction_type == InteractionType.FLIRT and relationship.is_romanceable:
                romance_points = 10
                romance_up, romance_msg = relationship.add_romance(romance_points)
                if romance_up:
                    message += f"\n{romance_msg}"
            
            return True, message
        
        return False, "无效的交互类型"
    
    def give_gift(self, character_id: str, character_name: str, 
                  gift_name: str, is_loved: bool = False, is_liked: bool = False,
                  is_hated: bool = False) -> Tuple[bool, str]:
        relationship = self.get_or_create_relationship(character_id, character_name)
        
        if relationship.gift_count >= 1:
            return False, "今天已经送过礼物了"
        
        points = 10
        reaction = "谢谢你的礼物。"
        
        if is_loved:
            points = 80
            reaction = "哇！这是我最喜欢的东西！太感谢你了！"
        elif is_liked:
            points = 40
            reaction = "这个我很喜欢，谢谢你！"
        elif is_hated:
            points = -20
            reaction = "呃...这个我不太喜欢..."
        
        relationship.gift_count += 1
        level_up, message = relationship.add_friendship(points, "送礼", f"送了{gift_name}", self.current_day)
        
        result = reaction
        if level_up:
            result += f"\n{message}"
        
        return True, result
    
    def propose_marriage(self, character_id: str) -> Tuple[bool, str]:
        if character_id not in self.relationships:
            return False, "你们还不认识"
        
        relationship = self.relationships[character_id]
        
        can_marry, reason = relationship.can_marry()
        if not can_marry:
            return False, reason
        
        success = random.random() < 0.8
        
        if success:
            return relationship.marry(self.current_day)
        else:
            relationship.add_friendship(-50, "求婚", "求婚被拒绝", self.current_day)
            return False, "求婚被拒绝了..."
    
    def new_day(self):
        for relationship in self.relationships.values():
            relationship.gift_count = 0
    
    def get_all_relationships_summary(self) -> List[str]:
        summaries = []
        for rel in sorted(self.relationships.values(), key=lambda r: r.friendship_points, reverse=True):
            summaries.append(f"{rel.character_name}: {rel.relationship_type.value} ({rel.friendship_points})")
        return summaries
    
    def get_save_data(self) -> Dict:
        return {
            "current_day": self.current_day,
            "relationships": {
                char_id: {
                    "friendship_points": rel.friendship_points,
                    "romance_points": rel.romance_points,
                    "trust_points": rel.trust_points,
                    "respect_points": rel.respect_points,
                    "interaction_count": rel.interaction_count,
                    "gift_count": rel.gift_count,
                    "first_met_day": rel.first_met_day,
                    "last_interaction_day": rel.last_interaction_day,
                    "is_married": rel.is_married,
                    "marriage_day": rel.marriage_day,
                    "is_romanceable": rel.is_romanceable
                } for char_id, rel in self.relationships.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.current_day = data.get("current_day", 1)
        
        for char_id, rel_data in data.get("relationships", {}).items():
            relationship = CharacterRelationship(
                character_id=char_id,
                character_name=rel_data.get("character_name", char_id),
                friendship_points=rel_data.get("friendship_points", 0),
                romance_points=rel_data.get("romance_points", 0),
                trust_points=rel_data.get("trust_points", 0),
                respect_points=rel_data.get("respect_points", 0),
                interaction_count=rel_data.get("interaction_count", 0),
                gift_count=rel_data.get("gift_count", 0),
                first_met_day=rel_data.get("first_met_day", 0),
                last_interaction_day=rel_data.get("last_interaction_day", 0),
                is_married=rel_data.get("is_married", False),
                marriage_day=rel_data.get("marriage_day", 0),
                is_romanceable=rel_data.get("is_romanceable", False)
            )
            self.relationships[char_id] = relationship


class ReputationManager:
    
    def __init__(self):
        self.factions: Dict[FactionType, FactionReputation] = {}
        self._init_factions()
    
    def _init_factions(self):
        faction_data = {
            FactionType.VILLAGE: "宁静村",
            FactionType.MERCHANTS_GUILD: "商人公会",
            FactionType.ADVENTURERS_GUILD: "冒险者公会",
            FactionType.MAGES_GUILD: "法师公会",
            FactionType.WARRIORS_GUILD: "战士公会",
            FactionType.FARMERS_UNION: "农夫联盟",
            FactionType.CHURCH: "教会",
            FactionType.THIEVES_GUILD: "盗贼公会",
            FactionType.ROYAL_COURT: "王室",
            FactionType.REBELS: "反抗军"
        }
        
        for faction_type, name in faction_data.items():
            self.factions[faction_type] = FactionReputation(
                faction_type=faction_type,
                faction_name=name
            )
    
    def get_faction(self, faction_type: FactionType) -> FactionReputation:
        return self.factions.get(faction_type)
    
    def add_reputation(self, faction_type: FactionType, amount: int) -> Tuple[bool, str]:
        faction = self.get_faction(faction_type)
        if not faction:
            return False, "未知势力"
        
        level_up, message = faction.add_reputation(amount)
        
        opposing_factions = {
            FactionType.ROYAL_COURT: FactionType.REBELS,
            FactionType.REBELS: FactionType.ROYAL_COURT,
            FactionType.CHURCH: FactionType.THIEVES_GUILD,
            FactionType.THIEVES_GUILD: FactionType.CHURCH
        }
        
        if faction_type in opposing_factions:
            opposing = opposing_factions[faction_type]
            if opposing in self.factions:
                self.factions[opposing].add_reputation(-amount // 2)
        
        return level_up, message
    
    def get_all_reputations(self) -> List[Tuple[str, str, int]]:
        return [
            (faction.faction_name, faction.reputation_level.value, faction.reputation_points)
            for faction in self.factions.values()
        ]
    
    def get_discount(self, faction_type: FactionType) -> float:
        faction = self.get_faction(faction_type)
        if faction:
            return faction.get_discount()
        return 0.0
    
    def get_save_data(self) -> Dict:
        return {
            "factions": {
                faction_type.value: {
                    "reputation_points": faction.reputation_points,
                    "completed_quests": faction.completed_quests,
                    "failed_quests": faction.failed_quests,
                    "special_titles": faction.special_titles,
                    "unlocked_rewards": faction.unlocked_rewards
                } for faction_type, faction in self.factions.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        for faction_str, faction_data in data.get("factions", {}).items():
            try:
                faction_type = FactionType(faction_str)
                if faction_type in self.factions:
                    faction = self.factions[faction_type]
                    faction.reputation_points = faction_data.get("reputation_points", 0)
                    faction.completed_quests = faction_data.get("completed_quests", 0)
                    faction.failed_quests = faction_data.get("failed_quests", 0)
                    faction.special_titles = faction_data.get("special_titles", [])
                    faction.unlocked_rewards = faction_data.get("unlocked_rewards", [])
            except ValueError:
                pass


class QuestGenerator:
    
    @staticmethod
    def generate_daily_quest(day: int, player_level: int) -> Quest:
        quest_templates = [
            {
                "name": "日常采集",
                "description": "收集一些基础材料",
                "type": QuestType.DAILY,
                "objectives": [("gather", "wood", 10), ("gather", "stone", 5)],
                "rewards": {"gold": 100, "exp": 50}
            },
            {
                "name": "怪物讨伐",
                "description": "清除附近的怪物",
                "type": QuestType.DAILY,
                "objectives": [("kill", "slime", 5)],
                "rewards": {"gold": 150, "exp": 80}
            },
            {
                "name": "物品运送",
                "description": "将物品送到目的地",
                "type": QuestType.DAILY,
                "objectives": [("deliver", "package", 1)],
                "rewards": {"gold": 80, "exp": 30}
            }
        ]
        
        template = random.choice(quest_templates)
        
        objectives = [
            QuestObjective(
                objective_id=f"obj_{i}",
                description=f"{obj[0]} {obj[2]}个{obj[1]}",
                objective_type=obj[0],
                target=obj[1],
                required_amount=obj[2]
            ) for i, obj in enumerate(template["objectives"])
        ]
        
        return Quest(
            quest_id=f"daily_{day}_{random.randint(1000, 9999)}",
            name=template["name"],
            description=template["description"],
            quest_type=template["type"],
            objectives=objectives,
            rewards=QuestReward(
                gold=template["rewards"]["gold"],
                exp=template["rewards"]["exp"]
            ),
            status=QuestStatus.AVAILABLE,
            is_repeatable=True,
            repeat_cooldown=1
        )
    
    @staticmethod
    def generate_hunting_quest(target: str, count: int, difficulty: int) -> Quest:
        return Quest(
            quest_id=f"hunt_{target}_{random.randint(1000, 9999)}",
            name=f"讨伐{target}",
            description=f"击败{count}只{target}",
            quest_type=QuestType.HUNTING,
            objectives=[
                QuestObjective(
                    objective_id="kill_target",
                    description=f"击败{target}",
                    objective_type="kill",
                    target=target,
                    required_amount=count
                )
            ],
            rewards=QuestReward(
                gold=50 * difficulty * count,
                exp=30 * difficulty * count
            ),
            status=QuestStatus.AVAILABLE,
            required_level=difficulty * 5,
            is_repeatable=True,
            repeat_cooldown=3
        )
    
    @staticmethod
    def generate_gathering_quest(item: str, count: int, difficulty: int) -> Quest:
        return Quest(
            quest_id=f"gather_{item}_{random.randint(1000, 9999)}",
            name=f"收集{item}",
            description=f"收集{count}个{item}",
            quest_type=QuestType.GATHERING,
            objectives=[
                QuestObjective(
                    objective_id="gather_target",
                    description=f"收集{item}",
                    objective_type="gather",
                    target=item,
                    required_amount=count
                )
            ],
            rewards=QuestReward(
                gold=30 * difficulty * count,
                exp=20 * difficulty * count,
                items={item: count // 2}
            ),
            status=QuestStatus.AVAILABLE,
            required_level=difficulty * 3,
            is_repeatable=True,
            repeat_cooldown=2
        )


class QuestManager:
    
    def __init__(self):
        self.active_quests: Dict[str, Quest] = {}
        self.completed_quests: Set[str] = set()
        self.available_quests: Dict[str, Quest] = {}
        
        self.daily_quests: List[Quest] = []
        self.current_day: int = 1
    
    def add_quest(self, quest: Quest):
        if quest.quest_type == QuestType.DAILY:
            self.daily_quests.append(quest)
        else:
            self.available_quests[quest.quest_id] = quest
    
    def accept_quest(self, quest_id: str, player_level: int) -> Tuple[bool, str]:
        quest = self.available_quests.get(quest_id)
        if not quest:
            return False, "找不到该任务"
        
        can_accept, reason = quest.can_accept(player_level, self.completed_quests, {})
        if not can_accept:
            return False, reason
        
        success, message = quest.accept(self.current_day)
        
        if success:
            self.active_quests[quest_id] = quest
            if quest_id in self.available_quests:
                del self.available_quests[quest_id]
        
        return success, message
    
    def update_quest_progress(self, objective_type: str, target: str, amount: int = 1) -> List[Tuple[str, str]]:
        completed = []
        
        for quest_id, quest in self.active_quests.items():
            updated, message = quest.update_objective(objective_type, target, amount)
            if updated:
                completed.append((quest.name, message))
        
        return completed
    
    def complete_quest(self, quest_id: str) -> Tuple[bool, QuestReward, str]:
        quest = self.active_quests.get(quest_id)
        if not quest:
            return False, QuestReward(), "找不到该任务"
        
        success, message = quest.complete(self.current_day)
        
        if success:
            self.completed_quests.add(quest_id)
            del self.active_quests[quest_id]
            
            if quest.chain_next:
                pass
            
            return True, quest.rewards, message
        
        return False, QuestReward(), message
    
    def abandon_quest(self, quest_id: str) -> Tuple[bool, str]:
        quest = self.active_quests.get(quest_id)
        if not quest:
            return False, "找不到该任务"
        
        success, message = quest.abandon()
        
        if success:
            del self.active_quests[quest_id]
        
        return success, message
    
    def generate_daily_quests(self, player_level: int):
        self.daily_quests = []
        
        for i in range(3):
            quest = QuestGenerator.generate_daily_quest(self.current_day + i, player_level)
            self.daily_quests.append(quest)
    
    def new_day(self, player_level: int):
        self.current_day += 1
        
        for quest in self.daily_quests:
            quest.reset()
        
        for quest_id, quest in list(self.active_quests.items()):
            if quest.time_limit > 0:
                if self.current_day - quest.start_day >= quest.time_limit:
                    quest.status = QuestStatus.FAILED
                    del self.active_quests[quest_id]
        
        for quest in list(self.available_quests.values()):
            if quest.is_repeatable and quest.last_complete_day > 0:
                if self.current_day - quest.last_complete_day >= quest.repeat_cooldown:
                    quest.reset()
        
        self.generate_daily_quests(player_level)
    
    def get_active_quests_summary(self) -> List[str]:
        return [quest.get_progress_display() for quest in self.active_quests.values()]
    
    def get_available_quests(self) -> List[Quest]:
        return list(self.available_quests.values()) + self.daily_quests
    
    def get_save_data(self) -> Dict:
        return {
            "current_day": self.current_day,
            "completed_quests": list(self.completed_quests),
            "active_quests": {
                quest_id: {
                    "quest_id": quest.quest_id,
                    "name": quest.name,
                    "start_day": quest.start_day,
                    "status": quest.status.value,
                    "objectives": [
                        {
                            "objective_id": obj.objective_id,
                            "current_amount": obj.current_amount,
                            "is_completed": obj.is_completed
                        } for obj in quest.objectives
                    ]
                } for quest_id, quest in self.active_quests.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.current_day = data.get("current_day", 1)
        self.completed_quests = set(data.get("completed_quests", []))
        
        for quest_id, quest_data in data.get("active_quests", {}).items():
            pass


class InteractionSystem:
    
    def __init__(self):
        self.relationships = RelationshipManager()
        self.reputation = ReputationManager()
        self.quests = QuestManager()
        
        self.current_day: int = 1
        self.player_level: int = 1
    
    def interact_with_character(self, character_id: str, character_name: str,
                                interaction_type: InteractionType, context: Dict = None) -> Tuple[bool, str]:
        return self.relationships.interact(character_id, character_name, interaction_type, context or {})
    
    def give_gift_to_character(self, character_id: str, character_name: str,
                               gift_name: str, gift_preference: str = "neutral") -> Tuple[bool, str]:
        is_loved = gift_preference == "loved"
        is_liked = gift_preference == "liked"
        is_hated = gift_preference == "hated"
        
        return self.relationships.give_gift(character_id, character_name, gift_name, is_loved, is_liked, is_hated)
    
    def propose_to_character(self, character_id: str) -> Tuple[bool, str]:
        return self.relationships.propose_marriage(character_id)
    
    def update_faction_reputation(self, faction_type: FactionType, amount: int) -> Tuple[bool, str]:
        return self.reputation.add_reputation(faction_type, amount)
    
    def accept_quest(self, quest_id: str) -> Tuple[bool, str]:
        return self.quests.accept_quest(quest_id, self.player_level)
    
    def update_quest_objective(self, objective_type: str, target: str, amount: int = 1) -> List[Tuple[str, str]]:
        return self.quests.update_quest_progress(objective_type, target, amount)
    
    def complete_quest(self, quest_id: str) -> Tuple[bool, QuestReward, str]:
        success, rewards, message = self.quests.complete_quest(quest_id)
        
        if success:
            for faction, amount in rewards.reputation.items():
                self.reputation.add_reputation(faction, amount)
            
            for char_id, amount in rewards.friendship.items():
                if char_id in self.relationships.relationships:
                    rel = self.relationships.relationships[char_id]
                    rel.add_friendship(amount, "任务", "完成任务获得好感", self.current_day)
        
        return success, rewards, message
    
    def new_day(self):
        self.current_day += 1
        self.relationships.new_day()
        self.quests.new_day(self.player_level)
    
    def get_full_status(self) -> Dict:
        return {
            "day": self.current_day,
            "player_level": self.player_level,
            "relationships": self.relationships.get_all_relationships_summary(),
            "reputations": self.reputation.get_all_reputations(),
            "active_quests": len(self.quests.active_quests),
            "completed_quests": len(self.quests.completed_quests)
        }
    
    def get_save_data(self) -> Dict:
        return {
            "current_day": self.current_day,
            "player_level": self.player_level,
            "relationships": self.relationships.get_save_data(),
            "reputation": self.reputation.get_save_data(),
            "quests": self.quests.get_save_data()
        }
    
    def load_save_data(self, data: Dict):
        self.current_day = data.get("current_day", 1)
        self.player_level = data.get("player_level", 1)
        
        if "relationships" in data:
            self.relationships.load_save_data(data["relationships"])
        if "reputation" in data:
            self.reputation.load_save_data(data["reputation"])
        if "quests" in data:
            self.quests.load_save_data(data["quests"])
