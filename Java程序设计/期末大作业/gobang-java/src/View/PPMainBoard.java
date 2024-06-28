package View;

import Model.timerThread;
import Net.NetTool;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class PPMainBoard extends MainBoard {
    private PPChessBoard cb; // 对战棋盘
    private JButton btn_startGame; // 开始游戏按钮
    private JButton btn_back; // 退出按钮
    private JTextField tf_ip; // 输入IP地址文本框
    private String ip; // IP地址
    private DatagramSocket socket; // 数据报套接字
    private String gameState; // 游戏状态
    private String enemyGameState; // 对手游戏状态

    /**
     * 获取开始游戏按钮
     *
     * @return 开始游戏按钮对象
     */
    public JButton getBtn_startGame() {
        return btn_startGame;
    }

    /**
     * 获取IP地址
     *
     * @return IP地址字符串
     */
    public String getIp() {
        return ip;
    }

    /**
     * 构造函数，初始化主面板
     */
    public PPMainBoard() {
        super();
        label_timeCount.setBounds(602, 330, 230, 40);
        init();
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }

    /**
     * 初始化界面组件
     */
    public void init() {
        gameState = "NOT_START";
        enemyGameState = "NOT_START";
        // 提示信息
        JLabel help = new JLabel("请输入IP地址");
        help.setBounds(582, 350, 190, 30);
        help.setFont(new Font("Microsoft Yahei", Font.BOLD, 16));
        tf_ip = new JTextField();
        tf_ip.setBounds(582, 380, 190, 30);
        tf_ip.addMouseListener(this);
        btn_startGame = new JButton("准备游戏");
        btn_startGame.setFocusPainted(false);
        btn_startGame.setBackground(Color.CYAN);
        btn_startGame.setFont(new Font("Microsoft Yahei", Font.BOLD, 22));
        btn_startGame.addActionListener(this);
        btn_startGame.setBounds(582, 430, 190, 50);
        btn_back = new JButton("退      出");
        btn_back.setFocusPainted(false);
        btn_back.setBackground(Color.CYAN);
        btn_back.setFont(new Font("Microsoft Yahei", Font.BOLD, 22));
        btn_back.addActionListener(this);
        btn_back.setBounds(582, 500, 190, 50);
        JTextArea ta_chess_info = new JTextArea();
        ta_chess_info.setEnabled(false);
        ta_chess_info.setBackground(Color.WHITE);
        ta_chess_info.setForeground(Color.black);
        JScrollPane p = new JScrollPane(ta_chess_info);
        p.setBounds(582, 20, 190, 300);
        WinDialog dialog = new WinDialog(this, "恭喜", true);
        cb = new PPChessBoard(this, dialog);
        cb.setClickable(PPMainBoard.CAN_NOT_CLICK_INFO);
        cb.setBounds(0, 20, 570, 585);
        cb.setVisible(true);
        cb.setInfoBoard(ta_chess_info);
        add(help);
        add(tf_ip);
        add(cb);
        add(btn_startGame);
        add(p);
        add(btn_back);
        ReicThread();
        repaint();
    }

    /**
     * 接收信息放在线程中
     */
    public void ReicThread() {
        new Thread(new Runnable() {
            public void run() {
                try {
                    byte[] buf = new byte[1024];
                    socket = new DatagramSocket(2222);
                    DatagramPacket dp = new DatagramPacket(buf, buf.length);
                    while (true) {
                        socket.receive(dp);

                        String data = new String(dp.getData(), 0, dp.getLength());
                        if (data.isEmpty()) {
                            cb.setClickable(CAN_NOT_CLICK_INFO);
                        } else {
                            String[] msg = data.split(",");
                            System.out.println(msg[0]);
                            // 接收到对面准备信息并且自己点击了准备
                            if (msg[0].equals("ready")) {
                                enemyGameState = "ready";
                                System.out.println("对方已准备");
                                if (gameState.equals("ready")) {
                                    gameState = "FIGHTING";
                                    cb.setClickable(CAN_CLICK_INFO);
                                    btn_startGame.setText("正在游戏");
                                    timer = new timerThread(label_timeCount);
                                    timer.start();
                                }
                            } else if (msg[0].equals("POS")) {
                                System.out.println("发送坐标");
                                // 接受坐标以及角色
                                cb.setCoord(Integer.parseInt(msg[1]), Integer.parseInt(msg[2]),
                                        Integer.parseInt(msg[3]));
                            }

                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }
    /**
     * 响应按钮点击事件
     *
     * @param e 事件对象
     */
    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == btn_startGame) {
            if (!tf_ip.getText().isEmpty() &&
                    !tf_ip.getText().equals("不能为空") &&
                    !tf_ip.getText().equals("请输入IP地址") &&
                    !tf_ip.getText().equals("不能连接到此IP")) {
                ip = tf_ip.getText();
                btn_startGame.setEnabled(false);
                btn_startGame.setText("等待对方准备");
                tf_ip.setEditable(false);
                NetTool.sendUdpBroadCast(ip, "ready");
                gameState = "ready";
                if (enemyGameState != null && enemyGameState.equals("ready")) {
                    gameState = "FIGHTING";
                    cb.setClickable(CAN_CLICK_INFO);
                    btn_startGame.setText("正在游戏");
                    timer = new timerThread(label_timeCount);
                    timer.start();
                }
            } else {
                tf_ip.setText("不能为空");
            }
        } else if (e.getSource() == btn_back) {
            System.exit(0);
        }
    }
}
