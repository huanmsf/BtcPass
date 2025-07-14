#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_opencl_kernel():
    """测试OpenCL内核编译和基本功能"""
    
    print("=" * 60)
    print("OpenCL内核测试")
    print("=" * 60)
    
    try:
        import pyopencl as cl
        import numpy as np
        
        print("1. 检查OpenCL平台和设备...")
        platforms = cl.get_platforms()
        print(f"   找到 {len(platforms)} 个OpenCL平台")
        
        for i, platform in enumerate(platforms):
            print(f"   平台 {i}: {platform.name}")
            devices = platform.get_devices(cl.device_type.GPU)
            print(f"   GPU设备数量: {len(devices)}")
            
            for j, device in enumerate(devices):
                print(f"   设备 {j}: {device.name}")
                print(f"   内存: {device.global_mem_size // (1024**3)} GB")
                print(f"   最大工作组大小: {device.get_info(cl.device_info.MAX_WORK_GROUP_SIZE)}")
        
        print("\n2. 测试Bitcoin Core OpenCL内核...")
        
        # 获取第一个GPU设备
        devices = cl.get_platforms()[0].get_devices(cl.device_type.GPU)
        if not devices:
            print("   ❌ 未找到GPU设备")
            return
        
        device = devices[0]
        print(f"   使用设备: {device.name}")
        
        # 创建上下文和队列
        context = cl.Context([device])
        queue = cl.CommandQueue(context)
        
        # 读取OpenCL内核源码
        kernel_path = os.path.join(os.path.dirname(__file__), "btcrecover", "sha512-bc-kernel.cl")
        print(f"   内核文件: {kernel_path}")
        
        with open(kernel_path, 'r') as f:
            kernel_source = f.read()
        
        print(f"   内核源码长度: {len(kernel_source)} 字符")
        
        # 编译内核
        print("   编译内核...")
        try:
            program = cl.Program(context, kernel_source).build(options=["-w"])
            print("   ✅ 内核编译成功")
            
            # 获取内核函数
            kernel = program.kernel_sha512_bc
            print(f"   ✅ 找到内核函数: kernel_sha512_bc")
            
            # 设置参数类型
            kernel.set_scalar_arg_dtypes([None, np.uint32])
            print("   ✅ 参数类型设置成功")
            
        except Exception as e:
            print(f"   ❌ 内核编译失败: {e}")
            traceback.print_exc()
            return
        
        print("\n3. 测试基本内存操作...")
        
        # 测试内存分配
        try:
            test_size = 1024 * 64  # 64KB
            test_buffer = cl.Buffer(context, cl.mem_flags.READ_WRITE, test_size)
            print(f"   ✅ 内存分配成功: {test_size} 字节")
            
            # 测试数据传输
            test_data = np.random.bytes(test_size)
            cl.enqueue_copy(queue, test_buffer, test_data)
            print("   ✅ 数据传输成功")
            
            # 清理
            test_buffer.release()
            print("   ✅ 内存释放成功")
            
        except Exception as e:
            print(f"   ❌ 内存操作失败: {e}")
            traceback.print_exc()
        
        print("\n4. 测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_opencl_kernel() 