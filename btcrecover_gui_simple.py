#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BtcPass GUI - 比特币钱包密码恢复工具图形界面
简化版本，专注于核心功能
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os
import subprocess
import queue
import time

class BtcPassGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BtcPass - 比特币钱包密码恢复工具")
        self.root.geometry("800x800")  # 增加窗口高度
        
        # 变量
        self.wallet_file = tk.StringVar()
        self.password_file = tk.StringVar()
        self.enable_gpu = tk.BooleanVar(value=False)
        self.threads = tk.IntVar(value=os.cpu_count() or 4)
        self.global_ws = tk.IntVar(value=4096)
        self.local_ws = tk.IntVar(value=64)
        self.utf8_mode = tk.BooleanVar(value=True)
        
        # 运行状态
        self.is_running = False
        self.process = None
        
        # 创建界面
        self.create_widgets()
        
        # 进度队列
        self.progress_queue = queue.Queue()
        self.check_progress_queue()
        
    def create_widgets(self):
        """创建GUI组件"""
        
        # 创建主滚动框架
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 主框架
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="BtcPass - 比特币钱包密码恢复工具", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 文件选择框架
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 钱包文件
        ttk.Label(file_frame, text="钱包文件:").pack(anchor=tk.W)
        wallet_frame = ttk.Frame(file_frame)
        wallet_frame.pack(fill=tk.X, pady=(5, 10))
        
        ttk.Entry(wallet_frame, textvariable=self.wallet_file).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(wallet_frame, text="浏览", command=self.browse_wallet_file).pack(side=tk.RIGHT)
        
        # 密码文件
        ttk.Label(file_frame, text="密码字典:").pack(anchor=tk.W)
        password_frame = ttk.Frame(file_frame)
        password_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Entry(password_frame, textvariable=self.password_file).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(password_frame, text="浏览", command=self.browse_password_file).pack(side=tk.RIGHT)
        
        # 选项框架
        options_frame = ttk.LabelFrame(main_frame, text="选项设置", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # CPU线程数
        threads_frame = ttk.Frame(options_frame)
        threads_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(threads_frame, text="CPU线程数:").pack(side=tk.LEFT)
        threads_scale = ttk.Scale(threads_frame, from_=1, to=32, variable=self.threads, orient=tk.HORIZONTAL)
        threads_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        threads_scale.configure(command=lambda x: self.update_threads_label())
        
        self.threads_label = ttk.Label(threads_frame, text=str(self.threads.get()))
        self.threads_label.pack(side=tk.RIGHT)
        
        # UTF-8模式
        ttk.Checkbutton(options_frame, text="启用UTF-8模式（支持中文密码）", 
                       variable=self.utf8_mode).pack(anchor=tk.W, pady=5)
        
        # GPU选项
        gpu_frame = ttk.LabelFrame(main_frame, text="GPU加速（实验性）", padding="10")
        gpu_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Checkbutton(gpu_frame, text="启用GPU加速", 
                       variable=self.enable_gpu, 
                       command=self.toggle_gpu_options).pack(anchor=tk.W, pady=5)
        
        # GPU参数
        gpu_params_frame = ttk.Frame(gpu_frame)
        gpu_params_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(gpu_params_frame, text="全局工作组大小:").grid(row=0, column=0, sticky=tk.W)
        self.global_ws_entry = ttk.Entry(gpu_params_frame, textvariable=self.global_ws, width=10)
        self.global_ws_entry.grid(row=0, column=1, padx=(5, 20))
        
        ttk.Label(gpu_params_frame, text="本地工作组大小:").grid(row=0, column=2, sticky=tk.W)
        self.local_ws_entry = ttk.Entry(gpu_params_frame, textvariable=self.local_ws, width=10)
        self.local_ws_entry.grid(row=0, column=3, padx=(5, 0))
        
        # 控制按钮
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=15)
        
        self.start_button = ttk.Button(control_frame, text="开始恢复", command=self.start_recovery)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="停止", command=self.stop_recovery, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="清空日志", command=self.clear_log).pack(side=tk.LEFT, padx=(0, 10))
        
        # 日志框架
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20)  # 增加日志区域高度
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 进度条
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.pack(pady=(0, 10))
        
        # 配置滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 初始化GPU选项状态
        self.toggle_gpu_options()
        
    def update_threads_label(self):
        """更新线程数标签"""
        self.threads_label.config(text=str(self.threads.get()))
        
    def toggle_gpu_options(self):
        """切换GPU选项状态"""
        if self.enable_gpu.get():
            self.global_ws_entry.config(state="normal")
            self.local_ws_entry.config(state="normal")
        else:
            self.global_ws_entry.config(state="disabled")
            self.local_ws_entry.config(state="disabled")
                    
    def browse_wallet_file(self):
        """浏览钱包文件"""
        filename = filedialog.askopenfilename(
            title="选择钱包文件",
            filetypes=[
                ("所有支持的钱包文件", "*.dat;*.wallet;*.aes;*.json;*.db"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.wallet_file.set(filename)
            
    def browse_password_file(self):
        """浏览密码文件"""
        filename = filedialog.askopenfilename(
            title="选择密码字典文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.password_file.set(filename)
            
    def validate_inputs(self):
        """验证输入参数"""
        if not self.wallet_file.get():
            messagebox.showerror("错误", "请选择钱包文件")
            return False
            
        if not self.password_file.get():
            messagebox.showerror("错误", "请选择密码字典文件")
            return False
            
        if not os.path.exists(self.wallet_file.get()):
            messagebox.showerror("错误", "钱包文件不存在")
            return False
            
        if not os.path.exists(self.password_file.get()):
            messagebox.showerror("错误", "密码字典文件不存在")
            return False
            
        return True
        
    def start_recovery(self):
        """开始密码恢复"""
        if not self.validate_inputs():
            return
            
        if self.is_running:
            return
            
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.status_var.set("正在运行...")
        
        # 清空日志
        self.clear_log()
        self.log_message("开始密码恢复...")
        self.log_message(f"钱包文件: {self.wallet_file.get()}")
        self.log_message(f"密码字典: {self.password_file.get()}")
        self.log_message(f"CPU线程数: {self.threads.get()}")
        if self.enable_gpu.get():
            self.log_message(f"GPU加速: 启用")
            self.log_message(f"全局工作组大小: {self.global_ws.get()}")
            self.log_message(f"本地工作组大小: {self.local_ws.get()}")
        else:
            self.log_message(f"GPU加速: 禁用")
        self.log_message("-" * 50)
        
        # 在新线程中运行恢复过程
        self.recovery_thread = threading.Thread(target=self.run_recovery)
        self.recovery_thread.daemon = True
        self.recovery_thread.start()
        
    def run_recovery(self):
        """运行密码恢复（在后台线程中）"""
        try:
            # 构建命令行
            cmd = [sys.executable, "btcrecover.py"]
            cmd.extend(["--wallet", self.wallet_file.get()])
            cmd.extend(["--passwordlist", self.password_file.get()])
            cmd.extend(["--threads", str(self.threads.get())])
            
            if self.utf8_mode.get():
                cmd.append("--utf8")
                
            if self.enable_gpu.get():
                cmd.append("--enable-gpu")
                cmd.extend(["--global-ws", str(self.global_ws.get())])
                cmd.extend(["--local-ws", str(self.local_ws.get())])
                
            self.log_message(f"执行命令: {' '.join(cmd)}")
            
            # 启动进程
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # 读取输出
            for line in iter(self.process.stdout.readline, ''):
                if not self.is_running:
                    break
                line = line.strip()
                if line:
                    self.progress_queue.put(("log", line))
                    
            # 等待进程结束
            return_code = self.process.wait()
            
            if return_code == 0:
                self.progress_queue.put(("success", "密码恢复完成"))
            else:
                self.progress_queue.put(("error", f"进程退出，返回码: {return_code}"))
                
        except Exception as e:
            self.progress_queue.put(("error", f"发生错误: {str(e)}"))
            
    def stop_recovery(self):
        """停止密码恢复"""
        self.is_running = False
        if self.process:
            self.process.terminate()
        self.log_message("正在停止...")
        
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        
    def check_progress_queue(self):
        """检查进度队列"""
        try:
            while True:
                msg_type, message = self.progress_queue.get_nowait()
                
                if msg_type == "log":
                    self.log_message(message)
                elif msg_type == "success":
                    self.log_message("✓ " + message)
                    self.finish_recovery()
                elif msg_type == "error":
                    self.log_message("✗ " + message)
                    self.finish_recovery()
                    
        except queue.Empty:
            pass
            
        # 继续检查队列
        self.root.after(100, self.check_progress_queue)
        
    def finish_recovery(self):
        """完成恢复过程"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.status_var.set("完成")

def main():
    """主函数"""
    root = tk.Tk()
    app = BtcPassGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 