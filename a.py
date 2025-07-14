#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def check_gpu_support():
    """检查GPU是否支持btcrecover的GPU加速功能"""
    print("=" * 60)
    print("GPU 支持检查工具")
    print("=" * 60)
    
    # 1. 检查Python版本
    print(f"Python版本: {sys.version}")
    print()
    
    # 2. 检查PyOpenCL
    print("1. 检查PyOpenCL库...")
    try:
        import pyopencl
        print("   ✅ PyOpenCL 已安装")
        print(f"   PyOpenCL版本: {pyopencl.VERSION}")
    except ImportError:
        print("   ❌ PyOpenCL 未安装")
        print("   请运行: pip install pyopencl")
        return False
    print()
    
    # 3. 检查NumPy
    print("2. 检查NumPy库...")
    try:
        import numpy
        print("   ✅ NumPy 已安装")
        print(f"   NumPy版本: {numpy.__version__}")
    except ImportError:
        print("   ❌ NumPy 未安装")
        print("   请运行: pip install numpy")
        return False
    print()
    
    # 4. 检查OpenCL平台和设备
    print("3. 检查OpenCL平台和设备...")
    try:
        platforms = pyopencl.get_platforms()
        if not platforms:
            print("   ❌ 未找到OpenCL平台")
            return False
        
        print(f"   找到 {len(platforms)} 个OpenCL平台:")
        
        total_devices = 0
        supported_devices = []
        
        for i, platform in enumerate(platforms):
            print(f"   平台 {i+1}: {platform.name}")
            print(f"     版本: {platform.version}")
            print(f"     供应商: {platform.vendor}")
            
            devices = platform.get_devices()
            print(f"     设备数量: {len(devices)}")
            
            for j, device in enumerate(devices):
                total_devices += 1
                print(f"     设备 {j+1}: {device.name}")
                print(f"       类型: {device.type}")
                print(f"       可用: {'是' if device.available else '否'}")
                print(f"       配置文件: {device.profile}")
                print(f"       字节序: {'小端' if device.endian_little else '大端'}")
                print(f"       全局内存: {device.global_mem_size // (1024**2)} MB")
                print(f"       本地内存: {device.local_mem_size // 1024} KB")
                
                # 检查btcrecover的要求
                is_supported = (
                    device.available == 1 and 
                    device.profile == "FULL_PROFILE" and 
                    device.endian_little == 1
                )
                
                if is_supported:
                    supported_devices.append(device)
                    print(f"       ✅ 支持btcrecover GPU加速")
                else:
                    print(f"       ❌ 不支持btcrecover GPU加速")
                    if not device.available:
                        print(f"         原因: 设备不可用")
                    if device.profile != "FULL_PROFILE":
                        print(f"         原因: 需要FULL_PROFILE，当前为{device.profile}")
                    if not device.endian_little:
                        print(f"         原因: 需要小端字节序")
                print()
        
        print(f"总结: 找到 {total_devices} 个设备，其中 {len(supported_devices)} 个支持btcrecover")
        
        if supported_devices:
            print("✅ 你的系统支持btcrecover GPU加速！")
            return True
        else:
            print("❌ 没有找到支持btcrecover GPU加速的设备")
            return False
            
    except Exception as e:
        print(f"   ❌ 检查OpenCL时出错: {e}")
        return False
    
    print()

def test_btcrecover_gpu():
    """测试btcrecover的GPU功能"""
    print("4. 测试btcrecover GPU功能...")
    try:
        # 导入btcrecover的GPU检测函数
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from btcrecover.btcrpass import get_opencl_devices
        
        devices = get_opencl_devices()
        if devices:
            print(f"   ✅ btcrecover找到 {len(devices)} 个支持的GPU设备:")
            for i, device in enumerate(devices):
                print(f"     设备 {i+1}: {device.name}")
                print(f"       全局内存: {device.global_mem_size // (1024**2)} MB")
                print(f"       计算单元: {device.max_compute_units}")
                print(f"       最大工作组大小: {device.max_work_group_size}")
            return True
        else:
            print("   ❌ btcrecover未找到支持的GPU设备")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试btcrecover GPU功能时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始检查GPU支持...")
    print()
    
    # 基本检查
    basic_support = check_gpu_support()
    
    if basic_support:
        print()
        # btcrecover特定检查
        btcrecover_support = test_btcrecover_gpu()
        
        if btcrecover_support:
            print()
            print("🎉 恭喜！你的系统完全支持btcrecover GPU加速！")
            print()
            print("使用建议:")
            print("1. 运行性能测试:")
            print("   python btcrecover.py --wallet wallet.dat --performance --enable-gpu --global-ws 4096 --local-ws 512")
            print()
            print("2. 实际破解:")
            print("   python btcrecover.py --wallet wallet.dat --enable-gpu --global-ws 4096 --local-ws 512")
            print()
            print("3. 调优参数以获得最佳性能")
        else:
            print()
            print("⚠️  基本GPU支持正常，但btcrecover可能需要额外配置")
    else:
        print()
        print("❌ 你的系统不支持GPU加速")
        print()
        print("解决方案:")
        print("1. 安装支持OpenCL的显卡驱动")
        print("2. 安装PyOpenCL: pip install pyopencl")
        print("3. 安装NumPy: pip install numpy")
        print("4. 确保显卡支持OpenCL 1.0或更高版本")

if __name__ == "__main__":
    main()