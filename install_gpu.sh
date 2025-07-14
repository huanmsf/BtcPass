#!/bin/bash

echo "=========================================="
echo "btcrecover GPU环境自动化安装脚本"
echo "=========================================="

# 更新系统
echo "1. 更新系统..."
apt update && apt upgrade -y

# 安装基础依赖
echo "2. 安装基础依赖..."
apt install -y python3 python3-pip python3-dev build-essential wget curl

# 安装OpenCL
echo "3. 安装OpenCL..."
apt install -y ocl-icd-opencl-dev opencl-headers

# 检测GPU类型并安装驱动
echo "4. 检测GPU并安装驱动..."
if lspci | grep -i nvidia > /dev/null; then
    echo "检测到NVIDIA GPU，安装NVIDIA驱动..."
    apt install -y nvidia-driver-535 nvidia-cuda-toolkit
    echo "NVIDIA驱动安装完成"
elif lspci | grep -i amd > /dev/null; then
    echo "检测到AMD GPU，安装AMD驱动..."
    apt install -y rocm-opencl-dev
    echo "AMD驱动安装完成"
else
    echo "未检测到GPU，安装CPU版本依赖..."
fi

# 安装Python依赖
echo "5. 安装Python依赖..."
pip3 install pyopencl numpy

# 验证安装
echo "6. 验证安装..."
echo "Python版本:"
python3 --version

echo "pyopencl版本:"
python3 -c "import pyopencl; print('pyopencl版本:', pyopencl.VERSION)"

echo "GPU设备:"
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU状态:"
    nvidia-smi
fi

if command -v clinfo &> /dev/null; then
    echo "OpenCL设备:"
    clinfo | grep -A 5 "Device Name"
fi

echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo "现在可以运行btcrecover GPU破解了："
echo "python3 btcrecover.py --wallet wallet.dat --passwordlist rockyou.txt --enable-gpu --global-ws 32768 --local-ws 1024 --no-eta" 