#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import hashlib
import struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet

def debug_algorithm():
    """详细调试 Bitcoin Core 破解算法"""
    try:
        wallet = load_wallet("wallet.dat")
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
        print(f"测试密码: '{test_password}'")
        print(f"密码字节: {test_password.encode('utf-8').hex()}")
        
        # 步骤1: 密码 + salt
        derived_key = test_password.encode('utf-8') + salt
        print(f"步骤1 - 密码+salt: {derived_key.hex()}")
        
        # 步骤2: SHA-512 迭代 (只做前几次和后几次)
        print(f"步骤2 - 开始 SHA-512 迭代...")
        
        # 前3次迭代
        for i in range(3):
            derived_key = hashlib.sha512(derived_key).digest()
            print(f"  迭代 {i+1:6d}: {derived_key.hex()}")
        
        # 中间跳过
        print(f"  ... (跳过中间 {iter_count - 6} 次迭代) ...")
        
        # 最后3次迭代
        for i in range(iter_count - 3, iter_count):
            derived_key = hashlib.sha512(derived_key).digest()
            print(f"  迭代 {i+1:6d}: {derived_key.hex()}")
        
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
            print(f"期望填充: {expected_padding.hex()}")
            
            if decrypted == expected_padding:
                print("✅ 算法验证成功！密码正确")
                return True
            else:
                print(f"❌ 算法验证失败！")
                print(f"   期望: {expected_padding.hex()}")
                print(f"   实际: {decrypted.hex()}")
                
                # 分析差异
                print(f"   差异分析:")
                for i, (exp, act) in enumerate(zip(expected_padding, decrypted)):
                    if exp != act:
                        print(f"     字节 {i}: 期望 {exp:02x}, 实际 {act:02x}")
                
                return False
                
        except Exception as e:
            print(f"❌ 解密失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def compare_with_official():
    """对比官方算法描述"""
    print("\n" + "=" * 60)
    print("Bitcoin Core 官方算法分析")
    print("=" * 60)
    
    print("根据 Bitcoin Core 源码，钱包加密算法应该是：")
    print("1. 密码 + salt (UTF-8编码)")
    print("2. SHA-512 迭代 N 次")
    print("3. 取前32字节作为 AES-256-CBC 密钥")
    print("4. 解密主密钥的最后32字节")
    print("5. 验证 PKCS7 填充 (16字节的 0x10)")
    print()
    
    print("可能的问题：")
    print("1. 密码编码方式不同")
    print("2. 迭代次数计算错误")
    print("3. AES 解密实现问题")
    print("4. 钱包文件格式解析错误")
    print("5. 版本兼容性问题")

if __name__ == "__main__":
    debug_algorithm()
    compare_with_official() 