#!/bin/bash

echo "=========================================="
echo "btcrecover GPU环境安装脚本 (虚拟环境版)"
echo "=========================================="

# 更新系统
echo "1. 更新系统..."
apt update && apt upgrade -y

# 安装基础依赖
echo "2. 安装基础依赖..."
apt install -y python3 python3-pip python3-venv python3-dev build-essential wget curl

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

# 创建虚拟环境
echo "5. 创建Python虚拟环境..."
python3 -m venv btcrecover_env
echo "虚拟环境创建完成: btcrecover_env"

# 激活虚拟环境并安装Python依赖
echo "6. 在虚拟环境中安装Python依赖..."
source btcrecover_env/bin/activate
pip install --upgrade pip
pip install pyopencl numpy

# 验证安装
echo "7. 验证安装..."
echo "Python版本:"
python --version

echo "pyopencl版本:"
python -c "import pyopencl; print('pyopencl版本:', pyopencl.VERSION)"

echo "GPU设备:"
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU状态:"
    nvidia-smi
fi

if command -v clinfo &> /dev/null; then
    echo "OpenCL设备:"
    clinfo | grep -A 5 "Device Name"
fi

# 创建运行脚本
echo "8. 创建运行脚本..."
cat > run_btcrecover.sh << 'EOF'
#!/bin/bash
echo "激活虚拟环境并运行btcrecover..."
source btcrecover_env/bin/activate
python btcrecover.py "$@"
EOF

chmod +x run_btcrecover.sh

echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo "使用方法："
echo "1. 激活虚拟环境: source btcrecover_env/bin/activate"
echo "2. 运行GPU破解: python btcrecover.py --wallet wallet.dat --passwordlist apss.txt --enable-gpu --global-ws 32768 --local-ws 1024 --no-eta"
echo ""
echo "或者使用快捷脚本:"
echo "./run_btcrecover.sh --wallet wallet.dat --passwordlist apss.txt --enable-gpu --global-ws 32768 --local-ws 1024 --no-eta" 