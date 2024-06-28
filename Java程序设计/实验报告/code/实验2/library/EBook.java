package library;

public class EBook extends Book {
    private String downloadLink;
    public static String format;

    // 接收书名、作者和下载链接的构造方法
    public EBook(String title, String author, String downloadLink) {
        super(title, author);
        this.downloadLink = downloadLink;
        System.out.println("EBook 类的构造方法被调用");
    }

    // 覆盖displayInfo()方法
    @Override
    public void displayInfo() {
        super.displayInfo();
        System.out.println("下载链接: " + downloadLink + ", 格式: " + format);
    }
}
