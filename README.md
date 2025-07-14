# BtcPass - 比特币钱包密码恢复工具

一个开源的比特币钱包密码和种子恢复工具，专为 Python 3.11+ 优化。

## 📚 新手指南

如果你是第一次使用，请先阅读：
- **[快速开始指南](快速开始指南.md)** - 5分钟快速上手
- **[新手安装运行手册](新手安装运行手册.md)** - 详细安装说明
- **[一键安装依赖](install_dependencies.bat)** - 自动安装所有依赖包

## 快速开始

### GUI界面（推荐）
```bash
# 启动GUI启动器
python start_gui.py

# 或直接启动GUI版本
python btcrecover_gui_simple.py
```

### 命令行基本用法
```bash
# 恢复钱包密码
python btcrecover.py --wallet 你的钱包文件 --passwordlist 密码字典.txt

# 示例：恢复 Electrum 钱包密码
python btcrecover.py --wallet wallet.dat --passwordlist pass.txt --utf8
```

### 支持的钱包类型
- **Bitcoin Core** - 比特币核心钱包 仅适用0.13.x版本客户端生成的xx.dat钱包文件，新版本的不支持（123456.dat支持，huanmsf.dat不支持）
- **Electrum** - 电子钱包 (1.x, 2.x, 4.x)
- **Armory** - 军械库钱包
- **MultiBit** - 多重比特钱包
- **Blockchain.info** - 区块链钱包
- **BIP-39** - 标准助记词钱包 (TREZOR, Ledger 等)
- **Android 比特币钱包** - 安卓比特币钱包
- **Bither** - 比太钱包

## 核心功能

### 🔐 密码恢复
- 支持多种加密算法 (PBKDF2, scrypt, AES 等)
- 多线程并行破解，提高效率
- 支持 Unicode 密码和特殊字符
- 自动保存找到的密码到 `result_found.txt`

### 🎯 智能匹配
- 支持通配符扩展 (`%d` 数字, `%l` 小写字母等)
- 拼写错误模拟 (大小写、字符替换、插入等)
- 正则表达式过滤
- 进度条和剩余时间显示

### 🛡️ 安全特性
- 离线模式 - 只提取必要信息，不暴露私钥
- 可中断和恢复 - 自动保存进度
- 支持 GPU 加速 (实验性)

## 安装要求

- Python 3.11 或更高版本
- 可选依赖：
  - `coincurve` - 用于 Electrum 4.x 钱包
  - `pylibscrypt` - 用于 scrypt 算法
  - `pyopencl` - 用于 GPU 加速

### 安装依赖
```bash
pip install coincurve pylibscrypt pyopencl
```

## 使用示例

### 1. 恢复 Electrum 钱包密码
```bash
python btcrecover.py --wallet electrum_wallet --passwordlist rockyou.txt --utf8
```

### 2. 使用自定义密码列表
```bash
python btcrecover.py --wallet wallet.dat --passwordlist my_passwords.txt
```

### 3. 多线程CPU加速破解
```bash
python btcrecover.py --wallet wallet.dat --passwordlist pass.txt --threads 8
```
- `--threads 8` 指定使用8个CPU线程（根据CPU核心数调整）
- 默认自动使用多线程，适合绝大多数用户

### 4. 启用GPU加速破解（实验性）
```bash
python btcrecover.py --wallet wallet.dat --passwordlist pass.txt --enable-gpu --global-ws 512 --local-ws 64
```
- `--enable-gpu` 启用OpenCL GPU加速（仅支持部分钱包类型，如Bitcoin Core）
- `--global-ws` 设置全局工作组大小（推荐512~4096，需为local-ws整数倍）
- `--local-ws` 设置本地工作组大小（推荐64/128/256，具体取决于显卡）
- 如遇报错可尝试调整参数，如`--local-ws 256`、`--global-ws 1024`
- GPU加速对驱动、依赖和硬件要求较高，部分服务器GPU（如Tesla V100）可能不兼容

### 5. 模拟拼写错误
```bash
python btcrecover.py --wallet wallet.dat --passwordlist pass.txt --typos 2 --typos-swap --typos-capslock
```

## 输出结果

找到密码时，程序会显示：
```
==============================
成功找到密码：'your_password'
==============================
```

同时自动保存到 `result_found.txt`：
```
钱包文件: wallet.dat
密码: your_password
```

## GUI功能特性

### 🖥️ 图形界面
- **GUI版本**：完整的图形用户界面，支持所有核心功能
- **启动器**：统一入口，可选择GUI版本或命令行版本

### 🎯 核心功能
- 钱包文件选择（支持拖拽）
- 密码字典文件选择
- 钱包类型自动检测/手动选择
- CPU线程数调节
- GPU加速选项（实验性）
- 实时运行日志显示
- 进度条和状态显示

### ⚙️ 高级选项
- UTF-8模式支持中文密码
- 跳过密码数设置
- 最大运行时间限制
- GPU参数调节
- 自动保存结果

## 注意事项

- 大文件 (如 `rockyou.txt`) 已被 `.gitignore` 排除
- 建议使用较小的密码字典进行测试
- 确保钱包文件路径正确
- 某些钱包类型可能需要额外依赖
- **GPU加速为实验性功能，推荐优先使用CPU多线程模式**
- GPU模式如遇崩溃或找不到密码，请切换回CPU多线程
- **首次使用建议选择GUI版本进行测试**

## 许可证

GPL v2 - 开源软件，可自由使用和修改

## 致谢

感谢原项目 [btcrecover](https://github.com/gurnec/btcrecover) 的贡献者。

---

**如果这个工具对你有帮助，请考虑小额捐赠：**
`bc1qj930pd7u93qlftx6gf33zsd07wlp220q258v38`
