#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet

def batch_test():
    try:
        wallet = load_wallet("555.dat")
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        print("=" * 50)
        
        # 常见密码列表
        common_passwords = [
            "123", "1234", "12345", "123456", "1234567", "12345678", "123456789",
            "password", "pass", "pass123", "admin", "admin123",
            "bitcoin", "wallet", "money", "crypto",
            "test", "demo", "sample", "example",
            "a", "aa", "aaa", "aaaa", "aaaaa",
            "1", "11", "111", "1111", "11111",
            "",  # 空密码
        ]
        
        print(f"开始测试 {len(common_passwords)} 个常见密码...")
        
        for i, password in enumerate(common_passwords, 1):
            print(f"[{i:2d}/{len(common_passwords)}] 测试: '{password}'", end=" ")
            
            result, count = wallet.return_verified_password_or_false([password])
            
            if result:
                print("✅ 找到正确密码！")
                print(f"🎉 密码是: {result}")
                return True
            else:
                print("❌")
                
        print("\n❌ 所有常见密码都测试失败")
        return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    batch_test() 