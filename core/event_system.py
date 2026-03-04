"""
事件系统模块
管理游戏中的各种事件，包括剧情事件、随机事件等
"""

import random
from typing import List, Optional, Dict, Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GameEvent:
    """
    游戏事件基类
    """
    id: str
    name: str
    description: str
    probability: float  # 事件触发概率
    min_day: int = 1  # 最小触发天数
    max_day: Optional[int] = None  # 最大触发天数，None表示无限制
    required_season: Optional[str] = None  # 要求的季节，None表示所有季节
    required_weather: Optional[str] = None  # 要求的天气，None表示所有天气
    required_money: int = 0  # 要求的最低金币
    required_farm_level: int = 0  # 要求的最低农场等级
    has_occurred: bool = False  # 事件是否已经发生
    
    def can_trigger(self, game_manager) -> bool:
        """
        检查事件是否可以触发
        
        Args:
            game_manager: 游戏管理器实例
            
        Returns:
            bool: 是否可以触发
        """
        if self.has_occurred:
            return False
        
        # 检查天数
        current_day = game_manager.time_system.get_total_days()
        if current_day < self.min_day:
            return False
        if self.max_day is not None and current_day > self.max_day:
            return False
        
        # 检查季节
        if self.required_season:
            current_season = game_manager.time_system.season.value
            if current_season != self.required_season:
                return False
        
        # 检查天气
        if self.required_weather:
            current_weather = game_manager.time_system.weather.value
            if current_weather != self.required_weather:
                return False
        
        # 检查金币
        if game_manager.player.money < self.required_money:
            return False
        
        # 检查农场等级
        if game_manager.player.upgrade_level < self.required_farm_level:
            return False
        
        return True
    
    def trigger(self, game_manager) -> str:
        """
        触发事件
        
        Args:
            game_manager: 游戏管理器实例
            
        Returns:
            str: 事件触发后的消息
        """
        self.has_occurred = True
        return self.description


@dataclass
class StoryEvent(GameEvent):
    """
    剧情事件
    """
    chapter: int = 1  # 章节
    is_main_story: bool = True  # 是否为主线剧情
    next_event_id: Optional[str] = None  # 下一个事件ID


@dataclass
class RandomEvent(GameEvent):
    """
    随机事件
    """
    repeatable: bool = False  # 是否可重复触发
    
    def trigger(self, game_manager) -> str:
        """
        触发事件
        
        Args:
            game_manager: 游戏管理器实例
            
        Returns:
            str: 事件触发后的消息
        """
        if not self.repeatable:
            self.has_occurred = True
        return self.description


@dataclass
class QuestEvent(GameEvent):
    """
    任务事件
    """
    quest_id: str = ""
    reward_money: int = 0
    reward_items: Optional[Dict[str, int]] = None
    
    def __post_init__(self):
        if self.reward_items is None:
            self.reward_items = {}
        if not self.quest_id:
            raise ValueError("QuestEvent must have a quest_id")
    
    def trigger(self, game_manager) -> str:
        """
        触发事件
        
        Args:
            game_manager: 游戏管理器实例
            
        Returns:
            str: 事件触发后的消息
        """
        self.has_occurred = True
        
        # 给予奖励
        if self.reward_money > 0:
            game_manager.player.earn_money(self.reward_money)
        
        for item_name, quantity in self.reward_items.items():
            for _ in range(quantity):
                game_manager.player.add_to_inventory(item_name)
        
        return self.description


