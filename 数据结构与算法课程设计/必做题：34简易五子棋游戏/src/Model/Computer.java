package Model;

public class Computer {
    // 记录当前的分数
    private int scores;

    // 当前选定的坐标
    private Coord coord = new Coord();

    // 每个玩家点的评分
    private final int[][] everyPlayerPointScore = new int[19][19];

    // 每个电脑点的评分
    private final int[][] everyComputerPointScore = new int[19][19];

    /**
     * 计算下棋的位置
     *
     * @param chess 棋盘的当前状态，19x19的二维数组
     * @return 计算出的最佳下棋位置
     */
    public Coord computePos(int[][] chess) {
        // 根据当前棋盘状态计算最佳下棋位置
        countMaxLines(chess, Chess.WHITE);
        return coord;
    }

    /**
     * 找出分数最大的坐标
     *
     * @param chess 棋盘数组
     * @param role  当前角色（白棋还是黑棋）
     */
    public void countMaxLines(int[][] chess, int role) {
        Coord playerCoord = new Coord();
        Coord computerCoord = new Coord();
        int x, y;

        // 遍历棋盘每一个点
        for (x = 0; x < 19; x++) {
            for (y = 0; y < 19; y++) {
                // 如果该位置没有棋子
                if (chess[x][y] == Chess.NO_CHESS) {
                    // 计算该位置对玩家和电脑的评分
                    countEveryPos(x, y, chess, role);
                    everyPlayerPointScore[x][y] = scores;
                    countEveryPos(x, y, chess, Chess.BLACK);
                    everyComputerPointScore[x][y] = scores;
                } else {
                    // 如果有棋子，分数为0
                    everyPlayerPointScore[x][y] = 0;
                    everyComputerPointScore[x][y] = 0;
                }
            }
        }

        // 找到评分最高的点
        if (findBestPos(everyPlayerPointScore, playerCoord) >= findBestPos(everyComputerPointScore, computerCoord)) {
            coord = playerCoord;
        } else {
            coord = computerCoord;
        }
    }

    /**
     * 找到最大分数点的坐标
     *
     * @param a 存储每个点的分数的数组
     * @param c 保存最大分数点的坐标
     * @return 最大的分数值
     */
    public int findBestPos(int[][] a, Coord c) {
        int i, j, max = 0;

        // 遍历找到最大分数的点
        for (i = 0; i < 19; i++) {
            for (j = 0; j < 19; j++) {
                if (a[i][j] > max) {
                    max = a[i][j];
                    c.setX(i);
                    c.setY(j);
                }
            }
        }
        return max;
    }

    /**
     * 根据连子数量和对方棋子的阻挡情况进行评分
     *
     * @param count 当前方向上连续相同颜色棋子的数量
     * @param i     阻挡当前方向的对方棋子数量
     * @param countTwo 两边有一个空位的两个连在一起的棋子数量
     * @param role 当前角色
     */
    public void mark(int count, int i, int countTwo, int role) {
        if (count == 1) {
            scores += 10;
        } else if (count == 2 && i == 0 && role == Chess.WHITE && countTwo <= 1) {
            scores += 200;
        } else if (count == 2 && i == 0 && role == Chess.BLACK && countTwo <= 1) {
            scores += 400;
        } else if (count == 2 && i == 1) {
            scores += 50;
        } else if (count == 2 && i == 0 && countTwo > 1) {
            scores += 84000;
            System.out.println("双活二" + scores);
        } else if (count == 3 && i == 0 && role == Chess.WHITE) {
            scores += 85000;
        } else if (count == 3 && i == 0 && role == Chess.BLACK) {
            scores += 86000;
        } else if (count == 3 && i == 1 && role == Chess.WHITE) {
            scores += 300;
            System.out.println("白子冲三" + scores);
        } else if (count == 3 && i == 1 && role == Chess.BLACK) {
            scores += 1000;
            System.out.println("黑子冲三" + scores);
        } else if (count == 4 && i == 0 && role == Chess.WHITE) {
            scores += 90000;
        } else if (count == 4 && i == 0 && role == Chess.BLACK) {
            scores += 91000;
        } else if (count == 4 && i == 1) {
            scores += 87000;
        } else if (count == 5) {
            scores += 100000;
        }
    }

    /**
     * 根据坐标位置增加基础分数
     *
     * @param x 横坐标
     * @param y 纵坐标
     */
    public void basicScore(int x, int y) {
        if (x == 0 || y == 0) {
            scores += 3;
        } else {
            scores += 5;
        }
    }

    /**
     * 计算每个位置的分数
     *
     * @param x 当前坐标的横坐标
     * @param y 当前坐标的纵坐标
     * @param chess 当前棋盘的状态
     * @param role 当前角色
     */
    public void countEveryPos(int x, int y, int[][] chess, int role) {
        scores = 0;
        basicScore(x, y);

        int matchRole = (role == Chess.BLACK) ? Chess.WHITE : Chess.BLACK;
        int startX = x, startY = y;
        int count = 0, up = 0, down = 0, left = 0, right = 0;
        int leftUp = 0, leftDown = 0, rightUp = 0, rightDown = 0, countTwo = 0;

        // 竖直方向上判断
        while (true) {
            y--;
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else if ((x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == matchRole) || y < 0) {
                up++;
                break;
            } else {
                break;
            }
        }
        y = startY;
        while (true) {
            y++;
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else if ((x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == matchRole) || y > 19) {
                down++;
                break;
            } else {
                break;
            }
        }
        if (count == 2 && (up + down == 0)) {
            countTwo++;
        }
        mark(count, up + down, countTwo, role);

        // 水平方向判断
        x = startX;
        y = startY;
        count = 0;
        while (true) {
            x--;
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else if ((x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == matchRole) || x == 0) {
                left++;
                break;
            } else {
                break;
            }
        }
        x = startX;
        while (true) {
            x++;
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else if ((x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == matchRole) || x > 19) {
                right++;
                break;
            } else {
                break;
            }
        }
        if (count == 2 && (left + right == 0)) {
            countTwo++;
        }
        mark(count, left + right, countTwo, role);

        // 右倾斜方向判断
        x = startX;
        y = startY;
        count = 0;
        while (true) {
            y--;
            x--;
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else if ((x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == matchRole) || x < 0 || y < 0) {
                leftUp++;
                break;
            } else {
                break;
            }
        }
        x = startX;
        y = startY;
        while (true) {
            x++;
            y++;
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else if ((x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == matchRole) || x > 19 || y > 19) {
                rightDown++;
                break;
            } else {
                break;
            }
        }
        if (count == 2 && (leftUp + rightDown == 0)) {
            countTwo++;
        }
        mark(count, leftUp + rightDown, countTwo, role);

        // 左倾斜方向判断
        x = startX;
        y = startY;
        count = 0;
        while (true) {
            x--;
            y++;
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else if ((x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == matchRole) || x < 0 || y > 19) {
                leftDown++;
                break;
            } else {
                break;
            }
        }
        x = startX;
        y = startY;
        while (true) {
            x++;
            y--;
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else if ((x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == matchRole) || x > 19 || y < 0) {
                rightUp++;
                break;
            } else {
                break;
            }
        }
        if (count == 2 && (leftDown + rightUp == 0)) {
            countTwo++;
        }
        mark(count, leftDown + rightUp, countTwo, role);
    }
}
