#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
游戏主循环系统
负责游戏流程控制、玩家交互、状态更新
"""

from entities.player import Player
from entities.identity import IdentitySystem
from entities.city import CitySystem
from core.economy import EconomySystem
from core.company import CompanySystem
from core.shopping import ShoppingMall
from core.strategy import StrategySystem
from core.intelligence import IntelligenceSystem
from core.unlock import UnlockSystem


class ChineseMillionaireGame:
    """
    中国百万富翁 - 游戏主类
    """
    
    def __init__(self):
        self.player = None
        self.day = 1
        self.economy = EconomySystem()
        self.company_system = CompanySystem()
        self.shopping_mall = ShoppingMall()
        self.strategy_system = StrategySystem()
        self.intelligence = IntelligenceSystem()
        self.unlock_system = UnlockSystem()
        self.identity_system = IdentitySystem()
        self.city_system = CitySystem()
        self.running = True
        
    def start(self):
        """游戏开始"""
        self.show_title()
        self.create_character()
        self.main_loop()
        
    def show_title(self):
        """显示标题"""
        print("\n" + "=" * 80)
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                                                              ║")
        print("║                    中国百万富翁                              ║")
        print("║                  CHINESE MILLIONAIRE                         ║")
        print("║                                                              ║")
        print("║              你的致富之路，从这里开始！                      ║")
        print("║                                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print("=" * 80)
        
    def create_character(self):
        """创建角色 - 选择身份"""
        print("\n" + "=" * 80)
        print("【第一步：选择你的起始身份】")
        print("=" * 80)
        print()
        print("不同的身份将决定你的：")
        print("  • 启动资金")
        print("  • 初始人脉")
        print("  • 特殊技能")
        print("  • 发展路线")
        print()
        
        identities = self.identity_system.get_all_identities()
        
        for i, identity in enumerate(identities, 1):
            print(f"{i}. {identity['name']}")
            print(f"   描述：{identity['description']}")
            print(f"   启动资金：¥{identity['start_money']:,}")
            print(f"   初始人脉：{identity['connections']}/100")
            print(f"   特殊技能：{', '.join(identity['skills'])}")
            print(f"   核心优势：{identity['bonus_description']}")
            print()
            
        while True:
            try:
                choice = int(input("请选择身份 (1-6): "))
                if 1 <= choice <= 6:
                    break
                else:
                    print("❌ 请输入 1-6 之间的数字")
            except ValueError:
                print("❌ 请输入有效的数字")
                
        selected_identity = identities[choice - 1]
        
        print("\n" + "-" * 80)
        player_name = input(f"请输入你的名字：")
        
        self.player = Player(
            name=player_name,
            identity_data=selected_identity
        )
        
        print("\n" + "=" * 80)
        print(f"✅ 角色创建成功！")
        print(f"欢迎你，{self.player.name}！你的致富之路开始了！")
        print(f"初始身份：{self.player.identity}")
        print(f"启动资金：¥{self.player.cash:,.0f}")
        print(f"当前阶层：{self.player.current_class}")
        print("=" * 80)
        
    def main_loop(self):
        """主游戏循环"""
        while self.running and not self.check_gameover():
            # 1. 显示日报表
            self.show_daily_report()
            
            # 2. 显示可用行动（根据身份动态显示）
            self.show_available_actions()
            
            # 3. 玩家选择行动
            action = self.get_player_action()
            
            # 4. 执行行动
            self.execute_action(action)
            
            # 5. 更新游戏状态
            self.update_game_state()
            
            # 6. 进入下一天
            self.day += 1
            
    def show_daily_report(self):
        """显示每日报表"""
        print("\n" + "=" * 80)
        print(f"【第 {self.day} 天】{self.player.name} 的经营报告")
        print("=" * 80)
        
        # 显示财务摘要
        print(f"\n💰 资产状况:")
        print(f"   现金：¥{self.player.cash:,.0f}")
        print(f"   总资产：¥{self.player.total_assets:,.0f}")
        print(f"   净资产：¥{self.player.net_worth:,.0f}")
        
        print(f"\n📊 社会地位:")
        print(f"   当前阶层：{self.player.current_class}")
        print(f"   人脉关系：{self.player.connections}/100")
        print(f"   声誉：{self.player.reputation}/100")
        
        print(f"\n📈 今日情报:")
        intel = self.intelligence.get_market_info("房地产", self.player.class_level)
        print(f"   房地产市场：{intel}")
        
        print()
        
    def show_available_actions(self):
        """显示可用行动"""
        print("【今日行动】")
        print("-" * 80)
        
        # 基础行动（始终可用）
        print("\n📌 基础行动:")
        print("  1. 工作赚钱        - 打工获取收入")
        print("  2. 学习提升        - 提升技能")
        print("  3. 休息恢复        - 恢复体力")
        print("  4. 查看情报        - 获取市场信息")
        
        # 商业行动（根据身份解锁）
        if self.player.class_level >= 2:
            print("\n💼 商业行动:")
            print("  5. 经营公司        - 管理你的企业")
            print("  6. 拓展业务        - 扩大经营规模")
            
        if self.player.class_level >= 4:
            print("  7. 并购重组        - 收购其他公司")
            
        # 投资行动
        if self.player.class_level >= 2:
            print("\n📈 投资行动:")
            print("  8. 购买理财        - 稳健投资")
            
        if self.player.class_level >= 3:
            print("  9. 炒股            - 高风险高回报")
            
        if self.player.class_level >= 4:
            print("  10. 投资房产       - 买房收租")
            
        # 消费行动
        print("\n🛒 消费行动:")
        print("  S. 逛商场购物      - 提升生活质量")
        
        # 查看状态
        print("\n📊 查询:")
        print("  A. 查看完整资产    - 详细财务报表")
        print("  C. 查看公司状况    - 公司经营数据")
        print("  M. 查看地图        - 可前往的城市")
        
        # 保存退出
        print("\n⏸️  游戏控制:")
        print("  0. 保存并退出")
        print()
        
    def get_player_action(self):
        """获取玩家选择的行动"""
        while True:
            action = input("请选择行动：").strip().upper()
            
            # 验证输入
            valid_actions = ['1', '2', '3', '4', 'S', 'A', 'C', 'M', '0']
            
            if self.player.class_level >= 2:
                valid_actions.extend(['5', '6'])
            if self.player.class_level >= 3:
                valid_actions.extend(['9'])
            if self.player.class_level >= 4:
                valid_actions.extend(['7', '8', '10'])
                
            if action in valid_actions:
                return action
            else:
                print("❌ 无效的行动，请重新选择")
                
    def execute_action(self, action):
        """执行玩家行动"""
        if action == "1":  # 工作赚钱
            income = self.player.work()
            print(f"\n💪 你今天努力工作，收入¥{income:,.0f}")
            self.player.stamina -= 10
            
        elif action == "2":  # 学习提升
            result = self.player.study()
            print(f"\n📚 你学习了新知识，技能提升了！")
            self.player.stamina -= 5
            
        elif action == "3":  # 休息恢复
            recovered = self.player.rest()
            print(f"\n😴 你休息了一天，体力恢复了{recovered}点")
            
        elif action == "4":  # 查看情报
            self.show_intelligence()
            
        elif action == "5":  # 经营公司
            if self.player.company:
                profit = self.player.operate_company()
                print(f"\n💼 公司经营结果：利润¥{profit:,.0f}")
            else:
                print("\n❌ 你还没有公司，需要先创建公司")
                
        elif action == "6":  # 拓展业务
            if self.player.company:
                result = self.player.expand_business()
                print(f"\n📈 业务拓展：{result}")
            else:
                print("\n❌ 你还没有公司")
                
        elif action == "S":  # 购物
            self.shopping()
            
        elif action == "A":  # 查看完整资产
            self.show_assets()
            
        elif action == "C":  # 查看公司状况
            self.show_company_status()
            
        elif action == "M":  # 查看地图
            self.show_map()
            
        elif action == "0":  # 保存并退出
            self.save_game()
            self.running = False
            
    def shopping(self):
        """购物系统"""
        print("\n" + "=" * 80)
        print("【购物中心】")
        print("=" * 80)
        
        # 显示可用商店（根据身份过滤）
        available_shops = self.unlock_system.get_available_shops(
            self.player.class_level,
            self.player.city
        )
        
        print(f"\n📍 当前城市：{self.player.city}")
        print(f"可用商店：{', '.join(available_shops)}")
        
        # 简化版购物
        print("\n商品分类:")
        print("  1. 生活用品 (¥10-1000)")
        print("  2. 奢侈品 (¥10000+)")
        print("  3. 房产 (¥100 万+)")
        
        choice = input("请选择分类：")
        
        if choice == "1":
            print("\n你购买了生活用品，生活质量提升了！")
            self.player.cash -= 500
            self.player.happiness += 5
            
        elif choice == "2":
            if self.player.cash >= 10000:
                print("\n你购买了奢侈品，虚荣心得到了满足！")
                self.player.cash -= 10000
                self.player.happiness += 10
                self.player.reputation += 2
            else:
                print("\n❌ 余额不足！")
                
        elif choice == "3":
            print("\n房产交易需要更多操作，将在完整版中实现")
            
    def show_intelligence(self):
        """显示情报"""
        print("\n" + "=" * 80)
        print("【市场情报】")
        print("=" * 80)
        
        # 根据身份显示不同精度的情报
        real_estate_info = self.intelligence.get_market_info(
            "房地产",
            self.player.class_level
        )
        stock_info = self.intelligence.get_market_info(
            "股票",
            self.player.class_level
        )
        
        print(f"\n🏠 房地产市场:")
        print(f"   {real_estate_info}")
        
        print(f"\n📈 股票市场:")
        print(f"   {stock_info}")
        
        # 显示谣言
        rumors = self.intelligence.generate_rumors(self.player.class_level)
        print(f"\n📰 街头传闻:")
        for rumor in rumors:
            print(f"   • {rumor}")
            
    def show_assets(self):
        """显示完整资产"""
        print("\n" + "=" * 80)
        print("【完整财务报表】")
        print("=" * 80)
        
        print(f"\n💰 资产:")
        print(f"   现金：¥{self.player.cash:,.0f}")
        print(f"   房产：¥{self.player.real_estate:,.0f}")
        print(f"   车辆：¥{self.player.vehicles:,.0f}")
        print(f"   投资：¥{self.player.investments:,.0f}")
        print(f"   总资产：¥{self.player.total_assets:,.0f}")
        
        print(f"\n💸 负债:")
        print(f"   贷款：¥{self.player.loans:,.0f}")
        print(f"   总负债：¥{self.player.total_liabilities:,.0f}")
        
        print(f"\n📊 净资产：¥{self.player.net_worth:,.0f}")
        
        print(f"\n📈 财富排名:")
        print(f"   本地排名：第{self.player.ranking}名")
        
    def show_company_status(self):
        """显示公司状况"""
        if self.player.company:
            print("\n" + "=" * 80)
            print("【公司经营状况】")
            print("=" * 80)
            
            company = self.player.company
            print(f"\n公司名称：{company.name}")
            print(f"类型：{company.type}")
            print(f"等级：{company.level}")
            print(f"员工：{company.employees}人")
            print(f"月收入：¥{company.monthly_revenue:,.0f}")
            print(f"月成本：¥{company.monthly_cost:,.0f}")
            print(f"月利润：¥{company.monthly_profit:,.0f}")
        else:
            print("\n❌ 你还没有公司")
            
    def show_map(self):
        """显示地图"""
        print("\n" + "=" * 80)
        print("【可前往的城市】")
        print("=" * 80)
        
        available_cities = self.unlock_system.get_visible_locations(
            self.player.class_level
        )
        
        for city_name in available_cities:
            city_data = self.city_system.get_city(city_name)
            if city_data:
                print(f"\n📍 {city_name}")
                print(f"   {city_data['description']}")
                print(f"   生活成本：{city_data['cost_of_living']}倍")
                print(f"   产业优势：{', '.join(city_data['business_bonus'].keys())}")
                
    def update_game_state(self):
        """更新游戏状态"""
        # 更新经济系统
        self.economy.update_daily()
        
        # 更新公司状态
        if self.player.company:
            self.player.company.update_daily()
            
        # 检查阶层晋升
        self.player.check_class_promotion()
        
        # 随机事件
        if self.day % 7 == 0:  # 每周触发一次
            self.trigger_random_event()
            
    def trigger_random_event(self):
        """触发随机事件"""
        events = [
            ("政策利好", "政府出台新政策，你的企业受益！利润 +20%", 0.3),
            ("市场低迷", "经济不景气，收入减少", -0.2),
            ("贵人相助", "遇到贵人指点，获得投资机会", 0.5),
            ("意外支出", "突然生病/修车，支出增加", -0.1),
        ]
        
        import random
        event = random.choice(events)
        
        print(f"\n📰 随机事件：{event[0]}")
        print(f"   {event[1]}")
        
        # 应用效果
        if event[2] > 0:
            self.player.cash *= (1 + event[2])
        else:
            self.player.cash *= (1 + event[2])
            
    def check_gameover(self):
        """检查游戏结束条件"""
        # 破产判定
        if self.player.net_worth < 0:
            print("\n" + "=" * 80)
            print("💀 游戏结束")
            print("=" * 80)
            print(f"\n你破产了！")
            print(f"最终净资产：¥{self.player.net_worth:,.0f}")
            print(f"存活天数：{self.day}天")
            print("\n感谢游玩！欢迎重新开始！")
            return True
            
        # 健康判定
        if self.player.health <= 0:
            print("\n" + "=" * 80)
            print("💀 游戏结束")
            print("=" * 80)
            print(f"\n你累倒了！健康最重要！")
            print(f"最终资产：¥{self.player.net_worth:,.0f}")
            return True
            
        # 腐败判定（官二代专属）
        if hasattr(self.player, 'corruption') and self.player.corruption >= 100:
            print("\n" + "=" * 80)
            print("💀 游戏结束")
            print("=" * 80)
            print(f"\n你被调查了！")
            print(f"腐败值：{self.player.corruption}/100")
            return True
            
        # 胜利条件
        if self.player.net_worth >= 100_000_000_000:  # 1000 亿
            print("\n" + "=" * 80)
            print("🏆 恭喜通关！")
            print("=" * 80)
            print(f"\n你成为了千亿富豪！")
            print(f"最终资产：¥{self.player.net_worth:,.0f}")
            print(f"用时：{self.day}天")
            print("\n你是真正的中国百万富翁！")
            return True
            
        return False
        
    def save_game(self):
        """保存游戏"""
        import json
        import os
        
        save_data = {
            "day": self.day,
            "player": self.player.to_dict()
        }
        
        save_file = f"saves/save_{self.player.name}_{self.day}.json"
        
        try:
            os.makedirs("saves", exist_ok=True)
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 游戏已保存到：{save_file}")
        except Exception as e:
            print(f"\n❌ 保存失败：{e}")
