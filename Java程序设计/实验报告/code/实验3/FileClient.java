import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;

// FileClient类用于向服务器发送文件
public class FileClient {
    private static final String SERVER_ADDRESS = "localhost";
    private static final int SERVER_PORT = 12345;

    public static void main(String[] args) {
        // 检查命令行参数是否正确
        if (args.length != 1) {
            System.err.println(getCurrentTime() + "[ERROR] 请使用: java FileClient.java <input_file> 命令发送文件");
            System.exit(1);
        }

        String inputFile = args[0];
        File file = new File(inputFile);

        // 检查文件是否存在
        if (!file.exists()) {
            System.err.println(getCurrentTime() + "[ERROR] 无法找到文件: " + inputFile);
            System.exit(1);
        }

        Socket socket = null;
        try {
            // 创建套接字并连接到服务器
            socket = new Socket(SERVER_ADDRESS, SERVER_PORT);
            System.out.println(getCurrentTime() + "[INFO] 已连接到服务器：" + socket.getInetAddress().getHostAddress() + ":"
                    + socket.getPort() + "，本地端口：" + socket.getLocalPort());

            try (DataInputStream fis = new DataInputStream(new FileInputStream(file));
                    DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
                    DataInputStream dis = new DataInputStream(socket.getInputStream())) {

                // 发送文件名到服务器
                dos.writeUTF(file.getName());

                // 读取文件并发送到服务器
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fis.read(buffer)) != -1) {
                    dos.write(buffer, 0, bytesRead);
                }

                // 关闭输出流，表示文件发送完成
                socket.shutdownOutput();

                // 接收并打印服务器的响应
                String response = dis.readUTF();
                System.out.println(getCurrentTime() + "[INFO] 服务器响应：" + response);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // 关闭套接字
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    // 获取当前时间
    public static String getCurrentTime() {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String currentTime = "[" + dateFormat.format(System.currentTimeMillis()) + "]";
        return currentTime;
    }
}
