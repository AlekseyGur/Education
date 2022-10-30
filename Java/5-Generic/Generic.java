// Компиляция
    // javac Generic.java
// Выполнение java
    // java Generic

// лучшее объяснение дженериков: https://www.youtube.com/watch?v=K1iu1kXkVoA    

public class Generic {
    public static void Generic(String []args) {
        Printer<Integer> printer = new Printer<>(23);
        printer.print();
        
        Printer<Double> doublePrinter = new Printer<>(33.5);
        doublePrinter.print();
        
        Printer<Cat> cats = new Printer<>(23);
        cats.add(new Cat());
        
        Printer<Cat> printer = new Printer<>(new Cat());
        printer.print();
        
        shout("John");
        shout(50);
        shout(new Cat);
        
        List<Integer> intList = new ArrayList<>();
        intList.add(3);
        printList(intList);
        
        List<Cat> catList = new ArrayList<>();
        catList.add(new Cat());
        printList(catList);
    }
    
    public static <T, V> void shout(T thingToShout, V otherThing) {
        // Если не поставить <T>, то жава скажет, что не знает такого типа "T", который указан в аргументе shout(T thingToShout).
        // Вместо Т можно указать любое своё название типа
        // В аргументам может быть несколько произвоьлных типов, тогда их надо записывать через запятую <T, V>
        System.out.println(thingToShout + "!!!!");
        System.out.println(otherThing + "!!!!");
    }
    
    // если нужно указать ещё возвращаемое значение в виде произвольного типа, то перепишем вместо void название типа без скобок
    public static <T> T shout(T thingToShout) {
        System.out.println(thingToShout + "!!!!");
        
        return thingToShout;
    }
    
    private static void printList(List<?> mylist) {
        // чтобы принимать списки, состоящие из любых типов, ставят значок <?>. Называется wildcard "подстановочный знак"
        // можно добавить "<? extends Animal>", чтобы использовать именно тип, который выходит из Animal
        System.out.println(mylist);
    }
    
}

public class Printer <T extends Animal & Serializable> {
    // Вместо "Т" можно написать любое слово, которое будет обозначать тип, с которым работает класс
    // Необязательная фараза "extends Animal" означает то, что в T должен быть объектом класса Animal и можно применять методы в нём из этого класса
    // Можно работать сразу с класс и интерфейс, указав их через &: "extends Animal & Serializable". Но интерфейс должен стоять последним!
    T thingToPrint;
    
    public Printer(T thingToPrint) {
        this.thingToPrint = thingToPrint;
    }
    
    public void print() {
        System.out.println(thingToPrint);
    }
}

// если нужно нескольк типов, которые обрабатывает класс, то пишем:
public class Printer <T, V> {
    T thingToPrint;
    V thingToPrint;
    
    public Printer(T thingToPrint) {
        this.thingToPrint = thingToPrint;
    }
    
    public void print() {
        System.out.println(thingToPrint);
    }
}
