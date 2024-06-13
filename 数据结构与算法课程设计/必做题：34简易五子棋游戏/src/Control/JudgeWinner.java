package Control;

public class JudgeWinner {
    /**
     * 判断当前玩家是否获胜
     *
     * @param x 当前棋子所在的横坐标
     * @param y 当前棋子所在的纵坐标
     * @param chess 当前棋盘的状态，19x19的二维数组
     * @param role 当前玩家的角色（例如1代表黑子，2代表白子）
     * @return 如果当前玩家获胜，则返回角色编号；如果没有玩家获胜，则返回0
     */
    public static int PPJudge(int x, int y, int[][] chess, int role) {
        int startX = x, startY = y, count = 1;

        // 竖直方向上判断输赢
        // 向上判断
        while (true) {
            y--;
            // 检查棋子是否在棋盘内且与当前角色一致
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else {
                break;
            }
        }
        y = startY; // 恢复原始位置
        // 向下判断
        while (true) {
            y++;
            // 检查棋子是否在棋盘内且与当前角色一致
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else {
                break;
            }
        }
        // 判断是否形成5个连续的棋子
        if (count >= 5) {
            return role;
        }

        // 水平方向判断输赢
        x = startX;
        y = startY;
        count = 1;
        // 向左判断
        while (true) {
            x--;
            // 检查棋子是否在棋盘内且与当前角色一致
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else {
                break;
            }
        }
        x = startX; // 恢复原始位置
        // 向右判断
        while (true) {
            x++;
            // 检查棋子是否在棋盘内且与当前角色一致
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else {
                break;
            }
        }
        // 判断是否形成5个连续的棋子
        if (count >= 5) {
            return role;
        }

        // 右倾斜方向判断输赢
        x = startX;
        y = startY;
        count = 1;
        // 向左上判断
        while (true) {
            y--;
            x--;
            // 检查棋子是否在棋盘内且与当前角色一致
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else {
                break;
            }
        }
        x = startX;
        y = startY; // 恢复原始位置
        // 向右下判断
        while (true) {
            x++;
            y++;
            // 检查棋子是否在棋盘内且与当前角色一致
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else {
                break;
            }
        }
        // 判断是否形成5个连续的棋子
        if (count >= 5) {
            return role;
        }

        // 左倾斜方向判断输赢
        x = startX;
        y = startY;
        count = 1;
        // 向左下判断
        while (true) {
            x--;
            y++;
            // 检查棋子是否在棋盘内且与当前角色一致
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else {
                break;
            }
        }
        x = startX;
        y = startY; // 恢复原始位置
        // 向右上判断
        while (true) {
            x++;
            y--;
            // 检查棋子是否在棋盘内且与当前角色一致
            if (x >= 0 && x < 19 && y >= 0 && y < 19 && chess[x][y] == role) {
                count++;
            } else {
                break;
            }
        }
        // 判断是否形成5个连续的棋子
        if (count >= 5) {
            return role;
        }

        // 如果没有玩家获胜，返回0
        return 0;
    }
}
