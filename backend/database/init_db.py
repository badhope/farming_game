"""
数据库初始化脚本
创建所有表并初始化数据
"""

from backend.database.db_config import engine, Base
from backend.models.db_models import PlayerModel, InventoryModel, FarmFieldModel, GameSaveModel, AchievementModel


def init_db():
    """初始化数据库"""
    print("正在初始化数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print("✅ 数据库表创建成功！")
    print(f"数据库文件：farming_game.db")


if __name__ == "__main__":
    init_db()
