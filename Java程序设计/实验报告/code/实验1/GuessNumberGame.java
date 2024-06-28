import java.util.Random;
import java.util.Scanner;

public class GuessNumberGame {
    public static void main(String[] args) {
        // 随机生成目标数字（1到100之间的整数）
        Random random = new Random();
        int targetNumber = random.nextInt(100) + 1;

        // 创建Scanner对象来接收用户输入
        Scanner scanner = new Scanner(System.in);

        // 初始化猜测次数计数器
        int guessCount = 0;

        // 开始游戏循环
        while (true) {
            // 提示用户输入猜测的数字
            System.out.print("请输入你猜测的数字（1-100）：");
            int guess = scanner.nextInt();

            // 猜测次数加一
            guessCount++;

            // 检查用户猜测的数字与目标数字的关系
            if (guess > targetNumber) {
                System.out.println("太大了");
            } else if (guess < targetNumber) {
                System.out.println("太小了");
            } else {
                System.out.println("恭喜，猜对了！");
                break; // 猜对了，退出循环
            }
        }

        // 输出猜测次数
        System.out.println("你猜了" + guessCount + "次");

        // 关闭Scanner对象
        scanner.close();
    }
}
