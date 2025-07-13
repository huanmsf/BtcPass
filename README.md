# BtcPass - 比特币钱包密码恢复工具

一个开源的比特币钱包密码和种子恢复工具，专为 Python 3.11+ 优化。

## 快速开始

### 基本用法
```bash
# 恢复钱包密码
python btcrecover.py --wallet 你的钱包文件 --passwordlist 密码字典.txt

# 示例：恢复 Electrum 钱包密码
python btcrecover.py --wallet wallet.dat --passwordlist pass.txt --utf8
```

### 支持的钱包类型
- **Bitcoin Core** - 比特币核心钱包
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

### 3. 多线程加速
```bash
python btcrecover.py --wallet wallet.dat --passwordlist pass.txt --threads 8
```

### 4. 模拟拼写错误
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

## 注意事项

- 大文件 (如 `rockyou.txt`) 已被 `.gitignore` 排除
- 建议使用较小的密码字典进行测试
- 确保钱包文件路径正确
- 某些钱包类型可能需要额外依赖

## 许可证

GPL v2 - 开源软件，可自由使用和修改

## 致谢

感谢原项目 [btcrecover](https://github.com/gurnec/btcrecover) 的贡献者。

---

**如果这个工具对你有帮助，请考虑小额捐赠：**
`3Au8ZodNHPei7MQiSVAWb7NB2yqsb48GW4`
