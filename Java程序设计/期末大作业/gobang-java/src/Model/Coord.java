package Model;

/**
 * Coord 类用于表示棋盘上的一个坐标点。
 */
public class Coord {
    // 坐标的横坐标（列）
    private int x;

    // 坐标的纵坐标（行）
    private int y;

    /**
     * 设置坐标的横坐标值。
     *
     * @param x 新的横坐标值
     */
    public void setX(int x) {
        this.x = x;
    }

    /**
     * 设置坐标的纵坐标值。
     *
     * @param y 新的纵坐标值
     */
    public void setY(int y) {
        this.y = y;
    }

    /**
     * 获取坐标的横坐标值。
     *
     * @return 当前的横坐标值
     */
    public int getX() {
        return x;
    }

    /**
     * 获取坐标的纵坐标值。
     *
     * @return 当前的纵坐标值
     */
    public int getY() {
        return y;
    }
}
