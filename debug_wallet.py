#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet
import hashlib

def debug_wallet_password(wallet_file, password):
    try:
        wallet = load_wallet(wallet_file)
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        
        # 打印钱包内部信息
        print(f"Salt: {wallet._salt.hex()}")
        print(f"Iteration count: {wallet._iter_count}")
        print(f"Part encrypted master key: {wallet._part_encrypted_master_key.hex()}")
        
        # 手动验证密码过程
        print(f"\n手动验证密码: {password}")
        
        # 步骤1: 密码 + salt
        derived_key = password.encode('utf-8') + wallet._salt
        print(f"步骤1 - 密码+salt: {derived_key.hex()}")
        
        # 步骤2: SHA-512 迭代
        for i in range(wallet._iter_count):
            derived_key = hashlib.sha512(derived_key).digest()
            if i < 3 or i >= wallet._iter_count - 3:  # 只显示前3次和后3次
                print(f"步骤2.{i+1} - SHA-512迭代: {derived_key.hex()}")
            elif i == 3:
                print(f"... (省略中间 {wallet._iter_count - 6} 次迭代) ...")
        
        # 步骤3: 尝试解密
        from btcrecover.btcrpass import aes256_cbc_decrypt
        try:
            part_master_key = aes256_cbc_decrypt(
                derived_key[:32], 
                wallet._part_encrypted_master_key[:16], 
                wallet._part_encrypted_master_key[16:]
            )
            print(f"步骤3 - 解密结果: {part_master_key.hex()}")
            
            # 检查PKCS7填充
            expected_padding = b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"
            if part_master_key == expected_padding:
                print("✅ 密码正确！PKCS7填充验证成功")
                return True
            else:
                print(f"❌ 密码错误！期望填充: {expected_padding.hex()}")
                print(f"   实际填充: {part_master_key.hex()}")
                return False
                
        except Exception as e:
            print(f"❌ 解密失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    wallet_file = "555.dat"
    password = "12345678"
    
    print(f"调试钱包文件: {wallet_file}")
    print("=" * 60)
    
    debug_wallet_password(wallet_file, password) 