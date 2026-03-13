#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
购物系统
管理商场、商品、购买行为
"""


class ShoppingMall:
    """
    购物系统 - 管理商品购买
    """
    
    def __init__(self):
        # 商品分类
        self.categories = {
            "生活消费": {
                "便利店": [
                    {"name": "便当", "price": 15, "effect": "体力 +5"},
                    {"name": "饮料", "price": 5, "effect": "体力 +2"},
                    {"name": "零食", "price": 10, "effect": "心情 +3"}
                ],
                "超市": [
                    {"name": "食材", "price": 100, "effect": "可做饭"},
                    {"name": "日用品", "price": 50, "effect": "生活必需"},
                    {"name": "小家电", "price": 500, "effect": "生活质量 +5"}
                ],
                "餐厅": [
                    {"name": "快餐", "price": 30, "effect": "体力 +10"},
                    {"name": "正餐", "price": 200, "effect": "体力 +20, 心情 +10"},
                    {"name": "高端料理", "price": 1000, "effect": "体力 +50, 心情 +30"}
                ]
            },
            
            "奢侈品": {
                "名牌店": [
                    {"name": "名牌包包", "price": 5000, "effect": "心情 +50, 声誉 +5"},
                    {"name": "名牌手表", "price": 20000, "effect": "心情 +80, 声誉 +10"},
                    {"name": "珠宝", "price": 50000, "effect": "心情 +100, 声誉 +20"}
                ],
                "豪车店": [
                    {"name": "宝马 3 系", "price": 300000, "effect": "交通工具，声誉 +30"},
                    {"name": "奔驰 E 级", "price": 500000, "effect": "交通工具，声誉 +50"},
                    {"name": "保时捷 911", "price": 1500000, "effect": "顶级交通工具，声誉 +100"}
                ]
            },
            
            "房产": {
                "住宅": [
                    {"name": "公寓 (50 平)", "price": 2000000, "effect": "住所，每月升值"},
                    {"name": "别墅 (300 平)", "price": 10000000, "effect": "豪华住所，声誉 +50"}
                ],
                "商铺": [
                    {"name": "写字楼", "price": 5000000, "effect": "可出租，月租金收入"},
                    {"name": "店面", "price": 3000000, "effect": "可自营或出租"}
                ]
            }
        }
        
    def browse(self, category, shop_name=None):
        """浏览商品"""
        if category not in self.categories:
            return []
            
        if shop_name:
            return self.categories[category].get(shop_name, [])
        else:
            # 返回所有商店
            result = []
            for shop, items in self.categories[category].items():
                result.extend(items)
            return result
            
    def purchase(self, item_name, player):
        """
        购买商品
        返回是否成功
        """
        # 查找商品
        item = self._find_item(item_name)
        
        if not item:
            return False, "商品不存在"
            
        # 检查余额
        if player.cash < item['price']:
            return False, "余额不足"
            
        # 扣款
        player.cash -= item['price']
        
        # 应用效果（简化版）
        print(f"✅ 购买了{item_name}，花费¥{item['price']:,}")
        print(f"效果：{item['effect']}")
        
        # 根据商品类型增加属性
        if "心情" in item['effect']:
            player.happiness += 5
        if "声誉" in item['effect']:
            player.reputation += 1
            
        return True, "购买成功"
        
    def _find_item(self, item_name):
        """查找商品"""
        for category, shops in self.categories.items():
            for shop, items in shops.items():
                for item in items:
                    if item['name'] == item_name:
                        return item
        return None
        
    def get_price_range(self, category):
        """获取价格区间"""
        items = self.browse(category)
        if not items:
            return (0, 0)
            
        prices = [item['price'] for item in items]
        return (min(prices), max(prices))
