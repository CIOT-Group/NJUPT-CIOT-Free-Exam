package View;

import Control.JudgeWinner;
import Model.Chess;
import Net.NetTool;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;

/**
 * PPChessBoard 类表示玩家对战的五子棋棋盘，继承自 ChessBoard 类。
 */
public class PPChessBoard extends ChessBoard {

    private int role; // 角色，黑色或白色
    private JTextArea ta_pos_info; // 位置信息文本区域
    private final PPMainBoard mb; // 主界面对象
    private final WinDialog dialog; // 胜利对话框

    /**
     * 构造函数，初始化棋盘和相关组件
     * @param mb 主界面对象
     * @param dialog 胜利对话框对象
     */
    public PPChessBoard(PPMainBoard mb, WinDialog dialog) {
        super(); // 调用父类构造方法初始化棋盘
        this.mb = mb;
        this.dialog = dialog;
        setRole(Chess.WHITE); // 设置默认角色为白色
    }

    /**
     * 设置位置信息文本区域
     * @param ta 位置信息文本区域对象
     */
    public void setInfoBoard(JTextArea ta) {
        ta_pos_info = ta;
    }

    /**
     * 设置棋子横纵坐标和角色
     * @param x 横坐标
     * @param y 纵坐标
     * @param r 角色，黑/白
     */
    public void setCoord(int x, int y, int r) {
        if (r == Chess.WHITE) {
            role = Chess.BLACK;
        } else {
            role = Chess.WHITE;
        }
        chess[x][y] = r;
        if (r == Chess.WHITE) {
            ta_pos_info.append("白棋位置为:" + x + "," + y + "\n");
        } else {
            ta_pos_info.append("黑棋位置为:" + x + "," + y + "\n");
        }
        int winner = JudgeWinner.PPJudge(x, y, chess, r);
        WinEvent(winner);
        setClickable(MainBoard.CAN_CLICK_INFO);
        repaint();
    }

    /**
     * 设置角色
     * @param role 角色，黑/白
     */
    public void setRole(int role) {
        this.role = role;
    }

    /**
     * 绘制棋盘图形
     * @param g 绘图对象
     */
    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g); // 调用父类方法绘制基本图形
    }

    /**
     * 处理胜利事件
     * @param winner 胜利者
     */
    public void WinEvent(int winner) {
        if (winner == Chess.WHITE) { // 白棋获胜
            try {
                mb.getTimer().interrupt();
            } catch (Exception e1) {
                e1.printStackTrace();
            }
            mb.getBtn_startGame().setText("开始游戏");
            mb.getBtn_startGame().setEnabled(true);
            ta_pos_info.append("白棋获胜\n");
            result = Chess.WHITE;
            dialog.setWinnerInfo("白棋获胜!");
            setClickable(PPMainBoard.CAN_NOT_CLICK_INFO);
            dialog.setVisible(true);
            if (dialog.getMsg() == WinDialog.BACK) {
                mb.dispose();
                new SelectMenu();
            } else {
                initArray();
                mb.getLabel().setText(null);
                ta_pos_info.setText(null);
            }
        } else if (winner == Chess.BLACK) { // 黑棋获胜
            try {
                mb.getTimer().interrupt();
            } catch (Exception e1) {
                e1.printStackTrace();
            }
            mb.getBtn_startGame().setText("开始游戏");
            mb.getBtn_startGame().setEnabled(true);
            ta_pos_info.append("黑棋获胜\n");
            result = Chess.BLACK;
            setClickable(MainBoard.CAN_NOT_CLICK_INFO);
            dialog.setWinnerInfo("黑棋获胜!");
            dialog.setVisible(true);
            if (dialog.getMsg() == WinDialog.BACK) {
                mb.dispose();
                new SelectMenu();
            } else {
                initArray();
                mb.getLabel().setText(null);
                ta_pos_info.setText(null);
            }
        }
    }

    /**
     * 处理鼠标按下事件
     * @param e 鼠标事件对象
     */
    @Override
    public void mousePressed(MouseEvent e) {
        if (clickable == PPMainBoard.CAN_CLICK_INFO) { // 如果可以点击
            chessX = e.getX();
            chessY = e.getY();
            if (chessX < 524 && chessX > 50 && chessY < 523 && chessY > 50) {
                float x = (float) (chessX - 49) / 25;
                float y = (float) (chessY - 50) / 25;
                int x1 = (int) x;
                int y1 = (int) y;
                if (chess[x1][y1] == 0) { // 如果该位置没有棋子
                    chess[x1][y1] = role; // 放置棋子
                    if (role == Chess.WHITE) {
                        ta_pos_info.append("白棋位置为:" + x1 + "," + y1 + "\n");
                    } else {
                        ta_pos_info.append("黑棋位置为:" + x1 + "," + y1 + "\n");
                    }
                    NetTool.sendUdpBroadCast(mb.getIp(), "POS" + "," + x1 + "," + y1 + "," + role); // 发送位置信息
                    int winner = JudgeWinner.PPJudge(x1, y1, chess, role); // 判断是否有玩家获胜
                    WinEvent(winner); // 处理获胜事件
                    setClickable(MainBoard.CAN_NOT_CLICK_INFO); // 设置不可点击
                }
            }
        }
    }
}

