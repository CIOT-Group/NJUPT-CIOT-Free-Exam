<div align="center">

# Java 第三次作业

</div>

## 题目

1. Java 提供了哪些接口和类实现多线程机制？各有什么作用？怎样启动一个线程？
2. 什么是交互线程?什么是线程互斥与同步？说明线程互斥与同步机制怎样保证交互线程对共享变量操作的正确性，不产生与时间有关的错误。

## 解答

### 1. Java 提供了哪些接口和类实现多线程机制？各有什么作用？怎样启动一个线程？

Java 提供了多种接口和类来实现多线程机制，主要包括 `Thread` 类和 `Runnable` 接口：

#### `Thread` 类

- **作用**：`Thread` 类本身就是一个线程的实现类。通过继承 `Thread` 类，可以创建一个新的线程。
- **用法**：继承 `Thread` 类并重写其 `run()` 方法。在 `run()` 方法中定义线程执行的任务。

#### `Runnable` 接口

- **作用**：`Runnable` 接口是一个功能性接口，用于定义线程执行的任务。相比继承 `Thread` 类，实现 `Runnable` 接口是一种更灵活的方式，因为 Java 是单继承模型。
- **用法**：实现 `Runnable` 接口并重写其 `run()` 方法。在 `run()` 方法中定义线程执行的任务。然后，将该实现传递给 `Thread` 对象并启动线程。

#### 启动一个线程的方法

1. **通过继承 `Thread` 类**：

   ```java
   class MyThread extends Thread {
       public void run() {
           System.out.println("Thread is running");
       }
   }

   public class Main {
       public static void main(String[] args) {
           MyThread t1 = new MyThread();
           t1.start();  // 启动线程
       }
   }
   ```

2. **通过实现 `Runnable` 接口**：

   ```java
   class MyRunnable implements Runnable {
       public void run() {
           System.out.println("Thread is running");
       }
   }

   public class Main {
       public static void main(String[] args) {
           MyRunnable myRunnable = new MyRunnable();
           Thread t1 = new Thread(myRunnable);
           t1.start();  // 启动线程
       }
   }
   ```

### 2. 什么是交互线程?什么是线程互斥与同步？说明线程互斥与同步机制怎样保证交互线程对共享变量操作的正确性，不产生与时间有关的错误。

#### 交互线程

交互线程指的是多个线程之间进行交互和通信的情况，通常需要共享数据或资源。在多线程编程中，线程的交互需要小心处理，以避免竞争条件和其他同步问题。

#### 线程互斥

线程互斥指的是确保在任何时刻只有一个线程能够访问某个特定的共享资源或代码块。常见的实现方式包括使用 `synchronized` 关键字和 `Lock` 接口。

#### 线程同步

线程同步是指协调多个线程的执行顺序，以保证共享数据的正确性。同步可以防止多个线程同时访问和修改共享变量，从而避免不一致性和竞争条件。

#### 线程互斥与同步机制的保证

通过互斥和同步机制，可以确保多个线程对共享变量的操作是原子性的，即这些操作要么全部完成，要么全部不完成，从而避免了因线程交替执行引起的时间相关错误（如竞争条件）。具体来说：

- **原子性**：通过互斥锁（如 `synchronized` 或 `Lock`），确保每次只有一个线程可以进入临界区，从而避免多个线程同时修改共享变量，保证操作的原子性。
- **可见性**：同步机制还可以确保变量的修改对其他线程是可见的，避免了缓存导致的可见性问题。
- **有序性**：通过同步块，可以确保代码块的执行顺序按照预期进行，避免指令重排导致的并发问题。

#### 互斥与同步机制的实现

1. **`synchronized` 关键字**：

   ```java
   class Counter {
       private int count = 0;

       public synchronized void increment() {
           count++;
       }

       public int getCount() {
           return count;
       }
   }
   ```

2. **`Lock` 接口**：

   ```java
   import java.util.concurrent.locks.Lock;
   import java.util.concurrent.locks.ReentrantLock;

   class Counter {
       private int count = 0;
       private final Lock lock = new ReentrantLock();

       public void increment() {
           lock.lock();
           try {
               count++;
           } finally {
               lock.unlock();
           }
       }

       public int getCount() {
           return count;
       }
   }
   ```
