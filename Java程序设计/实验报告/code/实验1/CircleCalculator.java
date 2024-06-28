import java.util.Scanner;

public class CircleCalculator {
    public static void main(String[] args) {
        // 创建一个Scanner对象，用于接收用户输入
        Scanner scanner = new Scanner(System.in);
        // 输出提示信息，提示用户输入圆的半径
        System.out.print("请输入圆的半径：");
        // 接收用户输入的半径值，并将其存储在radius变量中
        double radius = scanner.nextDouble();
        // 定义一个常量，表示圆周率
        final double PI = 3.14159;
        // 计算圆的面积
        double area = PI * radius * radius;
        // 计算圆的周长
        double circumference = 2 * PI * radius;
        // 输出圆的面积
        System.out.println("圆的面积为：" + area);
        // 输出圆的周长
        System.out.println("圆的周长为：" + circumference);
        // 关闭Scanner对象
        scanner.close();
    }
}
