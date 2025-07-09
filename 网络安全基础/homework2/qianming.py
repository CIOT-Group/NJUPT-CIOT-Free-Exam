from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

def generate_key_pair(key_size=2048):
    """生成RSA密钥对"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_keys_to_file(private_key, public_key, private_key_file="private_key.pem", public_key_file="public_key.pem"):
    """将密钥保存到文件"""
    with open(private_key_file, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    with open(public_key_file, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

def load_keys_from_file(private_key_file="private_key.pem", public_key_file="public_key.pem"):
    """从文件加载密钥"""
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(
            data=f.read(),
            password=None,
            backend=default_backend()
        )
    with open(public_key_file, "rb") as f:
        public_key = serialization.load_pem_public_key(
            data=f.read(),
            backend=default_backend()
        )
    return private_key, public_key

def sign_message(message, private_key):
    """使用私钥对消息的哈希值进行签名"""
    if isinstance(message, str):
        message = message.encode('utf-8')
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(message, signature, public_key):
    """验证签名的有效性"""
    if isinstance(message, str):
        message = message.encode('utf-8')
    # 将Base64编码的签名转换回字节
    signature_bytes = base64.b64decode(signature)
    try:
        # 使用公钥验证签名
        public_key.verify(
            signature_bytes,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


if __name__ == "__main__":
    print("1. 生成RSA密钥对并保存到文件")
    private_key, public_key = generate_key_pair()
    save_keys_to_file(private_key, public_key)
    print("私钥和公钥已保存到文件")

    print("2. 从文件加载密钥并进行签名")
    private_key, public_key = load_keys_from_file()
    message = "这是一个需要签名的消息"
    print(f"原始消息: {message}")
    signature = sign_message(message, private_key)
    print(f"生成的签名: {signature}")

    print("3. 从文件加载密钥并验证签名")
    private_key, public_key = load_keys_from_file()
    is_valid = verify_signature(message, signature, public_key)
    print(f"签名验证结果: {'有效' if is_valid else '无效'}")
    tampered_message = "这是一个篡改签名的消息"
    is_valid = verify_signature(tampered_message, signature, public_key)
    print(f"篡改消息后验证结果: {'有效' if is_valid else '无效'}")