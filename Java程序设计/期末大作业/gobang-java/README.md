<div align="center">

# Gobang-Java

![GitHub](https://img.shields.io/github/license/SUC-DriverOld/gobang-java)
![GitHub](https://img.shields.io/github/languages/top/SUC-DriverOld/gobang-java)
![GitHub](https://img.shields.io/github/repo-size/SUC-DriverOld/gobang-java)
![GitHub](https://img.shields.io/github/release/SUC-DriverOld/gobang-java)

gobang-java 使用 java swing 实现的五子棋，目前有人机对战模式和双人对战模式\
项目用于：B22080415 南京邮电大学《java 程序设计》课程大作业\
如需simple版本（仅有人机对战功能），请切换到[simple](https://github.com/SUC-DriverOld/gobang-java/tree/simple)分支

</div>

## 快速开始

从[Release](https://github.com/SUC-DriverOld/gobang-java/releases)下载打包发布的版本。

## 开发

1. 下载 JDK1.8 并添加到环境变量
2. 克隆本仓库

   ```bash
   git clone https://github.com/SUC-DriverOld/gobang-java.git
   ```

3. 从`src\View\SelectMenu.java`启动

> [!WARNING]
> 从`.jar`启动时请在同级目录下添加`src/images`文件夹，否则会出现找不到图片的错误。例如：

```bash
gobang
│ gobang.jar
└─src
    └─images
         black.png
         ...
```

## 致谢

- [Swing](https://docs.oracle.com/javase/tutorial/uiswing/index.html)
- [Avidel](https://github.com/avidele)
