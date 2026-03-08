"""
农耕系统单元测试
测试种植、浇水、收获等核心功能
"""

import unittest
from models.farming_system import (
    FarmingManager, FarmField, PlantedCrop, CropInfo, CropRegistry,
    CropStage, CropQuality
)
from config.enums import CropType


class TestCropInfo(unittest.TestCase):
    """测试作物信息类"""
    
    def test_crop_creation(self):
        """测试作物创建"""
        crop = CropInfo(
            crop_id="test_crop",
            name="测试作物",
            icon="🌱",
            description="测试",
            seed_price=50,
            base_sell_price=120,
            grow_days=3,
        )
        
        self.assertEqual(crop.name, "测试作物")
        self.assertEqual(crop.seed_price, 50)
        self.assertEqual(crop.grow_days, 3)
    
    def test_crop_from_config(self):
        """测试从配置创建作物"""
        config = {
            "name": "土豆",
            "seed_price": 50,
            "sell_price": 120,
            "grow_days": 3,
            "seasons": ["SPRING", "AUTUMN"],
            "water_needed": 1,
            "emoji": "🥔",
        }
        
        crop = CropInfo.from_config("potato", config)
        
        self.assertEqual(crop.crop_id, "potato")
        self.assertEqual(crop.name, "土豆")
        self.assertEqual(crop.seed_price, 50)
        self.assertIn("SPRING", crop.seasons)


class TestPlantedCrop(unittest.TestCase):
    """测试已种植作物"""
    
    def setUp(self):
        """准备测试数据"""
        self.crop_info = CropInfo(
            crop_id="test",
            name="测试",
            icon="🌱",
            description="test",
            grow_days=3,
            water_per_day=1,
            base_yield=3,
        )
    
    def test_plant_crop(self):
        """测试种植作物"""
        planted = PlantedCrop(crop_info=self.crop_info, planted_day=1)
        
        self.assertEqual(planted.current_stage, CropStage.SEED)
        self.assertEqual(planted.days_grown, 0)
        self.assertTrue(planted.health > 0)
    
    def test_water_crop(self):
        """测试浇水"""
        planted = PlantedCrop(crop_info=self.crop_info)
        
        planted.water(1)
        self.assertEqual(planted.water_level, 1)
        
        planted.water(2)
        self.assertEqual(planted.water_level, 3)  # 最大值
    
    def test_advance_day_with_water(self):
        """测试作物生长（有浇水）"""
        planted = PlantedCrop(crop_info=self.crop_info)
        
        # 模拟 3 天的生长
        for day in range(3):
            planted.water(1)
            result = planted.advance_day({"growth": 1.0}, "SPRING")
        
        # 应该成熟了
        self.assertEqual(planted.current_stage, CropStage.MATURE)
        self.assertTrue(result["harvestable"])
    
    def test_advance_day_without_water(self):
        """测试作物生长（未浇水）"""
        planted = PlantedCrop(crop_info=self.crop_info)
        
        # 不浇水，生长会变慢
        result = planted.advance_day({"growth": 1.0}, "SPRING")
        
        # 健康度应该下降
        self.assertLess(planted.health, 100)
    
    def test_harvest_mature_crop(self):
        """测试收获成熟作物"""
        planted = PlantedCrop(crop_info=self.crop_info)
        
        # 直接设置为成熟
        planted.current_stage = CropStage.MATURE
        
        success, amount, quality, message = planted.harvest()
        
        self.assertTrue(success)
        self.assertGreater(amount, 0)
        self.assertIn("收获了", message)
    
    def test_harvest_immature_crop(self):
        """测试收获未成熟作物"""
        planted = PlantedCrop(crop_info=self.crop_info)
        
        success, amount, quality, message = planted.harvest()
        
        self.assertFalse(success)
        self.assertIn("还未成熟", message)


