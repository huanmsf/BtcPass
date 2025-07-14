#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, '.')

from btcrecover import btcrpass

def debug_gpu_password():
    """调试GPU破解过程中的密码处理"""
    
    # 测试密码
    test_passwords = ['12345678', '123456', '1234567890']
    
    print("=== GPU密码处理调试 ===")
    
    for password in test_passwords:
        print(f"\n测试密码: {password}")
        print(f"类型: {type(password)}")
        print(f"长度: {len(password)}")
        
        # 转换为bytes
        password_bytes = password.encode('utf-8')
        print(f"转换为bytes: {password_bytes}")
        print(f"bytes类型: {type(password_bytes)}")
        print(f"bytes长度: {len(password_bytes)}")
        
        # 检查是否在pass.txt中
        with open('pass.txt', 'r', encoding='utf-8') as f:
            passwords_in_file = [line.strip() for line in f.readlines()]
        
        if password in passwords_in_file:
            print(f"✓ 密码在pass.txt中找到")
        else:
            print(f"✗ 密码不在pass.txt中")
        
        # 检查密码变体
        variants = []
        if password.isdigit():
            variants.append(password)
        if len(password) >= 6:
            variants.append(password[:6])
        if len(password) >= 8:
            variants.append(password[:8])
        
        print(f"可能的变体: {variants}")
        
        for variant in variants:
            if variant in passwords_in_file:
                print(f"  ✓ 变体 '{variant}' 在pass.txt中")
            else:
                print(f"  ✗ 变体 '{variant}' 不在pass.txt中")

if __name__ == "__main__":
    debug_gpu_password() 