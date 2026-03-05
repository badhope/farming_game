"""
生化危机随机事件系统模块
提供15种以上不同类型的随机遭遇事件
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import random


class RandomEventType(Enum):
    RESOURCE_SUPPLY = "resource_supply"
    SUDDEN_INFECTION = "sudden_infection"
    NPC_HELP = "npc_help"
    COMBAT_ENCOUNTER = "combat_encounter"
    DISCOVERY = "discovery"
    TRADE = "trade"
    WEATHER_HAZARD = "weather_hazard"
    LOOT = "loot"
    MORALE_EVENT = "morale_event"
    INFECTION_SPREAD = "infection_spread"
    RESCUE_MISSION = "rescue_mission"
    SUPPLY_DROP = "supply_drop"
    TRAP = "trap"
    ALLIANCE = "alliance"
    BETRAYAL = "betrayal"
    MIRACLE = "miracle"
    HORROR = "horror"


class EventPriority(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5


@dataclass
class EventChoice:
    choice_id: str
    text: str
    success_rate: float = 1.0
    requirements: Dict = field(default_factory=dict)
    rewards: Dict = field(default_factory=dict)
    penalties: Dict = field(default_factory=dict)
    next_event_id: Optional[str] = None


@dataclass
class RandomEvent:
    event_id: str
    event_type: RandomEventType
    title: str
    description: str
    icon: str
    choices: List[EventChoice] = field(default_factory=list)
    priority: EventPriority = EventPriority.COMMON
    min_day: int = 1
    max_day: int = 999
    min_infection_rate: float = 0.0
    max_infection_rate: float = 1.0
    cooldown_days: int = 0
    one_time: bool = False
    location_requirement: Optional[str] = None


BIOHAZARD_EVENTS = [
    RandomEvent(
        event_id="supply_cache",
        event_type=RandomEventType.RESOURCE_SUPPLY,
        title="📦 补给箱",
        description="""
你在废墟中发现了一个完好无损的补给箱！

箱子上印着军方的标志，看起来是空投物资。
你不确定里面有什么，但任何资源都是宝贵的。
        """,
        icon="📦",
        choices=[
            EventChoice(
                choice_id="open_carefully",
                text="小心打开",
                success_rate=0.95,
                rewards={"money": 100, "items": {"食物": 3, "水": 2, "药品": 1}}
            ),
            EventChoice(
                choice_id="open_quickly",
                text="快速打开",
                success_rate=0.7,
                rewards={"money": 150, "items": {"食物": 5, "水": 3, "药品": 2, "弹药": 5}},
                penalties={"health": -10}
            ),
            EventChoice(
                choice_id="check_trap",
                text="检查是否有陷阱",
                success_rate=1.0,
                rewards={"money": 80, "items": {"食物": 2, "水": 1}}
            )
        ],
        priority=EventPriority.COMMON
    ),
    RandomEvent(
        event_id="infected_attack",
        event_type=RandomEventType.SUDDEN_INFECTION,
        title="🧟 感染者袭击！",
        description="""
突然，一群感染者从阴影中冲了出来！

他们的眼睛泛着诡异的红光，动作扭曲但迅速。
你只有几秒钟做出反应！
        """,
        icon="🧟",
        choices=[
            EventChoice(
                choice_id="fight",
                text="战斗！",
                success_rate=0.6,
                rewards={"exp": 50, "items": {"感染组织": 2}},
                penalties={"health": -30, "stress": 0.2}
            ),
            EventChoice(
                choice_id="run",
                text="逃跑！",
                success_rate=0.8,
                penalties={"stress": 0.1}
            ),
            EventChoice(
                choice_id="hide",
                text="躲藏",
                success_rate=0.7,
                rewards={"exp": 20}
            )
        ],
        priority=EventPriority.COMMON,
        min_infection_rate=0.1
    ),
    RandomEvent(
        event_id="wounded_survivor",
        event_type=RandomEventType.NPC_HELP,
        title="🩹 受伤的幸存者",
        description="""
