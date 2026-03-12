from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(tags=["商店"])

class ShopItem(BaseModel):
    id: str
    name: str
    emoji: str
    category: str
    price: int
    description: str
    effect: Optional[dict] = None

class BuyRequest(BaseModel):
    item_id: str
    quantity: int = 1

shop_items = [
    # ========== 肥料类 ==========
    ShopItem(
        id="fertilizer_basic",
        name="普通肥料",
        emoji="🧪",
        category="fertilizer",
        price=50,
        description="促进作物生长，生长速度+10%。是最基础的肥料，适合新手使用。",
        effect={"growth_bonus": 0.1}
    ),
    ShopItem(
        id="fertilizer_advanced",
        name="高级肥料",
        emoji="⚗️",
        category="fertilizer",
        price=150,
        description="显著促进作物生长，生长速度+25%。含有丰富的营养成分。",
        effect={"growth_bonus": 0.25}
    ),
    ShopItem(
        id="fertilizer_premium",
        name="顶级肥料",
        emoji="🧬",
        category="fertilizer",
        price=500,
        description="卓越的作物生长促进剂，生长速度+50%。含有稀有微量元素。",
        effect={"growth_bonus": 0.5}
    ),
    ShopItem(
        id="fertilizer_magic",
        name="魔法肥料",
        emoji="✨",
        category="fertilizer",
        price=1000,
        description="神奇的魔法肥料，生长速度翻倍！让作物在最短时间内成熟。",
        effect={"growth_bonus": 1.0}
    ),
    
    # ========== 工具类 ==========
    ShopItem(
        id="water_can",
        name="高级水壶",
        emoji="🚿",
        category="tool",
        price=200,
        description="浇水效率提升，一次可以浇更多作物。容量是普通水壶的两倍。",
        effect={"water_capacity": 10}
    ),
    ShopItem(
        id="water_can_pro",
        name="专业水壶",
        emoji="💦",
        category="tool",
        price=500,
        description="专业级浇水工具，一次可以浇灌整个农田。效率提升200%。",
        effect={"water_capacity": 25}
    ),
    ShopItem(
        id="golden_shovel",
        name="黄金铲子",
        emoji="🥄",
        category="tool",
        price=800,
        description="挖掘作物时更加高效，减少对作物根系的损伤。",
        effect={"harvest_bonus": 0.2}
    ),
    ShopItem(
        id="magic_gloves",
        name="神奇手套",
        emoji="🧤",
        category="tool",
        price=600,
        description="保护作物在收获时不受损伤，提升作物品质。",
        effect={"quality_bonus": 0.15}
    ),
    ShopItem(
        id="compass",
        name="农用指南针",
        emoji="🧭",
        category="tool",
        price=300,
        description="帮助你找到最适合当前季节种植的作物。",
        effect={"season_advice": True}
    ),
    ShopItem(
        id="magnifying_glass",
        name="观察放大镜",
        emoji="🔍",
        category="tool",
        price=400,
        description="更清楚地观察作物生长状态，不错过最佳收获时机。",
        effect={"growth_detail": True}
    ),
    
    # ========== 装饰类 ==========
    ShopItem(
        id="scarecrow",
        name="稻草人",
        emoji="🎃",
        category="decoration",
        price=300,
        description="保护农田不受乌鸦侵扰，是农场的守护者。",
        effect={"protect_birds": True}
    ),
    ShopItem(
        id="garden_gnome",
        name="花园精灵",
        emoji="🧙",
        category="decoration",
        price=500,
        description="传说中能带来好运的精灵，提升作物稀有掉落率。",
        effect={"luck_bonus": 0.1}
    ),
    ShopItem(
        id="wind_chime",
        name="风铃",
        emoji="🔔",
        category="decoration",
        price=450,
        description="清脆的风铃声让农场更加和谐，提升作物心情。",
        effect={"mood_bonus": 0.1}
    ),
    ShopItem(
        id="solar_lamp",
        name="太阳能灯",
        emoji="💡",
        category="decoration",
        price=600,
        description="白天收集阳光，夜晚照亮农田。提升夜间工作安全性。",
        effect={"night_visible": True}
    ),
    ShopItem(
        id="birdbath",
        name="鸟浴盆",
        emoji="🛁",
        category="decoration",
        price=350,
        description="吸引益鸟前来，帮助消灭害虫，保护作物健康生长。",
        effect={"pest_control": 0.2}
    ),
    
    # ========== 建筑类 ==========
    ShopItem(
        id="greenhouse",
        name="温室大棚",
        emoji="🏡",
        category="building",
        price=2000,
        description="保护作物不受恶劣天气影响，全年都可以种植任何作物。",
        effect={"weather_protection": True, "all_season_plant": True}
    ),
    ShopItem(
        id="chicken_coop",
        name="鸡舍",
        emoji="🐔",
        category="building",
        price=1500,
        description="每天自动产出鸡蛋，是稳定的副业收入来源。",
        effect={"auto_eggs": True}
    ),
    ShopItem(
        id="cow_barn",
        name="牛棚",
        emoji="🐄",
        category="building",
        price=3000,
        description="每天自动产出牛奶，高价值的副产品。",
        effect={"auto_milk": True}
    ),
    ShopItem(
        id="sheep_pen",
        name="羊圈",
        emoji="🐑",
        category="building",
        price=3500,
        description="养殖绵羊，收获羊毛和羊肉。羊毛是纺织品的原料。",
        effect={"auto_wool": True}
    ),
    ShopItem(
        id="pig_sty",
        name="猪圈",
        emoji="🐖",
        category="building",
        price=4000,
        description="养殖猪只，猪肉是重要的食材。粪便还可以作为肥料。",
        effect={"auto_pork": True, "fertilizer_production": 0.2}
    ),
    ShopItem(
        id="horse_stable",
        name="马厩",
        emoji="🐴",
        category="building",
        price=5000,
        description="养殖马匹，可以用于快速旅行。农场身份的象征。",
        effect={"travel_speed": 0.5, "status_bonus": True}
    ),
    ShopItem(
        id="bee_hive",
        name="蜂箱",
        emoji="🐝",
        category="building",
        price=2500,
        description="蜜蜂传授花粉，提升附近作物的产量和品质。",
        effect={"pollination": 0.3, "honey_production": True}
    ),
    ShopItem(
        id="fish_pond",
        name="鱼塘",
        emoji="🐟",
        category="building",
        price=4500,
        description="养殖各种鱼类，是稳定的水产收入来源。",
        effect={"fish_farming": True, "water_income": True}
    ),
    ShopItem(
        id="tool_shed",
        name="工具房",
        emoji="🏚️",
        category="building",
        price=1800,
        description="存放工具，提升工具耐久度使用效率。",
        effect={"tool_durability": 0.5}
    ),
    ShopItem(
        id="root_cellar",
        name="地下储藏室",
        emoji="🍄",
        category="building",
        price=2200,
        description="延长作物保鲜期，减少储存损失。",
        effect={"storage_bonus": 0.4}
    ),
    
    # ========== 种子类 - 蔬菜 ==========
    ShopItem(
        id="seed_radish",
        name="萝卜种子",
        emoji="🥕",
        category="seed",
        price=20,
        description="生长快速，适合新手。只需2天即可收获。",
        effect={"crop": "radish", "grow_days": 2}
    ),
    ShopItem(
        id="seed_lettuce",
        name="生菜种子",
        emoji="🥬",
        category="seed",
        price=25,
        description="生长快速的绿叶蔬菜，2天即可收获。适合快速周转。",
        effect={"crop": "lettuce", "grow_days": 2}
    ),
    ShopItem(
        id="seed_cabbage",
        name="白菜种子",
        emoji="🥬",
        category="seed",
        price=30,
        description="适应性强的常见蔬菜，三季可种。",
        effect={"crop": "cabbage", "grow_days": 3}
    ),
    ShopItem(
        id="seed_potato",
        name="土豆种子",
        emoji="🥔",
        category="seed",
        price=50,
        description="基础农作物，生长周期3天，新手首选。",
        effect={"crop": "potato", "grow_days": 3}
    ),
    ShopItem(
        id="seed_carrot",
        name="胡萝卜种子",
        emoji="🥕",
        category="seed",
        price=40,
        description="生长最快的作物之一，2天即可收获。",
        effect={"crop": "carrot", "grow_days": 2}
    ),
    ShopItem(
        id="seed_cucumber",
        name="黄瓜种子",
        emoji="🥒",
        category="seed",
        price=60,
        description="夏季清凉蔬菜，4天生长周期。",
        effect={"crop": "cucumber", "grow_days": 4}
    ),
    ShopItem(
        id="seed_tomato",
        name="番茄种子",
        emoji="🍅",
        category="seed",
        price=80,
        description="高收益作物，5天生长周期。夏季特産。",
        effect={"crop": "tomato", "grow_days": 5}
    ),
    ShopItem(
        id="seed_corn",
        name="玉米种子",
        emoji="🌽",
        category="seed",
        price=100,
        description="中等收益作物，6天生长周期。",
        effect={"crop": "corn", "grow_days": 6}
    ),
    ShopItem(
        id="seed_eggplant",
        name="茄子种子",
        emoji="🍆",
        category="seed",
        price=70,
        description="秋季蔬菜，4天生长周期。性价比不错。",
        effect={"crop": "eggplant", "grow_days": 4}
    ),
    ShopItem(
        id="seed_pepper",
        name="青椒种子",
        emoji="🫑",
        category="seed",
        price=80,
        description="维生素C含量高，5天生长周期。",
        effect={"crop": "pepper", "grow_days": 5}
    ),
    
    # ========== 种子类 - 水果 ==========
    ShopItem(
        id="seed_watermelon",
        name="西瓜种子",
        emoji="🍉",
        category="seed",
        price=150,
        description="夏季高价值水果，8天生长周期。",
        effect={"crop": "watermelon", "grow_days": 8}
    ),
    ShopItem(
        id="seed_strawberry",
        name="草莓种子",
        emoji="🍓",
        category="seed",
        price=200,
        description="春季珍品，10天生长周期。价格昂贵但收益丰厚。",
        effect={"crop": "strawberry", "grow_days": 10}
    ),
    ShopItem(
        id="seed_grape",
        name="葡萄种子",
        emoji="🍇",
        category="seed",
        price=300,
        description="高价值水果，14天生长周期。收益最高。",
        effect={"crop": "grape", "grow_days": 14}
    ),
    ShopItem(
        id="seed_peach",
        name="桃树苗",
        emoji="🍑",
        category="seed",
        price=180,
        description="夏季甜美水果，12天生长周期。",
        effect={"crop": "peach", "grow_days": 12}
    ),
    ShopItem(
        id="seed_apple",
        name="苹果树苗",
        emoji="🍎",
        category="seed",
        price=200,
        description="世界最受欢迎的水果，15天生长周期。",
        effect={"crop": "apple", "grow_days": 15}
    ),
    ShopItem(
        id="seed_pear",
        name="梨树苗",
        emoji="🍐",
        category="seed",
        price=150,
        description="秋季润燥水果，11天生长周期。",
        effect={"crop": "pear", "grow_days": 11}
    ),
    ShopItem(
        id="seed_blueberry",
        name="蓝莓种子",
        emoji="🫐",
        category="seed",
        price=380,
        description="超级水果之王，14天生长周期。富含花青素。",
        effect={"crop": "blueberry", "grow_days": 14}
    ),
    ShopItem(
        id="seed_cherry",
        name="樱桃树苗",
        emoji="🍒",
        category="seed",
        price=450,
        description="春季高端水果，16天生长周期。传奇级别作物。",
        effect={"crop": "cherry", "grow_days": 16}
    ),
    
    # ========== 种子类 - 花卉 ==========
    ShopItem(
        id="seed_sunflower",
        name="向日葵种子",
        emoji="🌻",
        category="seed",
        price=250,
        description="夏季花卉，12天生长周期。种子可榨油。",
        effect={"crop": "sunflower", "grow_days": 12}
    ),
    ShopItem(
        id="seed_rose",
        name="玫瑰种子",
        emoji="🌹",
        category="seed",
        price=300,
        description="美丽花卉，10天生长周期。高价值，适合送礼。",
        effect={"crop": "rose", "grow_days": 10}
    ),
    ShopItem(
        id="seed_tulip",
        name="郁金香种球",
        emoji="🌷",
        category="seed",
        price=200,
        description="春季球根花卉，8天生长周期。色彩鲜艳。",
        effect={"crop": "tulip", "grow_days": 8}
    ),
    ShopItem(
        id="seed_lavender",
        name="薰衣草种子",
        emoji="💜",
        category="seed",
        price=250,
        description="紫色浪漫花卉，11天生长周期。香气怡人。",
        effect={"crop": "lavender", "grow_days": 11}
    ),
    ShopItem(
        id="seed_chrysanthemum",
        name="菊花种子",
        emoji="🌼",
        category="seed",
        price=180,
        description="秋季名花，9天生长周期。象征高洁。",
        effect={"crop": "chrysanthemum", "grow_days": 9}
    ),
    ShopItem(
        id="seed_orchid",
        name="兰花幼苗",
        emoji="🪻",
        category="seed",
        price=500,
        description="花中君子，18天生长周期。传奇级别作物。",
        effect={"crop": "orchid", "grow_days": 18}
    ),
    
    # ========== 种子类 - 经济作物 ==========
    ShopItem(
        id="seed_wheat",
        name="小麦种子",
        emoji="🌾",
        category="seed",
        price=20,
        description="世界最重要的粮食作物，4天生长周期。适合大规模种植。",
        effect={"crop": "wheat", "grow_days": 4}
    ),
    ShopItem(
        id="seed_rice",
        name="水稻秧苗",
        emoji="🍚",
        category="seed",
        price=35,
        description="重要的粮食作物，5天生长周期。需要充足水分。",
        effect={"crop": "rice", "grow_days": 5}
    ),
    ShopItem(
        id="seed_cotton",
        name="棉花种子",
        emoji="☁️",
        category="seed",
        price=100,
        description="重要经济作物，10天生长周期。纺织原料。",
        effect={"crop": "cotton", "grow_days": 10}
    ),
    ShopItem(
        id="seed_tea",
        name="茶树苗",
        emoji="🍵",
        category="seed",
        price=180,
        description="世界三大饮料之一，20天生长周期。高端经济作物。",
        effect={"crop": "tea", "grow_days": 20}
    ),
    ShopItem(
        id="seed_coffee",
        name="咖啡树苗",
        emoji="☕",
        category="seed",
        price=350,
        description="世界三大饮料之一，25天生长周期。传奇级别作物。",
        effect={"crop": "coffee", "grow_days": 25}
    ),
    ShopItem(
        id="seed_cocoa",
        name="可可树苗",
        emoji="🍫",
        category="seed",
        price=400,
        description="巧克力原料，22天生长周期。传奇级别作物。",
        effect={"crop": "cocoa", "grow_days": 22}
    ),
    ShopItem(
        id="seed_bamboo",
        name="竹子幼苗",
        emoji="🎋",
        category="seed",
        price=80,
        description="四君子之一，30天生长周期。一次种植多年收获。",
        effect={"crop": "bamboo", "grow_days": 30}
    ),
    ShopItem(
        id="seed_mushroom",
        name="蘑菇菌种",
        emoji="🍄",
        category="seed",
        price=120,
        description="营养丰富的菌类，5天生长周期。需要潮湿环境。",
        effect={"crop": "mushroom", "grow_days": 5}
    ),
    
    # ========== 特殊道具 ==========
    ShopItem(
        id="time_capsule",
        name="时光胶囊",
        emoji="⏳",
        category="special",
        price=1000,
        description="可以让时间前进1天，但会消耗大量体力。紧急情况使用。",
        effect={"time_advance": 1}
    ),
    ShopItem(
        id="rain_totem",
        name="求雨图腾",
        emoji="🌧️",
        category="special",
        price=800,
        description="祈求降雨，解决干旱问题。有效期3天。",
        effect={"rain_boost": 3}
    ),
    ShopItem(
        id="sun_totem",
        name="求晴图腾",
        emoji="☀️",
        category="special",
        price=800,
        description="祈求晴天，驱散雨云。有效期3天。",
        effect={"sun_boost": 3}
    ),
    ShopItem(
        id="luck_charm",
        name="幸运护符",
        emoji="🍀",
        category="special",
        price=600,
        description="提升当天的好运概率，增加稀有作物掉落率。",
        effect={"luck_boost": 0.3}
    ),
    ShopItem(
        id="seed_boost",
        name="催芽剂",
        emoji="🌱",
        category="special",
        price=350,
        description="使用后24小时内种植的作物生长速度提升50%。",
        effect={"germination_boost": 0.5}
    ),
    ShopItem(
        id="harvest_blessing",
        name="丰收祝福",
        emoji="🎊",
        category="special",
        price=500,
        description="使用后当天收获的作物价值提升20%。",
        effect={"harvest_value_boost": 0.2}
    ),
    ShopItem(
        id="pest_spray",
        name="除虫药剂",
        emoji="💨",
        category="special",
        price=250,
        description="驱除所有害虫，保护作物健康生长。",
        effect={"pest_removal": True}
    ),
    ShopItem(
        id="weather_shield",
        name="天气护盾",
        emoji="🛡️",
        category="special",
        price=1200,
        description="保护农田免受恶劣天气影响3天。",
        effect={"weather_shield_days": 3}
    ),
    ShopItem(
        id="golden_water",
        name="黄金水",
        emoji="💧",
        category="special",
        price=800,
        description="神奇的生命之水，浇水后作物24小时内不会缺水。",
        effect={"water_retention": 24}
    ),
    ShopItem(
        id="xp_boost",
        name="经验药水",
        emoji="🧪",
        category="special",
        price=400,
        description="使用后获得的经验值翻倍。",
        effect={"xp_boost": 1.0}
    ),
]

