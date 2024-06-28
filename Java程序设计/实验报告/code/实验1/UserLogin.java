import java.util.Scanner;

public class UserLogin {
    public static void main(String[] args) {
        // 预设的用户名和密码
        String username = "user";
        String password = "pass";
        // 创建Scanner对象来接收用户输入
        Scanner scanner = new Scanner(System.in);
        // 提示用户输入用户名和密码
        System.out.print("请输入用户名：");
        String inputUsername = scanner.nextLine();
        System.out.print("请输入密码：");
        String inputPassword = scanner.nextLine();
        // 检查用户名和密码是否匹配
        if (inputUsername.equals(username) && inputPassword.equals(password)) {
            System.out.println("登录成功");
        } else {
            System.out.println("登录失败");
        }
        // 关闭Scanner对象
        scanner.close();
    }
}
