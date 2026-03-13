#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
中国百万富翁 - 文字模拟经营游戏
版本：0.1.0
作者：独立开发者
"""

import sys
from core.game import ChineseMillionaireGame


def main():
    """游戏入口"""
    print("=" * 60)
    print("        中国百万富翁 v0.1.0")
    print("        你的致富之路，从这里开始！")
    print("=" * 60)
    print()
    
    try:
        game = ChineseMillionaireGame()
        game.start()
    except KeyboardInterrupt:
        print("\n\n游戏已退出。欢迎下次再来！")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 游戏发生错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
