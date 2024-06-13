package View;

import Control.JudgeWinner;
import Model.Chess;
import Model.Computer;
import Model.Coord;

import javax.swing.border.LineBorder;
import java.awt.*;
import java.awt.event.MouseEvent;

/**
 * 电脑对战模式下的棋盘面板，继承自 ChessBoard 类。
 */
public class PCChessBoard extends ChessBoard {
    private final int role; // 角色，表示玩家执棋的颜色
    private int result = 1; // 游戏结果
    private final PCMainBoard mb; // 主游戏面板
    private final WinDialog dialog; // 获胜对话框
    private final Computer com; // 电脑对象，用于计算电脑下棋位置
    private final int[][] step = new int[30 * 30][2]; // 记录每一步棋的坐标
    private int stepCount = 0; // 记录步数

    /**
     * 设置游戏结果。
     *
     * @param result 游戏结果，1 表示游戏未结束，0 表示游戏结束。
     */
    public void setResult(int result) {
        this.result = result;
    }

    /**
     * 构造函数，初始化 PCChessBoard 对象。
     *
     * @param mb 主游戏面板对象
     */
    public PCChessBoard(PCMainBoard mb) {
        this.mb = mb;
        role = Chess.WHITE; // 玩家执白棋
        com = new Computer(); // 初始化电脑对象
        dialog = new WinDialog(mb, "恭喜", true); // 初始化获胜对话框
    }

    /**
     * 保存黑白棋子的坐标到二维数组中。
     *
     * @param posX 棋子的横坐标
     * @param posY 棋子的纵坐标
     */
    private void saveStep(int posX, int posY) {
        stepCount++;
        step[stepCount][0] = posX;
        step[stepCount][1] = posY;
    }

    /**
     * 悔棋操作，回退上一步的棋子。
     */
    public void backStep() {
        if (stepCount >= 2) {
            chess[step[stepCount][0]][step[stepCount][1]] = 0;
            chess[step[stepCount - 1][0]][step[stepCount - 1][1]] = 0;
            stepCount = stepCount - 2;
        }
    }

    /**
     * 处理游戏结束事件，包括玩家赢和电脑赢两种情况。
     *
     * @param winner 获胜者，Chess.WHITE 表示玩家赢，Chess.BLACK 表示电脑赢。
     */
    public void WinEvent(int winner) {
        // 白棋赢
        if (winner == Chess.WHITE) {
            result = GAME_OVER;
            mb.getTimer().interrupt(); // 中断计时器线程
            mb.getBtn_startGame().setText("开始游戏"); // 设置开始游戏按钮的文本
            mb.getBtn_startGame().setEnabled(true); // 启用开始游戏按钮
            dialog.setWinnerInfo("白棋获胜!"); // 设置获胜对话框的内容
            setClickable(MainBoard.CAN_NOT_CLICK_INFO); // 设置不能点击棋盘
            dialog.setVisible(true); // 显示获胜对话框
            // 根据对话框的选择来决定下一步操作
            if (dialog.getMsg() == WinDialog.EXIT) {
                mb.dispose();
                System.exit(0);
            } else {
                initArray();
            }
        }
        // 黑棋赢
        else if (winner == Chess.BLACK) {
            result = GAME_OVER;
            mb.getTimer().interrupt(); // 中断计时器线程
            mb.getBtn_startGame().setText("开始游戏"); // 设置开始游戏按钮的文本
            mb.getBtn_startGame().setEnabled(true); // 启用开始游戏按钮
            setClickable(MainBoard.CAN_NOT_CLICK_INFO); // 设置不能点击棋盘
            dialog.setWinnerInfo("黑棋获胜!"); // 设置获胜对话框的内容
            dialog.setVisible(true); // 显示获胜对话框
            // 根据对话框的选择来决定下一步操作
            if (dialog.getMsg() == WinDialog.EXIT) {
                mb.dispose();
                System.exit(0);
            } else {
                initArray();
            }
        }
    }

    /**
     * 处理鼠标按下事件，即玩家下棋操作。
     *
     * @param e 鼠标事件对象
     */
    @Override
    public void mousePressed(MouseEvent e) {
        int winner;
        if (clickable == MainBoard.CAN_CLICK_INFO) { // 如果可以点击棋盘
            chessX = e.getX(); // 获取鼠标点击的横坐标
            chessY = e.getY(); // 获取鼠标点击的纵坐标
            if (chessX < 524 && chessX > 50 && chessY < 523 && chessY > 50) { // 如果点击的位置在棋盘范围内
                float x = (float) (chessX - 49) / 25;
                float y = (float) (chessY - 50) / 25;
                int x1 = (int) x;
                int y1 = (int) y;
                // 如果这个地方没有棋子
                if (chess[x1][y1] == Chess.NO_CHESS) {
                    chess[x1][y1] = role; // 玩家下棋
                    saveStep(x1, y1); // 保存下棋的坐标
                    setClickable(MainBoard.CAN_NOT_CLICK_INFO); // 设置不能点击棋盘
                    winner = JudgeWinner.PPJudge(x1, y1, chess, role); // 判断游戏是否结束
                    WinEvent(winner); // 处理游戏结束事件
                    if (result != GAME_OVER) { // 如果游戏没有结束
                        Coord coord = com.computePos(chess); // 计算电脑下棋位置
                        chess[coord.getX()][coord.getY()] = Chess.BLACK; // 电脑下棋
                        saveStep(coord.getX(), coord.getY()); // 保存电脑下棋的坐标
                        winner = JudgeWinner.PPJudge(coord.getX(), coord.getY(), chess, Chess.BLACK); // 判断游戏是否结束
                        WinEvent(winner); // 处理游戏结束事件
                        if (result != GAME_OVER) { // 如果游戏没有结束
                            setClickable(MainBoard.CAN_CLICK_INFO); // 设置可以点击棋盘
                        }
                    }
                }
            }
        }
    }
}
