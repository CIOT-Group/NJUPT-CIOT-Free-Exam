package Net;

import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.MulticastSocket;

/**
 * NetTool 类提供网络工具方法，用于发送 UDP 广播消息。
 */
public class NetTool {

    /**
     * 发送 UDP 广播消息。
     *
     * @param ip 目标 IP 地址
     * @param msg 要发送的消息
     */
    public static void sendUdpBroadCast(String ip, String msg) {
        try {
            // 创建一个多播套接字
            MulticastSocket ms = new MulticastSocket();

            // 获取目标 IP 地址
            InetAddress ia = InetAddress.getByName(ip);

            // 创建一个数据报包，包含消息的字节数组，指定目标地址和端口
            DatagramPacket dp = new DatagramPacket(msg.getBytes(), 0, msg.length(), ia, 1111);

            // 通过多播套接字发送数据报包
            ms.send(dp);

            // 关闭多播套接字
            ms.close();
        } catch (Exception e) {
            // 捕获并打印异常
            e.printStackTrace();
        }
    }
}
