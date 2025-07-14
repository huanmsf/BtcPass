#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet

def test_password_variants():
    try:
        wallet = load_wallet("wallet.dat")
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        print("=" * 50)
        
        # 测试不同的密码变体
        password_variants = [
            "12345678",
            "12345678 ",  # 带空格
            " 12345678",  # 前面空格
            "12345678\n",  # 带换行
            "12345678\r",  # 带回车
            "12345678\t",  # 带制表符
            "12345678",    # 重新测试原密码
        ]
        
        for i, password in enumerate(password_variants, 1):
            print(f"[{i:2d}/{len(password_variants)}] 测试: '{repr(password)}'", end=" ")
            
            result, count = wallet.return_verified_password_or_false([password])
            
            if result:
                print("✅ 找到正确密码！")
                print(f"🎉 密码是: {repr(result)}")
                return True
            else:
                print("❌")
                
        print("\n❌ 所有密码变体都测试失败")
        return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    test_password_variants() 