你发现了一个受伤的幸存者，他靠在墙边，呼吸微弱。

"求求你...帮帮我..."他虚弱地说道。
他的手臂上有明显的抓痕，但你不确定是否感染。
        """,
        icon="🩹",
        choices=[
            EventChoice(
                choice_id="help_him",
                text="帮助他",
                success_rate=0.7,
                rewards={"karma": 15, "exp": 30, "new_survivor": True},
                penalties={"items": {"药品": -2}, "risk": 0.3}
            ),
            EventChoice(
                choice_id="give_supplies",
                text="给些物资让他自己走",
                success_rate=1.0,
                rewards={"karma": 5},
                penalties={"items": {"食物": -1, "水": -1}}
            ),
            EventChoice(
                choice_id="leave_him",
                text="离开",
                success_rate=1.0,
                penalties={"karma": -10, "stress": 0.05}
            )
        ],
        priority=EventPriority.COMMON
    ),
    RandomEvent(
        event_id="military_patrol",
        event_type=RandomEventType.COMBAT_ENCOUNTER,
        title="🎖️ 军方巡逻队",
        description="""
一支全副武装的军方巡逻队出现在你面前。

"停下！接受检查！"队长喊道。
他们的表情严肃，枪口微微抬起。
        """,
        icon="🎖️",
        choices=[
            EventChoice(
                choice_id="cooperate",
                text="配合检查",
                success_rate=1.0,
                rewards={"exp": 20, "trust": 10}
            ),
            EventChoice(
                choice_id="negotiate",
                text="尝试交涉",
                success_rate=0.6,
                rewards={"items": {"弹药": 10}, "trust": 5},
                penalties={"money": -100}
            ),
            EventChoice(
                choice_id="avoid",
                text="悄悄避开",
                success_rate=0.5,
                penalties={"stress": 0.1}
            )
        ],
        priority=EventPriority.UNCOMMON
    ),
    RandomEvent(
        event_id="abandoned_lab",
        event_type=RandomEventType.DISCOVERY,
        title="🔬 废弃实验室",
        description="""
你发现了一个隐藏在地下室的实验室。

设备虽然蒙尘，但大部分仍然完好。
桌上散落着各种文件和试管。
        """,
        icon="🔬",
        choices=[
            EventChoice(
                choice_id="search_files",
                text="搜索文件",
                success_rate=0.8,
                rewards={"exp": 100, "items": {"研究笔记": 1, "机密文件": 1}}
            ),
            EventChoice(
                choice_id="take_samples",
                text="采集样本",
                success_rate=0.6,
                rewards={"items": {"病毒样本": 2, "解药原料": 1}},
                penalties={"health": -15, "risk": 0.4}
            ),
            EventChoice(
                choice_id="destroy_lab",
                text="销毁实验室",
                success_rate=1.0,
                rewards={"karma": 10, "exp": 50}
            )
        ],
        priority=EventPriority.RARE,
        min_day=10
    ),
    RandomEvent(
        event_id="wandering_merchant",
        event_type=RandomEventType.TRADE,
        title="🧳 流浪商人",
        description="""
一个背着大包小包的商人出现在你面前。

"嘿，朋友！想看看我的货吗？"
他神秘地笑了笑，"都是好东西，保证你在外面买不到。"
        """,
        icon="🧳",
        choices=[
            EventChoice(
                choice_id="buy_weapons",
                text="购买武器",
                success_rate=1.0,
                requirements={"money": 300},
                rewards={"items": {"手枪": 1, "弹药": 20}},
                penalties={"money": -300}
            ),
            EventChoice(
                choice_id="buy_medicine",
                text="购买药品",
                success_rate=1.0,
                requirements={"money": 200},
                rewards={"items": {"药品": 5, "绷带": 10}},
                penalties={"money": -200}
            ),
            EventChoice(
                choice_id="trade_info",
                text="交换情报",
                success_rate=0.7,
                rewards={"exp": 50, "info": "安全区位置"}
            )
        ],
        priority=EventPriority.UNCOMMON
    ),
    RandomEvent(
        event_id="toxic_fog",
        event_type=RandomEventType.WEATHER_HAZARD,
        title="🌫️ 毒雾",
        description="""
