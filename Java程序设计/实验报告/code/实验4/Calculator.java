import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Calculator extends JFrame implements ActionListener {

    public static void main(String[] args) {
        new Calculator();
    }

    // 定义组件
    private JTextField display; // 显示文本框
    private JTextArea history; // 历史记录文本区域
    private JButton[] buttons; // 按钮数组
    private String[] buttonLabels = {
            "7", "8", "9", "÷",
            "4", "5", "6", "×",
            "1", "2", "3", "-",
            ".", "0", "=", "+",
    }; // 按钮标签数组
    private JPanel panel; // 面板

    // 定义计算变量
    private double num1 = 0, num2 = 0, result = 0;
    private char operator; // 运算符
    private boolean operatorEntered = false; // 是否已经输入运算符

    public Calculator() {
        // 设置JFrame
        this.setTitle("Calculator");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // 设置关闭窗口时的操作
        this.setSize(420, 550); // 设置窗口大小
        this.setResizable(false); // 禁止调整窗口大小
        this.setLayout(null); // 绝对布局

        // 初始化显示文本框
        display = new JTextField();
        display.setBounds(50, 25, 300, 50); // 设置文本框位置和大小
        display.setFont(new Font("Arial", Font.PLAIN, 24)); // 设置字体样式和大小
        display.setEditable(false); // 设置文本框不可编辑
        display.setHorizontalAlignment(JTextField.RIGHT); // 设置数字显示靠右

        // 初始化历史记录文本区域
        history = new JTextArea();
        history.setBounds(50, 80, 300, 25); // 设置文本位置和大小
        history.setFont(new Font("Arial", Font.PLAIN, 20)); // 设置字体样式和大小
        history.setEditable(false); // 设置文本区域不可编辑
        history.setOpaque(false); // 设置文本区域底色为透明
        history.setBorder(null); // 移除文本区域边框
        history.setLineWrap(true); // 设置自动换行
        history.setWrapStyleWord(true); // 设置自动换行并保持单词完整性

        // 初始化按钮
        buttons = new JButton[buttonLabels.length];
        for (int i = 0; i < buttonLabels.length; i++) {
            buttons[i] = new JButton(buttonLabels[i]);
            buttons[i].addActionListener(this);
            buttons[i].setFont(new Font("Arial", Font.PLAIN, 24)); // 设置按钮字体样式和大小
            buttons[i].setFocusable(false); // 禁止按钮获得焦点
            if (buttonLabels[i].matches("[÷×\\-+]")) {
                buttons[i].setBackground(Color.ORANGE); // 设置四则运算按钮为橙色
            } else {
                buttons[i].setBackground(Color.LIGHT_GRAY); // 设置其他按钮为灰色
            }
        }

        // 创建面板并设置布局
        panel = new JPanel();
        panel.setBounds(50, 120, 300, 300);
        panel.setLayout(new GridLayout(4, 4, 10, 10)); // 设置面板为4x4的网格布局，并设置水平和垂直间距

        // 将按钮添加到面板
        for (JButton button : buttons) {
            panel.add(button);
        }

        // 将组件添加到JFrame
        this.add(display);
        this.add(history);
        this.add(panel);

        // 设置Del按钮
        JButton delButton = new JButton("Del");
        delButton.setBounds(50, 430, 145, 50);
        delButton.setFont(new Font("Arial", Font.PLAIN, 24));
        delButton.setFocusable(false); // 禁止按钮获得焦点
        delButton.setBackground(Color.LIGHT_GRAY); // 设置按钮底色为灰色
        delButton.addActionListener(this); // 添加按钮点击事件监听器
        this.add(delButton);

        // 设置Clr按钮
        JButton clrButton = new JButton("Clr");
        clrButton.setBounds(205, 430, 145, 50);
        clrButton.setFont(new Font("Arial", Font.PLAIN, 24));
        clrButton.setFocusable(false); // 禁止按钮获得焦点
        clrButton.setBackground(Color.LIGHT_GRAY); // 设置按钮底色为灰色
        clrButton.addActionListener(this); // 添加按钮点击事件监听器
        this.add(clrButton);

        this.setVisible(true); // 显示窗口
    }

    // 按钮点击事件处理
    @Override
    public void actionPerformed(ActionEvent e) {
        // 获取按下的命令
        String command = e.getActionCommand();
        // 如果命令是数字或小数点，则直接显示
        if ((command.charAt(0) >= '0' && command.charAt(0) <= '9') || command.equals(".")) {
            if (operatorEntered) {
                display.setText(""); // 如果已经有操作符，则清空显示框
                operatorEntered = false; // 重置操作符已输入
            }
            display.setText(display.getText().concat(command)); // 显示命令
            // 如果命令是删除，则删除显示框的最后一位
        } else if (command.equals("Del")) {
            String text = display.getText();
            display.setText(""); // 清空显示框
            for (int i = 0; i < text.length() - 1; i++) { // 从第一位开始，逐位显示
                display.setText(display.getText() + text.charAt(i));
            }
            // 如果命令是清除，则清空显示框和计算历史
        } else if (command.equals("Clr")) {
            display.setText(""); // 清空显示框
            history.setText(""); // 清空计算历史
            // 如果命令是等于，则执行计算并将结果显示在显示框
        } else if (command.equals("=")) {
            num2 = Double.parseDouble(display.getText()); // 获取数字
            switch (operator) { // 执行相应的运算
                case '+':
                    result = num1 + num2;
                    break;
                case '-':
                    result = num1 - num2;
                    break;
                case '×':
                    result = num1 * num2;
                    break;
                case '÷':
                    result = num1 / num2;
                    break;
            }
            history.setText(num1 + " " + operator + " " + num2 + " = "); // 记录运算历史
            if (result == (int) result) { // 如果结果是整数，则显示整数
                display.setText(Integer.toString((int) result));
            } else { // 否则显示浮点数
                display.setText(Double.toString(result));
            }
            num1 = result; // 重置数字
            // 如果命令是操作符，则记录显示框的内容，并重置操作符已输入
        } else {
            if (!display.getText().isEmpty()) { // 如果显示框有内容
                if (!operatorEntered) { // 如果操作符未输入
                    history.setText(display.getText() + " " + command + "\n"); // 记录运算历史
                    operatorEntered = true; // 重置操作符已输入
                }
                num1 = Double.parseDouble(display.getText()); // 获取数字
                operator = command.charAt(0); // 获取操作符
                display.setText(""); // 清空显示框
            }
        }
    }
}
