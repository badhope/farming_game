#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试脚本
自动演示游戏基本流程
"""

import sys
sys.path.insert(0, '.')

from entities.player import Player
from entities.identity import IdentitySystem
from core.economy import EconomySystem
from core.company import Company, CompanySystem
from core.shopping import ShoppingMall

def test_game():
    """测试游戏基本功能"""
    
    print("=" * 80)
    print("中国百万富翁 - 功能测试")
    print("=" * 80)
    
    # 测试 1: 身份系统
    print("\n【测试 1: 身份系统】")
    identity_system = IdentitySystem()
    identities = identity_system.get_all_identities()
    
    print(f"共有 {len(identities)} 个身份:")
    for i, identity in enumerate(identities, 1):
        print(f"{i}. {identity['name']} - 启动资金：¥{identity['start_money']:,}")
        
    # 测试 2: 创建玩家
    print("\n【测试 2: 创建玩家】")
    player = Player("测试玩家", identities[0])  # 选择农民
    print(f"玩家：{player.name}")
    print(f"身份：{player.identity}")
    print(f"现金：¥{player.cash:,}")
    print(f"阶层：{player.current_class}")
    
    # 测试 3: 工作赚钱
    print("\n【测试 3: 工作赚钱】")
    income = player.work()
    print(f"工作收入：¥{income:,}")
    print(f"当前现金：¥{player.cash:,}")
    
    # 测试 4: 学习提升
    print("\n【测试 4: 学习提升】")
    old_rep = player.reputation
    player.study()
    print(f"声誉：{old_rep} → {player.reputation}")
    
    # 测试 5: 休息恢复
    print("\n【测试 5: 休息恢复】")
    player.stamina = 50
    recovered = player.rest()
    print(f"体力恢复：{recovered}点，当前体力：{player.stamina}")
    
    # 测试 6: 公司系统
    print("\n【测试 6: 公司系统】")
    company_system = CompanySystem()
    company = company_system.create_company("测试农场", "农业", player)
    player.company = company
    print(f"创建公司：{company.name} ({company.type})")
    
    profit = company.daily_operation()
    print(f"日利润：¥{profit:,}")
    print(f"月利润：¥{company.monthly_profit:,}")
    
    # 测试 7: 阶层晋升
    print("\n【测试 7: 阶层晋升测试】")
    player.cash = 1000000  # 直接给 100 万
    player.check_class_promotion()
    print(f"当前阶层：{player.current_class} (等级{player.class_level})")
    
    # 测试 8: 购物系统
    print("\n【测试 8: 购物系统】")
    mall = ShoppingMall()
    items = mall.browse("生活消费")
    print(f"生活消费品数量：{len(items)}")
    print("前 3 个商品:")
    for i, item in enumerate(items[:3], 1):
        print(f"  {i}. {item['name']} - ¥{item['price']} ({item['effect']})")
        
    # 测试 9: 经济系统
    print("\n【测试 9: 经济系统】")
    economy = EconomySystem()
    print(f"GDP 增长率：{economy.gdp_growth:.2%}")
    print(f"通胀率：{economy.inflation_rate:.2%}")
    print(f"失业率：{economy.unemployment_rate:.2%}")
    
    # 测试 10: 财务报表
    print("\n【测试 10: 财务报表】")
    print(f"总资产：¥{player.total_assets:,}")
    print(f"净资产：¥{player.net_worth:,}")
    print(f"财富排名：第{player.ranking}名")
    
    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)
    

if __name__ == "__main__":
    test_game()
