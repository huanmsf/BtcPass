#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet

# 定义 tstr 变量，与主程序保持一致
tstr = str

def test_wallet_password(wallet_file, password):
    try:
        wallet = load_wallet(wallet_file)
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        
        # 测试单个密码
        result, count = wallet.return_verified_password_or_false([password])
        if result:
            print(f"✅ 密码正确: {result}")
            return True
        else:
            print(f"❌ 密码错误: {password}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    wallet_file = "555.dat"
    test_passwords = ["123456", "12345678", "123456789", "1111111111", "1234567890", "123456123456", "2222222222"]
    
    print(f"测试钱包文件: {wallet_file}")
    print("=" * 50)
    
    for password in test_passwords:
        print(f"\n测试密码: {password}")
        if test_wallet_password(wallet_file, password):
            break
    else:
        print("\n❌ 所有密码都测试失败") 