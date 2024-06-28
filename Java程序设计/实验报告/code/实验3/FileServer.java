import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.text.SimpleDateFormat;

// FileServer类用于接收客户端发送的文件
public class FileServer {
    // 服务器监听端口
    private static final int PORT = 12345;
    // 接收文件保存的目录
    private static final String SAVE_DIR = "received_files/";

    public static void main(String[] args) {
        ServerSocket serverSocket = null;
        try {
            // 创建服务器套接字并开始监听端口
            serverSocket = new ServerSocket(PORT);
            System.out.println(getCurrentTime() + "[INFO] 服务器已启动，等待客户端连接...");

            // 创建保存文件的目录
            File saveDir = new File(SAVE_DIR);
            if (!saveDir.exists()) {
                saveDir.mkdirs();
            }

            // 循环接收客户端连接
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println(getCurrentTime() + "[INFO] 已连接到客户端：" + clientSocket.getInetAddress().getHostAddress()
                        + ":" + clientSocket.getPort());
                // 启动新线程处理客户端请求
                new Thread(new ClientHandler(clientSocket)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // 关闭服务器套接字
            if (serverSocket != null) {
                try {
                    serverSocket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    // 处理客户端发送的文件
    private static class ClientHandler implements Runnable {
        private Socket clientSocket;

        public ClientHandler(Socket clientSocket) {
            this.clientSocket = clientSocket;
        }

        @Override
        public void run() {
            try (DataInputStream dis = new DataInputStream(clientSocket.getInputStream());
                    DataOutputStream dos = new DataOutputStream(clientSocket.getOutputStream())) {

                // 读取文件名
                String originalFileName = dis.readUTF();
                String fileName = generateUniqueFileName(originalFileName);
                File outputFile = new File(SAVE_DIR + fileName);

                // 将接收的文件写入接收文件夹
                try (FileOutputStream fos = new FileOutputStream(outputFile)) {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    while ((bytesRead = dis.read(buffer)) != -1) {
                        fos.write(buffer, 0, bytesRead);
                    }
                }

                // 发送文件接收完成的消息给客户端
                dos.writeUTF("文件接收完成：" + fileName);
                System.out.println(getCurrentTime() + "[INFO] 文件接收完成：" + fileName);
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                // 关闭客户端套接字
                try {
                    clientSocket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        // 生成唯一的文件名，用于避免文件名冲突
        private String generateUniqueFileName(String originalFileName) {
            String baseName = originalFileName;
            String extension = "";
            int dotIndex = originalFileName.lastIndexOf('.');
            if (dotIndex != -1) {
                baseName = originalFileName.substring(0, dotIndex);
                extension = originalFileName.substring(dotIndex);
            }

            String fileName = baseName + extension;
            int counter = 1;
            while (Files.exists(Paths.get(SAVE_DIR + fileName))) {
                fileName = baseName + "_" + counter++ + extension;
            }
            return fileName;
        }
    }

    // 获取当前时间
    public static String getCurrentTime() {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String currentTime = "[" + dateFormat.format(System.currentTimeMillis()) + "]";
        return currentTime;
    }
}
