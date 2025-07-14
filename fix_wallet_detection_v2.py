#!/usr/bin/env python3

# 修复 load_wallet 函数，使其能够自动检测所有支持的钱包类型

def fix_load_wallet_function():
    with open('btcrecover/btcrpass.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到 load_wallet 函数的开始和结束
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith('def load_wallet('):
            start_line = i
        elif start_line is not None and line.strip() == 'raise ValueError("Unknown wallet file type")':
            end_line = i
            break
    
    if start_line is not None and end_line is not None:
        # 替换整个函数
        new_function = [
            'def load_wallet(wallet_filename):\n',
            '    # Try each registered wallet type to see if it can load this file\n',
            '    for wallet_type in wallet_types:\n',
            '        with open(wallet_filename, "rb") as wallet_file:\n',
            '            wallet_file.seek(0)\n',
            '            found = wallet_type.is_wallet_file(wallet_file)\n',
            '            if found:\n',
            '                wallet_file.seek(0)\n',
            '                return wallet_type.load_from_filename(wallet_filename)\n',
            '    raise ValueError("Unknown wallet file type")\n'
        ]
        
        # 替换函数
        lines[start_line:end_line+1] = new_function
        
        # 写回文件
        with open('btcrecover/btcrpass.py', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"成功修复 load_wallet 函数！替换了第 {start_line+1} 到第 {end_line+1} 行。")
    else:
        print("未找到需要替换的函数，可能已经被修复了。")

if __name__ == "__main__":
    fix_load_wallet_function() 