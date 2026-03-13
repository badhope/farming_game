#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
解锁系统
管理随身份提升逐步开放的内容
"""


class UnlockSystem:
    """
    解锁系统 - 动态解锁游戏内容
    
    设计理念:
    - 低身份只能看到基础功能
    - 高身份解锁隐藏功能
    - 同一地点，不同身份看到不同内容
    """
    
    def __init__(self):
        # 商场解锁层级
        self.mall_unlocks = {
            1: ["路边摊", "小卖部"],
            2: ["超市", "快餐店"],
            3: ["品牌店", "电器城"],
            4: ["奢侈品店", "车行"],
            5: ["豪宅销售中心", "私人银行"],
            6: ["艺术品拍卖行", "私人俱乐部"],
            7: ["私人飞机销售", "海岛销售"],
            8: ["卫星订购", "私人军队"]
        }
        
        # 城市解锁层级
        self.city_unlocks = {
            1: ["县城", "乡镇"],
            2: ["地级市"],
            3: ["省会城市"],
            4: ["一线城市（北上广深）"],
            5: ["港澳台"],
            6: ["东南亚", "日韩"],
            7: ["欧美", "中东"],
            8: ["全球任意地点"]
        }
        
        # 信息渠道解锁
        self.info_channels = {
            1: ["街头传闻", "本地新闻"],
            2: ["电视新闻", "报纸"],
            3: ["网络论坛", "行业报告"],
            4: ["财经新闻", "内部会议"],
            5: ["私人情报网", "投行报告"],
            6: ["政府内参", "高层饭局"],
            7: ["国家机密", "国际情报"],
            8: ["全知视角"]
        }
        
        # 商业功能解锁
        self.business_unlocks = {
            1: ["打工", "摆摊"],
            2: ["开小店", "批发零售"],
            3: ["开公司", "银行贷款"],
            4: ["招投标", "政府采购"],
            5: ["房地产投资", "股票基金"],
            6: ["并购重组", "私募股权"],
            7: ["跨国贸易", "金融杠杆"],
            8: ["垄断行业", "影响政策"]
        }
        
    def get_visible_locations(self, player_level):
        """获取玩家可见的地点"""
        visible = []
        for level, locations in self.city_unlocks.items():
            if level <= player_level:
                visible.extend(locations)
        return visible
        
    def get_available_shops(self, player_level, location):
        """
        根据身份返回可用商店
        
        同一地点，不同身份看到不同商店
        """
        # 基础商店映射
        base_shops_map = {
            "县城": ["小卖部", "超市", "饭店"],
            "地级市": ["商场", "车行", "餐厅"],
            "省会城市": ["品牌店", "电器城", "酒店"],
            "一线城市（北上广深）": ["奢侈品店", "车行", "豪宅销售中心"],
            "港澳台": ["奢侈品店", "私人银行"],
            "东南亚": ["度假村", "赌场"],
            "欧美": ["私人飞机销售", "艺术品拍卖行"],
            "全球任意地点": ["海岛销售", "卫星订购"]
        }
        
        # 获取基础商店
        base_shops = []
        for loc_name, shops in base_shops_map.items():
            if loc_name in location or location in loc_name:
                base_shops.extend(shops)
                
        # 过滤掉身份不够的商店
        filtered_shops = []
        for shop in base_shops:
            required_level = self._get_shop_requirement(shop)
            if required_level <= player_level:
                filtered_shops.append(shop)
            else:
                # 显示为"？？？"，增加神秘感
                filtered_shops.append(f"??? (需要身份等级{required_level})")
                
        return filtered_shops if filtered_shops else ["小卖部"]
        
    def _get_shop_requirement(self, shop_name):
        """获取商店需要的身份等级"""
        requirements = {
            "路边摊": 1,
            "小卖部": 1,
            "超市": 2,
            "快餐店": 2,
            "品牌店": 3,
            "电器城": 3,
            "奢侈品店": 4,
            "车行": 4,
            "豪宅销售中心": 5,
            "私人银行": 5,
            "艺术品拍卖行": 6,
            "私人俱乐部": 6,
            "私人飞机销售": 7,
            "海岛销售": 7,
            "卫星订购": 8,
            "私人军队": 8
        }
        return requirements.get(shop_name, 99)
        
    def get_unlocked_business(self, player_level):
        """获取解锁的商业功能"""
        unlocked = []
        for level, businesses in self.business_unlocks.items():
            if level <= player_level:
                unlocked.extend(businesses)
        return unlocked
        
    def get_info_channels(self, player_level):
        """获取可用的信息渠道"""
        channels = []
        for level, channel_list in self.info_channels.items():
            if level <= player_level:
                channels.extend(channel_list)
        return channels
