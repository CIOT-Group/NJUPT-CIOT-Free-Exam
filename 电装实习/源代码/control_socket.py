import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

esp_ip = "172.20.10.12"
esp_port = 12345
commands = ["start"]

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html_content = """
        <html>
        <head>
            <title>舵机控制</title>
            <meta charset="UTF-8">  <!-- 设置字符编码为 UTF-8 -->
        </head>
        <body>
            <h1>舵机控制</h1>
            <button onclick="controlServo()">控制舵机</button>
            <script>
                function controlServo() {
                    var xhr = new XMLHttpRequest();
                    console.log("Send Command: Start");
                    xhr.open("GET", "/control", true);
                    xhr.send();
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(bytes(html_content, "utf-8"))
        if self.path == '/control':  # 如果路径是 /control
            send_command()

    def log_message(self, format, *args):
        return


class UDPServer:
    def __init__(self):
        self.server_address = ("", 8000)
        self.httpd = HTTPServer(self.server_address, RequestHandler)

    def start(self):
        print('server start on "http://localhost:8000"')
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.server_close()


def send_command():
    udp_client.sendto(commands[0].encode(), (esp_ip, esp_port))
    print("Send Command: Start")
    time.sleep(0.1)


if __name__ == '__main__':
    try:
        udp_server = UDPServer()
        udp_server.start()
    except KeyboardInterrupt:
        print("Exit")
        udp_client.close()
        udp_server.stop()
