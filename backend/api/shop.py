from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/shop", tags=["shop"])

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
    ShopItem(
        id="fertilizer_basic",
        name="普通肥料",
        emoji="🧪",
        category="fertilizer",
        price=50,
        description="促进作物生长，生长速度+10%",
        effect={"growth_bonus": 0.1}
    ),
    ShopItem(
        id="fertilizer_advanced",
        name="高级肥料",
        emoji="⚗️",
        category="fertilizer",
        price=150,
        description="显著促进作物生长，生长速度+25%",
        effect={"growth_bonus": 0.25}
    ),
    ShopItem(
        id="water_can",
        name="高级水壶",
        emoji="🚿",
        category="tool",
        price=200,
        description="浇水效率提升，一次可以浇更多作物",
        effect={"water_capacity": 10}
    ),
    ShopItem(
        id="scarecrow",
        name="稻草人",
        emoji="🎃",
        category="decoration",
        price=300,
        description="保护农田不受乌鸦侵扰",
        effect={"protect_birds": True}
    ),
    ShopItem(
        id="greenhouse",
        name="温室大棚",
        emoji="🏡",
        category="building",
        price=2000,
        description="保护作物不受恶劣天气影响",
        effect={"weather_protection": True}
    ),
    ShopItem(
        id="chicken_coop",
        name="鸡舍",
        emoji="🐔",
        category="building",
        price=1500,
        description="每天自动产出鸡蛋",
        effect={"auto_eggs": True}
    ),
    ShopItem(
        id="cow_barn",
        name="牛棚",
        emoji="🐄",
        category="building",
        price=3000,
        description="每天自动产出牛奶",
        effect={"auto_milk": True}
    ),
    ShopItem(
        id="seed_radish",
        name="萝卜种子",
        emoji="🥕",
        category="seed",
        price=20,
        description="生长快速，适合新手",
        effect={"crop": "radish", "grow_days": 3}
    ),
    ShopItem(
        id="seed_corn",
        name="玉米种子",
        emoji="🌽",
        category="seed",
        price=50,
        description="中等收益作物",
        effect={"crop": "corn", "grow_days": 5}
    ),
    ShopItem(
        id="seed_tomato",
        name="番茄种子",
        emoji="🍅",
        category="seed",
        price=80,
        description="高收益作物",
        effect={"crop": "tomato", "grow_days": 7}
    ),
]

@router.get("/items", response_model=List[ShopItem])
async def get_shop_items():
    return shop_items

@router.post("/buy")
async def buy_item(request: BuyRequest, db=None):
    from backend.main import game_session
    from models.player import Player
    
    player = game_session.player
    if not player:
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    item = next((i for i in shop_items if i.id == request.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    total_price = item.price * request.quantity
    if player.gold < total_price:
        raise HTTPException(status_code=400, detail="金币不足")
    
    player.gold -= total_price
    
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
        "remaining_gold": player.gold
    }

@router.get("/history")
async def get_shop_history():
    from backend.main import game_session
    player = game_session.player
    if not player:
        return {"history": []}
    return {"history": getattr(player, 'shop_history', [])}
