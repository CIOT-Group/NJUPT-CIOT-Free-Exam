import socket
import time
import keyboard

# ESP8266的IP地址和端口号
esp_ip = "YOUR_ESP8266_IP_ADDRESS"
esp_port = 12345

# 创建UDP客户端
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 定义小车运动命令
commands = ["forward", "backward", "left", "right", "stop"]
print("通过'W':前进，'S':后退，'A':左转，'D':右转，'Space':刹车，来控制小车")

try:
    while True:
        if keyboard.is_pressed('w'):
            udp_client.sendto(commands[0].encode(), (esp_ip, esp_port))
            print("Send Command: Forward")
            time.sleep(0.2)
            udp_client.sendto(commands[4].encode(), (esp_ip, esp_port))
        elif keyboard.is_pressed('s'):
            udp_client.sendto(commands[1].encode(), (esp_ip, esp_port))
            print("Send Command: Backward")
            time.sleep(0.2)
            udp_client.sendto(commands[4].encode(), (esp_ip, esp_port))
        elif keyboard.is_pressed('a'):
            udp_client.sendto(commands[2].encode(), (esp_ip, esp_port))
            print("Send Command: Left")
            time.sleep(0.2)
            udp_client.sendto(commands[4].encode(), (esp_ip, esp_port))
        elif keyboard.is_pressed('d'):
            udp_client.sendto(commands[3].encode(), (esp_ip, esp_port))
            print("Send Command: Right")
            time.sleep(0.2)
            udp_client.sendto(commands[4].encode(), (esp_ip, esp_port))
        elif keyboard.is_pressed('space'):
            udp_client.sendto(commands[4].encode(), (esp_ip, esp_port))
            print("Send Command: Stop")
            time.sleep(0.2)
except KeyboardInterrupt:
    print("Exit")
    udp_client.close()