@router.get("/items", response_model=List[ShopItem])
async def get_shop_items():
    return shop_items

@router.post("/buy")
async def buy_item(request: BuyRequest):
    from backend.services.game_session import game_service
    
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    gm = game_service.get_current_game()
    player = gm.player
    
    item = next((i for i in shop_items if i.id == request.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    total_price = item.price * request.quantity
    if player.money < total_price:
        raise HTTPException(status_code=400, detail="金币不足")
    
    player.money -= total_price
    
    if item.category == "seed":
        if not hasattr(player, 'inventory'):
            player.inventory = {}
        seed_key = f"seed_{item.effect['crop']}"
        player.inventory[seed_key] = player.inventory.get(seed_key, 0) + request.quantity
    
    if not hasattr(player, 'shop_history'):
        player.shop_history = []
    player.shop_history.append({
        "item_id": item.id,
        "quantity": request.quantity,
        "total_price": total_price
    })
    
    return {
        "success": True,
        "message": f"购买了 {request.quantity} 个 {item.name}",
        "remaining_gold": player.money
    }

@router.get("/history")
async def get_shop_history():
    from backend.services.game_session import game_service
    
    if not game_service.has_active_game():
        return {"history": []}
    
    gm = game_service.get_current_game()
    player = gm.player
    return {"history": getattr(player, 'shop_history', [])}
