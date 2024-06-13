package View;

import Model.timerThread;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;

/**
 * PCMainBoard 类是五子棋游戏的主界面，继承自 MainBoard 类。
 */
public class PCMainBoard extends MainBoard {

    private PCChessBoard cb; // PCChessBoard 对象，表示五子棋棋盘
    private JButton btn_startGame; // 开始游戏按钮
    private JButton btn_back; // 悔棋按钮
    private JButton btn_exit; // 返回按钮

    /**
     * 获取开始游戏按钮对象
     * @return 开始游戏按钮对象
     */
    public JButton getBtn_startGame() {
        return btn_startGame;
    }

    /**
     * PCMainBoard 类的构造方法，初始化界面
     */
    public PCMainBoard() {
        super(); // 调用父类构造方法初始化主界面
        init(); // 初始化界面组件
        setDefaultCloseOperation(DISPOSE_ON_CLOSE); // 设置默认的关闭操作
    }

    /**
     * 初始化界面组件
     */
    public void init() {
        cb = new PCChessBoard(this); // 创建 PCChessBoard 对象
        cb.setClickable(PCMainBoard.CAN_NOT_CLICK_INFO); // 设置初始不可点击
        cb.setBounds(0, 20, 570, 585); // 设置 PCChessBoard 组件在界面中的位置和大小
        cb.setVisible(true); // 设置 PCChessBoard 可见

        // 创建并设置"开始游戏"按钮
        btn_startGame = new JButton("开始游戏");
        btn_startGame.setBounds(582, 205, 190, 50);
        btn_startGame.setBackground(new Color(227, 164, 113));
        btn_startGame.setFocusable(false);
        btn_startGame.setFont(new Font("Microsoft Yahei", Font.BOLD, 20));
        btn_startGame.addActionListener(this);

        // 创建并设置"悔棋"按钮
        btn_back = new JButton("悔      棋");
        btn_back.setBounds(582, 270, 190, 50);
        btn_back.setBackground(new Color(144, 142, 153));
        btn_back.setFocusable(false);
        btn_back.setFont(new Font("Microsoft Yahei", Font.BOLD, 22));
        btn_back.addActionListener(this);

        // 创建并设置"返回"按钮
        btn_exit = new JButton("退      出");
        btn_exit.setBackground(new Color(82, 109, 165));
        btn_exit.setBounds(582, 335, 190, 50);
        btn_exit.setFocusable(false);
        btn_exit.setFont(new Font("Microsoft Yahei", Font.BOLD, 22));
        btn_exit.addActionListener(this);

        // 将组件添加到主界面中
        add(cb);
        add(btn_back);
        add(btn_startGame);
        add(btn_exit);
    }

    /**
     * 按钮点击事件处理方法
     * @param e 事件对象
     */
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == btn_startGame) { // 开始游戏按钮点击事件
            btn_startGame.setEnabled(false); // 禁用开始游戏按钮
            btn_startGame.setText("正在游戏"); // 设置按钮文本为"正在游戏"
            cb.setClickable(CAN_CLICK_INFO); // 设置棋盘可点击
            timer = new timerThread(label_timeCount); // 创建并启动计时器线程
            timer.start();
            cb.setResult(1); // 设置游戏状态为进行中
        } else if (e.getSource() == btn_back) { // 悔棋按钮点击事件
            cb.backStep(); // 调用 PCChessBoard 的悔棋方法
        } else if (e.getSource() == btn_exit) { // 返回按钮点击事件
            dispose(); // 关闭当前窗口
            System.exit(0); // 打开选择菜单窗口
        }
    }
}
