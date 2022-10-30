// Компиляция
    // javac Console.java
// Выполнение java
    // java Console

import java.util.Scanner;

public class Console{
    public static boolean isNumeric(String str) {
        try {
            Double.parseDouble(str);
            return true;
        } catch(NumberFormatException e){
            return false;
        }
    }

    public static void main(String args[]){
        Scanner console = new Scanner(System.in);
        
        String val = console.nextLine();
        
        Console ConsoleClass = new Console();
        
        if (ConsoleClass.isNumeric(val)){
            int valInt = Integer.parseInt(val);
            valInt += 1;
            System.out.println("Integer: " + valInt);
        }else{
            System.out.println("Line: " + val + '!');
        }
    }
}
