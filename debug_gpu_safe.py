#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import signal
import traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def signal_handler(signum, frame):
    print(f"\n⚠️  收到信号 {signum}，程序被中断")
    sys.exit(1)

def debug_gpu_safe():
    """安全的GPU调试脚本"""
    
    # 设置信号处理器
    signal.signal(signal.SIGSEGV, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("安全的GPU调试测试")
    print("=" * 60)
    
    try:
        from btcrecover.btcrpass import load_wallet, get_opencl_devices
        
        # 加载钱包
        print("1. 加载钱包...")
        wallet = load_wallet("123456.dat")
        print(f"   钱包类型: {type(wallet).__name__}")
        print(f"   钱包难度: {wallet.difficulty_info()}")
        
        # 测试密码
        test_password = "123456"
        print(f"\n2. 测试密码: '{test_password}'")
        
        # CPU验证
        print("\n3. CPU验证:")
        try:
            result_cpu = wallet._return_verified_password_or_false_cpu([test_password])
            print(f"   CPU结果: {result_cpu}")
            if result_cpu[0]:
                cpu_password = result_cpu[0].decode('utf-8') if isinstance(result_cpu[0], bytes) else result_cpu[0]
                print(f"   CPU成功: {cpu_password == test_password}")
                print(f"   CPU找到密码: '{cpu_password}'")
            else:
                print(f"   CPU成功: False")
        except Exception as e:
            print(f"   CPU错误: {e}")
            traceback.print_exc()
        
        # GPU验证
        print("\n4. GPU验证:")
        try:
            # 检查GPU设备
            devices = get_opencl_devices()
            if not devices:
                print("   ❌ 未找到GPU设备")
                return
            
            print(f"   GPU设备: {devices[0].name.strip()}")
            
            # 尝试不同的参数组合
            param_combinations = [
                (512, 64),
                (1024, 256),
                (256, 32),
                (2048, 512)
            ]
            
            for global_ws, local_ws in param_combinations:
                print(f"\n   尝试参数: global-ws={global_ws}, local-ws={local_ws}")
                try:
                    # 初始化GPU
                    wallet.init_opencl_kernel(devices, [global_ws], [local_ws], 1)
                    print("   ✅ GPU初始化成功")
                    
                    # GPU验证
                    result_gpu = wallet._return_verified_password_or_false_opencl([test_password])
                    print(f"   GPU结果: {result_gpu}")
                    
                    if result_gpu[0]:
                        gpu_password = result_gpu[0].decode('utf-8') if isinstance(result_gpu[0], bytes) else result_gpu[0]
                        print(f"   GPU成功: {gpu_password == test_password}")
                        print(f"   GPU找到密码: '{gpu_password}'")
                        break
                    else:
                        print(f"   GPU成功: False")
                        break
                        
                except Exception as e:
                    print(f"   ❌ GPU错误: {e}")
                    if "local-ws" in str(e) and "exceeds max" in str(e):
                        print(f"   ⚠️  local-ws参数过大，跳过此组合")
                        continue
                    else:
                        print(f"   🔍 详细错误:")
                        traceback.print_exc()
                        break
                        
        except Exception as e:
            print(f"   ❌ GPU初始化错误: {e}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ 程序错误: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("调试完成")

if __name__ == "__main__":
    debug_gpu_safe() 