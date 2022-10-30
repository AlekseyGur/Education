// Компиляция
    // javac Loops.java
// Выполнение java
    // java Loops

public class Loops {
    public static void main(String args[]){
        String[] fruits = new String[] {
            "Orange",
            "Apple",
            "Pear",
            "Strawberry"
        };

        for (String fruit : fruits) {
            System.out.println("fruit: " + fruit);
        }
        
        Arrays.fill(x, 3, 7, 999);
        System.out.println( Arrays.toString(fruits) );
        
        boolean isExit = false;
        while (!isExit)
        {
            String s = "exit";
            isExit = s.equals("exit");
            System.out.println("exit while");
        }
    }
}
