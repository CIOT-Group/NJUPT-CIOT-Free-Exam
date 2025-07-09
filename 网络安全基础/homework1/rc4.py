import base64
from typing import Generator, Union


class RC4:
    def __init__(self, key: Union[str, bytes] = None):
        if isinstance(key, str):
            key = key.encode("utf-8")
        self.key = key
        self.S = self.KSA()

    def KSA(self) -> list:
        """Key-Scheduling Algorithm (KSA)"""
        key_length = len(self.key)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + self.key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def PRGA(self) -> Generator[int, None, None]:
        """Pseudo-Random Generation Algorithm (PRGA)"""
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            K = self.S[(self.S[i] + self.S[j]) % 256]
            yield K

    def encrypt_decrypt_bytes(self, data: bytes) -> bytes:
        """加密或解密字节数据"""
        keystream = self.PRGA()
        return bytes(b ^ next(keystream) for b in data)

    def encrypt_str(self, plaintext: str) -> str:
        """加密字符串并输出为Base64编码"""
        plaintext_bytes = plaintext.encode("utf-8")
        encrypted_bytes = self.encrypt_decrypt_bytes(plaintext_bytes)
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def decrypt_str(self, encrypted_base64: str) -> str:
        """解密Base64编码的字符串"""
        encrypted_bytes = base64.b64decode(encrypted_base64)
        decrypted_bytes = self.encrypt_decrypt_bytes(encrypted_bytes)
        return decrypted_bytes.decode("utf-8")


if __name__ == "__main__":
    key = "secret"
    cipher = RC4(key)

    # 加密字符串
    plaintext = "Hello World!"
    encrypted = cipher.encrypt_str(plaintext)
    print("Encrypted:", encrypted)

    # 解密字符串
    cipher = RC4(key)  # 需要重新创建RC4实例，否则S状态已被修改
    decrypted = cipher.decrypt_str(encrypted)
    print("Decrypted:", decrypted)

    # 加密文件
    with open("webui.py", "rb") as f:
        input_file = f.read()
    cipher = RC4(key)
    encrypted_file = cipher.encrypt_decrypt_bytes(input_file)
    with open("encrypted.bin", "wb") as f:
        f.write(encrypted_file)

    # 解密文件
    cipher = RC4(key) # 需要重新创建RC4实例，否则S状态已被修改
    decrypted_file = cipher.encrypt_decrypt_bytes(encrypted_file)
    with open("decrypted.txt", "wb") as f:
        f.write(decrypted_file)