import java.util.Scanner;

public class UserInput {
   public static void main(String[] args) {
       Scanner scanner = new Scanner(System.in);
       System.out.println("请输入多个数字，以空格分隔：");
       String input = scanner.nextLine();
       String[] numbers = input.split(" ");
       int sum = 0;
       for (String number : numbers) {
           sum += Integer.parseInt(number);
       }
       System.out.println("输入的数字之和为：" + sum);
       scanner.close();
   }
}

