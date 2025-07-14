#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet

def test_pass_file():
    try:
        wallet = load_wallet("wallet.dat")
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        print("=" * 50)
        
        # 读取 pass.txt 文件
        with open("pass.txt", "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        print(f"从 pass.txt 读取到 {len(passwords)} 个密码:")
        for i, pwd in enumerate(passwords, 1):
            print(f"  {i}. '{pwd}' (长度: {len(pwd)})")
        print("=" * 50)
        
        # 逐个测试每个密码
        for i, password in enumerate(passwords, 1):
            print(f"[{i:2d}/{len(passwords)}] 测试: '{password}'", end=" ")
            
            result, count = wallet.return_verified_password_or_false([password])
            
            if result:
                print("✅ 找到正确密码！")
                print(f"🎉 密码是: {result}")
                return True
            else:
                print("❌")
                
        print("\n❌ pass.txt 中所有密码都测试失败")
        print("\n建议:")
        print("1. 确认 wallet.dat 文件是否正确")
        print("2. 检查密码是否包含特殊字符")
        print("3. 尝试在 Bitcoin Core 客户端中重新输入密码")
        return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    test_pass_file() 