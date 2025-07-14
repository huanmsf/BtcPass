#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def debug_password_file(filename):
    """调试密码文件"""
    print("=" * 60)
    print(f"调试密码文件: {filename}")
    print("=" * 60)
    
    if not os.path.exists(filename):
        print(f"❌ 文件不存在: {filename}")
        return
    
    # 文件基本信息
    file_size = os.path.getsize(filename)
    print(f"文件大小: {file_size} 字节")
    
    # 读取文件内容
    with open(filename, 'rb') as f:
        content = f.read()
    
    # 检查编码
    print(f"文件编码检测:")
    try:
        decoded = content.decode('utf-8')
        print("  ✅ UTF-8编码")
    except UnicodeDecodeError:
        try:
            decoded = content.decode('gbk')
            print("  ✅ GBK编码")
        except UnicodeDecodeError:
            print("  ❌ 未知编码")
            return
    
    # 检查行结束符
    lines = decoded.split('\n')
    print(f"总行数: {len(lines)}")
    
    # 检查每行的格式
    print("\n所有行内容:")
    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            print(f"  {i+1}: '{line}' (长度: {len(line)})")
    
    # 检查是否包含目标密码
    target_password = "123456"
    found_positions = []
    for i, line in enumerate(lines):
        if line.strip() == target_password:
            found_positions.append(i+1)
    
    if found_positions:
        print(f"\n✅ 找到目标密码 '{target_password}' 在以下行: {found_positions}")
    else:
        print(f"\n❌ 未找到目标密码 '{target_password}'")
        
        # 检查相似密码
        similar = []
        for i, line in enumerate(lines):
            line = line.strip()
            if target_password in line or line in target_password:
                similar.append((i+1, line))
        
        if similar:
            print(f"找到相似密码:")
            for line_num, password in similar:
                print(f"  第{line_num}行: '{password}'")
    
    # 检查特殊字符
    print(f"\n检查特殊字符:")
    special_chars = set()
    for line in lines:
        for char in line:
            if ord(char) > 127:
                special_chars.add(char)
    
    if special_chars:
        print(f"发现特殊字符: {special_chars}")
    else:
        print("未发现特殊字符")
    
    # 检查行结束符类型
    if '\r\n' in decoded:
        print("行结束符: Windows (CRLF)")
    elif '\r' in decoded:
        print("行结束符: Mac (CR)")
    else:
        print("行结束符: Unix (LF)")
    
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_password_file(sys.argv[1])
    else:
        debug_password_file("pass.txt") 