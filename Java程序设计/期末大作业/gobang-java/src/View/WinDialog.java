package View;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * WinDialog 类表示游戏胜利时弹出的对话框，允许用户重新开始游戏或返回主菜单。
 */
public class WinDialog extends JDialog implements ActionListener {
    public static final int RESTART = 1;
    public static final int BACK = 0;
    private JButton btn_restart, btn_back;
    private JLabel label;
    private int msg;

    /**
     * 构造一个 WinDialog 对象。
     *
     * @param f     父窗口
     * @param title 对话框标题
     * @param b     模态对话框的模式
     */
    public WinDialog(JFrame f, String title, boolean b) {
        super(f, title, b);
        setLayout(null);
        setResizable(false);
        setBounds(500, 300, 300, 200);
        init();
    }

    /**
     * 获取用户的选择信息。
     *
     * @return 选择信息，1 为重新开始游戏，0 为返回主页面
     */
    public int getMsg() {
        return msg;
    }

    /**
     * 设置胜利信息。
     *
     * @param winnerInfo 胜利信息
     */
    public void setWinnerInfo(String winnerInfo) {
        label.setText(winnerInfo);
    }

    private void init() {
        btn_restart = new JButton("重新开始");
        btn_restart.setFocusPainted(false);
        btn_restart.setFont(new Font("Microsoft Yahei", Font.BOLD, 15));
        btn_restart.setForeground(Color.WHITE);
        btn_restart.setBackground(new Color(82, 109, 165));
        btn_restart.addActionListener(this);
        btn_restart.setBounds(20, 110, 115, 40);
        btn_back = new JButton("返回主页面");
        btn_back.setFocusPainted(false);
        btn_back.setFont(new Font("Microsoft Yahei", Font.BOLD, 15));
        btn_back.setForeground(Color.WHITE);
        btn_back.setBounds(155, 110, 115, 40);
        btn_back.setBackground(new Color(82, 109, 165));
        btn_back.addActionListener(this);
        label = new JLabel();
        label.setFont(new Font("Microsoft Yahei", Font.BOLD, 20));
        label.setFont(new Font(Font.DIALOG_INPUT, Font.BOLD, 20));
        label.setBounds(100, 10, 100, 100);
        add(btn_restart);
        add(btn_back);
        add(label);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == btn_restart) {
            msg = RESTART;
            setVisible(false);
        } else if (e.getSource() == btn_back) {
            msg = BACK;
            setVisible(false);
        }
    }
}
