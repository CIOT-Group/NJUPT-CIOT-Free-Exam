import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64
import json
import traceback
from tkinter import messagebox

class KeyManager:
    def __init__(self, logger, debug=False, keys_dir="keys"):
        self.logger = logger
        self.debug = debug
        self.keys_dir = keys_dir
        self.private_key_path = os.path.join(keys_dir, "private_key.pem")
        self.public_key_path = os.path.join(keys_dir, "public_key.pem")
        self.peer_keys_dir = os.path.join(keys_dir, "peer_keys")  # 存储对方公钥的目录
        self.peer_keys_index = os.path.join(self.peer_keys_dir, "index.json")  # 公钥索引文件

        self.private_key = None
        self.public_key = None
        self.peer_public_keys = {}  # {ip_address: public_key}

        # 确保密钥目录存在
        os.makedirs(keys_dir, exist_ok=True)
        os.makedirs(self.peer_keys_dir, exist_ok=True)  # 确保对方公钥目录存在

        # 检查是否已有密钥，没有则生成
        self.ensure_keys_exist()

        # 加载对方公钥
        self.load_peer_public_keys()

    def ensure_keys_exist(self):
        """确保密钥存在，如不存在则生成"""
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            # 加载已有密钥
            self.load_keys()
            self.logger.debug("已加载本地密钥对")
        else:
            # 生成新密钥对
            self.generate_keys()
            self.logger.debug("已生成新的密钥对")

    def generate_keys(self, key_size=2048):
        """生成RSA密钥对"""
        try:
            # 生成私钥
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend()
            )

            # 获取对应的公钥
            self.public_key = self.private_key.public_key()

            # 保存密钥到文件
            self.save_keys()

            return True
        except Exception as e:
            self.logger.error(f"生成密钥对失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("密钥生成失败", f"生成密钥对失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def save_keys(self):
        """将密钥保存到文件"""
        try:
            # 保存私钥
            with open(self.private_key_path, "wb") as f:
                f.write(
                    self.private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    )
                )

            # 保存公钥
            with open(self.public_key_path, "wb") as f:
                f.write(
                    self.public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                )

            return True
        except Exception as e:
            self.logger.error(f"保存密钥对失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("密钥保存失败", f"保存密钥对失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def load_keys(self):
        """从文件加载密钥"""
        try:
            # 加载私钥
            with open(self.private_key_path, "rb") as f:
                self.private_key = serialization.load_pem_private_key(
                    data=f.read(),
                    password=None,
                    backend=default_backend()
                )

            # 加载公钥
            with open(self.public_key_path, "rb") as f:
                self.public_key = serialization.load_pem_public_key(
                    data=f.read(),
                    backend=default_backend()
                )

            return True
        except Exception as e:
            self.logger.error(f"加载密钥对失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("密钥加载失败", f"加载密钥对失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def load_peer_public_keys(self):
        """从文件加载对方的公钥"""
        try:
            # 如果索引文件存在，读取IP和公钥文件的映射
            if os.path.exists(self.peer_keys_index):
                with open(self.peer_keys_index, 'r') as f:
                    peer_keys_map = json.load(f)
                self.logger.debug(f"已加载对方公钥索引: {peer_keys_map}")

                # 加载每个IP对应的公钥
                for ip, filename in peer_keys_map.items():
                    key_path = os.path.join(self.peer_keys_dir, filename)
                    if os.path.exists(key_path):
                        try:
                            with open(key_path, 'rb') as key_file:
                                public_key = serialization.load_pem_public_key(
                                    data=key_file.read(),
                                    backend=default_backend()
                                )
                                self.peer_public_keys[ip] = public_key
                                self.logger.debug(f"已从文件加载 {ip} 的公钥")
                        except Exception as e:
                            self.logger.error(f"加载 {ip} 的公钥失败: {str(e)}\n{traceback.format_exc()}")
                            messagebox.showerror("公钥加载失败", f"加载 {ip} 的公钥失败: {str(e)}\n{traceback.format_exc()}")

            self.logger.debug(f"已加载 {len(self.peer_public_keys)} 个对方公钥")
            return True
        except Exception as e:
            self.logger.error(f"加载对方公钥失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("公钥加载失败", f"加载对方公钥失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def save_peer_public_keys(self):
        """将对方公钥保存到文件"""
        try:
            # 创建IP到文件名的映射
            peer_keys_map = {} # {ip_address: filename}

            # 保存每个IP的公钥
            for ip, public_key in self.peer_public_keys.items():
                # 生成安全的文件名（IP中的点可能导致文件路径问题）
                filename = f"peer_key_{ip.replace('.', '_')}.pem"
                key_path = os.path.join(self.peer_keys_dir, filename)

                # 保存公钥到文件
                with open(key_path, 'wb') as f:
                    f.write(
                        public_key.public_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo
                        )
                    )

                # 添加到映射
                peer_keys_map[ip] = filename

            # 保存映射到索引文件
            self.logger.debug(f"对方公钥索引: {peer_keys_map}")
            with open(self.peer_keys_index, 'w') as f:
                json.dump(peer_keys_map, f, indent=2)
            self.logger.debug(f"已保存 {len(self.peer_public_keys)} 个对方公钥到文件")
            return True
        except Exception as e:
            self.logger.error(f"保存对方公钥失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("公钥保存失败", f"保存对方公钥失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def get_public_key_pem(self):
        """获取PEM格式的公钥"""
        if not self.public_key:
            return None

        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def add_peer_public_key(self, ip, public_key_pem):
        """添加对等方的公钥"""
        try:
            if isinstance(public_key_pem, bytes):
                public_key = serialization.load_pem_public_key(
                    data=public_key_pem,
                    backend=default_backend()
                )
                self.peer_public_keys[ip] = public_key

                # 将公钥保存到文件
                self.save_peer_public_keys()

                self.logger.debug(f"已添加并保存 {ip} 的公钥")
                return True
            return False
        except Exception as e:
            self.logger.error(f"添加对等方公钥失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("公钥添加失败", f"添加对等方公钥失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def sign_message(self, message):
        """对消息进行签名"""
        if not self.private_key:
            self.logger.error("签名失败: 私钥不可用")
            return None

        try:
            if isinstance(message, str):
                message = message.encode('utf-8')

            signature = self.private_key.sign(
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            self.logger.debug("消息签名成功")
            return base64.b64encode(signature).decode('utf-8')
        except Exception as e:
            self.logger.error(f"签名失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("签名失败", f"签名失败: {str(e)}\n{traceback.format_exc()}")
            return None

    def verify_signature(self, message, signature, ip=None, public_key=None):
        """
        验证签名
        message: 原始消息
        signature: Base64编码的签名
        ip: 发送方IP (如提供，将使用存储的对应公钥)
        public_key: 公钥 (如提供IP，则忽略此参数)
        """
        try:
            # 获取用于验证的公钥
            if ip and ip in self.peer_public_keys:
                verify_key = self.peer_public_keys[ip]
            elif public_key:
                if isinstance(public_key, bytes):
                    verify_key = serialization.load_pem_public_key(
                        data=public_key,
                        backend=default_backend()
                    )
                else:
                    verify_key = public_key
            else:
                self.logger.error("验证签名失败: 无可用的公钥")
                return False

            # 转换消息为字节
            if isinstance(message, str):
                message = message.encode('utf-8')

            # 解码签名
            signature_bytes = base64.b64decode(signature)

            # 验证签名
            verify_key.verify(
                signature_bytes,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            return True
        except Exception as e:
            self.logger.error(f"验证签名失败: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("签名验证失败", f"验证签名失败: {str(e)}\n{traceback.format_exc()}")
            return False

    def has_peer_public_key(self, ip):
        """检查是否有指定IP的公钥"""
        # 检查ip是否在peer_public_keys中
        return ip in self.peer_public_keys

    def regenerate_keys(self):
        """重新生成密钥对"""
        try:
            # 生成新的密钥对
            self.generate_keys()
            self.logger.debug("已重新生成新的密钥对")
            return True
        except Exception as e:
            self.logger.error(f"重新生成密钥对失败: {str(e)}\n{traceback.format_exc()}")
            return False