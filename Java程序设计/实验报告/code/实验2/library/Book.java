package library;

public class Book {
    private String title;
    private String author;

    // 无参构造方法
    public Book() {
        System.out.println("Book 类的无参构造方法被调用");
    }

    // 接收书名和作者的构造方法
    public Book(String title, String author) {
        this.title = title;
        this.author = author;
        System.out.println("Book 类的有参构造方法被调用");
    }

    // 显示书名和作者的方法
    public void displayInfo() {
        System.out.println("书名: " + title + ", 作者: " + author);
    }
}
