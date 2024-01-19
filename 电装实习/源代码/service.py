import machine
import time
import network
import socket

# 定义L298N连接到ESP-12F的引脚
IN1_PIN = 12  # IO12
IN2_PIN = 13  # IO13
IN3_PIN = 4   # IO4
IN4_PIN = 5   # IO5

# 初始化引脚
in1 = machine.Pin(IN1_PIN, machine.Pin.OUT)
in2 = machine.Pin(IN2_PIN, machine.Pin.OUT)
in3 = machine.Pin(IN3_PIN, machine.Pin.OUT)
in4 = machine.Pin(IN4_PIN, machine.Pin.OUT)

# 初始化网络
# 输入你的wifi名字和密码
wifi_ssid = "YOUR_WIFI_NAME"
wifi_password = "YOUR_WIFI_PASSWORD"
udp_port = 12345

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(wifi_ssid, wifi_password)

# 等待连接成功
while not sta.isconnected():
    pass

# 打印ESP8266的IP地址
print("Connected to WiFi")
print("IP Address:", sta.ifconfig()[0])

# 设置UDP服务器
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('0.0.0.0', udp_port))

# 接收并解析UDP命令


def process_udp_command(data):
    if data == b'forward':
        forward()
    elif data == b'backward':
        backward()
    elif data == b'left':
        left()
    elif data == b'right':
        right()
    elif data == b'stop':
        stop()

# 控制小车向前


def forward():
    in1.off()
    in2.on()
    in3.on()
    in4.off()

# 控制小车向后


def backward():
    in1.on()
    in2.off()
    in3.off()
    in4.on()

# 控制小车左转


def left():
    in1.off()
    in2.on()
    in3.off()
    in4.on()

# 控制小车右转


def right():
    in1.on()
    in2.off()
    in3.on()
    in4.off()

# 停止小车运动


def stop():
    in1.off()
    in2.off()
    in3.off()
    in4.off()


# 循环，等待UDP命令
try:
    while True:
        data, addr = udp_server.recvfrom(1024)
        process_udp_command(data)
except KeyboardInterrupt:
    udp_server.close()
