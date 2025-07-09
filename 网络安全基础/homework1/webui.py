"""requirement: pip install gradio"""
import os
import gradio as gr
from rc4 import RC4

def encrypt_string(key: str, plaintext: str) -> str:
    cipher = RC4(key)
    return cipher.encrypt_str(plaintext)

def decrypt_string(key: str, ciphertext: str) -> str:
    cipher = RC4(key)
    return cipher.decrypt_str(ciphertext)

def encrypt_file(key: str, input_file: str) -> str:
    file_name = os.path.basename(input_file)
    with open(input_file, "rb") as f:
        input_file = f.read()
    cipher = RC4(key)
    output_bytes = cipher.encrypt_decrypt_bytes(input_file)
    os.makedirs("encrypted", exist_ok=True)
    output_file = os.path.join("encrypted", file_name + ".bin")
    with open(output_file, "wb") as f:
        f.write(output_bytes)
    return output_file

def decrypt_file(key: str, input_file: str) -> str:
    file_name = os.path.basename(input_file)
    with open(input_file, "rb") as f:
        input_file = f.read()
    cipher = RC4(key)
    output_bytes = cipher.encrypt_decrypt_bytes(input_file)
    os.makedirs("decrypted", exist_ok=True)
    output_file = os.path.join("decrypted", file_name[:-4])
    with open(output_file, "wb") as f:
        f.write(output_bytes)
    return output_file

def main():
    with gr.Blocks() as demo:
        gr.Markdown('''<div align="center"><font size=6><b>Python RC4 Demo WebUI</b></font></div>''')
        key = gr.Textbox(label="密钥", placeholder="请输入密钥", lines=1, interactive=True)
        with gr.Tabs():
            with gr.TabItem(label="加密/解密字符串"):
                with gr.Row():
                    plaintext = gr.Textbox(label="明文", placeholder="此处为明文", lines=20, interactive=True)
                    ciphertext = gr.Textbox(label="密文", placeholder="此处为密文", lines=20, interactive=True)
                with gr.Row():
                    encrypt_s = gr.Button(value="加密字符串")
                    decrypt_s = gr.Button(value="解密字符串")
            with gr.TabItem(label="加密/解密文件"):
                input_file = gr.File(label="输入文件", type="filepath", interactive=True)
                with gr.Row():
                    encrypt_f = gr.Button(value="加密文件")
                    decrypt_f = gr.Button(value="解密文件")
                output_file = gr.File(label="输出文件", type="filepath", interactive=False)

        encrypt_s.click(encrypt_string, [key, plaintext], outputs=ciphertext)
        decrypt_s.click(decrypt_string, [key, ciphertext], outputs=plaintext)
        encrypt_f.click(encrypt_file, [key, input_file], outputs=output_file)
        decrypt_f.click(decrypt_file, [key, input_file], outputs=output_file)

    return demo

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip_address", type=str, default=None, help="IP address to bind to")
    parser.add_argument("-p", "--port", type=int, default=None, help="Port to bind to")
    parser.add_argument("-s", "--share", action="store_true", help="Share this interface on a public URL")
    args = parser.parse_args()

    main().queue().launch(inbrowser=True, share=args.share, server_name=args.ip_address, server_port=args.port)