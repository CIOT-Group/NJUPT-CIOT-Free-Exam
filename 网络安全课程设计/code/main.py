import os
import tkinter as tk
import logging
from tkinter import ttk, filedialog, messagebox, scrolledtext
from key_manager import KeyManager
from network_manager import NetworkManager
from logger import get_logger, set_log_level
import traceback


class SecureMessagingApp:
    def __init__(self, root, isdebug=False, key_regeneration_interval=300):
        """初始化应用程序"""
        self.root = root
        self.root.title("基于 RSA 数字签名应用程序设计与实现")
        self.root.geometry("600x500") # 窗口大小
        self.root.resizable(True, True)
        self.logger = get_logger(console_level=logging.INFO)
        self.debug = isdebug
        self.key_regeneration_interval = key_regeneration_interval
        
        if self.debug:
            set_log_level(self.logger, logging.DEBUG)
        
        # 初始化密钥管理器
        self.key_manager = KeyManager(logger=self.logger, debug=self.debug)
        
        # 初始化网络管理器
        self.network_manager = NetworkManager(logger=self.logger, debug=self.debug, key_regeneration_interval=self.key_regeneration_interval, callback=self.handle_network_message)
        self.network_manager.set_key_manager(self.key_manager)
        
        # 存储接收到的文件内容
        self.received_files = {}  # {ip: (filename, data, signature)}
        
        # 启动服务器
        if self.network_manager.start_server():
            self.logger.info("服务器已成功启动")
        else:
            self.logger.error("服务器启动失败")
        
        # 创建GUI界面
        self.create_main_widgets()
        
        # 启动定时刷新任务
        self.schedule_refresh()

    def schedule_refresh(self):
        """定时刷新连接列表"""
        self.refresh_connections()
        self.refresh_pending_connections()
        # 每5秒刷新一次
        self.root.after(5000, self.schedule_refresh)

    def create_main_widgets(self):
        """创建主应用界面"""
        # 显示当前用户IP
        user_frame = ttk.Frame(self.root, padding="5")
        user_frame.pack(fill='x')

        # 显示IP地址
        ttk.Label(
            user_frame,
            text=f"本机IP: {self.network_manager.local_ip}",
            font=("Helvetica", 12),
            foreground="blue"
        ).pack(side='left', padx=10)
        
        # 创建标签页控件
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 连接管理标签页
        conn_frame = ttk.Frame(notebook)
        notebook.add(conn_frame, text='连接管理')
        
        # 消息通信标签页
        msg_frame = ttk.Frame(notebook)
        notebook.add(msg_frame, text='消息通信')
        
        # 文件传输标签页
        file_frame = ttk.Frame(notebook)
        notebook.add(file_frame, text='文件传输')
        
        # 创建连接管理页面组件
        self.create_connection_widgets(conn_frame)
        
        # 创建消息通信页面组件
        self.create_message_widgets(msg_frame)
        
        # 创建文件传输页面组件
        self.create_file_transfer_widgets(file_frame)

    def create_connection_widgets(self, parent):
        """创建连接管理界面"""
        # 连接到服务器区域
        connect_frame = ttk.LabelFrame(parent, text="连接到其他用户")
        connect_frame.pack(fill='x', expand=True, padx=10, pady=5)
        
        ttk.Label(connect_frame, text="目标IP地址:").grid(row=0, column=0, padx=5, pady=5)
        self.target_ip_entry = ttk.Entry(connect_frame, width=30)
        self.target_ip_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(connect_frame, text="发送连接请求", command=self.request_connection).grid(row=0, column=2, padx=5, pady=5)
        
        # 待确认连接请求区域
        pending_frame = ttk.LabelFrame(parent, text="待确认连接请求")
        pending_frame.pack(fill='x', expand=True, padx=10, pady=5)
        
        # 创建表格显示待确认连接
        columns = ('ip', 'status')
        self.pending_tree = ttk.Treeview(pending_frame, columns=columns, show='headings', height=3)
        
        # 设置列标题
        self.pending_tree.heading('ip', text='发送方IP地址')
        self.pending_tree.heading('status', text='状态')
        
        # 设置列宽
        self.pending_tree.column('ip', width=200)
        self.pending_tree.column('status', width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(pending_frame, orient=tk.VERTICAL, command=self.pending_tree.yview)
        self.pending_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pending_tree.pack(fill='both', expand=True)
        
        # 按钮区域
        button_frame = ttk.Frame(pending_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="接受", command=self.accept_connection_request).pack(side='right', padx=5)
        ttk.Button(button_frame, text="拒绝", command=self.reject_connection_request).pack(side='right', padx=5)
        
        # 已连接用户列表
        connections_frame = ttk.LabelFrame(parent, text="已连接用户")
        connections_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 创建表格显示已连接用户
        columns = ('ip', 'status', 'key_status')
        self.connections_tree = ttk.Treeview(connections_frame, columns=columns, show='headings')
        
        # 设置列标题
        self.connections_tree.heading('ip', text='IP地址')
        self.connections_tree.heading('status', text='连接状态')
        self.connections_tree.heading('key_status', text='公钥状态')
        
        # 设置列宽
        self.connections_tree.column('ip', width=200)
        self.connections_tree.column('status', width=100)
        self.connections_tree.column('key_status', width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(connections_frame, orient=tk.VERTICAL, command=self.connections_tree.yview)
        self.connections_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.connections_tree.pack(fill='both', expand=True)
        
        # 刷新连接按钮
        ttk.Button(connections_frame, text="刷新连接列表", command=self.refresh_connections).pack(side='right', padx=5, pady=5)

    def create_message_widgets(self, parent):
        """创建消息通信界面"""
        # 发送消息区域
        send_frame = ttk.LabelFrame(parent, text="发送消息")
        send_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Label(send_frame, text="目标IP:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.message_target_ip = ttk.Combobox(send_frame, width=30)
        self.message_target_ip.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(send_frame, text="消息内容:").grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        self.message_input = scrolledtext.ScrolledText(send_frame, wrap=tk.WORD, width=60, height=5)
        self.message_input.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Button(send_frame, text="发送", command=self.send_message).grid(row=2, column=1, padx=5, pady=5, sticky='e')
        
        # 接收消息区域
        recv_frame = ttk.LabelFrame(parent, text="接收消息")
        recv_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Label(recv_frame, text="发送者IP:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.message_sender_ip = ttk.Label(recv_frame, text="无")
        self.message_sender_ip.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(recv_frame, text="收到的消息:").grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        self.received_message = scrolledtext.ScrolledText(recv_frame, wrap=tk.WORD, width=60, height=5)
        self.received_message.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(recv_frame, text="签名验证:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.signature_verification = ttk.Label(recv_frame, text="待验证")
        self.signature_verification.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def create_file_transfer_widgets(self, parent):
        """创建文件传输界面"""
        # 发送文件区域
        send_frame = ttk.LabelFrame(parent, text="发送文件")
        send_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Label(send_frame, text="目标IP:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.file_target_ip = ttk.Combobox(send_frame, width=30)
        self.file_target_ip.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Button(send_frame, text="选择文件", command=self.select_file).grid(row=1, column=0, padx=5, pady=5)
        self.file_path = ttk.Label(send_frame, text="未选择文件")
        self.file_path.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Button(send_frame, text="发送", command=self.send_file).grid(row=2, column=1, padx=5, pady=5, sticky='e')
        
        # 接收文件区域
        recv_frame = ttk.LabelFrame(parent, text="接收文件")
        recv_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Label(recv_frame, text="发送者IP:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.file_sender_ip = ttk.Label(recv_frame, text="无")
        self.file_sender_ip.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(recv_frame, text="收到的文件:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.file_received = ttk.Label(recv_frame, text="无")
        self.file_received.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(recv_frame, text="签名验证:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.file_verification = ttk.Label(recv_frame, text="待验证")
        self.file_verification.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Button(recv_frame, text="保存文件", command=self.save_received_file).grid(row=3, column=1, padx=5, pady=5, sticky='e')

    def request_connection(self):
        """向目标服务器发送连接请求"""
        target_ip = self.target_ip_entry.get().strip()
        
        if not target_ip:
            self.logger.error("目标IP地址不能为空")
            messagebox.showerror("错误", "请输入目标IP地址")
            return

        # 检查是否为有效IP
        import re
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', target_ip):
            self.logger.error("无效的IP地址")
            messagebox.showerror("错误", "请输入有效的IP地址")
            return

        # 如果已连接，不再重复连接
        if self.network_manager.is_connected(target_ip):
            self.logger.warning("已经连接到目标IP, 不需要重复连接")
            messagebox.showinfo("提示", f"已经连接到 {target_ip}")
            return

        # 发送连接请求
        if self.network_manager.request_connection(target_ip):
            self.logger.info(f"已向 {target_ip} 发送连接请求，等待对方确认...")
            messagebox.showinfo("成功", f"已向 {target_ip} 发送连接请求")
        else:
            self.logger.error(f"发送连接请求到 {target_ip} 失败")
            messagebox.showerror("错误", f"发送连接请求到 {target_ip} 失败")

    def accept_connection_request(self):
        """接受连接请求"""
        # 获取选中的连接请求
        selected_item = self.pending_tree.selection()
        if not selected_item:
            self.logger.error("没有选中任何连接请求")
            messagebox.showerror("错误", "请先选择一个连接请求")
            return
        
        # 获取IP地址
        client_ip = self.pending_tree.item(selected_item[0], 'values')[0]
        self.logger.debug(f"接受连接请求来自 {client_ip}")
        
        # 接受连接请求
        if self.network_manager.accept_connection(client_ip):
            self.logger.info(f"已接受来自 {client_ip} 的连接请求")
            
            # 发送公钥
            public_key_pem = self.key_manager.get_public_key_pem()
            if public_key_pem:
                self.network_manager.send_public_key(client_ip, public_key_pem)
                self.logger.debug(f"已发送公钥给 {client_ip}")
            
            # 更新连接列表
            self.refresh_connections()
            self.refresh_pending_connections()
        else:
            self.logger.error(f"接受来自 {client_ip} 的连接请求失败")
            messagebox.showerror("错误", f"接受来自 {client_ip} 的连接请求失败")

    def reject_connection_request(self):
        """拒绝连接请求"""
        # 获取选中的连接请求
        selected_item = self.pending_tree.selection()
        if not selected_item:
            self.logger.error("没有选中任何连接请求")
            messagebox.showerror("错误", "请先选择一个连接请求")
            return
        
        # 获取IP地址
        client_ip = self.pending_tree.item(selected_item[0], 'values')[0]
        self.logger.debug(f"拒绝连接请求来自 {client_ip}")
        
        # 拒绝连接请求
        if self.network_manager.reject_connection(client_ip):
            self.logger.info(f"已拒绝来自 {client_ip} 的连接请求")
            self.refresh_pending_connections()
        else:
            self.logger.error(f"拒绝来自 {client_ip} 的连接请求失败")
            messagebox.showerror("错误", f"拒绝来自 {client_ip} 的连接请求失败")

    def refresh_pending_connections(self):
        """刷新待确认连接列表"""
        # 清空现有连接列表
        for item in self.pending_tree.get_children():
            self.pending_tree.delete(item)

        # 获取待确认的连接请求
        pending_connections = self.network_manager.get_pending_connections()
        
        # 向列表中添加连接信息
        for ip in pending_connections:
            self.pending_tree.insert('', 'end', values=(ip, "等待确认"))

    def refresh_connections(self):
        """刷新连接列表"""
        # 清空现有连接列表
        for item in self.connections_tree.get_children():
            self.connections_tree.delete(item)
        
        # 获取已连接的客户端
        connected_clients = self.network_manager.get_connected_clients()
        
        # 向列表中添加连接信息
        for ip in connected_clients:
            status = "已连接"
            key_status = "已接收" if self.key_manager.has_peer_public_key(ip) else "未接收"
            self.connections_tree.insert('', 'end', values=(ip, status, key_status))
            
        # 更新下拉框选项
        self.message_target_ip['values'] = connected_clients
        self.file_target_ip['values'] = connected_clients
        
        if connected_clients:
            self.message_target_ip.current(0)
            self.file_target_ip.current(0)

    def handle_network_message(self, message_dict):
        """处理网络消息的回调函数"""
        message_type = message_dict.get('type')
        ip = message_dict.get('ip')
        
        # 处理不同类型的消息
        if message_type == 'connection_request':
            # 收到连接请求
            self.logger.info(f"收到来自 {ip} 的连接请求")
            
            # 更新待确认连接列表
            self.refresh_pending_connections()
            
            # 提示用户有新的连接请求
            messagebox.showinfo("连接请求", f"收到来自 {ip} 的连接请求，请前往连接管理页面确认")
        
        elif message_type == 'connection_accepted':
            # 连接请求被接受
            self.logger.info(f"{ip} 已接受连接请求")
            
            # 发送公钥
            public_key_pem = self.key_manager.get_public_key_pem()
            if public_key_pem:
                self.network_manager.send_public_key(ip, public_key_pem)
                self.logger.debug(f"已发送公钥给 {ip}")
            
            # 更新连接列表
            self.refresh_connections()
            
            messagebox.showinfo("连接成功", f"{ip} 已接受您的连接请求")
        
        elif message_type == 'connection_rejected':
            # 连接请求被拒绝
            self.logger.info(f"{ip} 拒绝了连接请求")
            messagebox.showinfo("连接拒绝", f"{ip} 拒绝了您的连接请求")
        
        elif message_type == 'public_key_received':
            # 收到公钥
            public_key = message_dict.get('public_key')
            if public_key:
                self.key_manager.add_peer_public_key(ip, public_key)
                self.logger.debug(f"已接收并保存来自 {ip} 的公钥")
                
                # 更新连接列表
                self.refresh_connections()
        
        elif message_type == 'text_message':
            # 收到文本消息
            message = message_dict.get('message')
            self.logger.debug(f"收到来自 {ip} 的消息: {message}")
            signature = message_dict.get('signature')
            self.logger.debug(f"收到来自 {ip} 的签名: {signature}")
            
            # 更新UI
            self.received_message.delete("1.0", tk.END)
            self.received_message.insert(tk.END, message)
            self.message_sender_ip.config(text=ip)
            
            # 验证签名
            if self.key_manager.has_peer_public_key(ip):
                is_valid = self.key_manager.verify_signature(message, signature, ip)
                
                if is_valid:
                    self.signature_verification.config(text="✓ 签名有效，消息完整", foreground="green")
                    self.logger.info(f"收到来自 {ip} 的消息，签名有效")
                else:
                    self.signature_verification.config(text="✗ 签名无效，消息可能被篡改", foreground="red")
                    self.logger.warning(f"收到来自 {ip} 的消息，但签名无效")
            else:
                self.signature_verification.config(text="? 无法验证（未接收到发送者公钥）", foreground="orange")
                self.logger.warning(f"收到来自 {ip} 的消息，但没有公钥无法验证签名")
        
        elif message_type == 'file_message':
            # 收到文件
            filename = message_dict.get('filename')
            self.logger.debug(f"收到来自 {ip} 的文件: {filename}")
            file_data = message_dict.get('data')
            self.logger.debug(f"收到来自 {ip} 的文件数据")
            signature = message_dict.get('signature')
            self.logger.debug(f"收到来自 {ip} 的文件签名: {signature}")
            
            # 保存接收到的文件信息
            self.received_files[ip] = (filename, file_data, signature)
            
            # 更新UI
            self.file_received.config(text=filename)
            self.file_sender_ip.config(text=ip)
            
            # 验证签名
            if self.key_manager.has_peer_public_key(ip):
                is_valid = self.key_manager.verify_signature(file_data, signature, ip)
                
                if is_valid:
                    self.file_verification.config(text="✓ 签名有效，文件完整", foreground="green")
                    self.logger.info(f"收到来自 {ip} 的文件 {filename}，签名有效")
                else:
                    self.file_verification.config(text="✗ 签名无效，文件可能被篡改", foreground="red")
                    self.logger.warning(f"收到来自 {ip} 的文件 {filename}，但签名无效")
            else:
                self.file_verification.config(text="? 无法验证（未接收到发送者公钥）", foreground="orange")
                self.logger.warning(f"收到来自 {ip} 的文件 {filename}，但没有公钥无法验证签名")
        
        elif message_type == 'client_disconnected':
            # 客户端断开连接
            self.logger.warning(f"客户端 {ip} 已断开连接")
            # 更新连接列表
            self.refresh_connections()
    
    def send_message(self):
        """发送消息"""
        target_ip = self.message_target_ip.get().strip()
        message = self.message_input.get("1.0", tk.END).strip()
        
        if not target_ip:
            self.logger.error("目标IP地址不能为空")
            messagebox.showerror("错误", "请选择目标IP地址")
            return
        
        if not message:
            self.logger.error("消息内容不能为空")
            messagebox.showerror("错误", "消息内容不能为空")
            return
        
        # 检查是否已连接
        if not self.network_manager.is_connected(target_ip):
            self.logger.error(f"未连接到 {target_ip}")
            messagebox.showerror("错误", f"未连接到 {target_ip}")
            return
        
        # 签名消息
        signature = self.key_manager.sign_message(message)
        if not signature:
            self.logger.error("消息签名失败")
            messagebox.showerror("错误", "消息签名失败")
            return
        
        # 发送消息
        if self.network_manager.send_text_message(target_ip, message, signature):
            self.logger.info(f"已发送消息给 {target_ip}")
            self.message_input.delete("1.0", tk.END)
            messagebox.showinfo("成功", "消息已发送")
        else:
            self.logger.error("发送消息失败")
            messagebox.showerror("错误", "发送消息失败")
    
    def select_file(self):
        """选择要发送的文件"""
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        
        self.selected_file_path = filepath
        self.file_path.config(text=os.path.basename(filepath))
        self.logger.info(f"已选择文件: {os.path.basename(filepath)}")
    
    def send_file(self):
        """发送文件"""
        target_ip = self.file_target_ip.get().strip()
        
        if not target_ip:
            self.logger.error("目标IP地址不能为空")
            messagebox.showerror("错误", "请选择目标IP地址")
            return
        
        if not hasattr(self, 'selected_file_path') or not self.selected_file_path:
            self.logger.error("未选择文件")
            messagebox.showerror("错误", "请先选择要发送的文件")
            return
        
        # 检查是否已连接
        if not self.network_manager.is_connected(target_ip):
            self.logger.error(f"未连接到 {target_ip}")
            messagebox.showerror("错误", f"未连接到 {target_ip}")
            return
        
        try:
            # 读取文件内容
            with open(self.selected_file_path, 'rb') as f:
                file_data = f.read()
            
            # 对文件内容进行签名
            signature = self.key_manager.sign_message(file_data)
            if not signature:
                self.logger.error("文件签名失败")
                messagebox.showerror("错误", "文件签名失败")
                return
                
            # 获取文件名
            filename = os.path.basename(self.selected_file_path)
            
            # 发送文件
            if self.network_manager.send_file(target_ip, filename, file_data, signature):
                self.logger.info(f"已发送文件给 {target_ip}: {filename}")
                messagebox.showinfo("成功", "文件已发送")
            else:
                self.logger.error("发送文件失败")
                messagebox.showerror("错误", "发送文件失败")
        except Exception as e:
            error_msg = f"发送文件失败: {str(e)}\n{traceback.format_exc()}"
            self.logger.error(error_msg)
            messagebox.showerror("错误", error_msg)
    
    def save_received_file(self):
        """保存接收到的文件"""
        sender_ip = self.file_sender_ip.cget("text")
        
        if sender_ip == "无" or sender_ip not in self.received_files:
            self.logger.error("没有接收到文件")
            messagebox.showerror("错误", "没有接收到文件")
            return
        
        filename, file_data, _ = self.received_files[sender_ip]
        
        # 选择保存位置
        filetypes = [("All Files", "*.*")]
        filepath = filedialog.asksaveasfilename(
            defaultextension=".*",
            filetypes=filetypes,
            initialfile=filename
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'wb') as f:
                f.write(file_data)
            self.logger.info(f"文件已保存到: {filepath}")
            messagebox.showinfo("成功", "文件已保存")
        except Exception as e:
            error_msg = f"保存文件失败: {str(e)}\n{traceback.format_exc()}"
            self.logger.error(error_msg)
            messagebox.showerror("错误", error_msg)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--key_regeneration_interval", type=int, default=300, help="Key regeneration interval in seconds")
    args = parser.parse_args()

    root = tk.Tk()
    SecureMessagingApp(root=root, isdebug=args.debug, key_regeneration_interval=args.key_regeneration_interval)
    root.mainloop()