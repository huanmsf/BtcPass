#!/usr/bin/env python3

# 修复 load_wallet 函数，使其能够自动检测所有支持的钱包类型

def fix_load_wallet_function():
    with open('btcrecover/btcrpass.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到并替换 load_wallet 函数
    old_function = '''def load_wallet(wallet_filename):
    # 只检?Bitcoin Core 钱包类型，避免base64误判
    from .btcrpass import WalletBitcoinCore
    wallet_type = WalletBitcoinCore
    with open(wallet_filename, "rb") as wallet_file:
        wallet_file.seek(0)
        found = wallet_type.is_wallet_file(wallet_file)
        if found:
            wallet_file.seek(0)
            return wallet_type.load_from_filename(wallet_filename)
    raise ValueError("Unknown wallet file type")'''
    
    new_function = '''def load_wallet(wallet_filename):
    # Try each registered wallet type to see if it can load this file
    for wallet_type in wallet_types:
        with open(wallet_filename, "rb") as wallet_file:
            wallet_file.seek(0)
            found = wallet_type.is_wallet_file(wallet_file)
            if found:
                wallet_file.seek(0)
                return wallet_type.load_from_filename(wallet_filename)
    raise ValueError("Unknown wallet file type")'''
    
    if old_function in content:
        content = content.replace(old_function, new_function)
        with open('btcrecover/btcrpass.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("成功修复 load_wallet 函数！")
    else:
        print("未找到需要替换的函数，可能已经被修复了。")

if __name__ == "__main__":
    fix_load_wallet_function() 