一阵诡异的绿色雾气从远处飘来。

空气中弥漫着刺鼻的气味，你的眼睛开始刺痛。
这绝对不是普通的雾！
        """,
        icon="🌫️",
        choices=[
            EventChoice(
                choice_id="find_shelter",
                text="寻找掩体",
                success_rate=0.8,
                rewards={"exp": 20}
            ),
            EventChoice(
                choice_id="hold_breath",
                text="屏住呼吸快速通过",
                success_rate=0.5,
                penalties={"health": -25, "stress": 0.15}
            ),
            EventChoice(
                choice_id="use_mask",
                text="使用防毒面具",
                success_rate=1.0,
                requirements={"items": {"防毒面具": 1}},
                rewards={"exp": 30},
                penalties={"items": {"防毒面具": -1}}
            )
        ],
        priority=EventPriority.COMMON,
        min_infection_rate=0.3
    ),
    RandomEvent(
        event_id="hidden_bunker",
        event_type=RandomEventType.LOOT,
        title="🚪 隐藏地堡",
        description="""
你发现了一个被伪装门遮住的地下地堡。

门上有一个密码锁，但旁边有一些划痕，
似乎有人尝试过破解...
        """,
        icon="🚪",
        choices=[
            EventChoice(
                choice_id="try_default",
                text="尝试默认密码",
                success_rate=0.3,
                rewards={"money": 500, "items": {"高级武器": 1, "弹药": 50}},
                penalties={"stress": 0.1}
            ),
            EventChoice(
                choice_id="force_open",
                text="强行打开",
                success_rate=0.6,
                rewards={"money": 300, "items": {"武器": 1, "食物": 10}},
                penalties={"items": {"工具": -1}}
            ),
            EventChoice(
                choice_id="find_key",
                text="寻找钥匙",
                success_rate=0.4,
                rewards={"money": 800, "items": {"高级装备": 1, "弹药": 100}},
                penalties={"time": 2}
            )
        ],
        priority=EventPriority.RARE
    ),
    RandomEvent(
        event_id="survivor_group",
        event_type=RandomEventType.MORALE_EVENT,
        title="👥 幸存者团队",
        description="""
你遇到了一群幸存者，他们正在寻找安全的地方。

"我们听说你在经营一个农场...能收留我们吗？"
他们的领袖问道，"我们可以帮忙干活。"
        """,
        icon="👥",
        choices=[
            EventChoice(
                choice_id="accept_all",
                text="全部收留",
                success_rate=0.7,
                rewards={"karma": 20, "workers": 5, "exp": 100},
                penalties={"food_consumption": 2, "risk": 0.3}
            ),
            EventChoice(
                choice_id="accept_some",
                text="收留部分人",
                success_rate=1.0,
                rewards={"karma": 10, "workers": 2, "exp": 50},
                penalties={"food_consumption": 1}
            ),
            EventChoice(
                choice_id="refuse",
                text="婉拒",
                success_rate=1.0,
                penalties={"karma": -5}
            )
        ],
        priority=EventPriority.UNCOMMON
    ),
    RandomEvent(
        event_id="infection_wave",
        event_type=RandomEventType.INFECTION_SPREAD,
        title="🌊 感染潮",
        description="""
远处传来密集的嘶吼声，感染潮正在逼近！

