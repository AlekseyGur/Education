package ru.alexgur;

// Компиляция
    // mkdir classes
    // javac -classpath ./classes -d ./classes HelloWorld.java
// Выполнение java
    // java -classpath ./classes ru.alexgur.HelloWorld
// Создание архива jar
    // Файл манифеста "manifest.mf"
        // $ cat > manifest.mf
        // Manifest-Version: 1.0
        // Created-By: 0.0.1 (alexgur.ru Inc)
        // Main-Class: ru.alexgur.HelloWorld
        
        // Можно подключить jar файлы из папок строкой:
            // Class-Path: lib/velocity-1.4.jar lib/log4j-1.2.8.jar

    // Файл Jar
        // jar cvmf manifest.mf hellowWorld.jar -C ./classes/ .
// Выполнение jar
    // java -jar hellowWorld.jar


public class HelloWorld{
    public static void main(String args[]){
        System.out.println("Hello, World!");
    }
}
