package Model;

import javax.swing.*;

/**
 * timerThread 类用于在 JLabel 上显示计时器。该线程会定期更新 JLabel 显示的时间。
 */
public class timerThread extends Thread {
    // 用于显示时间的 JLabel 组件
    private final JLabel label;

    /**
     * 构造函数，初始化 timerThread 实例。
     *
     * @param label 用于显示时间的 JLabel 组件
     */
    public timerThread(JLabel label) {
        this.label = label;
    }

    /**
     * 线程的运行方法，启动计时器并定期更新 JLabel 上的时间显示。
     */
    public void run() {
        // 记录计时器开始的时间
        long startTime = System.currentTimeMillis();

        // 持续更新时间，直到线程被中断
        do {
            // 获取当前时间
            long currentTime = System.currentTimeMillis();

            // 计算经过的时间
            long time = currentTime - startTime;

            // 格式化经过的时间并更新 JLabel 的文本
            label.setText(format(time));
        } while (!this.isInterrupted());
    }

    /**
     * 格式化经过的时间，将毫秒转换为 HH:mm:ss 格式的字符串。
     *
     * @param elapsed 经过的时间，单位为毫秒
     * @return 格式化后的时间字符串，格式为 HH:mm:ss
     */
    private String format(long elapsed) {
        int hour, minute, second;

        // 将毫秒转换为秒
        elapsed = elapsed / 1000;

        // 计算秒
        second = (int) (elapsed % 60);
        elapsed = elapsed / 60;

        // 计算分钟
        minute = (int) (elapsed % 60);
        elapsed = elapsed / 60;

        // 计算小时
        hour = (int) (elapsed % 60);

        // 返回格式化后的时间字符串
        return String.format("%02d:%02d:%02d", hour, minute, second);
    }
}