你必须立刻做出决定，否则后果不堪设想。
        """,
        icon="🌊",
        choices=[
            EventChoice(
                choice_id="fortify",
                text="加固防御",
                success_rate=0.6,
                rewards={"exp": 150, "achievement_progress": "防御大师"},
                penalties={"items": {"建材": -10}, "health": -20}
            ),
            EventChoice(
                choice_id="evacuate",
                text="紧急撤离",
                success_rate=0.8,
                penalties={"items": {"部分物资": -1}, "stress": 0.2}
            ),
            EventChoice(
                choice_id="fight_head_on",
                text="正面迎战",
                success_rate=0.3,
                rewards={"exp": 300, "items": {"大量战利品": 1}},
                penalties={"health": -50, "risk": 0.7}
            )
        ],
        priority=EventPriority.EPIC,
        min_infection_rate=0.5
    ),
    RandomEvent(
        event_id="distress_signal",
        event_type=RandomEventType.RESCUE_MISSION,
        title="📻 求救信号",
        description="""
收音机里传来断断续续的求救信号：

"这里是...医疗站...感染者围攻...请求支援...
位置...坐标...请..."

信号突然中断了。
        """,
        icon="📻",
        choices=[
            EventChoice(
                choice_id="respond_immediately",
                text="立即响应",
                success_rate=0.5,
                rewards={"karma": 30, "exp": 200, "items": {"医疗设备": 1}},
                penalties={"health": -30, "time": 1}
            ),
            EventChoice(
                choice_id="gather_team",
                text="组建救援队",
                success_rate=0.7,
                requirements={"workers": 3},
                rewards={"karma": 25, "exp": 150, "new_survivors": 3},
                penalties={"time": 2}
            ),
            EventChoice(
                choice_id="ignore",
                text="忽略信号",
                success_rate=1.0,
                penalties={"karma": -20, "stress": 0.1}
            )
        ],
        priority=EventPriority.UNCOMMON,
        min_day=5
    ),
    RandomEvent(
        event_id="airdrop",
        event_type=RandomEventType.SUPPLY_DROP,
        title="🪂 空投物资",
        description="""
你看到天空中有一个降落伞正在缓缓下降！

那是一个补给箱，看起来是军方的空投。
但它落在了危险区域...
        """,
        icon="🪂",
        choices=[
            EventChoice(
                choice_id="rush_to_get",
                text="冲过去抢夺",
                success_rate=0.5,
                rewards={"money": 300, "items": {"高级物资": 1, "弹药": 30}},
                penalties={"health": -20, "stress": 0.15}
            ),
            EventChoice(
                choice_id="wait_and_see",
                text="等待观察",
                success_rate=0.8,
                rewards={"money": 150, "items": {"普通物资": 1}}
            ),
            EventChoice(
                choice_id="let_it_go",
                text="放弃",
                success_rate=1.0
            )
        ],
        priority=EventPriority.RARE
    ),
    RandomEvent(
        event_id="ambush",
        event_type=RandomEventType.TRAP,
        title="⚠️ 伏击！",
        description="""
当你走进一条小巷时，突然意识到这是个陷阱！

周围出现了几个持枪的人，他们的眼神充满恶意。
"把值钱的东西都交出来！"领头的人喊道。
        """,
        icon="⚠️",
        choices=[
            EventChoice(
                choice_id="fight_back",
                text="反击！",
                success_rate=0.4,
                rewards={"money": 200, "items": {"武器": 1, "弹药": 15}},
                penalties={"health": -40}
            ),
            EventChoice(
                choice_id="surrender",
                text="投降",
                success_rate=1.0,
                penalties={"money": -200, "items": {"部分装备": -1}}
            ),
            EventChoice(
                choice_id="negotiate",
                text="谈判",
                success_rate=0.5,
                penalties={"money": -100}
            ),
            EventChoice(
                choice_id="escape",
                text="尝试逃脱",
                success_rate=0.3,
                penalties={"health": -20, "stress": 0.2}
            )
        ],
        priority=EventPriority.UNCOMMON
    ),
    RandomEvent(
        event_id="resistance_contact",
        event_type=RandomEventType.ALLIANCE,
        title="🏴 反抗军联络",
        description="""
一个穿着迷彩服的人悄悄接近你。

