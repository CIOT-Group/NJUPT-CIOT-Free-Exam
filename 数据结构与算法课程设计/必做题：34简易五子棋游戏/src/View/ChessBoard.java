package View;

import Model.Chess;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

/**
 * 自定义棋盘面板类，继承自 JPanel，并实现 MouseListener 接口，用于绘制五子棋棋盘和处理鼠标事件。
 */
public class ChessBoard extends JPanel implements MouseListener {
    // 游戏结束标志
    public static final int GAME_OVER = 0;
    // 棋盘的列数
    public static final int COLS = 19;
    // 棋盘的行数
    public static final int RAWS = 19;
    // 游戏结果标志，初始为 1，表示游戏进行中
    public int result = 1;
    // 白棋图片
    public Image whiteChess;
    // 黑棋图片
    public Image blackChess;
    // 棋盘图片
    public Image chessBoardImage;
    // 边框装饰图片
    public Image laceImage;
    // 棋子的横坐标
    public int chessX;
    // 棋子的纵坐标
    public int chessY;
    // 棋盘上的隐形坐标数组，每个小区域代表一个数组元素
    public int[][] chess = new int[COLS][RAWS];
    // 是否可点击的标志
    public int clickable;

    /**
     * 构造函数，初始化棋盘的图片，并初始化数组。
     */
    public ChessBoard() {
        chessBoardImage = Toolkit.getDefaultToolkit().getImage("src/images/gobang.png");
        laceImage = Toolkit.getDefaultToolkit().getImage("src/images/lace.png");
        whiteChess = Toolkit.getDefaultToolkit().getImage("src/images/white.png");
        blackChess = Toolkit.getDefaultToolkit().getImage("src/images/black.png");
        initArray();
        addMouseListener(this);
    }

    /**
     * 设置棋盘是否可点击。
     *
     * @param clickable 是否可点击的标志
     */
    public void setClickable(int clickable) {
        this.clickable = clickable;
    }

    /**
     * 初始化棋盘数组，将数组中的值全部设为 Chess.NO_CHESS。
     */
    public void initArray() {
        for (int i = 0; i < COLS; i++) {
            for (int j = 0; j < RAWS; j++) {
                chess[i][j] = Chess.NO_CHESS;
            }
        }
    }

    /**
     * 重写 paintComponent 方法，绘制棋盘和棋子。
     *
     * @param g 该参数是绘制图形的句柄
     */
    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.drawImage(laceImage, 0, 0, null);
        g.drawImage(chessBoardImage, 35, 35, null);
        for (int i = 0; i < COLS; i++) {
            for (int j = 0; j < RAWS; j++) {
                if (chess[i][j] == Chess.WHITE) {
                    g.drawImage(whiteChess, 60 + i * 25 - 11, 62 + j * 25 - 12, null);
                } else if (chess[i][j] == Chess.BLACK) {
                    g.drawImage(blackChess, 60 + i * 25 - 11, 62 + j * 25 - 12, null);
                }
            }
        }
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
