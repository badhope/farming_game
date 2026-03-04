"""
经济系统模块
管理游戏中的买卖交易
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List
from config.settings import CropData, Season
from models.crop import Crop
from models.player import Player


@dataclass
class TransactionResult:
    """
    交易结果数据类
    
    记录一次交易的详细信息
    """
    success: bool
    item_name: str
    quantity: int
    unit_price: int
    total_amount: int
    message: str


class EconomySystem:
    """
    经济系统类
    
    管理商店、买卖逻辑、价格计算等
    """
    
    def __init__(self):
        """初始化经济系统"""
        self._crop_cache: Dict[str, Crop] = {}
        self._build_crop_cache()
    
    def _build_crop_cache(self) -> None:
        """构建作物数据缓存"""
        for name, data in CropData.CROPS.items():
            crop = Crop(
                name=name,
                seed_price=data["seed_price"],
                sell_price=data["sell_price"],
                grow_days=data["grow_days"],
                seasons=data["seasons"],
                water_needed=data["water_needed"],
                emoji=data["emoji"],
                crop_type=data["crop_type"],
                description=data.get("description", ""),
            )
            self._crop_cache[name] = crop
    
    # ========== 作物数据获取 ==========
    
    def get_crop(self, crop_name: str) -> Optional[Crop]:
        """
        获取作物数据
        
        Args:
            crop_name: 作物名称
            
        Returns:
            Optional[Crop]: 作物对象，不存在返回None
        """
        return self._crop_cache.get(crop_name)
    
    def get_all_crops(self) -> List[Crop]:
        """
        获取所有作物列表
        
        Returns:
            List[Crop]: 作物列表
        """
        return list(self._crop_cache.values())
    
    def get_crops_by_season(self, season: Season) -> List[Crop]:
        """
        获取指定季节可种植的作物
        
        Args:
            season: 季节
            
        Returns:
            List[Crop]: 可种植作物列表
        """
        return [
            crop for crop in self._crop_cache.values()
            if crop.can_plant_in_season(season)
        ]
    
    def get_crop_names(self) -> List[str]:
        """
        获取所有作物名称列表
        
        Returns:
            List[str]: 作物名称列表
        """
        return list(self._crop_cache.keys())
    
    # ========== 购买种子 ==========
    
    def buy_seeds(
        self, player: Player, crop_name: str, quantity: int = 1
    ) -> TransactionResult:
        """
        玩家购买种子
        
        Args:
            player: 玩家对象
            crop_name: 作物名称
            quantity: 购买数量
            
        Returns:
            TransactionResult: 交易结果
        """
        crop = self.get_crop(crop_name)
        
        # 检查作物是否存在
        if crop is None:
            return TransactionResult(
                success=False,
                item_name=crop_name,
                quantity=quantity,
                unit_price=0,
                total_amount=0,
                message=f"❌ 没有名为「{crop_name}」的种子！"
            )
        
        # 计算总价
        total_cost = crop.seed_price * quantity
        
        # 检查金币是否足够
        if not player.can_afford(total_cost):
            return TransactionResult(
                success=False,
                item_name=crop_name,
                quantity=quantity,
                unit_price=crop.seed_price,
                total_amount=total_cost,
                message=f"❌ 金币不足！需要 {total_cost} 金币，你只有 {player.money} 金币。"
            )
        
        # 执行购买
        player.spend_money(total_cost)
        player.add_seeds(crop_name, quantity)
        
        return TransactionResult(
            success=True,
            item_name=crop_name,
            quantity=quantity,
            unit_price=crop.seed_price,
            total_amount=total_cost,
            message=f"✅ 成功购买 {quantity} 个 {crop.emoji} {crop_name} 种子，花费 {total_cost} 金币。"
        )
    
    # ========== 出售作物 ==========
    
    def sell_crop(
        self, player: Player, crop_name: str, quantity: int = 1
    ) -> TransactionResult:
        """
        玩家出售作物
        
        Args:
            player: 玩家对象
            crop_name: 作物名称
            quantity: 出售数量
            
        Returns:
            TransactionResult: 交易结果
        """
        crop = self.get_crop(crop_name)
        
        # 检查作物是否存在
        if crop is None:
            return TransactionResult(
                success=False,
                item_name=crop_name,
                quantity=quantity,
                unit_price=0,
                total_amount=0,
                message=f"❌ 没有名为「{crop_name}」的作物！"
            )
        
        # 检查背包中是否有足够的作物
        if not player.has_item(crop_name, quantity):
            owned = player.get_inventory_count(crop_name)
            return TransactionResult(
                success=False,
                item_name=crop_name,
                quantity=quantity,
                unit_price=crop.sell_price,
                total_amount=0,
                message=f"❌ {crop.emoji} {crop_name} 数量不足！你有 {owned} 个，想卖 {quantity} 个。"
            )
        
        # 执行出售
        total_earning = crop.sell_price * quantity
        player.remove_from_inventory(crop_name, quantity)
        player.earn_money(total_earning)
        
        return TransactionResult(
            success=True,
            item_name=crop_name,
            quantity=quantity,
            unit_price=crop.sell_price,
            total_amount=total_earning,
            message=f"💰 成功出售 {quantity} 个 {crop.emoji} {crop_name}，获得 {total_earning} 金币！"
        )
    
    def sell_all_of_type(self, player: Player, crop_name: str) -> TransactionResult:
        """
        出售背包中指定作物的全部数量
        
        Args:
            player: 玩家对象
            crop_name: 作物名称
            
        Returns:
            TransactionResult: 交易结果
        """
        quantity = player.get_inventory_count(crop_name)
        
        if quantity <= 0:
            crop = self.get_crop(crop_name)
            emoji = crop.emoji if crop else ""
            return TransactionResult(
                success=False,
                item_name=crop_name,
                quantity=0,
                unit_price=0,
                total_amount=0,
                message=f"❌ 你的背包中没有 {emoji} {crop_name}！"
            )
        
        return self.sell_crop(player, crop_name, quantity)
    
    def sell_all_crops(self, player: Player) -> List[TransactionResult]:
        """
        出售背包中的所有作物

        Args:
            player: 玩家对象

        Returns:
            List[TransactionResult]: 所有交易结果列表
        """
        results = []
        
        try:
            # 获取背包中所有作物名称（复制一份，因为会在循环中修改）
            items_to_sell = list(player.inventory.keys())
            
            for crop_name in items_to_sell:
                try:
                    result = self.sell_all_of_type(player, crop_name)
                    results.append(result)
                except Exception as e:
                    # 单个作物出售失败不影响其他作物
                    results.append(TransactionResult(
                        success=False,
                        item_name=crop_name,
                        quantity=0,
                        unit_price=0,
                        total_amount=0,
                        message=f"❌ 出售 {crop_name} 时出错: {str(e)}"
                    ))
        except Exception as e:
            # 整体操作失败，返回错误结果
            results.append(TransactionResult(
                success=False,
                item_name="",
                quantity=0,
                unit_price=0,
                total_amount=0,
                message=f"❌ 出售所有作物时出错: {str(e)}"
            ))
        
        return results
    
    # ========== 价格信息 ==========
    
    def get_price_info(self, crop_name: str) -> Optional[Dict]:
        """
        获取作物的价格信息
        
        Args:
            crop_name: 作物名称
            
        Returns:
            Optional[Dict]: 价格信息字典
        """
        crop = self.get_crop(crop_name)
        
        if crop is None:
            return None
        
        return {
            "name": crop.name,
            "emoji": crop.emoji,
            "seed_price": crop.seed_price,
            "sell_price": crop.sell_price,
            "profit": crop.get_profit(),
            "profit_per_day": crop.get_profit_per_day(),
            "roi": crop.get_roi(),
        }
    
    def get_best_profit_crops(self, limit: int = 5) -> List[Tuple[str, int]]:
        """
        获取利润最高的作物
        
        Args:
            limit: 返回数量限制
            
        Returns:
            List[Tuple[str, int]]: (作物名称, 利润) 列表
        """
        profits = [
            (name, crop.get_profit())
            for name, crop in self._crop_cache.items()
        ]
        
        # 按利润降序排序
        profits.sort(key=lambda x: x[1], reverse=True)
        
        return profits[:limit]
    
    def get_best_roi_crops(self, limit: int = 5) -> List[Tuple[str, float]]:
        """
        获取投资回报率最高的作物
        
        Args:
            limit: 返回数量限制
            
        Returns:
            List[Tuple[str, float]]: (作物名称, ROI) 列表
        """
        rois = [
            (name, crop.get_roi())
            for name, crop in self._crop_cache.items()
        ]
        
        # 按ROI降序排序
        rois.sort(key=lambda x: x[1], reverse=True)
        
        return rois[:limit]
    
    def get_fastest_growing_crops(self, limit: int = 5) -> List[Tuple[str, int]]:
        """
        获取生长最快的作物
        
        Args:
            limit: 返回数量限制
            
        Returns:
            List[Tuple[str, int]]: (作物名称, 生长天数) 列表
        """
        grow_times = [
            (name, crop.grow_days)
            for name, crop in self._crop_cache.items()
        ]
        
        # 按生长天数升序排序
        grow_times.sort(key=lambda x: x[1])
        
        return grow_times[:limit]
    
    # ========== 商店显示 ==========
    
    def get_shop_display(self, season: Optional[Season] = None) -> str:
        """
        获取商店显示文本
        
        Args:
            season: 当前季节（用于标记可种植作物）
            
        Returns:
            str: 商店显示文本
        """
        lines = [
            "",
            "=" * 60,
            "🏪 种子商店",
            "=" * 60,
            "",
            "可购买的种子：",
            "",
        ]
        
        for name, crop in self._crop_cache.items():
            # 检查是否是当前季节可种植
            can_plant = season and crop.can_plant_in_season(season)
            status_icon = "✅" if can_plant else "⬜"
            
            # 计算投资回报率
            roi = crop.get_roi()
            profit_per_day = crop.get_profit_per_day()
            
            line = (
                f"  {status_icon} {crop.emoji} {name:6s} | "
                f"种子: {crop.seed_price:4d}金 | "
                f"售价: {crop.sell_price:4d}金 | "
                f"利润: {crop.get_profit():4d}金 | "
                f"周期: {crop.grow_days}天 | "
                f"日收益: {profit_per_day:.1f}金"
            )
            lines.append(line)
        
        lines.extend([
            "",
            "📌 提示: ✅ = 当前季节可种植",
            "=" * 60,
        ])
        
        return "\n".join(lines)
    
    def get_crop_detail_display(self, crop_name: str) -> str:
        """
        获取作物详情显示
        
        Args:
            crop_name: 作物名称
            
        Returns:
            str: 详情显示文本
        """
        crop = self.get_crop(crop_name)
        
        if crop is None:
            return f"❌ 没有名为「{crop_name}」的作物！"
        
        lines = [
            "",
            "=" * 50,
            f"{crop.emoji} {crop.name}",
            "=" * 50,
            f"📝 描述: {crop.description}",
            f"🌱 种子价格: {crop.seed_price} 金币",
            f"💰 出售价格: {crop.sell_price} 金币",
            f"📈 利润: {crop.get_profit()} 金币",
            f"📅 生长周期: {crop.grow_days} 天",
            f"💧 每日需水: {crop.water_needed} 次",
            f"🌡️ 适宜季节: {crop.get_seasons_str()}",
            f"📊 投资回报率: {crop.get_roi()}%",
            f"📆 日均收益: {crop.get_profit_per_day()} 金币/天",
            f"🏷️ 类型: {crop.crop_type.value}",
            "=" * 50,
        ]
        
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return f"EconomySystem(crops={len(self._crop_cache)})"
    
    def __repr__(self) -> str:
        return f"EconomySystem(crop_count={len(self._crop_cache)})"
