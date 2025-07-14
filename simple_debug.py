#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet

def simple_test():
    try:
        wallet = load_wallet("555.dat")
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        
        # 直接使用钱包的验证方法
        result, count = wallet.return_verified_password_or_false(["123"])
        print(f"验证结果: {result}")
        print(f"测试密码数: {count}")
        
        if result:
            print("✅ 密码正确！")
        else:
            print("❌ 密码错误！")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    simple_test() 