"""
API 集成测试
测试后端 API 的完整功能流程
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """测试健康检查接口"""
    
    def test_health_check(self):
        """测试健康检查返回正确状态"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestGameLifecycle:
    """测试游戏生命周期"""
    
    def test_create_game(self):
        """测试创建新游戏"""
        response = client.post(
            "/api/player/create",
            json={"player_name": "测试玩家", "difficulty": "normal"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "state" in data
        assert data["state"]["player_name"] == "测试玩家"
    
    def test_get_player_info(self):
        """测试获取玩家信息"""
        client.post("/api/player/create", json={"player_name": "测试"})
        response = client.get("/api/player/info")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "gold" in data
        assert "level" in data
    
    def test_get_game_status(self):
        """测试获取游戏状态"""
        client.post("/api/player/create", json={"player_name": "测试"})
        response = client.get("/api/game/status")
        assert response.status_code == 200
        data = response.json()
        assert data["has_game"] is True


class TestFarmingOperations:
    """测试农场操作"""
    
    @pytest.fixture(autouse=True)
    def setup_game(self):
        """每个测试前创建新游戏"""
        client.post("/api/player/create", json={"player_name": "农民"})
    
    def test_get_plots(self):
        """测试获取农田列表"""
        response = client.get("/api/farm/plots")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_available_crops(self):
        """测试获取可种植作物"""
        response = client.get("/api/farm/crops")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_plant_crop(self):
        """测试种植作物"""
        response = client.post(
            "/api/farm/plant",
            json={"row": 0, "col": 0, "crop_name": "胡萝卜"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_plant_invalid_crop(self):
        """测试种植不存在的作物"""
        response = client.post(
            "/api/farm/plant",
            json={"row": 0, "col": 0, "crop_name": "不存在的作物"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
    
    def test_water_crop(self):
        """测试浇水"""
        client.post("/api/farm/plant", json={"row": 0, "col": 0, "crop_name": "胡萝卜"})
        response = client.post("/api/farm/water", json={"row": 0, "col": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_harvest_crop(self):
        """测试收获作物（需要先种植多天）"""
        client.post("/api/farm/plant", json={"row": 0, "col": 0, "crop_name": "胡萝卜"})
        for _ in range(5):
            client.post("/api/farm/water", json={"row": 0, "col": 0})
            client.post("/api/game/advance_day")
        
        response = client.post("/api/farm/harvest", json={"row": 0, "col": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestShopOperations:
    """测试商店功能"""
    
    @pytest.fixture(autouse=True)
    def setup_game(self):
        """每个测试前创建新游戏"""
        client.post("/api/player/create", json={"player_name": "商人", "difficulty": "easy"})
    
    def test_get_shop_items(self):
        """测试获取商店物品列表"""
        response = client.get("/api/shop/items")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_buy_item(self):
        """测试购买物品"""
        response = client.post(
            "/api/shop/buy",
            json={"item_id": "fertilizer_basic", "quantity": 1}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_buy_insufficient_funds(self):
        """测试金币不足时购买"""
        client.post("/api/player/create", json={"player_name": "穷鬼", "difficulty": "hard"})
        response = client.post(
            "/api/shop/buy",
            json={"item_id": "greenhouse", "quantity": 1}
        )
        assert response.status_code == 400
    
    def test_get_shop_history(self):
        """测试获取购买历史"""
        client.post("/api/shop/buy", json={"item_id": "fertilizer_basic", "quantity": 1})
        response = client.get("/api/shop/history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert len(data["history"]) > 0


class TestTimeSystem:
    """测试时间系统"""
    
    @pytest.fixture(autouse=True)
    def setup_game(self):
        """每个测试前创建新游戏"""
        client.post("/api/player/create", json={"player_name": "时间测试"})
    
    def test_advance_day(self):
        """测试时间推进"""
        response = client.post("/api/game/advance_day")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_time_status(self):
        """测试获取时间状态"""
        response = client.get("/api/farm/time")
        assert response.status_code == 200
        data = response.json()
        assert "season" in data
        assert "day" in data
        assert "year" in data
        assert "weather" in data


class TestSaveLoad:
    """测试存档功能"""
    
    @pytest.fixture(autouse=True)
    def setup_game(self):
        """每个测试前创建新游戏"""
        client.post("/api/player/create", json={"player_name": "存档测试"})
    
    def test_save_game(self):
        """测试保存游戏"""
        response = client.post(
            "/api/game/save",
            json={"save_name": "test_save"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_load_game(self):
        """测试加载游戏"""
        client.post("/api/game/save", json={"save_name": "test_load"})
        response = client.post(
            "/api/game/load",
            json={"save_name": "test_load"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_list_saves(self):
        """测试获取存档列表"""
        client.post("/api/game/save", json={"save_name": "list_test"})
        response = client.get("/api/game/saves")
        assert response.status_code == 200
        data = response.json()
        assert "saves" in data
        assert "count" in data


class TestErrorHandling:
    """测试错误处理"""
    
    def test_no_game_error(self):
        """测试没有游戏时的错误处理"""
        response = client.get("/api/farm/plots")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_invalid_load(self):
        """测试加载不存在的存档"""
        response = client.post(
            "/api/game/load",
            json={"save_name": "nonexistent_save_file"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
