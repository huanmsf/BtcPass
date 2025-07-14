#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gpu_support():
    """测试GPU支持"""
    print("=" * 60)
    print("GPU 支持测试")
    print("=" * 60)
    
    try:
        from btcrecover.btcrpass import get_opencl_devices
        devices = get_opencl_devices()
        
        if devices:
            print(f"✅ 找到 {len(devices)} 个GPU设备:")
            for i, device in enumerate(devices, 1):
                print(f"  {i}. {device.name.strip()}")
                print(f"     类型: {device.type}")
                print(f"     内存: {device.global_mem_size // (1024**2)} MB")
                print(f"     计算单元: {device.max_compute_units}")
                print()
        else:
            print("❌ 未找到支持的GPU设备")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ GPU检测失败: {e}")
        return False

def test_gpu_performance():
    """测试GPU性能"""
    print("=" * 60)
    print("GPU 性能测试")
    print("=" * 60)
    
    try:
        # 测试钱包加载
        from btcrecover.btcrpass import load_wallet, get_opencl_devices
        wallet = load_wallet("wallet.dat")
        print(f"钱包类型: {type(wallet).__name__}")
        print(f"钱包难度: {wallet.difficulty_info()}")
        
        # 测试GPU初始化
        devices = get_opencl_devices()
        if devices:
            print(f"\n初始化GPU加速...")
            global_ws = [4096] * len(devices)
            local_ws = [512] * len(devices)
            wallet.init_opencl_kernel(devices, global_ws, local_ws, 1)
            print("✅ GPU加速初始化成功")
            
            # 测试小批量密码
            test_passwords = ["test123", "password", "123456", "wrong"]
            result, count = wallet.return_verified_password_or_false(test_passwords)
            print(f"测试完成: 尝试了 {count} 个密码")
            
        return True
        
    except Exception as e:
        print(f"❌ GPU性能测试失败: {e}")
        return False

if __name__ == "__main__":
    if test_gpu_support():
        test_gpu_performance() 