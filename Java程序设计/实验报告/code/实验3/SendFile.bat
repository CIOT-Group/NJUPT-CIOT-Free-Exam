@echo off
chcp 65001

Java .\FileClient.java .\send_files\test01.txt
Java .\FileClient.java .\send_files\test02.csv

pause
