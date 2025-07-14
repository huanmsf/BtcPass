#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, '.')

def debug_gpu_flow():
    """调试GPU破解流程中的密码处理"""
    
    print("=== GPU破解流程调试 ===")
    
    # 读取密码文件
    with open('pass.txt', 'r', encoding='utf-8') as f:
        passwords = [line.strip() for line in f.readlines()]
    
    print(f"密码文件中的密码: {passwords}")
    
    # 模拟GPU流程中的密码处理
    for i, password in enumerate(passwords):
        print(f"\n处理密码 {i+1}: '{password}'")
        
        # 原始字符串
        print(f"  原始类型: {type(password)}")
        print(f"  原始值: {repr(password)}")
        
        # 转换为bytes (模拟GPU处理)
        try:
            password_bytes = password.encode('utf-8')
            print(f"  转换为bytes: {password_bytes}")
            print(f"  bytes类型: {type(password_bytes)}")
            
            # 检查是否为空
            if len(password_bytes) == 0:
                print(f"  ⚠️  警告: 密码转换为bytes后为空")
            
            # 检查长度
            print(f"  bytes长度: {len(password_bytes)}")
            
            # 转换回字符串
            password_back = password_bytes.decode('utf-8')
            print(f"  转换回字符串: {repr(password_back)}")
            
            # 检查是否一致
            if password == password_back:
                print(f"  ✓ 转换前后一致")
            else:
                print(f"  ✗ 转换前后不一致!")
                
        except Exception as e:
            print(f"  ✗ 转换失败: {e}")
        
        # 检查特殊字符
        if any(ord(c) > 127 for c in password):
            print(f"  ⚠️  包含非ASCII字符")
        
        # 检查空白字符
        if password.strip() != password:
            print(f"  ⚠️  包含空白字符")

if __name__ == "__main__":
    debug_gpu_flow() 