class TestFarmField(unittest.TestCase):
    """测试农田地块"""
    
    def test_field_is_empty(self):
        """测试地块是否为空"""
        field = FarmField(row=0, col=0)
        
        self.assertTrue(field.is_empty())
    
    def test_plant_in_field(self):
        """测试在地块种植"""
        field = FarmField(row=0, col=0)
        crop_info = CropInfo(
            crop_id="test", name="测试", icon="🌱", 
            description="test", grow_days=3
        )
        
        field.plant(crop_info, day=1)
        
        self.assertFalse(field.is_empty())
        self.assertIsNotNone(field.planted_crop)
    
    def test_cannot_plant_occupied_field(self):
        """测试不能在已有作物的地块种植"""
        field = FarmField(row=0, col=0)
        crop_info = CropInfo(
            crop_id="test", name="测试", icon="🌱",
            description="test", grow_days=3
        )
        
        field.plant(crop_info, day=1)
        
        with self.assertRaises(ValueError):
            field.plant(crop_info, day=2)
    
    def test_water_field(self):
        """测试浇水"""
        field = FarmField(row=0, col=0)
        crop_info = CropInfo(
            crop_id="test", name="测试", icon="🌱",
            description="test", grow_days=3
        )
        
        field.plant(crop_info, day=1)
        field.water()
        
        self.assertTrue(field.is_watered)
        self.assertEqual(field.planted_crop.water_level, 1)
    
    def test_harvest_field(self):
        """测试收获"""
        field = FarmField(row=0, col=0)
        crop_info = CropInfo(
            crop_id="test", name="测试", icon="🌱",
            description="test", grow_days=3, base_yield=3
        )
        
        field.plant(crop_info, day=1)
        field.planted_crop.current_stage = CropStage.MATURE
        
        success, amount, quality, message = field.harvest()
        
        self.assertTrue(success)
        self.assertTrue(field.is_empty())  # 收获后应该为空
        self.assertFalse(field.is_watered)


class TestFarmingManager(unittest.TestCase):
    """测试农耕管理器"""
    
    def setUp(self):
        """准备测试数据"""
        self.manager = FarmingManager()
    
    def test_plant_crop(self):
        """测试种植作物"""
        # 先注册一个测试作物
        test_crop = CropInfo(
            crop_id="test_potato",
            name="测试土豆",
            icon="🥔",
            description="test",
            seed_price=50,
            base_sell_price=120,
            grow_days=3,
            seasons=["SPRING"],
        )
        CropRegistry._crops["test_potato"] = test_crop
        CropRegistry._initialized = True
        
        success, message = self.manager.plant_crop(0, 0, "test_potato", day=1)
        
        self.assertTrue(success)
        self.assertIn("种植了", message)
    
    def test_water_crop(self):
        """测试浇水"""
        field = self.manager.get_or_create_field(0, 0)
        crop_info = CropInfo(
            crop_id="test", name="测试", icon="🌱",
            description="test", grow_days=3
        )
        field.plant(crop_info, day=1)
        
        success, message = self.manager.water_crop(0, 0)
        
        self.assertTrue(success)
    
    def test_get_mature_fields(self):
        """测试获取成熟地块"""
        field = self.manager.get_or_create_field(0, 0)
        crop_info = CropInfo(
            crop_id="test", name="测试", icon="🌱",
            description="test", grow_days=3
        )
        field.plant(crop_info, day=1)
        field.planted_crop.current_stage = CropStage.MATURE
        
        mature_fields = self.manager.get_mature_fields()
        
        self.assertEqual(len(mature_fields), 1)
    
    def test_harvest_count_tracking(self):
        """测试收获计数"""
        field = self.manager.get_or_create_field(0, 0)
        crop_info = CropInfo(
            crop_id="test", name="测试", icon="🌱",
            description="test", grow_days=3, base_yield=3
        )
        field.plant(crop_info, day=1)
        field.planted_crop.current_stage = CropStage.MATURE
        
        initial_count = self.manager.harvest_count
        self.manager.harvest_crop(0, 0)
        
        self.assertEqual(self.manager.harvest_count, initial_count + 1)


class TestCropRegistry(unittest.TestCase):
    """测试作物注册表"""
    
    def test_get_crop(self):
        """测试获取作物"""
        # 手动注册一个测试作物
        test_crop = CropInfo(
            crop_id="registry_test",
            name="注册测试",
            icon="🌱",
            description="test",
            grow_days=1,
        )
        CropRegistry._crops["registry_test"] = test_crop
        CropRegistry._initialized = True
        
        crop = CropRegistry.get_crop("registry_test")
        
        self.assertIsNotNone(crop)
        self.assertEqual(crop.name, "注册测试")
    
    def test_get_nonexistent_crop(self):
        """测试获取不存在的作物"""
        crop = CropRegistry.get_crop("nonexistent")
        
        self.assertIsNone(crop)


if __name__ == '__main__':
    unittest.main()
