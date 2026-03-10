#!/usr/bin/env python3
"""测试脚本 - 用于验证 API 功能"""
import requests

BASE_URL = "http://localhost:8000/api"

def main():
    # 创建游戏
    print("=== 测试创建游戏 ===")
    r = requests.post(f"{BASE_URL}/player/create", json={"player_name": "测试农夫"})
    print(r.json())
    
    # 测试种植
    print("\n=== 测试种植 ===")
    r = requests.post(f"{BASE_URL}/farm/plant", json={"row": 0, "col": 0, "crop_name": "土豆"})
    print(f"种植结果: {r.json()}")
    
    # 测试浇水
    print("\n=== 测试浇水 ===")
    r = requests.post(f"{BASE_URL}/farm/water", json={"row": 0, "col": 0})
    print(f"浇水结果: {r.json()}")
    
    # 推进时间让作物成熟（土豆需要3天）
    print("\n=== 推进时间 ===")
    for i in range(10):
        r = requests.post(f"{BASE_URL}/game/advance_day")
        data = r.json()
        if data.get("success"):
            print(f"第{i+1}天: {data.get('message', '')}")
    
    # 检查农田状态
    print("\n=== 检查农田状态 ===")
    r = requests.get(f"{BASE_URL}/farm/plots")
    plots = r.json()
    print(f"  位置 (0, 0): is_mature={plots[0]['is_mature']}, days_since_planted={plots[0]['days_since_planted']}")
    
    # 测试收获
    print("\n=== 测试收获 ===")
    r = requests.post(f"{BASE_URL}/farm/harvest", json={"row": 0, "col": 0})
    print(f"收获结果: {r.json()}")
    
    # 测试保存游戏
    print("\n=== 测试保存游戏 ===")
    r = requests.post(f"{BASE_URL}/game/save", json={"save_name": "test_save"})
    print(f"保存结果: {r.json()}")
    
    # 测试读取存档列表
    print("\n=== 测试存档列表 ===")
    r = requests.get(f"{BASE_URL}/game/saves")
    print(f"存档列表: {r.json()}")
    
    # 测试AI建议
    print("\n=== 测试AI建议 ===")
    r = requests.get(f"{BASE_URL}/ai/advice/planting")
    print(f"种植建议: {r.json()}")
    
    # 测试玩家信息
    print("\n=== 测试玩家信息 ===")
    r = requests.get(f"{BASE_URL}/player/info")
    print(f"玩家信息: {r.json()}")
    
    # 测试玩家统计
    print("\n=== 测试玩家统计 ===")
    r = requests.get(f"{BASE_URL}/player/stats")
    if r.status_code == 200:
        print(f"玩家统计: {r.json()}")
    else:
        print(f"错误: {r.status_code}")

    # 测试AI聊天
    print("\n=== 测试AI聊天 ===")
    r = requests.post(f"{BASE_URL}/ai/chat", json={"message": "现在适合种什么?"})
    print(f"AI回复: {r.json()}")
    
    # 测试游戏状态
    print("\n=== 测试游戏状态 ===")
    r = requests.get(f"{BASE_URL}/game/status")
    print(f"游戏状态: {r.json()}")

if __name__ == "__main__":
    main()
