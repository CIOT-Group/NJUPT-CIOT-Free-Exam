<div align="center">

# Java 第二次作业

</div>

## 题目

1. 声明银行账户类 Account，成员变量包括账号、储户姓名、开户时间、身份证号码、存款余额等账户信息，成员方法包括开户、存款、取款、查询（余额、明细）、销户等操作。
2. 说明接口与抽象类的区别。
3. Java API 采用什么组织方式？默认导入的包是什么？
4. Java 为什么需要声明基本数据类型的包装类？基本数据类型的包装类有哪些？

## 解答

1. 题目 1 代码：

   ```java
   public class Account {
      private String accountNumber;       // 账号
      private String accountHolderName;   // 储户姓名
      private Date openingDate;           // 开户时间
      private String idNumber;            // 身份证号码
      private double balance;             // 账户余额

      // 开户
      public void openAccount(String accountNumber, String accountHolderName, Date openingDate, String idNumber, double balance)
      // 存款
      public void deposit(String accountNumber, double amount)
      // 取款
      public void withdraw(String accountNumber, double amount)
      // 查询余额
      public double getBalance()
      // 查询明细
      public void printAccountDetails(String accountNumber)
      // 销户
      public void closeAccount(String accountNumber)
   }
   ```

2. 区别：

   a. **方法实现**：

   - 接口中的方法都是抽象的，不包含方法的实现。接口中的方法默认为`public abstract`。
   - 抽象类可以包含抽象方法和普通方法，可以有部分方法的实现。抽象方法用`abstract`关键字修饰，普通方法可以有具体的实现。

   b. **多继承**：

   - 一个类可以实现多个接口，通过`implements`关键字实现。
   - Java 中不支持多继承，一个类只能继承一个抽象类，但可以实现多个接口。

   c. **构造器**：

   - 接口不能有构造器，因为接口不能被实例化。
   - 抽象类可以有构造器，但抽象类本身不能被实例化。

   d. **成员变量**：

   - 接口中只能包含常量，不能包含非常量的成员变量。
   - 抽象类中可以包含非常量的成员变量。

   f. **设计目的**：

   - 接口主要用于定义一组行为，而不关心实现的细节，通过接口可以实现多态性。
   - 抽象类则用于定义一类对象的通用特性，并提供一些默认的实现。

3. Java API 采用了包的组织方式。包是一种命名空间，用于组织和管理相关的类和接口。Java API 中的类和接口按功能和用途被组织成不同的包。默认 Java 会自动导入`java.lang`包。
4. Java 声明基本数据类型的包装类是为了将基本数据类型转换为对象，从而使其具有对象的特性和功能。能够提供对象化的操作，提供空值表示，与泛型的兼容，并且支持面向对象的编程。

   基本数据类型的包装类如下：

   - `Boolean`：对应`boolean`类型
   - `Byte`：对应`byte`类型
   - `Short`：对应`short`类型
   - `Integer`：对应`int`类型
   - `Long`：对应`long`类型
   - `Float`：对应`float`类型
   - `Double`：对应`double`类型
