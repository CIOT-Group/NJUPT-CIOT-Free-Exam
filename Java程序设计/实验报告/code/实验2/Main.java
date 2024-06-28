import library.EBook;

public class Main {
    public static void main(String[] args) {
        // 设置电子书的格式
        EBook.format = "PDF";

        // 创建EBook对象
        EBook ebook1 = new EBook("Java 编程思想", "Bruce Eckel", "http://example.com/java");
        ebook1.displayInfo();
        System.out.println("");

        // 修改静态成员format的值
        EBook.format = "EPUB";

        // 创建另一个EBook对象
        EBook ebook2 = new EBook("Effective Java", "Joshua Bloch", "http://example.com/effectivejava");
        ebook2.displayInfo();
        System.out.println("");

        // 再次调用第一个EBook对象的displayInfo()方法
        ebook1.displayInfo();
    }
}
