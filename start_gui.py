#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BtcPass GUI 启动器
选择启动GUI版本或命令行版本
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class LauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BtcPass 启动器")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 创建界面
        self.create_widgets()
        
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """创建GUI组件"""
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="BtcPass 启动器", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 30))
        
        # 说明文字
        desc_label = ttk.Label(main_frame, text="请选择要启动的版本：", 
                              font=("Arial", 10))
        desc_label.pack(pady=(0, 20))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # GUI版本按钮
        gui_button = ttk.Button(button_frame, text="启动图形界面版本", 
                               command=self.start_gui, width=25)
        gui_button.pack(pady=10)
        
        # 命令行版本按钮
        cli_button = ttk.Button(button_frame, text="启动命令行版本", 
                               command=self.start_cli, width=25)
        cli_button.pack(pady=10)
        
        # 退出按钮
        exit_button = ttk.Button(button_frame, text="退出", 
                                command=self.root.quit, width=25)
        exit_button.pack(pady=10)
        
        # 版本信息
        version_label = ttk.Label(main_frame, text="BtcPass - 比特币钱包密码恢复工具", 
                                 font=("Arial", 8))
        version_label.pack(side=tk.BOTTOM, pady=(20, 0))
        
    def start_gui(self):
        """启动GUI版本"""
        try:
            # 检查GUI文件是否存在
            gui_file = "btcrecover_gui_simple.py"
            if not os.path.exists(gui_file):
                messagebox.showerror("错误", f"找不到GUI文件: {gui_file}")
                return
                
            # 启动GUI
            subprocess.Popen([sys.executable, gui_file])
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动GUI失败: {str(e)}")
            
    def start_cli(self):
        """启动命令行版本"""
        try:
            # 检查主程序文件是否存在
            main_file = "btcrecover.py"
            if not os.path.exists(main_file):
                messagebox.showerror("错误", f"找不到主程序文件: {main_file}")
                return
                
            # 显示帮助信息
            help_text = """
BtcPass 命令行版本

基本用法:
python btcrecover.py --wallet <钱包文件> --passwordlist <密码字典>

常用参数:
--wallet <文件>          指定钱包文件
--passwordlist <文件>    指定密码字典文件
--threads <数量>         设置CPU线程数
--utf8                   启用UTF-8模式（支持中文密码）
--enable-gpu             启用GPU加速（实验性）

示例:
python btcrecover.py --wallet wallet.dat --passwordlist passwords.txt --threads 8 --utf8

按确定启动命令行版本...
            """
            
            result = messagebox.askokcancel("命令行版本", help_text)
            if result:
                # 启动命令行版本
                subprocess.Popen([sys.executable, main_file, "--help"])
                self.root.quit()
                
        except Exception as e:
            messagebox.showerror("错误", f"启动命令行版本失败: {str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    app = LauncherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 