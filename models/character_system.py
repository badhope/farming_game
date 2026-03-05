"""
增强角色系统模块
提供详细的角色档案、对话树系统和多样化NPC原型
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import random


class PersonalityTrait(Enum):
    FRIENDLY = "友善"
    GRUMPY = "暴躁"
    MYSTERIOUS = "神秘"
    CHEERFUL = "开朗"
    SHY = "害羞"
    BRAVE = "勇敢"
    WISE = "睿智"
    MISCHIEVOUS = "调皮"
    GENTLE = "温柔"
    STERN = "严厉"
    OPTIMISTIC = "乐观"
    PESSIMISTIC = "悲观"
    LOYAL = "忠诚"
    AMBITIOUS = "有抱负"
    LAZY = "懒散"


class NPCArchetype(Enum):
    BLACKSMITH = "铁匠"
    MERCHANT = "商人"
    QUEST_GIVER = "任务发布者"
    HEALER = "治疗者"
    VILLAGER = "村民"
    ELDER = "长老"
    GUARD = "守卫"
    INNKEEPER = "旅馆老板"
    FARMER = "农夫"
    SCHOLAR = "学者"
    HUNTER = "猎人"
    ARTISAN = "工匠"
    WANDERING_MERCHANT = "流浪商人"
    MYSTERIOUS_STRANGER = "神秘陌生人"
    BEAST_TAMER = "驯兽师"


class VisualFeature(Enum):
    HAIR_BLACK = "黑发"
    HAIR_WHITE = "白发"
    HAIR_RED = "红发"
    HAIR_BLONDE = "金发"
    HAIR_BROWN = "棕发"
    HAIR_BLUE = "蓝发"
    EYE_BROWN = "棕色眼睛"
    EYE_BLUE = "蓝色眼睛"
    EYE_GREEN = "绿色眼睛"
    EYE_GOLD = "金色眼睛"
    EYE_RED = "红色眼睛"
    TALL = "高个子"
    SHORT = "矮个子"
    MUSCULAR = "肌肉发达"
    SLENDER = "身材修长"
    SCAR = "有伤疤"
    GLASSES = "戴眼镜"
    BEARD = "有胡须"
    TATTOO = "有纹身"
    ACCESSORY = "佩戴饰品"


class DialogueConditionType(Enum):
    FRIENDSHIP_LEVEL = "friendship_level"
    QUEST_COMPLETED = "quest_completed"
    ITEM_OWNED = "item_owned"
    TIME_OF_DAY = "time_of_day"
    SEASON = "season"
    WEATHER = "weather"
    PLAYER_LEVEL = "player_level"
    STORY_PROGRESS = "story_progress"
    REPUTATION = "reputation"
    VISIT_COUNT = "visit_count"


@dataclass
class VisualAppearance:
    hair_color: str = "黑色"
    hair_style: str = "短发"
    eye_color: str = "棕色"
    height: str = "中等"
    build: str = "普通"
    skin_tone: str = "正常"
    distinguishing_features: List[str] = field(default_factory=list)
    clothing_style: str = "朴素"
    accessories: List[str] = field(default_factory=list)
    age_appearance: str = "成年"
    
    def get_description(self) -> str:
        features = "、".join(self.distinguishing_features) if self.distinguishing_features else "无明显特征"
        accessories = "、".join(self.accessories) if self.accessories else "无"
        return (
            f"外貌：{self.age_appearance}，{self.height}身材，{self.build}。\n"
            f"发色：{self.hair_color}，{self.hair_style}。\n"
            f"眼睛：{self.eye_color}。\n"
            f"特征：{features}。\n"
            f"着装：{self.clothing_style}风格，佩戴{accessories}。"
        )


@dataclass
class Backstory:
    birthplace: str = "未知"
    childhood: str = "童年经历不详"
    turning_point: str = ""
    current_goal: str = ""
    hidden_secret: str = ""
    relationships: Dict[str, str] = field(default_factory=dict)
    notable_events: List[str] = field(default_factory=list)
    
    def get_summary(self) -> str:
        summary = f"出生于{self.birthplace}。{self.childhood}"
        if self.turning_point:
            summary += f"\n人生转折：{self.turning_point}"
        if self.current_goal:
            summary += f"\n当前目标：{self.current_goal}"
        return summary


@dataclass
class Personality:
    traits: List[PersonalityTrait] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    dreams: List[str] = field(default_factory=list)
    quirks: List[str] = field(default_factory=list)
    speech_patterns: List[str] = field(default_factory=list)
    
    def get_trait_description(self) -> str:
        if not self.traits:
            return "性格普通"
        return "、".join([t.value for t in self.traits])
    
    def generate_dialogue_modifier(self) -> str:
        if PersonalityTrait.CHEERFUL in self.traits:
            return random.choice(["~", "！", "呢~", "呀！"])
        elif PersonalityTrait.GRUMPY in self.traits:
            return random.choice(["...", "哼。", "。", "罢了。"])
        elif PersonalityTrait.MYSTERIOUS in self.traits:
            return random.choice(["...", "呵呵。", "~", "。"])
        elif PersonalityTrait.SHY in self.traits:
            return random.choice(["...", "那个...", "呢...", "。"])
        return "。"


@dataclass
class DialogueCondition:
    condition_type: DialogueConditionType
    value: any
    comparison: str = "equals"
    
    def check(self, context: Dict) -> bool:
        context_value = context.get(self.condition_type.value, 0)
        
        if self.comparison == "equals":
            return context_value == self.value
        elif self.comparison == "greater":
            return context_value > self.value
        elif self.comparison == "less":
            return context_value < self.value
        elif self.comparison == "contains":
            return self.value in context_value
        elif self.comparison == "in_list":
            return context_value in self.value
        
        return False


@dataclass
class DialogueChoice:
    text: str
    next_node_id: str
    conditions: List[DialogueCondition] = field(default_factory=list)
    effects: Dict[str, any] = field(default_factory=dict)
    required_items: Dict[str, int] = field(default_factory=dict)
    friendship_change: int = 0
    reputation_change: int = 0
    is_hidden: bool = False
    
    def is_available(self, context: Dict) -> bool:
        for condition in self.conditions:
            if not condition.check(context):
                return False
        
        for item_id, count in self.required_items.items():
            if context.get("inventory", {}).get(item_id, 0) < count:
                return False
        
        return True


@dataclass
class DialogueNode:
    node_id: str
    text: str
    speaker_emotion: str = "normal"
    choices: List[DialogueChoice] = field(default_factory=list)
    is_end: bool = False
    on_enter_effects: Dict[str, any] = field(default_factory=dict)
    next_node_id: str = ""
    
    def get_available_choices(self, context: Dict) -> List[DialogueChoice]:
        return [c for c in self.choices if c.is_available(context)]


@dataclass
class DialogueTree:
    tree_id: str
    name: str
    description: str = ""
    nodes: Dict[str, DialogueNode] = field(default_factory=dict)
    start_node_id: str = ""
    repeatable: bool = True
    cooldown_days: int = 0
    last_triggered_day: int = -999
    
    def get_start_node(self) -> Optional[DialogueNode]:
        return self.nodes.get(self.start_node_id)
    
    def get_node(self, node_id: str) -> Optional[DialogueNode]:
        return self.nodes.get(node_id)
    
    def can_trigger(self, current_day: int) -> bool:
        if not self.repeatable:
            return self.last_triggered_day < 0
        if self.cooldown_days > 0:
            return current_day - self.last_triggered_day >= self.cooldown_days
        return True


@dataclass
class ShopItem:
    item_id: str
    name: str
    price: int
    stock: int = -1
    restock_days: int = 7
    discount: float = 0.0
    required_friendship: int = 0
    required_reputation: int = 0
    description: str = ""
    icon: str = "📦"
    
    def get_final_price(self, friendship: int) -> int:
        discount = self.discount
        if friendship >= 500:
            discount += 0.1
        elif friendship >= 300:
            discount += 0.05
        
        return int(self.price * (1 - discount))


@dataclass
class ShopInventory:
    items: List[ShopItem] = field(default_factory=list)
    buy_multiplier: float = 1.0
    sell_multiplier: float = 0.5
    special_items: List[ShopItem] = field(default_factory=list)
    
    def get_available_items(self, friendship: int, reputation: int) -> List[ShopItem]:
        return [
            item for item in self.items
            if item.required_friendship <= friendship
            and item.required_reputation <= reputation
            and item.stock != 0
        ]
    
    def get_buy_price(self, item: ShopItem, friendship: int) -> int:
        return item.get_final_price(friendship)
    
    def get_sell_price(self, base_price: int, friendship: int) -> int:
        bonus = 0
        if friendship >= 500:
            bonus = 0.2
        elif friendship >= 300:
            bonus = 0.1
        return int(base_price * self.sell_multiplier * (1 + bonus))


@dataclass
class EnhancedCharacterProfile:
    character_id: str
    name: str
    archetype: NPCArchetype
    emoji: str
    
    appearance: VisualAppearance = field(default_factory=VisualAppearance)
    personality: Personality = field(default_factory=Personality)
    backstory: Backstory = field(default_factory=Backstory)
    
    friendship: int = 0
    max_friendship: int = 1000
    reputation_with_player: int = 0
    
    dialogue_trees: Dict[str, DialogueTree] = field(default_factory=dict)
    default_dialogues: Dict[str, List[str]] = field(default_factory=dict)
    
    shop_inventory: Optional[ShopInventory] = None
    services: List[str] = field(default_factory=list)
    
    schedule: Dict[str, str] = field(default_factory=dict)
    current_location: str = "家"
    
    quests_available: List[str] = field(default_factory=list)
    quests_given: List[str] = field(default_factory=list)
    
    talked_today: bool = False
    gifted_today: bool = False
    visited_today: bool = False
    visit_count: int = 0
    
    birthday: Tuple[int, int] = (1, 1)
    special_dates: Dict[Tuple[int, int], str] = field(default_factory=dict)
    
    loved_gifts: List[str] = field(default_factory=list)
    liked_gifts: List[str] = field(default_factory=list)
    neutral_gifts: List[str] = field(default_factory=list)
    hated_gifts: List[str] = field(default_factory=list)
    
    unlock_conditions: Dict[str, any] = field(default_factory=dict)
    is_unlocked: bool = True
    is_hidden: bool = False
    
    voice_lines: Dict[str, str] = field(default_factory=dict)
    
    @property
    def friendship_level(self) -> str:
        percentage = self.friendship / self.max_friendship
        if percentage >= 0.9:
            return "挚友"
        elif percentage >= 0.7:
            return "好朋友"
        elif percentage >= 0.5:
            return "朋友"
        elif percentage >= 0.3:
            return "点头之交"
        elif percentage >= 0.1:
            return "认识"
        return "陌生人"
    
    @property
    def reputation_level(self) -> str:
        if self.reputation_with_player >= 500:
            return "崇敬"
        elif self.reputation_with_player >= 300:
            return "尊敬"
        elif self.reputation_with_player >= 100:
            return "友好"
        elif self.reputation_with_player >= 0:
            return "中立"
        elif self.reputation_with_player >= -100:
            return "冷淡"
        else:
            return "敌对"
    
    def add_friendship(self, amount: int) -> Tuple[bool, str]:
        old_level = self.friendship_level
        self.friendship = max(0, min(self.max_friendship, self.friendship + amount))
        new_level = self.friendship_level
        
        if new_level != old_level:
            return True, f"与{self.name}的关系提升到了【{new_level}】！"
        return False, ""
    
    def add_reputation(self, amount: int) -> Tuple[bool, str]:
        old_level = self.reputation_level
        self.reputation_with_player += amount
        new_level = self.reputation_level
        
        if new_level != old_level:
            return True, f"你在{self.name}心中的声望变为【{new_level}】！"
        return False, ""
    
    def get_dialogue(self, dialogue_type: str, context: Dict) -> str:
        if dialogue_type in self.dialogue_trees:
            tree = self.dialogue_trees[dialogue_type]
            if tree.can_trigger(context.get("current_day", 0)):
                return tree.get_start_node().text if tree.get_start_node() else ""
        
        dialogues = self.default_dialogues.get(dialogue_type, [])
        if dialogues:
            dialogue = random.choice(dialogues)
            modifier = self.personality.generate_dialogue_modifier()
            return dialogue + modifier
        
        return "..."
    
    def get_location(self, time_of_day: str) -> str:
        return self.schedule.get(time_of_day, self.current_location)
    
    def new_day(self):
        self.talked_today = False
        self.gifted_today = False
        self.visited_today = False
    
    def get_full_description(self) -> str:
        return (
            f"【{self.name}】\n"
            f"身份：{self.archetype.value}\n"
            f"关系：{self.friendship_level} ({self.friendship}/{self.max_friendship})\n"
            f"声望：{self.reputation_level}\n"
            f"\n{self.appearance.get_description()}\n"
            f"\n性格：{self.personality.get_trait_description()}\n"
            f"\n背景：{self.backstory.get_summary()}"
        )


class CharacterRegistry:
    
    @staticmethod
    def create_blacksmith() -> EnhancedCharacterProfile:
        return EnhancedCharacterProfile(
            character_id="blacksmith_iron",
            name="铁大山",
            archetype=NPCArchetype.BLACKSMITH,
            emoji="⚒️",
            appearance=VisualAppearance(
                hair_color="黑色",
                hair_style="寸头",
                eye_color="棕色",
                height="高大",
                build="肌肉发达",
                distinguishing_features=["手臂上有烧伤痕迹", "浓眉大眼"],
                clothing_style="工装",
                accessories=["皮围裙", "护目镜"],
                age_appearance="中年"
            ),
            personality=Personality(
                traits=[PersonalityTrait.STERN, PersonalityTrait.BRAVE, PersonalityTrait.LOYAL],
                values=["工匠精神", "诚实", "坚韧"],
                fears=["打造出劣质武器", "村子被袭击"],
                dreams=["打造出传说级武器", "收个好徒弟"],
                quirks=["说话声音很大", "喜欢敲打东西思考"],
                speech_patterns=["哼！", "听好了！", "这可是上好的货！"]
            ),
            backstory=Backstory(
                birthplace="铁匠世家",
                childhood="从小跟随父亲学习打铁，展现出惊人的天赋",
                turning_point="在一次怪物袭击中，他打造的武器保护了整个村庄",
                current_goal="打造出能传承百年的神兵利器",
                hidden_secret="其实他年轻时曾是冒险者",
                relationships={"村长": "老友", "守卫队长": "战友"}
            ),
            default_dialogues={
                "greeting": ["欢迎来到铁山铁匠铺！", "要看看我的作品吗？", "有什么需要打造的？"],
                "farewell": ["下次再来！", "武器要好好保养！", "路上小心！"],
                "shop": ["这些都是我精心打造的！", "买把好武器保命要紧！", "质量保证！"],
                "high_friendship": ["你是我见过最有眼光的顾客！", "这把武器就当礼物送你吧！", "有什么困难尽管来找我！"],
                "low_friendship": ["新来的？看看有什么需要的。", "别乱碰东西。", "买就买，不买别挡道。"]
            },
            shop_inventory=ShopInventory(
                items=[
                    ShopItem("iron_sword", "铁剑", 500, icon="⚔️", description="基础铁剑"),
                    ShopItem("steel_sword", "钢剑", 1200, icon="🗡️", description="优质钢剑", required_friendship=100),
                    ShopItem("iron_shield", "铁盾", 400, icon="🛡️", description="基础铁盾"),
                    ShopItem("pickaxe", "矿镐", 200, icon="⛏️", description="采矿工具"),
                    ShopItem("axe", "斧头", 150, icon="🪓", description="砍伐工具"),
                    ShopItem("hammer", "铁锤", 100, icon="🔨", description="建筑工具"),
                ],
                buy_multiplier=1.0,
                sell_multiplier=0.4
            ),
            services=["修理装备", "强化武器", "打造定制装备"],
            schedule={
                "morning": "铁匠铺",
                "afternoon": "铁匠铺",
                "evening": "酒馆",
                "night": "家"
            },
            loved_gifts=["铁矿石", "金矿石", "稀有金属"],
            liked_gifts=["煤炭", "木材", "酒"],
            neutral_gifts=["食物", "布料"],
            hated_gifts=["花朵", "化妆品"]
        )
    
    @staticmethod
    def create_merchant() -> EnhancedCharacterProfile:
        return EnhancedCharacterProfile(
            character_id="merchant_golden",
            name="金万两",
            archetype=NPCArchetype.MERCHANT,
            emoji="💰",
            appearance=VisualAppearance(
                hair_color="黑色",
                hair_style="梳得整齐",
                eye_color="黑色",
                height="中等",
                build="微胖",
                distinguishing_features=["总是带着微笑", "手指上有多个戒指"],
                clothing_style="华丽",
                accessories=["金链子", "玉佩", "算盘"],
                age_appearance="中年"
            ),
            personality=Personality(
                traits=[PersonalityTrait.FRIENDLY, PersonalityTrait.AMBITIOUS, PersonalityTrait.MISCHIEVOUS],
                values=["利润", "信誉", "人脉"],
                fears=["亏本", "货物被抢"],
                dreams=["成为大陆首富", "建立商业帝国"],
                quirks=["说话时喜欢摸胡子", "总是随身带着算盘"],
                speech_patterns=["客官~", "这个价格已经很优惠了！", "买卖不成仁义在~"]
            ),
            backstory=Backstory(
                birthplace="商业都市",
                childhood="出身贫寒，从小在街头叫卖",
                turning_point="一次偶然的机会救了一位大商人，被收为徒弟",
                current_goal="把生意做到大陆每个角落",
                hidden_secret="其实他在暗中资助孤儿院",
                relationships={"流浪商人": "竞争对手兼朋友"}
            ),
            default_dialogues={
                "greeting": ["欢迎光临金氏商行！", "客官想看点什么？", "今天有新货到哦~"],
                "farewell": ["慢走~欢迎下次再来！", "记得常来捧场！", "祝您生意兴隆！"],
                "shop": ["这个可是稀罕货！", "给您打个折~", "包您满意！"],
                "high_friendship": ["老朋友来了！今天有特价！", "这可是我特意为您留的！", "咱们之间不用客气！"],
                "low_friendship": ["看看有什么喜欢的？", "都是好货，童叟无欺。", "价格好商量~"]
            },
            shop_inventory=ShopInventory(
                items=[
                    ShopItem("basic_seed_pack", "基础种子包", 50, icon="🌱", description="各种基础种子"),
                    ShopItem("premium_seed_pack", "高级种子包", 200, icon="🌿", description="稀有种子", required_friendship=100),
                    ShopItem("fertilizer", "肥料", 30, icon="🧪", description="促进作物生长"),
                    ShopItem("watering_can", "浇水壶", 100, icon="🚿", description="浇水工具"),
                    ShopItem("backpack_small", "小背包", 300, icon="🎒", description="增加背包容量"),
                    ShopItem("mystery_box", "神秘盒子", 100, icon="🎁", description="随机开出物品"),
                ],
                buy_multiplier=1.0,
                sell_multiplier=0.6
            ),
            services=["鉴定物品", "寄售物品", "情报交易"],
            schedule={
                "morning": "商店",
                "afternoon": "市场",
                "evening": "商店",
                "night": "家"
            },
            loved_gifts=["金币", "宝石", "古董"],
            liked_gifts=["稀有物品", "特产", "情报"],
            neutral_gifts=["食物", "日用品"],
            hated_gifts=["垃圾", "损坏物品"]
        )
    
    @staticmethod
    def create_healer() -> EnhancedCharacterProfile:
        return EnhancedCharacterProfile(
            character_id="healer_lotus",
            name="荷花仙子",
            archetype=NPCArchetype.HEALER,
            emoji="🌸",
            appearance=VisualAppearance(
                hair_color="淡粉色",
                hair_style="长发及腰",
                eye_color="绿色",
                height="中等",
                build="纤细",
                distinguishing_features=["气质出尘", "身上有淡淡花香"],
                clothing_style="飘逸长裙",
                accessories=["花环", "玉笛"],
                age_appearance="年轻"
            ),
            personality=Personality(
                traits=[PersonalityTrait.GENTLE, PersonalityTrait.WISE, PersonalityTrait.SHY],
                values=["生命", "自然", "和平"],
                fears=["无法救活病人", "战争"],
                dreams=["找到治愈所有疾病的方法", "建立一座大医院"],
                quirks=["说话轻声细语", "喜欢哼小曲"],
                speech_patterns=["请保重身体~", "让奴家看看...", "愿自然之力庇佑你"]
            ),
            backstory=Backstory(
                birthplace="神秘的花谷",
                childhood="被一位隐居的神医收养，学习医术",
                turning_point="师父去世后，她决定走出山谷救治更多人",
                current_goal="用医术帮助更多的人",
                hidden_secret="她其实是花仙子的后裔",
                relationships={}
            ),
            default_dialogues={
                "greeting": ["欢迎来到药庐~", "身体不舒服吗？", "需要什么药材？"],
                "farewell": ["保重身体~", "有需要随时来找我", "愿您健康平安"],
                "shop": ["这些都是上好的药材~", "按方抓药，效果更好", "这个对您的症状有帮助"],
                "high_friendship": ["您能来我真高兴~", "这些药材送您吧", "让我为您检查一下身体"],
                "low_friendship": ["请问有什么需要？", "请描述您的症状", "我会尽力帮助您"]
            },
            shop_inventory=ShopInventory(
                items=[
                    ShopItem("health_potion_small", "小型生命药水", 50, icon="❤️", description="恢复50生命值"),
                    ShopItem("health_potion_large", "大型生命药水", 150, icon="💖", description="恢复200生命值"),
                    ShopItem("antidote", "解毒剂", 80, icon="💊", description="解除中毒状态"),
                    ShopItem("bandage", "绷带", 20, icon="🩹", description="止血包扎"),
                    ShopItem("herb_pack", "草药包", 100, icon="🌿", description="各种治疗草药"),
                    ShopItem("revival_pill", "复活丹", 500, icon="✨", description="濒死时保命", required_friendship=200),
                ],
                buy_multiplier=1.0,
                sell_multiplier=0.5
            ),
            services=["治疗", "解毒", "制作药剂", "体检"],
            schedule={
                "morning": "药庐",
                "afternoon": "采药",
                "evening": "药庐",
                "night": "家"
            },
            loved_gifts=["稀有草药", "花蜜", "纯净之水"],
            liked_gifts=["普通草药", "花朵", "水果"],
            neutral_gifts=["食物", "日用品"],
            hated_gifts=["武器", "毒药"]
        )
    
    @staticmethod
    def create_quest_giver() -> EnhancedCharacterProfile:
        return EnhancedCharacterProfile(
            character_id="elder_wisdom",
            name="智长老",
            archetype=NPCArchetype.QUEST_GIVER,
            emoji="📜",
            appearance=VisualAppearance(
                hair_color="白色",
                hair_style="长须长发",
                eye_color="灰色",
                height="中等",
                build="瘦削",
                distinguishing_features=["满脸皱纹但精神矍铄", "手持拐杖"],
                clothing_style="古朴长袍",
                accessories=["老花镜", "古书", "拐杖"],
                age_appearance="老年"
            ),
            personality=Personality(
                traits=[PersonalityTrait.WISE, PersonalityTrait.GENTLE, PersonalityTrait.MYSTERIOUS],
                values=["知识", "传承", "正义"],
                fears=["知识失传", "村子衰败"],
                dreams=["建立一座大图书馆", "培养出优秀的继承人"],
                quirks=["说话喜欢引经据典", "经常陷入沉思"],
                speech_patterns=["古人云...", "且听老夫一言...", "此事说来话长..."]
            ),
            backstory=Backstory(
                birthplace="本村",
                childhood="年轻时是著名的学者，游历四方",
                turning_point="发现村子面临危机，决定回来守护",
                current_goal="找到能拯救村子的人",
                hidden_secret="他知道村子的惊天秘密",
                relationships={"村长": "老友", "学者": "师徒"}
            ),
            default_dialogues={
                "greeting": ["年轻人，你来了。", "老夫等你很久了。", "有要事相商。"],
                "farewell": ["去吧，愿智慧指引你。", "记住老夫的话。", "期待你的好消息。"],
                "quest": ["这件事关系重大...", "老夫需要你的帮助。", "只有你能完成这个任务。"],
                "high_friendship": ["你就像我的孙子一样。", "村子有你是福分。", "这些秘密只告诉你。"],
                "low_friendship": ["年轻人，有何贵干？", "老夫很忙。", "说吧，什么事？"]
            },
            services=["发布任务", "传授知识", "解读古籍"],
            schedule={
                "morning": "书房",
                "afternoon": "村委会",
                "evening": "广场",
                "night": "家"
            },
            loved_gifts=["古籍", "文物", "稀有知识"],
            liked_gifts=["书籍", "茶叶", "棋具"],
            neutral_gifts=["食物", "日用品"],
            hated_gifts=["噪音物品", "俗气的东西"]
        )
    
    @staticmethod
    def create_innkeeper() -> EnhancedCharacterProfile:
        return EnhancedCharacterProfile(
            character_id="innkeeper_rosy",
            name="玫瑰阿姨",
            archetype=NPCArchetype.INNKEEPER,
            emoji="🏠",
            appearance=VisualAppearance(
                hair_color="棕色",
                hair_style="盘发",
                eye_color="棕色",
                height="中等",
                build="丰满",
                distinguishing_features=["总是笑眯眯的", "围裙上有花边"],
                clothing_style="朴素大方",
                accessories=["围裙", "发簪"],
                age_appearance="中年"
            ),
            personality=Personality(
                traits=[PersonalityTrait.CHEERFUL, PersonalityTrait.FRIENDLY, PersonalityTrait.GENTLE],
                values=["家庭", "美食", "温暖"],
                fears=["客人不满意", "旅馆倒闭"],
                dreams=["做出最美味的菜肴", "看客人满意的样子"],
                quirks=["喜欢给客人塞吃的", "说话很热情"],
                speech_patterns=["哎呀~", "来来来~", "阿姨给你做点好吃的~"]
            ),
            backstory=Backstory(
                birthplace="附近村庄",
                childhood="从小跟母亲学做菜，厨艺精湛",
                turning_point="嫁到这个村子，开了这家旅馆",
                current_goal="让每个客人都有回家的感觉",
                hidden_secret="她其实是个隐藏的美食家",
                relationships={}
            ),
            default_dialogues={
                "greeting": ["哎呀，来啦！", "快进来坐！", "今天想吃点什么？"],
                "farewell": ["下次再来啊！", "路上小心！", "记得常来！"],
                "shop": ["这是阿姨的拿手菜！", "保证让你满意！", "多吃点，看你瘦的~"],
                "high_friendship": ["孩子，阿姨给你留了好吃的！", "来，这个不收你钱！", "有什么烦心事跟阿姨说~"],
                "low_friendship": ["欢迎光临！", "看看菜单吧。", "需要住宿吗？"]
            },
            shop_inventory=ShopInventory(
                items=[
                    ShopItem("bread", "面包", 10, icon="🍞", description="新鲜面包"),
                    ShopItem("soup", "热汤", 20, icon="🍲", description="暖胃热汤"),
                    ShopItem("meat_stew", "炖肉", 50, icon="🍖", description="美味炖肉"),
                    ShopItem("fruit_salad", "水果沙拉", 30, icon="🥗", description="清爽沙拉"),
                    ShopItem("special_dish", "招牌菜", 100, icon="🍽️", description="今日特餐", required_friendship=100),
                    ShopItem("room_night", "住宿一晚", 80, icon="🛏️", description="恢复体力"),
                ],
                buy_multiplier=1.0,
                sell_multiplier=0.3
            ),
            services=["住宿", "餐饮", "情报收集"],
            schedule={
                "morning": "旅馆厨房",
                "afternoon": "旅馆大厅",
                "evening": "旅馆大厅",
                "night": "旅馆"
            },
            loved_gifts=["新鲜食材", "香料", "厨具"],
            liked_gifts=["蔬菜", "水果", "酒"],
            neutral_gifts=["日用品"],
            hated_gifts=["垃圾", "坏掉的食材"]
        )
    
    @staticmethod
    def create_beast_tamer() -> EnhancedCharacterProfile:
        return EnhancedCharacterProfile(
            character_id="tamer_wild",
            name="野风",
            archetype=NPCArchetype.BEAST_TAMER,
            emoji="🦊",
            appearance=VisualAppearance(
                hair_color="棕色",
                hair_style="凌乱短发",
                eye_color="琥珀色",
                height="中等偏高",
                build="结实",
                distinguishing_features=["身上有动物抓痕", "眼神锐利"],
                clothing_style="皮毛装饰",
                accessories=["动物牙项链", "驯兽鞭"],
                age_appearance="青年"
            ),
            personality=Personality(
                traits=[PersonalityTrait.BRAVE, PersonalityTrait.MYSTERIOUS, PersonalityTrait.LOYAL],
                values=["自由", "自然", "动物"],
                fears=["动物被伤害", "失去自由"],
                dreams=["与所有动物沟通", "找到传说中的神兽"],
                quirks=["说话简短", "经常与动物交流"],
                speech_patterns=["...", "动物不会撒谎。", "跟着感觉走。"]
            ),
            backstory=Backstory(
                birthplace="森林深处",
                childhood="被狼群抚养长大，后被人发现带回村庄",
                turning_point="发现自己能与动物心灵相通",
                current_goal="保护森林中的动物",
                hidden_secret="他能听懂所有动物的语言",
                relationships={}
            ),
            default_dialogues={
                "greeting": ["...", "你来了。", "动物们说你来了。"],
                "farewell": ["保重。", "动物们会保护你。", "下次再来。"],
                "shop": ["这些伙伴想跟你走。", "好好照顾它们。", "它们选择了你。"],
                "high_friendship": ["你...与众不同。", "动物们信任你。", "我可以教你与动物沟通。"],
                "low_friendship": ["...", "有什么事？", "动物们不喜欢你。"]
            },
            shop_inventory=ShopInventory(
                items=[
                    ShopItem("pet_food", "宠物粮", 30, icon="🍖", description="宠物食物"),
                    ShopItem("pet_toy", "宠物玩具", 50, icon="🎾", description="增加宠物快乐度"),
                    ShopItem("pet_bed", "宠物窝", 100, icon="🛏️", description="宠物休息处"),
                    ShopItem("treats", "宠物零食", 20, icon="🦴", description="训练用零食"),
                    ShopItem("pet_medicine", "宠物药", 80, icon="💊", description="治疗宠物"),
                    ShopItem("rare_pet_egg", "稀有宠物蛋", 500, icon="🥚", description="孵化稀有宠物", required_friendship=300),
                ],
                buy_multiplier=1.0,
                sell_multiplier=0.4
            ),
            services=["驯服宠物", "宠物训练", "宠物治疗"],
            schedule={
                "morning": "森林",
                "afternoon": "牧场",
                "evening": "森林边缘",
                "night": "森林"
            },
            loved_gifts=["稀有宠物", "野生动物喜欢的食物", "自然之物"],
            liked_gifts=["宠物用品", "肉类", "皮革"],
            neutral_gifts=["普通食物"],
            hated_gifts=["动物制品", "武器"]
        )


class EnhancedCharacterManager:
    
    def __init__(self):
        self.characters: Dict[str, EnhancedCharacterProfile] = {}
        self.active_dialogues: Dict[str, str] = {}
        self._init_characters()
    
    def _init_characters(self):
        characters = [
            CharacterRegistry.create_blacksmith(),
            CharacterRegistry.create_merchant(),
            CharacterRegistry.create_healer(),
            CharacterRegistry.create_quest_giver(),
            CharacterRegistry.create_innkeeper(),
            CharacterRegistry.create_beast_tamer(),
        ]
        
        for char in characters:
            self.characters[char.character_id] = char
    
    def get_character(self, character_id: str) -> Optional[EnhancedCharacterProfile]:
        return self.characters.get(character_id)
    
    def get_all_characters(self) -> List[EnhCharacterProfile]:
        return list(self.characters.values())
    
    def get_characters_by_archetype(self, archetype: NPCArchetype) -> List[EnhancedCharacterProfile]:
        return [c for c in self.characters.values() if c.archetype == archetype]
    
    def get_characters_at_location(self, location: str, time_of_day: str) -> List[EnhancedCharacterProfile]:
        return [
            c for c in self.characters.values()
            if c.get_location(time_of_day) == location and c.is_unlocked
        ]
    
    def start_dialogue(self, character_id: str, dialogue_type: str, context: Dict) -> Tuple[bool, str, Optional[DialogueNode]]:
        character = self.get_character(character_id)
        if not character:
            return False, "找不到这个人", None
        
        if dialogue_type in character.dialogue_trees:
            tree = character.dialogue_trees[dialogue_type]
            if tree.can_trigger(context.get("current_day", 0)):
                start_node = tree.get_start_node()
                if start_node:
                    self.active_dialogues[character_id] = dialogue_type
                    return True, start_node.text, start_node
        
        dialogue = character.get_dialogue(dialogue_type, context)
        return True, dialogue, None
    
    def continue_dialogue(self, character_id: str, choice_index: int, context: Dict) -> Tuple[bool, str, Optional[DialogueNode], Dict]:
        character = self.get_character(character_id)
        if not character:
            return False, "找不到这个人", None, {}
        
        dialogue_type = self.active_dialogues.get(character_id)
        if not dialogue_type or dialogue_type not in character.dialogue_trees:
            return False, "没有进行中的对话", None, {}
        
        tree = character.dialogue_trees[dialogue_type]
        
        return False, "对话已结束", None, {}
    
    def end_dialogue(self, character_id: str) -> bool:
        if character_id in self.active_dialogues:
            del self.active_dialogues[character_id]
            return True
        return False
    
    def give_gift(self, character_id: str, gift_name: str, context: Dict) -> Tuple[bool, int, str]:
        character = self.get_character(character_id)
        if not character:
            return False, 0, "找不到这个人"
        
        if character.gifted_today:
            return False, 0, "今天已经送过礼物了"
        
        character.gifted_today = True
        points = 0
        reaction = ""
        
        if gift_name in character.loved_gifts:
            points = 80
            reaction = f"哇！这是我最喜欢的东西！太感谢你了！"
        elif gift_name in character.liked_gifts:
            points = 40
            reaction = f"这个我很喜欢，谢谢你！"
        elif gift_name in character.hated_gifts:
            points = -20
            reaction = f"呃...这个我不太喜欢..."
        else:
            points = 10
            reaction = f"谢谢你的礼物。"
        
        character.add_friendship(points)
        return True, points, reaction
    
    def buy_item(self, character_id: str, item_id: str, context: Dict) -> Tuple[bool, int, str]:
        character = self.get_character(character_id)
        if not character or not character.shop_inventory:
            return False, 0, "无法购买"
        
        item = None
        for shop_item in character.shop_inventory.items:
            if shop_item.item_id == item_id:
                item = shop_item
                break
        
        if not item:
            return False, 0, "没有这个商品"
        
        if item.required_friendship > character.friendship:
            return False, 0, "好感度不足"
        
        final_price = character.shop_inventory.get_buy_price(item, character.friendship)
        
        return True, final_price, f"购买{item.name}需要{final_price}金币"
    
    def sell_item(self, character_id: str, item_name: str, base_price: int) -> Tuple[bool, int, str]:
        character = self.get_character(character_id)
        if not character or not character.shop_inventory:
            return False, 0, "无法出售"
        
        final_price = character.shop_inventory.get_sell_price(base_price, character.friendship)
        return True, final_price, f"出售{item_name}可获得{final_price}金币"
    
    def new_day(self):
        for character in self.characters.values():
            character.new_day()
    
    def to_dict(self) -> Dict:
        return {
            char_id: {
                "friendship": char.friendship,
                "reputation": char.reputation_with_player,
                "talked_today": char.talked_today,
                "gifted_today": char.gifted_today,
                "visited_today": char.visited_today,
                "visit_count": char.visit_count,
                "is_unlocked": char.is_unlocked
            }
            for char_id, char in self.characters.items()
        }
    
    def from_dict(self, data: Dict):
        for char_id, char_data in data.items():
            if char_id in self.characters:
                char = self.characters[char_id]
                char.friendship = char_data.get("friendship", 0)
                char.reputation_with_player = char_data.get("reputation", 0)
                char.talked_today = char_data.get("talked_today", False)
                char.gifted_today = char_data.get("gifted_today", False)
                char.visited_today = char_data.get("visited_today", False)
                char.visit_count = char_data.get("visit_count", 0)
                char.is_unlocked = char_data.get("is_unlocked", True)
