"""
配置加载器单元测试
测试 JSON 配置文件的读取和解析
"""

import unittest
import json
import os
from pathlib import Path
from config.config_loader import ConfigLoader, get_crop_config, get_achievement_config


class TestConfigLoader(unittest.TestCase):
    """测试配置加载器"""
    
    def setUp(self):
        """准备测试环境"""
        self.loader = ConfigLoader()
        # 重置单例状态
        ConfigLoader._instance = None
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        loader1 = ConfigLoader()
        loader2 = ConfigLoader()
        
        self.assertIs(loader1, loader2)
    
    def test_load_crop_data(self):
        """测试加载作物数据"""
        crops = self.loader.get_crop_data()
        
        self.assertIsInstance(crops, dict)
        self.assertGreater(len(crops), 0)
        
        # 检查是否有土豆
        self.assertIn("potato", crops)
    
    def test_load_achievement_data(self):
        """测试加载成就数据"""
        achievements = self.loader.get_achievement_data()
        
        self.assertIsInstance(achievements, dict)
        self.assertGreater(len(achievements), 0)
        
        # 检查是否有初次收获成就
        self.assertIn("first_harvest", achievements)
    
    def test_get_crop_by_id(self):
        """测试根据 ID 获取作物"""
        crop = self.loader.get_crop_by_id("potato")
        
        self.assertIsNotNone(crop)
        self.assertEqual(crop["name"], "土豆")
        self.assertEqual(crop["seed_price"], 50)
    
    def test_get_nonexistent_crop(self):
        """测试获取不存在的作物"""
        crop = self.loader.get_crop_by_id("nonexistent_crop")
        
        self.assertIsNone(crop)
    
    def test_get_all_crop_ids(self):
        """测试获取所有作物 ID"""
        crop_ids = self.loader.get_all_crop_ids()
        
        self.assertIsInstance(crop_ids, list)
        self.assertGreater(len(crop_ids), 0)
        self.assertIn("potato", crop_ids)
    
    def test_get_achievement_by_id(self):
        """测试根据 ID 获取成就"""
        achievement = self.loader.get_achievement_by_id("first_harvest")
        
        self.assertIsNotNone(achievement)
        self.assertIn("初次收获", achievement["name"])
    
    def test_get_all_achievement_ids(self):
        """测试获取所有成就 ID"""
        achievement_ids = self.loader.get_all_achievement_ids()
        
        self.assertIsInstance(achievement_ids, list)
        self.assertGreater(len(achievement_ids), 0)
        self.assertIn("first_harvest", achievement_ids)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_get_crop_config(self):
        """测试获取作物配置便捷函数"""
        crop = get_crop_config("potato")
        
        self.assertIsNotNone(crop)
        self.assertEqual(crop["name"], "土豆")
    
    def test_get_achievement_config(self):
        """测试获取成就配置便捷函数"""
        achievement = get_achievement_config("first_harvest")
        
        self.assertIsNotNone(achievement)
        self.assertIn("初次收获", achievement["name"])


class TestConfigDataIntegrity(unittest.TestCase):
    """测试配置数据完整性"""
    
    def setUp(self):
        """准备测试数据"""
        self.loader = ConfigLoader()
    
    def test_crop_data_structure(self):
        """测试作物数据结构完整性"""
        crops = self.loader.get_crop_data()
        
        required_fields = [
            "name", "seed_price", "sell_price", 
            "grow_days", "seasons", "emoji"
        ]
        
        for crop_id, crop_data in crops.items():
            for field in required_fields:
                self.assertIn(
                    field, crop_data,
                    f"作物 {crop_id} 缺少字段 {field}"
                )
    
    def test_crop_price_valid(self):
        """测试作物价格有效性"""
        crops = self.loader.get_crop_data()
        
        for crop_id, crop_data in crops.items():
            self.assertGreater(
                crop_data["seed_price"], 0,
                f"作物 {crop_id} 种子价格无效"
            )
            self.assertGreater(
                crop_data["sell_price"], 0,
                f"作物 {crop_id} 出售价格无效"
            )
            self.assertGreater(
                crop_data["sell_price"], crop_data["seed_price"],
                f"作物 {crop_id} 售价应该高于种子价格"
            )
    
    def test_crop_grow_days_valid(self):
        """测试作物生长天数有效性"""
        crops = self.loader.get_crop_data()
        
        for crop_id, crop_data in crops.items():
            grow_days = crop_data["grow_days"]
            self.assertGreater(
                grow_days, 0,
                f"作物 {crop_id} 生长天数无效"
            )
            self.assertLessEqual(
                grow_days, 30,
                f"作物 {crop_id} 生长天数过长"
            )
    
    def test_achievement_data_structure(self):
        """测试成就数据结构完整性"""
        achievements = self.loader.get_achievement_data()
        
        required_fields = [
            "name", "description", "condition", "reward_text"
        ]
        
        for ach_id, ach_data in achievements.items():
            for field in required_fields:
                self.assertIn(
                    field, ach_data,
                    f"成就 {ach_id} 缺少字段 {field}"
                )
    
    def test_achievement_condition_format(self):
        """测试成就条件格式"""
        achievements = self.loader.get_achievement_data()
        
        for ach_id, ach_data in achievements.items():
            condition = ach_data["condition"]
            # 条件应该包含比较运算符
            self.assertTrue(
                ">=" in condition or "==" in condition,
                f"成就 {ach_id} 条件格式不正确：{condition}"
            )


class TestJSONFileValidity(unittest.TestCase):
    """测试 JSON 文件有效性"""
    
    def test_crops_json_valid(self):
        """测试 crops.json 文件格式"""
        json_path = Path(__file__).parent.parent / "data" / "crops.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn("crops", data)
        self.assertIsInstance(data["crops"], dict)
    
    def test_achievements_json_valid(self):
        """测试 achievements.json 文件格式"""
        json_path = Path(__file__).parent.parent / "data" / "achievements.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn("achievements", data)
        self.assertIsInstance(data["achievements"], dict)


if __name__ == '__main__':
    unittest.main()
