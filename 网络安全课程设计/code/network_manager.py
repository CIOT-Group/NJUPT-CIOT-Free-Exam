import socket
import threading
import pickle
import traceback
from tkinter import messagebox

class NetworkManager:
    def __init__(self, logger, debug=False, port=12345, key_regeneration_interval=300, callback=None):
        self.logger = logger
        self.debug = debug
        self.port = port # 服务器监听端口
        self.callback = callback # 消息接收回调函数
        self.server_socket = None # 服务器socket
        self.is_server_running = False # 服务器是否正在运行
        self.server_thread = None # 服务器线程
        self.connections = {}  # {ip_address: (socket, public_key)}
        self.pending_connections = {}  # {ip_address: socket} 等待确认的连接
        self.local_ip = self._get_local_ip()
        self.key_regeneration_interval = key_regeneration_interval  # 5分钟(300秒)重新生成一次密钥
        self.key_regeneration_timer = None

    def _get_local_ip(self):
        """获取本机IP地址"""
        try:
            # 创建一个临时socket连接来获取本机IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) # 连接到Google的公共DNS服务器
            ip = s.getsockname()[0] # 获取本机IP地址
            s.close()
            return ip
        except Exception as e:
            self.logger.error(f"获取本机IP失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"无法获取本机IP地址: {str(e)}\n{traceback.format_exc()}")
            return "无法获取IP地址"

    def start_server(self):
        """启动服务器监听连接请求"""
        if self.is_server_running:
            return
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)
            
            self.is_server_running = True
            self.server_thread = threading.Thread(target=self._accept_connections)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.logger.debug(f"服务器已启动，监听端口: {self.port}")
            return True
        except Exception as e:
            self.logger.error(f"启动服务器失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"无法启动服务器: {str(e)}\n{traceback.format_exc()}")
            return False
    
    def _accept_connections(self):
        """接受客户端连接请求的线程函数"""
        while self.is_server_running:
            try:
                client_socket, addr = self.server_socket.accept()
                client_ip = addr[0]
                
                # 启动新线程处理客户端连接
                client_thread = threading.Thread(target=self._handle_client, args=(client_socket, client_ip))
                client_thread.daemon = True
                client_thread.start()
                
                self.logger.debug(f"接受来自 {client_ip} 的连接")
            except Exception as e:
                if self.is_server_running:
                    self.logger.error(f"接受连接时出错: {str(e)}\n{traceback.format_exc()}")
                    messagebox.showerror("错误", f"接受连接时出错: {str(e)}\n{traceback.format_exc()}")
    
    def _handle_client(self, client_socket, client_ip):
        """处理客户端连接的线程函数"""
        try:
            # 接收客户端消息
            while self.is_server_running:
                # 接收消息长度
                length_data = client_socket.recv(4)
                if not length_data:
                    break
                
                message_length = int.from_bytes(length_data, byteorder='big')
                
                # 接收完整消息
                data = b''
                remaining = message_length
                while remaining > 0:
                    chunk = client_socket.recv(min(4096, remaining))
                    if not chunk:
                        break
                    data += chunk
                    remaining -= len(chunk)
                
                if not data:
                    break
                
                # 解析消息
                try:
                    message_dict = pickle.loads(data)
                    message_type = message_dict.get('type')
                    
                    # 处理连接请求
                    if message_type == 'connection_request':
                        self.logger.debug(f"收到来自 {client_ip} 的连接请求")
                        # 将连接放入待确认列表
                        self.pending_connections[client_ip] = client_socket
                        
                        # 通知UI有新的连接请求
                        if self.callback:
                            self.callback({
                                'type': 'connection_request',
                                'ip': client_ip
                            })
                    
                    # 处理连接确认
                    elif message_type == 'connection_accepted':
                        self.logger.debug(f"{client_ip} 已接受连接请求")
                        # 将连接添加到连接列表
                        self.connections[client_ip] = (client_socket, None)
                        
                        # 通知UI连接已确认
                        if self.callback:
                            self.callback({
                                'type': 'connection_accepted',
                                'ip': client_ip
                            })
                    
                    # 处理连接拒绝
                    elif message_type == 'connection_rejected':
                        self.logger.warning(f"{client_ip} 拒绝了连接请求")
                        
                        # 通知UI连接被拒绝
                        if self.callback:
                            self.callback({
                                'type': 'connection_rejected',
                                'ip': client_ip
                            })
                    
                    # 处理公钥交换
                    elif message_type == 'public_key':
                        public_key_pem = message_dict.get('data')
                        self.logger.debug(f"接收到来自 {client_ip} 的公钥")
                        
                        # 更新连接信息
                        if client_ip in self.connections:
                            socket_obj, _ = self.connections[client_ip]
                            self.connections[client_ip] = (socket_obj, public_key_pem)
                        
                        # 如果提供了回调，通知UI更新公钥状态
                        if self.callback:
                            self.callback({
                                'type': 'public_key_received',
                                'ip': client_ip,
                                'public_key': public_key_pem
                            })
                    
                    # 处理文本消息
                    elif message_type == 'text':
                        message = message_dict.get('data')
                        signature = message_dict.get('signature')
                        self.logger.debug(f"接收到来自 {client_ip} 的文本消息")
                        
                        # 如果提供了回调，通知UI显示消息
                        if self.callback:
                            self.callback({
                                'type': 'text_message',
                                'ip': client_ip,
                                'message': message,
                                'signature': signature
                            })
                    
                    # 处理文件消息
                    elif message_type == 'file':
                        filename = message_dict.get('filename')
                        file_data = message_dict.get('data')
                        signature = message_dict.get('signature')
                        self.logger.debug(f"接收到来自 {client_ip} 的文件: {filename}")
                        
                        # 如果提供了回调，通知UI显示文件
                        if self.callback:
                            self.callback({
                                'type': 'file_message',
                                'ip': client_ip,
                                'filename': filename,
                                'data': file_data,
                                'signature': signature
                            })
                    
                except Exception as e:
                    self.logger.error(f"解析消息时出错: {str(e)}\n{traceback.format_exc()}")
                    messagebox.showerror("错误", f"解析消息时出错: {str(e)}\n{traceback.format_exc()}")
                
        except Exception as e:
            self.logger.error(f"处理客户端 {client_ip} 连接时出错: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"处理客户端连接时出错: {str(e)}\n{traceback.format_exc()}")
        finally:
            # 关闭连接
            try:
                client_socket.close()
                self.logger.debug(f"关闭与 {client_ip} 的连接")
            except:
                pass
            
            # 从连接列表中移除
            if client_ip in self.connections:
                del self.connections[client_ip]
                
                # 通知UI客户端已断开连接
                if self.callback:
                    self.callback({
                        'type': 'client_disconnected',
                        'ip': client_ip
                    })
                
                self.logger.debug(f"客户端 {client_ip} 已断开连接")
            
            # 从待确认列表中移除
            if client_ip in self.pending_connections:
                del self.pending_connections[client_ip]

    def connect_to_server(self, server_ip):
        """连接到服务器"""
        if server_ip in self.connections:
            return True  # 已连接
            
        try:
            # 创建新socket连接到服务器
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, self.port))
            
            # 将连接添加到连接列表
            self.connections[server_ip] = (client_socket, None)
            
            # 启动线程处理服务器响应
            client_thread = threading.Thread(target=self._handle_client, args=(client_socket, server_ip))
            client_thread.daemon = True
            client_thread.start()
            
            self.logger.debug(f"成功连接到服务器: {server_ip}")
            return True
        except Exception as e:
            self.logger.error(f"连接到服务器 {server_ip} 失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"连接到服务器 {server_ip} 失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def request_connection(self, server_ip):
        """向服务器发送连接请求"""
        if server_ip in self.connections:
            return True  # 已连接
            
        try:
            # 创建新socket连接到服务器
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, self.port))
            
            # 将连接添加到待确认列表
            self.pending_connections[server_ip] = client_socket
            
            # 启动线程处理服务器响应
            client_thread = threading.Thread(target=self._handle_client, args=(client_socket, server_ip))
            client_thread.daemon = True
            client_thread.start()
            
            # 发送连接请求
            message = {
                'type': 'connection_request'
            }
            self._send_message_with_socket(client_socket, message)
            
            self.logger.debug(f"已向 {server_ip} 发送连接请求")
            return True
        except Exception as e:
            self.logger.error(f"连接到服务器 {server_ip} 失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"连接到服务器 {server_ip} 失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def accept_connection(self, client_ip):
        """接受连接请求"""
        if client_ip not in self.pending_connections:
            self.logger.error(f"接受连接失败: 没有来自 {client_ip} 的待处理连接请求")
            return False
        
        try:
            # 获取socket
            client_socket = self.pending_connections[client_ip]
            
            # 将连接从待确认列表移到已连接列表
            self.connections[client_ip] = (client_socket, None)
            del self.pending_connections[client_ip]
            
            # 发送接受连接的消息
            message = {
                'type': 'connection_accepted'
            }
            self._send_message_with_socket(client_socket, message)
            
            self.logger.debug(f"已接受来自 {client_ip} 的连接请求")
            return True
        except Exception as e:
            self.logger.error(f"接受来自 {client_ip} 的连接请求失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"接受连接请求失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def reject_connection(self, client_ip):
        """拒绝连接请求"""
        if client_ip not in self.pending_connections:
            self.logger.error(f"拒绝连接失败: 没有来自 {client_ip} 的待处理连接请求")
            return False
        
        try:
            # 获取socket
            client_socket = self.pending_connections[client_ip]
            
            # 发送拒绝连接的消息
            message = {
                'type': 'connection_rejected'
            }
            self._send_message_with_socket(client_socket, message)
            
            # 关闭连接
            client_socket.close()
            
            # 从待确认列表中移除
            del self.pending_connections[client_ip]
            
            self.logger.debug(f"已拒绝来自 {client_ip} 的连接请求")
            return True
        except Exception as e:
            self.logger.error(f"拒绝来自 {client_ip} 的连接请求失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"拒绝连接请求失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def send_public_key(self, target_ip, public_key_pem):
        """发送公钥给目标IP"""
        if target_ip not in self.connections:
            self.logger.error(f"发送公钥失败: 未连接到 {target_ip}")
            return False
        
        try:
            # 准备消息
            message = {
                'type': 'public_key',
                'data': public_key_pem
            }
            
            # 发送消息
            self._send_message(target_ip, message)
            self.logger.debug(f"已将公钥发送给 {target_ip}")
            return True
        except Exception as e:
            self.logger.error(f"发送公钥给 {target_ip} 失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"发送公钥失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def send_text_message(self, target_ip, message, signature):
        """发送文本消息给目标IP"""
        if target_ip not in self.connections:
            self.logger.error(f"发送消息失败: 未连接到 {target_ip}")
            return False
            
        try:
            # 准备消息
            message_dict = {
                'type': 'text',
                'data': message,
                'signature': signature
            }
            
            # 发送消息
            self._send_message(target_ip, message_dict)
            self.logger.debug(f"已将文本消息发送给 {target_ip}")
            return True
        except Exception as e:
            self.logger.error(f"发送文本消息给 {target_ip} 失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"发送文本消息失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def send_file(self, target_ip, filename, file_data, signature):
        """发送文件给目标IP"""
        if target_ip not in self.connections:
            self.logger.error(f"发送文件失败: 未连接到 {target_ip}")
            return False
            
        try:
            # 准备消息
            message = {
                'type': 'file',
                'filename': filename,
                'data': file_data,
                'signature': signature
            }
            
            # 发送消息
            self._send_message(target_ip, message)
            self.logger.debug(f"已将文件 {filename} 发送给 {target_ip}")
            return True
        except Exception as e:
            self.logger.error(f"发送文件给 {target_ip} 失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("错误", f"发送文件失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def _send_message(self, target_ip, message_dict):
        """发送消息的底层方法"""
        if target_ip not in self.connections:
            self.logger.error(f"发送消息失败: 未连接到 {target_ip}")
            messagebox.showerror("错误", f"发送消息失败: 未连接到 {target_ip}")
            raise Exception(f"未连接到 {target_ip}\n{traceback.format_exc()}")
        
        client_socket = self.connections[target_ip][0]
        
        # 序列化消息
        data = pickle.dumps(message_dict)
        
        # 发送消息长度
        length = len(data)
        client_socket.sendall(length.to_bytes(4, byteorder='big'))
        
        # 发送消息内容
        client_socket.sendall(data)

    @staticmethod
    def _send_message_with_socket(socket_obj, message_dict):
        """使用指定socket发送消息"""
        # 序列化消息
        data = pickle.dumps(message_dict)
        
        # 发送消息长度
        length = len(data)
        socket_obj.sendall(length.to_bytes(4, byteorder='big'))
        
        # 发送消息内容
        socket_obj.sendall(data)

    def get_public_key(self, ip):
        """获取指定IP的公钥"""
        if ip in self.connections:
            return self.connections[ip][1]
        return None

    def get_connected_clients(self):
        """获取所有已连接的客户端IP"""
        return list(self.connections.keys())

    def get_pending_connections(self):
        """获取所有待确认的连接请求"""
        return list(self.pending_connections.keys())

    def is_connected(self, ip):
        """检查是否已连接到指定IP"""
        return ip in self.connections

    def stop_server(self):
        """停止服务器"""
        self.is_server_running = False
        
        # 关闭所有连接
        for ip, (socket_obj, _) in list(self.connections.items()):
            try:
                socket_obj.close()
            except:
                pass
            
        # 关闭服务器socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            
        self.logger.debug("服务器已停止")

    def start_key_regeneration_timer(self):
        """启动密钥重新生成定时器"""
        if self.key_regeneration_timer:
            self.key_regeneration_timer.cancel()
        
        self.key_regeneration_timer = threading.Timer(
            self.key_regeneration_interval,
            self._regenerate_and_exchange_keys
        )
        self.key_regeneration_timer.daemon = True
        self.key_regeneration_timer.start()

    def _regenerate_and_exchange_keys(self):
        """重新生成密钥并与所有已连接的对等方交换"""
        if not hasattr(self, 'key_manager'):
            self.logger.debug("密钥管理器不可用，跳过密钥重新生成")
            return
        
        try:
            # 重新生成密钥
            if self.key_manager.regenerate_keys():
                self.logger.debug("本地密钥对已重新生成")
                
                # 获取新的公钥
                public_key_pem = self.key_manager.get_public_key_pem()
                if public_key_pem:
                    # 向所有已连接的对等方发送新公钥
                    for ip in self.get_connected_clients():
                        self.send_public_key(ip, public_key_pem)
                        self.logger.info(f"已向 {ip} 发送新的公钥")
        except Exception as e:
            self.logger.error(f"密钥重新生成和交换过程中出错: {str(e)}\n{traceback.format_exc()}")
        finally:
            # 重新启动定时器
            self.start_key_regeneration_timer()

    def set_key_manager(self, key_manager):
        """设置密钥管理器引用"""
        self.key_manager = key_manager
        # 首次启动定时器
        self.start_key_regeneration_timer()