#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet, get_opencl_devices

def test_password_verification():
    """测试GPU和CPU的密码验证逻辑"""
    print("=" * 60)
    print("GPU vs CPU 密码验证对比测试")
    print("=" * 60)
    
    # 加载钱包
    wallet = load_wallet("123456.dat")
    print(f"钱包类型: {type(wallet).__name__}")
    print(f"钱包难度: {wallet.difficulty_info()}")
    print()
    
    # 测试密码
    test_password = "123456"
    print(f"测试密码: '{test_password}'")
    print()
    
    # CPU验证
    print("1. CPU验证:")
    try:
        result_cpu = wallet._return_verified_password_or_false_cpu([test_password])
        print(f"   CPU结果: {result_cpu}")
        # 修正比较逻辑：CPU返回的是字节串，需要解码
        if result_cpu[0]:
            cpu_password = result_cpu[0].decode('utf-8') if isinstance(result_cpu[0], bytes) else result_cpu[0]
            print(f"   CPU成功: {cpu_password == test_password}")
            print(f"   CPU找到密码: '{cpu_password}'")
        else:
            print(f"   CPU成功: False")
    except Exception as e:
        print(f"   CPU错误: {e}")
    print()
    
    # GPU验证
    print("2. GPU验证:")
    try:
        # 检查GPU设备
        devices = get_opencl_devices()
        if not devices:
            print("   ❌ 未找到GPU设备")
            return
        
        print(f"   GPU设备: {devices[0].name.strip()}")
        
        # 修复GPU初始化参数
        global_ws = [4096] * len(devices)
        local_ws = [256] * len(devices)
        
        # 初始化GPU
        wallet.init_opencl_kernel(devices, global_ws, local_ws, 1)
        print("   ✅ GPU初始化成功")
        
        # GPU验证
        result_gpu = wallet._return_verified_password_or_false_opencl([test_password])
        print(f"   GPU结果: {result_gpu}")
        # 修正比较逻辑：GPU返回的也是字节串
        if result_gpu[0]:
            gpu_password = result_gpu[0].decode('utf-8') if isinstance(result_gpu[0], bytes) else result_gpu[0]
            print(f"   GPU成功: {gpu_password == test_password}")
            print(f"   GPU找到密码: '{gpu_password}'")
        else:
            print(f"   GPU成功: False")
        
    except Exception as e:
        print(f"   GPU错误: {e}")
        import traceback
        traceback.print_exc()
    print()
    
    # 详细对比
    print("3. 详细对比:")
    try:
        # 获取钱包参数
        salt = wallet._salt
        iter_count = wallet._iter_count
        part_encrypted_master_key = wallet._part_encrypted_master_key
        
        print(f"   Salt (hex): {salt.hex()}")
        print(f"   Iteration count: {iter_count}")
        print(f"   Part encrypted master key (hex): {part_encrypted_master_key.hex()}")
        print()
        
        # 手动计算CPU版本
        print("   CPU手动计算:")
        derived_key = test_password.encode('utf-8') + salt
        for i in range(iter_count):
            derived_key = hashlib.sha512(derived_key).digest()
        
        from btcrecover.btcrpass import aes256_cbc_decrypt
        part_master_key = aes256_cbc_decrypt(derived_key[:32], 
                                           part_encrypted_master_key[:16], 
                                           part_encrypted_master_key[16:])
        
        expected_padding = b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"
        cpu_success = part_master_key == expected_padding
        
        print(f"   派生密钥 (hex): {derived_key[:32].hex()}")
        print(f"   解密结果 (hex): {part_master_key.hex()}")
        print(f"   期望填充 (hex): {expected_padding.hex()}")
        print(f"   CPU验证结果: {cpu_success}")
        
    except Exception as e:
        print(f"   详细对比错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password_verification() 