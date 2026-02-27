"""
游戏主入口文件
文字农场 - Python控制台版
"""

import sys
import time
import os

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import GameManager
from systems import SaveManager, DisplayManager
from config.settings import GameConfig


class Game:
    """
    游戏主类
    
    管理游戏的主循环和用户交互
    """
    
    def __init__(self):
        """初始化游戏"""
        self.manager = GameManager()
        self.save_manager = SaveManager()
        self.display = DisplayManager(self.manager)
        self.running = True
    
    def start(self) -> None:
        """启动游戏"""
        # 尝试加载存档
        self._check_save_file()
        
        # 进入主循环
        self._main_loop()
    
    def _check_save_file(self) -> None:
        """检查并存档文件"""
        if self.save_manager.has_save():
            print("\n" + "=" * 50)
            print("🔍 检测到存档文件！")
            
            info = self.save_manager.get_save_info()
            if info:
                print(f"   存档时间: {info['timestamp']}")
                print(f"   农夫: {info['player_name']}")
                print(f"   进度: 第{info['year']}年 {info['season']} 第{info['day']}天")
                print(f"   金币: {info['money']}")
            
            print("=" * 50)
            choice = input("是否读取存档？(y/n): ").strip().lower()
            
            if choice == 'y':
                if self.save_manager.load_game(self.manager):
                    # 加载成功后，需要同步显示管理器的游戏引用（如果需要）
                    # 这里因为DisplayManager持有manager引用，数据已更新，无需额外操作
                    print("✅ 存档加载成功！")
                    time.sleep(1)
                else:
                    print("❌ 存档加载失败，开始新游戏。")
                    time.sleep(1)
    
    def _main_loop(self) -> None:
        """游戏主循环"""
        while self.running:
            # 获取新消息（如成就解锁等）
            messages = self.manager.get_new_messages()
            
            # 渲染界面
            self.display.render_frame(messages)
            
            # 获取用户输入
            choice = self.display.show_input_prompt("请选择操作")
            
            # 处理输入
            self._handle_input(choice)
    
    def _handle_input(self, choice: str) -> None:
        """
        处理用户输入
        
        Args:
            choice: 用户输入的选项
        """
        if choice == '1':
            self._handle_plant()
        elif choice == '2':
            self._handle_water()
        elif choice == '3':
            self._handle_harvest()
        elif choice == '4':
            self._handle_shop()
        elif choice == '5':
            self._handle_sell()
        elif choice == '6':
            self._handle_sleep()
        elif choice == '7':
            self._handle_details()
        elif choice == '8':
            self._handle_achievements()
        elif choice == '9':
            self._handle_save()
        elif choice == '0':
            self._handle_exit()
        else:
            print("\n⚠️ 无效的选项，请重新输入！")
            time.sleep(1)
    
    # ========== 功能处理方法 ==========
    
    def _handle_plant(self) -> None:
        """处理种植逻辑"""
        while True:
            self.display.show_plant_menu()
            user_input = self.display.show_input_prompt("输入坐标和作物名")
            
            if user_input == '0':
                break
            
            # 解析输入
            parts = user_input.split()
            if len(parts) != 3:
                print("\n⚠️ 输入格式错误！示例: 0 0 土豆")
                time.sleep(1)
                continue
            
            try:
                row = int(parts[0])
                col = int(parts[1])
                crop_name = parts[2]
                
                success, msg = self.manager.plant_crop(row, col, crop_name)
                print(f"\n{msg}")
                time.sleep(1)
                
                if success:
                    # 种植成功后刷新界面，让用户决定是否继续
                    pass
                    
            except ValueError:
                print("\n⚠️ 坐标必须是数字！")
                time.sleep(1)
    
    def _handle_water(self) -> None:
        """处理浇水逻辑"""
        # 如果下雨，自动跳过
        if self.manager.time_system.is_rainy():
            print("\n🌧️ 今天下雨，无需浇水！")
            time.sleep(1)
            return
        
        print("\n💧 正在给所有作物浇水...")
        success_count, _ = self.manager.water_all_plots()
        
        if success_count > 0:
            print(f"✅ 成功给 {success_count} 块地浇水！")
        else:
            print("💧 没有需要浇水的作物。")
        
        time.sleep(1)
    
    def _handle_harvest(self) -> None:
        """处理收获逻辑"""
        print("\n🌾 正在收获所有成熟的作物...")
        
        count, messages = self.manager.harvest_all_mature()
        
        if count > 0:
            print(f"🎉 收获了 {count} 个作物！")
        else:
            print("🍂 没有成熟的作物可以收获。")
        
        time.sleep(1)
    
    def _handle_shop(self) -> None:
        """处理商店逻辑"""
        while True:
            self.display.show_shop_menu()
            choice = self.display.show_input_prompt("选择要购买的种子编号")
            
            if choice == '0':
                break
            
            try:
                crops = self.manager.economy_system.get_all_crops()
                idx = int(choice) - 1
                
                if 0 <= idx < len(crops):
                    crop = crops[idx]
                    amount = self.display.show_input_prompt(f"购买 {crop.name} 的数量")
                    
                    try:
                        quantity = int(amount)
                        if quantity > 0:
                            success, msg = self.manager.buy_seeds(crop.name, quantity)
                            print(f"\n{msg}")
                        else:
                            print("\n⚠️ 数量必须大于0！")
                    except ValueError:
                        print("\n⚠️ 请输入有效的数字！")
                else:
                    print("\n⚠️ 无效的编号！")
                
                time.sleep(1)
                
            except ValueError:
                print("\n⚠️ 请输入数字编号！")
                time.sleep(1)
    
    def _handle_sell(self) -> None:
        """处理出售逻辑"""
        while True:
            self.display.show_sell_menu()
            user_input = self.display.show_input_prompt("输入作物名和数量")
            
            if user_input == '0':
                break
            
            parts = user_input.split()
            if len(parts) < 2:
                print("\n⚠️ 输入格式错误！示例: 土豆 5 或 土豆 all")
                time.sleep(1)
                continue
            
            crop_name = parts[0]
            amount_str = parts[1]
            
            try:
                if amount_str.lower() == 'all':
                    # 出售全部
                    results = self.manager.sell_all_crops()
                    for success, msg in results:
                        print(msg)
                else:
                    quantity = int(amount_str)
                    success, msg = self.manager.sell_crop(crop_name, quantity)
                    print(f"\n{msg}")
                
                time.sleep(1)
                
            except ValueError:
                print("\n⚠️ 数量必须是数字或 'all'！")
                time.sleep(1)
    
    def _handle_sleep(self) -> None:
        """处理睡觉（推进时间）逻辑"""
        print("\n🛏️ 结束了一天，准备睡觉...")
        time.sleep(1)
        
        # 推进时间
        result = self.manager.advance_day()
        
        # 显示结果
        print(f"\n{'='*50}")
        print(f"🌞 第{result.day}天 - {result.season} - {result.weather}")
        print(f"{'='*50}")
        
        if result.events:
            print("📜 今日事件:")
            for event in result.events:
                print(f"   {event}")
        
        if result.crops_matured > 0:
            print(f"\n🌿 有 {result.crops_matured} 个作物成熟了！")
        
        if result.crops_died > 0 or result.crops_destroyed > 0:
            print(f"\n💀 损失了 {result.crops_died + result.crops_destroyed} 个作物。")
        
        print(f"\n{'='*50}")
        
        input("\n按回车键继续...")
    
    def _handle_details(self) -> None:
        """处理详情查看逻辑"""
        while True:
            self.display.show_detail_menu()
            choice = self.display.show_input_prompt("选择查看内容")
            
            if choice == '0':
                break
            elif choice == '1':
                name = self.display.show_input_prompt("输入作物名称")
                self.display.show_crop_detail(name)
                input("\n按回车键返回...")
            elif choice == '2':
                try:
                    coord = self.display.show_input_prompt("输入坐标(行 列)")
                    parts = coord.split()
                    if len(parts) == 2:
                        row, col = int(parts[0]), int(parts[1])
                        self.display.show_plot_status(row, col)
                    else:
                        print("⚠️ 格式错误，请输入: 行 列")
                except ValueError:
                    print("⚠️ 请输入数字！")
                input("\n按回车键返回...")
            elif choice == '3':
                self.display.show_statistics()
                input("\n按回车键返回...")
    
    def _handle_achievements(self) -> None:
        """处理成就查看逻辑"""
        self.display.show_achievements()
        input("\n按回车键返回...")
    
    def _handle_save(self) -> None:
        """处理存档逻辑"""
        print("\n💾 正在保存游戏...")
        
        if self.save_manager.save_game(self.manager):
            print("✅ 游戏保存成功！")
        else:
            print("❌ 游戏保存失败！")
        
        time.sleep(1)
    
    def _handle_exit(self) -> None:
        """处理退出逻辑"""
        print("\n⚠️ 确定要退出游戏吗？")
        confirm = input("输入 'y' 确认退出，输入其他返回游戏: ").strip().lower()
        
        if confirm == 'y':
            # 询问是否保存
            print("\n💾 退出前是否保存游戏？")
            save_choice = input("输入 'y' 保存，输入其他直接退出: ").strip().lower()
            
            if save_choice == 'y':
                self.save_manager.save_game(self.manager)
            
            self.display.show_goodbye()
            self.running = False


def main():
    """主函数入口"""
    # 设置控制台标题（Windows系统）
    if sys.platform == 'win32':
        os.system('title 文字农场 - Python版')
    
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