class EventSystem:
    """
    事件系统类
    """
    
    def __init__(self):
        """初始化事件系统"""
        self.events: List[GameEvent] = []
        self.init_events()
    
    def init_events(self):
        """初始化事件"""
        # 主线剧情事件
        main_story_events = [
            StoryEvent(
                id="story_1",
                name="新的开始",
                description="你来到了宁静村，接管了爷爷留下的农场。村长王大爷热情地欢迎你，告诉你这是一个充满希望的地方。\n\n王大爷：'欢迎来到宁静村，年轻人！你爷爷的农场已经闲置很久了，我们都期待着它重新焕发生机。'\n\n你：'谢谢您，王大爷。我会努力经营好这个农场的。'\n\n王大爷：'很好！村里的人都会帮助你的。有什么需要，随时来找我。'",
                probability=1.0,
                min_day=1,
                max_day=1,
                is_main_story=True,
                next_event_id="story_2"
            ),
            StoryEvent(
                id="story_2",
                name="第一个挑战",
                description="你的农场需要清理和翻整土地。邻居李婶给你送来了一些工具和种子。\n\n李婶：'听说你来了，我特意给你带了一些种子和工具。刚开始可能会有点累，但坚持下去就会好的。'\n\n你：'太感谢您了，李婶！这些对我来说真是及时雨。'\n\n李婶：'别客气，我们都是邻居嘛。有时间来我家喝杯茶。'",
                probability=1.0,
                min_day=2,
                max_day=5,
                is_main_story=True,
                next_event_id="story_3"
            ),
            StoryEvent(
                id="story_3",
                name="神秘的访客",
                description="一位神秘的商人来到你的农场，他对你的农场很感兴趣。\n\n商人：'年轻人，你的农场很有潜力。我可以提供一些稀有的种子和工具，但你需要用农场的产品来交换。'\n\n你：'好的，我很乐意和你合作。'\n\n商人：'很好，我们的合作会很愉快的。'",
                probability=1.0,
                min_day=8,
                max_day=12,
                is_main_story=True,
                next_event_id="story_4"
            ),
            StoryEvent(
                id="story_4",
                name="农场升级",
                description="你的农场已经有了一定的规模，王大爷建议你升级农场设施。\n\n王大爷：'你的农场经营得不错，是时候考虑升级了。升级后可以种植更多种类的作物，也能提高产量。'\n\n你：'好的，我会考虑的。'\n\n王大爷：'需要帮助的话，村里的木匠张师傅可以帮你。'",
                probability=1.0,
                min_day=15,
                max_day=20,
                required_farm_level=1,
                is_main_story=True,
                next_event_id="story_5"
            ),
            StoryEvent(
                id="story_5",
                name="季节变换",
                description="季节变换了，李婶提醒你要种植适合的作物。\n\n李婶：'秋天到了，该种些适合这个季节的作物了。我这里有一些秋播的种子，你可以拿去试试。'\n\n你：'谢谢您，李婶。我会按照您的建议种植的。'\n\n李婶：'不客气，希望你有个好收成。'",
                probability=1.0,
                min_day=25,
                max_day=30,
                is_main_story=True,
                next_event_id="story_6"
            ),
            StoryEvent(
                id="story_6",
                name="丰收季节",
                description="丰收季节到了，你的努力得到了回报。村民们都来祝贺你。\n\n王大爷：'恭喜你，年轻人！你的农场经营得非常好。'\n\n李婶：'看看这些丰收的作物，真是让人高兴！'\n\n你：'谢谢大家的帮助和支持，没有你们我不可能做到这些。'\n\n王大爷：'这是你自己的努力，我们都为你感到骄傲。'",
                probability=1.0,
                min_day=40,
                max_day=45,
                is_main_story=True,
                next_event_id="story_7"
            ),
            StoryEvent(
                id="story_7",
                name="新的机遇",
                description="一位城里的餐厅老板来到你的农场，想要和你长期合作。\n\n餐厅老板：'你的农产品质量很好，我想和你签订长期合同，定期收购你的作物。'\n\n你：'好的，这对我来说是个很好的机会。'\n\n餐厅老板：'那我们就这么说定了，希望我们合作愉快。'",
                probability=1.0,
                min_day=50,
                max_day=55,
                is_main_story=True
            )
        ]
        
        # 随机事件
        random_events = [
            RandomEvent(
                id="random_1",
                name="友好的邻居",
                description="你的邻居给你送来了一些种子和新鲜的蔬菜。\n\n邻居：'这是我家种的一些蔬菜，还有一些多余的种子，你拿去种吧。'\n\n你：'太感谢了，真是太贴心了！'\n\n邻居：'别客气，都是邻居嘛。'",
                probability=0.1,
                min_day=3,
                repeatable=True
            ),
            RandomEvent(
                id="random_2",
                name="暴风雨",
                description="一场暴风雨袭击了你的农场，一些作物受损了。\n\n你：'唉，这场暴风雨把我的一些作物弄坏了。'\n\n李婶：'别担心，天气总会变好的。我们一起想办法补救。'",
                probability=0.05,
                min_day=5,
                required_weather="暴风雨",
                repeatable=True
            ),
            RandomEvent(
                id="random_3",
                name="市场行情",
                description="市场对某种作物的需求增加了，价格上涨了。\n\n商人：'告诉你一个好消息，现在市场上对胡萝卜的需求很大，价格涨了不少。'\n\n你：'真的吗？那我要多种一些胡萝卜。'",
                probability=0.15,
                min_day=7,
                repeatable=True
            ),
            RandomEvent(
                id="random_4",
                name="动物来访",
                description="一只小兔子来到你的农场，它似乎很喜欢这里。\n\n你：'好可爱的小兔子！以后这里就是你的家了。'\n\n小兔子似乎听懂了你的话，蹦蹦跳跳地跑开了。",
                probability=0.08,
                min_day=10,
                repeatable=True
            ),
            RandomEvent(
                id="random_5",
                name="神秘的果实",
                description="你在农场里发现了一些神秘的果实，它们看起来很特别。\n\n你：'这些果实看起来很奇怪，不知道是什么品种。'\n\n王大爷：'哦，这是传说中的幸运果实，吃了它会带来好运的。'",
                probability=0.05,
                min_day=15,
                repeatable=False
            )
        ]
        
        # 任务事件
        quest_events = [
            QuestEvent(
                id="quest_1",
                name="收集任务",
                description="村民请求你收集一些作物，完成后会给予奖励。\n\n村民：'我需要一些小麦和胡萝卜，你能帮我收集吗？'\n\n你：'好的，我这就去收集。'\n\n完成任务后...\n\n村民：'谢谢你的帮助，这是给你的奖励。'",
                probability=0.2,
                min_day=5,
                max_day=10,
                quest_id="collect_crops",
                reward_money=100,
                reward_items={"小麦": 5}
            ),
            QuestEvent(
                id="quest_2",
                name="种植任务",
                description="村民请求你种植一些特定的作物，完成后会给予奖励。\n\n村民：'我听说你种的西红柿特别好，能帮我种一些吗？'\n\n你：'当然可以，我这就去种。'\n\n完成任务后...\n\n村民：'太好了，谢谢你！这是给你的奖励。'",
                probability=0.15,
                min_day=10,
                max_day=15,
                quest_id="plant_crops",
                reward_money=200,
                reward_items={"胡萝卜种子": 10}
            ),
            QuestEvent(
                id="quest_3",
                name="救援任务",
                description="李婶的小猫被困在了树上，她请求你帮助救援。\n\n李婶：'我的小猫爬到树上下不来了，你能帮我把它救下来吗？'\n\n你：'没问题，我这就去救它。'\n\n完成任务后...\n\n李婶：'太谢谢你了！这只小猫是我的宝贝。这是给你的奖励。'",
                probability=0.1,
                min_day=12,
                max_day=18,
                quest_id="rescue_cat",
                reward_money=150,
                reward_items={"苹果": 3}
            ),
            QuestEvent(
                id="quest_4",
                name="节日准备",
                description="村里要举办丰收节，需要你提供一些作物作为庆典用品。\n\n王大爷：'丰收节快到了，我们需要一些新鲜的作物来庆祝。你能提供一些吗？'\n\n你：'当然可以，我会准备好的。'\n\n完成任务后...\n\n王大爷：'太好了！这些作物看起来很棒。这是给你的奖励，谢谢你的帮助。'",
                probability=0.15,
                min_day=30,
                max_day=35,
                quest_id="harvest_festival",
                reward_money=300,
                reward_items={"金苹果": 1, "小麦种子": 20}
            )
        ]
        
        # 将所有事件添加到事件列表中
        self.events.extend(main_story_events)
        self.events.extend(random_events)
        self.events.extend(quest_events)
    
    def check_events(self, game_manager) -> List[str]:
        """
        检查并触发事件
        
        Args:
            game_manager: 游戏管理器实例
            
        Returns:
            List[str]: 触发的事件消息列表
        """
        triggered_events = []
        
        for event in self.events:
            if event.can_trigger(game_manager):
                # 根据概率决定是否触发事件
                if random.random() < event.probability:
                    message = event.trigger(game_manager)
                    triggered_events.append(message)
        
        return triggered_events
    
    def get_event(self, event_id: str) -> Optional[GameEvent]:
        """
        根据ID获取事件
        
        Args:
            event_id: 事件ID
            
        Returns:
            Optional[GameEvent]: 事件对象，不存在返回None
        """
        for event in self.events:
            if event.id == event_id:
                return event
        return None
    
    def reset_events(self):
        """
        重置所有事件
        """
        for event in self.events:
            event.has_occurred = False
