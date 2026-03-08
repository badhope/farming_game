"""
测试运行脚本
用于快速运行所有单元测试
"""

import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_all_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 发现并添加所有测试
    test_dir = project_root / "tests"
    tests = loader.discover(str(test_dir), pattern="test_*.py")
    suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(
        verbosity=2,
        descriptions=True,
        failfast=False,
    )
    
    print("\n" + "=" * 70)
    print("🧪 开始运行单元测试")
    print("=" * 70 + "\n")
    
    result = runner.run(suite)
    
    # 打印统计信息
    print("\n" + "=" * 70)
    print("📊 测试统计")
    print("=" * 70)
    print(f"运行测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    print(f"跳过：{len(result.skipped)}")
    print("=" * 70 + "\n")
    
    # 返回退出码
    if result.wasSuccessful():
        print("✅ 所有测试通过！")
        return 0
    else:
        print("❌ 有测试失败或出错")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
