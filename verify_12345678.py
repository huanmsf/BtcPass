#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet

def verify_wallet():
    try:
        wallet = load_wallet("12345678.dat")
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        print("=" * 60)
        
        # 获取钱包参数
        salt = wallet._salt
        iter_count = wallet._iter_count
        part_encrypted_master_key = wallet._part_encrypted_master_key
        
        print(f"Salt (hex): {salt.hex()}")
        print(f"Iteration count: {iter_count}")
        print(f"Part encrypted master key (hex): {part_encrypted_master_key.hex()}")
        print("=" * 60)
        
        # 测试密码
        test_password = "12345678"
        print(f"测试密码: {test_password}")
        
        # 步骤1: 密码 + salt
        derived_key = test_password.encode('utf-8') + salt
        print(f"步骤1 - 密码+salt: {derived_key.hex()}")
        
        # 步骤2: SHA-512 迭代
        print(f"步骤2 - 开始 {iter_count} 次 SHA-512 迭代...")
        for i in range(iter_count):
            derived_key = hashlib.sha512(derived_key).digest()
            if i < 3 or i >= iter_count - 3:  # 显示前3次和后3次
                print(f"  迭代 {i+1:6d}: {derived_key.hex()}")
            elif i == 3:
                print(f"  ... (省略中间 {iter_count - 6} 次迭代) ...")
        
        # 步骤3: 提取前32字节作为AES密钥
        aes_key = derived_key[:32]
        print(f"步骤3 - AES密钥: {aes_key.hex()}")
        
        # 步骤4: 解密
        iv = part_encrypted_master_key[:16]
        ciphertext = part_encrypted_master_key[16:]
        print(f"步骤4 - IV: {iv.hex()}")
        print(f"步骤4 - 密文: {ciphertext.hex()}")
        
        try:
            # 使用钱包内部的解密方法
            from btcrecover.btcrpass import aes256_cbc_decrypt
            decrypted = aes256_cbc_decrypt(aes_key, iv, ciphertext)
            print(f"步骤4 - 解密结果: {decrypted.hex()}")
            
            # 检查PKCS7填充
            expected_padding = b"\x10" * 16  # 16 bytes of 0x10
            if decrypted == expected_padding:
                print("✅ 算法验证成功！密码正确")
                return True
            else:
                print(f"❌ 算法验证失败！期望: {expected_padding.hex()}")
                print(f"   实际: {decrypted.hex()}")
                return False
                
        except Exception as e:
            print(f"❌ 解密失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    verify_wallet() 