#!/usr/bin/env python3

# 修改 WalletElectrum28 类，使其在没有 coincurve 的情况下也能工作

def fix_electrum28_coincurve():
    with open('btcrecover/btcrpass.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到 WalletElectrum28 类的 __init__ 方法
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith('def __init__(self, loading = False):'):
            start_line = i
        elif start_line is not None and line.strip() == 'self._passwords_per_second = 800 if pbkdf2_library_name == "hashlib" else 140':
            end_line = i
            break
    
    if start_line is not None and end_line is not None:
        # 替换 __init__ 方法
        new_init = [
            '    def __init__(self, loading = False):\n',
            '        assert loading, \'use load_from_* to create a \' + self.__class__.__name__\n',
            '        global hmac\n',
            '        import hmac\n',
            '        try:\n',
            '            global coincurve\n',
            '            import coincurve\n',
            '        except ImportError:\n',
            '            coincurve = None\n',
            '        pbkdf2_library_name    = load_pbkdf2_library().__name__\n',
            '        self._aes_library_name = load_aes256_library().__name__\n',
            '        self._passwords_per_second = 800 if pbkdf2_library_name == "hashlib" else 140\n'
        ]
        
        # 替换方法
        lines[start_line:end_line+1] = new_init
        
        # 写回文件
        with open('btcrecover/btcrpass.py', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"成功修改 WalletElectrum28.__init__ 方法！替换了第 {start_line+1} 到第 {end_line+1} 行。")
    else:
        print("未找到需要替换的 __init__ 方法。")
    
    # 现在修改 load_from_filename 方法
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith('@classmethod') and i+1 < len(lines) and 'load_from_filename' in lines[i+1]:
            start_line = i
        elif start_line is not None and line.strip() == 'return self':
            end_line = i
            break
    
    if start_line is not None and end_line is not None:
        # 找到 coincurve.PublicKey 的使用
        for i in range(start_line, end_line + 1):
            if 'coincurve.PublicKey' in lines[i]:
                # 替换这一行
                lines[i] = lines[i].replace(
                    'self._ephemeral_pubkey = coincurve.PublicKey(data[4:37])',
                    'if coincurve is None:\n            raise ImportError("coincurve module is required for Electrum 2.8+ wallets. Please install it with: pip install coincurve")\n        self._ephemeral_pubkey = coincurve.PublicKey(data[4:37])'
                )
                break
        
        # 写回文件
        with open('btcrecover/btcrpass.py', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("成功修改 load_from_filename 方法，添加了 coincurve 检查。")
    else:
        print("未找到需要替换的 load_from_filename 方法。")

if __name__ == "__main__":
    fix_electrum28_coincurve() 