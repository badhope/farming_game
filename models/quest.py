"""
任务系统模块
管理游戏中的各类任务和任务链
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class QuestType(Enum):
    MAIN = "主线任务"
    SIDE = "支线任务"
    DAILY = "每日任务"
    SPECIAL = "特殊任务"


class QuestStatus(Enum):
    LOCKED = "未解锁"
    AVAILABLE = "可接取"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    FAILED = "失败"


@dataclass
class QuestObjective:
    description: str
    target_type: str
    target_name: str
    required_count: int
    current_count: int = 0
    
    def is_complete(self) -> bool:
        return self.current_count >= self.required_count
    
    def get_progress(self) -> float:
        if self.required_count == 0:
            return 100.0
        return min(100.0, (self.current_count / self.required_count) * 100)
    
    def update_progress(self, amount: int = 1) -> bool:
        self.current_count = min(self.current_count + amount, self.required_count)
        return self.is_complete()


@dataclass
class QuestReward:
    money: int = 0
    experience: int = 0
    items: Dict[str, int] = field(default_factory=dict)
    seeds: Dict[str, int] = field(default_factory=dict)
    skill_exp: Dict[str, int] = field(default_factory=dict)


@dataclass
class Quest:
    id: str
    name: str
    description: str
    quest_type: QuestType
    objectives: List[QuestObjective]
    reward: QuestReward
    status: QuestStatus = QuestStatus.LOCKED
    prerequisites: List[str] = field(default_factory=list)
    time_limit: Optional[int] = None
    start_day: Optional[int] = None
    complete_day: Optional[int] = None
    npc_giver: Optional[str] = None
    dialogue_start: str = ""
    dialogue_complete: str = ""
    
    def can_accept(self) -> bool:
        return self.status == QuestStatus.AVAILABLE
    
    def accept(self, current_day: int) -> bool:
        if not self.can_accept():
            return False
        self.status = QuestStatus.IN_PROGRESS
        self.start_day = current_day
        return True
    
    def is_complete(self) -> bool:
        return all(obj.is_complete() for obj in self.objectives)
    
    def complete(self, current_day: int) -> bool:
        if not self.is_complete():
            return False
        self.status = QuestStatus.COMPLETED
        self.complete_day = current_day
        return True
    
    def get_progress_percentage(self) -> float:
        if not self.objectives:
            return 0.0
        return sum(obj.get_progress() for obj in self.objectives) / len(self.objectives)
    
    def update_objective(self, target_type: str, target_name: str, amount: int = 1) -> bool:
        for obj in self.objectives:
            if obj.target_type == target_type and obj.target_name == target_name:
                return obj.update_progress(amount)
        return False


class QuestManager:
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.active_quests: List[str] = []
        self.completed_quests: List[str] = []
        self._init_quests()
    
    def _init_quests(self):
        main_quests = [
            Quest(
                id="main_1", name="🌱 初入农场", description="欢迎来到宁静村！",
                quest_type=QuestType.MAIN,
                objectives=[
                    QuestObjective("种植第一个作物", "plant", "any", 1),
                    QuestObjective("给作物浇水", "water", "any", 1),
                ],
                reward=QuestReward(money=100, experience=50, items={"胡萝卜": 5}),
                status=QuestStatus.AVAILABLE, npc_giver="村长王大爷",
                dialogue_start="年轻人，欢迎来到宁静村！",
                dialogue_complete="做得好！这是给你的奖励。"
            ),
            Quest(
                id="main_2", name="🌾 第一次收获", description="体验收获的喜悦。",
                quest_type=QuestType.MAIN,
                objectives=[
                    QuestObjective("收获成熟作物", "harvest", "any", 1),
                    QuestObjective("出售作物", "sell", "any", 1),
                ],
                reward=QuestReward(money=200, experience=100, seeds={"土豆": 10}),
                prerequisites=["main_1"], npc_giver="村长王大爷",
                dialogue_start="作物成熟后就可以收获了。",
                dialogue_complete="恭喜你完成了第一次收获！"
            ),
            Quest(
                id="main_3", name="🏪 商业头脑", description="学习如何经营农场。",
                quest_type=QuestType.MAIN,
                objectives=[
                    QuestObjective("累计赚取金币", "earn_money", "total", 1000),
                    QuestObjective("购买种子", "buy_seeds", "any", 5),
                ],
                reward=QuestReward(money=500, experience=200, seeds={"番茄": 5, "玉米": 5}),
                prerequisites=["main_2"], npc_giver="商人",
                dialogue_start="经营农场需要精打细算。",
                dialogue_complete="很好！你已经掌握了基本的经营之道。"
            ),
            Quest(
                id="main_4", name="🏘️ 扩建农场", description="农场需要扩建。",
                quest_type=QuestType.MAIN,
                objectives=[
                    QuestObjective("升级农场", "upgrade_farm", "any", 1),
                    QuestObjective("种植10个作物", "plant", "any", 10),
                ],
                reward=QuestReward(money=1000, experience=300, items={"金苹果": 1}),
                prerequisites=["main_3"], npc_giver="木匠张师傅",
                dialogue_start="你的农场发展得不错！是时候扩建了。",
                dialogue_complete="扩建完成！"
            ),
            Quest(
                id="main_5", name="🏆 成就达人", description="成为真正的农场主。",
                quest_type=QuestType.MAIN,
                objectives=[
                    QuestObjective("解锁成就", "achievement", "any", 3),
                    QuestObjective("累计收获作物", "harvest", "total", 50),
                ],
                reward=QuestReward(money=2000, experience=500, seeds={"葡萄": 3, "玫瑰": 3}),
                prerequisites=["main_4"], npc_giver="村长王大爷",
                dialogue_start="你已经成长为一个合格的农夫了！",
                dialogue_complete="太棒了！你是我们村的骄傲！"
            ),
        ]
        
        side_quests = [
            Quest(
                id="side_1", name="🥕 胡萝卜订单", description="餐厅需要新鲜胡萝卜。",
                quest_type=QuestType.SIDE,
                objectives=[QuestObjective("收获胡萝卜", "harvest", "胡萝卜", 5)],
                reward=QuestReward(money=300, experience=50),
                status=QuestStatus.AVAILABLE, npc_giver="餐厅老板",
                dialogue_start="你好！我需要一些新鲜的胡萝卜。",
                dialogue_complete="太感谢了！"
            ),
            Quest(
                id="side_2", name="🌻 花园美化", description="花卉展览需要美丽的花朵。",
                quest_type=QuestType.SIDE,
                objectives=[
                    QuestObjective("种植向日葵", "plant", "向日葵", 3),
                    QuestObjective("收获向日葵", "harvest", "向日葵", 3),
                ],
                reward=QuestReward(money=500, experience=100, seeds={"玫瑰": 5, "郁金香": 5}),
                status=QuestStatus.AVAILABLE, npc_giver="花店老板",
                dialogue_start="花卉展览快到了，能帮我种一些向日葵吗？",
                dialogue_complete="这些向日葵太美了！"
            ),
        ]
        
        daily_quests = [
            Quest(
                id="daily_water", name="💧 勤劳的农夫", description="每天给作物浇水。",
                quest_type=QuestType.DAILY,
                objectives=[QuestObjective("给作物浇水", "water", "any", 5)],
                reward=QuestReward(money=50, experience=20),
                status=QuestStatus.AVAILABLE, time_limit=1
            ),
            Quest(
                id="daily_harvest", name="🌾 收获季节", description="每天收获作物。",
                quest_type=QuestType.DAILY,
                objectives=[QuestObjective("收获作物", "harvest", "any", 3)],
                reward=QuestReward(money=100, experience=30),
                status=QuestStatus.AVAILABLE, time_limit=1
            ),
        ]
        
        for quest in main_quests + side_quests + daily_quests:
            self.quests[quest.id] = quest
    
    def update_quest_availability(self, completed_quest_ids: List[str]) -> List[str]:
        newly_available = []
        for quest_id, quest in self.quests.items():
            if quest.status == QuestStatus.LOCKED:
                if all(pre in completed_quest_ids for pre in quest.prerequisites):
                    quest.status = QuestStatus.AVAILABLE
                    newly_available.append(quest_id)
        return newly_available
    
    def accept_quest(self, quest_id: str, current_day: int) -> tuple:
        quest = self.quests.get(quest_id)
        if not quest:
            return (False, "任务不存在")
        if quest.accept(current_day):
            self.active_quests.append(quest_id)
            return (True, f"已接取任务：{quest.name}")
        return (False, "无法接取此任务")
    
    def update_objective(self, target_type: str, target_name: str, amount: int = 1) -> List[tuple]:
        completed = []
        for quest_id in self.active_quests[:]:
            quest = self.quests.get(quest_id)
            if quest and quest.status == QuestStatus.IN_PROGRESS:
                quest.update_objective(target_type, target_name, amount)
                if quest.is_complete():
                    completed.append((quest_id, quest.name))
        return completed
    
    def complete_quest(self, quest_id: str, current_day: int) -> tuple:
        quest = self.quests.get(quest_id)
        if not quest:
            return (False, "任务不存在", None)
        if quest.complete(current_day):
            if quest_id in self.active_quests:
                self.active_quests.remove(quest_id)
            self.completed_quests.append(quest_id)
            return (True, f"任务完成：{quest.name}", quest.reward)
        return (False, "任务未完成", None)
    
    def check_timeouts(self, current_day: int) -> List[str]:
        failed = []
        for quest_id in self.active_quests[:]:
            quest = self.quests.get(quest_id)
            if quest and quest.time_limit:
                if quest.start_day and (current_day - quest.start_day) >= quest.time_limit:
                    quest.status = QuestStatus.FAILED
                    self.active_quests.remove(quest_id)
                    failed.append(quest.name)
        return failed
    
    def get_quest(self, quest_id: str) -> Optional[Quest]:
        return self.quests.get(quest_id)
    
    def get_active_quests(self) -> List[Quest]:
        return [self.quests[qid] for qid in self.active_quests if qid in self.quests]
    
    def get_available_quests(self) -> List[Quest]:
        return [q for q in self.quests.values() if q.status == QuestStatus.AVAILABLE]
