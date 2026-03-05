"""
剧情系统模块
提供完整的剧情故事线、章节管理和剧情推进功能
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum


class StoryNodeType(Enum):
    DIALOGUE = "对话"
    NARRATION = "旁白"
    CHOICE = "选择"
    EVENT = "事件"
    BATTLE = "战斗"
    REWARD = "奖励"


class StoryStatus(Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class StoryChoice:
    choice_id: str
    text: str
    next_node_id: str
    condition: Optional[str] = None
    effect: Optional[Dict] = None


@dataclass
class StoryNode:
    node_id: str
    node_type: StoryNodeType
    title: str
    content: str
    speaker: Optional[str] = None
    choices: List[StoryChoice] = field(default_factory=list)
    next_node_id: Optional[str] = None
    rewards: Dict = field(default_factory=dict)
    effects: Dict = field(default_factory=dict)
    background: Optional[str] = None
    character_image: Optional[str] = None
    
    def has_choices(self) -> bool:
        return len(self.choices) > 0
    
    def is_end_node(self) -> bool:
        return self.next_node_id is None and not self.has_choices()


@dataclass
class StoryChapter:
    chapter_id: str
    chapter_number: int
    title: str
    description: str
    nodes: Dict[str, StoryNode] = field(default_factory=dict)
    start_node_id: Optional[str] = None
    status: StoryStatus = StoryStatus.LOCKED
    unlock_condition: Optional[Dict] = None
    completion_rewards: Dict = field(default_factory=dict)
    
    def get_start_node(self) -> Optional[StoryNode]:
        if self.start_node_id and self.start_node_id in self.nodes:
            return self.nodes[self.start_node_id]
        return None
    
    def get_node(self, node_id: str) -> Optional[StoryNode]:
        return self.nodes.get(node_id)
    
    def is_completed(self) -> bool:
        return self.status == StoryStatus.COMPLETED


class StoryManager:
    
    def __init__(self):
        self.chapters: Dict[str, StoryChapter] = {}
        self.current_chapter_id: Optional[str] = None
        self.current_node_id: Optional[str] = None
        self.story_flags: Dict[str, bool] = {}
        self.story_variables: Dict[str, any] = {}
        self.completed_chapters: List[str] = []
        self.on_story_event: Optional[Callable] = None
        
        self._init_story_data()
    
    def _init_story_data(self):
        self._create_chapter_1()
        self._create_chapter_2()
        self._create_chapter_3()
        self._create_chapter_4()
        self._create_chapter_5()
        
        if self.chapters:
            first_chapter = list(self.chapters.values())[0]
            first_chapter.status = StoryStatus.AVAILABLE
    
    def _create_chapter_1(self):
        nodes = {
            "node_1_1": StoryNode(
                node_id="node_1_1",
                node_type=StoryNodeType.NARRATION,
                title="新的开始",
                content="在一个阳光明媚的早晨，你收到了一封来自远方亲戚的信件...\n\n信中写道：亲爱的孩子，我已经老了，无法再照顾那片农场。它现在属于你了。希望你能在这里找到属于自己的人生。",
                background="farm_morning"
            ),
            "node_1_2": StoryNode(
                node_id="node_1_2",
                node_type=StoryNodeType.DIALOGUE,
                title="村长的欢迎",
                content="欢迎来到星露谷！我是这里的村长。这片农场已经荒废很久了，但我相信你一定能让它重新焕发生机！",
                speaker="村长",
                character_image="village_head"
            ),
            "node_1_3": StoryNode(
                node_id="node_1_3",
                node_type=StoryNodeType.DIALOGUE,
                title="农场巡视",
                content="让我带你看看这片农场。虽然有些破旧，但土地还是很肥沃的。你看，那边有一小块已经开垦好的田地，你可以从那里开始。",
                speaker="村长",
                next_node_id="node_1_4"
            ),
            "node_1_4": StoryNode(
                node_id="node_1_4",
                node_type=StoryNodeType.CHOICE,
                title="选择你的起点",
                content="村长递给你一袋种子，问道：你想先种什么呢？",
                speaker="村长",
                choices=[
                    StoryChoice(
                        choice_id="choice_potato",
                        text="我想种土豆，听说它很好养活",
                        next_node_id="node_1_5a"
                    ),
                    StoryChoice(
                        choice_id="choice_carrot",
                        text="胡萝卜怎么样？生长很快！",
                        next_node_id="node_1_5b"
                    ),
                    StoryChoice(
                        choice_id="choice_wheat",
                        text="我想试试种小麦",
                        next_node_id="node_1_5c"
                    )
                ]
            ),
            "node_1_5a": StoryNode(
                node_id="node_1_5a",
                node_type=StoryNodeType.DIALOGUE,
                title="土豆的选择",
                content="很好的选择！土豆是最适合新手的作物。它们耐寒、易种、产量稳定。这里给你10颗土豆种子！",
                speaker="村长",
                rewards={"seeds": {"土豆": 10}},
                next_node_id="node_1_6"
            ),
            "node_1_5b": StoryNode(
                node_id="node_1_5b",
                node_type=StoryNodeType.DIALOGUE,
                title="胡萝卜的选择",
                content="胡萝卜？眼光不错！它们生长快速，可以让你很快看到成果。这里给你15颗胡萝卜种子！",
                speaker="村长",
                rewards={"seeds": {"胡萝卜": 15}},
                next_node_id="node_1_6"
            ),
            "node_1_5c": StoryNode(
                node_id="node_1_5c",
                node_type=StoryNodeType.DIALOGUE,
                title="小麦的选择",
                content="小麦？有远见！虽然利润不高，但可以大规模种植。这里给你20颗小麦种子！",
                speaker="村长",
                rewards={"seeds": {"小麦": 20}},
                next_node_id="node_1_6"
            ),
            "node_1_6": StoryNode(
                node_id="node_1_6",
                node_type=StoryNodeType.NARRATION,
                title="第一章完成",
                content="就这样，你在星露谷的新生活开始了。\n\n村长离开后，你站在田边，望着这片即将属于你的土地。阳光洒在脸上，你感到前所未有的希望。\n\n【第一章：新的开始 - 完成】",
                rewards={"money": 100, "exp": 50}
            )
        }
        
        chapter = StoryChapter(
            chapter_id="chapter_1",
            chapter_number=1,
            title="🌱 新的开始",
            description="你来到了星露谷，继承了远房亲戚留下的农场。一切从这里开始...",
            nodes=nodes,
            start_node_id="node_1_1",
            status=StoryStatus.AVAILABLE,
            completion_rewards={"money": 500, "exp": 100}
        )
        self.chapters["chapter_1"] = chapter
    
    def _create_chapter_2(self):
        nodes = {
            "node_2_1": StoryNode(
                node_id="node_2_1",
                node_type=StoryNodeType.NARRATION,
                title="商人的到来",
                content="几天后，一辆马车停在了你的农场门口。一位穿着华丽的商人走了下来。\n\n'你好啊，年轻的农夫！我是皮埃尔，镇上杂货店的老板。听说有新邻居来了，我特意来看看！'"
            ),
            "node_2_2": StoryNode(
                node_id="node_2_2",
                node_type=StoryNodeType.DIALOGUE,
                title="杂货店介绍",
                content="我在镇上经营杂货店，那里有各种种子和农具出售。如果你需要什么，随时欢迎光临！\n\n对了，我这里有些特价种子，你想看看吗？",
                speaker="皮埃尔",
                character_image="merchant"
            ),
            "node_2_3": StoryNode(
                node_id="node_2_3",
                node_type=StoryNodeType.EVENT,
                title="商店解锁",
                content="【系统提示】商店系统已解锁！\n\n你可以在商店购买各种种子和道具。不同的季节有不同的作物可供选择。",
                effects={"unlock_feature": "shop"},
                next_node_id="node_2_4"
            ),
            "node_2_4": StoryNode(
                node_id="node_2_4",
                node_type=StoryNodeType.DIALOGUE,
                title="经营建议",
                content="记住，种地要看季节。春天适合种土豆和胡萝卜，夏天可以种番茄和玉米，秋天有南瓜和茄子。\n\n还有，别忘了每天浇水！除非下雨天，那就不需要了。",
                speaker="皮埃尔",
                next_node_id="node_2_5"
            ),
            "node_2_5": StoryNode(
                node_id="node_2_5",
                node_type=StoryNodeType.NARRATION,
                title="第二章完成",
                content="皮埃尔离开后，你对这个小镇有了更多了解。\n\n商店系统已经解锁，你可以购买更多的种子来扩大种植规模了。\n\n【第二章：商人的到来 - 完成】",
                rewards={"money": 200, "exp": 75}
            )
        }
        
        chapter = StoryChapter(
            chapter_id="chapter_2",
            chapter_number=2,
            title="🛒 商人的到来",
            description="镇上的商人皮埃尔来访，为你带来了商店系统。",
            nodes=nodes,
            start_node_id="node_2_1",
            status=StoryStatus.LOCKED,
            unlock_condition={"type": "harvest_count", "value": 5},
            completion_rewards={"money": 800, "exp": 150}
        )
        self.chapters["chapter_2"] = chapter
    
    def _create_chapter_3(self):
        nodes = {
            "node_3_1": StoryNode(
                node_id="node_3_1",
                node_type=StoryNodeType.NARRATION,
                title="神秘的矿洞",
                content="一天，你在农场附近散步时，发现了一个被藤蔓遮盖的洞口。\n\n好奇心驱使你拨开藤蔓，发现这竟然是一个矿洞入口！"
            ),
            "node_3_2": StoryNode(
                node_id="node_3_2",
                node_type=StoryNodeType.DIALOGUE,
                title="冒险者的警告",
                content="等等！那里很危险！\n\n一个背着剑的冒险者突然出现，拦住了你。",
                speaker="冒险者",
                character_image="adventurer"
            ),
            "node_3_3": StoryNode(
                node_id="node_3_3",
                node_type=StoryNodeType.DIALOGUE,
                title="矿洞的秘密",
                content="这个矿洞曾经是矿工们工作的地方，但后来出现了怪物。现在只有有准备的人才敢进去。\n\n不过，里面确实有很多珍贵的矿石和宝藏...",
                speaker="冒险者",
                next_node_id="node_3_4"
            ),
            "node_3_4": StoryNode(
                node_id="node_3_4",
                node_type=StoryNodeType.CHOICE,
                title="你的决定",
                content="你想现在就进去看看吗？",
                speaker="冒险者",
                choices=[
                    StoryChoice(
                        choice_id="explore_now",
                        text="我准备好了，让我进去！",
                        next_node_id="node_3_5a"
                    ),
                    StoryChoice(
                        choice_id="explore_later",
                        text="还是先准备一下吧...",
                        next_node_id="node_3_5b"
                    )
                ]
            ),
            "node_3_5a": StoryNode(
                node_id="node_3_5a",
                node_type=StoryNodeType.EVENT,
                title="探险系统解锁",
                content="【系统提示】探险系统已解锁！\n\n你可以在户外探险中探索矿洞，收集矿石和宝藏。\n但要小心，探险需要消耗体力！",
                effects={"unlock_feature": "exploration"},
                rewards={"item": {"铁剑": 1, "火把": 5}},
                next_node_id="node_3_6"
            ),
            "node_3_5b": StoryNode(
                node_id="node_3_5b",
                node_type=StoryNodeType.DIALOGUE,
                title="明智的选择",
                content="明智的选择！等你准备好了再来吧。我可以给你一些基础装备。\n\n这个矿洞不会跑的，它一直在这里等着勇敢的探险者。",
                speaker="冒险者",
                rewards={"item": {"铁剑": 1, "火把": 5}},
                effects={"unlock_feature": "exploration"},
                next_node_id="node_3_6"
            ),
            "node_3_6": StoryNode(
                node_id="node_3_6",
                node_type=StoryNodeType.NARRATION,
                title="第三章完成",
                content="矿洞的发现为你打开了新的可能性。\n\n探险系统已经解锁，你可以在户外探索中寻找矿石和宝藏。\n\n【第三章：神秘的矿洞 - 完成】",
                rewards={"money": 300, "exp": 100}
            )
        }
        
        chapter = StoryChapter(
            chapter_id="chapter_3",
            chapter_number=3,
            title="⛏️ 神秘的矿洞",
            description="发现了一个神秘的矿洞，里面隐藏着珍贵的矿石和宝藏。",
            nodes=nodes,
            start_node_id="node_3_1",
            status=StoryStatus.LOCKED,
            unlock_condition={"type": "days_played", "value": 7},
            completion_rewards={"money": 1000, "exp": 200}
        )
        self.chapters["chapter_3"] = chapter
    
    def _create_chapter_4(self):
        nodes = {
            "node_4_1": StoryNode(
                node_id="node_4_1",
                node_type=StoryNodeType.NARRATION,
                title="可爱的小家伙",
                content="一个雨天的傍晚，你在回家的路上听到了微弱的叫声。\n\n循声望去，你发现一只小狗躲在屋檐下，浑身湿透，瑟瑟发抖。"
            ),
            "node_4_2": StoryNode(
                node_id="node_4_2",
                node_type=StoryNodeType.CHOICE,
                title="你的选择",
                content="小狗用可怜巴巴的眼神看着你。你会怎么做？",
                choices=[
                    StoryChoice(
                        choice_id="adopt_dog",
                        text="把它带回家照顾",
                        next_node_id="node_4_3a"
                    ),
                    StoryChoice(
                        choice_id="find_owner",
                        text="帮它找主人",
                        next_node_id="node_4_3b"
                    )
                ]
            ),
            "node_4_3a": StoryNode(
                node_id="node_4_3a",
                node_type=StoryNodeType.EVENT,
                title="宠物系统解锁",
                content="【系统提示】宠物系统已解锁！\n\n你收养了一只小狗，给它取个名字吧！\n宠物可以陪伴你，还能帮助你照看农场。",
                effects={"unlock_feature": "pet"},
                rewards={"pet": {"type": "dog", "name": "小黄"}},
                next_node_id="node_4_4"
            ),
            "node_4_3b": StoryNode(
                node_id="node_4_3b",
                node_type=StoryNodeType.DIALOGUE,
                title="寻找主人",
                content="你在镇上打听了一圈，发现这只小狗是流浪狗。\n\n村长看到你对它的关心，说：'既然你这么有爱心，不如就收养它吧？'",
                speaker="村长",
                effects={"unlock_feature": "pet"},
                rewards={"pet": {"type": "dog", "name": "小黄"}},
                next_node_id="node_4_4"
            ),
            "node_4_4": StoryNode(
                node_id="node_4_4",
                node_type=StoryNodeType.NARRATION,
                title="第四章完成",
                content="从此，你有了一个忠实的伙伴。\n\n宠物系统已经解锁，你可以照顾和培养你的宠物。\n\n【第四章：可爱的小家伙 - 完成】",
                rewards={"money": 100, "exp": 150}
            )
        }
        
        chapter = StoryChapter(
            chapter_id="chapter_4",
            chapter_number=4,
            title="🐕 可爱的小家伙",
            description="在雨天遇到了一只流浪小狗，你的选择将决定它的命运。",
            nodes=nodes,
            start_node_id="node_4_1",
            status=StoryStatus.LOCKED,
            unlock_condition={"type": "money_earned", "value": 1000},
            completion_rewards={"money": 500, "exp": 300}
        )
        self.chapters["chapter_4"] = chapter
    
    def _create_chapter_5(self):
        nodes = {
            "node_5_1": StoryNode(
                node_id="node_5_1",
                node_type=StoryNodeType.NARRATION,
                title="丰收的季节",
                content="经过一段时间的辛勤劳作，你的农场已经初具规模。\n\n村长来到你的农场，看着满眼的绿色，满意地点了点头。"
            ),
            "node_5_2": StoryNode(
                node_id="node_5_2",
                node_type=StoryNodeType.DIALOGUE,
                title="村长的提议",
                content="年轻人，你做得很好！这片农场在你手中焕发了新生。\n\n镇上要举办丰收节，你愿意参加吗？这可是展示你农场成果的好机会！",
                speaker="村长",
                character_image="village_head"
            ),
            "node_5_3": StoryNode(
                node_id="node_5_3",
                node_type=StoryNodeType.EVENT,
                title="成就系统解锁",
                content="【系统提示】成就系统已解锁！\n\n完成各种成就可以获得丰厚奖励。\n参加丰收节可以获得特殊成就！",
                effects={"unlock_feature": "achievement"},
                next_node_id="node_5_4"
            ),
            "node_5_4": StoryNode(
                node_id="node_5_4",
                node_type=StoryNodeType.CHOICE,
                title="丰收节的选择",
                content="你想在丰收节上展示什么？",
                speaker="村长",
                choices=[
                    StoryChoice(
                        choice_id="show_crops",
                        text="展示我的农作物",
                        next_node_id="node_5_5a"
                    ),
                    StoryChoice(
                        choice_id="show_farm",
                        text="展示我的农场",
                        next_node_id="node_5_5b"
                    )
                ]
            ),
            "node_5_5a": StoryNode(
                node_id="node_5_5a",
                node_type=StoryNodeType.DIALOGUE,
                title="作物展示",
                content="太棒了！你的作物品质非常好！\n\n评委们对你的农产品赞不绝口，你获得了'最佳农产品'奖！",
                speaker="评委",
                rewards={"money": 2000, "achievement": "crop_master"},
                next_node_id="node_5_6"
            ),
            "node_5_5b": StoryNode(
                node_id="node_5_5b",
                node_type=StoryNodeType.DIALOGUE,
                title="农场展示",
                content="你的农场规划得很好！\n\n评委们对你的农场赞不绝口，你获得了'最佳农场'奖！",
                speaker="评委",
                rewards={"money": 2000, "achievement": "farm_master"},
                next_node_id="node_5_6"
            ),
            "node_5_6": StoryNode(
                node_id="node_5_6",
                node_type=StoryNodeType.NARRATION,
                title="第五章完成",
                content="丰收节的成功让你在镇上小有名气。\n\n你的农场之路才刚刚开始，未来还有更多的冒险等着你！\n\n【第五章：丰收的季节 - 完成】\n\n【第一章剧情线完结】",
                rewards={"money": 1000, "exp": 500}
            )
        }
        
        chapter = StoryChapter(
            chapter_id="chapter_5",
            chapter_number=5,
            title="🌾 丰收的季节",
            description="参加镇上的丰收节，展示你的农场成果。",
            nodes=nodes,
            start_node_id="node_5_1",
            status=StoryStatus.LOCKED,
            unlock_condition={"type": "harvest_count", "value": 50},
            completion_rewards={"money": 3000, "exp": 500}
        )
        self.chapters["chapter_5"] = chapter
    
    def start_chapter(self, chapter_id: str) -> bool:
        if chapter_id not in self.chapters:
            return False
        
        chapter = self.chapters[chapter_id]
        
        if chapter.status not in [StoryStatus.AVAILABLE, StoryStatus.IN_PROGRESS]:
            return False
        
        self.current_chapter_id = chapter_id
        chapter.status = StoryStatus.IN_PROGRESS
        
        start_node = chapter.get_start_node()
        if start_node:
            self.current_node_id = start_node.node_id
            self._trigger_event("chapter_start", chapter)
            return True
        
        return False
    
    def get_current_node(self) -> Optional[StoryNode]:
        if not self.current_chapter_id or not self.current_node_id:
            return None
        
        chapter = self.chapters.get(self.current_chapter_id)
        if chapter:
            return chapter.get_node(self.current_node_id)
        
        return None
    
    def advance_to_next_node(self, choice_id: Optional[str] = None) -> Optional[StoryNode]:
        current_node = self.get_current_node()
        if not current_node:
            return None
        
        next_node_id = None
        
        if choice_id and current_node.has_choices():
            for choice in current_node.choices:
                if choice.choice_id == choice_id:
                    next_node_id = choice.next_node_id
                    if choice.effect:
                        self._apply_effects(choice.effect)
                    break
        
        if not next_node_id and current_node.next_node_id:
            next_node_id = current_node.next_node_id
        
        if not next_node_id and current_node.is_end_node():
            self._complete_current_chapter()
            return None
        
        if next_node_id:
            chapter = self.chapters.get(self.current_chapter_id)
            if chapter and next_node_id in chapter.nodes:
                self.current_node_id = next_node_id
                next_node = chapter.get_node(next_node_id)
                
                if next_node:
                    if next_node.rewards:
                        self._trigger_event("rewards", next_node.rewards)
                    if next_node.effects:
                        self._apply_effects(next_node.effects)
                
                return next_node
        
        return None
    
    def _complete_current_chapter(self):
        if not self.current_chapter_id:
            return
        
        chapter = self.chapters.get(self.current_chapter_id)
        if chapter:
            chapter.status = StoryStatus.COMPLETED
            self.completed_chapters.append(self.current_chapter_id)
            
            if chapter.completion_rewards:
                self._trigger_event("chapter_complete", {
                    "chapter": chapter,
                    "rewards": chapter.completion_rewards
                })
            
            self._unlock_next_chapters()
        
        self.current_chapter_id = None
        self.current_node_id = None
    
    def _unlock_next_chapters(self):
        for chapter in self.chapters.values():
            if chapter.status == StoryStatus.LOCKED and chapter.unlock_condition:
                if self._check_unlock_condition(chapter.unlock_condition):
                    chapter.status = StoryStatus.AVAILABLE
                    self._trigger_event("chapter_unlock", chapter)
    
    def _check_unlock_condition(self, condition: Dict) -> bool:
        condition_type = condition.get("type")
        value = condition.get("value", 0)
        
        if condition_type == "harvest_count":
            return self.story_variables.get("total_harvest", 0) >= value
        elif condition_type == "days_played":
            return self.story_variables.get("days_played", 0) >= value
        elif condition_type == "money_earned":
            return self.story_variables.get("total_earnings", 0) >= value
        elif condition_type == "chapter_complete":
            return condition.get("chapter_id") in self.completed_chapters
        
        return False
    
    def _apply_effects(self, effects: Dict):
        for key, value in effects.items():
            if key == "set_flag":
                self.story_flags[value] = True
            elif key == "unlock_feature":
                self._trigger_event("unlock_feature", value)
    
    def _trigger_event(self, event_type: str, data):
        if self.on_story_event:
            self.on_story_event(event_type, data)
    
    def update_variable(self, key: str, value):
        self.story_variables[key] = value
    
    def get_available_chapters(self) -> List[StoryChapter]:
        return [
            chapter for chapter in self.chapters.values()
            if chapter.status in [StoryStatus.AVAILABLE, StoryStatus.IN_PROGRESS]
        ]
    
    def get_chapter_progress(self) -> Dict:
        total = len(self.chapters)
        completed = len(self.completed_chapters)
        return {
            "total": total,
            "completed": completed,
            "percentage": (completed / total * 100) if total > 0 else 0
        }
    
    def is_in_story(self) -> bool:
        return self.current_chapter_id is not None and self.current_node_id is not None
    
    def get_save_data(self) -> Dict:
        return {
            "current_chapter_id": self.current_chapter_id,
            "current_node_id": self.current_node_id,
            "story_flags": self.story_flags,
            "story_variables": self.story_variables,
            "completed_chapters": self.completed_chapters,
            "chapter_statuses": {
                ch_id: ch.status.value for ch_id, ch in self.chapters.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.current_chapter_id = data.get("current_chapter_id")
        self.current_node_id = data.get("current_node_id")
        self.story_flags = data.get("story_flags", {})
        self.story_variables = data.get("story_variables", {})
        self.completed_chapters = data.get("completed_chapters", [])
        
        for ch_id, status_str in data.get("chapter_statuses", {}).items():
            if ch_id in self.chapters:
                self.chapters[ch_id].status = StoryStatus(status_str)