"我们代表反抗军，"他低声说，
"我们一直在观察你，你似乎是个可以信任的人。
愿意加入我们吗？"
        """,
        icon="🏴",
        choices=[
            EventChoice(
                choice_id="join",
                text="加入反抗军",
                success_rate=1.0,
                rewards={"exp": 100, "trust": 30, "items": {"反抗军徽章": 1}},
                next_event_id="resistance_mission"
            ),
            EventChoice(
                choice_id="ask_more",
                text="询问更多信息",
                success_rate=1.0,
                rewards={"info": "反抗军情报"}
            ),
            EventChoice(
                choice_id="refuse",
                text="婉拒",
                success_rate=1.0,
                penalties={"trust": -10}
            )
        ],
        priority=EventPriority.RARE,
        min_day=15
    ),
    RandomEvent(
        event_id="traitor_reveal",
        event_type=RandomEventType.BETRAYAL,
        title="🎭 叛徒暴露",
        description="""
你无意中发现了一个令人震惊的事实：

你团队中有人在暗中与感染者交易！
他似乎在用活人换取...某种保护。
        """,
        icon="🎭",
        choices=[
            EventChoice(
                choice_id="confront",
                text="当面对质",
                success_rate=0.6,
                rewards={"exp": 100},
                penalties={"workers": -1, "stress": 0.2}
            ),
            EventChoice(
                choice_id="secret_investigate",
                text="暗中调查",
                success_rate=0.8,
                rewards={"exp": 50, "info": "叛徒证据"}
            ),
            EventChoice(
                choice_id="eliminate",
                text="...处理掉",
                success_rate=0.9,
                rewards={"exp": 30},
                penalties={"karma": -15, "workers": -1}
            )
        ],
        priority=EventPriority.EPIC,
        min_day=20,
        one_time=True
    ),
    RandomEvent(
        event_id="miracle_cure",
        event_type=RandomEventType.MIRACLE,
        title="✨ 奇迹",
        description="""
在一个废弃的医院里，你发现了一个奇迹：

一个完全康复的感染者！

"我...我好了，"他不敢相信地看着自己的手，
"那个药物...在地下室..."
        """,
        icon="✨",
        choices=[
            EventChoice(
                choice_id="search_basement",
                text="搜索地下室",
                success_rate=0.7,
                rewards={"items": {"解药原型": 1, "研究资料": 1}, "exp": 200}
            ),
            EventChoice(
                choice_id="take_survivor",
                text="带走康复者",
                success_rate=0.8,
                rewards={"karma": 20, "info": "康复者血液样本"},
                penalties={"food_consumption": 1}
            ),
            EventChoice(
                choice_id="report_finding",
                text="报告发现",
                success_rate=1.0,
                rewards={"trust": 20, "exp": 100}
            )
        ],
        priority=EventPriority.LEGENDARY,
        min_day=25,
        one_time=True
    ),
    RandomEvent(
        event_id="nightmare",
        event_type=RandomEventType.HORROR,
        title="💀 深夜惊魂",
        description="""
深夜，你被一阵奇怪的声音惊醒。

当你睁开眼睛，你看到一个身影站在床边...
那是一个完全变异的感染者，但它似乎在...哭泣？

