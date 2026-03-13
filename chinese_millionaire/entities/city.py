#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
城市系统
定义 4 个核心城市及其特性
"""


class City:
    """城市类"""
    
    def __init__(self, name, city_type, description, business_bonus, cost_of_living, special_events, culture):
        self.name = name
        self.type = city_type
        self.description = description
        self.business_bonus = business_bonus
        self.cost_of_living = cost_of_living
        self.special_events = special_events
        self.culture = culture


class CitySystem:
    """
    城市系统 - 管理所有城市数据
    """
    
    def __init__(self):
        self.cities = {
            "广州": City(
                name="广州",
                city_type="沿海发达",
                description="千年商都，商贸发达，美食天堂",
                business_bonus={
                    "trade": 1.3,  # 贸易 +30%
                    "food": 1.5  # 餐饮业 +50%
                },
                cost_of_living=1.2,
                special_events=["广交会", "春运"],
                culture="务实开放，饮茶文化"
            ),
            
            "深圳": City(
                name="深圳",
                city_type="沿海发达",
                description="科技之都，创新之城，年轻人聚集",
                business_bonus={
                    "tech": 1.5,  # 科技 +50%
                    "finance": 1.3  # 金融 +30%
                },
                cost_of_living=1.5,
                special_events=["高交会", "创业大赛"],
                culture="快节奏，创业氛围浓"
            ),
            
            "北京": City(
                name="北京",
                city_type="政治中心",
                description="首都，政治文化中心，国企总部聚集",
                business_bonus={
                    "gov_project": 1.5,  # 政府项目 +50%
                    "culture": 1.3  # 文化产业 +30%
                },
                cost_of_living=1.8,
                special_events=["两会", "中关村论坛"],
                culture="京味文化，圈子文化"
            ),
            
            "上海": City(
                name="上海",
                city_type="金融中心",
                description="魔都，金融中心，国际化大都市",
                business_bonus={
                    "finance": 1.5,  # 金融 +50%
                    "luxury": 1.4  # 奢侈品 +40%
                },
                cost_of_living=2.0,
                special_events=["进博会", "上海电影节"],
                culture="小资情调，精致生活"
            )
        }
        
    def get_city(self, city_name):
        """获取城市数据"""
        city = self.cities.get(city_name)
        if city:
            return {
                'name': city.name,
                'description': city.description,
                'business_bonus': city.business_bonus,
                'cost_of_living': city.cost_of_living,
                'special_events': city.special_events,
                'culture': city.culture
            }
        return None
        
    def get_all_cities(self):
        """获取所有城市"""
        return list(self.cities.keys())
