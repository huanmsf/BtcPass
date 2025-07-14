#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import hashlib
import numpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from btcrecover.btcrpass import load_wallet, get_opencl_devices

def test_step_by_step():
    """逐步对比GPU和CPU的计算过程"""
    print("=" * 60)
    print("GPU vs CPU 逐步对比测试")
    print("=" * 60)
    
    # 加载钱包
    wallet = load_wallet("123456.dat")
    test_password = "123456"
    
    print(f"测试密码: '{test_password}'")
    print(f"Salt (hex): {wallet._salt.hex()}")
    print(f"Iteration count: {wallet._iter_count}")
    print()
    
    # CPU计算过程
    print("1. CPU计算过程:")
    password_bytes = test_password.encode('utf-8')
    derived_key = password_bytes + wallet._salt
    print(f"   初始: password + salt = {derived_key.hex()}")
    
    # 只计算前几次迭代，避免输出过多
    for i in range(min(5, wallet._iter_count)):
        derived_key = hashlib.sha512(derived_key).digest()
        if i < 3:  # 只显示前3次
            print(f"   迭代{i+1}: {derived_key.hex()}")
    
    if wallet._iter_count > 5:
        print(f"   ... (省略中间{wallet._iter_count-5}次迭代)")
        for i in range(wallet._iter_count - 5, wallet._iter_count):
            derived_key = hashlib.sha512(derived_key).digest()
    
    print(f"   最终: {derived_key.hex()}")
    print(f"   密钥: {derived_key[:32].hex()}")
    print()
    
    # GPU计算过程（模拟）
    print("2. GPU计算过程:")
    try:
        devices = get_opencl_devices()
        if not devices:
            print("   ❌ 未找到GPU设备")
            return
        
        # 初始化GPU
        global_ws = [512] * len(devices)
        local_ws = [64] * len(devices)
        wallet.init_opencl_kernel(devices, global_ws, local_ws, 1)
        print("   ✅ GPU初始化成功")
        
        # 获取GPU计算的初始哈希
        hashes = numpy.empty([512, 64], numpy.uint8)
        for i, password in enumerate([test_password]):
            hashes[i] = numpy.fromstring(hashlib.sha512(password.encode('utf-8') + wallet._salt).digest(), numpy.uint8)
        
        print(f"   GPU初始哈希: {hashes[0].tobytes().hex()}")
        print(f"   GPU初始密钥: {hashes[0][:32].tobytes().hex()}")
        
        # 注意：GPU的后续计算在OpenCL内核中进行，我们无法直接观察
        # 但我们可以验证GPU的最终结果
        print("   GPU后续计算在OpenCL内核中进行...")
        
    except Exception as e:
        print(f"   GPU错误: {e}")
        import traceback
        traceback.print_exc()
    print()
    
    # 验证最终结果
    print("3. 验证最终结果:")
    from btcrecover.btcrpass import aes256_cbc_decrypt
    
    # CPU版本
    cpu_derived_key = password_bytes + wallet._salt
    for i in range(wallet._iter_count):
        cpu_derived_key = hashlib.sha512(cpu_derived_key).digest()
    
    cpu_part_master_key = aes256_cbc_decrypt(cpu_derived_key[:32], 
                                           wallet._part_encrypted_master_key[:16], 
                                           wallet._part_encrypted_master_key[16:])
    
    expected_padding = b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"
    cpu_success = cpu_part_master_key == expected_padding
    
    print(f"   CPU派生密钥: {cpu_derived_key[:32].hex()}")
    print(f"   CPU解密结果: {cpu_part_master_key.hex()}")
    print(f"   CPU验证成功: {cpu_success}")
    print()
    
    # 测试GPU是否能找到密码
    print("4. GPU密码验证测试:")
    try:
        result_gpu = wallet._return_verified_password_or_false_opencl([test_password])
        print(f"   GPU结果: {result_gpu}")
        if result_gpu[0]:
            gpu_password = result_gpu[0].decode('utf-8') if isinstance(result_gpu[0], bytes) else result_gpu[0]
            print(f"   GPU找到密码: '{gpu_password}'")
            print(f"   GPU验证成功: {gpu_password == test_password}")
        else:
            print(f"   GPU未找到密码")
    except Exception as e:
        print(f"   GPU验证错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_step_by_step() 