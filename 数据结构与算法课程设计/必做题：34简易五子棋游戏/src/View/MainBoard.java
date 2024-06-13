package View;

import Model.timerThread;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

/**
 * 主游戏界面类，继承自 JFrame，实现了 MouseListener 和 ActionListener 接口。
 * 用于创建五子棋游戏的主窗口和相关组件。
 */
public class MainBoard extends JFrame implements MouseListener, ActionListener {
    // 定义常量，表示是否可以点击
    public static final int CAN_CLICK_INFO = 1;
    public static final int CAN_NOT_CLICK_INFO = 0;

    // 显示计时的标签
    public JLabel label_timeCount;
    // 计时线程
    public timerThread timer;

    /**
     * 获取计时线程
     *
     * @return 当前的计时线程对象
     */
    public timerThread getTimer() {
        return timer;
    }

    /**
     * 构造函数，初始化主窗口
     */
    public MainBoard() {
        // 设置布局为空布局
        setLayout(null);
        // 设置窗口位置和大小
        setBounds(300, 70, 800, 620);
        // 初始化组件
        init1();
        // 设置窗口可见
        setVisible(true);
        // 设置默认关闭操作
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        // 设置窗口不可调整大小
        setResizable(false);
        // 设置窗口标题
        setTitle("五子棋游戏");
    }

    /**
     * 重写 paint 方法，调用父类的 paint 方法并重新绘制组件
     *
     * @param g 该参数是绘制图形的句柄
     */
    @Override
    public void paint(Graphics g) {
        super.paint(g);
        repaint();
    }

    /**
     * 初始化组件，添加计时标签
     */
    public void init1() {
        // 初始化计时标签
        label_timeCount = new JLabel();
        // 设置字体样式和大小
        label_timeCount.setFont(new Font("Microsoft Yahei", Font.BOLD, 30));
        // 设置标签位置和大小
        label_timeCount.setBounds(610, 100, 230, 40);
        // 添加标签到主窗口
        add(label_timeCount);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
    }

    @Override
    public void mouseClicked(MouseEvent e) {
    }

    @Override
    public void mousePressed(MouseEvent e) {
    }

    @Override
    public void mouseReleased(MouseEvent e) {
    }

    @Override
    public void mouseEntered(MouseEvent e) {
    }

    @Override
    public void mouseExited(MouseEvent e) {
    }
}