"救...救我..."它发出扭曲的声音。
        """,
        icon="💀",
        choices=[
            EventChoice(
                choice_id="attack",
                text="攻击！",
                success_rate=0.8,
                rewards={"exp": 50},
                penalties={"stress": 0.3}
            ),
            EventChoice(
                choice_id="listen",
                text="倾听它",
                success_rate=0.4,
                rewards={"karma": 10, "info": "感染者保留意识", "exp": 100},
                penalties={"stress": 0.4, "risk": 0.5}
            ),
            EventChoice(
                choice_id="run_away",
                text="逃跑",
                success_rate=0.9,
                penalties={"stress": 0.2}
            )
        ],
        priority=EventPriority.EPIC,
        min_day=10
    ),
]


class RandomEventManager:
    
    def __init__(self):
        self.events: Dict[str, RandomEvent] = {}
        self.event_cooldowns: Dict[str, int] = {}
        self.triggered_one_time: List[str] = []
        self.event_history: List[Dict] = []
        self.on_event_trigger: Optional[Callable] = None
        
        self._init_events()
    
    def _init_events(self):
        for event in BIOHAZARD_EVENTS:
            self.events[event.event_id] = event
    
    def get_available_events(self, current_day: int, infection_rate: float, 
                            location: Optional[str] = None) -> List[RandomEvent]:
        available = []
        
        for event in self.events.values():
            if event.event_id in self.triggered_one_time and event.one_time:
                continue
            
            if event.event_id in self.event_cooldowns:
                if current_day < self.event_cooldowns[event.event_id]:
                    continue
            
            if current_day < event.min_day or current_day > event.max_day:
                continue
            
            if infection_rate < event.min_infection_rate or infection_rate > event.max_infection_rate:
                continue
            
            if event.location_requirement and event.location_requirement != location:
                continue
            
            available.append(event)
        
        return available
    
    def trigger_random_event(self, current_day: int, infection_rate: float,
                            location: Optional[str] = None) -> Optional[Tuple[RandomEvent, bool]]:
        available = self.get_available_events(current_day, infection_rate, location)
        
        if not available:
            return None
        
        weights = []
        for event in available:
            weight = 6 - event.priority.value
            weights.append(weight)
        
        selected = random.choices(available, weights=weights, k=1)[0]
        
        if selected.one_time:
            self.triggered_one_time.append(selected.event_id)
        
        if selected.cooldown_days > 0:
            self.event_cooldowns[selected.event_id] = current_day + selected.cooldown_days
        
        should_trigger = random.random() < 0.3
        
        return selected, should_trigger
    
    def process_choice(self, event_id: str, choice_id: str) -> Dict:
        event = self.events.get(event_id)
        if not event:
            return {"success": False, "message": "未知事件"}
        
        choice = None
        for c in event.choices:
            if c.choice_id == choice_id:
                choice = c
                break
        
        if not choice:
            return {"success": False, "message": "无效选择"}
        
        success = random.random() < choice.success_rate
        
        result = {
            "success": success,
            "event_id": event_id,
            "choice_id": choice_id,
            "event_title": event.title,
            "rewards": {},
            "penalties": {},
            "message": ""
        }
        
        if success:
            result["rewards"] = choice.rewards.copy()
            result["message"] = "行动成功！"
        else:
            result["penalties"] = choice.penalties.copy()
            result["message"] = "行动失败..."
        
        self.event_history.append({
            "day": 0,
            "event_id": event_id,
            "choice_id": choice_id,
            "success": success
        })
        
        return result
    
    def get_event_by_id(self, event_id: str) -> Optional[RandomEvent]:
        return self.events.get(event_id)
    
    def get_event_stats(self) -> Dict:
        total_events = len(self.events)
        triggered = len(self.triggered_one_time)
        
        type_counts = {}
        for event in self.events.values():
            type_name = event.event_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        return {
            "total_events": total_events,
            "triggered_one_time": triggered,
            "type_distribution": type_counts,
            "history_count": len(self.event_history)
        }
    
    def advance_day(self):
        to_remove = []
        for event_id, cooldown_day in self.event_cooldowns.items():
            if cooldown_day <= 0:
                to_remove.append(event_id)
        
        for event_id in to_remove:
            del self.event_cooldowns[event_id]
    
    def get_save_data(self) -> Dict:
        return {
            "event_cooldowns": self.event_cooldowns,
            "triggered_one_time": self.triggered_one_time,
            "event_history": self.event_history[-20:]
        }
    
    def load_save_data(self, data: Dict):
        self.event_cooldowns = data.get("event_cooldowns", {})
        self.triggered_one_time = data.get("triggered_one_time", [])
        self.event_history = data.get("event_history", [])
