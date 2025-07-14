@echo off
chcp 65001 >nul
title BTC Recover 依赖安装脚本

echo ========================================
echo    BTC Recover 依赖包自动安装脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python环境
    echo.
    echo 请先安装Python：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装Python 3.8或更高版本
    echo 3. 安装时请勾选"Add Python to PATH"选项
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python环境检查通过
)

echo.
echo 正在检查pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到pip
    echo 请重新安装Python，确保包含pip
    pause
    exit /b 1
) else (
    echo ✅ pip检查通过
)

echo.
echo 正在升级pip...
python -m pip install --upgrade pip --quiet

echo.
echo 开始安装依赖包...
echo.

echo 1. 安装tkinter...
pip install tkinter --quiet
if errorlevel 1 (
    echo ❌ tkinter安装失败
) else (
    echo ✅ tkinter安装成功
)

echo.
echo 2. 安装coincurve...
pip install coincurve --quiet
if errorlevel 1 (
    echo ❌ coincurve安装失败，尝试使用预编译包...
    pip install coincurve --only-binary=all --quiet
    if errorlevel 1 (
        echo ❌ coincurve安装失败，请手动安装
    ) else (
        echo ✅ coincurve安装成功
    )
) else (
    echo ✅ coincurve安装成功
)

echo.
echo 3. 安装passlib...
pip install passlib --quiet
if errorlevel 1 (
    echo ❌ passlib安装失败
) else (
    echo ✅ passlib安装成功
)

echo.
echo 4. 安装progressbar...
pip install progressbar --quiet
if errorlevel 1 (
    echo ❌ progressbar安装失败
) else (
    echo ✅ progressbar安装成功
)

echo.
echo 5. 安装aespython...
pip install aespython --quiet
if errorlevel 1 (
    echo ❌ aespython安装失败
) else (
    echo ✅ aespython安装成功
)

echo.
echo ========================================
echo 依赖包安装完成！
echo ========================================
echo.
echo 验证安装结果...
echo.

python -c "import tkinter; print('✅ tkinter: 正常')" 2>nul || echo "❌ tkinter: 异常"
python -c "import coincurve; print('✅ coincurve: 正常')" 2>nul || echo "❌ coincurve: 异常"
python -c "import passlib; print('✅ passlib: 正常')" 2>nul || echo "❌ passlib: 异常"
python -c "import progressbar; print('✅ progressbar: 正常')" 2>nul || echo "❌ progressbar: 异常"

echo.
echo 如果所有依赖包都显示"正常"，说明安装成功！
echo.
echo 现在你可以运行 start_gui.bat 启动程序了。
echo.
pause 