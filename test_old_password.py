#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet

def test_old_passwords():
    try:
        wallet = load_wallet("555.dat")
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        print("=" * 50)
        
        # 可能的旧密码列表
        old_passwords = [
            "12345678",  # 当前密码
            "123456",    # 可能的旧密码
            "123456789", 
            "1234567890",
            "password",
            "bitcoin",
            "wallet",
            "123",
            "1234",
            "12345",
            "1234567",
            "",  # 空密码
        ]
        
        print(f"测试可能的旧密码...")
        
        for i, password in enumerate(old_passwords, 1):
            print(f"[{i:2d}/{len(old_passwords)}] 测试: '{password}'", end=" ")
            
            result, count = wallet.return_verified_password_or_false([password])
            
            if result:
                print("✅ 找到正确密码！")
                print(f"🎉 密码是: {result}")
                return True
            else:
                print("❌")
                
        print("\n❌ 所有测试密码都失败")
        print("\n建议：")
        print("1. 确认 555.dat 的备份时间")
        print("2. 回忆修改前的密码")
        print("3. 检查文件是否损坏")
        return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    test_old_passwords() 