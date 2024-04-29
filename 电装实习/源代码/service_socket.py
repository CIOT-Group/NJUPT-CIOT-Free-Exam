import machine
import network
import time
import socket

# 初始化引脚
in1 = machine.PWM(machine.Pin(12), freq=50, duty=0)

# 初始化网络
wifi_ssid = "Sucial"
wifi_password = "qwertyuiop"
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


def get_duty(direction):
    return int((10 / 18) * direction + 25)


def process_udp_command(data):
    if data == b'start':
        print("Start")
        start()


def start():
    in1.duty(get_duty(0))
    time.sleep(0.1)
    in1.duty(get_duty(90))
    time.sleep(0.1)
    in1.duty(get_duty(180))


# 循环，等待UDP命令
try:
    while True:
        data, addr = udp_server.recvfrom(1024)
        process_udp_command(data)
except KeyboardInterrupt:
    udp_server.close()

